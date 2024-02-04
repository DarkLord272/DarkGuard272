# scanner_service_win.py
import os
import servicemanager
import socket
import sys
import win32event
import win32service
import win32serviceutil
import win32timezone

class ScannerService(win32serviceutil.ServiceFramework):
    _svc_name_ = 'DarkGuardScanner'
    _svc_display_name_ = 'DarkGuard Scanner'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):
        # Добавьте здесь нужные действия или цикл
        i=0
        while i<10:
            win32event.WaitForSingleObject(self.hWaitStop, 1000)  # Пауза на 1 секунду
            i=i+1

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ScannerService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ScannerService)
