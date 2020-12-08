import sqlite3
import os

from sqlitedao import SqliteDao, ColumnDict
from typing import Type

import Utils
from collections import Iterable
from .models import Model, UsuariModel, PacientsModel

class Connection:
    DB_PATH: str
    def __init__(self, path: str = "db", dbname=f"default.db", version: int = 1):
        self.first_init = False
        Connection.DB_PATH = path + os.sep + dbname
        if not os.path.exists(Connection.DB_PATH):
            os.makedirs(path, exist_ok=True)
            self.first_init = True
        self.conn = sqlite3.connect(Connection.DB_PATH)
        self.dao = SqliteDao.get_instance(Connection.DB_PATH)
        self.autocommit = True
        self.cursor = self.conn.cursor()
        if self.first_init:
            if not self.check_existence(PacientsModel):
                self.create_table(PacientsModel.get_tablename(), PacientsModel.get_columns_dict())
            if not self.check_existence(UsuariModel):
                self.create_table(UsuariModel.get_tablename(), UsuariModel.get_columns_dict())
            self.execute(f"INSERT OR IGNORE INTO users VALUES ('Admin','{Utils.cypher('Admin')}')")

    def execute(self, sql, parameters: Iterable = None) -> list:
        print(f"Operation: {sql}, {parameters}")
        if parameters is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, parameters)
        if self.autocommit:
            self.conn.commit()
        return self.cursor.fetchall()

    def set_auto_commit(self, boolean: bool) -> None:
        self.autocommit = boolean

    def insert(self, sql, parameters: Iterable = None):
        if parameters is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, parameters)

    def create_table(self, tablename: str, columns: ColumnDict, indexes=None):
        self.dao.create_table(tablename, columns, indexes)

    def check_existence(self, model: Type[Model]) -> bool:
        self.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{model.get_tablename()}'")
        existence = self.cursor.fetchall()
        return existence.count(model.get_tablename()) == 1


def format_list(lista: list) -> str:
    return str(lista)[1:-1]


def format_dict(dictionary: dict, center="=") -> str:
    return str(dictionary)[1:-1].replace(":", center)


if __name__ == "__main__":
    pass
