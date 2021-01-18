import sys

import matplotlib
from PyQt5.QtCore import pyqtSignal

matplotlib.use('Qt5Agg')


class PacientInterface:
    """Los tabs heredan de esta. Ya que todos tienen casi la misma logica"""

    def __init__(self):
        self.last_pacient = None
        self.pacient = None
        self.index = None
        self.on_focus = False
        self.statusChangeSlot = None
        self.pacientSelectedSignal = None
        self.currentChangedSignal = None
        pass

    def is_on_focus(self) -> bool:
        return self.on_focus
    def getsignal_pacient_selected(self) -> pyqtSignal:
        return self.pacientSelectedSignal

    def set_signal_pacient_selected(self, signal: pyqtSignal):
        self.pacientSelectedSignal = signal

    def getsignal_current_changed(self) -> pyqtSignal:
        return self.currentChangedSignal

    def set_signal_current_changed(self, signal: pyqtSignal):
        self.currentChangedSignal = signal

    def pacientSelected(self, pacient, index):
        """The signal pacientSelected will get a Pacient and a row in the model."""
        self.pacient = pacient
        self.index = index

    def init(self):
        """Inicializas el widget. Concretamente las señales desde el mainWindow."""
        # UI.get_instance().pacientSelected.connect(self.pacientSelected)
        self.pacientSelectedSignal.connect(self.pacientSelected)
        self.currentChangedSignal.connect(self.currentChanged)
        # UI.get_instance().central.parent_tab_widget.currentChanged.connect(self.currentChanged)
        # self.statusChangeSlot = UI.get_instance().changeStatusBar

    def set_change_status_bar(self, signal: pyqtSignal):
        self.statusChangeSlot = signal

    def get_change_status_bar(self):
        return self.statusChangeSlot

    def currentChanged(self, index):
        self.on_focus = False
        self.sender().currentWidget().on_focus = True
