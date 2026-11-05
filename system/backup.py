"""Резервное копирование с манифестом SHA256, проверкой и выборочным восстановлением."""
import hashlib, json, os, shutil

def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def backup(sources, dest):
    os.makedirs(dest, exist_ok=True)
    manifest = {}
    for src in sources:
        src = os.path.abspath(src)
        base = os.path.dirname(src)
        walk = [(src, "")] if os.path.isfile(src) else [(os.path.join(r, f), "") for r, _, fs in os.walk(src) for f in fs]
        for p, _ in walk:
            rel = os.path.relpath(p, base)
            out = os.path.join(dest, "files", rel)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            shutil.copy2(p, out)
            manifest[rel] = _sha(out)
    json.dump(manifest, open(os.path.join(dest, "manifest.json"), "w"), indent=1)
    return manifest

def verify(dest):
    """Возвращает список повреждённых/отсутствующих файлов."""
    manifest = json.load(open(os.path.join(dest, "manifest.json")))
    bad = []
    for rel, h in manifest.items():
        p = os.path.join(dest, "files", rel)
        if not os.path.isfile(p) or _sha(p) != h:
            bad.append(rel)
    return bad

def restore(dest, rels, target, overwrite=False):
    for rel in rels:
        src = os.path.join(dest, "files", rel)
        out = os.path.join(target, rel)
        if os.path.exists(out) and not overwrite:
            raise FileExistsError(out)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        shutil.copy2(src, out)
