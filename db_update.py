# db_update.py
import PySimpleGUI as sg
import time

#иммитация обновления базы данных 
def database_update(window):
    #типа че-то делается
    for i in range(100):
        window['-PROGRESS-'].update_bar(i + 1)
        time.sleep(0.1)
    sg.popup('Обновление завершено!')
    window['-PROGRESS-'].update_bar(0)
