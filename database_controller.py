
import sqlite3

class DAO():
    def __init__(self):
        pass
    def get(self):
        pass
    def update(self):
        pass

class Cursor():
    instances: list = []

    def __init__(self, name="test/default.sql"):
        self.conn = sqlite3.connect(name)

    def select(self,table,parameters):
        self.conn.execute()

    def update(self,table,**kwargs):
        update_values = ""
        for x, y in kwargs:
            if len(update_values) == 0:
                update_values += f"{x} = {y},"
        update_values = update_values[:-1]
        self.conn.execute(f"UPDATE {table} SET {update_values}")

    def insert(self,table,parameters):
        self.conn.execute(f"UPDATE {table} SET {update_values}")

    def delete(self,table,parameters):
        pass