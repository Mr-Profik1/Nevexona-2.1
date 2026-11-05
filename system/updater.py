"""Update Center: обновление NEVEXONA без переустановки через GitHub Releases.
Проверка версии -> загрузка .deb -> проверка SHA256 -> установка только после подтверждения (pkexec apt)."""
import hashlib, json, os, re, subprocess, urllib.request

REPO = "Mr-Profik1/Nevexona-2.1"
CURRENT = "0.2.0"

def _ver(v):
    return tuple(int(x) for x in re.findall(r"\d+", v)[:3]) or (0,)

def newer(remote, local=CURRENT):
    return _ver(remote) > _ver(local)

def fetch_latest(opener=None, repo=REPO):
    """Возвращает {'version','deb_url','sha256_url'} или None, если релизов нет."""
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        data = json.load((opener or urllib.request.urlopen)(url, timeout=15))
    except Exception as e:
        raise RuntimeError(f"Нет связи с GitHub: {e}")
    deb = next((a for a in data.get("assets", []) if a["name"].endswith(".deb")), None)
    sha = next((a for a in data.get("assets", []) if a["name"].endswith(".sha256")), None)
    if not deb or not sha:
        return None
    return {"version": data["tag_name"].lstrip("v"), "deb_url": deb["browser_download_url"],
            "sha256_url": sha["browser_download_url"]}

def verify(path, expected_sha256):
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if h != expected_sha256.strip().split()[0].lower():
        raise ValueError("SHA256 не совпадает: файл не устанавливается")
    return True

def install(deb_path, confirmed=False, runner=None):
    if not confirmed:
        raise PermissionError("Установка обновления требует подтверждения")
    if not deb_path.endswith(".deb") or not os.path.isfile(deb_path):
        raise ValueError("нужен существующий .deb")
    return (runner or subprocess.run)(["pkexec", "apt", "install", "-y", os.path.abspath(deb_path)], shell=False, check=False)
