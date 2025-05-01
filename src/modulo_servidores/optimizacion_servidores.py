import numpy as np
from pulp import *
import copy

class OptimizacionServidores:
    def __init__(self, servidores, solicitudes):
        # Inicialización con las listas de servidores y solicitudes disponibles
        self.servidores = servidores      # Lista de objetos Servidor disponibles
        self.solicitudes = solicitudes    # Lista de objetos Solicitud a procesar
        self.asignaciones = {}            # Diccionario para almacenar las asignaciones finales
        
        # Ordenar solicitudes por prioridad (menor número = mayor prioridad)
        self.solicitudes.sort(key=lambda s: s.prioridad)


    #Crea una matriz de costos para las solicitudes pendientes y servidores disponibles
    def crear_matriz_costos(self, servidores_disponibles, solicitudes_pendientes):
        
        
        #servidores_disponibles: Lista de servidores con capacidad disponible
        #solicitudes_pendientes: Lista de solicitudes pendientes de asignar
        n_servidores = len(servidores_disponibles)
        n_solicitudes = len(solicitudes_pendientes)
        
        if n_servidores == 0 or n_solicitudes == 0:
            return np.array([]), [], []
        
        # Crear matriz de costos
        matriz_costos = np.zeros((n_servidores, n_solicitudes))
        
        # Mapear índices a los objetos reales
        indices_servidores = [self.servidores.index(s) for s in servidores_disponibles]
        indices_solicitudes = [self.solicitudes.index(s) for s in solicitudes_pendientes]
        
        for i, servidor in enumerate(servidores_disponibles):
            for j, solicitud in enumerate(solicitudes_pendientes):
                # Verificar si el servidor puede procesar la solicitud
                if not servidor.puede_procesar_solicitud(solicitud):
                    matriz_costos[i, j] = float('inf')
                else:
                    # El costo se calcula considerando varios factores:
                    costo_base = solicitud.get_costo_procesamiento(servidor)
                    
                    # Usar la prioridad directamente (menor número = mayor prioridad)
                    factor_prioridad = solicitud.prioridad
                    
                    # Considerar el tiempo máximo de procesamiento
                    factor_tiempo = solicitud.tiempo_maximo_procesamiento
                    
                    # Costo final combinado
                    matriz_costos[i, j] = costo_base * factor_prioridad * factor_tiempo
        
        return matriz_costos, indices_servidores, indices_solicitudes
        
    # Implementa el algoritmo húngaro (Kuhn-Munkres) para problemas de asignación.
    def metodo_hungaro(self, matriz_costos):
        
        if matriz_costos.size == 0:
            return []
            
        # Verificar si hay valores infinitos y reemplazarlos con un número muy grande
        matriz = copy.deepcopy(matriz_costos)
        muy_grande = np.max(matriz[matriz != float('inf')]) * 1000 if np.any(matriz != float('inf')) else 10000
        matriz[matriz == float('inf')] = muy_grande
        
        # El algoritmo húngaro trabaja con matrices cuadradas, así que adaptamos la matriz
        n_filas, n_columnas = matriz.shape
        if n_filas != n_columnas:
            # Crear una matriz cuadrada rellenando con valores grandes
            n_max = max(n_filas, n_columnas)
            matriz_cuadrada = np.ones((n_max, n_max)) * muy_grande
            matriz_cuadrada[:n_filas, :n_columnas] = matriz
            matriz = matriz_cuadrada
            
        # Paso 1: Restar el mínimo de cada fila
        for i in range(matriz.shape[0]):
            min_fila = np.min(matriz[i])
            if min_fila != muy_grande:  # Solo restar si la fila tiene valores válidos
                matriz[i] = matriz[i] - min_fila
                
        # Paso 2: Restar el mínimo de cada columna
        for j in range(matriz.shape[1]):
            min_columna = np.min(matriz[:, j])
            if min_columna != muy_grande:  # Solo restar si la columna tiene valores válidos
                matriz[:, j] = matriz[:, j] - min_columna
        
        # Bucle principal del algoritmo húngaro
        lineas = 0
        n = matriz.shape[0]
        asignaciones = []
        
        while lineas < n:
            # Paso 3: Encontrar el número mínimo de líneas para cubrir todos los ceros
            # Inicializar marcas y cubiertas
            fila_marcada = np.zeros(n, dtype=bool)
            columna_marcada = np.zeros(n, dtype=bool)
            fila_cubierta = np.zeros(n, dtype=bool)
            columna_cubierta = np.zeros(n, dtype=bool)
            
            # Marcar filas sin asignación y propagación
            for i in range(n):
                if not fila_cubierta[i]:
                    self._marcar_fila(matriz, i, fila_marcada, columna_marcada, fila_cubierta, columna_cubierta)
            
            # Cubrir columnas marcadas y filas no marcadas
            for j in range(n):
                if columna_marcada[j]:
                    columna_cubierta[j] = True
            for i in range(n):
                if not fila_marcada[i]:
                    fila_cubierta[i] = True
            
            # Contar líneas usadas
            lineas = np.sum(fila_cubierta) + np.sum(columna_cubierta)
            
            # Si el número de líneas es igual a n, hemos terminado
            if lineas >= n:
                break
                
            # Paso 4: Actualizar la matriz
            # Encontrar el valor mínimo no cubierto
            min_valor = muy_grande
            for i in range(n):
                for j in range(n):
                    if not fila_cubierta[i] and not columna_cubierta[j]:
                        min_valor = min(min_valor, matriz[i, j])
            
            # Restar el mínimo de las filas no cubiertas
            for i in range(n):
                if not fila_cubierta[i]:
                    matriz[i] = matriz[i] - min_valor
            
            # Sumar el mínimo a las columnas cubiertas
            for j in range(n):
                if columna_cubierta[j]:
                    matriz[:, j] = matriz[:, j] + min_valor
        
        # Encontrar la asignación óptima
        for i in range(n):
            for j in range(n):
                if matriz[i, j] == 0 and not any(i == a[0] or j == a[1] for a in asignaciones):
                    # Solo incluimos asignaciones válidas (no ficticias)
                    if i < n_filas and j < n_columnas:
                        if matriz_costos[i, j] != float('inf'):  # Verificar capacidad
                            asignaciones.append((i, j))
        
        # Filtrar las asignaciones para devolver solo las que están dentro de las dimensiones originales
        asignaciones_filtradas = [(i, j) for i, j in asignaciones if i < n_filas and j < n_columnas]
        return asignaciones_filtradas
    
    def _marcar_fila(self, matriz, i, fila_marcada, columna_marcada, fila_cubierta, columna_cubierta):
        # Función auxiliar para el paso 3 del algoritmo húngaro
        fila_marcada[i] = True
        for j in range(matriz.shape[1]):
            if matriz[i, j] == 0 and not columna_cubierta[j]:
                columna_marcada[j] = True
                for k in range(matriz.shape[0]):
                    if matriz[k, j] == 0 and not fila_marcada[k] and not fila_cubierta[k]:
                        self._marcar_fila(matriz, k, fila_marcada, columna_marcada, fila_cubierta, columna_cubierta)

    def resolver_problema_asignacion(self):
        
        print("Aplicando Método Húngaro para la asignación óptima de solicitudes a servidores...")
        
        # Inicializar asignaciones
        asignaciones = {}
        for servidor in self.servidores:
            asignaciones[servidor.id] = []
        
        # Crear copias de las listas para trabajar sobre ellas
        solicitudes_pendientes = self.solicitudes.copy()
        servidores_con_capacidad = self.servidores.copy()
        
        # Ejecutar el algoritmo húngaro iterativamente hasta que no haya más solicitudes
        # o no quede capacidad disponible en los servidores
        ronda = 1
        while solicitudes_pendientes and servidores_con_capacidad:
            print(f"\nRonda {ronda} de asignación:")
            print(f"  Solicitudes pendientes: {len(solicitudes_pendientes)}")
            print(f"  Servidores con capacidad disponible: {len(servidores_con_capacidad)}")
            
            # Crear matriz de costos para esta ronda
            matriz_costos, indices_servidores, indices_solicitudes = self.crear_matriz_costos(
                servidores_con_capacidad, solicitudes_pendientes
            )
            
            # Si no se pudo crear una matriz de costos válida, terminar
            if matriz_costos.size == 0:
                print("  No hay asignaciones posibles en esta ronda.")
                break
            
            # Ejecutar el algoritmo húngaro
            asignaciones_indices = self.metodo_hungaro(matriz_costos)
            
            # Si no se encontraron asignaciones, terminar
            if not asignaciones_indices:
                print("  No se encontraron asignaciones válidas en esta ronda.")
                break
            
            # Procesar las asignaciones encontradas
            for i, j in asignaciones_indices:
                servidor_idx = indices_servidores[i]
                solicitud_idx = indices_solicitudes[j]
                
                servidor = self.servidores[servidor_idx]
                solicitud = self.solicitudes[solicitud_idx]
                
                # Verificar si aún es posible la asignación
                if not servidor.puede_procesar_solicitud(solicitud):
                    continue
                
                # Realizar la asignación
                asignaciones[servidor.id].append(solicitud.id)
                solicitud.asignar_servidor(servidor)
                servidor.asignar_solicitud(solicitud)
                
                print(f"  Asignando solicitud {solicitud.id} ({solicitud.nombre}, Prioridad {solicitud.get_prioridad_texto()}) al servidor {servidor.id}")
                
                # Eliminar la solicitud de la lista de pendientes
                solicitudes_pendientes.remove(solicitud)
            
            # Actualizar la lista de servidores con capacidad disponible
            servidores_con_capacidad = [s for s in self.servidores if any(s.puede_procesar_solicitud(sol) for sol in solicitudes_pendientes)]
            
            ronda += 1
        
        # Buscar solicitudes no asignadas
        solicitudes_no_asignadas = [s for s in self.solicitudes if not s.asignada]
        if solicitudes_no_asignadas:
            print("\nADVERTENCIA: Las siguientes solicitudes no pudieron ser asignadas debido a restricciones de capacidad:")
            for solicitud in solicitudes_no_asignadas:
                print(f"- Solicitud {solicitud.id}: {solicitud.nombre} (Prioridad: {solicitud.get_prioridad_texto()})")
        
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

    def calcular_tiempo_total_procesamiento(self):
        """
        Calcula el tiempo total de procesamiento basado en las asignaciones realizadas.
        """
        tiempo_total = 0
        for servidor_id, solicitudes_ids in self.asignaciones.items():
            servidor = next(s for s in self.servidores if s.id == servidor_id)
            for solicitud_id in solicitudes_ids:
                solicitud = next(s for s in self.solicitudes if s.id == solicitud_id)
                # El tiempo de procesamiento es proporcional al costo
                tiempo_procesamiento = solicitud.get_costo_procesamiento(servidor)
                tiempo_total += tiempo_procesamiento
        return tiempo_total

    def generar_reporte(self):
        # Genera un reporte detallado de las asignaciones y estadísticas de balance
        reporte = "\n=== Reporte de Asignación de Servidores ===\n\n"
        
        # Primero muestra las asignaciones para cada servidor
        reporte += "Asignaciones por Servidor:\n"
        for servidor_id, solicitudes_ids in self.asignaciones.items():
            servidor = next(s for s in self.servidores if s.id == servidor_id)
            reporte += f"\n{servidor}\n"
            
            if not solicitudes_ids:
                reporte += "  No se asignaron solicitudes a este servidor.\n"
                continue
                
            reporte += "Solicitudes asignadas:\n"
            
            # Detalles de cada solicitud asignada a este servidor
            for solicitud_id in solicitudes_ids:
                solicitud = next(s for s in self.solicitudes if s.id == solicitud_id)
                costo = solicitud.get_costo_procesamiento(servidor)
                reporte += f"  - {solicitud.nombre} (Prioridad: {solicitud.get_prioridad_texto()})\n"
                reporte += f"    Costo de procesamiento: {costo:.2f}\n"
                reporte += f"    Tiempo máximo: {solicitud.tiempo_maximo_procesamiento:.2f} segundos\n"
        
        # Tiempo total de procesamiento
        tiempo_total = self.calcular_tiempo_total_procesamiento()
        reporte += f"\nTiempo total de procesamiento: {tiempo_total:.2f} unidades\n"
        
        # Luego muestra estadísticas sobre el balance de carga
        balance = self.calcular_balance_carga()
        reporte += "\nBalance de Carga:\n"
        for recurso, stats in balance.items():
            reporte += f"\n{recurso.capitalize()}:\n"
            reporte += f"  Promedio de utilización: {stats['promedio']:.1f}%\n"
            reporte += f"  Desviación estándar: {stats['desviacion']:.1f}%\n"
        
        # Verificación de cumplimiento de prioridades
        reporte += "\nVerificación de Prioridades:\n"
        # Agrupar solicitudes por prioridad
        por_prioridad = {}
        for solicitud in self.solicitudes:
            if solicitud.prioridad not in por_prioridad:
                por_prioridad[solicitud.prioridad] = []
            por_prioridad[solicitud.prioridad].append(solicitud)
        
        # Mostrar estado por nivel de prioridad
        for prioridad in sorted(por_prioridad.keys()):
            solicitudes = por_prioridad[prioridad]
            asignadas = sum(1 for s in solicitudes if s.asignada)
            total = len(solicitudes)
            reporte += f"  Prioridad {prioridad} ({next(s for s in solicitudes).get_prioridad_texto()}): {asignadas}/{total} asignadas\n"
        
        return reporte 