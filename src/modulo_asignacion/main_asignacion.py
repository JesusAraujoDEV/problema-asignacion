from .programador import Programador
from .tarea import Tarea
from .asignacion_transporte import AsignacionTransporte

def crear_datos_ejemplo():
    # Crear programadores
    programadores = [
        Programador(1, "Jesus", 2),
        Programador(2, "Luffy", 3),
        Programador(3, "Sanji", 2),
        Programador(4, "Messi", 2)
    ]

    # Crear tareas
    tareas = [
        Tarea(1, "Desarrollo Web", "Caracas", 2),
        Tarea(2, "Base de Datos", "Valencia", 1),
        Tarea(3, "Testing", "Maracay", 2),
        Tarea(4, "DevOps", "Barquisimeto", 1)
    ]

    # Asignar costos de desempeño
    costos_desempeno = {
        1: {1: 5, 2: 7, 3: 6, 4: 8},  # Costos para Jesus
        2: {1: 6, 2: 5, 3: 7, 4: 6},  # Costos para Luffy
        3: {1: 7, 2: 6, 3: 5, 4: 7},  # Costos para Sanji
        4: {1: 6, 2: 8, 3: 6, 4: 5}   # Costos para Messi
    }

    # Asignar costos de transporte
    costos_transporte = {
        1: {1: 2, 2: 3, 3: 4, 4: 5},  # Costos para Jesus
        2: {1: 3, 2: 2, 3: 3, 4: 4},  # Costos para Luffy
        3: {1: 4, 2: 3, 3: 2, 4: 3},  # Costos para Sanji
        4: {1: 5, 2: 4, 3: 3, 4: 2}   # Costos para Messi
    }

    # Asignar costos a programadores y tareas
    for prog in programadores:
        for tarea in tareas:
            prog.agregar_costo_transporte(tarea.id, costos_transporte[prog.id][tarea.id])
            tarea.agregar_costo_desempeno(prog.id, costos_desempeno[prog.id][tarea.id])

    return programadores, tareas

def main():
    print("\n=== Módulo de Asignación de Programadores a Tareas ===")
    
    # Crear datos de ejemplo
    programadores, tareas = crear_datos_ejemplo()
    
    # Crear y resolver el problema de asignación
    asignacion = AsignacionTransporte(programadores, tareas)
    asignacion.resolver_problema_transporte()
    
    # Generar y mostrar el reporte
    reporte = asignacion.generar_reporte()
    print(reporte)

if __name__ == "__main__":
    main() 