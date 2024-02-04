# main.py
import PySimpleGUI as sg #GUI библиотека
import configparser #Управление конфигурационным файлом
import os #Работа с операционной системой
from save_load import save_config, load_config
from scanner import full_scan, quick_scan
from autorun import set_autostartup
from db_update import database_update

def create_main_layout(theme): #отрисовка главного экрана
    return [
        [sg.Text('DarkGuard272', font=('Helvetica', 20), justification='center')],
        [sg.TabGroup([
            [sg.Tab('Сканирование', create_scan_layout())],
            [sg.Tab('Обновление', create_update_layout())],
            [sg.Tab('Настройки', create_settings_layout(theme))],
            [sg.Tab('Для разработчиков', create_dev_layout())]
        ], font=('Helvetica', 12))]
    ]

def create_scan_layout(): #отрисовка экрана сканирования
    return [
        [sg.Text('Выберите тип сканирования:', font=('Helvetica', 14))],
        [sg.Radio('Полное сканирование', 'SCAN_TYPE', key='-FULL_SCAN-', default=True, font=('Helvetica', 12))],
        [sg.Radio('Быстрое сканирование', 'SCAN_TYPE', key='-QUICK_SCAN-', font=('Helvetica', 12))],
        [sg.Button('Начать сканирование', size=(20, 2), font=('Helvetica', 12))]
    ]

def create_update_layout(): #отрисовка экрана обновления базы данных
    return [
        [sg.Text('Обновление базы данных', font=('Helvetica', 14))],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS-')],
        [sg.Button('Начать обновление', size=(20, 2), font=('Helvetica', 12))]
    ]

def create_settings_layout(theme): #отрисовка экрана настроек
    #выставляем значения из конфига
    auto_update = load_config('AutoUpdate') == 'True' 
    auto_startup = load_config('AutoStartup') == 'True'
    return [
        [sg.Text('Настройки антивируса', font=('Helvetica', 14))],
        [sg.Combo(['Default1', 'Black', 'Reddit', 'BlueMono', 'DarkGrey14'], default_value=theme, key='-THEME-')],
        [sg.Checkbox('Автоматически обновлять базу данных', default=auto_update, key='-AUTO_UPDATE-', font=('Helvetica', 12))],
        [sg.Checkbox('Запускать при старте Windows', default=auto_startup, key='-AUTO_STARTUP-', font=('Helvetica', 12))],
        [sg.Button('Сохранить настройки', size=(20, 2), font=('Helvetica', 12))]
    ]

def create_dev_layout(): #отрисовка хрени для разрабов
    return [
        [sg.Text('Для разработчиков', font=('Helvetica', 14))],
        [sg.Button('Все темы', size=(20, 2), font=('Helvetica', 12), key='-THEME_PREVIEWER-')]
    ]

def main(): #главная шайтан машина, в которой все крутится и настраивается
    theme = load_config('Theme')
    auto_startup = load_config('AutoStartup') == 'True'
    sg.theme(theme)

    if auto_startup:
        set_autostartup(True)

    layout = create_main_layout(theme)
    #название проги и размеры окна
    window = sg.Window('DarkGuard272', layout, size=(600, 500))

    while True:
        #порочный круг, в котором работают кнопки
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Выход':
            break
        elif event == 'Начать сканирование':
            if values['-FULL_SCAN-']:
                full_scan()
            elif values['-QUICK_SCAN-']:
                quick_scan()
        elif event == 'Начать обновление':
            database_update(window)
        elif event == 'Сохранить настройки':
            theme = values['-THEME-']
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
        elif event == '-THEME_PREVIEWER-':
            sg.theme_previewer()

    window.close()

if __name__ == "__main__":
    main()
