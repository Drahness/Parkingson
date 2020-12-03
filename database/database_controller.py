import sqlite3
import os


from collections import Iterable


class Connection:
    def __init__(self, name=f"test{os.sep}default.db"):
        if not os.path.exists("../test"):
            os.mkdir("../test")
        self.conn = sqlite3.connect(name)
        self.autocommit = True
        self.cursor = self.conn.cursor()

    def execute(self, string, parameters):
        print(f"Operation: {string}, {parameters}")
        self.cursor.execute(string, parameters)
        if self.autocommit:
            self.conn.commit()
        return self.cursor.fetchall()

    def set_auto_commit(self, boolean: bool):
        self.autocommit = boolean

    def insert(self, sql, parameters: Iterable = ""):
        self.conn.execute(sql, parameters)

    @staticmethod
    def __get_string_update(pair_key_value: dict):
        values = ""
        for x, y in pair_key_value.items():
            values += f"{x} = {y},"
        values = values[:-1]
        return values

    @staticmethod
    def __get_string_where(pair_key_value: dict, parameters: list = []):
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


def format_list(lista: list) -> str:
    return str(lista)[1:-1]


def format_dict(dictionary: dict, center="=") -> str:
    return str(dictionary)[1:-1].replace(":", center)


if __name__ == "__main__":
    cur = Connection()
    table = "aaaaaa"
    # cur.create_table(table, {"id": "INT",
    #                        "a":"VARHCAR",
    #                       },
    #                     {"id": "AUTOINCREMENTAL",
    #                     "a":"Unique"
    #                    })
    # CREATE TABLE aaaaaa (INT id AUTOINCREMENTAL,VARHCAR a Unique)

    print(cur.conn.execute(f"INSERT INTO {table} (a) VALUES (?)"))
    print(format_list([1, 5, 2, 5, 5, 3, 5, 8, 599, 65, 9, 54, 9]))
    print(format_dict({1: 5, 561: "a"}))
    # cur.select()
