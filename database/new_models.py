from typing import Type

import typing
from PyQt5.QtCore import QAbstractListModel, Qt, QModelIndex, QObject

from GUI.GUI_Resources import get_error_dialog_msg
from database.database_connection import ModelConnection
from database.entities_interface import Entity


class AbstractEntityModel:
    INSTANCES = {}

    def __init__(self, user: str, base: Type[Entity], implementation: type):
        super(AbstractEntityModel, self).__init__()
        self.implementation = implementation
        self.entity_type = base
        self.__check_subclass(base)
        self.conn: ModelConnection = ModelConnection.get_instance(user, base)
        self.conn.init()
        self.entities = base.load(self.conn)  # Al ser singleon, solo carga una vez y se matiene sincronizado.
        self.showable_items = None

    def change_callback(self): ...

    def reload(self):
        self.entities = self.entity_type.load(self.conn)
        self.change_callback()

    def change_model_list(self, entities):
        if entities is not None:
            if len(entities) > 0:
                if isinstance(entities[0], self.entity_type):
                    self.showable_items = entities
                    self.change_callback()
                else:
                    raise TypeError(f"Provided a list of non pure objects of type {self.entity_type}")
            else:
                self.showable_items = entities
                self.change_callback()

    def get(self, index: int):
        return self.entities[index]

    def __check_instance(self, entity):
        if not isinstance(entity, self.entity_type):
            raise TypeError(f"Method append expected {self.entity_type}, got {type(entity)}")

    def delete(self, entity):
        try:
            self.__check_instance(entity)
            entity.delete(self.conn)
            self.change_callback()
        except Exception as e:
            string = f"""Error mientras se eliminaba la entidad {type(entity).__name__} con identificador {entity.get_id()}"""
            get_error_dialog_msg(e, string, "Error de eliminacion").exec_()

    def update(self, entity, id_to_update):
        try:
            self.__check_instance(entity)
            entity.update(self.conn, id_to_update)
            self.change_callback()
        except Exception as e:
            string = f"""Error mientras se eliminaba la entidad {type(entity).__name__} con identificador {entity.get_id()}"""
            get_error_dialog_msg(e, string, "Error de actualizacion").exec_()

    def append(self, entity):
        """Append to the list."""
        try:
            self.__check_instance(entity)
            entity.insert(self.conn)
            self.change_callback()
        except Exception as e:
            string = f"""Error mientras se agregaba la entidad {type(entity).__name__} con identificador {entity.get_id()}"""
            get_error_dialog_msg(e, string, "Error de insertacion").exec_()

    @classmethod
    def get_instance(cls, user, type, implementation):
        if user not in cls.INSTANCES:
            cls.INSTANCES[user] = {type: {implementation: cls(user)}}
        elif type not in cls.INSTANCES[user]:
            cls.INSTANCES[user][type] = {implementation: cls(user)}
        elif implementation not in cls.INSTANCES[user][type]:
            cls.INSTANCES[user][type][implementation] = cls(user)
        return cls.INSTANCES[user][type][implementation]

    @staticmethod
    def __check_subclass(type):
        """Private instance to check if a instance is in hierarchy of the class passed as parameter in __init__"""
        if not issubclass(type, Entity):
            raise TypeError(f"Base class {type} must be a subclass of {type(Entity)}")

    def __len__(self) -> int:
        return len(self.entities)


class NewListModel(AbstractEntityModel,QAbstractListModel):
    INSTANCES = {}

    def __init__(self, user: str, base: Type[Entity]):
        super(NewListModel, self).__init__(user, base, QAbstractListModel)
        QAbstractListModel.__init__(self)


    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        """Retornara el objeto convertido a string sin mas
        Called to display information in the listview"""
        if self.showable_items is None:
            self.showable_items = self.entities
        if role == Qt.DisplayRole:
            item = self.showable_items[index.row()]
            return item

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """Called for me, idk what is QModelIndex"""
        return len(self.showable_items) if self.showable_items is not None else len(self.entities)

    @classmethod
    def get_instance(cls, user: str, type: type, implementation=QAbstractListModel):
        return super(NewListModel, cls).get_instance(user, type, implementation)

    def change_callback(self):
        self.layoutChanged.emit()

