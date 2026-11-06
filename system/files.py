"""Файловые операции Explorer: копирование, перемещение, поиск, корзина (стандарт freedesktop)."""
import datetime, fnmatch, os, shutil, urllib.parse

def copy(src, dst):
    if os.path.isdir(src): shutil.copytree(src, os.path.join(dst, os.path.basename(src)))
    else: shutil.copy2(src, dst)

def move(src, dst): shutil.move(src, dst)

def search(root, pattern, limit=200):
    out = []
    for r, ds, fs in os.walk(root):
        for n in ds + fs:
            if fnmatch.fnmatch(n.lower(), pattern.lower()):
                out.append(os.path.join(r, n))
                if len(out) >= limit: return out
    return out

def trash(path, trash_dir=None):
    trash_dir = trash_dir or os.path.expanduser("~/.local/share/Trash")
    files, info = os.path.join(trash_dir, "files"), os.path.join(trash_dir, "info")
    os.makedirs(files, exist_ok=True); os.makedirs(info, exist_ok=True)
    path = os.path.abspath(path); name = os.path.basename(path); n, i = name, 1
    while os.path.exists(os.path.join(files, n)):
        n = f"{name}.{i}"; i += 1
    open(os.path.join(info, n + ".trashinfo"), "w").write(
        f"[Trash Info]\nPath={urllib.parse.quote(path)}\nDeletionDate={datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')}\n")
    shutil.move(path, os.path.join(files, n)); return n

def restore(name, trash_dir=None):
    trash_dir = trash_dir or os.path.expanduser("~/.local/share/Trash")
    meta = open(os.path.join(trash_dir, "info", name + ".trashinfo")).read()
    orig = urllib.parse.unquote([l for l in meta.splitlines() if l.startswith("Path=")][0][5:])
    if os.path.exists(orig): raise FileExistsError(orig)
    shutil.move(os.path.join(trash_dir, "files", name), orig); os.remove(os.path.join(trash_dir, "info", name + ".trashinfo")); return orig
