import platform
import subprocess
import ipaddress

NETWORK = "192.168.1.0/24"


def ping(ip):
    system = platform.system().lower()

    if system == "windows":
        cmd = ["ping", "-n", "1", "-w", "500", str(ip)]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", str(ip)]

    try:
        output = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if output.returncode == 0:

            # very simple latency extraction
            text = output.stdout

            for line in text.splitlines():
                if "time=" in line:
                    return line.split("time=")[1].split(" ")[0]

            return "ok"

    except:
        pass

    return None


def scan_network():
    devices = []

    net = ipaddress.ip_network(NETWORK, strict=False)

    for ip in net.hosts():

        latency = ping(ip)

        if latency:
            devices.append({
                "ip": str(ip),
                "latency": latency
            })

    return devices
