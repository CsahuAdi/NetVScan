import socket
from typing import Dict

COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8000: "HTTP-alt",
}

def grab_banner(target: str, port: int, timeout: float = 1.0) -> str:
    """
    Connect to the target:port and try to grab the banner string.
    Returns the banner text if available, or empty string.
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            s.connect((target, port))
            # Some services send banner right away
            banner = s.recv(1024).decode(errors='ignore').strip()
            return banner
    except Exception:
        return ""


def detect_services(target: str, open_ports: Dict[int, str]) -> Dict[int, Dict[str, str]]:
    """
    Given a dict of open ports, return enriched info:
    {
        port: {
            'service': guessed_service_name,
            'banner': banner_text
        }
    }
    """
    results = {}
    print(f"\nDetecting services on open ports...\n")

    for port in open_ports.keys():
        service = COMMON_SERVICES.get(port, "Unknown")
        banner = grab_banner(target, port)

        if banner:
            print(f"[Port {port}] {service} | Banner: {banner}")
        else:
            print(f"[Port {port}] {service} | No banner detected.")

        results[port] = {
            'service': service,
            'banner': banner
        }

    return results


if __name__ == "__main__":
    # Example/test
    target = input("Enter target IP: ").strip()
    open_ports = {22: 'open', 80: 'open', 8000: 'open'}  # fake test data

    enriched = detect_services(target, open_ports)

    print("\nService detection complete.")
    for port, info in enriched.items():
        print(f"Port {port}: {info['service']} | Banner: {info['banner'] or 'N/A'}")