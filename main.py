import PySimpleGUI as sg
import configparser

CONFIG_FILE = 'darkguard_config.ini'

def create_main_layout(theme):
    return [
        [sg.Text('DarkGuard272', font=('Helvetica', 20), justification='center')],
        [sg.TabGroup([
            [sg.Tab('Сканирование', create_scan_layout())],
            [sg.Tab('Обновление', create_update_layout())],
            [sg.Tab('Настройки', create_settings_layout(theme))],
            [sg.Tab('Для разработчиков', create_dev_layout())]
        ], font=('Helvetica', 12))]
    ]

def create_scan_layout():
    return [
        [sg.Text('Выберите тип сканирования:', font=('Helvetica', 14))],
        [sg.Radio('Полное сканирование', 'SCAN_TYPE', key='-FULL_SCAN-', default=True, font=('Helvetica', 12))],
        [sg.Radio('Быстрое сканирование', 'SCAN_TYPE', key='-QUICK_SCAN-', font=('Helvetica', 12))],
        [sg.Button('Начать сканирование', size=(20, 2), font=('Helvetica', 12))]
    ]

def create_update_layout():
    return [
        [sg.Text('Обновление базы данных', font=('Helvetica', 14))],
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROGRESS-')],
        [sg.Button('Начать обновление', size=(20, 2), font=('Helvetica', 12))]
    ]

def create_settings_layout(theme):
    return [
        [sg.Text('Настройки антивируса', font=('Helvetica', 14))],
        [sg.Combo(['Default1', 'Black', 'Reddit', 'BlueMono', 'DarkGrey14'], default_value=theme, key='-THEME-')],
        [sg.Checkbox('Автоматически обновлять базу данных', default=True, key='-AUTO_UPDATE-', font=('Helvetica', 12))],
        [sg.Button('Сохранить настройки', size=(20, 2), font=('Helvetica', 12))]
    ]

def create_dev_layout():
    return [
        [sg.Text('Для разработчиков', font=('Helvetica', 14))],
        [sg.Button('Все темы', size=(20, 2), font=('Helvetica', 12), key='-THEME_PREVIEWER-')]
    ]

def save_config(theme):
    config = configparser.ConfigParser()
    config['Settings'] = {'Theme': theme}
    with open(CONFIG_FILE, 'w') as config_file:
        config.write(config_file)

def load_config():
    config = configparser.ConfigParser()
    try:
        config.read(CONFIG_FILE)
        if 'Settings' in config and 'Theme' in config['Settings']:
            return config['Settings']['Theme']
    except Exception as e:
        print(f"Error loading config: {e}")
    return 'Default1'  # Значение по умолчанию

def main():
    theme = load_config()
    if theme not in ['Default1', 'Black', 'Reddit', 'BlueMono', 'DarkGrey14']:
            theme = 'Default1'
    sg.theme(theme)

    layout = create_main_layout(theme)
    window = sg.Window('DarkGuard272', layout, size=(600, 500))

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED or event == 'Выход':
            break
        elif event == 'Начать сканирование':
            sg.popup('Сканирование в процессе...')
        elif event == 'Начать обновление':
            for i in range(100):
                window['-PROGRESS-'].update_bar(i + 1)
            sg.popup('Обновление завершено!')
        elif event == 'Сохранить настройки':
            theme = values['-THEME-']
            sg.theme(theme)
            save_config(theme)
            sg.popup('Настройки сохранены!')
            window.close()
            layout = create_main_layout(theme)
            window = sg.Window('DarkGuard272', layout, size=(600, 500))
        elif event == '-THEME_PREVIEWER-':
            sg.theme_previewer()

    window.close()

if __name__ == "__main__":
    main()
