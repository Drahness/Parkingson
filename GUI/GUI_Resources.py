import os
import traceback
from pathlib import Path

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QWidget, QMessageBox

paths = Path(os.path.abspath(__name__)).parents
MAIN_FOLDER = None
for parent in Path(os.path.abspath(__name__)).parents:
    folder = parent / Path("GUI")
    if folder.exists():
        MAIN_FOLDER = parent

if MAIN_FOLDER is None:
    raise ModuleNotFoundError("Malformed modules.")

from . import resources

GUI_FOLDER = MAIN_FOLDER / Path("GUI")
UIS_FOLDER = GUI_FOLDER / Path("UIs")
LOGIN_DIALOG = UIS_FOLDER / Path("login_dialog.ui")
REGISTER_DIALOG = UIS_FOLDER / Path("register_dialog.ui")
ERROR_DIALOG = UIS_FOLDER / Path("error_dialog.ui")
CRONOMETRO_WIDGET = UIS_FOLDER / Path("cronometro.ui")
BASIC_FORM = UIS_FOLDER / Path("basic_form.ui")
PACIENT_WIDGET = UIS_FOLDER / Path("pacients_widget.ui")
NO_EDITABLE_PACIENT_WIDGET = UIS_FOLDER / Path("pacients_widget_noeditable.ui")
CONFIRMATION_DIALOG = UIS_FOLDER / Path("confirmation_dialog.ui")
GRAPH_WIDGET = UIS_FOLDER / Path("graph_widget.ui")


def get_add_icon():
    return QIcon(":/icons/add")


def get_delete_icon():
    return QIcon(":/icons/del")


def get_edit_icon():
    return QIcon(":/icons/edit")


def get_save_icon():
    return QIcon(":/icons/save")


def get_basic_form(to: QDialog = None) -> QDialog:
    if to is None:
        return uic.loadUi(BASIC_FORM, QDialog())
    else:
        return uic.loadUi(BASIC_FORM, to)


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


def get_error_dialog_msg(e: Exception, string_before_trace: str = None, title: str = None) -> QMessageBox:
    title = title or type(e).__name__
    string_before_trace = string_before_trace or ""
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setText(string_before_trace + "\n\n" + type(e).__name__ + ":")
    msg.setInformativeText(traceback.format_exc())
    msg.setWindowTitle(title)
    traceback.print_exc()
    return msg


def get_login_register_dialog(conn):
    from .LoginForm import LoginRegisterWindow  # Para evitar imports circulares
    return LoginRegisterWindow(conn)


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



def get_pacient_widget_ui(to: QWidget):
    if to is None:
        pacient_widget: QWidget = uic.loadUi(PACIENT_WIDGET, QWidget())
    else:
        pacient_widget: QWidget = uic.loadUi(PACIENT_WIDGET, to)
    return pacient_widget


def get_pacient_widget_ui_noeditable(to: QWidget):
    if to is None:
        pacient_widget: QWidget = uic.loadUi(NO_EDITABLE_PACIENT_WIDGET, QWidget())
    else:
        pacient_widget: QWidget = uic.loadUi(NO_EDITABLE_PACIENT_WIDGET, to)
    return pacient_widget


def get_pacient_widget():
    from GUI.tab_widgets import PacientWidget
    return PacientWidget()


def get_confirmation_dialog_ui(msg: str, to: QDialog = None):
    if to is None:
        confirmation_dialog = uic.loadUi(CONFIRMATION_DIALOG, QDialog())
    else:
        confirmation_dialog = uic.loadUi(CONFIRMATION_DIALOG, to)

    confirmation_dialog.confirm_label.setText(msg)
    return confirmation_dialog


def get_performance_widget(to: QWidget = None) -> QWidget:
    if to is None:
        performance = uic.loadUi(GRAPH_WIDGET, QDialog())
    else:
        performance = uic.loadUi(GRAPH_WIDGET, to)
    return performance
