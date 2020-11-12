import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow, QWidget


class UserListWidget(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("user_list.ui",self)
        self.findChild()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = UserListWidget()
    window.show()
    print(dir(window))
    app.exec()