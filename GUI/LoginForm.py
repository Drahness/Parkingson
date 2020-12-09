import sys

import Utils
from GUI import GUI_Resources

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget


class LoginRegisterWindow(QDialog):
    """
    Formulario de Login/Registro, la variable result guardara el resultado, al darle aceptar.

    Una entrada correcta, dara como resultado una mapa asi:

    {\n"order": "login",
    \t"username": username_in_field,\n
    \t"password": password_in_field,\n
    \t"result": False or True\n}
    La clave "order", podra tener "login" o "register"
    """

    def __init__(self):
        super(LoginRegisterWindow, self).__init__()
        self.result = {"result": False}
        tab: QTabWidget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(tab)
        self._login_validator = None  # method
        self.login_widget = GUI_Resources.get_login_tab()
        self.register_widget = GUI_Resources.get_register_tab()

        tab.addTab(self.login_widget, "Login")
        tab.addTab(self.register_widget, "Registro")
        self.setLayout(layout)

        self.login_widget.positive.clicked.connect(self.__positive_login)
        self.login_widget.negative.clicked.connect(self.__cancelButtons)
        self.register_widget.Rnegative.clicked.connect(self.__cancelButtons)
        self.register_widget.Rpositive.clicked.connect(self.__positive_register)

    def __cancelButtons(self):
        sys.exit(0)

    def __positive_register(self):
        print("REGISTER")
        self.result = {"order": "register",
                       "username": self.register_widget.usernamefield.text(),
                       "password": Utils.cypher(self.register_widget.passwordfield.text())}
        self.accept()


    def __positive_login(self):
        print("LOGIN")
        if self.login_validator is None:
            raise AttributeError("You need to set the property self.login_validator to a method parametrized with 2 "
                                 "arguments username and password")
        self.result = {"order": "login",
                       "username": self.login_widget.usernamefield.text(),
                       "password": Utils.cypher(self.login_widget.passwordfield.text())
                       }
        self.result["result"] = self._login_validator(self.result["username"], self.result["password"])
        if self.result["result"]:
            self.accept()
        else:
            self.login_widget.error_label.setText("Usuario o contraseña incorrectos.")
            self.login_widget.passwordfield.setFocus()
            self.login_widget.passwordfield.selectAll()

    @property
    def login_validator(self):
        "Esta property, es utilizada para checkear las credenciales en el login."
        return self._login_validator

    @login_validator.setter
    def login_validator(self, method):
        """Tienes que pasarle una referencia a un metodo que tenga dos argumentos.
        username,password"""
        self._login_validator = method


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoginRegisterWindow()
    window.show()
    app.exec()
