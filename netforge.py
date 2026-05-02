import tkinter as tk
from tkinter import ttk
import threading
import time

import scanner


SCAN_INTERVAL = 5

devices_cache = {}


# ======================
# SCAN LOOP
# ======================

def update_scan():
    global devices_cache
    devices_cache = scanner.scan_network()


def loop_scanner(tree):

    while True:
        update_scan()
        refresh_ui(tree)
        time.sleep(SCAN_INTERVAL)


# ======================
# UI UPDATE
# ======================

def refresh_ui(tree):

    tree.delete(*tree.get_children())

    for ip, data in devices_cache.items():

        ports = ", ".join(data["ports"]) if data["ports"] else "unknown"

        tree.insert("", "end", values=(ip, data["status"], ports))


# ======================
# GUI
# ======================

def build_gui():

    root = tk.Tk()
    root.title("NetForge - 2 File Edition")
    root.geometry("800x500")

    label = tk.Label(root, text="NETFORGE", font=("Arial", 18))
    label.pack(pady=10)

    cols = ("IP", "STATUS", "PORTS")

    tree = ttk.Treeview(root, columns=cols, show="headings")

    for c in cols:
        tree.heading(c, text=c)

    tree.pack(fill="both", expand=True)

    btn = tk.Button(
        root,
        text="Manual Scan",
        command=lambda: update_scan()
    )
    btn.pack(pady=10)

    thread = threading.Thread(target=loop_scanner, args=(tree,))
    thread.daemon = True
    thread.start()

    root.mainloop()


if __name__ == "__main__":
    build_gui()
