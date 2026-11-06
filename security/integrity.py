"""Целостность важных файлов (эталон SHA256) и проверка автозапуска."""
import glob, hashlib, json, os

DEFAULT = ["/etc/passwd", "/etc/group", "/etc/fstab", "/etc/sudoers", "/etc/hosts", "/etc/ssh/sshd_config"]

def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""): h.update(b)
    return h.hexdigest()

def baseline(paths=None):
    out, skipped = {}, []
    for p in paths or DEFAULT:
        try: out[p] = _sha(p)
        except OSError: skipped.append(p)
    return {"hashes": out, "skipped": skipped}

def save(b, path): os.makedirs(os.path.dirname(path), exist_ok=True); json.dump(b, open(path, "w"), indent=1)

def compare(old, paths=None):
    new = baseline(paths or list(old["hashes"]))["hashes"]
    return {"changed": [p for p in old["hashes"] if p in new and new[p] != old["hashes"][p]],
            "missing": [p for p in old["hashes"] if p not in new]}

def autostart(dirs=None, openbox=None):
    dirs = dirs if dirs is not None else [os.path.expanduser("~/.config/autostart"), "/etc/xdg/autostart"]
    items = []
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(d, "*.desktop"))):
            ex = [l.split("=", 1)[1].strip() for l in open(f, errors="ignore") if l.startswith("Exec=")]
            items.append({"source": f, "exec": ex[0] if ex else ""})
    ob = openbox or os.path.expanduser("~/.config/openbox/autostart")
    if os.path.isfile(ob):
        items += [{"source": ob, "exec": l.strip().rstrip("&").strip()} for l in open(ob) if l.strip() and not l.startswith("#")]
    return items
