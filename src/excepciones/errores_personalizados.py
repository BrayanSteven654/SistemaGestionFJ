# Brayan Steven Beltran Zuelta
# 213023A_2204
# Ingenieria en Sistemas
# Codigo fuente: autoria propia

class ErrorSistemaFJ(Exception):
    """Clase base para todas las excepciones del Sistema FJ."""
    def __init__(self, mensaje="Ha ocurrido un error en el Sistema FJ."):
        super().__init__(mensaje)


class ClienteInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando los datos del cliente no cumplen las validaciones."""
    def __init__(self, mensaje="Error: Los datos del cliente son inválidos o incompletos."):
        super().__init__(mensaje)


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta solicitar un servicio no disponible."""
    def __init__(self, mensaje="Error: El servicio seleccionado no está disponible."):
        super().__init__(mensaje)


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza cuando una operación de reserva falla o tiene parámetros incorrectos."""
    def __init__(self, mensaje="Error: La operación de reserva no pudo ser procesada."):
        super().__init__(mensaje)
