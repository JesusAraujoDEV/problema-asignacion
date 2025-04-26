import numpy as np
from pulp import *

class OptimizacionServidores:
    def __init__(self, servidores, solicitudes):
        self.servidores = servidores
        self.solicitudes = solicitudes
        self.asignaciones = {}  # Diccionario para almacenar las asignaciones finales

    def crear_matriz_costos(self):
        n_servidores = len(self.servidores)
        n_solicitudes = len(self.solicitudes)
        matriz_costos = np.zeros((n_servidores, n_solicitudes))

        for i, servidor in enumerate(self.servidores):
            for j, solicitud in enumerate(self.solicitudes):
                # Costo base de procesamiento
                costo_base = solicitud.get_costo_procesamiento(servidor)
                
                # Factor de prioridad (mayor prioridad = menor costo)
                factor_prioridad = 1 / solicitud.prioridad
                
                # Factor de tiempo (tiempo más corto = menor costo)
                factor_tiempo = 1 / solicitud.tiempo_maximo_procesamiento
                
                # Costo ponderado
                matriz_costos[i][j] = costo_base * factor_prioridad * factor_tiempo

        return matriz_costos

    def resolver_problema_asignacion(self):
        # Crear el problema de optimización
        prob = LpProblem("Asignacion_Servidores", LpMinimize)

        # Crear variables de decisión
        x = {}
        for i, servidor in enumerate(self.servidores):
            for j, solicitud in enumerate(self.solicitudes):
                x[i, j] = LpVariable(f"x_{i}_{j}", 0, 1, LpInteger)

        # Función objetivo
        matriz_costos = self.crear_matriz_costos()
        prob += lpSum(matriz_costos[i][j] * x[i, j] 
                     for i in range(len(self.servidores))
                     for j in range(len(self.solicitudes)))

        # Restricciones de capacidad de servidores
        for i, servidor in enumerate(self.servidores):
            for j, solicitud in enumerate(self.solicitudes):
                if not servidor.puede_procesar_solicitud(solicitud):
                    prob += x[i, j] == 0

        # Restricciones de asignación única
        for j, solicitud in enumerate(self.solicitudes):
            prob += lpSum(x[i, j] for i in range(len(self.servidores))) == 1

        # Resolver el problema
        prob.solve()

        # Procesar resultados
        asignaciones = {}
        for i, servidor in enumerate(self.servidores):
            for j, solicitud in enumerate(self.solicitudes):
                if x[i, j].value() == 1:
                    if servidor.id not in asignaciones:
                        asignaciones[servidor.id] = []
                    asignaciones[servidor.id].append(solicitud.id)
                    solicitud.asignar_servidor(servidor)
                    servidor.asignar_solicitud(solicitud)

        self.asignaciones = asignaciones
        return asignaciones

    def calcular_balance_carga(self):
        utilizaciones = []
        for servidor in self.servidores:
            utilizacion = servidor.get_utilizacion_recursos()
            utilizaciones.append({
                'servidor': servidor.id,
                'cpu': utilizacion['cpu'],
                'memoria': utilizacion['memoria'],
                'ancho_banda': utilizacion['ancho_banda']
            })

        # Calcular promedios y desviaciones estándar
        stats = {
            'cpu': {
                'promedio': np.mean([u['cpu'] for u in utilizaciones]),
                'desviacion': np.std([u['cpu'] for u in utilizaciones])
            },
            'memoria': {
                'promedio': np.mean([u['memoria'] for u in utilizaciones]),
                'desviacion': np.std([u['memoria'] for u in utilizaciones])
            },
            'ancho_banda': {
                'promedio': np.mean([u['ancho_banda'] for u in utilizaciones]),
                'desviacion': np.std([u['ancho_banda'] for u in utilizaciones])
            }
        }

        return stats

    def generar_reporte(self):
        reporte = "=== Reporte de Asignación de Servidores ===\n\n"
        
        # Asignaciones por servidor
        reporte += "Asignaciones por Servidor:\n"
        for servidor_id, solicitudes_ids in self.asignaciones.items():
            servidor = next(s for s in self.servidores if s.id == servidor_id)
            reporte += f"\n{servidor}\n"
            reporte += "Solicitudes asignadas:\n"
            
            for solicitud_id in solicitudes_ids:
                solicitud = next(s for s in self.solicitudes if s.id == solicitud_id)
                costo = solicitud.get_costo_procesamiento(servidor)
                reporte += f"  - {solicitud.nombre} (Prioridad: {solicitud.get_prioridad_texto()})\n"
                reporte += f"    Costo de procesamiento: {costo:.2f}\n"
                reporte += f"    Tiempo máximo: {solicitud.tiempo_maximo_procesamiento:.2f} segundos\n"
        
        # Balance de carga
        balance = self.calcular_balance_carga()
        reporte += "\nBalance de Carga:\n"
        for recurso, stats in balance.items():
            reporte += f"\n{recurso.capitalize()}:\n"
            reporte += f"  Promedio de utilización: {stats['promedio']:.1f}%\n"
            reporte += f"  Desviación estándar: {stats['desviacion']:.1f}%\n"
        
        return reporte 