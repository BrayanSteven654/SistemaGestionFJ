import logging
import os
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/sistema_errores.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def registrar_evento(mensaje):
    """Registra un evento exitoso o informativo."""
    logging.info(mensaje)

def registrar_error(mensaje):
    """Registra una excepción o error controlado en el sistema."""
    logging.error(mensaje)