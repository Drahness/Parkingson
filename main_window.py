import sys

from PyQt5.QtWidgets import QMainWindow

from GUI.LoginForm import LoginRegisterWindow
from Utils import cypher
from database.database_controller import Connection


class UI(QMainWindow):
    """ Clase que importara los ajustes de Javi."""

    def __init__(self):
        super().__init__()
        self.validUser = False
        self.login_form: LoginRegisterWindow = LoginRegisterWindow()
        self.user_credentials = None

        self.credentials()
        self.connection = Connection(name="test\\haaasd.db")

    def credentials(self):
        """ Funcion que pide las credenciales. Si le dan a cancelar, sale del programa."""
        self.login_form.show()
        #       print(self.login_form.exec_()) print 1 on success, 0 on reject.
        if self.login_form.exec_() == 1:
            self.login_form.result["password"] = cypher(self.login_form.result["password"])
            self.user_credentials = self.login_form.result
        else:
            sys.exit(0)
        self.login_form.show()
