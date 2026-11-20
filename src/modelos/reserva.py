from src.utils.logger import registrar_evento, registrar_error
from src.modelos.entidad_base import Entidad
from src.modelos.cliente import Cliente
from src.modelos.servicio import Servicio
from src.excepciones.errores_personalizados import (
    ErrorSistemaFJ,
    ClienteInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError,
)


class Reserva(Entidad):
    # Estados posibles de la reserva
    PENDIENTE = "PENDIENTE"
    CONFIRMADA = "CONFIRMADA"
    CANCELADA = "CANCELADA"

    def __init__(self, id_reserva, cliente, servicio, duracion):
        super().__init__(id_reserva)
        try:
            # Validar que el cliente y el servicio sean correctos
            if not isinstance(cliente, Cliente):
                raise ClienteInvalidoError("La reserva necesita un cliente válido.")
            if not isinstance(servicio, Servicio):
                raise ServicioNoDisponibleError("La reserva necesita un servicio válido.")
            if not getattr(servicio, "disponible", True):
                raise ServicioNoDisponibleError("El servicio no está disponible.")

            # Validar la duración (horas)
            try:
                duracion = float(duracion)
                if duracion <= 0:
                    raise ValueError()
            except (TypeError, ValueError) as e:
                raise ReservaInvalidaError("La duración debe ser un número mayor a 0.") from e
        except ErrorSistemaFJ as e:
            registrar_error(f"Reserva {id_reserva} inválida: {e}")
            raise

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = Reserva.PENDIENTE
        registrar_evento(f"Reserva {id_reserva} creada.")

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    def confirmar(self):
        try:
            if self._estado != Reserva.PENDIENTE:
                raise ReservaInvalidaError(
                    f"No se puede confirmar una reserva {self._estado}.")
        except ReservaInvalidaError as e:
            registrar_error(f"Reserva {self.id}: {e}")
            raise
        else:
            self._estado = Reserva.CONFIRMADA
            registrar_evento(f"Reserva {self.id} confirmada.")
        finally:
            registrar_evento(f"Fin del intento de confirmar la reserva {self.id}.")

    def cancelar(self):
        try:
            if self._estado == Reserva.CANCELADA:
                raise ReservaInvalidaError("La reserva ya estaba cancelada.")
        except ReservaInvalidaError as e:
            registrar_error(f"Reserva {self.id}: {e}")
            raise
        else:
            self._estado = Reserva.CANCELADA
            registrar_evento(f"Reserva {self.id} cancelada.")

    # Sobrecarga: se puede llamar sin parámetros, con descuento o con impuesto
    def calcular_costo(self, descuento=0, impuesto=0):
        costo = self._servicio.calcular_costo_total() * self._duracion
        costo = costo - (costo * descuento) + (costo * impuesto)
        if costo < 0:
            raise ReservaInvalidaError("El costo calculado es inconsistente.")
        return round(costo, 2)

    def procesar(self, descuento=0, impuesto=0.19):
        try:
            if self._estado != Reserva.CONFIRMADA:
                raise ReservaInvalidaError("Solo se procesan reservas confirmadas.")
            total = self.calcular_costo(descuento, impuesto)
        except ErrorSistemaFJ as e:
            registrar_error(f"Reserva {self.id}: {e}")
            raise
        except Exception as e:
            registrar_error(f"Error al procesar la reserva {self.id}: {e}")
            raise ReservaInvalidaError("No se pudo procesar la reserva.") from e
        else:
            registrar_evento(f"Reserva {self.id} procesada. Total: {total:.2f}")
            return total

    def describir(self):
        return (f"Reserva {self.id}: {self._cliente.nombre} | "
                f"{self._servicio.nombre} | {self._duracion} h | {self._estado}")
