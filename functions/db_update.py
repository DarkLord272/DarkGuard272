# db_update.py
import PySimpleGUI as sg
import time

#иммитация обновления базы данных 
def database_update(window, values):
    window.TKroot.attributes("-disabled", True)

    #типа че-то делается
    window['-START_DB_UPDATE-'].update(disabled=True)
    for i in range(100):
        time.sleep(0.1)  # Имитация сканирования
        window['-PROGRESS_UPDATE-'].update_bar(i + 1)  # Обновляем прогрессбар
    sg.popup('Обновление завершено!')
    window['-START_DB_UPDATE-'].update(disabled=False)
    window['-PROGRESS_UPDATE-'].update_bar(0)

    window.TKroot.attributes("-disabled", False)
