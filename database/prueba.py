import datetime

from sqlitedao import ColumnDict

from Utils import get_timedeltas, timedelta_to_float
from database.entities_interface import Entity
from database.pacient import Pacient


class Prueba(Entity):
    def __init__(self,
                 identifier: int = None,
                 laps: list = None,
                 pacient_id: str = None,
                 datetime_of_test: datetime.datetime = None,
                 notas: list = None,
                 dictionary: dict = None):
        if dictionary is not None:
            self.dictionary = dictionary
            identifier = dictionary["identifier"]
            laps = dictionary["laps"]
            notas = dictionary["notas"]
            pacient_id = dictionary["pacient_id"]
            datetime_of_test = dictionary["datetime"]
        super().__init__(identifier)
        #self.identifier = identifier or None  # Integer
        if laps is not None:
            if len(laps) > 0 and isinstance(laps[0], float):
                self.laps = get_timedeltas(laps)
            else:
                self.laps = laps
        else:
            self.laps = laps
        self.pacient_id = pacient_id
        self.notas = notas
        if isinstance(datetime_of_test, str):
            self.datetime = datetime.datetime.strptime(datetime_of_test, '%Y-%m-%d %H:%M:%S.%f')
        else:
            self.datetime = datetime_of_test

    def insert(self, conexion) -> int:
        conexion.set_auto_commit(False)
        result = conexion.execute("SELECT seq FROM sqlite_sequence WHERE name = ?", [self.get_tablenames()[0]])

        if len(result) == 0:
            result = 0
        else:
            result = result[0][0] + 1
        self.id = result
        conexion.execute("INSERT INTO pruebas (identifier,pacient_id,datetime) VALUES (?,?,?)", [self.id,
                                                                                                 self.pacient_id,
                                                                                                 str(self.datetime)])
        for i_lap in range(0, len(self.laps)):
            curr_lap = self.laps[i_lap]
            curr_notas = self.notas[i_lap]
            conexion.execute("INSERT INTO pruebas_data (identifier,tiempo,notas,num_lap) VALUES (?,?,?,?)",
                             [self.id,
                              timedelta_to_float(curr_lap),
                              curr_notas,
                              i_lap])
        conexion.commit()
        conexion.set_auto_commit(True)
        self.append()
        return result

    def update(self, conexion, to_updated):
        if isinstance(to_updated, str):
            identifier = to_updated
        elif isinstance(to_updated, Prueba):
            identifier = to_updated.id
        else:
            raise AssertionError("argument type dont supported, type: " + str(type(to_updated)))
        laps_to_update = conexion.execute(
            f"SELECT rowid FROM {self.get_tablenames()[1]} WHERE identifier = ?", [identifier])
        conexion.execute(f"UPDATE {self.get_tablenames()[0]} SET identifier = ?, pacient_id = ?, datetime = ? WHERE "
                         f"identifier = ?",
                         [self.id,
                          self.pacient_id,
                          self.datetime,
                          identifier])
        for i in range(0, len(laps_to_update)):
            conexion.execute(
                f"UPDATE {self.get_tablenames()[1]} SET identifier = ?, notas= ? ,tiempo = ?, num_lap = ? WHERE rowid = ?",
                [
                    self.id,
                    self.notas[i],
                    timedelta_to_float(self.laps[i]),
                    i,
                    laps_to_update[i][0]
                ])

    @staticmethod
    def is_autoincrement() -> bool:
        return True

    @property
    def laps(self):
        return self._laps

    @laps.setter
    def laps(self, value: list):
        if isinstance(value, list):
            if len(value) == 3:
                if isinstance(value[0], float):
                    self._laps = get_timedeltas(value)
                elif isinstance(value[0], datetime.timedelta):
                    self._laps = value
                elif isinstance(value[0], datetime.time):
                    new_value = []
                    for time in value:
                        time: datetime.time = time
                        new_value.append(datetime.timedelta(seconds=time.second, minutes=time.minute))
                    self._laps = new_value
            else:
                self._laps = value
        else:
            return

    def delete(self, conexion):
        conexion.set_auto_commit(False)
        conexion.execute("DELETE FROM pruebas WHERE identifier = ?", [self.id])
        conexion.execute("DELETE FROM pruebas_data WHERE identifier = ?", [self.id])
        conexion.commit()
        conexion.set_auto_commit(True)
        self.remove()

    @classmethod
    def load(cls, connection) -> list:
        items = cls._get_list_of_instances()
        dictionaries = connection.dao.search_table(Prueba.get_tablenames()[0], {},
                                                   order_by=["datetime"])  # Este order by sobra
        # Implementar __repr__ deberia ser lo normal.
        for dictionary in dictionaries:
            time_x_lap = []
            notas_x_lap = []
            list_laps = connection.dao.search_table(table_name=Prueba.get_tablenames()[1],
                                                    search_dict={"identifier": dictionary["identifier"]},
                                                    order_by=["num_lap"])
            for lap in list_laps:
                time_x_lap.append(lap["tiempo"])
                notas_x_lap.append(lap["notas"])
            dictionary["laps"] = time_x_lap
            dictionary["notas"] = notas_x_lap
            items.append(cls(dictionary=dictionary))
        return items

    @staticmethod
    def get_tables_count() -> int:
        return 2

    @staticmethod
    def get_tablenames() -> tuple:
        return "pruebas", "pruebas_data"

    @staticmethod
    def get_columns_dict() -> tuple:
        first_table = ColumnDict()
        first_table.add_column("identifier", "INTEGER", "PRIMARY KEY AUTOINCREMENT")
        first_table.add_column("pacient_id", "TEXT")
        first_table.add_column("datetime", "datetime")
        first_table.add_column("FOREIGN KEY(pacient_id)",
                               f"REFERENCES {Pacient.get_tablenames()[0]}({Pacient.ID})")

        second_table = ColumnDict()
        second_table.add_column("identifier", "INTEGER")  # id de la prueba
        second_table.add_column("tiempo", "REAL")  # Real en segundos.microsegundos
        second_table.add_column("notas", "TEXT")
        second_table.add_column("num_lap", "INTEGER")
        return first_table, second_table

    def __str__(self, *args, **kwargs):
        string = ""
        for x in range(0, len(self.laps)):
            string += f'{x}: {self.laps[x]} | '
        return string

    def __le__(self, other):
        if isinstance(other, Prueba):
            return self.datetime < other.datetime or self.datetime == other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime < other or self.datetime == other
        if isinstance(other, datetime.date):
            return self.datetime.date() < other or self.datetime.date() == other

    def __ge__(self, other):
        if isinstance(other, Prueba):
            return self.datetime > other.datetime or self.datetime == other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime > other or self.datetime == other
        if isinstance(other, datetime.date):
            return self.datetime.date() > other or self.datetime.date() == other

    def __gt__(self, other):
        if isinstance(other, Prueba):
            return self.datetime > other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime > other
        if isinstance(other, datetime.date):
            return self.datetime.date() > other

    def __lt__(self, other):
        if isinstance(other, Prueba):
            return self.datetime < other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime < other
        if isinstance(other, datetime.date):
            return self.datetime.date() < other

    def __eq__(self, other):
        if isinstance(other, Prueba):
            return self.datetime == other.datetime
        if isinstance(other, datetime.datetime):
            return self.datetime == other
        if isinstance(other, datetime.date):
            return self.datetime.date() == other