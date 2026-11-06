#!/usr/bin/env python3
"""NEVEXONA Explorer (Tk). GUI ещё не запускалась на реальном экране."""
import os, subprocess, sys
sys.path.insert(0, os.environ.get("NEVEXONA_LIB", "/usr/lib/nevexona"))
from apps import explorer_core as core, theme

def main():
    import tkinter as tk
    from tkinter import ttk, messagebox
    root = tk.Tk(); root.title("NEVEXONA Explorer"); root.geometry("900x560"); theme.style(root)
    cur = {"p": os.path.expanduser("~")}
    bar = tk.Frame(root, bg=theme.BG); bar.pack(fill="x", padx=10, pady=8)
    ent = tk.Entry(bar, bg=theme.SURF, fg=theme.TXT, insertbackground=theme.TXT, relief="flat"); ent.pack(side="left", fill="x", expand=True, ipady=6)
    t = ttk.Treeview(root, columns=("n", "t", "s"), show="headings")
    for c, h in zip(("n", "t", "s"), ("Имя", "Тип", "Размер")): t.heading(c, text=h)
    t.column("n", width=520); t.pack(fill="both", expand=True, padx=10, pady=(0, 8))
    def show(p):
        try: rows = core.list_dir(p)
        except OSError as e: messagebox.showerror("Ошибка", str(e)); return
        cur["p"] = p; ent.delete(0, "end"); ent.insert(0, p); t.delete(*t.get_children())
        for r in rows: t.insert("", "end", values=r)
    def opened(_=None):
        s = t.selection()
        if s:
            v = t.item(s[0])["values"]; p = os.path.join(cur["p"], str(v[0]))
            if v[1] == "Папка": show(p)
            else: subprocess.Popen(["xdg-open", p])
    def to_trash():
        s = t.selection()
        if s and messagebox.askyesno("Корзина", "Переместить в корзину?"):
            core.delete(os.path.join(cur["p"], str(t.item(s[0])["values"][0]))); show(cur["p"])
    t.bind("<Double-1>", opened); ent.bind("<Return>", lambda e: show(ent.get()))
    ttk.Button(bar, text="Вверх", command=lambda: show(os.path.dirname(cur["p"]))).pack(side="left", padx=4)
    ttk.Button(bar, text="В корзину", command=to_trash).pack(side="left")
    show(cur["p"]); root.mainloop()

if __name__ == "__main__":
    main()
