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
        self.button_box: QDialogButtonBox = self.button_box
        #self.button_box.Ok

class LoginRegisterWindow(QWidget):
    def __init__(self):
        super(LoginRegisterWindow, self).__init__()
        tab: QTabWidget = QTabWidget()
        layout = QVBoxLayout()
        layout.addWidget(tab)
        widget = QDialog()
        widget2 = QDialog()
        uic.loadUi("login_form.ui",widget)
        uic.loadUi("register_dialog.ui", widget2)
        tab.addTab(widget,"Login")
        tab.addTab(widget2,"Registro")
        self.setLayout(layout)

class test(QWidget):
    def __init__(self):

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = LoginRegisterWindow()
    window = QWidget()

    window.show()
    print(dir(window))
    app.exec()