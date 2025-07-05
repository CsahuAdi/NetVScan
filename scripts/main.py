from input_handler import get_target_ip, get_port_range
from port_scanner import scan_port, scan_ports
from service_detector import detect_services
from vulnerability_checker import assess_vulnerabilities
from report_generator import save_report_csv, save_report_txt

target = get_target_ip()
ports = get_port_range()

open_ports = scan_ports(target, ports)

if open_ports :
    services = detect_services(target, open_ports)
else :
    print("No open ports detected.")

if services :
    vuln_report = assess_vulnerabilities(services)

save_report_txt(vuln_report, target)
save_report_csv(vuln_report, target)
