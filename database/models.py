import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from typing import Type

from database.DB_Resources import get_db_connection
from database.entities import Entity


class ListModel(QAbstractListModel):
    INSTANCES = {}
    def __init__(self, base: Type[Entity]):
        super(ListModel, self).__init__()
        self.instance_class = base
        self.__check_subclass(base)
        self.items = base.load(get_db_connection())  # Al ser singleon, solo carga una vez y se matiene sincronizado.

    """Retornara el objeto convertido a string sin mas"""

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        print("data called")
        if role == Qt.DisplayRole:
            item = self.items[index.row()]
            return str(item)

    def rowCount(self, parent: QModelIndex = ...) -> int:
        print("rowCount called")
        return len(self.items)

    def append(self, entity):
        self.__check_instance(entity)
        self.layoutChanged.emit()
        entity.insert(get_db_connection())

    def __check_instance(self, entity):
        if not isinstance(entity, self.instance_class):
            raise TypeError(f"Method append expected {self.instance_class}, got {type(entity)}")

    @staticmethod
    def __check_subclass(type):
        if not issubclass(type, Entity):
            raise TypeError(f"Base class {type} must be a subclass of {type(Entity)}")

    def delete(self, pacient):
        pass

    ## TODO Ver como seria este metodo.
    def modify(self, identifier, newInstance):
        pass

    @classmethod
    def get_instance(cls):
        if cls not in ListModel.INSTANCES:
            ListModel.INSTANCES[cls] = cls()
        return ListModel.INSTANCES[cls]


class UsuariListModel(ListModel):
    """ No se si la voy a usar"""
    def __init__(self):
        from database.entities import Usuari
        super(UsuariListModel, self).__init__(Usuari)


class PacientsListModel(ListModel):
    def __init__(self):
        from database.entities import Pacient
        super(PacientsListModel, self).__init__(Pacient)
        pass


class PruebasListModel(ListModel):
    def __init__(self):
        from database.entities import Prueba
        super(PruebasListModel, self).__init__(Prueba)
