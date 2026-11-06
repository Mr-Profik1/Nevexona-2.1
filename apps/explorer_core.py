"""Логика Проводника (без GUI): список папки, размеры, безопасные операции."""
import os
from system import files

def human(n):
    for u in ("Б", "КБ", "МБ", "ГБ"):
        if n < 1024 or u == "ГБ": return f"{n:.0f} {u}" if u == "Б" else f"{n:.1f} {u}"
        n /= 1024

def list_dir(path):
    out = []
    for e in os.scandir(path):
        try: d = e.is_dir(); size = "" if d else human(e.stat().st_size)
        except OSError: continue
        out.append((e.name, "Папка" if d else "Файл", size))
    return sorted(out, key=lambda x: (x[1] != "Папка", x[0].lower()))

def delete(path, trash_dir=None):
    """Удаление только в корзину (восстановимо)."""
    return files.trash(path, trash_dir)
