"""Ассистент: LOCAL / CLOUD (OpenRouter, по желанию) / AUTO (перед отправкой в облако всегда спрашивает).
Ключ хранится локально с правами 0600, не логируется."""
import json, os, shutil, subprocess, urllib.request

KEY_PATH = os.path.expanduser("~/.config/nevexona/openrouter.key")
URL = "https://openrouter.ai/api/v1/chat/completions"

def save_key(key, path=KEY_PATH):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f: f.write(key.strip())
    os.chmod(path, 0o600)

def load_key(path=KEY_PATH):
    try: return open(path).read().strip() or None
    except OSError: return None

def local_ready(model_path):
    return bool(model_path) and os.path.isfile(model_path) and shutil.which("llama-cli") is not None

def ask_local(prompt, model_path, runner=None):
    if not local_ready(model_path): raise RuntimeError("Локальная модель не загружена")
    r = (runner or subprocess.run)(["llama-cli", "-m", model_path, "-p", prompt, "-n", "256"], capture_output=True, text=True, shell=False, check=False)
    return r.stdout.strip()

def ask_cloud(prompt, key, model="openrouter/auto", opener=None):
    if not key: raise RuntimeError("Нет API-ключа (введите в настройках)")
    req = urllib.request.Request(URL, data=json.dumps({"model": model, "messages": [{"role": "user", "content": prompt}]}).encode(),
                                 headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    d = json.load((opener or urllib.request.urlopen)(req, timeout=60))
    return d["choices"][0]["message"]["content"]

def ask(prompt, mode="AUTO", model_path=None, key=None, consent=None, local=None, cloud=None):
    local, cloud = local or ask_local, cloud or ask_cloud
    if mode == "LOCAL": return "local", local(prompt, model_path)
    if mode == "CLOUD": return "cloud", cloud(prompt, key)
    if mode == "AUTO":
        if local_ready(model_path) or (local is not ask_local):
            return "local", local(prompt, model_path)
        if consent is None or not consent("Отправить запрос в облако (OpenRouter)?"):
            raise PermissionError("Локальной модели нет, отправка в облако не разрешена")
        return "cloud", cloud(prompt, key)
    raise ValueError("режим: LOCAL, CLOUD или AUTO")
