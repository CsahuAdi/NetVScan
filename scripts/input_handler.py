import ipaddress
import socket
import re

def clean_input(target: str) -> str:
    """
    Remove 'http://' or 'https://' from input if present.
    """
    target = target.strip().lower()
    target = re.sub(r'^https?://', '', target)
    # remove any trailing slash (e.g., www.example.com/)
    target = target
    return target

def resolve_hostname(hostname: str) -> str:
    """
    Resolve a hostname to its IPv4 address.
    Returns the IP address as a string.
    If already an IP, returns it unchanged.
    """
    hostname = clean_input(hostname)
    try:
        # If it’s already a valid IP, return as is
        ipaddress.ip_address(hostname)
        return hostname
    except ValueError:
        pass  # Not an IP, so try DNS

    try:
        ip = socket.gethostbyname(hostname)
        print(f"Resolved hostname '{hostname}' → IP: {ip}")
        return ip
    except socket.gaierror:
        print(f"Unable to resolve hostname: {hostname}")
        return None


def get_target_ip() -> str:
    """
    Prompt user for a target (IP or hostname).
    Validate and resolve to an IP if needed.
    Returns a valid IP or None if invalid.
    """
    while True:
        target = input("Enter target IP address or hostname/URL: ").strip()
        resolved_ip = resolve_hostname(target)
        if resolved_ip:
            print(f"Target resolved and validated: {resolved_ip}")
            return resolved_ip
        else:
            print("Invalid or unresolvable target. Please try again.")


def get_port_range():
    """
    Prompt the user for port range.
    Defaults to common ports if Enter is pressed.
    """
    default_ports = list(range(1, 1025))
    user_input = input("Enter port range (e.g., 20-80) or press Enter for default (1-1024): ").strip()

    if not user_input:
        print("Using default port range: 1-1024")
        return default_ports

    try:
        start, end = map(int, user_input.split('-'))
        if start < 1 or end > 65535 or start > end:
            raise ValueError
        ports = list(range(start, end + 1))
        print(f"Using custom port range: {start}-{end}")
        return ports
    except Exception:
        print("Invalid range. Falling back to default: 1-1024")
        return default_ports


if __name__ == "__main__":
    # Standalone test
    target = get_target_ip()
    ports = get_port_range()
    print(f"\nFinal Input: Target = {target}, Ports = {ports[:10]}{'...' if len(ports) > 10 else ''}")
