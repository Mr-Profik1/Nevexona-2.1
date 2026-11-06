"""Несколько мониторов через xrandr (разбор вывода, безопасные команды)."""
import re

def parse_xrandr(text):
    out, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^(\S+) (connected|disconnected)", line)
        if m: cur = {"name": m[1], "connected": m[2] == "connected", "modes": [], "current": None}; out.append(cur); continue
        m = re.match(r"^\s+(\d+x\d+)\s+(.*)$", line)
        if m and cur:
            cur["modes"].append(m[1])
            if "*" in m[2]: cur["current"] = m[1]
    return out

_N, _M = re.compile(r"^[A-Za-z0-9-]+$"), re.compile(r"^\d+x\d+$")

def set_mode(name, mode):
    if not _N.match(name) or not _M.match(mode): raise ValueError("недопустимые параметры")
    return ["xrandr", "--output", name, "--mode", mode]

def right_of(name, other):
    if not (_N.match(name) and _N.match(other)): raise ValueError("недопустимые параметры")
    return ["xrandr", "--output", name, "--right-of", other]
