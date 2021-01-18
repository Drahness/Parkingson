import datetime

from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QSizePolicy, QFrame

from GUI.QtRoundProgressBar import QRoundProgressBar, QRoundTimer


class Signaler(QObject):
    on_progress = pyqtSignal(datetime.timedelta)

    def __init__(self):
        super(Signaler, self).__init__()


class Timer(QRunnable):

    def __init__(self, stop_at: datetime = None):
        super().__init__()
        if stop_at is not None:
            self.stop_at = stop_at
        else:
            self.stop_at = datetime.datetime.now() + datetime.timedelta(hours=24 * 365)
        self.signaler = Signaler()
        self.start_point = datetime.datetime.now()
        self.is_running = False
        self.emit_again = True
        self.laps: list = []

    @pyqtSlot()
    def run(self):
        self.is_running = True
        now = last_emision = datetime.datetime.now()
        while now < self.stop_at and self.is_running:
            time = self.get_actual_time()
            # print(time)
            QApplication.processEvents()
            #  TODO el print hace que se sincronicen los tiempos. si se lo quitas va de pena
            if (now - last_emision) > datetime.timedelta(milliseconds=1) and self.emit_again:
                self.signaler.on_progress.emit(time)
                last_emision = now
            now = datetime.datetime.now()
        self.is_running = False
        self.signaler.on_progress.emit(datetime.timedelta(seconds=0))

    def lap(self) -> datetime.timedelta:
        lap = len(self.laps)
        self.laps.append(self.get_actual_time())
        self.start_point = datetime.datetime.now()
        return self.laps[lap]

    def stop(self):
        self.stop_at = datetime.datetime.now()

    def get_actual_time(self) -> datetime.timedelta:
        return datetime.datetime.now() - self.start_point

    def __str__(self):
        now = self.get_actual_time().__format__('{:02}:{:02}:{:02}')
        return str(now)


class ProgressCronometro(QRoundTimer):
    def __init__(self):
        super().__init__()
        self.setBarStyle(QRoundProgressBar.StyleDonut)
        # self.setBackgroundRole()
        self.setDataPenWidth(2)
        self.setMinimumSize(200,200)
        self.setOutlinePenWidth(2)
        self.setDonutThicknessRatio(0.95)
        self.setDecimals(self.MILISECONDS)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setFormat('%t')
        self.setDataColors(
            [
                (0., QColor.fromRgb(0, 255, 0)),
                (0.45, QColor.fromRgb(255, 255, 0)),
                (0.90, QColor.fromRgb(255, 0, 0))
            ])
        self.min = 0.0
        self.value = 0.0
        self.max = 10.0
