import PySimpleGUI as sg #GUI библиотека
import time

from functions.config import load_config

def create_scan_layout(): #отрисовка экрана сканирования
    return [
        [sg.Text('Выберите тип сканирования:', font=('Helvetica', 14))],
        [sg.Button('Проверка файла', size=(30, 2), font=('Helvetica', 12), key='-SCAN_FILE-', tooltip=('Сканирование выбранного файла'))],
        [sg.Button('Сканирование директории', size=(30, 2), font=('Helvetica', 12), key='-SCAN_DIRECTORY-', tooltip=('Сканирование выбранной папки'))],
        [sg.Button('Полное сканирование', size=(30, 2), font=('Helvetica', 12), key='-FULL_SCAN-', tooltip=('Сканирование всех дисков'))],
    ]

def create_update_layout(): #отрисовка экрана обновления базы данных
    last_update_date = load_config('LastUpdate')
    return [
        [sg.Text('Обновление базы данных', font=('Helvetica', 14))],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS_UPDATE-')],
        [sg.Text(f'Последнее обновление: {last_update_date}', key='-LAST_UPDATE-')],
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
    fake_scan(window)
              
def fake_scan(window):
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