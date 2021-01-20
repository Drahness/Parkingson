import datetime

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QSizePolicy, QTextEdit, QLabel

from GUI.GUI_Resources import get_cronometro_widget_ui, get_cronometro_bar_widget
from GUI.cronometro import Timer
from GUI.tab_widgets import PacientInterface
from database.Settings import UserSettings
from database.prueba import Prueba


class Cronometro(QWidget, PacientInterface):
    STOPPED = 3
    STARTED = 0
    END = 2
    # La parte int, la voy a dejar, pero no la usare.
    finishedSignal: pyqtSignal = pyqtSignal(Prueba, int)

    def pacientSelected(self, pacient, index):
        super().pacientSelected(pacient, index)
        self.start_and_lap.setEnabled(True)

    def __init__(self, user: str, parent=None):
        super(Cronometro, self).__init__(parent)
        self.user = user
        self.settings = UserSettings(user)
        PacientInterface.__init__(self)
        get_cronometro_widget_ui(self)
        self.setObjectName("cronometro_paciente")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.progress_bar = get_cronometro_bar_widget()
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.vuelta3: QLabel = self.vuelta3
        self.vuelta2: QLabel = self.vuelta3
        self.vuelta1: QLabel = self.vuelta3
        self.vuelta3_edit: QTextEdit = self.vuelta3_edit
        self.vuelta2_edit: QTextEdit = self.vuelta2_edit
        self.vuelta1_edit: QTextEdit = self.vuelta1_edit
        self.vuelta1.setText(self.settings.value(self.settings.LAP0_NAME))
        self.vuelta2.setText(self.settings.value(self.settings.LAP1_NAME))
        self.vuelta3.setText(self.settings.value(self.settings.LAP2_NAME))
        self.crono_widget.addWidget(self.progress_bar)
        self.stop_button.setEnabled(False)
        self.cancel_button.setEnabled(False)
        self.prueba_actual: Prueba = ...
        # Conexiones de los botones
        self.start_and_lap.clicked.connect(self.start_and_lap_slot)
        self.cancel_button.clicked.connect(self.cancel_slot)
        self.stop_button.clicked.connect(self.stop_slot)

        ###################################################################
        # Configuracion progress bar
        # self.start_and_lap.setEnabled(True)
        self.timer = None
        self.laps = []
        self.status = self.STOPPED
        self.start_and_lap.setText("Start")

    def start_and_lap_slot(self):
        from main_window import UI
        if self.status == self.STOPPED:
            self.sender().emit_again = True
            self.status = self.STARTED
            self.timer = Timer()

            self.prueba_actual = Prueba(pacient_id=self.pacient.dni,
                                        datetime_of_test=datetime.datetime.now(),
                                        laps=self.timer.laps)

            self.timer.signaler.on_progress.connect(self.on_progress)
            UI.threadpool.start(self.timer)
            button_string = "Lap " + str(self.status + 1)
            self.start_and_lap.setText(button_string)

            self.stop_button.setEnabled(True)
            self.cancel_button.setEnabled(True)
        elif self.status == self.END:  # A acabado el ciclo.
            self.stop_slot()
            self.timer.lap()
            self.status = self.STOPPED
            self.cancel_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.start_and_lap.setText("Start")
            self.prueba_actual.notas = [self.vuelta1_edit.text(),
                                  self.vuelta2_edit.text(),
                                  self.vuelta3_edit.text()]
            self.finishedSignal.emit(self.prueba_actual, self.index)
        else:  # Esta en ciclo.
            lap = self.timer.lap()
            self.progress_bar.setMaximun(lap)
            self.status += 1
            if self.status != self.END:
                button_string = "Lap " + str(self.status + 1)
            else:
                button_string = "End"
            self.start_and_lap.setText(button_string)

    def stop_slot(self):  # Paras el timer
        if self.status != self.STOPPED and self.timer is not None:
            self.cancel_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.timer.stop()
            self.status = self.STOPPED
            self.start_and_lap.setText("Start")

    def cancel_slot(self):  # Reseteas el timer
        self.stop_slot()
        self.timer = None
        self.progress_bar.setValue(datetime.timedelta(seconds=0))

    def on_progress(self, timdelta: datetime.timedelta):
        self.sender().emit_again = False
        self.progress_bar.setValue(timdelta)
        self.statusChangeSlot.emit(f"{self.prueba_actual}", 1)
        self.sender().emit_again = True

    def init(self):
        super().init()