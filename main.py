# This is a sample Python script.
import sys
import threading
from datetime import timedelta
import datetime

from PyQt5 import uic, QtWidgets
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PyQt5.QtWidgets import QMainWindow, QWidget
from LoginForm import LoginRegisterWindow

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.validUser = False
        self.login_form: LoginRegisterWindow = LoginRegisterWindow()

        self.credentials()

    def credentials(self):
        self.login_form.show()
        self.login_form.exec_()





# Press the green button in the gutter to run the script.

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    mainWindow = UI()

    app.exec()