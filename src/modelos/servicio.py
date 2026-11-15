from abc import ABC, abstractmethod
from src.utils.logger import registrar_evento, registrar_error
from src.excepciones.errores_personalizados import ErrorSistemaFJ

# 1. Clase Abstracta Base
class Servicio(ABC):
    def __init__(self, id_servicio, nombre, costo_base):
        self.id_servicio = id_servicio
        self.nombre = nombre
        self.costo_base = float(costo_base)

    @abstractmethod
    def calcular_costo_total(self):
        """Método abstracto que aplicará polimorfismo en las clases hijas."""
        pass

# 2. Clase Derivada 1: Salas
class ServicioSala(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, capacidad_personas):
        super().__init__(id_servicio, nombre, costo_base)
        self.capacidad_personas = int(capacidad_personas)

    def calcular_costo_total(self):

        # Sobrecarga/lógica: Si la sala es grande (más de 10 personas), aplica un recargo del 15%
        recargo = 1.15 if self.capacidad_personas > 10 else 1.0
        return self.costo_base * recargo

# 3. Clase Derivada 2: Equipos
class ServicioEquipo(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, horas_alquiler):
        super().__init__(id_servicio, nombre, costo_base)
        self.horas_alquiler = float(horas_alquiler)

    def calcular_costo_total(self):
        # El costo total depende de las horas de alquiler
        return self.costo_base * self.horas_alquiler

# 4. Clase Derivada 3: Asesorías
class ServicioAsesoria(Servicio):
    def __init__(self, id_servicio, nombre, costo_base, nivel_complejidad):
        super().__init__(id_servicio, nombre, costo_base)
        self.nivel_complejidad = nivel_complejidad.strip().lower()

    def calcular_costo_total(self):
        # Sobrecarga según complejidad ('alta' aumenta un 30%)
        if self.nivel_complejidad == "alta":
            return self.costo_base * 1.30
        return self.costo_base

# Gestor para administrar los servicios con try-except
class GestorServicios:
    def __init__(self):
        self.servicios = []

    def registrar_servicio(self, tipo, id_s, nombre, costo_txt, extra_txt):
        try:
            if not id_s.strip() or not nombre.strip():
                raise ValueError("El ID y el nombre del servicio no pueden estar vacíos.")
            
            try:
                costo = float(costo_txt)
                if costo <= 0:
                    raise ValueError("El costo base debe ser mayor a cero.")
            except ValueError:
                raise ValueError("El costo ingresado debe ser un número válido.")

            # Validar duplicados
            for s in self.servicios:
                if s.id_servicio == id_s.strip():
                    raise ErrorSistemaFJ(f"Ya existe un servicio con el ID '{id_s}'.")

            # Instanciar según el tipo seleccionado con su respectivo try-except
            if tipo == "Sala":
                try:
                    extra = int(extra_txt)
                    if extra <= 0: raise ValueError()
                except ValueError:
                    raise ValueError("La capacidad de personas debe ser un número entero positivo.")
                nuevo = ServicioSala(id_s.strip(), nombre.strip(), costo, extra)

            elif tipo == "Equipo":
                try:
                    extra = float(extra_txt)
                    if extra <= 0: raise ValueError()
                except ValueError:
                    raise ValueError("Las horas de alquiler deben ser un número mayor a cero.")
                nuevo = ServicioEquipo(id_s.strip(), nombre.strip(), costo, extra)

            elif tipo == "Asesoría":
                if extra_txt.strip().lower() not in ["normal", "alta"]:
                    raise ValueError("La complejidad debe ser 'normal' o 'alta'.")
                nuevo = ServicioAsesoria(id_s.strip(), nombre.strip(), costo, extra_txt)
            else:
                raise ValueError("Tipo de servicio no válido.")

            self.servicios.append(nuevo)
            registrar_evento(f"Servicio {tipo} registrado exitosamente: {nombre}.")
            return nuevo

        except (ValueError, ErrorSistemaFJ) as e:
            registrar_error(f"Error al registrar servicio: {str(e)}")
            raise
        except Exception as e:
            registrar_error(f"Error crítico en servicio: {str(e)}")
            raise ErrorSistemaFJ("Error interno al procesar el servicio.")