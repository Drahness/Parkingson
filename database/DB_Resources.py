def get_db_model_users():
    from database.models import UsuariListModel
    return UsuariListModel.get_instance()


def get_db_model_pacients():
    from database.models import PacientsListModel
    return PacientsListModel.get_instance()


def get_db_model_pruebas():
    from database.models import PruebasListModel
    return PruebasListModel.get_instance()


def get_entity_pacient(dni: str = None,
                       apellidos: str = None,
                       estadio: int = None,
                       nombre: str = None,
                       dictionary: dict = None):
    from database.entities import Pacient
    return Pacient(dni, apellidos, estadio, nombre, dictionary)


def get_entity_usuari(username: str = None,
                      password: str = None,
                      dictionary: dict = None):
    from database.entities import Usuari
    return Usuari(username, password, dictionary)


def get_entity_prueba(identifier: int = None,
                      laps: list = None,
                      pacient_id: str = None,
                      dictionary: dict = None):
    from database.entities import Prueba
    return Prueba(identifier, laps, pacient_id, dictionary)


def get_default_path():
    return "db"


def get_default_dbname():
    return "default.db"


def get_db_connection(path: str = get_default_path(), dbname: str = get_default_dbname()):
    from database.database_controller import Connection
    return Connection.get_instance(path, dbname)
