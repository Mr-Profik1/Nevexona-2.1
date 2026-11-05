"""NEVEXONA Android: обёртка над Waydroid (Android в контейнере на Linux).
Не эмулятор: нужен CPU с виртуализацией/ядро с binder и Wayland-сеанс. Образ Android скачивается по желанию пользователя.
Всё через фиксированные команды, без shell."""
import os, shutil, subprocess

def available():
    return shutil.which("waydroid") is not None

def run(args, runner=None):
    return (runner or subprocess.run)(["waydroid", *args], capture_output=True, text=True, shell=False, check=False)

def requirements():
    """Честная проверка среды. Возвращает список проблем (пусто = можно пробовать)."""
    problems = []
    if not available():
        problems.append("Waydroid не установлен")
    if not os.path.exists("/dev/binderfs") and not os.path.exists("/dev/binder"):
        problems.append("Ядро не предоставляет binder")
    if os.environ.get("XDG_SESSION_TYPE") != "wayland":
        problems.append("Нужен Wayland-сеанс (в X11 запускается отдельный композитор)")
    try:
        if "vmx" not in open("/proc/cpuinfo").read() and "svm" not in open("/proc/cpuinfo").read():
            problems.append("Процессор не показывает виртуализацию (vmx/svm)")
    except OSError:
        pass
    return problems

def install_apk(path, runner=None):
    if not path.lower().endswith(".apk") or not os.path.isfile(path):
        raise ValueError("нужен существующий .apk файл")
    return run(["app", "install", path], runner)

def launch(package, runner=None):
    if not package.replace(".", "").replace("_", "").isalnum():
        raise ValueError("недопустимое имя пакета")
    return run(["app", "launch", package], runner)

def list_apps(runner=None):
    return run(["app", "list"], runner).stdout
