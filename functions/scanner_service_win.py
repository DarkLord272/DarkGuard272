import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import sys

class ScannerService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'DarkGuard272'  # Имя службы
    _svc_display_name_ = 'DarkGuard272 Scanner'  # Отображаемое имя службы

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  # Создание события для ожидания остановки службы
        socket.setdefaulttimeout(5)
        self.is_alive = True  # Флаг для отслеживания активности службы

    def SvcStop(self):  # Метод для остановки службы
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)  # Установка события остановки
        self.is_alive = False

    def SvcDoRun(self):  # Метод для запуска службы
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()  # Запуск основной функциональности службы

    def main(self):  # Основная функциональность службы
        while self.is_alive:  # Пока служба активна
            print('Hello')  # Вывод сообщения

if __name__ == '__main__':
    if len(sys.argv) == 1:  # Если скрипт вызван без аргументов
        servicemanager.Initialize()  # Инициализация менеджера служб
        servicemanager.PrepareToHostSingle(ScannerService)  # Подготовка к запуску одиночной службы
        servicemanager.StartServiceCtrlDispatcher()  # Запуск диспетчера управления службами
    else:
        win32serviceutil.HandleCommandLine(ScannerService)  # Обработка командной строки для управления службой
