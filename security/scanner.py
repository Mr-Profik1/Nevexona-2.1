"""Security Center: проверка через ClamAV (clamscan). Не гарантирует 100% обнаружения; отчёт содержит ошибки и пропуски."""
import re, shutil, subprocess

def available():
    return shutil.which("clamscan") is not None

def parse_report(text, version=""):
    found = [{"path": m[1], "signature": m[2]} for m in re.finditer(r"^(.+): (.+) FOUND$", text, re.M)]
    def num(label):
        m = re.search(label + r":\s*(\d+)", text)
        return int(m[1]) if m else None
    errors = [l for l in text.splitlines() if l.startswith("ERROR") or "Can't" in l or "Permission denied" in l]
    return {"scanned": num("Scanned files"), "infected": num("Infected files") if num("Infected files") is not None else len(found),
            "detections": found, "errors": errors, "db_version": version,
            "note": "Обнаружение не гарантируется на 100%. Подозрение не равно доказанной инфекции."}

def scan(paths, runner=None):
    if not paths: raise ValueError("не выбраны папки для проверки")
    if runner is None and not available():
        return {"status": "ClamAV не найден", "scanned": 0, "infected": 0, "detections": [], "errors": [], "db_version": ""}
    run = runner or subprocess.run
    ver = run(["clamscan", "--version"], capture_output=True, text=True, shell=False, check=False).stdout.strip()
    r = run(["clamscan", "-r", "--"] + list(paths), capture_output=True, text=True, shell=False, check=False)
    rep = parse_report(r.stdout, ver); rep["status"] = "завершено"; return rep
