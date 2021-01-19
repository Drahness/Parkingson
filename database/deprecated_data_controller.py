import sqlite3
import os

from sqlitedao import SqliteDao, ColumnDict
from typing import Type

import Utils
from collections import Iterable

from .entities_interface import Entity
from .prueba import Prueba
from .usuari import Usuari
from .pacient import Pacient


# https://charlesleifer.com/blog/encrypted-sqlite-databases-with-python-and-sqlcipher/

class Connection:
    INSTANCE_MAP = {}

    def __init__(self, user="Admin", path: str = "db", dbname=f"default.db"):
        filepath = path + os.sep + dbname
        self.path = path
        self.dbname = dbname
        if not os.path.exists(filepath):
            os.makedirs(path, exist_ok=True)
        self.conn = sqlite3.connect(filepath)
        self.dao = SqliteDao.get_instance(filepath)
        self.user = user
        self.autocommit = True
        self.cursor = self.conn.cursor()

        if self.first_init():
            if not self.check_existence(Pacient):
                self.create_table(Pacient.get_tablenames()[0], Pacient.get_columns_dict()[0])
            if not self.check_existence(Usuari):
                self.create_table(Usuari.get_tablenames()[0], Usuari.get_columns_dict()[0])
            if not self.check_existence(Prueba.get_tablenames()[0]):
                self.create_table(Prueba.get_tablenames()[0], Prueba.get_columns_dict()[0])
            if not self.check_existence(Prueba.get_tablenames()[1]):
                self.create_table(Prueba.get_tablenames()[1], Prueba.get_columns_dict()[1])
            self.execute(f"INSERT OR IGNORE INTO {Usuari.get_tablenames()} VALUES ('Admin','{Utils.cypher('Admin')}')")
            self.execute(f"UPDATE first_init SET boolean_init = 1")

    def first_init(self):
        try:
            return self.execute(f"SELECT * FROM first_init")[0] == 0
        except:
            columns = ColumnDict()
            columns.add_column("boolean_init", "INTEGER")
            self.create_table("first_init", columns)
            self.execute(f"INSERT OR IGNORE INTO first_init VALUES (0)")
            return True

    def execute(self, sql, parameters: Iterable = None) -> list:
        print(f"DB:{self.path}/{self.dbname} - Operation: {sql}, {parameters}")
        if parameters is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, parameters)
        if self.autocommit:
            self.conn.commit()
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()

    def set_auto_commit(self, boolean: bool) -> None:
        self.autocommit = boolean

    def insert(self, sql, parameters: Iterable = None) -> None:
        if parameters is None:
            self.execute(sql)
        else:
            self.execute(sql, parameters)

    def create_table(self, tablename: str, columns: ColumnDict, indexes=None):
        self.dao.create_table(tablename, columns, indexes)

    def check_existence(self, model: Type[Entity] or str) -> bool:
        if isinstance(model, str):
            table = model
        elif issubclass(model, Entity):
            table = model.get_tablenames()
        else:
            raise AssertionError(f"Bad arguments. expected {str} or {type(Entity)} got {type(model)}")
        self.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table}'")
        existence = self.cursor.fetchall()
        return existence.count(table) == 1

    @staticmethod
    def get_instance(path: str, db: str):
        if path not in Connection.INSTANCE_MAP:
            Connection.INSTANCE_MAP[path + os.sep + db] = Connection(path=path, dbname=db)
        return Connection.INSTANCE_MAP[path + os.sep + db]


