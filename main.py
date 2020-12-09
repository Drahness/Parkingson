import sys

from PyQt5 import QtWidgets
from main_window import UI
from argparse import ArgumentParser

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    argparser = ArgumentParser()
    argparser.add_argument('-d', '--debug', help="Enables the debug/verbose mode.", action="store_true")
    arguments = argparser.parse_args()

    mainWindow = UI(arguments.debug)
    app.exec()
