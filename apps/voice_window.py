#!/usr/bin/env python3
"""NEVEXONA Voice Control (Tk): кнопка микрофона, видимый индикатор, подтверждение. GUI не запускалась на экране."""
import os, sys, tempfile
sys.path.insert(0, os.environ.get("NEVEXONA_LIB", "/usr/lib/nevexona"))
from apps import theme
from voice import session, intents, stt

def main():
    import tkinter as tk
    from tkinter import ttk, messagebox
    root = tk.Tk(); root.title("NEVEXONA Voice Control"); root.geometry("560x360"); theme.style(root)
    dot = tk.Label(root, text="● Микрофон выключен", bg=theme.BG, fg=theme.TXT2, font=("DejaVu Sans", 13)); dot.pack(pady=14)
    out = tk.Label(root, text="", bg=theme.BG, fg=theme.TXT, wraplength=520, font=("DejaVu Sans", 12)); out.pack(pady=8)
    def show(r):
        out.config(text=f"{r['status']}\\n«{r['text']}»" if r["text"] else r["status"])
        i = r["intent"]
        if i and (not i.confirm or messagebox.askyesno("Подтверждение", f"Выполнить: {i.name}?")):
            intents.run(i, confirmed=True)
    def listen():
        dot.config(text="● СЛУШАЮ (5 секунд)", fg="#E05252"); root.update()
        r = session.listen_once(os.path.join(tempfile.gettempdir(), "nvx-voice.wav"))
        dot.config(text="● Микрофон выключен", fg=theme.TXT2); show(r)
    ttk.Button(root, text="🎤 Говорить", command=listen).pack(pady=6)
    e = tk.Entry(root, bg=theme.SURF, fg=theme.TXT, insertbackground=theme.TXT); e.pack(fill="x", padx=30, pady=10, ipady=6)
    ttk.Button(root, text="Выполнить текстом", command=lambda: show(session.handle_text(e.get()))).pack()
    tk.Label(root, text=stt.info() if not stt.installed() else "Голосовая модель установлена", bg=theme.BG, fg=theme.TXT2, wraplength=520).pack(pady=12)
    ttk.Button(root, text="Скачать голосовую модель", command=lambda: messagebox.askyesno("Модель", stt.info() + "\\nСкачать?") and stt.download(True)).pack()
    root.mainloop()

if __name__ == "__main__":
    main()
