import os
import sqlite3
import traceback
from sqlite3 import Connection
from typing import Type, Iterable

from sqlitedao import SqliteDao, ColumnDict

import Utils
from database.entities_interface import Entity
from database.pacient import Pacient
from database.prueba import Prueba
from database.usuari import Usuari


class ModelConnection:
    __INSTANCE_MAP = {}

    # Its a connection for a model, i think its better to be multiple connections between the models.
    # 1 model == 1 connection
    def __init__(self, user, entity=Type[Entity], version_control: int = 1):
        self.path = user
        self.inited = False
        self.version_control = version_control
        self.dbname = entity.__name__ + ".db"
        self.model: Type[Entity] = entity
        filepath = self.path + os.sep + self.dbname
        if not os.path.exists(filepath):
            os.makedirs(self.path, exist_ok=True)
        self.conn: Connection = sqlite3.connect(filepath)
        self.dao: SqliteDao = SqliteDao.get_instance(filepath)
        self.user = user
        self.autocommit = True
        self.cursor = self.conn.cursor()

    def check_existence(self) -> bool:
        if issubclass(self.model, Entity):
            tables = self.model.get_tablenames()
        else:
            raise AssertionError(f"Bad arguments. Needs subclass of {type(Entity)} got {type(self.model)}")
        sql = f"SELECT name FROM sqlite_master WHERE type = 'table'"
        sql += " AND"
        for table in tables:
            sql += f" name = '{table}' or"
        sql = sql[:-2]
        self.execute(sql)
        existence = self.cursor.fetchall()
        i = 0
        for table in tables:
            i += 1 if existence.count(table) else 0
        return len(tables) == i

    def init(self):
        if not self.inited:
            try:
                if self.first_init():
                    if not self.check_existence():
                        for name, columns in self.model.get_definitions():
                            self.create_tables(name, columns)
                version = self.get_version_control()
                if self.version_control > version:
                    self.upgrade_version(version, self.version_control)
                elif self.version_control < version:
                    self.downgrade_version(version, self.version_control)
            except sqlite3.OperationalError:
                traceback.print_exc()
                self.conn.close()
                self.dao.close()
                os.remove(self.path + os.sep + self.dbname)

    @classmethod
    def get_instance(cls, user: str, model: Type[Entity]):
        if not isinstance(model, type):
            raise AssertionError()
        if user not in cls.__INSTANCE_MAP.keys():
            cls.__INSTANCE_MAP[user] = {model: ModelConnection(user, model)}
        elif model not in cls.__INSTANCE_MAP[user].keys():
            cls.__INSTANCE_MAP[user][model] = ModelConnection(user, model)
        return cls.__INSTANCE_MAP[user][model]

    def first_init(self):
        try:
            return self.execute(f"SELECT * FROM first_init")[0] == 0
        except:
            first_init_columns = ColumnDict()
            first_init_columns.add_column("boolean_init", "INTEGER")
            version_control = ColumnDict()
            version_control.add_column("version", "INTEGER")
            self.create_tables("first_init", first_init_columns)
            self.create_tables("version_control", version_control)
            self.execute(f"INSERT OR IGNORE INTO first_init VALUES (0)")
            self.execute(f"INSERT OR IGNORE INTO version_control VALUES (0)")
            return True

    def create_tables(self, tablename: str, columns: ColumnDict, indexes=None):
        self.dao.create_table(tablename, columns, indexes)

    def execute(self, sql, parameters: Iterable = None) -> list:
        print(f"DB:{self.path}/{self.dbname} - Operation: {sql} ¦ {parameters}")
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
    # Cronometro anadir notas
    def get_version_control(self) -> int:
        return 1  # query the database pls

    def upgrade_version(self, old, new) -> None:
        ...  ## this tecnically is pointless here

    def downgrade_version(self, old, new) -> None:
        ...  ## this tecnically is pointless here
