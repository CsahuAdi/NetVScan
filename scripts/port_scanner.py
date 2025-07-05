import socket
from typing import List, Dict

import socket
from typing import List, Dict

def scan_port(target: str, port: int, timeout: float = 1.0) -> bool:
    """
    Try to connect to the target on the specified port.
    Return True if port is open, False otherwise.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(timeout)
        try:
            s.connect((target, port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False


def scan_ports(target: str, ports: List[int], timeout: float = 1.0) -> Dict[int, str]:
    """
    Scan a list of ports on the target host.
    Return a dict of open ports and their state.
    """
    open_ports = {}
    print(f"\nScanning {len(ports)} ports on {target}...\n")

    for port in ports:
        if scan_port(target, port, timeout):
            print(f"[OPEN] Port {port}")
            open_ports[port] = 'open'
        else:
            # Optional: print closed ports or keep silent
            pass
    return open_ports


if __name__ == "__main__":
    # Example usage / test
    target = input("Enter target IP/hostname: ").strip()
    ports = list(range(20, 26))  # quick test range

    results = scan_ports(target, ports)
    print(f"\nScan complete. Open ports: {list(results.keys())}")
