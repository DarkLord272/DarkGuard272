import subprocess

def start_service():
    subprocess.run(['python', 'functions/scanner_service_win.py', 'start'], shell=True)

def stop_service():
    subprocess.run(['python', 'functions/scanner_service_win.py', 'stop'], shell=True)
