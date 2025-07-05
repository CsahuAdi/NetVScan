import socket
import ssl
from typing import Dict

import socket

def get_service_name(port: int) -> str:
    """
    Return service name from port using system's /etc/services.
    Falls back to 'Unknown' if not found.
    """
    try:
        return socket.getservbyport(port)
    except Exception:
        return "Unknown"

def grab_http_banner(target: str, port:int = 80, timeout:float = 3.0) :
    """
    Connect to HTTP port 80 and read the welcome banner
    """
    try :
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s :
            s.settimeout(timeout)
            s.connect((target, port))
            s.sendall(b"HEAD / HTTP/1.0\r\nHost: %b\r\n\r\n" % target.encode())
            response = s.recv(4096).decode(errors="ignore")
            return response or "(no response)"
    except Exception as e :
        return f"(error : {e})"

def grab_https_banner(target: str, port: int = 443, timeout: float = 3.0) :
    """
    Connect to HTTPS port 443, send HEAD request over SSL and read the response
    """
    context = ssl.create_default_context()
    try:
        with socket.create_connection((target, port), timeout=timeout) as sock:
            with context.wrap_socket(sock, server_hostname=target) as ssock:
                ssock.settimeout(timeout)
                ssock.sendall(b"HEAD / HTTP/1.1\r\nHost: %b\r\n\r\n" % target.encode())
                response = ssock.recv(4096).decode(errors='ignore')
                return response or "(no response)"
    except Exception as e:
        return f"(error: {e})"

def grab_banner(target: str, port: int, timeout: float = 1.0) -> str:
    """
    Connect to the target:port and try to grab the banner string.
    Returns the banner text if available, or empty string.
    """
    if port in [80, 8000, 8080] :
        return grab_http_banner(target, port, timeout)
    elif port == 443 :
        return grab_https_banner(target, port, timeout)
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
        service = get_service_name(port).upper()
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
    target = input("Enter HTTPS target (e.g., google.com): ").strip()
    banner = grab_https_banner(target)
    print(f"\nHTTPS Banner for {target}:\n{banner}")