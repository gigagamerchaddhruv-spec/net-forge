import tkinter as tk
from tkinter import ttk


class UI:
    def __init__(self, root):
        self.root = root
        self.tree = None

        self.setup()

    def setup(self):
        self.root.title("NetForge - Ping Mode")
        self.root.geometry("600x400")

        label = tk.Label(self.root, text="NETFORGE", font=("Arial", 18))
        label.pack(pady=10)

        cols = ("IP", "Latency (ms)")

        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c)

        self.tree.pack(fill="both", expand=True)

    def update(self, devices):

        self.tree.delete(*self.tree.get_children())

        for d in devices:
            self.tree.insert("", "end", values=(d["ip"], d["latency"]))
