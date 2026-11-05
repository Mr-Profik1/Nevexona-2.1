#!/usr/bin/env python3
"""Driver Center: обнаружение PCI-устройств (lspci -nnk) и подбор официальных Debian-пакетов.
Ничего не устанавливает сам: только показывает состояние и предложения."""
import re, subprocess

# vendor-id -> (производитель, пакет firmware из Debian non-free-firmware или None)
VENDORS = {
    "10de": ("NVIDIA", None),          # проприетарный драйвер: только по выбору пользователя
    "1002": ("AMD", "firmware-amd-graphics"),
    "8086": ("Intel", None),
    "10ec": ("Realtek", "firmware-realtek"),
    "14e4": ("Broadcom", "firmware-brcm80211"),
    "168c": ("Qualcomm Atheros", "firmware-atheros"),
    "14c3": ("MediaTek", "firmware-mediatek"),
}
_HDR = re.compile(r"^(\S+) (.+?) \[([0-9a-f]{4})\]: (.+?) \[([0-9a-f]{4}):([0-9a-f]{4})\]")

def parse_lspci(text):
    devs, cur = [], None
    for line in text.splitlines():
        m = _HDR.match(line)
        if m:
            cur = {"slot": m[1], "class": m[2], "name": m[4], "vendor_id": m[5], "device_id": m[6], "driver": None}
            devs.append(cur)
        elif cur and line.strip().startswith("Kernel driver in use:"):
            cur["driver"] = line.split(":", 1)[1].strip()
    for d in devs:
        v = VENDORS.get(d["vendor_id"])
        d["vendor"] = v[0] if v else "Неизвестно"
        d["firmware_pkg"] = v[1] if v else None
        d["status"] = "OK" if d["driver"] else "Нет драйвера"
        # Intel Wi-Fi требует firmware-iwlwifi
        if d["vendor_id"] == "8086" and "network" in d["class"].lower() and not d["driver"]:
            d["firmware_pkg"] = "firmware-iwlwifi"
    return devs

def scan():
    out = subprocess.run(["lspci", "-nnk"], capture_output=True, text=True, check=False).stdout
    return parse_lspci(out)

if __name__ == "__main__":
    for d in scan():
        print(f"{d['vendor']:<18} {d['name'][:48]:<48} {d['driver'] or '-':<12} {d['status']}")
