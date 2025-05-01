import numpy as np
from scipy.optimize import linear_sum_assignment
import os

class AsignacionSolicitudesServidores:
    def __init__(self, num_servidores, num_solicitudes, matriz_costos, prioridades=None, capacidades=None):
        
        self.num_servidores = num_servidores # Número de servidores disponibles
        self.num_solicitudes = num_solicitudes # Número de solicitudes a procesar
        self.matriz_costos = np.array(matriz_costos) # Matriz de costos C[S][R] donde cada elemento C[i][j]
        self.prioridades = prioridades if prioridades is not None else np.ones(num_solicitudes) # Vector de prioridades para cada solicitud (valores más bajos indican mayor prioridad)
        self.capacidades = capacidades if capacidades is not None else np.ones(num_servidores) * float('inf') # Vector de capacidades para cada servidor
        
        # Ajustar la matriz de costos según las prioridades
        self.matriz_costos_ajustada = self.ajustar_costos_por_prioridad()
        
        # Resultados
        self.asignaciones = None
        self.tiempo_total = None
        self.carga_servidores = None

    def ajustar_costos_por_prioridad(self):
        
        matriz_ajustada = self.matriz_costos.copy()
        
        # Normalizar prioridades para que estén entre 0 y 1
        if np.max(self.prioridades) > 0:
            prioridades_norm = self.prioridades / np.max(self.prioridades)
        else:
            prioridades_norm = self.prioridades
            
        # Ajustar cada columna (solicitud) según su prioridad
        for j in range(self.num_solicitudes):
            # Factor de ajuste: solicitudes con mayor prioridad (valor más bajo) tienen un factor menor
            factor = 1 + (1 - prioridades_norm[j])
            matriz_ajustada[:, j] = matriz_ajustada[:, j] / factor
            
        return matriz_ajustada

    def hacer_matriz_cuadrada(self):
        """
        Hace que la matriz de costos sea cuadrada para aplicar el método húngaro.
        Si hay más servidores que solicitudes, se agregan solicitudes ficticias.
        Si hay más solicitudes que servidores, se agregan servidores ficticios.
        """
        if self.num_servidores == self.num_solicitudes:
            return self.matriz_costos_ajustada
        
        elif self.num_servidores > self.num_solicitudes:
            # Agregar solicitudes ficticias con costo alto
            padding = np.full((self.num_servidores, self.num_servidores - self.num_solicitudes), 0)
            return np.hstack([self.matriz_costos_ajustada, padding])
        
        else:  # self.num_servidores < self.num_solicitudes
            # Agregar servidores ficticios con costo alto
            padding = np.full((self.num_solicitudes - self.num_servidores, self.num_solicitudes), 1e6)
            return np.vstack([self.matriz_costos_ajustada, padding])

    def resolver_metodo_hungaro(self):
        
        # Hacer la matriz cuadrada
        matriz_cuadrada = self.hacer_matriz_cuadrada()
        
        # Aplicar el método húngaro
        filas_ind, cols_ind = linear_sum_assignment(matriz_cuadrada)
        
        # Filtrar asignaciones válidas (no ficticias)
        self.asignaciones = []
        self.carga_servidores = np.zeros(self.num_servidores)
        
        for i, j in zip(filas_ind, cols_ind):
            if i < self.num_servidores and j < self.num_solicitudes:
                self.asignaciones.append((i, j, self.matriz_costos[i][j]))
                self.carga_servidores[i] += 1
        
        # Calcular tiempo total de procesamiento
        self.tiempo_total = sum(costo for _, _, costo in self.asignaciones)
        
        return self.asignaciones, self.tiempo_total, self.carga_servidores

    def verificar_restricciones(self):
        """
        Verifica si la solución cumple con las restricciones de capacidad y prioridad.
        """
        if self.asignaciones is None:
            return
            
        # Verificar restricciones de capacidad
        capacidad_excedida = False
        for i in range(self.num_servidores):
            if self.carga_servidores[i] > self.capacidades[i]:
                capacidad_excedida = True
                break
        
        # Verificar restricciones de prioridad
        # Comprobar si las solicitudes de mayor prioridad fueron asignadas a servidores más rápidos
        prioridad_violada = False
        asignaciones_por_solicitud = {j: (i, costo) for i, j, costo in self.asignaciones}
        
        for j1 in range(self.num_solicitudes):
            if j1 not in asignaciones_por_solicitud:
                continue
                
            for j2 in range(self.num_solicitudes):
                if j2 not in asignaciones_por_solicitud or j1 == j2:
                    continue
                    
                # Si j1 tiene mayor prioridad que j2 (valor más bajo)
                if self.prioridades[j1] < self.prioridades[j2]:
                    i1, costo1 = asignaciones_por_solicitud[j1]
                    i2, costo2 = asignaciones_por_solicitud[j2]
                    
                    # Verificar si la solicitud de mayor prioridad tiene un tiempo de procesamiento mayor
                    if costo1 > costo2:
                        prioridad_violada = True
                        break
            
            if prioridad_violada:
                break
        
        return {
            'capacidad_excedida': capacidad_excedida,
            'prioridad_violada': prioridad_violada
        }

    def generar_reporte(self):
        """
        Genera un reporte detallado de la optimización.
        """
        if self.asignaciones is None:
            return "Debe resolver el problema primero."
        
        reporte = "REPORTE DE ASIGNACIÓN DE SOLICITUDES A SERVIDORES\n"
        reporte += "=" * 50 + "\n\n"
        
        reporte += "RESUMEN:\n"
        reporte += f"- Número de servidores: {self.num_servidores}\n"
        reporte += f"- Número de solicitudes: {self.num_solicitudes}\n"
        reporte += f"- Tiempo total de procesamiento: {self.tiempo_total}\n\n"
        
        # Verificar restricciones
        restricciones = self.verificar_restricciones()
        if restricciones:
            reporte += "VERIFICACIÓN DE RESTRICCIONES:\n"
            reporte += f"- Capacidad excedida: {'Sí' if restricciones.get('capacidad_excedida', False) else 'No'}\n"
            reporte += f"- Prioridad violada: {'Sí' if restricciones.get('prioridad_violada', False) else 'No'}\n\n"
        
        reporte += "ASIGNACIONES DETALLADAS:\n"
        reporte += "-" * 50 + "\n"
        reporte += f"{'Servidor':<10} | {'Solicitud':<10} | {'Tiempo':<10} | {'Prioridad':<10}\n"
        reporte += "-" * 50 + "\n"
        
        for servidor, solicitud, tiempo in self.asignaciones:
            reporte += f"{servidor:<10} | {solicitud:<10} | {tiempo:<10.2f} | {self.prioridades[solicitud]:<10.2f}\n"
        
        reporte += "-" * 50 + "\n\n"
        
        # Análisis de carga de trabajo
        reporte += "DISTRIBUCIÓN DE CARGA DE TRABAJO:\n"
        reporte += "-" * 50 + "\n"
        reporte += f"{'Servidor':<10} | {'Solicitudes asignadas':<20} | {'% de carga':<10}\n"
        reporte += "-" * 50 + "\n"
        
        total_solicitudes = sum(self.carga_servidores)
        for i in range(self.num_servidores):
            porcentaje = (self.carga_servidores[i] / total_solicitudes * 100) if total_solicitudes > 0 else 0
            reporte += f"{i:<10} | {int(self.carga_servidores[i]):<20} | {porcentaje:<10.2f}%\n"
        
        return reporte
    

class MainServidores:
    def __init__(self):
        pass

    def leer_datos_consola(self):
        print("=== MÓDULO DE ASIGNACIÓN DE SOLICITUDES A SERVIDORES ===")
        
        # Validar número de servidores
        while True:
            try:
                S = int(input("Ingrese el número de servidores (S): "))
                if S <= 0:
                    print("Debe ingresar un número entero positivo.")
                    continue
                break
            except ValueError:
                print("Entrada inválida. Ingrese un número entero válido.")

        # Validar número de solicitudes
        while True:
            try:
                R = int(input("Ingrese el número de solicitudes (R): "))
                if R <= 0:
                    print("Debe ingresar un número entero positivo.")
                    continue
                break
            except ValueError:
                print("Entrada inválida. Ingrese un número entero válido.")

        # Matriz de costos
        print("\nIngrese la matriz de costos C[S][R] (tiempos de procesamiento):")
        C = []
        for i in range(S):
            while True:
                try:
                    fila = list(map(float, input(f"Tiempos para servidor {i}: ").strip().split()))
                    if len(fila) != R:
                        print(f"Error: Se esperaban {R} valores.")
                        continue
                    if any(x < 0 for x in fila):
                        print("Error: Los tiempos de procesamiento deben ser no negativos.")
                        continue
                    C.append(fila)
                    break
                except ValueError:
                    print("Error: Ingrese solo números reales separados por espacios.")

        # Prioridades
        prioridades = None
        usar_prioridades = input("\n¿Desea ingresar prioridades para las solicitudes? (s/n): ")
        if usar_prioridades.lower() == 's':
            while True:
                try:
                    prioridades = list(map(float, input("Prioridades (separadas por espacios): ").strip().split()))
                    if len(prioridades) != R:
                        print(f"Error: Se esperaban {R} valores.")
                        continue
                    if any(p < 0 for p in prioridades):
                        print("Error: Las prioridades deben ser no negativas.")
                        continue
                    break
                except ValueError:
                    print("Error: Ingrese solo números reales separados por espacios.")

        # Capacidades
        capacidades = None
        usar_capacidades = input("\n¿Desea ingresar capacidades para los servidores? (s/n): ")
        if usar_capacidades.lower() == 's':
            while True:
                try:
                    capacidades = list(map(int, input("Capacidades (separadas por espacios): ").strip().split()))
                    if len(capacidades) != S:
                        print(f"Error: Se esperaban {S} valores.")
                        continue
                    if any(c <= 0 for c in capacidades):
                        print("Error: Las capacidades deben ser enteros positivos.")
                        continue
                    break
                except ValueError:
                    print("Error: Ingrese solo números enteros separados por espacios.")
        
        return S, R, C, prioridades, capacidades


    def leer_datos_archivo(self,ruta):
        
        with open(ruta, 'r') as f:
            lineas = [line.strip() for line in f.readlines() if line.strip()]
            
            S = int(lineas[0])  # Número de servidores
            R = int(lineas[1])  # Número de solicitudes
            
            # Leer matriz de costos
            C = []
            for i in range(2, 2 + S):
                fila = list(map(float, lineas[i].split()))
                if len(fila) != R:
                    raise ValueError(f"Error: La fila {i-2} de la matriz de costos tiene {len(fila)} valores, se esperaban {R}.")
                C.append(fila)
            
            # Verificar si hay más líneas para prioridades y capacidades
            prioridades = None
            capacidades = None
            
            if len(lineas) > 2 + S:
                # Leer prioridades
                prioridades = list(map(float, lineas[2 + S].split()))
                if len(prioridades) != R:
                    raise ValueError(f"Error: Se esperaban {R} valores para las prioridades.")
            
            if len(lineas) > 3 + S:
                # Leer capacidades
                capacidades = list(map(int, lineas[3 + S].split()))
                if len(capacidades) != S:
                    raise ValueError(f"Error: Se esperaban {S} valores para las capacidades.")
            
            return S, R, C, prioridades, capacidades

    def main(self):
        """
        Función principal que ejecuta el módulo de asignación de solicitudes a servidores.
        """
        print("¿Cómo desea ingresar los datos?\n1. Consola\n2. Archivo")
        opcion = input("Seleccione una opción (1 o 2): ")
        
        try:
            if opcion == '1':
                S, R, C, prioridades, capacidades = self.leer_datos_consola()
            elif opcion == '2':
                ruta = input("Ingrese la ruta del archivo: ")
                carpeta_actual = os.path.dirname(os.path.abspath(__file__))
                ruta_completa = os.path.join(carpeta_actual, ruta)
                
                if not os.path.exists(ruta_completa):
                    print(f"Error: El archivo {ruta} no existe.")
                    return
                
                S, R, C, prioridades, capacidades = self.leer_datos_archivo(ruta_completa)
            else:
                print("Opción no válida.")
                return
            
            # Crear instancia del problema
            problema = AsignacionSolicitudesServidores(S, R, C, prioridades, capacidades)
            
            # Resolver con el método húngaro
            print("\nResolviendo con el método húngaro...")
            asignaciones, tiempo_total, carga_servidores = problema.resolver_metodo_hungaro()
            
            # Mostrar resultados
            print("\n=== RESULTADOS DE LA OPTIMIZACIÓN ===")
            print(f"Tiempo total de procesamiento: {tiempo_total}")
            print(f"Número total de asignaciones: {len(asignaciones)}")
            
            # Mostrar distribución de carga
            print("\nDistribución de carga por servidor:")
            for i in range(S):
                print(f"Servidor {i}: {int(carga_servidores[i])} solicitudes")
            
            # Verificar restricciones
            restricciones = problema.verificar_restricciones()
            if restricciones:
                print("\nVerificación de restricciones:")
                print(f"- Capacidad excedida: {'Sí' if restricciones.get('capacidad_excedida', False) else 'No'}")
                print(f"- Prioridad violada: {'Sí' if restricciones.get('prioridad_violada', False) else 'No'}")
            
            # Preguntar si se desea ver el reporte detallado
            ver_reporte = input("\n¿Desea ver el reporte detallado? (s/n): ")
            if ver_reporte.lower() == 's':
                reporte = problema.generar_reporte()
                print("\n" + reporte)
            
            # Preguntar si se desea guardar el reporte
            guardar_reporte = input("\n¿Desea guardar el reporte en un archivo? (s/n): ")
            if guardar_reporte.lower() == 's':
                nombre_archivo = input("Ingrese el nombre del archivo (sin extensión): ")
                with open(f"{nombre_archivo}.txt", 'w') as f:
                    f.write(problema.generar_reporte())
                print(f"Reporte guardado en {nombre_archivo}.txt")
            
        except Exception as e:
            print(f"Error: {str(e)}")

