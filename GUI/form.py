import datetime
import sys

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QDateEdit, QApplication, QCalendarWidget

from GUI.GUI_Resources import get_pacient_widget_ui
from database.entities import Pacient


class PacientInterface:
    """Los tabs heredan de esta. Ya que todos tienen casi la misma logica"""

    def __init__(self):
        self.last_pacient = None
        self.pacient = None
        self.index = None
        pass

    def on_pacient_selected(self, pacient, index):
        """The signal pacientSelected will get a Pacient and a row in the model."""
        self.pacient = pacient
        self.index = index

    def init(self):
        from main_window import UI
        UI.get_instance().pacientSelected.connect(self.on_pacient_selected)


class PacientWidget(QWidget, PacientInterface):
    default_date = datetime.date(1990, 12, 12)
    finishedSignal: pyqtSignal = pyqtSignal(bool)  # maybe another name is better
    resultSignal: pyqtSignal = pyqtSignal(bool, int)
    """ bool if canceled or accepted. int, the row of the pacient or -1 if new pacient """

    def __init__(self):
        super().__init__()
        get_pacient_widget_ui(self)
        self.calendarWidget.clicked.connect(self.on_calendar_changed)
        self.nacimiento_field.dateChanged.connect(self.on_calendar_changed)
        self.calendarWidget: QCalendarWidget = self.calendarWidget
        self.nacimiento_field: QDateEdit = self.nacimiento_field
        self.accept_button.clicked.connect(self.buttons)
        self.cancel_button.clicked.connect(self.buttons)
        self.on_pacient_selected(None)
        self.set_enabled(False)


    def save_pacient(self):
        """Updates the instance."""
        self.pacient.dni = self.dni_field.text()
        self.pacient.apellidos = self.apellidos_field.text()
        self.pacient.nombre = self.nombre_field.text()
        self.pacient.estadio = self.estadio_field.text()
        self.pacient.nacimiento = self.nacimiento_field.date()
        self.pacient.notas = self.notas_field.toPlainText()
        return self.pacient

    def buttons(self, *args):
        name = self.sender().objectName()
        print(name)
        if name == "accept_button":
            self.save_pacient()
            self.resultSignal.emit(True, self.index)
        elif name == "cancel_button":
            self.resultSignal.emit(False, -1)
        self.set_enabled(False)

    def on_pacient_selected(self, pacient, row: int = None):
        """Overriden method from PacientInterface"""
        self.index = row
        if pacient is not None:
            if isinstance(pacient, dict):
                dni = pacient.get("dni")
                nombre = pacient.get("nombre")
                apellidos = pacient.get("apellidos")
                estadio = pacient.get("estadio", default=0)
                nacimiento = pacient.get("nacimiento", default=self.default_date)
                notas = pacient.get("notas")
            elif isinstance(pacient, Pacient):
                dni = pacient.dni
                nombre = pacient.nombre
                apellidos = pacient.apellidos
                estadio = pacient.estadio or 0
                nacimiento = pacient.nacimiento or self.default_date
                notas = pacient.notas
            else:
                raise AssertionError()
        else:
            dni = None
            nombre = None
            apellidos = None
            estadio = ""
            nacimiento = self.default_date
            notas = None
        self.pacient = pacient
        self.last_pacient = dni
        self.dni_field.setText(dni)
        self.apellidos_field.setText(apellidos)
        self.nombre_field.setText(nombre)
        self.estadio_field.setText(str(estadio))
        self.nacimiento_field.setDate(nacimiento)
        self.notas_field.setText(notas)
        self.calendarWidget.setSelectedDate(nacimiento)
        self.estadio_field.setValidator(QIntValidator())

    def set_enabled(self, enabled: bool):
        self.dni_field.setEnabled(enabled)
        self.apellidos_field.setEnabled(enabled)
        self.nombre_field.setEnabled(enabled)
        self.estadio_field.setEnabled(enabled)
        self.nacimiento_field.setEnabled(enabled)
        self.notas_field.setEnabled(enabled)
        self.calendarWidget.setEnabled(enabled)
        self.cancel_button.setVisible(enabled)
        self.accept_button.setVisible(enabled)
        self.finishedSignal.emit(not enabled)

    def on_calendar_changed(self, *args):
        self.calendarWidget.setSelectedDate(args[0])
        self.nacimiento_field.setDate(args[0])

    def pacient_selected(self) -> bool:
        return self.pacient is not None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PacientWidget(False)
    widget.set_pacient(Pacient())
    widget.show()
    app.exec_()
