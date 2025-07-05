import csv
from datetime import datetime
from typing import Dict

def save_report_txt(vuln_report: Dict[int, Dict], target: str):
    """
    Saves the vulnerability report as a human-readable .txt file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"vuln_report_{target}_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(f"Vulnerability Scan Report for {target}\n")
        f.write("=" * 50 + "\n\n")

        for port, info in sorted(vuln_report.items()):
            f.write(f"Port: {port}\n")
            f.write(f"Service: {info.get('service', 'Unknown')}\n")
            f.write(f"Banner: {info.get('banner', '')}\n")
            f.write(f"Risk: {info.get('risk', 'N/A')}\n")
            f.write(f"Notes: {info.get('notes', '')}\n")

            # If CVEs present
            cves = info.get('cves', [])
            if cves:
                f.write("CVEs:\n")
                for cve_id, desc in cves:
                    f.write(f"  - {cve_id}: {desc}\n")

            f.write("-" * 50 + "\n")

    print(f"TXT report saved as: {filename}")


def save_report_csv(vuln_report: Dict[int, Dict], target: str):
    """
    Saves the vulnerability report as a .csv file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"vuln_report_{target}_{timestamp}.csv"

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Port", "Service", "Banner", "Risk", "Notes", "CVEs"])

        for port, info in sorted(vuln_report.items()):
            cves = info.get("cves", [])
            cve_text = "; ".join([f"{cve_id}: {desc}" for cve_id, desc in cves]) if cves else ""

            writer.writerow([
                port,
                info.get('service', 'Unknown'),
                info.get('banner', ''),
                info.get('risk', 'N/A'),
                info.get('notes', ''),
                cve_text
            ])

    print(f"CSV report saved as: {filename}")


# Example usage
if __name__ == "__main__":
    target = "localhost"
    vuln_report = {
        22: {
            'service': 'SSH',
            'banner': 'SSH-2.0-OpenSSH_8.2',
            'risk': 'Low',
            'notes': 'Secure version detected.',
            'cves': [
                ('CVE-2020-15778', 'OpenSSH scp arbitrary file write vulnerability.')
            ]
        },
        21: {
            'service': 'FTP',
            'banner': '220-FileZilla Server ready',
            'risk': 'High',
            'notes': 'Plain FTP. Needs verification.',
            'cves': []
        },
        8000: {
            'service': 'HTTP',
            'banner': '',
            'risk': 'Medium',
            'notes': 'Unencrypted HTTP.',
        }
    }

    save_report_txt(vuln_report, target)
    save_report_csv(vuln_report, target)
