import numpy as np
from pulp import *

class AsignacionTransporte:
    def __init__(self, programadores, tareas):
        self.programadores = programadores
        self.tareas = tareas
        self.asignaciones = {}  # Diccionario para almacenar las asignaciones finales

    def crear_matriz_costos(self):
        n_programadores = len(self.programadores)
        n_tareas = len(self.tareas)
        matriz_costos = np.zeros((n_programadores, n_tareas))

        for i, prog in enumerate(self.programadores):
            for j, tarea in enumerate(self.tareas):
                costo_desempeno = tarea.get_costo_desempeno(prog.id)
                costo_transporte = prog.get_costo_transporte(tarea.id)
                matriz_costos[i][j] = costo_desempeno + costo_transporte

        return matriz_costos

    def resolver_problema_transporte(self):
        # Crear el problema de optimización
        prob = LpProblem("Asignacion_Transporte", LpMinimize)

        # Crear variables de decisión
        x = {}
        for i, prog in enumerate(self.programadores):
            for j, tarea in enumerate(self.tareas):
                x[i, j] = LpVariable(f"x_{i}_{j}", 0, 1, LpInteger)

        # Función objetivo
        matriz_costos = self.crear_matriz_costos()
        prob += lpSum(matriz_costos[i][j] * x[i, j] 
                     for i in range(len(self.programadores))
                     for j in range(len(self.tareas)))

        # Restricciones de capacidad de programadores
        for i, prog in enumerate(self.programadores):
            prob += lpSum(x[i, j] for j in range(len(self.tareas))) <= prog.capacidad_maxima

        # Restricciones de requerimientos de tareas
        for j, tarea in enumerate(self.tareas):
            prob += lpSum(x[i, j] for i in range(len(self.programadores))) == tarea.programadores_requeridos

        # Resolver el problema
        prob.solve()

        # Procesar resultados
        asignaciones = {}
        for i, prog in enumerate(self.programadores):
            for j, tarea in enumerate(self.tareas):
                if x[i, j].value() == 1:
                    if prog.id not in asignaciones:
                        asignaciones[prog.id] = []
                    asignaciones[prog.id].append(tarea.id)

        self.asignaciones = asignaciones
        return asignaciones

    def calcular_costo_total(self):
        costo_total = 0
        for prog_id, tareas_ids in self.asignaciones.items():
            programador = next(p for p in self.programadores if p.id == prog_id)
            for tarea_id in tareas_ids:
                tarea = next(t for t in self.tareas if t.id == tarea_id)
                costo_total += (tarea.get_costo_desempeno(prog_id) + 
                              programador.get_costo_transporte(tarea_id))
        return costo_total

    def generar_reporte(self):
        reporte = "=== Reporte de Asignaciones ===\n\n"
        
        for prog_id, tareas_ids in self.asignaciones.items():
            programador = next(p for p in self.programadores if p.id == prog_id)
            reporte += f"{programador}\n"
            
            for tarea_id in tareas_ids:
                tarea = next(t for t in self.tareas if t.id == tarea_id)
                costo_desempeno = tarea.get_costo_desempeno(prog_id)
                costo_transporte = programador.get_costo_transporte(tarea_id)
                costo_total = costo_desempeno + costo_transporte
                
                reporte += f"  - {tarea.nombre} en {tarea.ubicacion}\n"
                reporte += f"    Costo desempeño: {costo_desempeno}\n"
                reporte += f"    Costo transporte: {costo_transporte}\n"
                reporte += f"    Costo total: {costo_total}\n"
            
            reporte += "\n"
        
        reporte += f"Costo total de la asignación: {self.calcular_costo_total()}\n"
        return reporte 