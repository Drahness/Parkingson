import datetime

from PyQt5.QtGui import QColor
from PyQt5.QtCore import QRunnable, pyqtSlot, pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QWidget, QApplication

from GUI.GUI_Resources import get_cronometro_widget_ui, get_cronometro_bar_widget
from GUI.QtRoundProgressBar import QRoundTimer, QRoundProgressBar
from main_window import UI


class Signaler(QObject):
    on_progress = pyqtSignal(datetime.timedelta)
    
    def __init__(self):
        super(Signaler, self).__init__()

class Timer(QRunnable):
    on_progress: pyqtSignal = pyqtSignal(datetime.timedelta)

    def __init__(self, stop_at: datetime = None):
        super().__init__()
        if stop_at is not None:
            self.stop_at = stop_at
        else:
            self.stop_at = datetime.datetime.now() + datetime.timedelta(hours=24 * 365)
        self.signaler = Signaler()
        self.start_point = datetime.datetime.now()
        self.is_running = False
        self.laps: list = []

    @pyqtSlot()
    def run(self):
        self.is_running = True
        now = last_emision = datetime.datetime.now()
        while now < self.stop_at and self.is_running:
            time = self.get_actual_time()
            print(time)
            if (now - last_emision) > datetime.timedelta(milliseconds=1):
                self.signaler.on_progress.emit(time)
                last_emision = now
            now = datetime.datetime.now()
        self.is_running = False

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
        self.setDataPenWidth(2)
        self.setOutlinePenWidth(2)
        self.setDonutThicknessRatio(0.75)
        self.setDecimals(4)
        self.setFormat('%v')
        self.setDataColors(
            [
                (0.0, QColor.fromRgb(255, 0, 0)),
                (1 / 3, QColor.fromRgb(0, 255, 0)),
                (2 / 3, QColor.fromRgb(0, 0, 255))
            ])
        self.min = datetime.timedelta(minutes=0).seconds
        self.value = datetime.timedelta(minutes=0).seconds
        self.max = datetime.timedelta(minutes=1).seconds


class Cronometro(QWidget):
    STOPPED = 4
    STARTED = 0
    END = 3

    def __init__(self, parent=None):
        super(Cronometro, self).__init__(parent)
        get_cronometro_widget_ui(self)
        self.progress_bar = get_cronometro_bar_widget()
        self.horizontalLayout.addWidget(self.progress_bar)
        # self.horizontalLayout.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # self.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
        # self.setStyleSheet("background:red")
        self.start_and_lap.clicked.connect(self.start_and_lap_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.stop_button.clicked.connect(self.stop_slot)
        self.progress_bar.setFormat("%t")
        self.progress_bar.setDecimals(self.progress_bar.MILISECONDS)
        self.progress_bar.setMaximun(datetime.timedelta(seconds=60))
        self.start_and_lap.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.timer = None
        self.laps = []
        self.status = self.STOPPED
        self.start_and_lap.setText("Start")


    def start_and_lap_slot(self):
        if self.status == self.STOPPED:
            self.status = self.STARTED
            self.timer = Timer()
            self.timer.signaler.on_progress.connect(self.on_progress)
            UI.threadpool.start(self.timer)
            button_string = "Lap " + str(self.status + 1)
            self.start_and_lap.setText(button_string)
            self.stop_button.setEnabled(True)
            self.cancel_button.setEnabled(True)
        elif self.status == self.END:
            self.stop_slot()
            self.status = self.STOPPED
            self.cancel_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.start_and_lap.setText("Start")
            self.laps.clear()  # Tengo que llevarlo a algun sitio
        else:
            lap = self.timer.lap()
            self.laps.append(lap)
            self.progress_bar.setMaximun(lap)
            self.status += 1
            if self.status != self.END:
                button_string = "Lap " + str(self.status + 1)
            else:
                button_string = "End"
            self.start_and_lap.setText(button_string)
        print(self.laps)
        print(len(self.laps))

    def stop_slot(self):  # Paras el timer
        if self.status != self.STOPPED and self.timer is not None:
            self.timer.stop()
            self.status = self.STOPPED
            self.start_and_lap.setText("Start")

    def cancel_slot(self):  # Reseteas el timer
        self.stop_slot()
        self.timer = None
        self.progress_bar.setValue(datetime.timedelta(seconds=0))

    def on_progress(self, timdelta: datetime.timedelta):
        self.sender().blockSignals(True)
        print("receiving")
        self.progress_bar.setValue(timdelta)
        self.sender().blockSignals(False)
