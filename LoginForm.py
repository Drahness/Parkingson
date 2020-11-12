import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QWidget, QDialog, QVBoxLayout


class LoginForm(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi("login_form.ui", self)
        print(self.findChild(QVBoxLayout,"a"))



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = LoginForm()
    window.show()
    print(dir(window))
    app.exec()