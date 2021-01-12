import datetime

from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import QDialog, QFormLayout, QLabel, QLineEdit, QDateTimeEdit, QDateEdit
from sqlitedao import ColumnDict

from GUI import GUI_Resources


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
            if isinstance(value, datetime.date) or isinstance(value, datetime.datetime):
                self.values[key] = value
            else:
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