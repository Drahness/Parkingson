import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QTabWidget, \
    QApplication

from GUI.graph import MplCanvas


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
        # sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        self.setCentralWidget(self.central_widget)
        self.show()


class CentralWidgetParkingson(QWidget):
    pacients_tab: QWidget  # Una vez seleccionado paciente, mostrara sus datos
    cronometro_tab: QWidget  # Una vez seleccionado paciente, lo testara
    rendimiento_tab: QWidget  # Una vez seleccionado paciente, mostrara su rendimiento

    pacients_list_view: QWidget  # Mostrara los pacientes en lista
    actions_buttons: dict  # Continene los botones de la app

    general_layout: QVBoxLayout
    buttons_layout: QHBoxLayout  # el layout de los botones de arriba
    content_layout: QHBoxLayout  # los layout de los tabs y el listview

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.general_layout = QVBoxLayout()
        self.buttons_layout = QHBoxLayout()
        self.content_layout = QHBoxLayout()

        self.actions_buttons = {
            'add': QPushButton('Anadir'),
            'delete': QPushButton('Eliminar'),
            'edit': QPushButton('Editar')
        }

        self.actions_buttons['add'].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.actions_buttons['delete'].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.actions_buttons['edit'].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.buttons_layout.addWidget(self.actions_buttons['add'])
        self.buttons_layout.addWidget(self.actions_buttons['delete'])
        self.buttons_layout.addWidget(self.actions_buttons['edit'])
        self.buttons_layout.setAlignment(Qt.AlignLeft)
        self.buttons_layout.setSpacing(20)

        self.pacients_list_view = Color("green")

        self.parent_tab_widget = QTabWidget()
        self.pacients_tab = Color("red")  # Tab1 Color

        self.rendimiento_tab = MplCanvas(self, width=5, height=4, dpi=100)  # Tab2 Grafica
        self.rendimiento_tab.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

        self.cronometro_tab = Color("green")  # Tab3 Color

        self.parent_tab_widget.resize(300, 300)  # Tab Parent

        self.parent_tab_widget.addTab(self.pacients_tab, "Paciente")
        self.parent_tab_widget.addTab(self.rendimiento_tab, "Rendimiento")
        self.parent_tab_widget.addTab(self.cronometro_tab, "Cronómetro")

        self.pacients_list_view.setMinimumSize(200, 400)
        self.pacients_list_view.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        self.content_layout.addWidget(self.pacients_list_view, stretch=3, alignment=Qt.AlignTop)
        self.content_layout.addWidget(self.parent_tab_widget, stretch=9)

        self.general_layout.addLayout(self.buttons_layout)
        self.general_layout.addLayout(self.content_layout)

        self.setMinimumSize(900, 600)
        self.setLayout(self.general_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
