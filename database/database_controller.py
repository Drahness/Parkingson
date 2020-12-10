import sqlite3
import os

from sqlitedao import SqliteDao, ColumnDict
from typing import Type

import Utils
from collections import Iterable
from .models import ListModel, UsuariListModel, PacientsListModel, PruebasListModel


class Connection:
    INSTANCE_MAP = {}

    def __init__(self, path: str = "db", dbname=f"default.db"):
        self.first_init = False
        filepath = path + os.sep + dbname
        if not os.path.exists(filepath):
            os.makedirs(path, exist_ok=True)
            self.first_init = True
        self.conn = sqlite3.connect(filepath)
        self.dao = SqliteDao.get_instance(filepath)
        self.autocommit = True
        self.cursor = self.conn.cursor()
        if self.first_init:
            if not self.check_existence(PacientsListModel):
                self.create_table(PacientsListModel.get_tablename(), PacientsListModel.get_columns_dict())
            if not self.check_existence(UsuariListModel):
                self.create_table(UsuariListModel.get_tablename(), UsuariListModel.get_columns_dict())
            if not self.check_existence(PruebasListModel.get_tablename()[0]):
                self.create_table(PruebasListModel.get_tablename()[0], PruebasListModel.get_columns_dict()[0])
            if not self.check_existence(PruebasListModel.get_tablename()[1]):
                self.create_table(PruebasListModel.get_tablename()[1], PruebasListModel.get_columns_dict()[1])
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
            self.execute(sql)
        else:
            self.execute(sql, parameters)

    def create_table(self, tablename: str, columns: ColumnDict, indexes=None):
        self.dao.create_table(tablename, columns, indexes)

    def check_existence(self, model: Type[ListModel] or str) -> bool:
        instance_of_something = False
        table = ""
        if isinstance(model, str):
            instance_of_something = True
            table = model
        elif issubclass(model, ListModel):
            instance_of_something = True
            table = model.get_tablename()
        if instance_of_something:
            self.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table}'")
            existence = self.cursor.fetchall()
            return existence.count(table) == 1
        else:
            raise AssertionError(f"Bad arguments. expected {type(str)} or {type(ListModel)} got {type(model)}")

    @staticmethod
    def get_instance(path: str, db: str):
        if path not in Connection.INSTANCE_MAP:
            Connection.INSTANCE_MAP[path+os.sep+db] = Connection(path, db)
        return Connection.INSTANCE_MAP[path+os.sep+db]
