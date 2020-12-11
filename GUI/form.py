import datetime
import sys

from PyQt5.QtCore import QDate, pyqtSignal
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QFormLayout, QDialog, QDateTimeEdit, \
    QDateEdit, QApplication, QCalendarWidget, QPushButton
from sqlitedao import ColumnDict

from GUI import GUI_Resources
from GUI.GUI_Resources import get_pacient_widget_ui, get_pacient_widget_ui_noeditable
from database.entities import Pacient


class SimpleForm(QDialog):
    """ A simple dialog, for simple input. Not meant to be in production"""

    def __init__(self, json: dict or ColumnDict, editable: bool = True):
        super(SimpleForm, self).__init__()
        GUI_Resources.get_basic_form(self)
        dictionary = json
        if isinstance(json, ColumnDict):
            dictionary = {}
            for column in json:
                dictionary[column] = json[column]["type"]
        self.json = dictionary
        self.values = {}
        self.formLayout: QFormLayout = self.formLayout
        self.init(editable)

    def init(self, editable):
        rows = self.formLayout.count()

        for i in range(0, rows):
            self.formLayout.removeRow(i)
        i = 0
        for key, value in self.json.items():
            tuple = WidgetSelector(key, value, editable).get_widgets()
            self.values[tuple[0].text()] = tuple[1]
            self.formLayout.insertRow(i, tuple[0], tuple[1])
            i += 1

    def get_values(self) -> dict:
        for key, value in self.values.items():
            self.values[key] = value.text()
        return self.values


class WidgetSelector:
    """ Helper class to SimpleForm class"""
    def __init__(self, key, value, editable: bool = True):
        self.key = QLabel(str(key))
        self.value = None
        if editable:
            lowered_value = value.lower()
            if isinstance(value, int) or lowered_value == "int" or lowered_value == "integer":
                self.value = QLineEdit()
                self.value.setValidator(QIntValidator())
            elif isinstance(value, float) or lowered_value == "float" \
                    or lowered_value == "decimal" or lowered_value == "double":
                self.value = QLineEdit()
                self.value.setValidator(QDoubleValidator())
            elif value is None or lowered_value == "null":
                self.value = QLineEdit("")
            elif isinstance(value, datetime.datetime) or lowered_value == "datetime":
                self.value = QDateTimeEdit()
            elif isinstance(value, datetime.date) or lowered_value == "date":
                self.value = QDateEdit()
            else:  # default is string
                self.value = QLineEdit("")
            pass
        else:
            self.value = QLabel(str(value))
            pass

    def get_widgets(self) -> tuple:
        return self.key, self.value


class PacientWidget(QWidget):
    default_date = datetime.date(1990, 12, 12)
    finishedSignal: pyqtSignal = pyqtSignal(bool)
    def __init__(self, editable: bool, pacient: dict or Pacient = None):
        super().__init__()
        get_pacient_widget_ui(self)

        self.pacient = pacient
        self.index: int = None
        self.calendarWidget.clicked.connect(self.on_calendar_changed)
        self.nacimiento_field.dateChanged.connect(self.on_calendar_changed)
        self.accept_button.clicked.connect(self.buttons)
        self.cancel_button.clicked.connect(self.buttons)
        self.set_pacient(pacient)
        self.set_enabled(editable)

    ## TODO tienes que pasarle a la entidad, que ella updatee la instancia,
    ## para que este en sincronia con la BBDD
    def save_pacient(self):
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
            self.set_enabled(False)
        elif name == "cancel_button":
            self.set_enabled(False)

    def set_pacient(self, pacient, row: int=None):
        self.index = row
        if pacient is not None:
            if isinstance(pacient, dict):
                dni = pacient.get("dni")
                nombre = pacient.get("nombre")
                apellidos = pacient.get("apellidos")
                estadio = pacient.get("estadio")
                nacimiento = pacient.get("nacimiento", default=self.default_date)
                notas = pacient.get("notas")
            elif isinstance(pacient, Pacient):
                dni = pacient.dni
                nombre = pacient.nombre
                apellidos = pacient.apellidos
                estadio = pacient.estadio
                nacimiento = pacient.nacimiento or self.default_date
                notas = pacient.notas
            else:
                raise AssertionError()
        else:
            dni = None
            nombre = None
            apellidos = None
            estadio = None
            nacimiento = self.default_date
            notas = None
        self.pacient = pacient
        self.calendarWidget: QCalendarWidget = self.calendarWidget
        self.nacimiento_field: QDateEdit = self.nacimiento_field
        self.estadio_field.setValidator(QIntValidator())
        self.dni_field.setText(dni)
        self.apellidos_field.setText(apellidos)
        self.nombre_field.setText(nombre)
        self.estadio_field.setText(str(estadio))
        self.nacimiento_field.setDate(nacimiento)
        self.notas_field.setText(notas)
        self.calendarWidget.setSelectedDate(nacimiento)

    def set_enabled(self, enabled: bool):
        self.finishedSignal.emit(not enabled)
        self.dni_field.setEnabled(enabled)
        self.apellidos_field.setEnabled(enabled)
        self.nombre_field.setEnabled(enabled)
        self.estadio_field.setEnabled(enabled)
        self.nacimiento_field.setEnabled(enabled)
        self.notas_field.setEnabled(enabled)
        self.calendarWidget.setEnabled(enabled)
        self.cancel_button.setVisible(enabled)
        self.accept_button.setVisible(enabled)

    def on_calendar_changed(self, *args):
        self.calendarWidget.setSelectedDate(args[0])
        self.nacimiento_field.setDate(args[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = PacientWidget(False)
    widget.set_pacient(Pacient())
    widget.show()
    app.exec_()
