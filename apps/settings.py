#!/usr/bin/env python3
"""NEVEXONA Settings (Tk): масштаб, профиль, обновления. GUI ещё не запускалась на реальном экране."""
import os, sys
sys.path.insert(0, os.environ.get("NEVEXONA_LIB", "/usr/lib/nevexona"))
from apps import theme, panels
from system import profiles, monitor

def main():
    import tkinter as tk
    from tkinter import ttk, messagebox
    root = tk.Tk(); root.title("NEVEXONA Settings"); root.geometry("640x480"); theme.style(root)
    def head(t): tk.Label(root, text=t, bg=theme.BG, fg=theme.ACC, font=("DejaVu Sans", 13, "bold")).pack(anchor="w", padx=20, pady=(18, 4))
    head("Масштаб интерфейса")
    row = tk.Frame(root, bg=theme.BG); row.pack(anchor="w", padx=20)
    for pc in (100, 125, 150, 200):
        ttk.Button(row, text=f"{pc}%", command=lambda x=pc: messagebox.showinfo("Масштаб", f"Сохранено: {panels.set_scale(x)} DPI. Перезайдите в сеанс.")).pack(side="left", padx=4)
    head("Профиль производительности")
    tk.Label(root, text=panels.profile_text(), bg=theme.BG, fg=theme.TXT).pack(anchor="w", padx=20)
    cb = ttk.Combobox(root, values=list(profiles.PROFILES), state="readonly"); cb.set(profiles.recommend(monitor.meminfo()["total"])); cb.pack(anchor="w", padx=20, pady=6)
    ttk.Button(root, text="Применить профиль", command=lambda: (profiles.save(cb.get(), os.path.expanduser("~/.config/nevexona/profile.json")), messagebox.showinfo("Профиль", "Сохранено"))).pack(anchor="w", padx=20)
    head("Обновления")
    out = tk.Label(root, text="", bg=theme.BG, fg=theme.TXT); out.pack(anchor="w", padx=20)
    ttk.Button(root, text="Проверить обновления", command=lambda: out.config(text=panels.update_status())).pack(anchor="w", padx=20, pady=6)
    root.mainloop()

if __name__ == "__main__":
    main()
