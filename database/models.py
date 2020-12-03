class Model:
    def __init__(self, __id: str or int):
        self.id = __id

    def get_table_structure(self):
        pass

class Usuari:
    def __init__(self,
                 username: str = None,
                 password: str = None):
        self.username = username
        self.password = password

    @staticmethod
    def get_table_structure():
        return """CREATE TABLE users ( username VARCHAR(50), password VARCHAR(?)"""


class Pacients:
    def __init__(self,
                 dni: str = None,
                 apellido: str = None,
                 apellido2: str = None,
                 estadio: int = None,
                 nombre: str = None):
        self.dni = dni
        self.apellido1 = apellido
        self.apellido2 = apellido2
        self.estadio = estadio
        self.nombre = nombre

    @staticmethod
    def get_table_structure():
        return """CREATE TABLE pacients ( name VARCHAR(20),
dni VARCHAR(9),
apellido1 VARCHAR(20),
apellido2 VARCHAR(20),
estadio tinyint );"""
