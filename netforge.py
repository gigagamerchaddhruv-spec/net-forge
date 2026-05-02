import socket
import ipaddress
import threading
import time
import tkinter as tk
from tkinter import ttk

# ======================
# CONFIG
# ======================

NETWORK = "192.168.1.0/24"
SCAN_DELAY = 5

COMMON_PORTS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB",
}

devices = {}

# ======================
# CORE SCANNER (CHAOS EDITION)
# ======================

def check_host(ip):
    try:
        socket.create_connection((str(ip), 80), timeout=0.2)
        return True
    except:
        return False


def scan_ports(ip):
    open_ports = []

    for port in COMMON_PORTS.keys():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)
            result = sock.connect_ex((str(ip), port))
            if result == 0:
                open_ports.append(f"{port}:{COMMON_PORTS[port]}")
            sock.close()
        except:
            pass

    return open_ports


def scan_network():
    global devices

    net = ipaddress.ip_network(NETWORK, strict=False)

    for ip in net.hosts():

        ip_str = str(ip)

        if check_host(ip):

            ports = scan_ports(ip)

            devices[ip_str] = {
                "ip": ip_str,
                "ports": ", ".join(ports) if ports else "unknown",
                "status": "alive"
            }


# ======================
# GUI CHAOS
# ======================

def refresh_table(tree):

    tree.delete(*tree.get_children())

    for ip, data in devices.items():
        tree.insert("", "end", values=(data["ip"], data["status"], data["ports"]))


def scan_loop(tree):

    while True:

        scan_network()
        refresh_table(tree)

        time.sleep(SCAN_DELAY)


# ======================
# UI BUILD
# ======================

def build_gui():

    root = tk.Tk()
    root.title("NetForge - Spaghetti Monster Edition")
    root.geometry("800x500")

    title = tk.Label(root, text="NETFORGE", font=("Arial", 20))
    title.pack(pady=10)

    cols = ("IP", "STATUS", "PORTS")

    tree = ttk.Treeview(root, columns=cols, show="headings")

    for c in cols:
        tree.heading(c, text=c)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    btn = tk.Button(
        root,
        text="Force Scan Now (optional chaos button)",
        command=lambda: scan_network()
    )
    btn.pack(pady=5)

    thread = threading.Thread(target=scan_loop, args=(tree,))
    thread.daemon = True
    thread.start()

    root.mainloop()


# ======================
# RUN IT ALL
# ======================

if __name__ == "__main__":
    build_gui()
