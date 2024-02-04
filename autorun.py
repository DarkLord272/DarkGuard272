# autorun.py
import sys
import os
import winreg as reg

def set_autostartup(enable):
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    app_name = "DarkGuard272"
    executable_path = sys.executable
    script_path = os.path.abspath(__file__)

    if enable:
        # Set autostartup
        try:
            key_handle = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(key_handle, app_name, 0, reg.REG_SZ, f'"{executable_path}"')
            reg.CloseKey(key_handle)
        except Exception as e:
            print(f"Error setting autostartup: {e}")
    else:
        # Remove autostartup
        try:
            key_handle = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
            reg.DeleteValue(key_handle, app_name)
            reg.CloseKey(key_handle)
        except Exception as e:
            print(f"Error removing autostartup: {e}")

if __name__ == "__main__":
    # При запуске файла автозапуска, устанавливаем приложение в автозапуск
    set_autostartup(True)
