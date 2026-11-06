"""Распознавание речи (офлайн, Vosk). Модель скачивается ТОЛЬКО по явному действию пользователя."""
import os, urllib.request, zipfile

MODEL = {"name": "vosk-model-small-ru-0.22", "url": "https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip",
         "size_mb": 45, "ram_mb": 300, "disk_mb": 100}
DIR = os.path.expanduser("~/.local/share/nevexona/models")

def info():
    m = MODEL
    return f"Модель {m['name']}: скачать ~{m['size_mb']} МБ, ОЗУ ~{m['ram_mb']} МБ, на диске ~{m['disk_mb']} МБ. После загрузки работает офлайн."

def installed(d=DIR): return os.path.isdir(os.path.join(d, MODEL["name"]))

def download(confirmed=False, d=DIR, opener=None):
    if not confirmed: raise PermissionError("Скачивание модели требует вашего подтверждения")
    os.makedirs(d, exist_ok=True); z = os.path.join(d, MODEL["name"] + ".zip")
    open(z, "wb").write((opener or urllib.request.urlopen)(MODEL["url"], timeout=120).read())
    zipfile.ZipFile(z).extractall(d); os.remove(z); return installed(d)

def transcribe(wav_path, d=DIR):
    """Возвращает текст или сообщение, что нужно. Требует пакет vosk и загруженную модель."""
    if not installed(d): return None, "Голосовая модель не загружена"
    try: import vosk, wave, json
    except ImportError: return None, "Модуль vosk не установлен"
    wf = wave.open(wav_path, "rb"); rec = vosk.KaldiRecognizer(vosk.Model(os.path.join(d, MODEL["name"])), wf.getframerate())
    while True:
        data = wf.readframes(4000)
        if not data: break
        rec.AcceptWaveform(data)
    return json.loads(rec.FinalResult()).get("text", ""), "ok"
