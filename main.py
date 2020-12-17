import sys

from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon

from argparse import ArgumentParser

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    argparser = ArgumentParser()
    argparser.add_argument('-d', '--debug', help="Disables logon", action="store_true")
    arguments = argparser.parse_args()
    from main_window import UI
    mainWindow = UI(arguments.debug)
    app.exec()
