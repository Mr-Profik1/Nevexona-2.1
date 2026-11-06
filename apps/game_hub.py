#!/usr/bin/env python3
"""NEVEXONA Game Hub (Tk). GUI ещё не запускалась на реальном экране."""
import os, sys
sys.path.insert(0, os.environ.get("NEVEXONA_LIB", "/usr/lib/nevexona"))
from apps import theme, panels
from gaming import hub, platforms, android

LIB = os.path.expanduser("~/.config/nevexona/games.json")

def main():
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog, simpledialog
    root = tk.Tk(); root.title("NEVEXONA Game Hub"); root.geometry("860x560"); theme.style(root)
    t = ttk.Treeview(root, columns=("n", "s"), show="headings"); t.heading("n", text="Игра"); t.heading("s", text="Источник"); t.column("n", width=520)
    t.pack(fill="both", expand=True, padx=10, pady=10)
    def refresh():
        t.delete(*t.get_children())
        for r in panels.games_rows(LIB): t.insert("", "end", values=r)
    def run():
        s = t.selection()
        if s:
            g = hub.Library(LIB).find(str(t.item(s[0])["values"][0]))
            if g: hub.launch(g[0])
    def add():
        p = filedialog.askopenfilename(title="Исполняемый файл игры")
        if p:
            name = simpledialog.askstring("Название", "Название игры:") or os.path.basename(p)
            try: hub.Library(LIB).add(name, [p]); refresh()
            except Exception as e: messagebox.showerror("Ошибка", str(e))
    bar = tk.Frame(root, bg=theme.BG); bar.pack(fill="x", padx=10, pady=(0, 10))
    for text, cmd in (("Запустить", run), ("Добавить игру", add), ("Обновить", refresh)): ttk.Button(bar, text=text, command=cmd).pack(side="left", padx=4)
    for pid in ("steam", "lutris", "wine"):
        def inst(x=pid):
            if messagebox.askyesno("Установка", f"Установить {x}? Будут изменены пакеты (потребуется пароль)."):
                res = platforms.install(x, confirmed=True); messagebox.showinfo("Установка", "Готово" if all(c == 0 for _, c in res) else "Ошибка, см. журнал apt")
        ttk.Button(bar, text=f"Установить {pid}", command=inst).pack(side="right", padx=4)
    tk.Label(root, text="NEVEXONA Android: " + panels.android_status(), bg=theme.BG, fg=theme.TXT2).pack(pady=(0, 8))
    refresh(); root.mainloop()

if __name__ == "__main__":
    main()
