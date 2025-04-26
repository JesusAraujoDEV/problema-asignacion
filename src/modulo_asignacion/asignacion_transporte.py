import numpy as np
from pulp import *

class AsignacionTransporte:
    def __init__(self, programadores, tareas):
        # Inicialización con las listas de programadores y tareas disponibles
        self.programadores = programadores  # Lista de objetos Programador
        self.tareas = tareas                # Lista de objetos Tarea
        self.asignaciones = {}              # Diccionario para almacenar las asignaciones finales

    def crear_matriz_costos(self):
        # Crea una matriz con los costos totales de asignar cada programador a cada tarea
        n_programadores = len(self.programadores)
        n_tareas = len(self.tareas)
        matriz_costos = np.zeros((n_programadores, n_tareas))

        for i, prog in enumerate(self.programadores):
            for j, tarea in enumerate(self.tareas):
                # El costo total es la suma del costo de desempeño y el costo de transporte
                costo_desempeno = tarea.get_costo_desempeno(prog.id)
                costo_transporte = prog.get_costo_transporte(tarea.id)
                matriz_costos[i][j] = costo_desempeno + costo_transporte

        return matriz_costos

    def resolver_problema_transporte(self):
        # Resuelve el problema de asignación usando programación lineal
        # Crear el problema de optimización
        prob = LpProblem("Asignacion_Transporte", LpMinimize)

        # Crear variables de decisión binarias (0-1)
        # x[i,j] = 1 si el programador i es asignado a la tarea j, 0 en caso contrario
        x = {}
        for i, prog in enumerate(self.programadores):
            for j, tarea in enumerate(self.tareas):
                x[i, j] = LpVariable(f"x_{i}_{j}", 0, 1, LpInteger)

        # Función objetivo: minimizar el costo total de las asignaciones
        matriz_costos = self.crear_matriz_costos()
        prob += lpSum(matriz_costos[i][j] * x[i, j] 
                     for i in range(len(self.programadores))
                     for j in range(len(self.tareas)))

        # Restricciones de capacidad: cada programador no puede exceder su capacidad máxima
        for i, prog in enumerate(self.programadores):
            prob += lpSum(x[i, j] for j in range(len(self.tareas))) <= prog.capacidad_maxima

        # Restricciones de requerimientos: cada tarea debe tener exactamente los programadores requeridos
        for j, tarea in enumerate(self.tareas):
            prob += lpSum(x[i, j] for i in range(len(self.programadores))) == tarea.programadores_requeridos

        # Resolver el problema utilizando el solucionador por defecto
        prob.solve()

        # Procesar resultados y guardar las asignaciones
        asignaciones = {}
        for i, prog in enumerate(self.programadores):
            for j, tarea in enumerate(self.tareas):
                # Si la variable binaria es 1, se hace la asignación
                if x[i, j].value() == 1:
                    if prog.id not in asignaciones:
                        asignaciones[prog.id] = []
                    asignaciones[prog.id].append(tarea.id)

        self.asignaciones = asignaciones
        return asignaciones

    def calcular_costo_total(self):
        # Calcula el costo total de todas las asignaciones realizadas
        costo_total = 0
        for prog_id, tareas_ids in self.asignaciones.items():
            programador = next(p for p in self.programadores if p.id == prog_id)
            for tarea_id in tareas_ids:
                tarea = next(t for t in self.tareas if t.id == tarea_id)
                # Suma el costo de desempeño y transporte para cada asignación
                costo_total += (tarea.get_costo_desempeno(prog_id) + 
                              programador.get_costo_transporte(tarea_id))
        return costo_total

    def generar_reporte(self):
        # Genera un reporte detallado de las asignaciones y sus costos
        reporte = "=== Reporte de Asignaciones ===\n\n"
        
        # Para cada programador, muestra sus tareas asignadas y los costos asociados
        for prog_id, tareas_ids in self.asignaciones.items():
            programador = next(p for p in self.programadores if p.id == prog_id)
            reporte += f"{programador}\n"
            
            for tarea_id in tareas_ids:
                tarea = next(t for t in self.tareas if t.id == tarea_id)
                costo_desempeno = tarea.get_costo_desempeno(prog_id)
                costo_transporte = programador.get_costo_transporte(tarea_id)
                costo_total = costo_desempeno + costo_transporte
                
                # Detalles de cada asignación
                reporte += f"  - {tarea.nombre} en {tarea.ubicacion}\n"
                reporte += f"    Costo desempeño: {costo_desempeno}\n"
                reporte += f"    Costo transporte: {costo_transporte}\n"
                reporte += f"    Costo total: {costo_total}\n"
            
            reporte += "\n"
        
        # Añade el costo total de todas las asignaciones
        reporte += f"Costo total de la asignación: {self.calcular_costo_total()}\n"
        return reporte 