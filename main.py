import sys
from src.modulo_asignacion.main_asignacion import main as main_asignacion
from src.modulo_servidores.main_servidores import main as main_servidores

def mostrar_menu():
    print("\n=== Sistema de Asignación y Optimización ===")
    print("1. Módulo de Asignación de Programadores")
    print("2. Módulo de Optimización de Servidores")
    print("3. Ejecutar ambos módulos")
    print("4. Salir")
    return input("Seleccione una opción (1-4): ")

def main():
    while True:
        opcion = mostrar_menu()
        
        if opcion == "1":
            print("\nEjecutando Módulo de Asignación de Programadores...")
            main_asignacion()
        elif opcion == "2":
            print("\nEjecutando Módulo de Optimización de Servidores...")
            main_servidores()
        elif opcion == "3":
            print("\nEjecutando ambos módulos...")
            main_asignacion()
            print("\n" + "="*50 + "\n")
            main_servidores()
        elif opcion == "4":
            print("\n¡Hasta luego!")
            sys.exit(0)
        else:
            print("\nOpción no válida. Por favor, seleccione una opción del 1 al 4.")

if __name__ == "__main__":
    main() 