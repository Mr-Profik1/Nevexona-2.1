"""Сеанс голосового управления: запись -> текст -> намерение -> подтверждение -> выполнение. Микрофон включается только явно."""
import os, subprocess
from voice import intents, stt

def record(path, seconds=5, runner=None):
    """Запись с микрофона на время seconds. Возвращает путь. Вызывается только по нажатию кнопки."""
    if not 1 <= seconds <= 30: raise ValueError("длительность 1–30 секунд")
    (runner or subprocess.run)(["arecord", "-q", "-d", str(seconds), "-f", "S16_LE", "-r", "16000", "-c", "1", path], shell=False, check=False)
    return path

def handle_text(text):
    i = intents.parse(text)
    if i is None: return {"status": "Команда не распознана", "intent": None, "needs_confirm": False, "text": text}
    return {"status": "Намерение: " + i.name, "intent": i, "needs_confirm": i.confirm, "text": text}

def listen_once(wav, seconds=5, recorder=None, transcriber=None):
    rec = recorder or record; tr = transcriber or stt.transcribe
    rec(wav, seconds); text, msg = tr(wav)
    try: os.remove(wav)
    except OSError: pass
    if text is None: return {"status": msg, "intent": None, "needs_confirm": False, "text": ""}
    return handle_text(text)
