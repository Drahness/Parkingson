import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from sqlitedao import ColumnDict, SqliteDao

from database.DB_Resources import get_db_connection


class ListModel(QAbstractListModel):
    def __init__(self, items: list, base: type):
        from main_window import UI
        super(ListModel, self).__init__()
        self.instance_class = base
        base.TABLENAME = self.get_tablename()
        self.items = items or []
        if items is None:
            dao: SqliteDao = SqliteDao.get_instance(UI.DB)
            for object in dao.search_table(self.get_tablename(), {}):
                self.items.append(self.instance_class(dictionary=object))

    @staticmethod
    def get_tablename() -> tuple or str:
        raise NotImplementedError()

    @staticmethod
    def get_columns_dict() -> tuple or ColumnDict:
        raise NotImplementedError()

    def create_instance(self, data: dict) -> any:
        raise NotImplementedError()

    """Retornara el objeto sin mas"""

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        if role == Qt.DisplayRole:
            item = self.items[index.row()]
            return str(item)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.items)

    def append(self, pacient):
        if not isinstance(pacient, self.instance_class):
            raise TypeError(f"Method append expected {self.instance_class}, got {type(pacient)}")
        self.items.append(pacient)
        self.layoutChanged.emit()
        pacient.insert(get_db_connection())


class UsuariListModel(ListModel):
    """ No se si la voy a usar"""
    INSTANCE = None

    def __init__(self, items: list = None):
        from database.entities import Usuari
        super(UsuariListModel, self).__init__(items, Usuari)

    @staticmethod
    def get_tablename() -> tuple or str:
        return "users"

    @staticmethod
    def get_columns_dict() -> tuple or ColumnDict:
        columns = ColumnDict()
        columns.add_column("username", "text", "PRIMARY KEY")
        columns.add_column("password", "text")
        return columns

    @staticmethod
    def valid_user(username: str, password: str):
        from main_window import UI
        dao: SqliteDao = SqliteDao.get_instance(UI.DB)
        return len(dao.search_table("users", {"username": username, "password": password})) > 0

    @staticmethod
    def get_instance(items=None):
        if UsuariListModel.INSTANCE is None:
            UsuariListModel.INSTANCE = UsuariListModel(items)
        return UsuariListModel.INSTANCE


class PacientsListModel(ListModel):
    ID = "dni"
    INSTANCE = None

    def __init__(self, items: list = None):
        from database.entities import Pacient
        super(PacientsListModel, self).__init__(items, Pacient)
        pass

    @staticmethod
    def get_tablename() -> tuple or str:
        return "pacients"

    @staticmethod
    def get_columns_dict() -> tuple or ColumnDict:
        columns = ColumnDict()
        columns.add_column("dni", "text", "PRIMARY KEY")
        columns.add_column("nombre", "text")
        columns.add_column("apellidos", "text")
        columns.add_column("estadio", "integer")
        return columns

    @staticmethod
    def get_instance(items=None):
        if PacientsListModel.INSTANCE is None:
            PacientsListModel.INSTANCE = PacientsListModel(items)
        return PacientsListModel.INSTANCE

class PruebasListModel(ListModel):
    INSTANCE = None
    def __init__(self, items: list = None):
        from database.entities import Prueba
        if items is None:
            items = []
            from main_window import UI
            dao: SqliteDao = SqliteDao.get_instance(UI.DB)
            dictionaries = dao.search_table(self.get_tablename()[0], {})
            for dictionary in dictionaries:
                final_list = []
                list_laps = dao.search_table(table_name=self.get_tablename()[1],
                                             search_dict={"pacient_id": dictionary["pacient_id"]},
                                             order_by=["num_lap"])
                for lap in list_laps:
                    final_list.append(lap["tiempo"])
                dictionary["laps"] = final_list
        super(PruebasListModel, self).__init__(items, Prueba)

    @staticmethod
    def get_tablename() -> tuple or str:
        return "pruebas", "pruebas_data"

    @staticmethod
    def get_columns_dict() -> tuple or ColumnDict:
        first_table = ColumnDict()
        first_table.add_column("id", "Integer", "PRIMARY KEY AUTOINCREMENT")
        first_table.add_column("pacient_id", "text")
        first_table.add_column("FOREIGN KEY(pacient)",
                               f"REFERENCES {PacientsListModel.get_tablename()}({PacientsListModel.ID})")

        second_table = ColumnDict()
        second_table.add_column("id", "Integer")
        second_table.add_column("tiempo", "Integer")
        second_table.add_column("num_lap", "Integer")
        return first_table, second_table

    @staticmethod
    def get_instance(items=None):
        if PruebasListModel.INSTANCE is None:
            PruebasListModel.INSTANCE = PruebasListModel(items)
        return PruebasListModel.INSTANCE
