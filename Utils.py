from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QFrame


class KeyValueWidget(QWidget):
    def __init__(self, key: str, value: str):
        super().__init__()
        self.main_layout = QHBoxLayout()
        self.main_layout.setAlignment(Qt.AlignCenter)
        self.key: QLabel = QLabel(key)
        self._value: QLabel = QLabel(value)
        self.key.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.value.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.main_layout.addWidget(self.key)
        self.main_layout.addWidget(self.value)
        self.setLayout(self.main_layout)

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self,value):
        if isinstance(value, QObject):
            self.main_layout = QHBoxLayout()
            self._value = value
            self.main_layout.addWidget(self.key)
            self.main_layout.addWidget(value)
            self.setLayout(self.main_layout)


class KeyValueMutable(KeyValueWidget):
    def __init__(self, key: str, is_hidden: bool):
        super().__init__(key, "")
        self.value: QTextEdit = QTextEdit("b")
