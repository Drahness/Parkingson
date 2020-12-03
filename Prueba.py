import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QWidget, QApplication, QMainWindow, QVBoxLayout,
    QHBoxLayout, QPushButton, QSizePolicy, QTabWidget
)

from Graph import MplCanvas


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
        self.chronometer_widget = ChronometerWidget(self)
        #sc = MplCanvas(self, width=5, height=4, dpi=100)
        #sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        self.setCentralWidget(self.chronometer_widget)
        self.show()


class ChronometerWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        general_layout = QVBoxLayout()
        buttons_layout = QHBoxLayout()
        content_layout = QHBoxLayout()

        actions_buttons = {
            'add': QPushButton('Anadir'),
            'delete': QPushButton('Eliminar'),
            'edit': QPushButton('Editar')
        }

        actions_buttons['add'].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        actions_buttons['delete'].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        actions_buttons['edit'].setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        buttons_layout.addWidget(actions_buttons['add'])
        buttons_layout.addWidget(actions_buttons['delete'])
        buttons_layout.addWidget(actions_buttons['edit'])
        buttons_layout.setAlignment(Qt.AlignLeft )
        buttons_layout.setSpacing(20)

        green_rectangle = Color("green")

        parent_tab_widget = QTabWidget()
        tab_patient = Color("red")  #Tab1 Color

        tab_performance = MplCanvas(self, width=5, height=4, dpi=100)   #Tab2 Grafica
        tab_performance.axes.plot([0,1,2,3,4], [10,1,20,3,40])  

        tab_chrono = Color("green") #Tab3 Color

        parent_tab_widget.resize(300, 300)  #Tab Parent



        parent_tab_widget.addTab(tab_patient, "Paciente")
        parent_tab_widget.addTab(tab_performance, "Rendimiento")
        parent_tab_widget.addTab(tab_chrono, "Cronómetro")

    
        green_rectangle.setMinimumSize(200, 400)
        green_rectangle.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

        content_layout.addWidget(green_rectangle, stretch=3, alignment=Qt.AlignTop)
        content_layout.addWidget(parent_tab_widget, stretch=9)
        

        general_layout.addLayout(buttons_layout)
        general_layout.addLayout(content_layout)

        self.setMinimumSize(900, 600)
        self.setLayout(general_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())