import os
import sys

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMainWindow, QListView, QWidget, QLabel, QDialog

from GUI import GUI_Resources
from Utils import cypher
from database.database_controller import Connection
from database.models import UsuariModel, PacientsModel


class UI(QMainWindow):
    """ Clase que importara los ajustes de Javi. Con la main window"""
    def __init__(self, debug=False):
        super().__init__()
        # TODO SINGLETONS ?¿?¿?¿?¿
        UI.instance = self
        UI.DB = "db"+os.sep+f"default.db"
        UI.threadpool = QThreadPool()
        UI.DEBUG = debug
        # TODO SINGLETONS ?¿?¿?¿?¿ THEY ARE REALLY NEEDED?
        self.validUser = False
        self.login_form = GUI_Resources.get_login_register_dialog()
        self.user_credentials = {"result": False}
        self.connection = Connection()
        self.credentials()
        central = GUI_Resources.get_main_widget()
        GUI_Resources.get_cronometro_widget_ui()
        if self.user_credentials["result"]:

            central.pacients_list_view.setModel(PacientsModel())
            self.setCentralWidget(central)
            self.show()
        else:
            sys.exit(0)
        # self.cen = QListView()
        # self.modelTest = models.PacientsModel()
        # self.cen.setModel(self.modelTest)
        # self.setCentralWidget(self.cen)
        # self.show()
        # self.modelTest.append(Pacients("AAAA","aaa","asdas",1,"asda"))
        # self.modelTest.layoutChanged.emit()

    def credentials(self):
        """ Funcion que pide las credenciales. Si le dan a cancelar, sale del programa. Si son incorrectas
        reintenta la conexion indefinidamente"""
        self.login_form.show()
        if not self.DEBUG:
            self.login_form.login_validator = UsuariModel.valid_user
        else:
            self.login_form.login_validator = UI.validator
        result = self.login_form.exec_()
        if result == 1 and self.login_form.result["result"]:
            self.user_credentials = self.login_form.result
        else:
            sys.exit(0)

    @staticmethod
    def validator(a,aa):
        return True

    @staticmethod
    def get_instace():
        return UI.instance
