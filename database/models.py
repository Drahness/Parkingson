import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from sqlitedao import ColumnDict, SqliteDao, TableItem


class Model(QAbstractListModel):
    def __init__(self, items: list, base: type):
        from main_window import UI
        super(Model, self).__init__()
        self.instance_class = base
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

    def append(self, pacient: any):
        if not isinstance(pacient, self.instance_class):
            raise TypeError(f"Method append expected {self.instance_class}, got {type(pacient)}")
        self.items.append(pacient)
        self.layoutChanged.emit()


class Usuari(TableItem):
    username: str
    password: str

    def __init__(self,
                 username: str = None,
                 password: str = None,
                 dictionary: dict = None):
        super().__init__()
        if dictionary is not None:
            username = dictionary["username"]
            password = dictionary["password"]
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.username}"


class UsuariModel(Model):
    """ No se si la voy a usar"""

    def __init__(self, items: list = None):
        super(UsuariModel, self).__init__(items, Usuari)

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


class Pacients:
    model: type
    dni: str
    apellidos: str
    estadio: int
    nombre: str

    def __init__(self,
                 dni: str = None,
                 apellidos: str = None,
                 estadio: int = None,
                 nombre: str = None,
                 dictionary: dict = None):
        if dictionary is not None:
            dni = dictionary["dni"]
            apellidos = dictionary["apellidos"]
            estadio = dictionary["estadio"]
            nombre = dictionary["nombre"]
        self.model = PacientsModel
        self.dni = dni
        self.apellidos = apellidos
        self.estadio = estadio
        self.nombre = nombre

    def __str__(self):
        return f"{self.dni}:{self.apellidos}, {self.nombre}"


class PacientsModel(Model):
    ID = "dni"

    def __init__(self, items: list = None):
        super(PacientsModel, self).__init__(items, Pacients)
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


class Prueba:
    def __init__(self,
                 identifier: int = None,
                 laps: list = None,
                 pacient_id: str = None,
                 dictionary: dict = None):
        if dictionary is not None:
            identifier = dictionary["identifier"]
            laps = dictionary["laps"]
            pacient_id = dictionary["pacient_id"]
        self.identifier = identifier
        self.laps = laps
        self.pacient_id = pacient_id


class PruebasModel(Model):
    def __init__(self, items: list = None):
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
        super(PruebasModel, self).__init__(items, Prueba)

    @staticmethod
    def get_tablename() -> tuple or str:
        return "pruebas", "pruebas_data"

    @staticmethod
    def get_columns_dict() -> tuple or ColumnDict:
        first_table = ColumnDict()
        first_table.add_column("id", "Integer", "PRIMARY KEY AUTOINCREMENT")
        first_table.add_column("pacient_id", "text")
        first_table.add_column("FOREIGN KEY(pacient)",
                               f"REFERENCES {PacientsModel.get_tablename()}({PacientsModel.ID})")

        second_table = ColumnDict()
        second_table.add_column("id", "Integer")
        second_table.add_column("tiempo", "Integer")
        second_table.add_column("num_lap", "Integer")
        return first_table, second_table
