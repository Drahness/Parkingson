import typing

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from typing import Type
import traceback

from GUI.GUI_Resources import get_error_dialog_msg
from database.DB_Resources import get_db_connection
from database.entities_interface import Entity

class AbstractEntityModel:
    def __init__(self,user:str, base: Type[Entity]):
        self.instance_class = base
        self.__check_subclass(base)
        self.conn = get_db_connection()
        self.items = base.load(self.conn)  # Al ser singleon, solo carga una vez y se matiene sincronizado.
        self.showable_items = None

    def reload(self):...
    def change_model_list(self, list):...
    def get(self, index):...
    def append(self, entity):...
    def __check_instance(self, entity):...
    @staticmethod
    def __check_subclass(type):...
    def delete(self, entity):...
    def update(self, entity, id_to_update):...
    @classmethod
    def get_instance(cls):
        if cls not in ListModel.INSTANCES:
            ListModel.INSTANCES[cls] = cls()
        return ListModel.INSTANCES[cls]

    def __len__(self) -> int:
        return len(self.items)

class ListModel(QAbstractListModel):
    INSTANCES = {}

    def __init__(self, base: Type[Entity]):
        super(ListModel, self).__init__()
        self.instance_class = base
        self.__check_subclass(base)
        self.conn = get_db_connection()
        self.items = base.load(self.conn)  # Al ser singleon, solo carga una vez y se matiene sincronizado.
        self.showable_items = None
        # TODO hacer que load sea mas dinamico, recargandose con algun cambio en la BBDD sin pasar con el programa? Maybe un thread que hace check?

    def reload(self):
        self.items = self.instance_class.load(self.conn)

    def change_model_list(self, list):
        if list is not None:
            if len(list) > 0:
                if isinstance(list[0], self.instance_class):
                    self.showable_items = list
                    self.layoutChanged.emit()
                else:
                    raise TypeError(f"Provided a list of non pure objects of type {self.instance_class}")
            else:
                self.showable_items = list
                self.layoutChanged.emit()

    def data(self, index: QModelIndex, role: int = ...) -> typing.Any:
        """Retornara el objeto convertido a string sin mas
        Called to display information in the listview"""
        if self.showable_items is None:
            self.showable_items = self.items
        if role == Qt.DisplayRole:
            item = self.showable_items[index.row()]
            return item

    def get(self, index):
        """Retorna el item clickado"""
        return self.showable_items[index]

    def rowCount(self, parent: QModelIndex = ...) -> int:
        """Called for me, idk what is QModelIndex"""
        return len(self.showable_items) if self.showable_items is not None else len(self.items)

    def append(self, entity):
        """Append to the list."""
        try:
            self.__check_instance(entity)
            entity.insert(self.conn)
            self.layoutChanged.emit()
        except Exception as e:
            string = f"""Error mientras se agregaba la entidad {type(entity).__name__} con identificador {entity.get_id()}"""
            get_error_dialog_msg(e, string, "Error de insertacion").exec_()

    def __check_instance(self, entity):
        """Check if the instance is equal to the instance passed."""
        if not isinstance(entity, self.instance_class):
            raise TypeError(f"Method append expected {self.instance_class}, got {type(entity)}")

    @staticmethod
    def __check_subclass(type):
        """Private instance to check if a instance is in hierarchy of the class passed as parameter in __init__"""
        if not issubclass(type, Entity):
            raise TypeError(f"Base class {type} must be a subclass of {type(Entity)}")

    def delete(self, entity):
        try:
            self.__check_instance(entity)
            entity.delete(self.conn)
            self.layoutChanged.emit()
        except Exception as e:
            string = f"""Error mientras se eliminaba la entidad {type(entity).__name__} con identificador {entity.get_id()}"""
            get_error_dialog_msg(e, string, "Error de eliminacion").exec_()

    def update(self, entity, id_to_update):
        try:
            self.__check_instance(entity)
            entity.update(self.conn, id_to_update)
            self.layoutChanged.emit()
        except Exception as e:
            string = f"""Error mientras se eliminaba la entidad {type(entity).__name__} con identificador {entity.get_id()}"""
            get_error_dialog_msg(e, string, "Error de actualizacion").exec_()

    @classmethod
    def get_instance(cls):
        if cls not in ListModel.INSTANCES:
            ListModel.INSTANCES[cls] = cls()
        return ListModel.INSTANCES[cls]

    def __len__(self) -> int:
        return len(self.items)


class UsuariListModel(ListModel):
    """ No se si la voy a usar"""

    def __init__(self):
        from database.usuari import Usuari
        super(UsuariListModel, self).__init__(Usuari)


class PacientsListModel(ListModel):
    def __init__(self):
        from database.pacient import Pacient
        super(PacientsListModel, self).__init__(Pacient)
        pass

    def data(self, index: QModelIndex, role: int = ...):
        pacient = super(PacientsListModel, self).data(index, role)
        if pacient is not None:
            return str(pacient)


class PruebasListModel(ListModel):
    def __init__(self):
        from database.prueba import Prueba
        super(PruebasListModel, self).__init__(Prueba)

    def get_pruebas(self, pacient) -> list:
        pruebas = []
        for prueba in self.items:
            if pacient.dni == prueba.pacient_id:
                pruebas.append(prueba)
        self.change_model_list(sorted(pruebas))
        return pruebas

    def data(self, index: QModelIndex, role: int = ...):
        prueba = super(PruebasListModel, self).data(index, role)
        if prueba is not None:
            return str(prueba.datetime.strftime("%m/%d/%Y, %H:%M:%S"))
