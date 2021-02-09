import datetime

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QWidget, QSizePolicy, QTextEdit, QLabel, QFormLayout

import Utils
from GUI.GUI_Resources import get_cronometro_widget_ui, get_cronometro_bar_widget
from GUI.cronometro import Timer
from GUI.pacient_oriented_tab_interface import PacientInterface
from GUI.static_actions import StaticActions
from database.settings import UserSettings
from database.prueba import Prueba


class Cronometro(QWidget, PacientInterface):
    STARTED = 0
    STOPPED = ...
    END = ...
    SAVE = ...
    # La parte int, la voy a dejar, pero no la usare.
    finishedSignal: pyqtSignal = pyqtSignal(Prueba, int)

    def pacientSelected(self, pacient, index):
        super().pacientSelected(pacient, index)
        self.start_and_lap.setEnabled(True)

    def __init__(self, user: str, parent=None):
        super(Cronometro, self).__init__(parent)
        self.user = user
        self.settings: UserSettings = UserSettings(user)
        PacientInterface.__init__(self)
        get_cronometro_widget_ui(self)
        self.formLayout: QFormLayout = self.formLayout
        self.vuelta3_label: QLabel = self.vuelta3_label
        self.vuelta2_label: QLabel = self.vuelta2_label
        self.vuelta1_label: QLabel = self.vuelta1_label
        self.vuelta3_edit: QTextEdit = self.vuelta3_edit
        self.vuelta2_edit: QTextEdit = self.vuelta2_edit
        self.vuelta1_edit: QTextEdit = self.vuelta1_edit
        self.setObjectName("cronometro_paciente")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.progress_bar = get_cronometro_bar_widget()
        self.progress_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # Le ponemos los colores y los maximos al cronometro

        # editamos los label con los ajustes
        self.shownResults0: QLabel = self.shownResults0
        self.shownResults1: QLabel = self.shownResults1
        self.shownResults2: QLabel = self.shownResults2
        self.vuelta1_label.setText(self.settings.value(self.settings.LAP0_NAME))
        self.vuelta2_label.setText(self.settings.value(self.settings.LAP1_NAME))
        self.vuelta3_label.setText(self.settings.value(self.settings.LAP2_NAME))
        self.crono_widget.addWidget(self.progress_bar)
        self.stop_button.setVisible(False)
        self.cancel_button.setEnabled(False)
        self.vuelta1_edit.setEnabled(False)
        self.vuelta2_edit.setEnabled(False)
        self.vuelta3_edit.setEnabled(False)
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
        self.STOPPED = 4
        self.END = self.STOPPED - 2
        self.SAVE = self.STOPPED - 1
        self.status = self.STOPPED
        self.set_to_actual_state()

    def start_and_lap_slot(self):
        from main_window import UI
        if self.status == self.STOPPED:
            self.vuelta1_edit.setEnabled(True)
            self.vuelta2_edit.setEnabled(True)
            self.vuelta3_edit.setEnabled(True)
            StaticActions.vista_crono.setEnabled(False)
            self.sender().emit_again = True
            self.status = self.STARTED
            self.timer = Timer()
            self.prueba_actual = Prueba(pacient_id=self.pacient.id,
                                        datetime_of_test=datetime.datetime.now(),
                                        laps=self.timer.laps)
            self.timer.signaler.on_progress.connect(self.on_progress)
            UI.threadpool.start(self.timer)
            self.stop_button.setEnabled(True)
            self.cancel_button.setEnabled(True)
        elif self.status == self.END:  # A acabado el ciclo.
            self.stop_slot()
            lap = self.timer.lap()
            self.change_result(lap)
            self.status += 1
        elif self.status == self.SAVE:
            #self.stop_slot()
            StaticActions.vista_crono.setEnabled(True)
            self.status = self.STOPPED
            self.prueba_actual.notas = [self.vuelta1_edit.toPlainText(),
                                        self.vuelta2_edit.toPlainText(),
                                        self.vuelta3_edit.toPlainText()]
            self.vuelta1_edit.setText("")
            self.vuelta2_edit.setText("")
            self.vuelta3_edit.setText("")
            self.finishedSignal.emit(self.prueba_actual, self.index)
            self.shownResults0.setText("")
            self.shownResults1.setText("")
            self.shownResults2.setText("")
            self.cancel_button.setEnabled(False)
        else:  # Esta en ciclo.
            lap = self.timer.lap()
            self.change_result(lap)
            self.status += 1
        self.set_to_actual_state()

    def change_result(self,actual_lap):  # 0 primera vuelta 1 segund 2 tercera 
        low = self.settings.get_lap_time(self.status, 0)
        hard = self.settings.get_lap_time(self.status, 1)
        if(actual_lap < low):#verde
            self.change_label(str(actual_lap), "color:green", "Estado: Leve")
            pass
        elif(actual_lap > hard):#rojo
            self.change_label(str(actual_lap), "color:red", "Estado: Grave")
            pass
        else:#amarillo
            self.change_label(str(actual_lap), "color:yellow", "Estado: Moderado")
            pass

    @Utils.function_error_safety
    def change_label(self,current_lap, stylesheet, estado):
        # switch 
        if(self.status == 0): #vuelta 1
            self.shownResults0.setText(f"<span style={stylesheet}>"+estado+"</span>\n"+current_lap)
            #self.shownResults0.setStyleSheet(stylesheet)
            pass
        elif(self.status == 1): #vuelta 2
            self.shownResults1.setText(f"<span style={stylesheet}>"+estado+"</span>\n"+current_lap)
            #self.shownResults1.setStyleSheet(stylesheet)
            pass
        elif(self.status == 2): #vuelta 3
            self.shownResults2.setText(f"<span style={stylesheet}>"+estado+"</span>\n"+current_lap)
            #self.shownResults2.setStyleSheet(stylesheet)
            pass
        else:
            raise RuntimeError("Se ha llamado cuando no debia")

    def set_to_actual_state(self):
        if self.status != self.STOPPED:
            if self.status == self.SAVE:
                button_string = "Guardar"
            else:
                string = self.settings.get_lap_name(self.status)
                button_string = "Actual: " + string
                self.progress_bar.setMaximun(self.settings.get_lap_time(self.status, 1))
                self.progress_bar.changeYellowThereshold(self.settings.get_lap_time(self.status, 0))
        else:
            button_string = "Empezar"
        self.start_and_lap.setText(button_string)

    def stop_slot(self):  # Paras el timer
        if self.status != self.STOPPED and self.timer is not None:
            #self.cancel_button.setEnabled(False)
            self.stop_button.setEnabled(False)
            self.timer.stop()
            


    def cancel_slot(self):  # Reseteas el timer
        #self.stop_slot()
        self.timer.stop()
        self.timer = None
        self.cancel_button.setEnabled(False)
        self.shownResults0.setText("")
        self.shownResults1.setText("")
        self.shownResults2.setText("")
        self.status = self.STOPPED
        self.progress_bar.setValue(datetime.timedelta(seconds=0))

    def on_progress(self, timdelta: datetime.timedelta):
        self.sender().emit_again = False
        self.progress_bar.setValue(timdelta)
        self.statusChangeSlot.emit(f"{self.prueba_actual}", 1)
        self.sender().emit_again = True

    def init(self):
        super().init()
