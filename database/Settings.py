from datetime import timedelta

from sqlitedao import ColumnDict, SqliteDao

import Utils
from database.database_controller import Connection
from database.entities import Entity, Usuari


class Settings(Entity):
    instance = ...
    @property
    def DEFAULT_USER(self):
        return "Admin"

    def __init__(self, dictionary: dict, user: str):
        super().__init__(self, dictionary)
        self.instance = self
        self.user = user
        self.isInserted = True
        self.lap0_name = dictionary.get('lap0_name')
        self.lap1_name = dictionary.get('lap1_name')
        self.lap2_name = dictionary.get('lap2_name')
        self.lap_total_name = dictionary.get('lap_total_name')
        self.lap0_lowmedium_start = Utils.get_timedelta(dictionary.get('lap0_lowmedium_start'))
        self.lap1_lowmedium_start = Utils.get_timedelta(dictionary.get('lap1_lowmedium_start'))
        self.lap2_lowmedium_start = Utils.get_timedelta(dictionary.get('lap2_lowmedium_start'))
        self.lap0_mediumhard_start = Utils.get_timedelta(dictionary.get('lap0_mediumhard_start'))
        self.lap1_mediumhard_start = Utils.get_timedelta(dictionary.get('lap1_mediumhard_start'))
        self.lap2_mediumhard_start = Utils.get_timedelta(dictionary.get('lap2_mediumhard_start'))
        self.locale = dictionary.get('locale')

    @classmethod
    def init_default(cls, user:str=None):
        if user is None:
            user = cls.DEFAULT_USER
        dictionary = {
            "lap0_name": "Marxa",
            "lap1_name": "Equilibri",
            "lap2_name": "Doble tasca",
            "lap_total_name": "Circuit",
            "lap0_lowmedium_start": timedelta(seconds=17, microseconds=160),
            "lap1_lowmedium_start": timedelta(seconds=15, microseconds=140),
            "lap2_lowmedium_start": timedelta(seconds=10, microseconds=430),
            "lap0_mediumhard_start": timedelta(seconds=23, microseconds=560),
            "lap1_mediumhard_start": timedelta(seconds=25, microseconds=900),
            "lap2_mediumhard_start": timedelta(seconds=13, microseconds=340),
            "locale": "Es"
        }
        return Settings(dictionary=dictionary, user=user)

    def insert(self, conexion: Connection) -> any:
        if conexion.has_users():
            results = conexion.execute(f"SELECT * FROM {self.get_tablename()} WHERE username like {self.user}")
            for val,key in self.dictionary.items():
                if {"key":key,"value":val,"username":self.user} in results:
                    pass
                    # TODO

        pass

    def update(self, conexion, to_updated):
        """With the settings the param to_updated is completely ignored. In all cases"""
        pass

    def delete(self, conexion):
        pass

    @staticmethod
    def get_instance():
        return Settings.instance

    @staticmethod
    def get_tablename():
        return "settings"

    @classmethod
    def load(cls, connection) -> list:
        dao: SqliteDao = connection.dao
        settingsDictionary = {}
        if connection.has_users():
            user = connection.user
        else:
            user = cls.DEFAULT_USER
        results = dao.search_table(cls.get_tablename(), {"username": user})
        for result in results:
            settingsDictionary[result.get("key")] = result.get("value")
        settings = Settings(settingsDictionary, user)
        return [settings]

    @staticmethod
    def get_columns_dict() -> tuple or ColumnDict:
        columns = ColumnDict()
        columns.add_column("key", "text", "PRIMARY KEY")
        columns.add_column("value", "text")
        columns.add_column("username", "text", )
        columns.add_column("FOREIGN KEY(pacient_id)",
                           f"REFERENCES {Usuari.get_tablename()}(username)")
