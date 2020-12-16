import os
import sys

from PyQt5.QtCore import QThreadPool, QModelIndex, pyqtSignal
from PyQt5.QtGui import QResizeEvent
from PyQt5.QtWidgets import QMainWindow, QDialog, QVBoxLayout

from GUI import GUI_Resources
from GUI.GUI_Resources import get_error_dialog_msg, get_confirmation_dialog_ui
from GUI.Utils import SimpleForm
from database.database_controller import Connection
from database.entities import Usuari, Pacient
from database.models import PacientsListModel, ListModel, PruebasListModel


class UI(QMainWindow):
    """ Clase que importara los ajustes de Javi. Con la main window"""
    pacientSelected = pyqtSignal(Pacient, int)

    def __init__(self, debug=False):
        super().__init__()
        # TODO SINGLETONS ?¿?¿?¿?¿
        UI.instance = self
        UI.DB = "db" + os.sep + f"default.db"
        UI.threadpool = QThreadPool()
        UI.DEBUG = debug
        self.setObjectName("Main_window")
        # TODO SINGLETONS ?¿?¿?¿?¿ THEY ARE REALLY NEEDED?

        self.validUser = False
        self.login_form = GUI_Resources.get_login_register_dialog()
        self.user_credentials = {"result": False}
        self.connection = Connection()
        self.credentials()
        self.central = GUI_Resources.get_main_widget()
        self.central.actions_buttons[self.central.ADD_button_key].clicked.connect(self.button_clicked)
        self.central.actions_buttons[self.central.DELETE_button_key].clicked.connect(self.button_clicked)
        self.central.actions_buttons[self.central.EDIT_button_key].clicked.connect(self.button_clicked)

        self.central.pacients_list_view.clicked.connect(self.on_listview_pacient_click)
        self.central.pacients_list_view.doubleClicked.connect(self.on_pacient_double_click)

        self.central.pacients_tab.finishedSignal.connect(self.on_finished)
        self.central.pacients_tab.resultSignal.connect(self.on_result)

        self.central.cronometro_tab.finishedSignal.connect(self.on_crono_finished)

        self.central.pacients_tab.init()
        self.central.cronometro_tab.init()
        self.central.rendimiento_tab.init()

        pacient_index = self.central.parent_tab_widget.indexOf(self.central.pacients_tab)
        self.central.parent_tab_widget.setCurrentIndex(pacient_index)

        self.setFixedSize(1020, 600)
        # self.iconSizeChanged.connect(self.iconSizeChanged)
        if self.user_credentials["result"]:
            self.setCentralWidget(self.central)
            self.show()
            self.listview_model: ListModel = PacientsListModel.get_instance()
            self.central.pacients_list_view.setModel(self.listview_model)
        else:
            sys.exit(0)

    def credentials(self):
        """ Funcion que pide las credenciales. Si le dan a cancelar, sale del programa. Si son incorrectas
        reintenta la conexion indefinidamente"""
        self.login_form.show()
        if not self.DEBUG:
            self.login_form.login_validator = Usuari.valid_user
        result = self.login_form.exec_()
        if result == 1 and self.login_form.result.get("result", False):
            self.user_credentials = self.login_form.result
        else:
            sys.exit(0)

    def on_listview_pacient_click(self, *args):
        """Slot for clicks in the listview, listens to the builtin Signal of clicked"""
        row = args[0].row()
        p = self.listview_model.instance_class.get_object(row)
        self.pacientSelected.emit(p, row)
        # self.central.pacients_tab.set_pacient(p, row)

    @staticmethod
    def get_instance():
        return UI.instance

    def on_finished(self, enable):
        """Finished slot"""
        self.central.actions_buttons[self.central.ADD_button_key].setEnabled(enable)
        self.central.actions_buttons[self.central.DELETE_button_key].setEnabled(enable)
        self.central.actions_buttons[self.central.EDIT_button_key].setEnabled(enable)
        self.central.pacients_list_view.setEnabled(enable)

    """Slots"""

    def on_result(self, acepted: bool, row: int):
        if acepted:  # si es true, significa que han acabado de editar
            if row == -1:  # estan creando un usuario
                self.listview_model.append(self.central.pacients_tab.pacient)
                self.central.pacients_list_view.setCurrentIndex(self.listview_model.index(len(self.listview_model), 0))
                # QModelIndex no se lo que es pero para llamarlo lo necesito
            else:  # estan editando un usuario, el PyQt da un numero aleatorio a row cuando es None
                self.listview_model.update(self.central.pacients_tab.pacient, self.central.pacients_tab.last_pacient)
                self.central.pacients_list_view.setCurrentIndex(self.listview_model.index(row, 0))

    def on_pacient_double_click(self, *args):
        print("double click")


    def button_clicked(self,*args):
        sender_name = self.sender().objectName()
        pacient_index =  self.central.parent_tab_widget.indexOf(self.central.pacients_tab)
        self.central.parent_tab_widget.setCurrentIndex(pacient_index)
        if sender_name == "add_button":
            self.central.pacients_tab.pacientSelected(Pacient(), -1)
            self.central.pacients_tab.set_enabled(True)
        elif sender_name == "delete_button":
            if self.central.pacients_tab.pacient_selected():
                pacient = self.listview_model.items[self.central.pacients_tab.index]
                dialog = get_confirmation_dialog_ui(f"Quieres eliminar el usuario {pacient}")
                if dialog.exec_() == 1:
                    self.listview_model.delete(pacient)
        elif sender_name == "edit_button":
            if self.central.pacients_tab.pacient_selected():
                self.central.pacients_tab.set_enabled(True)

    def on_crono_finished(self, prueba, row):
        PruebasListModel.get_instance().append(prueba)
