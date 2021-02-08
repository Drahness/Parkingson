from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QTabWidget, QListView

import Utils
from GUI.grafica_tab import EvolutionTab
from GUI.cronometro_tab import Cronometro
from GUI.pacient_widget_tab import PacientWidget

class CentralWidgetParkingson(QWidget):
    pacients_tab: QWidget  # Una vez seleccionado paciente, mostrara sus datos
    cronometro_tab: QWidget  # Una vez seleccionado paciente, lo testara
    evolution_tab: QWidget  # Una vez seleccionado paciente, mostrara su rendimiento

    pacients_list_view: QListView  # Mostrara los pacientes en lista
    actions_buttons: dict  # Continene los botones de la app

    general_layout: QVBoxLayout
    buttons_layout: QHBoxLayout  # el layout de los botones de arriba
    content_layout: QHBoxLayout  # los layout de los tabs y el listview

    ADD_button_key = "add"
    DELETE_button_key = "delete"
    EDIT_button_key = "edit"

    @Utils.function_error_safety
    def __init__(self, user:str, parent=None):
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
        self.pacients_tab: PacientWidget = PacientWidget()  # Tab1 Color

        # self.rendimiento_tab = MplCanvas(self, width=5, height=4, dpi=100)  # Tab2 Grafica
        self.evolution_tab = EvolutionTab(user)

        self.cronometro_tab = Cronometro(user)
        self.parent_tab_widget.resize(300, 300)  # Tab Parent

        self.parent_tab_widget.addTab(self.pacients_tab, "Paciente")
        self.parent_tab_widget.addTab(self.evolution_tab, "Evolucion")
        self.parent_tab_widget.addTab(self.cronometro_tab, "Cronómetro")

        self.pacients_list_view.setMinimumSize(200, 400)
        self.pacients_list_view.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.pacients_list_view.setContextMenuPolicy(Qt.CustomContextMenu)

        self.content_layout.addWidget(self.pacients_list_view, stretch=3, alignment=Qt.AlignTop)
        self.content_layout.addWidget(self.parent_tab_widget, stretch=9)

        # self.general_layout.addLayout(self.buttons_layout)
        self.general_layout.addLayout(self.content_layout)

        self.setMinimumSize(900, 600)
        self.setLayout(self.general_layout)

