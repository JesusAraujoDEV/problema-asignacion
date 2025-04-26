import numpy as np
from pulp import *

class OptimizacionServidores:
    def __init__(self, servidores, solicitudes):
        # Inicialización con las listas de servidores y solicitudes disponibles
        self.servidores = servidores      # Lista de objetos Servidor disponibles
        self.solicitudes = solicitudes    # Lista de objetos Solicitud a procesar
        self.asignaciones = {}            # Diccionario para almacenar las asignaciones finales

    def crear_matriz_costos(self):
        # Crea una matriz de costos ponderados para cada combinación servidor-solicitud
        n_servidores = len(self.servidores)
        n_solicitudes = len(self.solicitudes)
        matriz_costos = np.zeros((n_servidores, n_solicitudes))

        for i, servidor in enumerate(self.servidores):
            for j, solicitud in enumerate(self.solicitudes):
                # El costo se calcula considerando varios factores:
                
                # Costo base de procesamiento del servidor para esta solicitud
                costo_base = solicitud.get_costo_procesamiento(servidor)
                
                # Factor de prioridad: solicitudes de mayor prioridad (número menor) tienen menor costo
                factor_prioridad = 1 / solicitud.prioridad
                
                # Factor de tiempo: solicitudes con menor tiempo máximo tienen preferencia (menor costo)
                factor_tiempo = 1 / solicitud.tiempo_maximo_procesamiento
                
                # Ponderación final del costo
                matriz_costos[i][j] = costo_base * factor_prioridad * factor_tiempo

        return matriz_costos

    def resolver_problema_asignacion(self):
        # Resuelve el problema de asignación usando programación lineal
        # Crear el problema de optimización
        prob = LpProblem("Asignacion_Servidores", LpMinimize)

        # Crear variables de decisión binarias (0-1)
        # x[i,j] = 1 si la solicitud j es asignada al servidor i, 0 en caso contrario
        x = {}
        for i, servidor in enumerate(self.servidores):
            for j, solicitud in enumerate(self.solicitudes):
                x[i, j] = LpVariable(f"x_{i}_{j}", 0, 1, LpInteger)

        # Función objetivo: minimizar el costo total ponderado de las asignaciones
        matriz_costos = self.crear_matriz_costos()
        prob += lpSum(matriz_costos[i][j] * x[i, j] 
                     for i in range(len(self.servidores))
                     for j in range(len(self.solicitudes)))

        # Restricción: no asignar solicitudes a servidores sin capacidad suficiente
        for i, servidor in enumerate(self.servidores):
            for j, solicitud in enumerate(self.solicitudes):
                if not servidor.puede_procesar_solicitud(solicitud):
                    prob += x[i, j] == 0

        # Restricción: cada solicitud debe ser asignada exactamente a un servidor
        for j, solicitud in enumerate(self.solicitudes):
            prob += lpSum(x[i, j] for i in range(len(self.servidores))) == 1

        # Resolver el problema utilizando el solucionador por defecto
        prob.solve()

        # Procesar resultados y actualizar objetos con las asignaciones
        asignaciones = {}
        for i, servidor in enumerate(self.servidores):
            for j, solicitud in enumerate(self.solicitudes):
                # Si la variable binaria es 1, se hace la asignación
                if x[i, j].value() == 1:
                    if servidor.id not in asignaciones:
                        asignaciones[servidor.id] = []
                    asignaciones[servidor.id].append(solicitud.id)
                    # Actualizamos el estado de la solicitud y del servidor
                    solicitud.asignar_servidor(servidor)
                    servidor.asignar_solicitud(solicitud)

        self.asignaciones = asignaciones
        return asignaciones

    def calcular_balance_carga(self):
        # Calcula estadísticas sobre el balance de carga entre los servidores
        # Recopila datos de utilización para cada servidor
        utilizaciones = []
        for servidor in self.servidores:
            utilizacion = servidor.get_utilizacion_recursos()
            utilizaciones.append({
                'servidor': servidor.id,
                'cpu': utilizacion['cpu'],
                'memoria': utilizacion['memoria'],
                'ancho_banda': utilizacion['ancho_banda']
            })

        # Calcula el promedio y la desviación estándar para cada tipo de recurso
        # Una menor desviación estándar indica un mejor balance de carga
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
        # Genera un reporte detallado de las asignaciones y estadísticas de balance
        reporte = "=== Reporte de Asignación de Servidores ===\n\n"
        
        # Primero muestra las asignaciones para cada servidor
        reporte += "Asignaciones por Servidor:\n"
        for servidor_id, solicitudes_ids in self.asignaciones.items():
            servidor = next(s for s in self.servidores if s.id == servidor_id)
            reporte += f"\n{servidor}\n"
            reporte += "Solicitudes asignadas:\n"
            
            # Detalles de cada solicitud asignada a este servidor
            for solicitud_id in solicitudes_ids:
                solicitud = next(s for s in self.solicitudes if s.id == solicitud_id)
                costo = solicitud.get_costo_procesamiento(servidor)
                reporte += f"  - {solicitud.nombre} (Prioridad: {solicitud.get_prioridad_texto()})\n"
                reporte += f"    Costo de procesamiento: {costo:.2f}\n"
                reporte += f"    Tiempo máximo: {solicitud.tiempo_maximo_procesamiento:.2f} segundos\n"
        
        # Luego muestra estadísticas sobre el balance de carga
        balance = self.calcular_balance_carga()
        reporte += "\nBalance de Carga:\n"
        for recurso, stats in balance.items():
            reporte += f"\n{recurso.capitalize()}:\n"
            reporte += f"  Promedio de utilización: {stats['promedio']:.1f}%\n"
            reporte += f"  Desviación estándar: {stats['desviacion']:.1f}%\n"
        
        return reporte 