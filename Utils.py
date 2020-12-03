import datetime
import hashlib
import threading

from PyQt5.QtCore import Qt, QObject
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QHBoxLayout, QFrame


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
    def value(self, value):
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


class TimerThreadingClass(threading.Thread):
    def __init__(self, stop_at: datetime = None):
        super().__init__()
        if stop_at is not None:
            self.stop_at = stop_at
        else:
            self.stop_at = datetime.datetime.now() + datetime.timedelta(hours=100)
        self.start_point = datetime.datetime.now()
        self.is_running = False
        self.laps: list = []

    def run(self):
        self.is_running = True
        while datetime.datetime.now() < self.stop_at and self.is_running:
            pass
        self.is_running = False

    def lap(self):
        self.laps.append(self.get_actual_time())
        self.start_point = datetime.datetime.now()

    def cancel(self):
        self.stop_at = datetime.datetime.now()

    def get_actual_time(self) -> datetime.timedelta:
        return datetime.datetime.now() - self.start_point

    def __str__(self):
        returning = '{:02}:{:02}:{:02}'
        now = self.get_actual_time().__format__('{:02}:{:02}:{:02}')
        return str(now)


def run_timer():
    t = TimerThreadingClass()
    t.start()
    while t.is_running:
        print("Hilo principal")
        print(str(t))
        s = input()
        if s == "c":
            t.cancel()
        elif s == "l":
            t.lap()
        elif s == "get":
            print(t.laps)
            for x in t.laps:
                print(type(x))


def cypher(password: str) -> str:
    return hashlib.sha3_512(password.encode('utf-8')).digest().decode('utf-8')

if __name__ == "__main__":
    pass
