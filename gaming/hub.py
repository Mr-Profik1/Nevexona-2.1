"""Game Hub: библиотека установленных игр, запуск без shell, каталог платформ.
Ничего не скачивает без явного действия пользователя."""
import glob, json, os, re, shutil, subprocess

# Каталог платформ. status — честный статус совместимости на Linux.
PLATFORMS = [
    {"id": "steam", "name": "Steam", "install": ["apt", "install", "steam-installer"], "needs_i386": True,
     "status": "Работает; Windows-игры через Proton. Часть игр с античитом не запустится."},
    {"id": "lutris", "name": "Lutris", "install": ["apt", "install", "lutris"], "needs_i386": False,
     "status": "Работает (Wine-обёртки для игр вне Steam)."},
    {"id": "wine", "name": "Wine", "install": ["apt", "install", "wine"], "needs_i386": True,
     "status": "Совместимость зависит от конкретной игры."},
    {"id": "minecraft-java", "name": "Minecraft Java Edition", "install": ["apt", "install", "default-jre"], "needs_i386": False,
     "status": "Работает на Linux; нужен лаунчер Mojang или Prism Launcher (устанавливается отдельно) и ваша лицензия."},
    {"id": "roblox", "name": "Roblox", "install": None, "needs_i386": False,
     "status": "Официально НЕ поддерживается на Linux. Работа через Wine нестабильна и может блокироваться. Не обещаем."},
]

def steam_games(steam_root=None):
    """Читает appmanifest_*.acf установленных Steam-игр."""
    roots = [steam_root] if steam_root else [os.path.expanduser("~/.local/share/Steam"),
                                              os.path.expanduser("~/.steam/steam")]
    games = []
    for r in roots:
        for f in glob.glob(os.path.join(r, "steamapps", "appmanifest_*.acf")):
            t = open(f, errors="ignore").read()
            appid = re.search(r'"appid"\s+"(\d+)"', t)
            name = re.search(r'"name"\s+"([^"]+)"', t)
            if appid and name:
                games.append({"name": name[1], "source": "steam", "argv": ["steam", f"steam://rungameid/{appid[1]}"]})
    return games

class Library:
    def __init__(self, path):
        self.path = path
        self.custom = json.load(open(path)) if os.path.exists(path) else []

    def add(self, name, argv):
        if not argv or not shutil.which(argv[0]) and not os.path.isfile(argv[0]):
            raise FileNotFoundError(argv[0] if argv else "пустая команда")
        self.custom.append({"name": name, "source": "custom", "argv": list(argv)})
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        json.dump(self.custom, open(self.path, "w"), ensure_ascii=False, indent=1)

    def all(self, steam_root=None):
        return sorted(steam_games(steam_root) + self.custom, key=lambda g: g["name"].lower())

    def find(self, query, steam_root=None):
        q = query.lower()
        return [g for g in self.all(steam_root) if q in g["name"].lower()]

def launch(game, runner=None):
    return (runner or subprocess.Popen)(game["argv"], shell=False)

def disk_ok(path, need_gb):
    return shutil.disk_usage(path).free >= need_gb * 2**30
