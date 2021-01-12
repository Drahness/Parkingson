from PyQt5.QtCore import QDate
from sqlitedao import ColumnDict, SqliteDao

# from Utils import get_timedeltas, get_timedelta
from Utils import get_timedeltas
from database.DB_Resources import get_db_connection
import datetime
from dateutil.parser import parse


class Entity:
    __loaded_instances: dict = {}

    def __init__(self, id: any, dictionary: dict = None):
        self.dictionary = dictionary
        self.id = id
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

    def get_id(self):
        return self.id


class Prueba(Entity):
    def __gt__(self, other):
        if isinstance(other, Prueba):
            return self.datetime > other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime > other

    def __lt__(self, other):
        if isinstance(other, Prueba):
            return self.datetime < other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime < other

    def __eq__(self, other):
        if isinstance(other, Prueba):
            return self.datetime == other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime == other

    def __init__(self, identifier: int = None,
                 laps: list = None,
                 pacient_id: str = None,
                 datetime_of_test: datetime.datetime = None,
                 dictionary: dict = None):
        if dictionary is not None:
            self.dictionary = dictionary
            identifier = dictionary["identifier"]
            laps = dictionary["laps"]
            pacient_id = dictionary["pacient_id"]
            datetime_of_test = dictionary["datetime"]
        super().__init__(pacient_id)
        self.identifier = identifier or None  # Integer
        if laps is not None:
            if len(laps) > 0 and isinstance(laps[0], float):
                self.laps = get_timedeltas(laps)
            else:
                self.laps = laps
        else:
            self.laps = laps
        self.pacient_id = pacient_id
        if isinstance(datetime_of_test, str):
            self.datetime = datetime.datetime.strptime(datetime_of_test, '%Y-%m-%d %H:%M:%S.%f')
        else:
            self.datetime = datetime_of_test

    def insert(self, conexion) -> int:
        conexion.set_auto_commit(False)
        result = conexion.execute("SELECT seq FROM sqlite_sequence WHERE name = ?", [self.get_tablename()[0]])

        if len(result) == 0:
            result = 0
        else:
            result = result[0][0] + 1
        self.identifier = result
        conexion.insert("INSERT INTO pruebas (identifier,pacient_id,datetime) VALUES (?,?,?)", [self.identifier,
                                                                                                self.pacient_id,
                                                                                                str(self.datetime)])
        for i_lap in range(0, len(self.laps)):
            curr_lap = self.laps[i_lap]
            conexion.insert("INSERT INTO pruebas_data (identifier,tiempo,num_lap) VALUES (?,?,?)", [self.identifier,
                                                                                                    curr_lap.seconds + curr_lap.microseconds / (
                                                                                                            10 ** 6),
                                                                                                    i_lap])
        conexion.commit()
        conexion.set_auto_commit(True)
        self.append()
        return result

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

    @property
    def laps(self):
        return self._laps

    @laps.setter
    def laps(self, value: list):
        if isinstance(value, list):
            if len(value) == 3:
                if isinstance(value[0], float):
                    self._laps = get_timedeltas(value)
                elif isinstance(value[0], datetime.timedelta):
                    self._laps = value
            else:
                self._laps = value
        else:
            return

    def delete(self, conexion):
        conexion.set_auto_commit(False)
        conexion.execute("DELETE FROM pruebas WHERE identifier = ?", [self.identifier])
        conexion.execute("DELETE FROM pruebas_data WHERE identifier = ?", [self.identifier])
        conexion.commit()
        conexion.set_auto_commit(True)
        self.remove()

    @classmethod
    def load(cls, connection) -> list:
        dao = connection.dao
        items = cls._get_list_of_instances()
        dictionaries = dao.search_table(Prueba.get_tablename()[0], {}, order_by=["datetime"])  # Este order by sobra
        # Implementar __repr__ deberia ser lo normal.
        for dictionary in dictionaries:
            tests_list = []
            list_laps = dao.search_table(table_name=Prueba.get_tablename()[1],
                                         search_dict={"identifier": dictionary["identifier"]},
                                         order_by=["num_lap"])
            for lap in list_laps:
                tests_list.append(lap["tiempo"])
            dictionary["laps"] = tests_list
            items.append(cls(dictionary=dictionary))
        return items

    @staticmethod
    def get_tables_count() -> int:
        return 2

    @staticmethod
    def get_tablename() -> tuple or str:
        return "pruebas", "pruebas_data"

    @staticmethod
    def get_columns_dict() -> tuple or ColumnDict:
        first_table = ColumnDict()
        first_table.add_column("identifier", "INTEGER", "PRIMARY KEY AUTOINCREMENT")
        first_table.add_column("pacient_id", "TEXT")
        first_table.add_column("datetime", "datetime")
        first_table.add_column("FOREIGN KEY(pacient_id)",
                               f"REFERENCES {Pacient.get_tablename()}({Pacient.ID})")

        second_table = ColumnDict()
        second_table.add_column("identifier", "INTEGER")  # id de la prueba
        second_table.add_column("tiempo", "REAL")  # Real en segundos.microsegundos
        second_table.add_column("num_lap", "INTEGER")
        return first_table, second_table

    def __str__(self, *args, **kwargs):
        string = ""
        for x in range(0, len(self.laps)):
            string += f'{x}: {self.laps[x]} | '
        return string


class Pacient(Entity):
    ID = "dni"
    dni: str
    apellidos: str
    estadio: int
    nombre: str

    def __gt__(self, other):
        if isinstance(other, Pacient):
            return self.dni > other.dni
        if isinstance(other, str):
            return self.dni > other

    def __lt__(self, other):
        if isinstance(other, Pacient):
            return self.dni < other.dni
        if isinstance(other, str):
            return self.dni < other

    def __eq__(self, other):
        if isinstance(other, Pacient):
            return self.dni == other.dni
        if isinstance(other, str):
            return self.dni == other

    def __init__(self,
                 dni: str = None,
                 apellidos: str = None,
                 estadio: int = None,
                 nombre: str = None,
                 nacimiento: datetime.date = None,
                 notas: str = None,
                 telefono: int = None,
                 mail: str = None,
                 fotocara: bytes = None,
                 fotocuerpo: bytes = None,
                 direccion: str = None,
                 peso: float = None,
                 genero: str = None,
                 fecha_diagnostico: datetime.date = None,
                 imc: float = None,
                 dictionary: dict = None):
        if dictionary is not None:
            self.dictionary = dictionary
            dni = dictionary.get("dni")
            nacimiento = dictionary.get("nacimiento")
            apellidos = dictionary.get("apellidos")
            estadio = dictionary.get("estadio")
            nombre = dictionary.get("nombre")
            notas = dictionary.get("notas")
            telefono = dictionary.get("telefono")
            mail = dictionary.get("mail")
            fotocara = dictionary.get("fotocara")
            fotocuerpo = dictionary.get("fotocuerpo")
            direccion = dictionary.get("direccion")
            peso = dictionary.get("peso")
            genero = dictionary.get("genero")
            fecha_diagnostico = dictionary.get("fecha_diagnostico")
            imc = dictionary.get("imc")
        super().__init__(dni)
        self.dni = dni
        self.apellidos = apellidos
        self.estadio = estadio
        self.nombre = nombre
        self.nacimiento = nacimiento if not isinstance(nacimiento, str) else parse(nacimiento)
        self.notas = notas
        self.telefono = telefono
        self.mail = mail
        self.fotocara = fotocara
        self.fotocuerpo = fotocuerpo
        self.direccion = direccion
        self.peso = peso
        self.genero = genero
        self.fecha_diagnostico = fecha_diagnostico
        self.imc = imc

    def insert(self, conexion):
        attributes = [self.dni,
                      self.apellidos,
                      self.estadio,
                      self.nombre,
                      self.nacimiento,
                      self.notas,
                      self.telefono,
                      self.mail,
                      self.fotocara,
                      self.fotocuerpo,
                      self.direccion,
                      self.peso,
                      self.genero,
                      self.fecha_diagnostico,
                      self.imc]
        sql = "INSERT INTO pacients (dni,apellidos,estadio,nombre,nacimiento,notas,telefono,mail,fotocara,fotocuerpo,direccion,peso,genero,fecha_diagnostico,imc) VALUES "
        sql = (sql + "(" + ("?," * len(attributes)))[:-1] + ")"
        conexion.insert(sql, attributes)
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
                         "                  notas = ?" +
                         "                  telefono = ?" +
                         "                  mail = ? " +
                         "                  fotocara = ? " +
                         "                  fotocuerpo = ? " +
                         "                  direccion = ? " +
                         "                  peso = ? " +
                         "                  genero = ? " +
                         "                  fecha_diagnostico = ? " +
                         "                  imc = ? "
                         " WHERE dni = ?",
                         [self.dni,
                          self.apellidos,
                          self.estadio,
                          self.nombre,
                          self.nacimiento,
                          self.notas,
                          self.telefono,
                          self.mail,
                          self.fotocara,
                          self.fotocuerpo,
                          self.direccion,
                          self.peso,
                          self.genero,
                          self.fecha_diagnostico,
                          self.imc,
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
        columns.add_column("telefono", "integer")
        columns.add_column("mail", "text")
        columns.add_column("fotocara", "blob")
        columns.add_column("fotocuerpo", "blob")
        columns.add_column("direccion", "text")
        columns.add_column("peso", "integer")
        columns.add_column("genero", "text")
        columns.add_column("fecha_diagnostico", "date")
        columns.add_column("imc", "float")
        return columns

    def __str__(self):
        return f"{self.dni}:{self.apellidos}, {self.nombre}"

    @property
    def nacimiento(self):
        return self._nacimiento

    @nacimiento.setter
    def nacimiento(self, value):
        if isinstance(value, QDate):
            self._nacimiento = value.toPyDate()
        else:
            self._nacimiento = value


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
        super().__init__(username)
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
