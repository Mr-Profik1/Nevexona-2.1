"""Laptop Center: батарея и яркость из /sys. Данные есть не на всех устройствах — честно сообщаем об отсутствии."""
import glob, os

def _read(p, default=None):
    try: return open(p).read().strip()
    except OSError: return default

def battery(root="/sys/class/power_supply"):
    for d in sorted(glob.glob(os.path.join(root, "BAT*"))):
        cap = _read(d + "/capacity"); st = _read(d + "/status", "Unknown")
        full, design = _read(d + "/energy_full") or _read(d + "/charge_full"), _read(d + "/energy_full_design") or _read(d + "/charge_full_design")
        health = round(int(full) * 100 / int(design)) if full and design and int(design) else None
        return {"percent": int(cap) if cap else None, "status": st, "health_percent": health}
    return None

def brightness(root="/sys/class/backlight"):
    for d in sorted(glob.glob(os.path.join(root, "*"))):
        cur, mx = _read(d + "/brightness"), _read(d + "/max_brightness")
        if cur and mx and int(mx):
            return {"percent": round(int(cur) * 100 / int(mx)), "path": d, "max": int(mx)}
    return None

def set_brightness(percent, root="/sys/class/backlight", writer=None):
    b = brightness(root)
    if not b: raise FileNotFoundError("подсветка экрана недоступна")
    percent = max(5, min(100, int(percent)))
    val = round(b["max"] * percent / 100)
    (writer or (lambda p, v: open(p, "w").write(str(v))))(b["path"] + "/brightness", val)
    return val

def lid_hint():
    return "Действие при закрытии крышки: /etc/systemd/logind.conf (HandleLidSwitch)"
