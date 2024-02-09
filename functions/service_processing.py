import sys
import subprocess

# install_service
def install_service():
    try:
        subprocess.run(['python', 'functions/scanner_service_win.py', 'install'], shell=True, check=True)
        print("Служба успешно установлена.")
    except subprocess.CalledProcessError:
        print("Ошибка при установке службы.")
        sys.exit(1)

# uninstall_service
def uninstall_service():
    try:
        subprocess.run(['python', 'functions/scanner_service_win.py', 'remove'], shell=True, check=True)
        print("Служба успешно удалена.")
    except subprocess.CalledProcessError:
        print("Ошибка при удалении службы.")
        sys.exit(1)

def start_service():
    subprocess.run(['python', 'functions/scanner_service_win.py', 'start'], shell=True)

def stop_service():
    subprocess.run(['python', 'functions/scanner_service_win.py', 'stop'], shell=True)
