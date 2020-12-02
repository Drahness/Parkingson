import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget,QVBoxLayout, QLabel, QHBoxLayout, QTextEdit, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, QSize, Qt


class App(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("Pacientes")
        self.setFixedSize(QSize(1000, 1000))


        
        self.interfaz_widget = Interfaz(self)
        self.setCentralWidget(self.interfaz_widget)
        
        self.show()
    
class Interfaz(QWidget):
    
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self._createTopButtons()
        self._createTxt()

    def _createTopButtons(self):

        sp = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.buttonAdd=QPushButton("Añadir")
        self.buttonAdd.setSizePolicy(sp)

        self.buttonDelete=QPushButton("Eliminar")
        self.buttonDelete.setSizePolicy(sp)
        self.buttonEdit=QPushButton("Editar")
        self.buttonEdit.setSizePolicy(sp)

        self.layoutBotonesOpciones = QHBoxLayout(self)

        self.layoutBotonesOpciones.addWidget(self.buttonAdd, Qt.AlignLeft)
        self.layoutBotonesOpciones.addWidget(self.buttonDelete, Qt.AlignLeft)
        self.layoutBotonesOpciones.addWidget(self.buttonEdit, Qt.AlignLeft)

        self.layoutBotonesOpciones.addStretch()
        self.layout.addLayout(self.layoutBotonesOpciones)

    def _createTxt(self):
        
        self.text=QTextEdit()
        self.layoutTexto = QVBoxLayout(self)
        self.layoutTexto.addWidget(self.text)

        self.layout.addLayout(self.layoutTexto)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

























