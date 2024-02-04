import subprocess

def uninstall_service():
    subprocess.run(['python', 'functions/scanner_service_win.py', 'remove'], shell=True)