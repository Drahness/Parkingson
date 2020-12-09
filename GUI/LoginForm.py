from pathlib import Path
import sys

import Utils
from GUI import GUI_Resources

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget

from database.models import UsuariModel


class LoginRegisterWindow(QDialog):
    """
    Formulario de Login/Registro, la variable result guardara el resultado, al darle aceptar.

    Una entrada correcta, dara como resultado una mapa asi:

    {"order": "login",
     "username": username_in_field,
     "password": password_in_field}
     La clave "order", podra tener "login" o "register"
    """

    def __init__(self):
        super(LoginRegisterWindow, self).__init__()
        self.result = None
        tab: QTabWidget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(tab)

        self.login_widget = GUI_Resources.get_login_tab()
        self.register_widget = GUI_Resources.get_register_tab()

        # self.loginTab = uic.loadUi(GUI_Resources.LOGIN_DIALOG, self.login_widget)
        # self.registerTab = uic.loadUi(GUI_Resources.REGISTER_DIALOG, self.register_widget)

        tab.addTab(self.login_widget, "Login")
        tab.addTab(self.register_widget, "Registro")
        self.setLayout(layout)

        self.login_widget.positive.clicked.connect(self.__positive_login)
        self.login_widget.negative.clicked.connect(self.__cancelButtons)
        self.register_widget.Rnegative.clicked.connect(self.__cancelButtons)
        self.register_widget.Rpositive.clicked.connect(self.__positive_register)
        self.reject.connect()

    def __cancelButtons(self):
        sys.exit(0)

    def __positive_register(self):
        print("REGISTER")
        self.result = {"order": "register",
                       "username": self.register_widget.usernamefield.text(),
                       "password": Utils.cypher(self.register_widget.passwordfield.text())}
        self.accept()
            pass
    def __positive_login(self):
        print("LOGIN")
        self.result = {"order": "login",
                       "username": self.login_widget.usernamefield.text(),
                       "password": Utils.cypher(self.login_widget.passwordfield.text())}
        if UsuariModel.valid_user(self.result["username"], self.result["password"]):
            self.accept()
        else:
            self.login_widget.error_label.setText("Usuario o contraseña incorrectos.")
            self.login_widget.passwordfield.setFocus()
            self.login_widget.passwordfield.selectAll()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoginRegisterWindow()
    window.show()
    app.exec()
