"""Версии Proton и бэкап сохранений игр."""
import glob, os
from system import backup

def versions(steam_root=None):
    roots = [steam_root] if steam_root else [os.path.expanduser("~/.local/share/Steam"), os.path.expanduser("~/.steam/steam")]
    found = set()
    for r in roots:
        for pat in ("compatibilitytools.d/*", "steamapps/common/Proton*"):
            for d in glob.glob(os.path.join(r, pat)):
                if os.path.isdir(d): found.add(os.path.basename(d))
    return sorted(found)

def backup_saves(paths, dest):
    existing = [p for p in paths if os.path.exists(p)]
    if not existing: raise FileNotFoundError("сохранения не найдены")
    return backup.backup(existing, dest)
