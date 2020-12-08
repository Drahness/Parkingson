import sys

from PyQt5 import QtWidgets
from main_window import UI

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = UI()
    app.exec()
