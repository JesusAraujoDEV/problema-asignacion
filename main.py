import sys
from src.modulo_asignacion.main_asignacion import main as main_asignacion
from src.modulo_servidores.main_servidores import main as main_servidores

def mostrar_menu():
    """
    Muestra el menú principal de opciones al usuario y captura su selección.
    
    Returns:
        str: La opción seleccionada por el usuario.
    """
    print("\n=== Sistema de Asignación y Optimización ===")
    print("1. Módulo de Asignación de Programadores")
    print("2. Módulo de Optimización de Servidores")
    print("3. Ejecutar ambos módulos")
    print("4. Salir")
    
    # Validación de la entrada del usuario
    while True:
        try:
            opcion = input("Seleccione una opción (1-4): ")
            if opcion in ["1", "2", "3", "4"]:
                return opcion
            else:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 4.")
        except KeyboardInterrupt:
            # Manejar la interrupción de teclado (Ctrl+C)
            print("\n\nOperación cancelada por el usuario.")
            return "4"  # Devolver la opción de salir
        except Exception as e:
            print(f"Error inesperado: {str(e)}")
            print("Por favor, intente nuevamente.")

def main():
    """
    Función principal que controla el flujo del programa.
    Muestra el menú, procesa la selección del usuario y ejecuta los módulos correspondientes.
    """
    try:
        while True:
            # Obtener la opción seleccionada por el usuario
            opcion = mostrar_menu()
            
            # Procesar la opción seleccionada
            if opcion == "1":
                # Ejecuta solo el módulo de asignación de programadores
                print("\nEjecutando Módulo de Asignación de Programadores...")
                try:
                    main_asignacion()
                except Exception as e:
                    print(f"\nError en el módulo de asignación: {str(e)}")
                    print("Volviendo al menú principal...")
            elif opcion == "2":
                # Ejecuta solo el módulo de optimización de servidores
                print("\nEjecutando Módulo de Optimización de Servidores...")
                try:
                    main_servidores()
                except Exception as e:
                    print(f"\nError en el módulo de servidores: {str(e)}")
                    print("Volviendo al menú principal...")
            elif opcion == "3":
                # Ejecuta ambos módulos secuencialmente
                print("\nEjecutando ambos módulos...")
                try:
                    main_asignacion()
                    print("\n" + "="*50 + "\n")  # Separador visual entre módulos
                    main_servidores()
                except Exception as e:
                    print(f"\nError al ejecutar los módulos: {str(e)}")
                    print("Volviendo al menú principal...")
            elif opcion == "4":
                # Termina la ejecución del programa
                print("\n¡Hasta luego!")
                sys.exit(0)
    except KeyboardInterrupt:
        # Manejar la interrupción global (Ctrl+C)
        print("\n\nPrograma interrumpido por el usuario.")
        print("¡Hasta luego!")
        sys.exit(0)
    except Exception as e:
        # Capturar cualquier otra excepción no manejada
        print(f"\nError inesperado en el programa principal: {str(e)}")
        print("El programa se cerrará.")
        sys.exit(1)

if __name__ == "__main__":
    # Punto de entrada del programa cuando se ejecuta directamente
    main() 