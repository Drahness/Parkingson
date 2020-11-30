import sys
import sqlite3

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QVBoxLayout, QLabel, QLineEdit, QDialogButtonBox, \
    QPushButton, QTabWidget
from Utils import KeyValueMutable, KeyValueWidget


class LoginForm(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("login_form.ui", self)
        self.username = self.findChild(QLabel, "username")
        self.password = self.findChild(QLabel, "password")
        self.password_field = self.findChild(QLineEdit, "password_field")
        self.username_field = self.findChild(QLineEdit, "username_field")
        self.button_box = self.findChild(QDialogButtonBox)
        # self.button_box: QDialogButtonBox = self.button_box
        # self.button_box.Ok


class LoginRegisterWindow(QDialog):
    def __init__(self):
        super(LoginRegisterWindow, self).__init__()
        tab: QTabWidget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(tab)
        self.login_widget = QDialog()
        self.register_widget = QDialog()
        self.loginTab = uic.loadUi("login_dialog.ui", self.login_widget)
        self.registerTab = uic.loadUi("register_dialog.ui", self.register_widget)

        tab.addTab(self.login_widget, "Login")
        tab.addTab(self.register_widget, "Registro")
        self.setLayout(layout)
        '''
        self.buttonPositiveLogin = self.login_widget.findChild(QPushButton, "Lpositive")
        self.buttonPositiveRegister = self.register_widget.findChild(QPushButton, "Rpositive")
        self.buttonNegativeRegister = self.register_widget.findChild(QPushButton, "Rnegative")
        self.buttonNegativeLogin = self.login_widget.findChild(QPushButton, "Lnegative")
        
        self.FieldPassLogin = self.login_widget.findChild(QPushButton,"passwordfield")
        self.FieldUserRegister = self.register_widget.findChild(QPushButton,"usernamefield")
        self.FieldPassRegister = self.login_widget.findChild(QPushButton,"passwordfield")
        self.FieldUserLogin = self.register_widget.findChild(QPushButton,"usernamefield")
        '''

        self.loginTab.positive.clicked.connect(self.positive_login)
        self.loginTab.negative.clicked.connect(self.cancelButtons)
        self.registerTab.negative.clicked.connect(self.cancelButtons)
        self.registerTab.positive.clicked.connect(self.positive_register)
        self.result = None

    def cancelButtons(self):
        print("CANCEL")
        self.result = False
        self.closeForm()
        self.reject()

    def positive_register(self):
        print("REGISTER")
        self.result = {"order": "regiser",
                       "username": self.registerTab.usernamefield.text(),
                       "password": self.registerTab.passwordfield.text()}
        self.closeForm()
        self.accept()

    def positive_login(self):
        print("LOGIN")
        self.result = {"order": "login",
                       "username": self.loginTab.usernamefield.text(),
                       "password": self.loginTab.passwordfield.text()}
        self.closeForm()
        self.accept()


    def closeForm(self):
        self.registerTab.close()
        self.loginTab.close()
        self.login_widget.close()


    """Waits for user input."""

    def wait_for_result(self):
        while not self.finished:
            pass
        return self.result


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = LoginRegisterWindow()
    # window = QWidget()

    window.show()
    print(dir(window))
    app.exec()
