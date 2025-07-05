from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__)


def run_command(cmd):
    """
    Run a shell command and return its output.
    """
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return e.output.strip()


def service_status(name):
    """
    Check the status of a Windows service.
    Returns: 'Running', 'Stopped', or 'Unknown'
    """
    output = run_command(f'sc query {name}')
    output_lower = output.lower()
    if "running" in output_lower:
        return "Running"
    elif "stopped" in output_lower:
        return "Stopped"
    else:
        return "Unknown"


@app.route("/")
def home():
    ssh_status = service_status("sshd")
    ftp_status = service_status("filezilla-server")
    return render_template("dashboard.html", ssh_status=ssh_status, ftp_status=ftp_status)


@app.route("/start/<service>")
def start_service(service):
    if service == "ssh":
        result = run_command("net start sshd")
    elif service == "ftp":
        result = run_command("net start filezilla-server")
    print(result)
    return redirect(url_for("home"))


@app.route("/stop/<service>")
def stop_service(service):
    if service == "ssh":
        result = run_command("net stop sshd")
    elif service == "ftp":
        result = run_command("net stop filezilla-server")
    print(result)
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
