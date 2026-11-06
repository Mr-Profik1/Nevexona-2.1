"""Профили производительности (из ТЗ): меняют только безопасные необязательные вещи.
Безопасность, сеть и системные службы не отключаются."""
import json, os

PROFILES = {
    "ULTRA LOW": {"min_ram_gb": 0, "autostart_off": ["nm-applet-extras", "tray-widgets"], "animations": False, "swappiness": 100},
    "LOW": {"min_ram_gb": 1.5, "autostart_off": ["tray-widgets"], "animations": False, "swappiness": 100},
    "NORMAL": {"min_ram_gb": 3.5, "autostart_off": [], "animations": True, "swappiness": 60},
    "PERFORMANCE": {"min_ram_gb": 7, "autostart_off": [], "animations": True, "swappiness": 30},
    "GAMING": {"min_ram_gb": 15, "autostart_off": [], "animations": True, "swappiness": 10},
}
FORBIDDEN = {"networkmanager", "systemd", "polkit", "clamav", "ufw", "apparmor"}

def recommend(ram_bytes):
    gb = ram_bytes / 2**30
    best = "ULTRA LOW"
    for name, p in PROFILES.items():
        if gb >= p["min_ram_gb"]:
            best = name
    return best

def save(name, path):
    if name not in PROFILES:
        raise ValueError("неизвестный профиль")
    for a in PROFILES[name]["autostart_off"]:
        if a.lower() in FORBIDDEN:
            raise PermissionError("нельзя отключать системную службу")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump({"profile": name, **PROFILES[name]}, open(path, "w"), ensure_ascii=False, indent=1)
    return PROFILES[name]
