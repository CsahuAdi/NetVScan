import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
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
        except:
            return False


def scan_ports(target: str, ports: List[int], timeout: float = 1.0, max_workers: int = 100) -> Dict[int, str]:
    """
    Scan a list of ports on the target host using multithreading.
    Return a dict of open ports and their state.
    """
    open_ports = {}
    print(f"\nScanning {len(ports)} ports on {target} with up to {max_workers} threads...\n")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {
            executor.submit(scan_port, target, port, timeout): port for port in ports
        }

        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                if future.result():
                    print(f"[OPEN] Port {port}")
                    open_ports[port] = 'open'
            except Exception as e:
                print(f"[ERROR] Port {port}: {e}")

    return open_ports


if __name__ == "__main__":
    # Example usage
    target = input("Enter target IP/hostname: ").strip()
    ports = list(range(1, 1025))

    results = scan_ports(target, ports)
    print(f"\nScan complete. Open ports: {list(results.keys())}")
