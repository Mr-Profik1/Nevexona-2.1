"""Расписание резервных копий: генерирует пользовательские systemd-юниты (timer + service)."""
import os, re
WHEN = {"hourly": "hourly", "daily": "daily", "weekly": "weekly"}

def make_units(sources, dest, when="daily"):
    if when not in WHEN: raise ValueError("расписание: hourly, daily, weekly")
    for p in list(sources) + [dest]:
        if not p.startswith("/") or re.search(r"[\n\r\"']", p): raise ValueError("недопустимый путь: " + p)
    args = " ".join(f'"{s}"' for s in sources)
    service = ("[Unit]\nDescription=NEVEXONA backup\n\n[Service]\nType=oneshot\n"
               f'ExecStart=/usr/bin/python3 /usr/lib/nevexona/system/backup_cli.py "{dest}" {args}\n')
    timer = f"[Unit]\nDescription=NEVEXONA backup timer\n\n[Timer]\nOnCalendar={WHEN[when]}\nPersistent=true\n\n[Install]\nWantedBy=timers.target\n"
    return service, timer

def install_units(sources, dest, when="daily", home=None):
    d = os.path.join(home or os.path.expanduser("~"), ".config/systemd/user"); os.makedirs(d, exist_ok=True)
    s, t = make_units(sources, dest, when)
    open(os.path.join(d, "nevexona-backup.service"), "w").write(s); open(os.path.join(d, "nevexona-backup.timer"), "w").write(t)
    return d
