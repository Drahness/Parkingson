from pathlib import Path

from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QWidget

GUI_FOLDER = Path("GUI")
UIS_FOLDER = GUI_FOLDER / Path("UIs")

LOGIN_DIALOG = UIS_FOLDER / Path("login_dialog.ui")
REGISTER_DIALOG = UIS_FOLDER / Path("register_dialog.ui")
ERROR_DIALOG = UIS_FOLDER / Path("error_dialog.ui")
CRONOMETRO_WIDGET = UIS_FOLDER / Path("cronometro.ui")


def get_login_tab(to: QDialog = None) -> QDialog:
    if to is None:
        return uic.loadUi(LOGIN_DIALOG, QDialog())
    else:
        return uic.loadUi(LOGIN_DIALOG, to)


def get_register_tab(to: QDialog = None) -> QDialog:
    if to is None:
        return uic.loadUi(REGISTER_DIALOG, QDialog())
    else:
        return uic.loadUi(REGISTER_DIALOG, to)


def get_error_dialog(to: QDialog = None) -> QDialog:
    if to is None:
        return uic.loadUi(ERROR_DIALOG, QDialog())
    else:
        return uic.loadUi(ERROR_DIALOG, to)


def get_error_dialog_msg(msg: str, to: QDialog = None) -> QDialog:
    dialog = get_error_dialog(to)
    dialog.label.setText(msg)
    return dialog


def get_login_register_dialog():
    from .LoginForm import LoginRegisterWindow  # Para evitar imports circulares
    return LoginRegisterWindow()


def get_main_widget():
    from .main_window_javi import CentralWidgetParkingson  # Para evitar imports circulares
    return CentralWidgetParkingson()


def get_cronometro_widget_ui(to: QWidget = None):
    if to is None:
        cronometro_ui: QWidget = uic.loadUi(CRONOMETRO_WIDGET, QWidget())
    else:
        cronometro_ui: QWidget = uic.loadUi(CRONOMETRO_WIDGET, to)
    return cronometro_ui


def get_cronometro_bar_widget():
    from .cronometro import ProgressCronometro  # Para evitar imports circulares
    return ProgressCronometro()


def get_cronometro_widget():
    from GUI.cronometro import Cronometro
    return Cronometro()
