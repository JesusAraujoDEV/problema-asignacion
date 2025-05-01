import os
import sys
from modulo_asignacion_programadores import MainProgramadores
from modulo_asignacion_servidores import MainServidores

class MenuPrincipal:
    def __init__(self):
        pass

    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        os.system('cls' if os.name == 'nt' else 'clear')

    def mostrar_banner(self):
        """Muestra un banner decorativo para el programa."""
        print("=" * 70)
        print("                SISTEMA DE OPTIMIZACIÓN DE RECURSOS                ")
        print("=" * 70)
        print("  Desarrollado para resolver problemas de programación lineal")
        print("  Métodos implementados: Transporte y Húngaro")
        print("-" * 70)

    def validar_opcion(self,mensaje, opciones_validas):
        
        while True:
            try:
                opcion = input(mensaje)
                if opcion in opciones_validas:
                    return opcion
                else:
                    print(f"Error: Opción no válida. Las opciones válidas son: {', '.join(opciones_validas)}")
            except Exception as e:
                print(f"Error inesperado: {str(e)}. Por favor, intente de nuevo.")

    def mostrar_menu_principal(self):
        """Muestra el menú principal del programa."""
        print("\nMÓDULOS DISPONIBLES:")
        print("1. Asignación de Programadores a Tareas con Restricciones de Transporte")
        print("2. Optimización de la Asignación de Solicitudes a Servidores")
        print("0. Salir")
        
        return self.validar_opcion("\nSeleccione una opción (0-2): ", ['0', '1', '2'])

    def main(self):
        """Función principal que ejecuta el programa."""
        while True:
            self.limpiar_pantalla()
            self.mostrar_banner()
            opcion = self.mostrar_menu_principal()
            
            if opcion == '1':
                self.limpiar_pantalla()
                print("=" * 70)
                print("      MÓDULO DE ASIGNACIÓN DE PROGRAMADORES A TAREAS      ")
                print("=" * 70)
                try:
                    MainProgramadores().main()
                except Exception as e:
                    print(f"\nError al ejecutar el módulo: {str(e)}")
                input("\nPresione Enter para volver al menú principal...")
                
            elif opcion == '2':
                self.limpiar_pantalla()
                print("=" * 70)
                print("      MÓDULO DE ASIGNACIÓN DE SOLICITUDES A SERVIDORES      ")
                print("=" * 70)
                try:
                    MainServidores().main()
                except Exception as e:
                    print(f"\nError al ejecutar el módulo: {str(e)}")
                input("\nPresione Enter para volver al menú principal...")
                
            elif opcion == '0':
                self.limpiar_pantalla()
                print("Gracias por utilizar el Sistema de Optimización de Recursos.")
                print("¡Hasta pronto!")
                sys.exit(0)

if __name__ == "__main__":
    try:
        MenuPrincipal().main()
    except KeyboardInterrupt:
        print("\n\nPrograma interrumpido por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        sys.exit(1)
