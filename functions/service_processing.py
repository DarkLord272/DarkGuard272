import subprocess
import win32serviceutil
import win32service


def install_service(window, values):
    subprocess.run(['python', 'functions/scanner_service_win.py', 'install'], shell=True)

def uninstall_service(window, values):
    subprocess.run(['python', 'functions/scanner_service_win.py', 'remove'], shell=True)

def start_service():
    subprocess.run(["sc", "start", "DarkGuard272"], shell=True)

def stop_service():
    subprocess.run(['python', 'functions/scanner_service_win.py', 'stop'], shell=True)