import ipaddress
from typing import List
from concurrent.futures import ThreadPoolExecutor
from port_scanner import scan_ports

def get_hosts_from_cidr(cidr: str) -> List[str] :
    """
    Generate list of hosts from CIDR block.
    """
    network = ipaddress.ip_network(cidr, strict = False)
    return [str[ip] for ip in network.hosts()]

def scan_host(host: str, ports: List[int], timeout: float =1.0) -> dict :
    """
    Scan a single host and return its open ports.
    """
    open_ports = scan_ports(host, ports, timeout)
    return {host: open_ports}

def scan_subnet(cidr: str, ports: List[int], timeout: float = 1.0, max_workers: int = 10) -> dict :
    """
    Scan all hosts in a CIDR subnet in parallel.
    """
    results = {}
    hosts = get_hosts_from_cidr(cidr)
    print(f"{len(hosts)} hosts in subnet {cidr}...")

    with ThreadPoolExecutor(max_workers=max_workers) as executor :
        futures = {executor.submit(scan_host, host, ports, timeout) : host for host in hosts}
        for future in futures :
            host_result = future.result()
            results.update(host_result)

    return results

