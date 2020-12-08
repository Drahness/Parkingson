import sqlite3
import os

from .models import Model, Usuari, Pacients
from collections import Iterable


class Connection:
    def __init__(self, version: int = 1, path: str = "db", dbname=f"default.db"):
        self.first_init = False
        if not os.path.exists(path):
            os.makedirs(path)
            self.first_init = True
        if not os.path.exists(dbname):
            self.first_init = True
        self.conn = sqlite3.connect(path+os.sep+dbname)
        self.autocommit = True
        self.cursor = self.conn.cursor()
        if self.first_init:
            self.execute(Pacients.get_table_structure())
            self.execute(Usuari.get_table_structure())
            # self.execute("CREATE TABLE DBVersion (version INTEGER)")
            # self.execute("INSERT INTO DBVersion (?)", str(version))

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

    @staticmethod
    def __get_string_update(pair_key_value: dict):
        values = ""
        for x, y in pair_key_value.items():
            values += f"{x} = {y},"
        values = values[:-1]
        return values

    @staticmethod
    def __get_string_where(pair_key_value: dict, parameters=None):
        if parameters is None:
            parameters = []
        values = ""
        if len(pair_key_value) == 0:
            pass
        elif len(parameters) != len(pair_key_value) - 1:
            raise RuntimeError(f"Parameters uneven\n{parameters}\n{pair_key_value}")
        i = -1
        for x, y in pair_key_value.items():
            if len(values) == 0:
                values += f"{x} = {y}"
            else:
                values += f" {parameters[i]} {x} = {y}"
            i += 1
        return values

    def create_table(self, tablename, column_name_and_type: dict, column_name_and_aditional_parameters=None):
        if column_name_and_aditional_parameters is None:
            column_name_and_aditional_parameters = {}
        if len(column_name_and_aditional_parameters) != len(column_name_and_type):
            raise RuntimeError(
                f"Parameters uneven\naditional_parameters: {column_name_and_aditional_parameters}\ntype_value: {column_name_and_type}")
        create = F"CREATE TABLE {tablename}"
        values = ""
        for column, type in column_name_and_type.items():
            try:
                param = column_name_and_aditional_parameters[column]
            except KeyError:
                param = ""
            if len(values) == 0:
                values += f"{type} {column} {param}"
            else:
                values += f",{type} {column} {param}"
        create += f" ({values})"
        self.execute(create)

    def check_existence(self, model: Model) -> bool:
        self.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = {model.get_tablename()};")
        existence = self.cursor.fetchall()
        return existence.count(model.get_tablename()) == 1


def format_list(lista: list) -> str:
    return str(lista)[1:-1]


def format_dict(dictionary: dict, center="=") -> str:
    return str(dictionary)[1:-1].replace(":", center)


if __name__ == "__main__":
    pass
