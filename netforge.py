import tkinter as tk
import threading
import time

import scanner
from ui import UI


devices_cache = []


def scan_loop(ui):

    global devices_cache

    while True:
        devices_cache = scanner.scan_network()
        ui.update(devices_cache)

        time.sleep(5)


def main():

    root = tk.Tk()
    ui = UI(root)

    thread = threading.Thread(target=scan_loop, args=(ui,))
    thread.daemon = True
    thread.start()

    root.mainloop()


if __name__ == "__main__":
    main()
