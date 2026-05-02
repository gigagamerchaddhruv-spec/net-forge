import socket
import ipaddress
import threading
import tkinter as tk
from tkinter import scrolledtext

# =========================
# CONFIG
# =========================

NETWORK = "192.168.1.0/24"

# =========================
# CORE SCANNER
# =========================

def is_host_up(ip):
    try:
        socket.create_connection((str(ip), 80), timeout=0.3)
        return True
    except:
        return False


def scan_network(output_box):
    output_box.insert(tk.END, f"Scanning {NETWORK}...\n\n")

    net = ipaddress.ip_network(NETWORK, strict=False)

    for ip in net.hosts():

        if is_host_up(ip):
            msg = f"[+] Device found: {ip}\n"
            output_box.insert(tk.END, msg)
            output_box.see(tk.END)

    output_box.insert(tk.END, "\nScan complete.\n")


# =========================
# GUI LOGIC
# =========================

def start_scan(output_box):
    thread = threading.Thread(target=scan_network, args=(output_box,))
    thread.daemon = True
    thread.start()


def build_gui():
    window = tk.Tk()
    window.title("NetForge - Network Scanner")
    window.geometry("600x400")

    title = tk.Label(window, text="NetForge", font=("Arial", 18))
    title.pack(pady=10)

    scan_btn = tk.Button(
        window,
        text="Scan Network",
        font=("Arial", 12),
        command=lambda: start_scan(output_box)
    )
    scan_btn.pack(pady=10)

    output_box = scrolledtext.ScrolledText(window, width=70, height=15)
    output_box.pack(padx=10, pady=10)

    window.mainloop()


# =========================
# RUN
# =========================

if __name__ == "__main__":
    build_gui()
