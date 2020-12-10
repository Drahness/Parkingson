import datetime

from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QFormLayout, QDialog, QDateTimeEdit, \
    QDateEdit

from GUI import GUI_Resources


class Form(QDialog):
    def __init__(self, json: dict, editable: bool = True):
        super(Form, self).__init__()
        GUI_Resources.get_basic_form(self)
        self.json = json
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
    def __init__(self, key, value, editable: bool = True):
        self.key = QLabel(str(key))
        self.value = None
        if editable:
            if isinstance(value, int) or value == "int":
                self.value = QLineEdit()
                self.value.setValidator(QIntValidator())
            elif isinstance(value, float) or value == "float" or value == "decimal" or value == "double":
                self.value = QLineEdit()
                self.value.setValidator(QDoubleValidator())
            elif value is None or value.upper() == "null".upper():
                self.value = QLineEdit("")
            elif isinstance(value, datetime.datetime) or value.upper() == "datetime":
                self.value = QDateTimeEdit()
            elif isinstance(value, datetime.date) or value.upper() == "date":
                self.value = QDateEdit()
            else:  # default is string
                self.value = QLineEdit(value)
            pass
        else:
            self.value = QLabel(str(value))
            pass

    def get_widgets(self) -> tuple:

        return self.key, self.value
