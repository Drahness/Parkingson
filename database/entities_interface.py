from sqlitedao import ColumnDict, SqliteDao


# from Utils import get_timedeltas, get_timedelta


class Entity:
    __loaded_instances: dict = {}

    def __init__(self, id: any, dictionary: dict = None):
        self.dictionary = dictionary
        self._id = id
        pass

    @classmethod
    def load(cls, connection) -> list:
        items = cls._get_list_of_instances()
        dao: SqliteDao = connection.dao
        for obj in dao.search_table(cls.get_tablenames()[0], {}):
            items.append(cls(dictionary=obj))
        Entity.__loaded_instances[cls] = items
        return items

    @staticmethod
    @DeprecationWarning
    def get_columns_dict() -> tuple:...

    @staticmethod
    def is_autoincrement() -> bool:
        return False

    def insert(self, conexion) -> any:...

    def update(self, conexion, to_updated):...

    def delete(self, conexion):...

    @staticmethod
    def get_tables_count() -> int:
        return 1

    @staticmethod
    def get_tablenames() -> tuple:...

    @classmethod
    def get_tablename(cls,index):
        return cls.get_tablenames()[index]

    """ Para mantener la sincronizacion con la BBDD"""

    def append(self):
        list_of_instances: list = self._get_list_of_instances()
        list_of_instances.append(self)

    @classmethod
    def get_object(self, i):
        return self._get_list_of_instances()[i]

    @classmethod
    def _get_list_of_instances(cls) -> list:
        type_of_entity = cls
        if type_of_entity not in Entity.__loaded_instances:
            Entity.__loaded_instances[type_of_entity] = []
        return Entity.__loaded_instances[type_of_entity]

    def remove(self):
        list_of_instances = self._get_list_of_instances()
        list_of_instances.remove(self)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @classmethod
    def get_definitions(cls):
        return [(cls.get_tablenames()[i], cls.get_columns_dict()[i]) for i in range(0, cls.get_tables_count())]
