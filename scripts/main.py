from input_handler import get_target, get_port_range
from port_scanner import scan_ports
from subnet_scanner import scan_subnet
from service_detector import detect_services
from vulnerability_checker import assess_vulnerabilities
from report_generator import save_report_txt, save_report_csv

def process_host(host, ports):
    """
    Scan a single host and return vulnerability report.
    """
    open_ports = scan_ports(host, ports)
    if not open_ports:
        print(f"\nNo open ports detected on {host}.")
        return None

    services = detect_services(host, open_ports)
    vuln_report = assess_vulnerabilities(services)

    save_report_txt(vuln_report, host)
    save_report_csv(vuln_report, host)

    return vuln_report


if __name__ == "__main__":
    target = get_target()
    ports = get_port_range()

    if "/" in target:
        # CIDR — scan subnet
        results = scan_subnet(target, ports)
        for host, open_ports in results.items():
            if not open_ports:
                print(f"\nNo open ports detected on {host}.")
                continue

            services = detect_services(host, open_ports)
            vuln_report = assess_vulnerabilities(services)
            save_report_txt(vuln_report, host)
            save_report_csv(vuln_report, host)

    else:
        # Single host
        process_host(target, ports)
