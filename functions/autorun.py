# autorun.py
import sys
import os
import winreg as reg

def set_autostartup(enable):
    key = r"Software\Microsoft\Windows\CurrentVersion\Run" #реестровый путь до папки автозапуска
    app_name = "DarkGuard272"
    executable_path = sys.executable
    script_path = os.path.abspath(__file__)

    if enable:
        #врубаем автозапуск и добавляем процесс в реестровую папку
        try:
            key_handle = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
            reg.SetValueEx(key_handle, app_name, 0, reg.REG_SZ, f'"{executable_path}"')
            reg.CloseKey(key_handle)
        except Exception as e:
            print(f"Error setting autostartup: {e}")
    else:
        #вырубаем автозапуск и удаляем процесс из реестровой папки
        try:
            key_handle = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
            reg.DeleteValue(key_handle, app_name)
            reg.CloseKey(key_handle)
        except Exception as e:
            print(f"Error removing autostartup: {e}")

if __name__ == "__main__":
    #при запуске файла автозапуска, устанавливаем приложение в автозапуск
    set_autostartup(True)
