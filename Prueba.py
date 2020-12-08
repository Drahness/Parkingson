import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QWidget, QApplication, QMainWindow, QVBoxLayout,
    QHBoxLayout, QPushButton, QSizePolicy, QTabWidget
)
from Graph import MplCanvas  # Si se te instala numpy 1.19.4 puede tirar error en windows.


class Color(QWidget):
    def __init__(self, color):
        super().__init__()
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)


class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CronometroOrtsLayouts")
        self.chronometer_widget = CentralWidgetParkingson(self)
        # sc = MplCanvas(self, width=5, height=4, dpi=100)
        # sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        self.setCentralWidget(self.chronometer_widget)
        self.show()


class CentralWidgetParkingson(QWidget):
    pacients_tab: QWidget  # Una vez seleccionado paciente, mostrara sus datos
    cronometro_tab: QWidget  # Una vez seleccionado paciente, lo testara
    rendimiento_tab: QWidget  # Una vez seleccionado paciente, mostrara su rendimiento

    pacients_list_view: QWidget  # Mostrara los pacientes en lista
    actions_buttons: dict  # Continene los botones de la app

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        general_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        content_layout = QHBoxLayout()

        self.actions_buttons = {
            'add': QPushButton('Anadir'),
            'delete': QPushButton('Eliminar'),
            'edit': QPushButton('Editar')
        }

        self.actions_buttons['add'].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.actions_buttons['delete'].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.actions_buttons['edit'].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        buttons_layout.addWidget(self.actions_buttons['add'])
        buttons_layout.addWidget(self.actions_buttons['delete'])
        buttons_layout.addWidget(self.actions_buttons['edit'])
        buttons_layout.setAlignment(Qt.AlignLeft)
        buttons_layout.setSpacing(20)

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

        content_layout.addWidget(self.pacients_list_view, stretch=3, alignment=Qt.AlignTop)
        content_layout.addWidget(self.parent_tab_widget, stretch=9)

        general_layout.addLayout(buttons_layout)
        general_layout.addLayout(content_layout)

        self.setMinimumSize(900, 600)
        self.setLayout(general_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
