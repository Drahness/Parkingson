class Entity:

    def __init__(self):
        pass

    def insert(self, conexion):
        raise NotImplementedError()

    def update(self, conexion, to_updated):
        raise NotImplementedError()

    def delete(self, conexion):
        raise NotImplementedError()


class Prueba:
    def __init__(self,
                 identifier: int = None,
                 laps: list = None,
                 pacient_id: str = None,
                 dictionary: dict = None):
        if dictionary is not None:
            identifier = dictionary["identifier"]
            laps = dictionary["laps"]
            pacient_id = dictionary["pacient_id"]
        self.identifier = identifier
        self.laps = laps
        self.pacient_id = pacient_id


class Pacient:
    dni: str
    apellidos: str
    estadio: int
    nombre: str

    def __init__(self,
                 dni: str = None,
                 apellidos: str = None,
                 estadio: int = None,
                 nombre: str = None,
                 dictionary: dict = None):
        if dictionary is not None:
            dni = dictionary["dni"]
            apellidos = dictionary["apellidos"]
            estadio = dictionary["estadio"]
            nombre = dictionary["nombre"]

        self.dni = dni
        self.apellidos = apellidos
        self.estadio = estadio
        self.nombre = nombre

    def insert(self, conexion):
        conexion.insert("INSERT INTO pacients (dni,apellidos,estadio,nombre) VALUES (?,?,?,?)", [self.dni,
                                                                                                 self.apellidos,
                                                                                                 self.estadio,
                                                                                                 self.nombre])

    def update(self, conexion, to_updated):
        to_updated: Pacient
        conexion.execute("UPDATE pacients SET dni = ?, apellidos = ?, estadio = ?, nombre = ? WHERE dni = ?",
                         [to_updated.dni,
                          to_updated.apellidos,
                          to_updated.estadio,
                          to_updated.nombre,
                          self.dni])

    def delete(self, conexion):
        conexion.execute("DELETE FROM pacients WHERE dni = ?", [self.dni])

    def __str__(self):
        return f"{self.dni}:{self.apellidos}, {self.nombre}"


class Usuari:
    username: str
    password: str

    def __init__(self,
                 username: str = None,
                 password: str = None,
                 dictionary: dict = None):
        super().__init__()
        if dictionary is not None:
            username = dictionary["username"]
            password = dictionary["password"]
        self.username = username
        self.password = password

    def __str__(self):
        return f"{self.username}"

    def insert(self, conexion):
        conexion.insert("INSERT INTO pacients (dni,apellidos,estadio,nombre) VALUES (?,?,?,?)", [self.dni,
                                                                                                 self.apellidos,
                                                                                                 self.estadio,
                                                                                                 self.nombre])

    def update(self, conexion, to_updated):
        to_updated: Usuari
        conexion.execute("UPDATE pacients SET dni = ?, apellidos = ?, estadio = ?, nombre = ? WHERE dni = ?",
                         [to_updated.dni,
                          to_updated.apellidos,
                          to_updated.estadio,
                          to_updated.nombre,
                          self.dni])

    def delete(self, conexion):
        conexion.execute("DELETE FROM pacients WHERE dni = ?", [self.dni])
