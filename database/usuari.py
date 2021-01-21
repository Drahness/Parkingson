from sqlitedao import ColumnDict

import Utils
from database.database_connection import ModelConnection
from database.entities_interface import Entity


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

    def insert(self, conexion: ModelConnection):
        conexion.execute("INSERT INTO pacients (username,password) VALUES (?,?)", [self.username,
                                                                                  self.password])
        self.append()
        return self.username

    def update(self, conexion: ModelConnection, to_updated):
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

    def delete(self, conexion: ModelConnection):
        conexion.execute("DELETE FROM users WHERE dni = ?", [self.username])
        self.remove()

    @staticmethod
    def get_tablenames() -> tuple:
        return "users",

    @staticmethod
    def get_columns_dict() -> tuple:
        columns = ColumnDict()
        columns.add_column("username", "text", "PRIMARY KEY")
        columns.add_column("password", "text")
        return columns,

    @staticmethod
    def valid_user(conn, username, password):
        dao = conn.dao
        return len(dao.search_table(Usuari.get_tablenames()[0], {"username": username, "password": password})) > 0

class AuthConnection(ModelConnection):
    default_user = "admin"
    default_password = Utils.cypher(default_user)
    def __init__(self):
        super(AuthConnection, self).__init__("default", Usuari)
        self.init()

    def valid_user(self, username, password):
        return len(self.dao.search_table(Usuari.get_tablenames()[0], {"username": username, "password": password})) > 0

    def init(self):
        super(AuthConnection, self).init()
        self.execute(f"INSERT OR IGNORE INTO {self.model.get_tablenames()[0]} (username,password) VALUES (?,?)",
                     [self.default_user, self.default_password])