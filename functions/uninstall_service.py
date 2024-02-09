# uninstall_service.py
import sys
import subprocess

def uninstall_service():
    try:
        subprocess.run(['python', 'functions/scanner_service_win.py', 'remove'], shell=True, check=True)
        print("Служба успешно установлена.")
    except subprocess.CalledProcessError:
        print("Ошибка при установке службы.")
        sys.exit(1)

if __name__ == '__main__':
    uninstall_service()
