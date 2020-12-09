import datetime

from PyQt5.QtGui import QColor
from PyQt5.QtCore import QRunnable, pyqtSlot, Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QSizePolicy, QPushButton, QApplication

from GUI.GUI_Resources import get_cronometro_widget_ui, get_cronometro_bar_widget
from GUI.QtRoundProgressBar import QRoundProgressBarRebasable, QRoundProgressBar
from main_window import UI


class Timer(QRunnable):
    def __init__(self, stop_at: datetime = None, progress: QRoundProgressBar = None):
        super().__init__()
        if stop_at is not None:
            self.stop_at = stop_at
        else:
            self.stop_at = datetime.datetime.now() + datetime.timedelta(hours=24 * 365)
            # A ver quien se espera un año, quien es el listo
        self.progress_bar = progress
        self.start_point = datetime.datetime.now()
        self.is_running = False
        self.laps: list = []

    @pyqtSlot()
    def run(self):
        self.is_running = True
        QApplication.processEvents()
        while datetime.datetime.now() < self.stop_at and self.is_running:
            time = self.get_actual_time()
            if not self.progress_bar is None:
                self.progress_bar.setValue(time.seconds + time.microseconds/1000000)
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
        returning = '{:02}:{:02}:{:02}'
        now = self.get_actual_time().__format__('{:02}:{:02}:{:02}')
        return str(now)


class ProgressCronometro(QRoundProgressBarRebasable):
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
            self.timer = Timer(progress=self.progress_bar)
            UI.threadpool.start(self.timer)
            button_string = "Lap " + str(self.status+1)
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
            self.laps.append(self.timer.lap())
            self.status += 1
            if self.status != self.END:
                button_string = "Lap " + str(self.status+1)
            else:
                button_string = "End"
            self.start_and_lap.setText(button_string)
        print(self.laps)
        print(len(self.laps))

    def stop_slot(self):  # Todo estos dos creo que sobran :c
        if self.status != self.STOPPED and self.timer is not None:
            self.timer.stop()
            self.status = self.STOPPED
            self.start_and_lap.setText("Start")

    def cancel_slot(self):  # TODO resets.
        self.stop_slot()
        self.timer = None

