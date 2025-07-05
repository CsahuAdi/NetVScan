import csv
from datetime import datetime
from typing import Dict

def save_report_txt(vuln_report: Dict[int, Dict[str, str]], target: str):
    """
    Saves the vulnerability report as a human-readable .txt file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"vuln_report_{target}_{timestamp}.txt"

    with open(filename, "w") as f:
        f.write(f"Vulnerability Scan Report for {target}\n")
        f.write("="*50 + "\n\n")

        for port, info in sorted(vuln_report.items()):
            f.write(f"Port: {port}\n")
            f.write(f"Service: {info['service']}\n")
            f.write(f"Banner: {info['banner']}\n")
            f.write(f"Risk: {info['risk']}\n")
            f.write(f"Notes: {info['notes']}\n")
            f.write("-"*50 + "\n")
    
    print(f"TXT report saved as: {filename}")


def save_report_csv(vuln_report: Dict[int, Dict[str, str]], target: str):
    """
    Saves the vulnerability report as a .csv file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"vuln_report_{target}_{timestamp}.csv"

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Port", "Service", "Banner", "Risk", "Notes"])

        for port, info in sorted(vuln_report.items()):
            writer.writerow([
                port,
                info['service'],
                info['banner'],
                info['risk'],
                info['notes']
            ])
    
    print(f"CSV report saved as: {filename}")


# Example usage:
if __name__ == "__main__":
    # Simulated input
    target = "localhost"
    vuln_report = {
        22: {'service': 'SSH', 'banner': 'SSH-2.0-OpenSSH_8.2', 'risk': 'Low', 'notes': 'Secure version detected. Needs verification.'},
        21: {'service': 'FTP', 'banner': '220-FileZilla Server ready', 'risk': 'High', 'notes': 'Plain FTP. Needs verification.'},
        8000: {'service': 'HTTP', 'banner': '', 'risk': 'Medium', 'notes': 'Unencrypted HTTP. Needs verification.'}
    }

    save_report_txt(vuln_report, target)
    save_report_csv(vuln_report, target)
