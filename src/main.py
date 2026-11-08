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
        mostrar_menu()
        opcion = input("\nSeleccione una opción: ")
        
        try:
            if opcion == "1":
                print("\n[Módulo de Clientes - A cargo del Integrante 2]")
            elif opcion == "2":
                print("\n[Módulo de Servicios - A cargo del Integrante 3]")
            elif opcion == "3":
                print("\n[Módulo de Reservas - A cargo del Integrante 4]")
            elif opcion == "4":
                print("\n[Simulación de 10 Operaciones - A cargo del Líder]")
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
    