from datetime import datetime, timedelta

from PyQt5.QtWidgets import QDialog, QDateEdit, QLabel, QTextEdit, QTimeEdit

from GUI import GUI_Resources
from database.settings import UserSettings
from database.pacient import Pacient
from database.prueba import Prueba


class PruebaDialog(QDialog):

    def __init__(self, user, pacient: Pacient = None):
        super().__init__()
        GUI_Resources.get_prueba_dialog_ui(self)
        self.prueba = Prueba()
        self.fecha: QDateEdit = self.fecha
        self.pacient_nom: QLabel = self.pacient_nom
        self.lap1_notes: QTextEdit = self.lap1_notes
        self.lap2_notes: QTextEdit = self.lap2_notes
        self.lap3_notes: QTextEdit = self.lap3_notes
        self.lap1_time: QTimeEdit = self.lap1_time
        self.lap2_time: QTimeEdit = self.lap2_time
        self.lap3_time: QTimeEdit = self.lap3_time
        self.lap_header_1: QLabel = self.lap_header_1
        self.lap_header_2: QLabel = self.lap_header_2
        self.lap_header_3: QLabel = self.lap_header_3
        self.fecha: QDateEdit = self.fecha
        self.fecha: QDateEdit = self.fecha
        settings = UserSettings(user)
        self.lap_header_1.setText(settings.value(settings.LAP0_NAME))
        self.lap_header_2.setText(settings.value(settings.LAP1_NAME))
        self.lap_header_3.setText(settings.value(settings.LAP2_NAME))
        self.fecha.setDateTime(datetime.now())
        if pacient:
            self.pacient_nom.setText(pacient.get_fomatted_name())
            self.prueba.pacient_id = pacient.id

    def set_prueba(self, pacient: Pacient = None, prueba: Prueba = None):
        if prueba:
            self.prueba = prueba
            self.lap1_time.setTime((datetime.min + prueba.laps[0]).time())
            self.lap2_time.setTime((datetime.min + prueba.laps[1]).time())
            self.lap3_time.setTime((datetime.min + prueba.laps[2]).time())
            self.fecha.setDateTime(prueba.datetime)
            self.lap1_notes.setText(prueba.notas[0])
            self.lap2_notes.setText(prueba.notas[1])
            self.lap3_notes.setText(prueba.notas[2])
        if pacient:
            self.pacient_nom.setText(pacient.get_fomatted_name())
            self.prueba.pacient_id = pacient.id

    def get_prueba(self):
        laps = []
        notas = []
        laps.append(self.lap1_time.time().toPyTime())
        laps.append(self.lap2_time.time().toPyTime())
        laps.append(self.lap3_time.time().toPyTime())
        notas.append(self.lap1_notes.toPlainText())
        notas.append(self.lap2_notes.toPlainText())
        notas.append(self.lap3_notes.toPlainText())
        self.prueba.datetime = self.fecha.dateTime().toPyDateTime()
        self.prueba.datetime = self.prueba.datetime + timedelta(microseconds=1)
        self.prueba.notas = notas
        self.prueba.laps = laps
        return self.prueba
