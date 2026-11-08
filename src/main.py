from src.utils.logger import registrar_evento, registrar_error
from src.excepciones.errores_personalizados import ErrorSistemaFJ

def mostrar_menu():
    print("\n========================================")
    print("   SISTEMA INTEGRAL - SOFTWARE FJ")
    print("========================================")
    print("1. Gestionar Clientes")
    print("2. Gestionar Servicios")
    print("3. Registrar y Administrar Reservas")
    print("4. Ejecutar Simulación de 10 Operaciones")
    print("5. Salir")

def main():
    registrar_evento("Iniciado el Sistema Integral de Gestión Software FJ.")
    print("¡Bienvenido al sistema del grupo!")

    while True:
        try:
            mostrar_menu()
            opcion = input("\nSeleccione una opción: ")

            if opcion == "1":
                print("\n[Módulo de Clientes - A cargo del Integrante 2]")
            elif opcion == "2":
                print("\n[Módulo de Servicios - A cargo del Integrante 3]")
            elif opcion == "3":
                print("\n[Módulo de Reservas - A cargo del Integrante 4]")
            elif opcion == "4":
                ejecutar_simulacion_10_operaciones()
            elif opcion == "5":
                print("\nSaliendo del sistema... ¡Hasta pronto!")
                registrar_evento("El sistema finalizó correctamente.")
                break
            else:
                print("\nOpción no válida. Intente de nuevo.")
                
        except ErrorSistemaFJ as e:
            registrar_error(str(e))
            print(f"\n[Error Controlado]: {e}")
        except Exception as ex:
            registrar_error(f"Error inesperado: {ex}")
            print(f"\n[Error Inesperado]: {ex}")

if __name__ == "__main__":
    main()


    # Brayan Steven Beltran Zuelta
# Simulación de 10 Operaciones - Fase 4 POO
from src.modelos.cliente import GestorClientes
from src.excepciones.errores_personalizados import (
    ClienteInvalidoError,
    ServicioNoDisponibleError,
    ReservaInvalidaError
)
import logging

def ejecutar_simulacion_10_operaciones():
    print("\n" + "="*50)
    print("INICIANDO SIMULACIÓN DE 10 OPERACIONES (LÍDER)")
    print("="*50)
    
    gestor = GestorClientes()
    
    operaciones_exitosas = 0
    operaciones_fallidas = 0

    # Operación 1: Registrar un cliente válido exitosamente
    try:
        print("\n[Op 1] Registrando cliente válido...")
        gestor.registrar(101, "Carlos Andrés", "carlos@correo.com", "3001234567")
        print("-> Éxito: Cliente 101 registrado.")
        operaciones_exitosas += 1
    except Exception as e:
        print(f"-> Error inesperado: {e}")

    # Operación 2: Registrar un segundo cliente válido
    try:
        print("\n[Op 2] Registrando segundo cliente válido...")
        gestor.registrar(102, "Luisa Fernanda", "luisa@correo.com", "3109876543")
        print("-> Éxito: Cliente 102 registrado.")
        operaciones_exitosas += 1
    except Exception as e:
        print(f"-> Error inesperado: {e}")

    # Operación 3: Intentar registrar cliente con nombre inválido (Dispara DatoInvalidoError)
    try:
        print("\n[Op 3] Intentando registrar cliente con nombre muy corto...")
        gestor.registrar(103, "Jo", "jo@correo.com", "3001112222")
    except Exception as e:
        print(f"-> Excepción controlada correctamente: {e}")
        operaciones_fallidas += 1

    # Operación 4: Intentar registrar cliente con correo inválido
    try:
        print("\n[Op 4] Intentando registrar cliente con correo sin '@'...")
        gestor.registrar(104, "Pedro Pérez", "pedro-correo.com", "3001112222")
    except Exception as e:
        print(f"-> Excepción controlada correctamente: {e}")
        operaciones_fallidas += 1

    # Operación 5: Intentar registrar cliente con teléfono de menos de 10 dígitos
    try:
        print("\n[Op 5] Intentando registrar cliente con teléfono incompleto...")
        gestor.registrar(105, "Ana María", "ana@correo.com", "12345")
    except Exception as e:
        print(f"-> Excepción controlada correctamente: {e}")
        operaciones_fallidas += 1

    # Operación 6: Intentar registrar un cliente duplicado (Dispara ClienteDuplicadoError)
    try:
        print("\n[Op 6] Intentando registrar ID duplicado (101)...")
        gestor.registrar(101, "Carlos Repetido", "carlos2@correo.com", "3003334444")
    except Exception as e:
        print(f"-> Excepción controlada correctamente: {e}")
        operaciones_fallidas += 1

    # Operación 7: Buscar un cliente existente con éxito
    try:
        print("\n[Op 7] Buscando cliente existente (102)...")
        cliente = gestor.buscar(102)
        print(f"-> Éxito encontrado: {cliente.describir()}")
        operaciones_exitosas += 1
    except Exception as e:
        print(f"-> Error: {e}")

    # Operación 8: Intentar buscar un cliente que no existe (Dispara ClienteNoEncontradoError)
    try:
        print("\n[Op 8] Buscando cliente inexistente (999)...")
        gestor.buscar(999)
    except Exception as e:
        print(f"-> Excepción controlada correctamente: {e}")
        operaciones_fallidas += 1

    # Operación 9: Disparar manualmente excepción de Servicio No Disponible
    try:
        print("\n[Op 9] Simulando solicitud de servicio no disponible...")
        raise ServicioNoDisponibleError("El servicio técnico de soldadura está ocupado.")
    except ServicioNoDisponibleError as e:
        print(f"-> Excepción de servicio controlada: {e}")
        operaciones_fallidas += 1

    # Operación 10: Disparar manualmente excepción de Reserva Inválida
    try:
        print("\n[Op 10] Simulando error en reserva de cupo...")
        raise ReservaInvalidaError("La fecha seleccionada para la reserva ya pasó.")
    except ReservaInvalidaError as e:
        print(f"-> Excepción de reserva controlada: {e}")
        operaciones_fallidas += 1

    print("\n" + "="*50)
    print(f"FIN DE LA SIMULACIÓN")
    print(f"Operaciones exitosas: {operaciones_exitosas}")
    print(f"Operaciones con excepciones controladas: {operaciones_fallidas}")
    print("="*50 + "\n")
   