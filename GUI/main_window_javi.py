import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QTabWidget, QListView

from GUI.grafica_tab import PerformanceTab
from GUI.cronometro_tab import Cronometro
from GUI.pacient_widget_tab import PacientWidget


class Color(QWidget):
    """No la voy a usar"""

    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class App(QMainWindow):
    """ Esta clase no la voy a usar """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("CronometroOrtsLayouts")
        self.central_widget = CentralWidgetParkingson(self)

        self.setCentralWidget(self.central_widget)
        self.show()


class CentralWidgetParkingson(QWidget):
    pacients_tab: QWidget  # Una vez seleccionado paciente, mostrara sus datos
    cronometro_tab: QWidget  # Una vez seleccionado paciente, lo testara
    rendimiento_tab: QWidget  # Una vez seleccionado paciente, mostrara su rendimiento

    pacients_list_view: QListView  # Mostrara los pacientes en lista
    actions_buttons: dict  # Continene los botones de la app

    general_layout: QVBoxLayout
    buttons_layout: QHBoxLayout  # el layout de los botones de arriba
    content_layout: QHBoxLayout  # los layout de los tabs y el listview

    ADD_button_key = "add"
    DELETE_button_key = "delete"
    EDIT_button_key = "edit"

    def __init__(self, user:str, parent=None, debug=False):
        super(QWidget, self).__init__(parent)
        self.general_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.content_layout = QHBoxLayout()

        self.actions_buttons = {
            CentralWidgetParkingson.ADD_button_key: QPushButton('Anadir'),
            CentralWidgetParkingson.DELETE_button_key: QPushButton('Eliminar'),
            CentralWidgetParkingson.EDIT_button_key: QPushButton('Editar')
        }

        for x in self.actions_buttons:
            self.actions_buttons[x].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.actions_buttons[x].setObjectName(x + "_button")
            self.buttons_layout.addWidget(self.actions_buttons[x])

        self.buttons_layout.setAlignment(Qt.AlignLeft)
        self.buttons_layout.setSpacing(20)

        self.pacients_list_view = QListView()
        self.pacients_list_view.resize(200, 400)
        self.parent_tab_widget = QTabWidget()
        self.parent_tab_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pacients_tab: PacientWidget = PacientWidget(debug)  # Tab1 Color

        # self.rendimiento_tab = MplCanvas(self, width=5, height=4, dpi=100)  # Tab2 Grafica
        self.rendimiento_tab = PerformanceTab(user)

        self.cronometro_tab = Cronometro(user)
        self.parent_tab_widget.resize(300, 300)  # Tab Parent

        self.parent_tab_widget.addTab(self.pacients_tab, "Paciente")
        self.parent_tab_widget.addTab(self.rendimiento_tab, "Rendimiento")
        self.parent_tab_widget.addTab(self.cronometro_tab, "Cronómetro")

        self.pacients_list_view.setMinimumSize(200, 400)
        self.pacients_list_view.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.content_layout.addWidget(self.pacients_list_view, stretch=3, alignment=Qt.AlignTop)
        self.content_layout.addWidget(self.parent_tab_widget, stretch=9)

        # self.general_layout.addLayout(self.buttons_layout)
        self.general_layout.addLayout(self.content_layout)

        self.setMinimumSize(900, 600)
        self.setLayout(self.general_layout)

