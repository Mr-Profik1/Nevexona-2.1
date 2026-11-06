"""Установка игровых платформ из официальных репозиториев Debian — только по явному подтверждению."""
import subprocess

PACKAGES = {"steam": ["steam-installer"], "lutris": ["lutris"], "wine": ["wine"],
            "java": ["default-jre"]}
NEEDS_I386 = {"steam", "wine"}

def plan(pid):
    if pid not in PACKAGES: raise ValueError("неизвестная платформа")
    steps = []
    if pid in NEEDS_I386: steps.append(["pkexec", "dpkg", "--add-architecture", "i386"])
    steps += [["pkexec", "apt", "update"], ["pkexec", "apt", "install", "-y", *PACKAGES[pid]]]
    return steps

def install(pid, confirmed=False, runner=None):
    if not confirmed: raise PermissionError("Установка требует подтверждения и показывает изменения системы")
    out = []
    for argv in plan(pid):
        r = (runner or subprocess.run)(argv, shell=False, check=False)
        out.append((argv, getattr(r, "returncode", 0)))
        if getattr(r, "returncode", 0) != 0: break
    return out
