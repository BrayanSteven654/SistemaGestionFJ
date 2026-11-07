#Karina Andrea Palomo
#213023A_2204
#Ingenieria en Sistemas
#Codigo fuente: autoria propia

# clientes.py
from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    filename="logs.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class ErrorCliente(Exception):
    pass


class DatoInvalidoError(ErrorCliente):
    pass


class ClienteDuplicadoError(ErrorCliente):
    pass


class ClienteNoEncontradoError(ErrorCliente):
    pass


class Entidad(ABC):
    def __init__(self, id):
        self._id = id

    @property
    def id(self):
        return self._id

    @abstractmethod
    def describir(self):
        pass


class Cliente(Entidad):
    def __init__(self, id, nombre, correo, telefono):
        super().__init__(id)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError("Nombre inválido")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor:
            raise DatoInvalidoError("Correo inválido")
        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not str(valor).isdigit() or len(str(valor)) != 10:
            raise DatoInvalidoError("Teléfono inválido (10 dígitos)")
        self._telefono = str(valor)

    def describir(self):
        return f"Cliente {self.id}: {self.nombre} | {self.correo} | {self.telefono}"

    def actualizar(self, nombre=None, correo=None, telefono=None):
        if nombre is not None:
            self.nombre = nombre
        if correo is not None:
            self.correo = correo
        if telefono is not None:
            self.telefono = telefono


class GestorClientes:
    def __init__(self):
        self._clientes = []

    def registrar(self, id, nombre, correo, telefono):
        try:
            if self.buscar(id, silencioso=True):
                raise ClienteDuplicadoError(f"Ya existe el cliente {id}")
            cliente = Cliente(id, nombre, correo, telefono)
        except DatoInvalidoError as e:
            logging.error(f"Error al registrar cliente {id}: {e}")
            raise ErrorCliente("No se pudo registrar el cliente") from e
        except ClienteDuplicadoError as e:
            logging.error(e)
            raise
        else:
            self._clientes.append(cliente)
            logging.info(f"Cliente registrado: {id}")
            return cliente
        finally:
            logging.info(f"Intento de registro finalizado: {id}")

    def buscar(self, id, silencioso=False):
        for c in self._clientes:
            if c.id == id:
                return c
        if silencioso:
            return None
        logging.error(f"Cliente no encontrado: {id}")
        raise ClienteNoEncontradoError(f"No existe el cliente {id}")

    def eliminar(self, id):
        cliente = self.buscar(id)
        self._clientes.remove(cliente)
        logging.info(f"Cliente eliminado: {id}")

    def listar(self):
        return [c.describir() for c in self._clientes]


if __name__ == "__main__":
    gestor = GestorClientes()

    pruebas = [
        (1, "Ana Pérez", "ana@correo.com", "3001234567"),
        (2, "Luis Gómez", "luis@correo.com", "3109876543"),
        (3, "Jo", "jo@correo.com", "3001112222"),
        (4, "Carlos Ruiz", "carlos-correo.com", "3001112222"),
        (5, "María Díaz", "maria@correo.com", "123"),
        (1, "Ana Repetida", "ana2@correo.com", "3001234567"),
    ]

    for datos in pruebas:
        try:
            c = gestor.registrar(*datos)
            print("OK:", c.describir())
        except ErrorCliente as e:
            print("Error:", e, "| Causa:", e.__cause__)

    try:
        gestor.buscar(99)
    except ClienteNoEncontradoError as e:
        print("Error:", e)

    try:
        gestor.buscar(1).actualizar(correo="nuevo@correo.com")
        gestor.buscar(2).actualizar(telefono="abc")
    except ErrorCliente as e:
        logging.error(e)
        print("Error:", e)

    print(gestor.listar())
