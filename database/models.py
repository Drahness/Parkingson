from __future__ import annotations

from PyQt5.QtCore import QAbstractListModel, QModelIndex, Qt
from database.new_models import EntityListModel
from database.pacient import Pacient
from database.prueba import Prueba
from database.usuari import Usuari

class UsuariListModel(EntityListModel):
    """ No se si la voy a usar"""

    def __init__(self, user="Admin", base=Usuari):
        super(UsuariListModel, self).__init__(user, base)

    @classmethod
    def get_instance(cls, user, type=Pacient, implementation=None) -> UsuariListModel:
        return super(UsuariListModel, cls).get_instance(user, type)


class PacientsListModel(EntityListModel):
    def __init__(self, user="Admin", base=Pacient, implementation=QAbstractListModel):
        super(PacientsListModel, self).__init__(user, Pacient)
        pass

    def data(self, index: QModelIndex, role: int = ...):
        pacient = super(PacientsListModel, self).data(index, role)
        if pacient is not None:
            return str(pacient)

    @classmethod
    def get_instance(cls, user, type=Pacient, implementation=None) -> PacientsListModel:
        return super(PacientsListModel, cls).get_instance(user, type)


class PruebasListModel(EntityListModel):
    def __init__(self, user="Admin"):
        super(PruebasListModel, self).__init__(user, Prueba)

    def get_pruebas(self, pacient) -> list:
        pruebas = []
        for prueba in self.entities:
            if pacient.id == prueba.pacient_id:
                pruebas.insert(0,prueba)
        #self.change_model_list(sorted(pruebas)) esto no va aqui lol joan.
        return pruebas

    def data(self, index: QModelIndex, role: int = ...):
        prueba = super(PruebasListModel, self).data(index, role)
        if prueba is not None:
            return str(str(index.row()+1)+": "+prueba.datetime.strftime("%m/%d/%Y, %H:%M:%S"))

    @classmethod
    def get_instance(cls, user, typee=Prueba, implementation=None) -> PruebasListModel:
        return super(PruebasListModel, cls).get_instance(user, typee)

    def append(self, entity):
        super().append(entity)


