"""Данные для вкладок Control Center. Без GUI — полностью тестируется."""
from system import monitor, updater
from drivers import detect
from gaming import hub, android
from security.quarantine import Quarantine
from voice import intents
from system import profiles, display
from network import center as net
from laptop import center as lap
from security import scanner

def monitor_text():
    m, d = monitor.meminfo(), monitor.disk()
    l = monitor.load()
    return (f"ОЗУ: {m['used']//2**20} / {m['total']//2**20} МБ ({m['percent']}%)\n"
            f"Диск /: {d['used']//2**30} / {d['total']//2**30} ГБ ({d['percent']}%)\n"
            f"Нагрузка: {l[0]:.2f} {l[1]:.2f} {l[2]:.2f}")

def drivers_rows(scan=detect.scan):
    try:
        return [(d["vendor"], d["name"], d["driver"] or "—", d["status"], d["firmware_pkg"] or "") for d in scan()]
    except FileNotFoundError:
        return []  # lspci отсутствует

def games_rows(lib_path, steam_root=None):
    lib = hub.Library(lib_path)
    rows = [(g["name"], g["source"]) for g in lib.all(steam_root)]
    return rows

def platforms_rows():
    return [(p["name"], p["status"]) for p in hub.PLATFORMS]

def android_status():
    p = android.requirements()
    return "Готов к настройке" if not p else "Не готов: " + "; ".join(p)

def quarantine_rows(root):
    return [(m["id"][:8], m["orig"], m["reason"]) for m in Quarantine(root).list()]

def voice_preview(text):
    i = intents.parse(text)
    if i is None:
        return "Команда не распознана", None
    note = " (потребуется подтверждение)" if i.confirm else ""
    return f"Намерение: {i.name}{note}", i

def update_status(opener=None):
    try:
        r = updater.fetch_latest(opener=opener)
    except RuntimeError as e:
        return str(e)
    if r is None:
        return "Релизов с пакетом обновления пока нет"
    return f"Доступна версия {r['version']}" if updater.newer(r["version"]) else "У вас последняя версия"

def profile_text():
    m = monitor.meminfo()
    return f"ОЗУ: {m['total']//2**20} МБ. Рекомендуемый профиль: {profiles.recommend(m['total'])}"

def wifi_rows():
    try: return [(n["ssid"], f"{n['signal']}%", n["security"]) for n in net.wifi_list()]
    except FileNotFoundError: return []

def bt_rows():
    try: return [(d["name"], d["mac"]) for d in net.bt_devices()]
    except FileNotFoundError: return []

def laptop_text():
    b, br = lap.battery(), lap.brightness()
    parts = [f"Батарея: {b['percent']}% ({b['status']})" + (f", состояние {b['health_percent']}%" if b["health_percent"] else "") if b else "Батарея: не обнаружена",
             f"Яркость: {br['percent']}%" if br else "Яркость: управление недоступно"]
    return "\n".join(parts)

def scan_summary(paths, runner=None):
    r = scanner.scan(paths, runner=runner)
    if r.get("status") == "ClamAV не найден": return "ClamAV не найден"
    return f"Проверено файлов: {r['scanned']}, найдено: {r['infected']}, ошибок: {len(r['errors'])}"

def set_scale(percent): return display.set_scale(percent)
