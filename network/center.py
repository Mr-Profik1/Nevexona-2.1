"""Network Center: Wi-Fi (NetworkManager/nmcli) и Bluetooth (bluetoothctl). Без shell, пароли не логируются."""
import re, subprocess

def _run(argv, runner=None):
    return (runner or subprocess.run)(argv, capture_output=True, text=True, shell=False, check=False)

def _split_terse(line):
    parts, cur, esc = [], "", False
    for ch in line:
        if esc: cur += ch; esc = False
        elif ch == "\\": esc = True
        elif ch == ":": parts.append(cur); cur = ""
        else: cur += ch
    return parts + [cur]

def parse_wifi(text):
    nets = {}
    for line in text.splitlines():
        p = _split_terse(line)
        if len(p) < 3 or not p[0]:
            continue
        n = {"ssid": p[0], "signal": int(p[1] or 0), "security": p[2] or "открытая"}
        if p[0] not in nets or n["signal"] > nets[p[0]]["signal"]:
            nets[p[0]] = n
    return sorted(nets.values(), key=lambda x: -x["signal"])

def wifi_list(runner=None):
    r = _run(["nmcli", "-t", "-f", "SSID,SIGNAL,SECURITY", "dev", "wifi", "list", "--rescan", "yes"], runner)
    return parse_wifi(r.stdout)

def wifi_connect(ssid, password=None, runner=None):
    if not ssid or ssid.startswith("-") or "\n" in ssid:
        raise ValueError("недопустимое имя сети")
    argv = ["nmcli", "dev", "wifi", "connect", ssid] + (["password", password] if password else [])
    r = _run(argv, runner)
    return {"ok": r.returncode == 0, "message": "Подключено" if r.returncode == 0 else "Ошибка подключения (проверьте пароль)"}

def wifi_disconnect(runner=None):
    return _run(["nmcli", "radio", "wifi", "off"], runner)

MAC = re.compile(r"^([0-9A-F]{2}:){5}[0-9A-F]{2}$", re.I)

def parse_bt(text):
    out = []
    for line in text.splitlines():
        m = re.match(r"^Device ((?:[0-9A-F]{2}:){5}[0-9A-F]{2}) (.*)$", line.strip(), re.I)
        if m: out.append({"mac": m[1].upper(), "name": m[2]})
    return out

def bt_devices(runner=None):
    return parse_bt(_run(["bluetoothctl", "devices"], runner).stdout)

def bt_action(action, mac=None, runner=None):
    if action not in {"power-on", "power-off", "scan-on", "scan-off", "pair", "connect", "disconnect", "remove"}:
        raise ValueError("неизвестное действие")
    if action.startswith(("pair", "connect", "disconnect", "remove")):
        if not mac or not MAC.match(mac):
            raise ValueError("недопустимый MAC")
    cmd = {"power-on": ["power", "on"], "power-off": ["power", "off"], "scan-on": ["--timeout", "8", "scan", "on"],
           "scan-off": ["scan", "off"]}.get(action, [action, mac])
    return _run(["bluetoothctl", *cmd], runner)
