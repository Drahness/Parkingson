import sys

from PyQt5.QtWidgets import QMenuBar, QApplication, QAction, QMenu,  QToolBar

from GUI.actions import StaticActions


def _rep(string: str) -> str:
    return string.replace("&", "").replace(" ", "_").lower()

class ToolBar(QToolBar):
    def __init__(self):
        super().__init__()
        self.add_pacient = self.addAction(StaticActions.add_pacient_action)
        self.edit_pacient = self.addAction(StaticActions.edit_pacient_action)
        self.del_pacient = self.addAction(StaticActions.del_pacient_action)
        """
        # DATA
        self.recargar = self.data.addAction(StaticActions.recargar_action)
        self.consultar_tablas = self.data.addAction(StaticActions.consultar_tablas_action)
        self.data.addSeparator()
        self.exportar_JSON = self.data.addAction(StaticActions.exportar_JSON_action)
        self.exportar_XML = self.data.addAction(StaticActions.exportar_XML_action)
        # PRUEBA
        self.mod_prueba = self.pruebas.addAction(StaticActions.mod_prueba_action)
        self.del_prueba = self.pruebas.addAction(StaticActions.del_prueba_action)
        # AYUDA
        self.creditos = self.ayuda.addAction(StaticActions.creditos_action)
        """

    def addAction(self, action: 'QAction') -> None:
        super().addAction(action)
        action.setParent(self)


class MenuBar(QMenuBar):
    _pacients = "&Pacient"
    _data = "&Datos"
    _test = "&Pruebas"
    _settings = "&Ajustes"
    _help = "&Ayuda"

    @property
    def pacients_str(self):
        return _rep(MenuBar._pacients)

    @property
    def data_str(self):
        return _rep(MenuBar._data)

    @property
    def test_str(self):
        return _rep(MenuBar._test)

    @property
    def settings_str(self):
        return _rep(MenuBar._settings)

    @property
    def help_str(self):
        return _rep(MenuBar._help)

    def __init__(self) -> None:
        super().__init__()
        # INIT MENUS
        self.pacients = Menu(MenuBar._pacients)
        self.data = Menu(MenuBar._data)
        self.pruebas = Menu(MenuBar._test)
        self.ajustes = Menu(MenuBar._settings)
        self.ayuda = Menu(MenuBar._help)
        # PACIENTES
        self.add_pacient = self.pacients.addAction(StaticActions.add_pacient_action)
        self.edit_pacient = self.pacients.addAction(StaticActions.edit_pacient_action)
        self.del_pacient = self.pacients.addAction(StaticActions.del_pacient_action)
        # DATA
        self.recargar = self.data.addAction(StaticActions.recargar_action)
        self.consultar_tablas = self.data.addAction(StaticActions.consultar_tablas_action)
        self.data.addSeparator()
        self.exportar_JSON = self.data.addAction(StaticActions.exportar_JSON_action)
        self.exportar_XML = self.data.addAction(StaticActions.exportar_XML_action)
        # PRUEBA
        self.mod_prueba = self.pruebas.addAction(StaticActions.mod_prueba_action)
        self.del_prueba = self.pruebas.addAction(StaticActions.del_prueba_action)
        # AYUDA
        self.creditos = self.ayuda.addAction(StaticActions.creditos_action)
        # AÑADIR MENUS
        self.addMenu(self.pacients)
        self.addMenu(self.data)
        self.addMenu(self.pruebas)
        self.addMenu(self.ajustes)
        self.addMenu(self.ayuda)


class Menu(QMenu):

    def __init__(self, title: str = ""):
        super().__init__(title)

    def addAction(self, action: QAction or str) -> QAction:
        if isinstance(action, str):
            action = QAction(action)
        super(Menu, self).addAction(action)
        action.setParent(self)
        return action


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MenuBar()
    window.show()
    m = Menu()
    app.exec_()
