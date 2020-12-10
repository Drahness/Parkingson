import os
import sys

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QMainWindow, QDialog, QVBoxLayout

from GUI import GUI_Resources
from GUI.form import Form
from database.database_controller import Connection
from database.entities import Pacient
from database.models import UsuariListModel, PacientsListModel


class UI(QMainWindow):
    """ Clase que importara los ajustes de Javi. Con la main window"""

    def __init__(self, debug=False):
        super().__init__()
        # TODO SINGLETONS ?¿?¿?¿?¿
        UI.instance = self
        UI.DB = "db" + os.sep + f"default.db"
        UI.threadpool = QThreadPool()
        UI.DEBUG = debug
        # TODO SINGLETONS ?¿?¿?¿?¿ THEY ARE REALLY NEEDED?
        self.validUser = False
        self.login_form = GUI_Resources.get_login_register_dialog()
        self.user_credentials = {"result": False}
        self.connection = Connection()
        self.credentials()
        self.central = GUI_Resources.get_main_widget()

        self.central.actions_buttons[self.central.ADD_button_key].clicked.connect(self.add_pacient_slot)
        self.central.actions_buttons[self.central.DELETE_button_key].clicked.connect(self.del_pacient_slot)
        self.central.actions_buttons[self.central.EDIT_button_key].clicked.connect(self.mod_pacient_slot)

        if self.user_credentials["result"]:
            self.central.pacients_list_view.setModel(PacientsListModel())
            self.setCentralWidget(self.central)
            self.show()
            self.central.pacients_list_view.setModel(PacientsListModel.get_instance())
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
            self.login_form.login_validator = UsuariListModel.valid_user
        else:
            self.login_form.login_validator = UI.validator_debug
        result = self.login_form.exec_()
        if result == 1 and self.login_form.result["result"]:
            self.user_credentials = self.login_form.result
        else:
            sys.exit(0)

    @staticmethod
    def validator_debug(a, aa):
        return True

    @staticmethod
    def get_instace():
        return UI.instance

    """"""

    def add_pacient_slot(self):
        qdial = QDialog()
        lay = QVBoxLayout()
        qdial.setLayout(lay)
        form = Form({"nombre": "", "dni": "", "estadio": "int", "apellidos": ""}, True)
        """lay.addWidget(form)
        aceptar = QPushButton()
        cancelar = QPushButton()
        aceptar.clicked.connect(QDialog.accept)
        cancelar.clicked.connect(QDialog.reject)
        lay2 = QHBoxLayout()
        qwid = QWidget()
        lay.addWidget(qwid)
        lay2.addWidget(aceptar)
        lay2.addWidget(cancelar)
        qwid.setLayout(lay2) """
        if form.exec_() == 1:
            PacientsListModel.get_instance().append(Pacient(dictionary=form.get_values()))

    def del_pacient_slot(self):
        pass

    def mod_pacient_slot(self):
        pass

    def pacient_selected_slot(self):
        pass
