class Model:
    def __init__(self, __id: str or int):
        self._id = __id
        self.tablename: str

    @staticmethod
    def get_table_structure(self):
        raise NotImplementedError()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id: str or int):
        self._id = id

    @staticmethod
    def get_tablename():
        raise NotImplementedError()

class Usuari(Model):
    password: str  # Hexidigest
    username: str

    def __init__(self,
                 username: str = None,
                 password: str = None):
        super(Usuari, self).__init__(username)
        self.username = username
        self.password = password

    @staticmethod
    def get_table_structure():
        return """CREATE TABLE users ( username VARCHAR, password VARCHAR )"""

    @staticmethod
    def get_tablename():
        return "users"

class Pacients(Model):
    def __init__(self,
                 dni: str = None,
                 apellido: str = None,
                 apellido2: str = None,
                 estadio: int = None,
                 nombre: str = None):
        super(Pacients, self).__init__(dni)
        self.dni = dni
        self.apellido1 = apellido
        self.apellido2 = apellido2
        self.estadio = estadio
        self.nombre = nombre

    @staticmethod
    def get_table_structure():
        return """CREATE TABLE pacients ( name VARCHAR,
dni VARCHAR,
apellido1 VARCHAR,
apellido2 VARCHAR,
estadio tinyint );"""

    @staticmethod
    def get_tablename():
        return "pacients"
