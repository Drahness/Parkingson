import os
import sys

from PyQt5 import QtGui
from PyQt5.QtCore import QThreadPool, pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QSizePolicy

from GUI.MenuBar import MenuBar, ToolBar
from database.database_controller import Connection
from database.entities import Usuari, Pacient
from database.models import PacientsListModel, ListModel, PruebasListModel
from GUI import GUI_Resources


class UI(QMainWindow):
    """ Clase que importara los ajustes de Javi. Con la main window"""
    pacientSelected = pyqtSignal(Pacient, int)
    changeStatusBar = pyqtSignal(str, int)

    def __init__(self, debug=False):
        super().__init__()
        self.setObjectName("Main_window")
        # TODO SINGLETONS ?¿?¿?¿?¿
        UI.instance = self
        UI.DB = "db" + os.sep + f"default.db"
        UI.threadpool = QThreadPool()
        UI.DEBUG = debug
        # TODO SINGLETONS ?¿?¿?¿?¿ THEY ARE REALLY NEEDED?
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.login_form = GUI_Resources.get_login_register_dialog()
        self.user_credentials = {"result": False}
        self.connection = Connection()

        # Recogemos el Central widget, lo añadimos y luego lo inicializamos
        self.central = GUI_Resources.get_main_widgetDEPRECATED()
        self.setCentralWidget(self.central)

        self.menu_bar = MenuBar()
        self.status_bar = QStatusBar()
        self.toolbar = ToolBar()
        self.addToolBar(self.toolbar)
        self.setStatusBar(self.status_bar)
        self.setMenuBar(self.menu_bar)

        self.menu_bar.add_pacient.triggered.connect(self.button_clicked)
        self.menu_bar.edit_pacient.triggered.connect(self.button_clicked)
        self.menu_bar.del_pacient.triggered.connect(self.button_clicked)
        self.central.pacients_list_view.clicked.connect(self.on_listview_pacient_click)
        self.central.pacients_list_view.doubleClicked.connect(self.on_pacient_double_click)
        self.central.pacients_tab.finishedSignal.connect(self.on_finished)
        self.central.pacients_tab.resultSignal.connect(self.on_result)
        self.central.cronometro_tab.finishedSignal.connect(self.on_crono_finished)
        self.changeStatusBar.connect(self.changeStatus)

        self.menu_bar.data.setEnabled(False)
        self.menu_bar.ajustes.setEnabled(False)
        self.menu_bar.ayuda.setEnabled(False)
        self.menu_bar.pruebas.setEnabled(False)

        self.menu_bar.edit_pacient.setEnabled(False)
        self.menu_bar.del_pacient.setEnabled(False)

        self.central.pacients_tab.set_signal_pacient_selected(self.pacientSelected)
        self.central.cronometro_tab.set_signal_pacient_selected(self.pacientSelected)
        self.central.rendimiento_tab.set_signal_pacient_selected(self.pacientSelected)

        self.central.pacients_tab.set_change_status_bar(self.changeStatusBar)
        self.central.cronometro_tab.set_change_status_bar(self.changeStatusBar)
        self.central.rendimiento_tab.set_change_status_bar(self.changeStatusBar)

        self.central.pacients_tab.set_signal_current_changed(self.central.parent_tab_widget.currentChanged)
        self.central.cronometro_tab.set_signal_current_changed(self.central.parent_tab_widget.currentChanged)
        self.central.rendimiento_tab.set_signal_current_changed(self.central.parent_tab_widget.currentChanged)


        # INIT Tab Components
        self.central.pacients_tab.init()
        self.central.cronometro_tab.init()
        self.central.rendimiento_tab.init()
        # El tab de pacientes sera el por defecto.

        pacient_index = self.central.parent_tab_widget.indexOf(self.central.pacients_tab)
        self.central.parent_tab_widget.setCurrentIndex(pacient_index)
        self.iconSizeChanged.connect(self.iconSizeChanged)
        ##self.setFixedHeight(800)
        # self.setFixedWidth(1180)
        self.credentials()
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
        self.changeStatusBar.emit(f"Selecionado: {p}", 1)
        self.pacientSelected.emit(p, row)
        self.menu_bar.edit_pacient.setEnabled(True)
        self.menu_bar.del_pacient.setEnabled(True)

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
        row = args[0].row()
        p = self.listview_model.instance_class.get_object(row)
        self.status_bar.showMessage(f"Editando: {p}")
        self.menu_bar.edit_pacient.triggered.emit()

    def changeStatus(self, str, seconds):
        self.status_bar.showMessage(str, seconds * 1000)

    def button_clicked(self, *args):
        sender_name = self.sender().objectName()
        pacient_index = self.central.parent_tab_widget.indexOf(self.central.pacients_tab)
        self.central.parent_tab_widget.setCurrentIndex(pacient_index)
        if sender_name == "add_pacient_action":
            self.central.pacients_tab.pacientSelected(Pacient(), -1)
            self.central.pacients_tab.set_enabled(True)
        elif sender_name == "del_pacient_action":
            if self.central.pacients_tab.pacient_selected():
                pacient = self.listview_model.items[self.central.pacients_tab.index]
                dialog = GUI_Resources.get_confirmation_dialog_ui(f"Quieres eliminar el usuario {pacient}")
                if dialog.exec_() == 1:
                    self.listview_model.delete(pacient)
        elif sender_name == "edit_pacient_action":
            if self.central.pacients_tab.pacient_selected():
                self.central.pacients_tab.set_enabled(True)

    def on_crono_finished(self, prueba, row):
        PruebasListModel.get_instance().append(prueba)
        p = self.listview_model.instance_class.get_object(row)
        self.status_bar.showMessage(f"Insertada nueva prueba a {p}")

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        size = a0.size()
        old_size = a0.oldSize()
        print(f"{size} {old_size}")
