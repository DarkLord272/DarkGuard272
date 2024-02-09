import PySimpleGUI as sg
import threading

from functions.service_processing import start_service
from functions.layouts import show_scan_layout
from functions.service_processing import start_service, stop_service

def run_scan_and_show_progress(window, values):
    scan_thread = threading.Thread(target=start_service)
    scan_thread.start()
    show_scan_layout()
    stop_service()

