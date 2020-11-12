from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTextEdit


class KeyValueWidget(QWidget):
    def __init__(self, key: str, value: str):
        super().__init__()
        self.main_layout = QVBoxLayout()
        self._key: QLabel = QLabel(key)
        self._value: QLabel = QLabel(value)
        self.main_layout.addWidget(self.key)
        self.main_layout.addWidget(self.value)

    @property
    def key(self):
        return self._key.text()

    @key.setter
    def key(self, value):
        if isinstance(value,str):
            self._key.setText(value)
        elif isinstance(value,QLabel):
            self._key = value
        else:
            raise RuntimeError()

class KeyValueMutable(KeyValueWidget):
    def __init__(self, key: str, is_hidden: bool):
        super().__init__(key)
        self._value: QTextEdit = QTextEdit()
