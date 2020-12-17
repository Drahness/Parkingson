import sys
from UtilForms import Form as UtilForm

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import (
    QWidget, QApplication, QMainWindow, QVBoxLayout,
    QHBoxLayout, QSizePolicy, QTabWidget, QToolBar, QListWidget, QMessageBox
)

from .tab_widgets import MplCanvas


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
        self.chronometer_widget = CentralWidget(self)
        #sc = MplCanvas(self, width=5, height=4, dpi=100)
        #sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

        self.statusBar().showMessage("this is status bar") 

        self.setCentralWidget(self.chronometer_widget)
        self.show()


class CentralWidget(QWidget):

    def __init__(self, parent: QWidget = None):
        if parent is None:
            super(QWidget, self).__init__()
        else:
            super(QWidget, self).__init__(parent)
        """
        general_layout = QVBoxLayout()
        toolbar_layout = QHBoxLayout()
        buttons_layout = QHBoxLayout()
        content_layout = QHBoxLayout()

        añadir = QIcon("UIs/anadir.png")
        delete = QIcon("UIs/borrar.png")
        editar = QIcon("UIs/editar.png")
        save = QIcon("UIs/save.png")

        # Toolbar
        toolbar = QToolBar()
        self.parent().addToolBar(toolbar)

        toolbar_button_add = QAction(QIcon(añadir), "&Add", self)
        toolbar_button_add.triggered.connect(self.add)
        toolbar.addAction(toolbar_button_add)  # Comentar estas dos lineas si solo quieres el desplegable
        toolbar.addSeparator()  # si solo quieres el desplegable

        toolbar_button_delete = QAction(QIcon(delete), "&Delete", self)
        toolbar_button_delete.triggered.connect(self.delete)
        toolbar.addAction(toolbar_button_delete)  # Comentar estas dos lineas si solo quieres el desplegable
        toolbar.addSeparator()  # si solo quieres el desplegable

        toolbar_button_edit = QAction(QIcon(editar), "&Edit", self)
        toolbar_button_edit.triggered.connect(self.edit)
        toolbar.addAction(toolbar_button_edit)  # Comentar estas dos lineas si solo quieres el desplegable
        toolbar.addSeparator()  # si solo quieres el desplegable

        toolbar_button_save = QAction(QIcon(save), "&Save", self)
        toolbar_button_edit.triggered.connect(self.save)
        toolbar.addAction(toolbar_button_save)  # Comentar estas dos lineas si solo quieres el desplegable
        toolbar.addSeparator()  # si solo quieres el desplegable

        menu = self.parent().menuBar()
        file_menu = menu.addMenu("&Menu")
        file_menu.addAction(toolbar_button_add)
        file_menu.addSeparator()
        file_menu.addAction(toolbar_button_delete)
        file_menu.addSeparator()
        file_menu.addAction(toolbar_button_edit)
        file_menu.addSeparator()
        file_menu.addAction(toolbar_button_save)

        # Listado
        listWidget = QListWidget()
        listWidget.resize(200, 400)
        listWidget.setWindowTitle("Listado")
        listWidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        listWidget.addItem("Item 1")
        listWidget.addItem("Item 2")
        listWidget.itemClicked.connect(self.clicked)

        parent_tab_widget = QTabWidget()
        tab_patient = UtilForm(departmenJson)  # Tab1

        tab_performance = MplCanvas(self, width=5, height=4, dpi=100)  # Tab2 Grafica
        tab_performance.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40], [5, 4, 6, 9, 1])

        tab_chrono = Color("green")  # Tab3 Color

        parent_tab_widget.resize(300, 300)  # Tab Parent

        parent_tab_widget.addTab(tab_patient, "Paciente")
        parent_tab_widget.addTab(tab_performance, "Rendimiento")
        parent_tab_widget.addTab(tab_chrono, "Cronómetro")

        content_layout.addWidget(listWidget, stretch=3,
                                 alignment=Qt.AlignTop)  # Listado // Quitar el alignment si lo quieres estirado hasta abajo
        content_layout.addWidget(parent_tab_widget, stretch=9)

        general_layout.addLayout(toolbar_layout)  # Añadido el toolbar
        general_layout.addLayout(buttons_layout)  # Añadido los botones
        general_layout.addLayout(content_layout)  # Añadido los tabs y list
        
        self.setMinimumSize(900, 600)
        self.setLayout(general_layout)
        """

    def init(self):
        general_layout = QVBoxLayout()
        toolbar_layout = QHBoxLayout()
        buttons_layout = QHBoxLayout()
        content_layout = QHBoxLayout()

        """
        añadir = QIcon("UIs/anadir.png")
        delete = QIcon("UIs/borrar.png")
        editar = QIcon("UIs/editar.png")
        save = QIcon("UIs/save.png")
        """

        # Toolbar
        toolbar = QToolBar()
        self.parent().addToolBar(toolbar)

        """
        toolbar_button_add = QAction(QIcon(añadir), "&Add", self)
        toolbar_button_add.triggered.connect(self.add)
        toolbar.addAction(toolbar_button_add)  # Comentar estas dos lineas si solo quieres el desplegable
        toolbar.addSeparator()  # si solo quieres el desplegable

        toolbar_button_delete = QAction(QIcon(delete), "&Delete", self)
        toolbar_button_delete.triggered.connect(self.delete)
        toolbar.addAction(toolbar_button_delete)  # Comentar estas dos lineas si solo quieres el desplegable
        toolbar.addSeparator()  # si solo quieres el desplegable

        toolbar_button_edit = QAction(QIcon(editar), "&Edit", self)
        toolbar_button_edit.triggered.connect(self.edit)
        toolbar.addAction(toolbar_button_edit)  # Comentar estas dos lineas si solo quieres el desplegable
        toolbar.addSeparator()  # si solo quieres el desplegable

        toolbar_button_save = QAction(QIcon(save), "&Save", self)
        toolbar_button_edit.triggered.connect(self.save)
        toolbar.addAction(toolbar_button_save)  # Comentar estas dos lineas si solo quieres el desplegable
        toolbar.addSeparator()  # si solo quieres el desplegable
        """

        menu = self.parent().menuBar()

        file_menu = menu.addMenu("&Menu")

        """
        file_menu.addAction(toolbar_button_add)
        file_menu.addSeparator()
        file_menu.addAction(toolbar_button_delete)
        file_menu.addSeparator()
        file_menu.addAction(toolbar_button_edit)
        file_menu.addSeparator()
        file_menu.addAction(toolbar_button_save)
        """

        # Listado
        listWidget = QListWidget()
        listWidget.resize(200, 400)
        listWidget.setWindowTitle("Listado")
        listWidget.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        listWidget.addItem("Item 1")
        listWidget.addItem("Item 2")
        listWidget.itemClicked.connect(self.clicked)

        parent_tab_widget = QTabWidget()
        tab_patient = UtilForm(departmenJson)  # Tab1

        tab_performance = MplCanvas(self, width=5, height=4, dpi=100)  # Tab2 Grafica
        #tab_performance.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40], [5, 4, 6, 9, 1])

        tab_chrono = Color("green")  # Tab3 Color

        parent_tab_widget.resize(300, 300)  # Tab Parent

        parent_tab_widget.addTab(tab_patient, "Paciente")
        parent_tab_widget.addTab(tab_performance, "Rendimiento")
        parent_tab_widget.addTab(tab_chrono, "Cronómetro")

        content_layout.addWidget(listWidget, stretch=3,
                                 alignment=Qt.AlignTop)  # Listado // Quitar el alignment si lo quieres estirado hasta abajo
        content_layout.addWidget(parent_tab_widget, stretch=9)

        general_layout.addLayout(toolbar_layout)  # Añadido el toolbar
        general_layout.addLayout(buttons_layout)  # Añadido los botones
        general_layout.addLayout(content_layout)  # Añadido los tabs y list

        self.setMinimumSize(900, 600)
        self.setLayout(general_layout)


    def add(self):
        print("Añadir")
        self.parent().statusBar().showMessage("Status: Add") 
    
    def delete(self):
        print("Delete")
        self.parent().statusBar().showMessage("Status: Delete") 
    
    def edit(self):
        print("Edit")
        self.parent().statusBar().showMessage("Status: Edit") 

    def save(self):
        print("Save")
        self.parent().statusBar().showMessage("Status: Save") 


    def clicked(self, item):
        QMessageBox.information(self, "ListWidget", "ListWidget: " + item.text())
        self.parent().statusBar().showMessage("Status: List") 


departmenJson = {
    'Nombre': 'Enrique',
    'Apellido': 'Cotaina',
    'Edad': '19'
}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())