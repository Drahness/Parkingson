import sys

from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTabWidget, QVBoxLayout, QDialog

import Utils
from GUI import GUI_Resources
from GUI.GUI_Resources import get_shown_icon, get_hidden_icon


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

    def __init__(self,conn):
        super(LoginRegisterWindow, self).__init__()
        self.setWindowTitle("Autenticador")
        self.result = {}
        self.conn = conn
        self.tab: QTabWidget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.tab)
        self._login_validator = self.validator_debug  # method
        self._user_checker = self.validator_debug
        self.login_widget = GUI_Resources.get_login_tab()
        self.register_widget = GUI_Resources.get_register_tab()

        self.oculto_login: QPushButton = self.login_widget.oculto
        self.oculto_register: QPushButton = self.register_widget.oculto
        self.oculto_confirm: QPushButton = self.register_widget.oculto_confirm
        self.tab.addTab(self.login_widget, "Login")
        self.tab.addTab(self.register_widget, "Registro")
        self.setLayout(layout)
        self.shown: QIcon = get_shown_icon()
        self.hidden: QIcon = get_hidden_icon()
        self.debug = False
        self.login_widget.positive.clicked.connect(self.__positive_login)
        self.login_widget.negative.clicked.connect(self.__cancel_buttons)
        self.register_widget.Rnegative.clicked.connect(self.__cancel_buttons)
        self.register_widget.Rpositive.clicked.connect(self.__positive_register)
        self.oculto_confirm.pressed.connect(self.show_handler)
        self.oculto_confirm.released.connect(self.hide_handler)
        self.oculto_login.pressed.connect(self.show_handler)
        self.oculto_login.released.connect(self.hide_handler)
        self.oculto_register.released.connect(self.hide_handler)
        self.oculto_register.pressed.connect(self.show_handler)
        self.login_widget.passwordfield.textEdited.connect(self.hide_handler)
        self.register_widget.passwordfield.textEdited.connect(self.hide_handler)
        self.register_widget.confirm_password.textEdited.connect(self.hide_handler)

    def __cancel_buttons(self):
        sys.exit(0)

    def __positive_register(self):
        print("REGISTER")
        if self._user_checker(self.register_widget.usernamefield.text()):
            if self.register_widget.passwordfield.text() == self.register_widget.confirm_password.text():
                self.result = { "result":True,
                                "order": "register",
                                "username": self.register_widget.usernamefield.text(),
                                "password": Utils.cypher(self.register_widget.passwordfield.text())}
                self.accept()
            else:
                self.register_widget.error_label.setText("Las contraseñas no coinciden.")
        else:
            self.register_widget.error_label.setText("Usuario existente.")


    def __positive_login(self):
        print("LOGIN")
        if self.login_validator is None:
            raise AttributeError("You need to set the property self.login_validator to a method parametrized with 2 "
                                 "arguments username and password")
        self.result = {"order": "login",
                       "username": "Admin" if self.debug else self.login_widget.usernamefield.text(),
                       "password": Utils.cypher(self.login_widget.passwordfield.text())
                       }
        self.result["result"] = self._login_validator(self.result["username"], self.result["password"])
        if self.result["result"]:
            self.accept()
        else:
            self.login_widget.error_label.setText("Usuario o contraseña incorrectos.")
            self.login_widget.passwordfield.setFocus()
            self.login_widget.passwordfield.selectAll()

    def hide_handler(self):
        if self.sender() == self.oculto_login or self.sender() == self.login_widget.passwordfield:
            self.login_widget.passwordfield.setEchoMode(QLineEdit.Password)
            self.oculto_login.setIcon(self.hidden)
        elif self.sender() == self.oculto_register or self.sender() == self.register_widget.passwordfield:
            self.register_widget.passwordfield.setEchoMode(QLineEdit.Password)
            self.oculto_register.setIcon(self.hidden)
        elif self.sender() == self.oculto_confirm or self.sender() == self.register_widget.confirm_password:
            self.register_widget.confirm_password.setEchoMode(QLineEdit.Password)
            self.oculto_confirm.setIcon(self.hidden)

    def show_handler(self):
        if self.sender() == self.oculto_login:
            self.login_widget.passwordfield.setEchoMode(QLineEdit.Normal)
            self.oculto_login.setIcon(self.shown)
        elif self.sender() == self.oculto_register:
            self.register_widget.passwordfield.setEchoMode(QLineEdit.Normal)
            self.oculto_register.setIcon(self.shown)
        elif self.sender() == self.oculto_confirm or self.sender() == self.register_widget.confirm_password:
            self.register_widget.confirm_password.setEchoMode(QLineEdit.Normal)
            self.oculto_confirm.setIcon(self.shown)

    @property
    def login_validator(self):
        """Esta property, es utilizada para checkear las credenciales en el login."""
        return self._login_validator

    @login_validator.setter
    def login_validator(self, method):
        """Tienes que pasarle una referencia a un metodo que tenga dos argumentos.
        username,password"""
        self._login_validator = method

    @property
    def user_checker(self):
        """Esta property, es utilizada para checkear las credenciales en el login."""
        return self._user_checker

    @user_checker.setter
    def user_checker(self, method):
        """Tienes que pasarle una referencia a un metodo que tenga dos argumentos.
        username,password"""
        self._user_checker = method

    @staticmethod
    def validator_debug(*args):
        return True

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0 == QtCore.Qt.Key_Enter:
            if self.tab.currentWidget() == self.login_widget:
                self.login_widget.positive.clicked.emit()
            elif self.tab.currentWidget() == self.register_widget:
                self.register_widget.positive.clicked.emit()
        elif 10 == QtCore.Qt.Key_Escape:
            self.__cancel_buttons()
        super().keyPressEvent(a0)

