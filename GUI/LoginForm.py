from pathlib import Path
import sys
from GUI import GUI_Resources

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget


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

        self.login_widget = QDialog()
        self.register_widget = QDialog()

        self.loginTab = uic.loadUi(GUI_Resources.LOGIN_DIALOG, self.login_widget)
        self.registerTab = uic.loadUi(GUI_Resources.REGISTER_DIALOG, self.register_widget)

        tab.addTab(self.login_widget, "Login")
        tab.addTab(self.register_widget, "Registro")
        self.setLayout(layout)

        self.loginTab.positive.clicked.connect(self.__positive_login)
        self.loginTab.negative.clicked.connect(self.__cancelButtons)
        self.registerTab.Rnegative.clicked.connect(self.__cancelButtons)
        self.registerTab.Rpositive.clicked.connect(self.__positive_register)

    def __cancelButtons(self):
        print("CANCEL")
        self.result = False
        self.__closeForm()
        self.reject()

    def __positive_register(self):
        print("REGISTER")
        self.result = {"order": "regiser",
                       "username": self.registerTab.usernamefield.text(),
                       "password": self.registerTab.passwordfield.text()}
        self.__closeForm()
        self.accept()

    def __positive_login(self):
        print("LOGIN")
        self.result = {"order": "login",
                       "username": self.loginTab.usernamefield.text(),
                       "password": self.loginTab.passwordfield.text()}
        self.__closeForm()
        self.accept()

    def __closeForm(self):
        self.registerTab.close()
        self.loginTab.close()
        self.login_widget.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LoginRegisterWindow()
    window.show()
    app.exec()
