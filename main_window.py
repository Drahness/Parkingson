import os
import sys
import time

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QListView, QWidget, QLabel, QDialog

from GUI.LoginForm import LoginRegisterWindow
from Utils import cypher
from database.database_controller import Connection
from database.models import Pacients, UsuariModel


class UI(QMainWindow):
    """ Clase que importara los ajustes de Javi. Con la main window"""

    def __init__(self):
        super().__init__()
        UI.instance = self
        UI.DB = "db"+os.sep+f"default.db"
        self.validUser = False
        self.login_form: LoginRegisterWindow = LoginRegisterWindow()
        self.user_credentials = None
        self.credentials()
        self.connection = Connection()

        # self.cen = QListView()
        # self.modelTest = models.PacientsModel()
        # self.cen.setModel(self.modelTest)
        # self.setCentralWidget(self.cen)
        # self.show()
        # self.modelTest.append(Pacients("AAAA","aaa","asdas",1,"asda"))
        # self.modelTest.layoutChanged.emit()

    def credentials(self):
        """ Funcion que pide las credenciales. Si le dan a cancelar, sale del programa."""
        self.login_form.show()
        q_widget = uic.loadUi("error_dialog.ui",QDialog())
        #       print(self.login_form.exec_()) print 1 on success, 0 on reject.
        if self.login_form.exec_() == 1:
            password = cypher(self.login_form.result["password"])
            username = self.login_form.result["username"]
            while not UsuariModel.valid_user(username, password):
                q_widget.show()
                q_widget.exec_()
                self.login_form = LoginRegisterWindow()
                self.login_form.show()
                if self.login_form.exec_() == 1:
                    password = cypher(self.login_form.result["password"])
                    username = self.login_form.result["username"]
                else:
                    sys.exit(0)
        else:
            sys.exit(0)

    @staticmethod
    def get_instace():
        return UI.instance
