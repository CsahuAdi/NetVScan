import ipaddress
import socket
import re

def clean_input(target: str) -> str:
    """
    Remove 'http://' or 'https://' from input if present.
    """
    target = target.strip().lower()
    target = re.sub(r'^https?://', '', target)
    target = target.rstrip('/')
    return target

def resolve_hostname(hostname: str) -> str:
    """
    Resolve a hostname to its IPv4 address.
    If already an IP, returns as is.
    """
    hostname = clean_input(hostname)
    try:
        ipaddress.ip_address(hostname)
        return hostname
    except ValueError:
        pass  # Not a direct IP — try DNS

    try:
        ip = socket.gethostbyname(hostname)
        print(f"Resolved hostname '{hostname}' → IP: {ip}")
        return ip
    except socket.gaierror:
        print(f"Unable to resolve hostname: {hostname}")
        return None

def validate_cidr(cidr: str) -> str:
    """
    Validate that a string is a proper CIDR.
    If valid, returns it as is.
    """
    try:
        ipaddress.ip_network(cidr, strict=False)
        return cidr
    except ValueError:
        print(f"Invalid CIDR: {cidr}")
        return None

def get_target() -> str:
    """
    Prompt user for a target (single host or CIDR).
    Detects and validates the input accordingly.
    Returns the target string (IP or CIDR).
    """
    while True:
        target = input("Enter target (IP/hostname or CIDR): ").strip()
        if not target:
            print("Please enter a target.")
            continue

        if '/' in target:
            # CIDR
            cidr = validate_cidr(target)
            if cidr:
                print(f"Valid CIDR: {cidr}")
                return cidr
            else:
                print("Invalid CIDR. Please try again.")
        else:
            # Single host
            resolved_ip = resolve_hostname(target)
            if resolved_ip:
                print(f"Target resolved and validated: {resolved_ip}")
                return resolved_ip
            else:
                print("Invalid or unresolvable target. Please try again.")

def get_port_range():
    """
    Prompt the user for port range.
    Defaults to 1-1024 if Enter is pressed.
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
    target = get_target()
    ports = get_port_range()
    print(f"\nFinal Input: Target = {target}, Ports = {ports[:10]}{'...' if len(ports) > 10 else ''}")
