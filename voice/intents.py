"""Голосовые намерения NEVEXONA. Распознанный текст НИКОГДА не выполняется как shell.
Только белый список намерений -> фиксированные argv. Опасные требуют подтверждения."""
import re
from dataclasses import dataclass, field

@dataclass(frozen=True)
class Intent:
    name: str
    argv: tuple            # фиксированная команда, без shell
    confirm: bool = False  # требуется подтверждение пользователя
    admin: bool = False    # нужна повторная аутентификация (через polkit)

APPS = {"браузер": "firefox-esr", "файловый менеджер": "pcmanfm", "настройки": "nevexona-settings",
        "терминал": "lxterminal"}
FOLDERS = {"загрузки": "Downloads", "документы": "Documents", "музыка": "Music", "изображения": "Pictures"}

_RULES = [
    (r"^(открой|запусти) (браузер|файловый менеджер|настройки|терминал)$", "open_app"),
    (r"^открой папку (загрузки|документы|музыка|изображения)$", "open_folder"),
    (r"^увеличь громкость$", "vol_up"), (r"^уменьши громкость$", "vol_down"),
    (r"^выключи звук$", "mute"),
    (r"^включи wi-?fi$", "wifi_on"), (r"^выключи wi-?fi$", "wifi_off"),
    (r"^включи bluetooth$", "bt_on"),
    (r"^покажи свободное место$", "disk_free"),
    (r"^сделай снимок экрана$", "screenshot"),
    (r"^проверь обновления$", "check_updates"),
    (r"^заблокируй экран$", "lock"),
    (r"^выключи компьютер$", "poweroff"), (r"^перезагрузи компьютер$", "reboot"),
]

def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower().rstrip(".!?"))

def parse(text: str):
    """Возвращает Intent или None. Параметры только из закрытых списков."""
    t = _norm(text)
    for pat, name in _RULES:
        m = re.match(pat, t)
        if not m:
            continue
        if name == "open_app":
            return Intent(name, (APPS[m.group(2)],))
        if name == "open_folder":
            return Intent(name, ("pcmanfm", "~/" + FOLDERS[m.group(1)]))
        table = {
            "vol_up": Intent(name, ("amixer", "set", "Master", "5%+")),
            "vol_down": Intent(name, ("amixer", "set", "Master", "5%-")),
            "mute": Intent(name, ("amixer", "set", "Master", "toggle")),
            "wifi_on": Intent(name, ("nmcli", "radio", "wifi", "on")),
            "wifi_off": Intent(name, ("nmcli", "radio", "wifi", "off")),
            "bt_on": Intent(name, ("rfkill", "unblock", "bluetooth")),
            "disk_free": Intent(name, ("df", "-h", "/")),
            "screenshot": Intent(name, ("scrot",)),
            "check_updates": Intent(name, ("apt", "list", "--upgradable")),
            "lock": Intent(name, ("loginctl", "lock-session")),
            "poweroff": Intent(name, ("systemctl", "poweroff"), confirm=True, admin=True),
            "reboot": Intent(name, ("systemctl", "reboot"), confirm=True, admin=True),
        }
        return table[name]
    return None

def run(intent: Intent, confirmed: bool = False, runner=None):
    """Выполняет намерение. Без подтверждения опасные не запускаются."""
    if intent.confirm and not confirmed:
        raise PermissionError("Требуется подтверждение: " + intent.name)
    import os, subprocess
    argv = [os.path.expanduser(a) for a in intent.argv]
    return (runner or subprocess.run)(argv, shell=False, check=False)
