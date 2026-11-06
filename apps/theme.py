BG, BG2, SURF, ACC, HOV, TXT, TXT2, BORDER = "#171717", "#202020", "#292929", "#FF781F", "#FF914D", "#F2F2F2", "#A0A0A0", "#3A3A3A"

def style(root):
    from tkinter import ttk
    root.configure(bg=BG); st = ttk.Style(root); st.theme_use("clam")
    st.configure("Treeview", background=SURF, fieldbackground=SURF, foreground=TXT, rowheight=28, borderwidth=0)
    st.map("Treeview", background=[("selected", ACC)], foreground=[("selected", BG)])
    st.configure("Treeview.Heading", background=BG2, foreground=TXT2)
    st.configure("TButton", background=ACC, foreground=BG, padding=8, borderwidth=0)
    st.map("TButton", background=[("active", HOV)])
