# main.py
import PySimpleGUI as sg #GUI библиотека
import threading #мультипоточность
import time

from functions.save_load import save_config, load_config
from functions.autorun import set_autostartup
from functions.db_update import database_update
from functions.scanner import start_service, stop_service
from functions.install_service import install_service
from functions.uninstall_service import uninstall_service

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

def create_scan_layout(): #отрисовка экрана сканирования
    return [
        [sg.Text('Выберите тип сканирования:', font=('Helvetica', 14))],
        [sg.Button('Проверка файла', size=(30, 2), font=('Helvetica', 12), key='-SCAN_FILE-', tooltip=('Сканирование выбранного файла'))],
        [sg.Button('Сканирование директории', size=(30, 2), font=('Helvetica', 12), key='-SCAN_DIRECTORY-', tooltip=('Сканирование выбранной папки'))],
        [sg.Button('Полное сканирование', size=(30, 2), font=('Helvetica', 12), key='-FULL_SCAN-', tooltip=('Сканирование всех дисков'))],
    ]

def create_update_layout(): #отрисовка экрана обновления базы данных
    return [
        [sg.Text('Обновление базы данных', font=('Helvetica', 14))],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS_UPDATE-')],
        [sg.Button('Начать обновление', size=(20, 2), font=('Helvetica', 12), key='-START_DB_UPDATE-')]
    ]

def create_settings_layout(theme): #отрисовка экрана настроек
    #выставляем значения из конфига
    auto_update = load_config('AutoUpdate') == 'True' 
    auto_startup = load_config('AutoStartup') == 'True'
    return [
        [sg.Text('Настройки антивируса', font=('Helvetica', 14))],
        [sg.Text('Тема', font=('Helvetica', 12))],
        [sg.Combo(['Default1', 'Black', 'Reddit', 'BlueMono', 'DarkGrey14'], default_value=theme, key='-THEME-')],
        [sg.Checkbox('Автоматически обновлять базу данных', default=auto_update, key='-AUTO_UPDATE-', font=('Helvetica', 12))],
        [sg.Checkbox('Запускать при старте Windows', default=auto_startup, key='-AUTO_STARTUP-', font=('Helvetica', 12))],
        [sg.Button('Сохранить настройки', size=(20, 2), font=('Helvetica', 12), key='-SAVE_SETTINGS-')]
    ]

def create_dev_layout(): #отрисовка хрени для разрабов
    return [
        [sg.Text('Для разработчиков', font=('Helvetica', 14))],
        [sg.Text('Просмотр всех существующий тем', font=('Helvetica', 12))],
        [sg.Button('Все темы', size=(20, 2), font=('Helvetica', 12), key='-THEME_PREVIEWER-')],
        [sg.Text('Управление службой', font=('Helvetica', 12))],
        [sg.Button('Установить службу', size=(20, 2), font=('Helvetica', 12), key='-INSTALL_SERVICE-', button_color=('black', 'green'))],
        [sg.Button('Удалить службу', size=(20, 2), font=('Helvetica', 12), key='-UNINSTALL_SERVICE-', button_color=('black', 'red'))]
    ]

def show_scan_layout():
    layout = [
        [sg.Text('Прогресс сканирования:', font=('Helvetica', 14))],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS-')],
        [sg.Text('Сканирование завершено!', font=('Helvetica', 14), key='-DONE-')],
        [sg.Button('Отмена', size=(10, 2), font=('Helvetica', 12), key='-CANCEL_SCAN-'), sg.Button('Готово', size=(10, 2), font=('Helvetica', 12), key='-DONE_SCAN-')]
    ]
    window = sg.Window('Сканирование', layout, finalize=True)
    progress_bar = window['-PROGRESS-']
    cancel_scan = window['-CANCEL_SCAN-']
    done_scan = window['-DONE_SCAN-']

    window['-DONE_SCAN-'].update(visible=False)
    window['-DONE-'].update(visible=False)
    window.TKroot.grab_set()
    for i in range(100):
        time.sleep(0.1)  # Имитация сканирования
        window['-PROGRESS-'].update_bar(i + 1)  # Обновляем прогрессбар
        event, values = window.read(timeout=0)
        if event == sg.WIN_CLOSED or event == '-CANCEL_SCAN-':
                window.TKroot.grab_release()
                window.close()
                return  # Если окно закрыли, завершаем сканирование

    window['-CANCEL_SCAN-'].update(visible=False)
    window['-DONE_SCAN-'].update(visible=True)
    window['-DONE-'].update(visible=True)

    while True:
        event, values = window.read(timeout=100)

        if event == sg.WIN_CLOSED or event == '-DONE_SCAN-':
            window.TKroot.grab_release()
            window.close()
            break
            
def run_scan_and_show_progress(window, values):
    scan_thread = threading.Thread(target=start_service)
    scan_thread.start()
    show_scan_layout()
    stop_service()

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
        '-THEME_PREVIEWER-': sg.theme_previewer
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