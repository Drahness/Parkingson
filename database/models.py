import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from sqlitedao import ColumnDict, SqliteDao


class Model(QAbstractListModel):
    def __init__(self, items: list, base: type):
        super(Model, self).__init__()
        self.items = items or []
        self.instance_class = base

    @staticmethod
    def get_table_structure(self):
        raise NotImplementedError()

    @staticmethod
    def get_tablename():
        raise NotImplementedError()

    """Retornara el objeto sin mas"""

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            item = self.items[index.row()]
            return item

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.items)

    def append(self, pacient: any):
        if not isinstance(pacient, self.instance_class):
            raise TypeError(f"append expected {self.instance_class}, got {type(pacient)}")
        self.items.append(pacient)
        self.layoutChanged.emit()


class UsuariModel(Model):
    """ No se si la voy a usar"""

    def __init__(self, items: list = None):
        super(UsuariModel, self).__init__(items, None)

    @staticmethod
    def get_tablename():
        return "users"

    @staticmethod
    def get_columns_dict() -> ColumnDict:
        columns = ColumnDict()
        columns.add_column("username", "text", "PRIMARY KEY")
        columns.add_column("password", "text")
        return columns

    @staticmethod
    def valid_user(username: str, password: str):
        from main_window import UI
        dao: SqliteDao = SqliteDao.get_instance(UI.DB)
        return len(dao.search_table("users", {"username":username, "password":password})) > 0



class Pacients:
    model: type
    dni: str
    apellido: str
    apellido2: str
    estadio: int
    nombre: str

    def __init__(self,
                 dni: str = None,
                 apellido: str = None,
                 apellido2: str = None,
                 estadio: int = None,
                 nombre: str = None):
        self.model = PacientsModel
        self.dni = dni
        self.apellido1 = apellido
        self.apellido2 = apellido2
        self.estadio = estadio
        self.nombre = nombre

    def __str__(self):
        return f"{self.dni}:{self.apellido1}, {self.nombre}"


class PacientsModel(Model):
    def __init__(self, items: list = None):
        super(PacientsModel, self).__init__(items, Pacients)
        pass

    @staticmethod
    def get_tablename():
        return "pacients"

    @staticmethod
    def get_columns_dict() -> ColumnDict:
        columns = ColumnDict()
        columns.add_column("dni", "text", "PRIMARY KEY")
        columns.add_column("name", "text")
        columns.add_column("apellido1", "text", )
        columns.add_column("apellido2", "text", )
        columns.add_column("estadio", "integer")
        return columns
