import datetime
import hashlib
import inspect
import math
import threading
import re

import traceback

from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QObject, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QTextEdit, QHBoxLayout, QFrame, QMessageBox, QMenu

debug = False


def print_debug(msg: str):
    if debug:
        print(msg)


def throw_qt_error(e: Exception, string_before_trace: str = None, title: str = None):
    title = title or type(e).__name__
    string_before_trace = string_before_trace or ""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(string_before_trace)
    informative = "Error type: " + type(e).__name__
    informative += "\n" + inspect.stack()[0][3] + "\n" + inspect.stack()[1][3]
    msg.setInformativeText(informative)
    msg.setDetailedText(traceback.format_exc())
    msg.setWindowTitle(title)
    traceback.print_exc()
    msg.resize(1000, 3000)
    return msg


def function_error_safety(function):
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception as e:
            string = f"""Error args = {args}, kwars = {kwargs}"""
            throw_qt_error(e, string, "Error").exec_()

    return wrapper


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


def cypher(password: str) -> str:
    return hashlib.sha3_512(password.encode('utf-8')).hexdigest()


def format_list(lista: list) -> str:
    return str(lista)[1:-1]


def format_dict(dictionary: dict, center="=") -> str:
    return str(dictionary)[1:-1].replace(":", center)


def timedelta_to_float(delta: datetime.timedelta):
    return delta.seconds + delta.microseconds / (10 ** 6)


def get_from_dict(dictionary: dict, key: any) -> any or None:
    """ Metodo para coger cosas de un diccionario, y si da error devuelve None"""
    try:
        return dictionary[key]
    except KeyError:
        return None


def get_timedelta(real_number: float or datetime.timedelta, canbeNone=False):
    if real_number is None:
        if canbeNone:
            return real_number
        else:
            raise ValueError("the real_number cant be none.")
    if isinstance(real_number, float) or isinstance(real_number, int):
        micro, seconds = math.modf(real_number)
        return datetime.timedelta(seconds=seconds, microseconds=micro * 1000000)
    elif isinstance(real_number, datetime.timedelta):
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


def get_bytes_from_pixmap(pix: QPixmap):
    if isinstance(pix, QPixmap):
        barray = QtCore.QByteArray()
        buff = QtCore.QBuffer(barray)
        buff.open(QtCore.QIODevice.WriteOnly)
        ok = pix.save(buff, "png")
        return barray.data() if ok else None
    else:
        return None


def get_pixmap_from_bytes(by: bytes):
    if isinstance(by, bytes):
        pix = QPixmap()
        pix.loadFromData(by)
        return pix
    else:
        return None


def get_position(widget: QWidget, relative_point: QPoint = None, *args, **kwargs):
    x = 0
    y = 0
    while widget.parent() is not None:
        x += widget.pos().x()
        y += widget.pos().y()
        widget = widget.parent()
    x += widget.pos().x() + (relative_point.x() if relative_point else 0)
    y += widget.pos().y() + (relative_point.y() if relative_point else 0)
    return QPoint(x, y)


def popup_context_menu(sender: QWidget, menu: QMenu, relative_point: QPoint = None, *args, **kwargs):
    menu.popup(get_position(sender, relative_point))
