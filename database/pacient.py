import datetime

from PyQt5.QtCore import QDate
from dateutil.parser import parse
from sqlitedao import ColumnDict

from database.entities_interface import Entity


class Pacient(Entity):
    ID = "dni"
    dni: str
    apellidos: str
    estadio: int
    nombre: str

    def __gt__(self, other):
        if isinstance(other, Pacient):
            return self.id > other.id
        if isinstance(other, str):
            return self.id > other

    def __lt__(self, other):
        if isinstance(other, Pacient):
            return self.id < other.id
        if isinstance(other, str):
            return self.id < other

    def __eq__(self, other):
        if isinstance(other, Pacient):
            return self.id == other.id
        if isinstance(other, str):
            return self.id == other

    def __init__(self,
                 dni: str = None,
                 apellidos: str = None,
                 estadio: int = None,
                 nombre: str = None,
                 nacimiento: datetime.date = None,
                 notas: str = None,
                 telefono: str = None,
                 mail: str = None,
                 fotocara: bytes = None,
                 fotocuerpo: bytes = None,
                 direccion: str = None,
                 peso: float = None,
                 genero: str = None,
                 altura: float = None,
                 fecha_diagnostico: datetime.date = None,
                 dictionary: dict = None):
        if dictionary is not None:
            self.dictionary = dictionary
            dni = dictionary.get("dni")
            nacimiento = dictionary.get("nacimiento")
            apellidos = dictionary.get("apellidos")
            estadio = dictionary.get("estadio")
            nombre = dictionary.get("nombre")
            notas = dictionary.get("notas")
            telefono = dictionary.get("telefono")
            mail = dictionary.get("mail")
            fotocara = dictionary.get("fotocara")
            fotocuerpo = dictionary.get("fotocuerpo")
            direccion = dictionary.get("direccion")
            peso = dictionary.get("peso")
            genero = dictionary.get("genero")
            altura = dictionary.get("altura")
            fecha_diagnostico = dictionary.get("fecha_diagnostico")
        super().__init__(dni)
        self.apellidos = apellidos
        self.estadio = estadio
        self.nombre = nombre
        self.nacimiento = nacimiento if not isinstance(nacimiento, str) else parse(nacimiento)
        self.notas = notas
        self.telefono = telefono
        self.mail = mail
        self.fotocara = fotocara
        self.fotocuerpo = fotocuerpo
        self.direccion = direccion
        self.peso = peso
        self.genero = genero
        self.fecha_diagnostico = fecha_diagnostico if not isinstance(fecha_diagnostico, str) else parse(fecha_diagnostico)
        self.altura = altura

    def insert(self, conexion):
        attributes = [self.id,
                      self.apellidos,
                      self.estadio,
                      self.nombre,
                      self.nacimiento,
                      self.notas,
                      self.telefono,
                      self.mail,
                      self.fotocara,
                      self.fotocuerpo,
                      self.direccion,
                      self.peso,
                      self.genero,
                      self.fecha_diagnostico,
                      self.altura]
        sql = "INSERT INTO pacients (  dni," \
              "apellidos," \
              "estadio," \
              "nombre," \
              "nacimiento," \
              "notas," \
              "telefono," \
              "mail," \
              "fotocara," \
              "fotocuerpo," \
              "direccion," \
              "peso," \
              "genero," \
              "fecha_diagnostico," \
              "altura)" \
              " VALUES "
        sql = (sql + "(" + ("?," * len(attributes)))[:-1] + ")"
        conexion.execute(sql, attributes)
        self.append()
        return self.id

    def update(self, conexion, to_updated):
        if isinstance(to_updated, str):
            dni = to_updated
        elif isinstance(to_updated, Pacient):
            dni = to_updated.dni
        else:
            raise AssertionError("argument type dont supported, type: " + str(type(to_updated)))
        if self.id != dni:
            atributos = [self.id,
                         self.apellidos,
                         self.estadio,
                         self.nombre,
                         self.nacimiento,
                         self.notas,
                         self.telefono,
                         self.mail,
                         self.fotocara,
                         self.fotocuerpo,
                         self.direccion,
                         self.peso,
                         self.genero,
                         self.fecha_diagnostico,
                         self.altura,
                         dni]
            sql = """UPDATE pacients SET
                   dni = ?
"                  apellidos = ?,
                   estadio = ?,
                   nombre = ? ,
                   nacimiento = ?,
                   notas = ?,
                   telefono = ?,
                   mail = ?,
                   fotocara = ?,
                   fotocuerpo = ?,
                   direccion = ?,
                   peso = ?,
                   genero = ?,
                   fecha_diagnostico = ?,
                   altura = ?
                    WHERE dni = ?"""
        else:
            atributos = [self.apellidos,
                         self.estadio,
                         self.nombre,
                         self.nacimiento,
                         self.notas,
                         self.telefono,
                         self.mail,
                         self.fotocara,
                         self.fotocuerpo,
                         self.direccion,
                         self.peso,
                         self.genero,
                         self.fecha_diagnostico,
                         self.altura,
                         dni]
            sql = """UPDATE pacients SET
                              apellidos = ?,
                               estadio = ?,
                               nombre = ? ,
                               nacimiento = ?,
                               notas = ?,
                               telefono = ?,
                               mail = ?,
                               fotocara = ?,
                               fotocuerpo = ?,
                               direccion = ?,
                               peso = ?,
                               genero = ?,
                               fecha_diagnostico = ?,
                               altura = ?
                                WHERE dni = ?"""
        conexion.execute(sql, atributos)

    def delete(self, conexion):
        conexion.execute(f"DELETE FROM {self.get_tablenames()[0]} WHERE dni = ?", [self.id])
        self.remove()

    @staticmethod
    def get_tablenames() -> tuple:
        return "pacients",

    @staticmethod
    def get_columns_dict() -> tuple:
        columns = ColumnDict()
        columns.add_column("dni", "text", "PRIMARY KEY")
        columns.add_column("nombre", "text")
        columns.add_column("apellidos", "text")
        columns.add_column("estadio", "float")
        columns.add_column("nacimiento", "date")
        columns.add_column("notas", "text")
        columns.add_column("telefono", "text")
        columns.add_column("mail", "text")
        columns.add_column("fotocara", "blob")
        columns.add_column("fotocuerpo", "blob")
        columns.add_column("direccion", "text")
        columns.add_column("peso", "float")
        columns.add_column("genero", "text")
        columns.add_column("fecha_diagnostico", "date")
        columns.add_column("altura", "float")
        return columns,

    def __str__(self):
        return f"{self.id}:{self.apellidos}, {self.nombre}"

    @property
    def nacimiento(self):
        return self._nacimiento

    @nacimiento.setter
    def nacimiento(self, value):
        if isinstance(value, QDate):
            self._nacimiento = value.toPyDate()
        else:
            self._nacimiento = value

    @property
    def fecha_diagnostico(self):
        return self._fecha_diagnostico

    @fecha_diagnostico.setter
    def fecha_diagnostico(self, value):
        if isinstance(value, QDate):
            self._fecha_diagnostico = value.toPyDate()
        else:
            self._fecha_diagnostico = value

    def get_fomatted_name(self):
        string = ""
        if self.apellidos:
            string += self.apellidos
        if self.nombre and string == "":
            string += self.nombre
        elif self.nombre:
            string += ", " + self.nombre
        return string

    def has_fotocara(self):
        return self.fotocara

    def has_fotocuerpo(self):
        return self.fotocuerpo