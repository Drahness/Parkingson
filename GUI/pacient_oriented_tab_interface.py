import sys

import matplotlib
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QObject

matplotlib.use('Qt5Agg')


class PacientInterface:
    """Los tabs heredan de esta. Ya que todos tienen casi la misma logica"""

    def __init__(self):
        self.last_pacient = None
        self.pacient = None
        self.index = None
        self.on_focus = False
        self.statusChangeSlot = None
        self.pacientSelectedSignal: pyqtSignal = ...
        self.currentChangedSignal: pyqtSignal = ...
        self.key_pressedSignal: pyqtSignal = ...
        pass

    def set_key_pressed(self, signal: pyqtSignal):
        self.key_pressedSignal = signal

    def get_key_pressed(self):
        return self.key_pressedSignal

    def is_on_focus(self) -> bool:
        return self.on_focus

    def get_signal_pacient_selected(self) -> pyqtSignal:
        return self.pacientSelectedSignal

    def set_signal_pacient_selected(self, signal: pyqtSignal):
        self.pacientSelectedSignal = signal

    def get_signal_current_changed(self) -> pyqtSignal:
        return self.currentChangedSignal

    def set_signal_current_changed(self, signal: pyqtSignal):
        self.currentChangedSignal = signal

    def pacientSelected(self, pacient, index):
        """The signal pacientSelected will get a Pacient and a row in the model."""
        self.pacient = pacient
        self.index = index

    def init(self):
        """Inicializas el widget. Concretamente las señales desde el mainWindow."""
        self.pacientSelectedSignal.connect(self.pacientSelected)
        self.currentChangedSignal.connect(self.currentChanged)
        self.key_pressedSignal.connect(self.key_pressed)


    def set_change_status_bar(self, signal: pyqtSignal):
        self.statusChangeSlot = signal

    def get_change_status_bar(self):
        return self.statusChangeSlot

    def currentChanged(self, index):
        self.on_focus = False
        self.sender().currentWidget().on_focus = True

    def key_pressed(self, key: QtGui.QKeyEvent, *args):
        pass

    def sender(self) -> QObject: ...
    """Para que no dé warnings, normalmente es un metodo heredado de QObject"""
