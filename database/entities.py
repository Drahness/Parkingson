from PyQt5.QtCore import QDate
from sqlitedao import ColumnDict, SqliteDao

from database.DB_Resources import get_db_connection
import datetime


class Entity:
    __loaded_instances: dict = {}

    def __init__(self, dictionary: dict = None):
        self.dictionary = dictionary
        pass

    @classmethod
    def load(cls, connection) -> list:
        items = cls._get_list_of_instances()
        dao: SqliteDao = connection.dao
        for obj in dao.search_table(cls.get_tablename(), {}):
            items.append(cls(dictionary=obj))
        Entity.__loaded_instances[cls] = items
        return items

    @staticmethod
    def is_autoincrement() -> bool:
        return False

    def insert(self, conexion) -> any:
        raise NotImplementedError()

    def update(self, conexion, to_updated):
        raise NotImplementedError()

    def delete(self, conexion):
        raise NotImplementedError()

    @staticmethod
    def get_tables_count() -> int:
        return 1

    @staticmethod
    def get_tablename():
        raise NotImplementedError()

    """ Para mantener la sincronizacion con la BBDD"""

    def append(self):
        list_of_instances: list = self._get_list_of_instances()
        list_of_instances.append(self)

    @classmethod
    def get_object(self, i):
        return self._get_list_of_instances()[i]

    @classmethod
    def _get_list_of_instances(cls) -> list:
        type_of_entity = cls
        if type_of_entity not in Entity.__loaded_instances:
            Entity.__loaded_instances[type_of_entity] = []
        return Entity.__loaded_instances[type_of_entity]

    def remove(self):
        list_of_instances = self._get_list_of_instances()
        list_of_instances.remove(self)


class Prueba(Entity):
    def __init__(self, identifier: int = None,
                 laps: list = None,
                 pacient_id: str = None,
                 datetime_of_test: datetime.datetime = None,
                 dictionary: dict = None):
        super().__init__()
        if dictionary is not None:
            self.dictionary = dictionary
            identifier = dictionary["identifier"]
            laps = dictionary["laps"]
            pacient_id = dictionary["pacient_id"]
            datetime_of_test = dictionary["datetime"]

        self.identifier = identifier  # Integer
        self.laps = laps
        self.pacient_id = pacient_id
        self.datetime = datetime_of_test

    def insert(self, conexion) -> int:
        conexion.set_auto_commit(False)
        identifier = conexion.execute("SELECT seq FROM sqlite_sequence WHERE name = ?", [self.get_tablename()])[0]
        self.identifier = identifier
        conexion.insert("INSERT INTO pruebas (pacient_id,datetime) VALUES (?,?,?)", [self.identifier,
                                                                                     self.pacient_id,
                                                                                     self.datetime])
        for i_lap in range(0, len(self.laps)):
            conexion.insert("INSERT INTO pruebas_data (identifier,tiempo,num_lap)", [self.identifier,
                                                                                     self.laps[i_lap],
                                                                                     i_lap])
        conexion.commit()
        conexion.set_auto_commit(True)
        self.append()
        return identifier

    def update(self, conexion, to_updated):
        if isinstance(to_updated, str):
            identifier: str = to_updated
        elif isinstance(to_updated, Prueba):
            identifier: str = to_updated.identifier
        else:
            raise AssertionError("argument type dont supported, type: " + str(type(to_updated)))
        laps_to_update = conexion.execute(
            f"SELECT (rowid,tiempo,num_lap) FROM {self.get_tablename()[1]} WHERE identifier = ?", identifier)
        conexion.execute(f"UPDATE {self.get_tablename()[0]} SET identifier = ?, pacient_id = ?, datetime = ? WHERE "
                         f"identifier = ?",
                         [self.identifier,
                          self.pacient_id,
                          self.datetime,
                          identifier])
        for i in range(0, len(laps_to_update)):
            conexion.execute(
                f"UPDATE {self.get_tablename()[1]} SET identifier = ?, tiempo = ?, num_lap = ? WHERE rowid =", [
                    self.identifier,
                    self.laps[i],
                    i,
                    laps_to_update[i][0]
                ])

    @staticmethod
    def is_autoincrement() -> bool:
        return True

    def delete(self, conexion):
        conexion.execute("DELETE FROM pruebas WHERE id = ?", [self.identifier])
        conexion.execute("DELETE FROM pruebas_data WHERE id = ?", [self.identifier])
        self.remove()

    @classmethod
    def load(cls, connection) -> list:
        dao = connection.dao
        items = cls._get_list_of_instances()
        dictionaries = dao.search_table(Prueba.get_tablename()[0], {})
        for dictionary in dictionaries:
            tests_list = []
            list_laps = dao.search_table(table_name=Prueba.get_tablename()[1],
                                         search_dict={"pacient_id": dictionary["pacient_id"]},
                                         order_by=["num_lap"])
            for lap in list_laps:
                tests_list.append(lap["tiempo"])
            dictionary["laps"] = tests_list
            items.append(cls(dictionary=dictionary))
        return dictionaries

    @staticmethod
    def get_tables_count() -> int:
        return 2

    @staticmethod
    def get_tablename() -> tuple or str:
        return "pruebas", "pruebas_data"

    @staticmethod
    def get_columns_dict() -> tuple or ColumnDict:
        first_table = ColumnDict()
        first_table.add_column("identifier", "Integer", "PRIMARY KEY AUTOINCREMENT")
        first_table.add_column("pacient_id", "text")
        first_table.add_column("datetime", "datetime")
        first_table.add_column("FOREIGN KEY(pacient_id)",
                               f"REFERENCES {Pacient.get_tablename()}({Pacient.ID})")

        second_table = ColumnDict()
        second_table.add_column("identifier", "Integer")  # id de la prueba
        second_table.add_column("tiempo", "Integer")  # dateti
        second_table.add_column("num_lap", "Integer")
        return first_table, second_table


class Pacient(Entity):
    ID = "dni"
    dni: str
    apellidos: str
    estadio: int
    nombre: str

    def __init__(self,
                 dni: str = None,
                 apellidos: str = None,
                 estadio: int = None,
                 nombre: str = None,
                 nacimiento: datetime.date = None,
                 notas: str = None,
                 dictionary: dict = None):
        super().__init__()
        if dictionary is not None:
            self.dictionary = dictionary
            dni = dictionary.get("dni")
            nacimiento = dictionary.get("nacimiento")
            apellidos = dictionary.get("apellidos")
            estadio = dictionary.get("estadio")
            nombre = dictionary.get("nombre")
            notas = dictionary.get("notas")
        self.dni = dni
        self.apellidos = apellidos
        self.estadio = estadio
        self.nombre = nombre
        self.nacimiento = nacimiento if not isinstance(nacimiento, str) else datetime.date.fromisoformat(nacimiento)
        self.notas = notas

    def insert(self, conexion):
        conexion.insert("INSERT INTO pacients (dni,apellidos,estadio,nombre,nacimiento,notas) VALUES (?,?,?,?,?,?)",
                        [self.dni,
                         self.apellidos,
                         self.estadio,
                         self.nombre,
                         self.nacimiento,
                         self.notas])
        self.append()
        return self.dni

    def update(self, conexion, to_updated):
        if isinstance(to_updated, str):
            dni = to_updated
        elif isinstance(to_updated, Pacient):
            dni = to_updated.dni
        else:
            raise AssertionError("argument type dont supported, type: " + str(type(to_updated)))
        conexion.execute("UPDATE pacients SET dni = ?,"
                         "                  apellidos = ?,"
                         "                  estadio = ?,"
                         "                  nombre = ? ,"
                         "                  nacimiento = ?,"
                         "                  notas = ?"
                         " WHERE dni = ?",
                         [self.dni,
                          self.apellidos,
                          self.estadio,
                          self.nombre,
                          self.nacimiento,
                          self.notas,
                          dni])

    def delete(self, conexion):
        conexion.execute(f"DELETE FROM {self.get_tablename()} WHERE dni = ?", [self.dni])
        self.remove()

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
        columns.add_column("nacimiento", "date")
        columns.add_column("notas", "text")
        return columns

    def __str__(self):
        return f"{self.dni}:{self.apellidos}, {self.nombre}"


class Usuari(Entity):
    username: str
    password: str

    def __init__(self,
                 username: str = None,
                 password: str = None,
                 dictionary: dict = None):
        super().__init__()
        if dictionary is not None:
            self.dictionary = dictionary
            username = dictionary["username"]
            password = dictionary["password"]
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.username}"

    def insert(self, conexion):
        conexion.insert("INSERT INTO pacients (username,password) VALUES (?,?)", [self.username,
                                                                                  self.password])
        self.append()
        return self.username

    def update(self, conexion, to_updated):
        if isinstance(to_updated, str):
            username: str = to_updated
        elif isinstance(to_updated, Usuari):
            username: str = to_updated.username
        else:
            raise AssertionError("argument type dont supported, type: " + str(type(to_updated)))
        conexion.execute("UPDATE usuaris SET dni = ?, apellidos = ?, estadio = ?, nombre = ? WHERE dni = ?",
                         [self.username,
                          self.password,
                          username])

    def delete(self, conexion):
        conexion.execute("DELETE FROM users WHERE dni = ?", [self.username])
        self.remove()

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
    def valid_user(username, password):
        dao = get_db_connection().dao
        return len(dao.search_table("users", {"username": username, "password": password})) > 0
