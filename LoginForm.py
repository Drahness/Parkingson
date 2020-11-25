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
        self.username = self.findChild(QLabel,"username")
        self.password = self.findChild(QLabel,"password")
        self.password_field = self.findChild(QLineEdit,"password_field")
        self.username_field = self.findChild(QLineEdit,"username_field")
        self.button_box = self.findChild(QDialogButtonBox)
        #self.button_box: QDialogButtonBox = self.button_box
        #self.button_box.Ok

class LoginRegisterWindow(QWidget):
    def __init__(self):
        super(LoginRegisterWindow, self).__init__()
        tab: QTabWidget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(tab)
        self.login_widget = QDialog()
        self.register_widget = QDialog()
        loginTab = uic.loadUi("login_dialog.ui", self.login_widget)
        registerTab = uic.loadUi("register_dialog.ui", self.register_widget)

        tab.addTab(self.login_widget, "Login")
        tab.addTab(self.register_widget, "Registro")
        self.setLayout(layout)

        print(self.login_widget.findChild(QPushButton, "positive"))
        print(self.login_widget.findChild(QPushButton, "negative"))
        print(self.register_widget.findChild(QPushButton, "positive"))
        print(self.register_widget.findChild(QPushButton, "negative"))
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

        loginTab.positive.clicked.connect(self.positive_login)
            #.clicked.connect(self.cancelButtons)
        #self.buttonPositiveRegister.clicked.connect(self.positive_register)
        #self.buttonNegativeRegister.clicked.connect(self.positive_login)
        #self.buttonNegativeLogin.clicked.connect(self.cancelButtons)

        self.result = None
        self.finished = False

    def cancelButtons(self):
        print("CANCEL")
        pass

    def positive_register(self):
        print("REGISTER")
        pass

    def positive_login(self):
        print("LOGIN")
        pass


    def exec_(self):
        self.login_widget.exec_()
        self.register_widget.exec_()

    """Waits for user input."""
    def wait_for_result(self):
        while not self.finished:
            pass
        return self.result




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)




    window = LoginRegisterWindow()
    #window = QWidget()

    window.show()
    print(dir(window))
    app.exec()
