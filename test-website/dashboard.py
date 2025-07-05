from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

# Helpers
def run_command(cmd):
    try:
        result = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
        return result.strip()
    except subprocess.CalledProcessError as e:
        return e.output.strip()

def service_status(name):
    output = run_command(f'sc query {name}')
    if "RUNNING" in output:
        return "Running"
    elif "STOPPED" in output:
        return "Stopped"
    else:   
        return "Unknown"

@app.route("/")
def home():
    ssh_status = service_status("sshd")
    ftp_status = service_status("FileZilla Server")
    return render_template("dashboard.html", ssh_status=ssh_status, ftp_status=ftp_status)

@app.route("/start/<service>")
def start_service(service):
    if service == "ssh":
        run_command("net start sshd")
    elif service == "ftp":
        result = run_command('net start "FileZilla Server"')
        if "the system cannot find the path specified" or "the service name is invalid" in result.lower():
            result = run_command(r'"C:\Program Files\FileZilla Server\filezilla-server.exe"')
        print(result)
    return redirect(url_for("home"))

@app.route("/stop/<service>")
def stop_service(service):
    if service == "ssh":
        run_command("net stop sshd")
    elif service == "ftp":
        run_command('net stop "FileZilla Server"')
        if "the system cannot find the path specified" or "the service name is invalid" in result.lower():
            result = run_command(r'taskkill /IM filezilla-server.exe /F')
        print(result)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
