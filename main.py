# main.py
import PySimpleGUI as sg #GUI библиотека

from functions.config import save_config, load_config
from functions.autorun import set_autostartup
from functions.db_update import database_update
from functions.service_processing import install_service, uninstall_service, stop_service
from functions.layouts import create_scan_layout, create_update_layout, create_settings_layout, create_dev_layout
from functions.develop_def import run_scan_and_show_progress

def create_main_layout(theme): #отрисовка главного экрана
    return [
        [sg.Text('DarkGuard272', font=('Helvetica', 20), justification='center')],
        [sg.TabGroup([
            [sg.Tab('Сканирование', create_scan_layout())],
            [sg.Tab('Обновление', create_update_layout())],
            [sg.Tab('Настройки', create_settings_layout(theme))],
            [sg.Tab('Для разработчиков', create_dev_layout())]
        ], font=('Helvetica', 12), size=(600, 405))]
    ]

def save_settings(window, values):
    theme = values['-THEME-']
    sg.theme(theme)
    save_config('Theme', theme)

    auto_update = values['-AUTO_UPDATE-']
    save_config('AutoUpdate', str(auto_update))
    
    auto_startup = values['-AUTO_STARTUP-']
    save_config('AutoStartup', str(auto_startup))
    set_autostartup(auto_startup)
    
    sg.popup('Настройки сохранены!')
    window.close()
    layout = create_main_layout(theme)
    window = sg.Window('DarkGuard272', layout, size=(600, 500))

def main(): #главная шайтан машина, в которой все крутится и настраивается
    #загружаем тему из конфига
    theme = load_config('Theme')
    
    #устанавливаем тему
    sg.theme(theme)

    #загружаем параметр автозагрузки из конфига
    auto_startup = load_config('AutoStartup') == 'True'
    if auto_startup:
        set_autostartup(True)

    layout = create_main_layout(theme)

    #название проги и размеры окна
    window = sg.Window('DarkGuard272', layout, size=(600, 500))

    actions = {
        '-FULL_SCAN-': run_scan_and_show_progress,
        '-SCAN_DIRECTORY-': run_scan_and_show_progress,
        '-SCAN_FILE-': run_scan_and_show_progress,
        '-INSTALL_SERVICE-': install_service,
        '-UNINSTALL_SERVICE-': uninstall_service,
        '-START_DB_UPDATE-': database_update,
        '-SAVE_SETTINGS-': save_settings,
    }

    while True:
        #порочный круг, в котором работают кнопки
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            stop_service()
            break
        
        if event in actions:
            actions[event](window, values)  # Вызываем соответствующую функцию из словаря

    window.close()

if __name__ == "__main__":
    main()