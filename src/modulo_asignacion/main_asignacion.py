from .programador import Programador
from .tarea import Tarea
from .asignacion_transporte import AsignacionTransporte

def crear_datos_ejemplo():
    # Creación de los programadores de ejemplo con sus capacidades
    # Vector S[N] - capacidad máxima de tareas por programador:
    programadores = [
        Programador(1, "Jesus", 2),  # Jesus puede asumir hasta 2 tareas
        Programador(2, "Luffy", 3),  # Luffy puede asumir hasta 3 tareas
        Programador(3, "Sanji", 2),  # Sanji puede asumir hasta 2 tareas
        Programador(4, "Messi", 2)   # Messi puede asumir hasta 2 tareas
    ]

    # Creación de las tareas con sus ubicaciones y programadores requeridos
    # Vector D[M] - programadores requeridos por tarea:
    tareas = [
        Tarea(1, "Desarrollo Web", "Caracas", 2),     # Requiere 2 programadores
        Tarea(2, "Base de Datos", "Valencia", 1),     # Requiere 1 programador
        Tarea(3, "Testing", "Maracay", 2),            # Requiere 2 programadores
        Tarea(4, "DevOps", "Barquisimeto", 1)         # Requiere 1 programador
    ]

    # Matriz de costos de desempeño para cada programador en cada tarea
    # Estos valores representan la eficiencia de cada programador para cada tipo de tarea
    # Valores más bajos indican mejor desempeño
    costos_desempeno = {
        1: {1: 5, 2: 7, 3: 6, 4: 8},  # Costos para Jesus
        2: {1: 6, 2: 5, 3: 7, 4: 6},  # Costos para Luffy
        3: {1: 7, 2: 6, 3: 5, 4: 7},  # Costos para Sanji
        4: {1: 6, 2: 8, 3: 6, 4: 5}   # Costos para Messi
    }

    #Matriz de costos de asignación y transporte C[N][M]:
    
    # Matriz de costos de transporte para cada programador a cada ubicación de tarea
    # Representa la distancia o tiempo de viaje desde la ubicación del programador
    costos_transporte = {
        1: {1: 2, 2: 3, 3: 4, 4: 5},  # Costos para Jesus
        2: {1: 3, 2: 2, 3: 3, 4: 4},  # Costos para Luffy
        3: {1: 4, 2: 3, 3: 2, 4: 3},  # Costos para Sanji
        4: {1: 5, 2: 4, 3: 3, 4: 2}   # Costos para Messi
    }

    # Asignación de los costos a cada objeto programador y tarea
    for prog in programadores:
        for tarea in tareas:
            prog.agregar_costo_transporte(tarea.id, costos_transporte[prog.id][tarea.id])
            tarea.agregar_costo_desempeno(prog.id, costos_desempeno[prog.id][tarea.id])

    return programadores, tareas

def leer_entero_positivo(mensaje, minimo=1):
    
    while True:
        try:
            valor = int(input(mensaje))
            if valor < minimo:
                print(f"Error: El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Error: Debe ingresar un número entero válido.")

def leer_float_positivo(mensaje, minimo=0):
    
    while True:
        try:
            valor = float(input(mensaje))
            if valor < minimo:
                print(f"Error: El valor debe ser mayor o igual a {minimo}.")
                continue
            return valor
        except ValueError:
            print("Error: Debe ingresar un número decimal válido.")

def ingresar_datos_por_consola():
    
    try:
        print("\n=== Ingreso de datos para el problema de asignación ===")
        
        # Leer número de programadores y tareas
        n_programadores = leer_entero_positivo("Ingrese el número de programadores (N): ")
        n_tareas = leer_entero_positivo("Ingrese el número de tareas (M): ")
        
        # Crear programadores
        print("\n--- Datos de los programadores ---")
        programadores = []
        for i in range(1, n_programadores + 1):
            print(f"\nProgramador {i}:")
            nombre = input(f"Nombre del programador {i}: ")
            while not nombre.strip():
                print("Error: El nombre no puede estar vacío.")
                nombre = input(f"Nombre del programador {i}: ")
                
            capacidad = leer_entero_positivo(f"Capacidad máxima de tareas para {nombre}: ")
            programadores.append(Programador(i, nombre, capacidad))
        
        # Crear tareas
        print("\n--- Datos de las tareas ---")
        tareas = []
        for j in range(1, n_tareas + 1):
            print(f"\nTarea {j}:")
            nombre = input(f"Nombre de la tarea {j}: ")
            while not nombre.strip():
                print("Error: El nombre no puede estar vacío.")
                nombre = input(f"Nombre de la tarea {j}: ")
                
            ubicacion = input(f"Ubicación de la tarea {j}: ")
            while not ubicacion.strip():
                print("Error: La ubicación no puede estar vacía.")
                ubicacion = input(f"Ubicación de la tarea {j}: ")
                
            requeridos = leer_entero_positivo(f"Programadores requeridos para la tarea {j}: ")
            tareas.append(Tarea(j, nombre, ubicacion, requeridos))
        
        # Verificar si hay suficientes programadores
        total_capacidad = sum(prog.capacidad_maxima for prog in programadores)
        total_requeridos = sum(tarea.programadores_requeridos for tarea in tareas)
        
        if total_capacidad < total_requeridos:
            print("\nADVERTENCIA: La capacidad total de los programadores es menor que los requerimientos totales.")
            print(f"Capacidad total: {total_capacidad}, Requerimiento total: {total_requeridos}")
            if input("¿Desea continuar de todos modos? (s/n): ").lower() != 's':
                print("Operación cancelada. Volviendo al menú principal.")
                return None, None
        
        # Ingresar costos de desempeño y transporte
        print("\n--- Costos de desempeño ---")
        for prog in programadores:
            for tarea in tareas:
                costo = leer_float_positivo(
                    f"Costo de desempeño de {prog.nombre} en la tarea {tarea.nombre}: "
                )
                tarea.agregar_costo_desempeno(prog.id, costo)
        
        print("\n--- Costos de transporte ---")
        for prog in programadores:
            for tarea in tareas:
                costo = leer_float_positivo(
                    f"Costo de transporte de {prog.nombre} a {tarea.ubicacion} (tarea {tarea.nombre}): "
                )
                prog.agregar_costo_transporte(tarea.id, costo)
        
        return programadores, tareas
        
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
        return None, None
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        return None, None

def main():
    print("\n=== Módulo de Asignación de Programadores a Tareas ===")
    
    # Preguntar si usar datos de ejemplo o ingresar datos
    opcion = ""
    while opcion not in ['1', '2']:
        print("\nSeleccione una opción:")
        print("1. Usar datos de ejemplo")
        print("2. Ingresar datos manualmente")
        opcion = input("Opción (1-2): ")
        if opcion not in ['1', '2']:
            print("Opción no válida. Intente nuevamente.")
    
    # Obtener los datos según la opción elegida
    if opcion == '1':
        programadores, tareas = crear_datos_ejemplo()
    else:
        programadores, tareas = ingresar_datos_por_consola()
        
    # Verificar si se obtuvieron datos válidos
    if programadores is None or tareas is None or len(programadores) == 0 or len(tareas) == 0:
        print("\nNo hay datos suficientes para realizar la optimización.")
        return
    
    # Inicializamos y resolvemos el problema de asignación
    try:
        print("\nResolviendo el problema de asignación...")
        asignacion = AsignacionTransporte(programadores, tareas)
        asignacion.resolver_problema_transporte()  # Ejecuta el algoritmo de optimización
        
        # Generamos un reporte detallado con los resultados
        reporte = asignacion.generar_reporte()
        print(reporte)  # Mostramos el reporte en consola
    except Exception as e:
        print(f"\nError al resolver el problema de optimización: {str(e)}")

if __name__ == "__main__":
    main() 