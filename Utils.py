import datetime
import hashlib
import math
import threading
import re

import os
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
    return hashlib.sha3_512(password.encode('utf-8')).hexdigest()


def format_list(lista: list) -> str:
    return str(lista)[1:-1]


def format_dict(dictionary: dict, center="=") -> str:
    return str(dictionary)[1:-1].replace(":", center)


def get_from_dict(dictionary: dict, key: any) -> any or None:
    """ Metodo para coger cosas de un diccionario, y si da error devuelve None"""
    try:
        return dictionary[key]
    except KeyError:
        return None


def get_timedelta(real_number: float or datetime.timedelta,canbeNone=False):
    if real_number is None:
        if canbeNone:
            return real_number
        else:
            raise ValueError("the real_number cant be none.")
    if isinstance(real_number,float) or isinstance(real_number,int):
        micro, seconds = math.modf(real_number)
        return datetime.timedelta(seconds=seconds, microseconds=micro)
    elif isinstance(real_number,datetime.timedelta):
        return real_number
    else:
        raise ValueError("Unknown number.")


def get_timedeltas(real_numbers: list):
    for x in range(0, len(real_numbers)):
        delta = get_timedelta(real_numbers[x])
        real_numbers.pop(x)
        real_numbers.insert(x, delta)
    return real_numbers


def parse_timedelta(s: str):
    if 'day' in s:
        m = re.match(r'(?P<days>[-\d]+) day[s]*, (?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    else:
        m = re.match(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d[\.\d+]*)', s)
    return {key: float(val) for key, val in m.groupdict().iteritems()}


if __name__ == "__main__":
    os.makedirs("aaaa/polaas/xd")
