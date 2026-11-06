"""Масштаб интерфейса (HiDPI) через Xft.dpi в ~/.Xresources."""
import os, re
SCALES = {100: 96, 125: 120, 150: 144, 175: 168, 200: 192}

def set_scale(percent, home=None):
    if percent not in SCALES: raise ValueError("допустимо: " + ", ".join(map(str, SCALES)))
    p = os.path.join(home or os.path.expanduser("~"), ".Xresources")
    t = open(p).read() if os.path.exists(p) else ""
    line = f"Xft.dpi: {SCALES[percent]}"
    t = re.sub(r"^Xft\.dpi:.*$", line, t, flags=re.M) if re.search(r"^Xft\.dpi:", t, re.M) else t + line + "\n"
    open(p, "w").write(t); return SCALES[percent]
