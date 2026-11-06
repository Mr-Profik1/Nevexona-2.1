#!/usr/bin/env python3
"""NEVEXONA Backup & Recovery (Tk). GUI не запускалась на экране."""
import os, sys
sys.path.insert(0, os.environ.get("NEVEXONA_LIB", "/usr/lib/nevexona"))
from apps import theme
from system import backup, schedule

def main():
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    root = tk.Tk(); root.title("NEVEXONA Backup & Recovery"); root.geometry("600x420"); theme.style(root)
    st = {"src": [], "dst": ""}
    info = tk.Label(root, text="Выберите папку для копирования и место назначения", bg=theme.BG, fg=theme.TXT, wraplength=560); info.pack(pady=14)
    def src():
        p = filedialog.askdirectory(title="Что копировать")
        if p: st["src"] = [p]; info.config(text=f"Источник: {p}\\nНазначение: {st['dst'] or '—'}")
    def dst():
        p = filedialog.askdirectory(title="Куда копировать")
        if p: st["dst"] = p; info.config(text=f"Источник: {(st['src'] or ['—'])[0]}\\nНазначение: {p}")
    def go():
        if not (st["src"] and st["dst"]): return messagebox.showwarning("Копия", "Выберите источник и назначение")
        backup.backup(st["src"], st["dst"]); bad = backup.verify(st["dst"])
        messagebox.showinfo("Копия", "Готово, целостность проверена" if not bad else "Повреждены: " + ", ".join(bad))
    def plan():
        if st["src"] and st["dst"]: schedule.install_units(st["src"], st["dst"], "daily"); messagebox.showinfo("Расписание", "Ежедневное расписание создано (systemctl --user enable --now nevexona-backup.timer)")
    for t, c in (("1. Выбрать источник", src), ("2. Выбрать назначение", dst), ("Сделать копию и проверить", go), ("Включить ежедневную копию", plan)):
        ttk.Button(root, text=t, command=c).pack(pady=5)
    tk.Label(root, text="Сброс системы не выполняется без объяснения последствий и вашего подтверждения.", bg=theme.BG, fg=theme.TXT2, wraplength=560).pack(pady=14)
    root.mainloop()

if __name__ == "__main__":
    main()
