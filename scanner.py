import socket
import ipaddress

COMMON_PORTS = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    445: "SMB"
}

NETWORK = "192.168.1.0/24"


def is_host_alive(ip):
    try:
        socket.create_connection((str(ip), 80), timeout=0.2)
        return True
    except:
        return False


def scan_ports(ip):
    open_ports = []

    for port, name in COMMON_PORTS.items():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.2)

            if sock.connect_ex((str(ip), port)) == 0:
                open_ports.append(f"{port}:{name}")

            sock.close()
        except:
            pass

    return open_ports


def scan_network():
    devices = {}

    net = ipaddress.ip_network(NETWORK, strict=False)

    for ip in net.hosts():

        ip_str = str(ip)

        if is_host_alive(ip):

            devices[ip_str] = {
                "ip": ip_str,
                "ports": scan_ports(ip),
                "status": "alive"
            }

    return devices
