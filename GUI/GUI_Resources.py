from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog
from .LoginForm import LoginRegisterWindow
from .main_window_javi import CentralWidgetParkingson

GUI_FOLDER = Path("GUI")
UIS_FOLDER = GUI_FOLDER / Path("UIs")

LOGIN_DIALOG = UIS_FOLDER / Path("login_dialog.ui")
REGISTER_DIALOG = UIS_FOLDER / Path("register_dialog.ui")
ERROR_DIALOG = UIS_FOLDER / Path("error_dialog.ui")


def get_login_tab() -> QDialog:
    return uic.loadUi(LOGIN_DIALOG, QDialog())


def get_register_tab() -> QDialog:
    return uic.loadUi(REGISTER_DIALOG, QDialog())


def get_error_dialog() -> QDialog:
    return uic.loadUi(ERROR_DIALOG, QDialog())


def get_error_dialog_msg(msg: str) -> QDialog:
    dialog = get_error_dialog()
    dialog.label.setText(msg)
    return dialog

def get_login_register_dialog() -> QDialog:
    return LoginRegisterWindow()

def get_main_widget():
    return CentralWidgetParkingson()