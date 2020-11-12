# This is a sample Python script.
import sys

from PyQt5 import uic, QtWidgets
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from PyQt5.QtWidgets import QMainWindow


class UI(QMainWindow):
    def __init__(self):
        super().__init__()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = uic.loadUi("main_window.ui")
    window.show()
    app.exec()
