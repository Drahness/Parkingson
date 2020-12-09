import sqlite3
import os

from sqlitedao import SqliteDao, ColumnDict
from typing import Type

import Utils
from collections import Iterable
from .models import Model, UsuariModel, PacientsModel, PruebasModel


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
            if not self.check_existence(PruebasModel.get_tablename()[0]):
                self.create_table(PruebasModel.get_tablename()[0], PruebasModel.get_columns_dict()[0])
            if not self.check_existence(PruebasModel.get_tablename()[1]):
                self.create_table(PruebasModel.get_tablename()[1], PruebasModel.get_columns_dict()[1])
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

    def check_existence(self, model: Type[Model] or str) -> bool:
        instance_of_something = False
        table = ""
        if isinstance(model, str):
            instance_of_something = True
            table = model
        elif issubclass(model, Model):
            instance_of_something = True
            table = model.get_tablename()
        if instance_of_something:
            self.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table}'")
            existence = self.cursor.fetchall()
            return existence.count(table) == 1
        else:
            raise AssertionError(f"Bad arguments. expected {type(str)} or {type(Model)} got {type(model)}")



if __name__ == "__main__":
    pass
