#!/usr/bin/env python3
"""NEVEXONA Control Center — окно на Tk (python3-tk). ВНИМАНИЕ: GUI-оболочка ещё не запускалась на реальном экране."""
import os, sys
sys.path.insert(0, os.environ.get("NEVEXONA_LIB", "/usr/lib/nevexona"))
from apps import panels
from gaming import platforms
from ai import assistant
from voice import stt

BG, BG2, SURF, ACC, TXT, TXT2 = "#171717", "#202020", "#292929", "#FF781F", "#F2F2F2", "#A0A0A0"
LIB = os.path.expanduser("~/.config/nevexona/games.json")
QDIR = os.path.expanduser("~/.local/share/nevexona/quarantine")

def main():
    import tkinter as tk
    from tkinter import ttk, messagebox
    root = tk.Tk(); root.title("NEVEXONA Control Center"); root.geometry("980x620"); root.configure(bg=BG)
    st = ttk.Style(root); st.theme_use("clam")
    st.configure("TNotebook", background=BG, borderwidth=0)
    st.configure("TNotebook.Tab", background=SURF, foreground=TXT, padding=(16, 8))
    st.map("TNotebook.Tab", background=[("selected", ACC)], foreground=[("selected", BG)])
    st.configure("Treeview", background=SURF, fieldbackground=SURF, foreground=TXT, rowheight=26, borderwidth=0)
    st.configure("TButton", background=ACC, foreground=BG, padding=8)
    nb = ttk.Notebook(root); nb.pack(fill="both", expand=True, padx=12, pady=12)

    def tab(name):
        f = tk.Frame(nb, bg=BG2); nb.add(f, text=name); return f
    def table(parent, cols):
        t = ttk.Treeview(parent, columns=cols, show="headings")
        for c in cols: t.heading(c, text=c); t.column(c, width=150)
        t.pack(fill="both", expand=True, padx=10, pady=10); return t
    def fill(t, rows):
        t.delete(*t.get_children())
        for r in rows: t.insert("", "end", values=r)

    f = tab("Монитор"); lbl = tk.Label(f, bg=BG2, fg=TXT, justify="left", font=("DejaVu Sans", 13)); lbl.pack(anchor="w", padx=20, pady=20)
    def tick(): lbl.config(text=panels.monitor_text()); root.after(2000, tick)
    tick()

    f = tab("Драйверы"); t = table(f, ("Производитель", "Устройство", "Драйвер", "Статус", "Пакет"))
    ttk.Button(f, text="Сканировать", command=lambda: fill(t, panels.drivers_rows())).pack(pady=(0, 10))

    f = tab("Игры"); t = table(f, ("Игра / платформа", "Источник / статус"))
    def refresh_games(): fill(t, panels.games_rows(LIB) + panels.platforms_rows())
    ttk.Button(f, text="Обновить", command=refresh_games).pack(); tk.Label(f, text="NEVEXONA Android: " + panels.android_status(), bg=BG2, fg=TXT2).pack(pady=8)

    for pid, label in (("steam", "Установить Steam"), ("lutris", "Установить Lutris"), ("wine", "Установить Wine")):
        def go(x=pid, l=label):
            if messagebox.askyesno(l, "Будут изменены пакеты системы (потребуется пароль). Продолжить?"):
                res = platforms.install(x, confirmed=True)
                messagebox.showinfo(l, "Готово" if all(c == 0 for _, c in res) else "Ошибка установки: смотрите журнал apt")
        ttk.Button(f, text=label, command=go).pack(side="left", padx=6, pady=8)
    f = tab("Безопасность"); t = table(f, ("ID", "Исходный путь", "Причина"))
    ttk.Button(f, text="Показать карантин", command=lambda: fill(t, panels.quarantine_rows(QDIR))).pack(pady=(0, 10))

    f = tab("Голос"); e = tk.Entry(f, font=("DejaVu Sans", 13), bg=SURF, fg=TXT, insertbackground=TXT); e.pack(fill="x", padx=20, pady=20)
    out = tk.Label(f, bg=BG2, fg=TXT, font=("DejaVu Sans", 12)); out.pack()
    ttk.Button(f, text="Проверить команду", command=lambda: out.config(text=panels.voice_preview(e.get())[0])).pack(pady=10)
    tk.Label(f, text="Распознавание речи (микрофон) ещё не подключено: здесь проверка текстовых команд.", bg=BG2, fg=TXT2).pack()

    f = tab("Ассистент"); e2 = tk.Entry(f, font=("DejaVu Sans", 12), bg=SURF, fg=TXT, insertbackground=TXT); e2.pack(fill="x", padx=20, pady=12)
    ao = tk.Label(f, bg=BG2, fg=TXT, wraplength=800, justify="left"); ao.pack(padx=20)
    def ask_ai():
        try:
            who, text = assistant.ask(e2.get(), "AUTO", key=assistant.load_key(), consent=lambda m: messagebox.askyesno("Облако", m))
            ao.config(text=f"[{who}] {text}")
        except Exception as ex: ao.config(text=str(ex))
    ttk.Button(f, text="Спросить", command=ask_ai).pack(pady=6)
    tk.Label(f, text="Ключ OpenRouter вводится в настройках и хранится только на этом компьютере. " + stt.info(), bg=BG2, fg=TXT2, wraplength=800).pack(pady=8)
    f = tab("Профиль"); pl = tk.Label(f, bg=BG2, fg=TXT, font=("DejaVu Sans", 13)); pl.pack(padx=20, pady=30)
    pl.config(text=panels.profile_text())
    f = tab("Сеть"); t = table(f, ("Сеть / устройство", "Сигнал / MAC", "Защита"))
    ttk.Button(f, text="Wi-Fi: найти сети", command=lambda: fill(t, [r + ("",) * (3 - len(r)) for r in panels.wifi_rows()])).pack(side="left", padx=10, pady=(0, 10))
    ttk.Button(f, text="Bluetooth: устройства", command=lambda: fill(t, [r + ("",) for r in panels.bt_rows()])).pack(side="left", pady=(0, 10))
    f = tab("Ноутбук"); ll = tk.Label(f, bg=BG2, fg=TXT, justify="left", font=("DejaVu Sans", 13)); ll.pack(anchor="w", padx=20, pady=20)
    ll.config(text=panels.laptop_text())
    f = tab("Масштаб"); tk.Label(f, text="Масштаб интерфейса (применяется после перезахода):", bg=BG2, fg=TXT).pack(pady=20)
    for pc in (100, 125, 150, 200):
        ttk.Button(f, text=f"{pc}%", command=lambda x=pc: messagebox.showinfo("Масштаб", f"Сохранено: {panels.set_scale(x)} DPI. Перезайдите в сеанс.")).pack(pady=4)
    f = tab("Обновления"); out2 = tk.Label(f, bg=BG2, fg=TXT, font=("DejaVu Sans", 13)); out2.pack(padx=20, pady=30)
    ttk.Button(f, text="Проверить обновления", command=lambda: out2.config(text=panels.update_status())).pack()
    root.mainloop()

if __name__ == "__main__":
    main()
