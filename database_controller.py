import sqlite3
#
#self.conn.execute("""CREATE TABLE pacients ( name VARCHAR(20),
#dni VARCHAR(9),
#apellido1 VARCHAR(20),
#apellido2 VARCHAR(20),
#estadio tinyint );""")
#self.conn.execute("""CREATE TABLE users ( username VARCHAR(50), password VARCHAR(?)""")
class DAO():
    def __init__(self):
        pass

    def get(self):
        pass

    def update(self):
        pass

    def delete(self, id):

class Cursor():
    def __init__(self, name="test/default.db"):
        self.conn = sqlite3.connect(name)
        self.autocommit = True
        self.cursor = self.conn.cursor()

    def execute(self, string):
        print(f"Operation: {string}")
        self.cursor.execute(string)
        if self.autocommit:
            self.conn.commit()
        return self.cursor.fetchall()

    def set_auto_commit(self, boolean: bool):
        self.autocommit = boolean

    def select_parametrized(self, table: str, where: dict={},and_or: list=[], fields: list = None):
        if fields is None:
            query = f"SELECT * "
        else:
            query = f"SELECT {str(fields)[1:-1]} "
        query += f"{Cursor.__get_string_where(where)}"

        self.execute(query)

    def update_parametrized(self, table: str, column_newvalue, where: dict = {}):
        if where is None:
            self.execute(f"UPDATE {table} SET {Cursor.__get_string_update(column_newvalue)}")
        else:
            self.execute(f"UPDATE {table} SET {Cursor.__get_string_update(column_newvalue)} WHERE {Cursor.__get_string_where(where)}")

    def insert_parametrized(self, table: str, parameters: list):
        insert = format_list(parameters)
        self.execute(f"INSERT INTO {table} VALUES ({insert})")

    def delete_parametrized(self, table: str, and_or: list = [], pair_key_value: dict = {}):
        if len(pair_key_value) == 0:
            self.execute(f"DELETE FROM {table}")
        else:
            self.execute(f"DELETE FROM {table} WHERE {Cursor.__get_string_where(and_or, pair_key_value)}")

    @staticmethod
    def __get_string_update(pair_key_value: dict):
        values = ""
        for x, y in pair_key_value.items():
            values += f"{x} = {y},"
        values = values[:-1]
        return values

    @staticmethod
    def __get_string_where(pair_key_value: dict,parameters: list=[]):
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

    """G"""

    def create_table(self, tablename, column_type: dict, aditional_parameters=None):
        if aditional_parameters is None:
            aditional_parameters = {}
        if len(aditional_parameters) != len(column_type):
            raise RuntimeError(
                f"Parameters uneven\naditional_parameters: {aditional_parameters}\ntype_value: {column_type}")
        create = F"CREATE TABLE {tablename}"
        values = ""
        for column, type in column_type.items():
            try:
                param = aditional_parameters[column]
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
    cur = Cursor()
    table = "aaaaaa"
    #cur.create_table(table, {"id": "INT","a":"VARHCAR"}, {"id": "AUTOINCREMENTAL","a":"Unique"})
    #cur.insert(table, [1,"a"])
   # cur.update(table, {"INT": "12"},{"INT":1})
   # cur.select(table, {"INT": "12"})
   # cur.delete(table)
    print(cur.execute(f"select * from {table}"))
    print(format_list([1, 5, 2, 5, 5, 3, 5, 8, 599, 65, 9, 54, 9]))
    print(format_dict({1: 5, 561: "a"}))
    # cur.select()
