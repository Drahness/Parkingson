import os
import sys
import threading

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QThreadPool, pyqtSignal, QSize, QRect, QPoint
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QSizePolicy, QApplication
from cv2.cv2 import VideoCapture

from GUI.MenuBar import MenuBar, ToolBar
from GUI.actions import StaticActions
from GUI.main_window_javi import CentralWidgetParkingson
from database.Settings import Settings, UserSettings
from database.deprecated_data_controller import Connection  # TODO change to a new more basic Connection manager.
from database.new_models import AbstractEntityModel
from database.usuari import Usuari
from database.pacient import Pacient
from database.models import PacientsListModel, ListModel, PruebasListModel
from GUI import GUI_Resources


class UI(QMainWindow):
    """ Clase que importara los ajustes de Javi. Con la main window"""
    pacientSelected = pyqtSignal(Pacient, int)
    changeStatusBar = pyqtSignal(str, int)
    hideViews = pyqtSignal(bool)
    key_press = pyqtSignal(QtGui.QKeyEvent)
    inited = False

    def __init__(self, debug=False):
        super().__init__()
        self.setObjectName("Main_window")
        self.settings = None
        # TODO SINGLETONS ?¿?¿?¿?¿
        UI.instance = self
        UI.DB = "db" + os.sep + f"default.db"
        UI.threadpool = QThreadPool()
        UI.DEBUG = debug
        # TODO SINGLETONS ?¿?¿?¿?¿ THEY ARE REALLY NEEDED?
        self.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.connection = Connection()
        self.login_form = GUI_Resources.get_login_register_dialog(self.connection)
        self.user_credentials = {"result": False}
        self.credentials()
        if self.user_credentials["result"]:
            self.show()
        else:
            sys.exit(0)
        # Recogemos el Central widget, lo añadimos y luego lo inicializamos
        if debug and self.user_credentials["username"] == '':
            self.user_credentials["username"] = "Admin"

        self.central = CentralWidgetParkingson(self.user_credentials["username"], debug=debug)
        self.setCentralWidget(self.central)
        # Creamos el objeto settings
        self.settings = UserSettings(self.user_credentials["username"])

        if self.settings.value(self.settings.SIZE):
            rect = self.settings.value(self.settings.SIZE, type=QSize)
            self.resize(rect.width(), rect.height())
        if self.settings.value(self.settings.FULLSCREEN, False, bool):
            self.showMaximized()

        pos = self.settings.value(self.settings.POSITION, QPoint(50,50), QPoint)
        self.move(pos)





        PruebasListModel.get_instance(self.user_credentials["username"])
        self.listview_model: AbstractEntityModel = PacientsListModel.get_instance(self.user_credentials["username"])
        self.central.pacients_list_view.setModel(self.listview_model)

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
        self.menu_bar.mod_prueba.triggered.connect(self.button_clicked)
        self.menu_bar.del_prueba.triggered.connect(self.button_clicked)

        self.central.pacients_list_view.clicked.connect(self.on_listview_pacient_click)
        self.central.pacients_list_view.doubleClicked.connect(self.on_pacient_double_click)
        self.central.pacients_tab.finishedSignal.connect(self.on_finished)
        self.central.pacients_tab.resultSignal.connect(self.on_result)
        self.central.cronometro_tab.finishedSignal.connect(self.on_crono_finished)
        self.changeStatusBar.connect(self.changeStatus)

        self.menu_bar.data.setEnabled(False)
        self.menu_bar.ajustes.setEnabled(False)
        self.menu_bar.ayuda.setEnabled(False)
        # self.menu_bar.pruebas.setEnabled(False)
        StaticActions.mod_prueba_action.setEnabled(False)
        self.menu_bar.edit_pacient.setEnabled(False)
        self.menu_bar.del_pacient.setEnabled(False)

        self.central.pacients_tab.set_signal_pacient_selected(self.pacientSelected)
        self.central.cronometro_tab.set_signal_pacient_selected(self.pacientSelected)
        self.central.rendimiento_tab.set_signal_pacient_selected(self.pacientSelected)

        self.central.pacients_tab.set_change_status_bar(self.changeStatusBar)
        self.central.cronometro_tab.set_change_status_bar(self.changeStatusBar)
        self.central.rendimiento_tab.set_change_status_bar(self.changeStatusBar)

        self.central.pacients_tab.set_key_pressed(self.key_press)
        self.central.cronometro_tab.set_key_pressed(self.key_press)
        self.central.rendimiento_tab.set_key_pressed(self.key_press)

        self.central.pacients_tab.set_signal_current_changed(self.central.parent_tab_widget.currentChanged)
        self.central.cronometro_tab.set_signal_current_changed(self.central.parent_tab_widget.currentChanged)
        self.central.rendimiento_tab.set_signal_current_changed(self.central.parent_tab_widget.currentChanged)

        self.hideViews.connect(self.hide_view)

        self.menu_bar.view_pacientes.setCheckable(True)
        self.menu_bar.view_toolbar.setCheckable(True)
        self.menu_bar.view_crono.setCheckable(True)
        self.menu_bar.view_rendimiento.setCheckable(True)

        self.menu_bar.view_pacientes.setChecked(True)
        self.menu_bar.view_toolbar.setChecked(True)
        self.menu_bar.view_crono.setChecked(True)
        self.menu_bar.view_rendimiento.setChecked(True)

        self.menu_bar.view_pacientes.changed.connect(self.hide_view)
        self.menu_bar.view_toolbar.changed.connect(self.hide_view)
        self.menu_bar.view_crono.changed.connect(self.hide_view)
        self.menu_bar.view_rendimiento.changed.connect(self.hide_view)

        self.central.parent_tab_widget.setEnabled(False)

        # INIT Tab Components

        self.central.pacients_tab.init()
        self.central.cronometro_tab.init()
        self.central.rendimiento_tab.init()

        # El tab de pacientes sera el por defecto.

        pacient_index = self.central.parent_tab_widget.indexOf(self.central.pacients_tab)
        self.central.parent_tab_widget.setCurrentIndex(pacient_index)
        self.iconSizeChanged.connect(self.iconSizeChanged)

        threading.Thread(target=self.check_camera_worker).start()
        self.inited = True

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
        if not self.central.parent_tab_widget.isEnabled():
            self.central.parent_tab_widget.setEnabled(True)
        p = self.listview_model.get(row)
        self.changeStatusBar.emit(f"Selecionado: {p}", 1)
        self.pacientSelected.emit(p, row)
        self.menu_bar.edit_pacient.setEnabled(True)
        self.menu_bar.del_pacient.setEnabled(True)

    def hide_view(self, *args):
        name = self.sender().objectName()
        if "action_view_toolbar" == name:
            if not self.sender().isChecked():
                self.removeToolBar(self.toolbar)
            else:
                self.addToolBar(self.toolbar)
                self.toolbar.setVisible(True)
        elif "action_view_crono" == name:
            self.central.cronometro_tab.setVisible(self.sender().isChecked())
            self.central.parent_tab_widget.currentChanged.emit(self.central.parent_tab_widget.currentIndex())
            if not self.sender().isChecked():
                self.central.parent_tab_widget.setTabVisible(2, False)
                self.central.cronometro_tab.setVisible(False)
            else:
                self.central.parent_tab_widget.setTabVisible(2, True)
                self.central.cronometro_tab.setVisible(self.central.cronometro_tab.is_on_focus())
            pass
        elif "action_view_pacientes" == name:
            self.central.pacients_tab.setVisible(self.sender().isChecked())
            self.central.parent_tab_widget.currentChanged.emit(self.central.parent_tab_widget.currentIndex())
            if not self.sender().isChecked():
                self.central.parent_tab_widget.setTabVisible(0, False)
                self.central.pacients_tab.setVisible(False)
                self.central.pacients_tab.cancel_button.clicked.emit()
            else:
                self.central.parent_tab_widget.setTabVisible(0, True)
                self.central.pacients_tab.setVisible(self.central.cronometro_tab.is_on_focus())
        elif "action_view_rendimiento" == name:
            self.central.rendimiento_tab.setVisible(self.sender().isChecked())
            self.central.parent_tab_widget.currentChanged.emit(self.central.parent_tab_widget.currentIndex())
            if not self.sender().isChecked():
                self.central.parent_tab_widget.setTabVisible(1, False)
                self.central.rendimiento_tab.setVisible(False)
            else:
                self.central.parent_tab_widget.setTabVisible(1, True)
                self.central.rendimiento_tab.setVisible(self.central.rendimiento_tab.is_on_focus())
        #  slf.update()

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
        p = self.listview_model.get(row)
        self.status_bar.showMessage(f"Editando: {p}")
        self.menu_bar.edit_pacient.triggered.emit()

    def changeStatus(self, string, microseconds):
        self.status_bar.showMessage(string, microseconds * 1000)

    def button_clicked(self, *args):
        pacient_index = self.central.parent_tab_widget.indexOf(self.central.pacients_tab)
        self.central.parent_tab_widget.setCurrentIndex(pacient_index)
        if self.sender() == StaticActions.add_pacient_action:
            self.central.pacients_tab.pacientSelected(Pacient(), -1)
            self.central.pacients_tab.set_enabled(True)
            self.central.parent_tab_widget.setEnabled(True)
        elif self.sender() == StaticActions.del_pacient_action:
            if len(self.listview_model) > 0 and self.central.pacients_tab.pacient_selected():
                pacient = self.listview_model.entities[self.central.pacients_tab.index]
                dialog = GUI_Resources.get_confirmation_dialog_ui(f"Quieres eliminar el usuario {pacient}")
                if dialog.exec_() == 1:
                    self.listview_model.delete(pacient)
        elif self.sender() == StaticActions.edit_pacient_action:
            if len(self.listview_model.entities) > 0 and self.central.pacients_tab.pacient_selected():
                self.central.pacients_tab.set_enabled(True)
        elif self.sender() == StaticActions.del_prueba_action:
            dialog = GUI_Resources.get_confirmation_dialog_ui(
                f"Quieres eliminar la prueba de rendimiento del paciente")
            if dialog.exec_() == 1:
                PruebasListModel.get_instance().delete(self.central.rendimiento_tab.selected_prueba)

    def on_crono_finished(self, prueba, row):
        PruebasListModel.get_instance(self.user_credentials["username"]).append(prueba)
        p = self.listview_model.get(row)
        self.status_bar.showMessage(f"Insertada nueva prueba a {p}")

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        super().resizeEvent(a0)
        size = a0.size()
        old_size = a0.oldSize()
        if self.inited:
            self.settings.setValue(self.settings.SIZE, a0.size())
            self.settings.setValue(self.settings.FULLSCREEN, self.isFullScreen())
        print(f"{size} {old_size}")

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        super().keyPressEvent(a0)
        self.key_press.emit(a0)

    @staticmethod
    def check_camera_worker():
        if not VideoCapture(0).read()[0]:  # Compruebo si hay camara. si no la hay haz X
            StaticActions.tomar_foto.setEnabled(False)

    def moveEvent(self, a0: QtGui.QMoveEvent) -> None:
        super().moveEvent(a0)
        if self.inited:
            self.settings.setValue(self.settings.POSITION, self.pos())


