import pandas as pd
from pulp import *
import numpy as np
import os

class AsignacionProgramadoresTareas:

    def __init__(self, num_programadores, num_tareas, matriz_costos, capacidad_programadores, demanda_tareas):
        
        self.num_programadores = num_programadores # num_programadores (int): Número de programadores disponibles
        self.num_tareas = num_tareas # num_tareas (int): Número de tareas a realizar
        self.matriz_costos = matriz_costos # Matriz de costos C[N][M]
        self.capacidad_programadores = capacidad_programadores # Vector S[N] que indica la cantidad máxima de tareas 
        self.demanda_tareas = demanda_tareas # Vector D[M] que indica la cantidad de programadores requeridos por cada tarea
        
        # Crear identificadores para programadores y tareas
        self.programadores = [f'Programador_{i}' for i in range(num_programadores)]
        self.tareas = [f'Tarea_{j}' for j in range(num_tareas)]
        
        # Convertir listas a diccionarios para compatibilidad con PuLP
        self.oferta = {self.programadores[i]: capacidad_programadores[i] for i in range(num_programadores)}
        self.demanda = {self.tareas[j]: demanda_tareas[j] for j in range(num_tareas)}
        
        # Crear matriz de costos como diccionario de diccionarios
        self.costo_asignacion = {}
        for i in range(num_programadores):
            self.costo_asignacion[self.programadores[i]] = {}
            for j in range(num_tareas):
                self.costo_asignacion[self.programadores[i]][self.tareas[j]] = matriz_costos[i][j]

        # Balancear si es necesario
        self.balancear_oferta_demanda()
        
        # Inicializar el problema de optimización
        self.prob = LpProblem('AsignacionProgramadoresTareas', LpMinimize)
        self.asignaciones = None
        self.costo_total = None


    def balancear_oferta_demanda(self):
        """
        Balancea el problema de transporte agregando una fila o columna ficticia
        si la suma de la oferta y la demanda no coincide.
        """
        total_oferta = sum(self.capacidad_programadores)
        total_demanda = sum(self.demanda_tareas)

        if total_oferta == total_demanda:
            return  # No se necesita balanceo

        if total_oferta > total_demanda:
            # Agregar columna ficticia (tarea ficticia)
            exceso = total_oferta - total_demanda
            for fila in self.matriz_costos:
                fila.append(0)  # Costo cero o alto si se quiere penalizar
            self.num_tareas += 1
            self.demanda_tareas.append(exceso)
            tarea_ficticia = f'Tarea_Ficticia'
            self.tareas.append(tarea_ficticia)
            for i in range(self.num_programadores):
                self.costo_asignacion[self.programadores[i]][tarea_ficticia] = 0
            self.demanda[tarea_ficticia] = exceso

        elif total_demanda > total_oferta:
            # Agregar fila ficticia (programador ficticio)
            exceso = total_demanda - total_oferta
            fila_ficticia = [0] * self.num_tareas  # Costo cero o alto
            self.matriz_costos.append(fila_ficticia)
            self.num_programadores += 1
            self.capacidad_programadores.append(exceso)
            programador_ficticio = f'Programador_Ficticio'
            self.programadores.append(programador_ficticio)
            self.costo_asignacion[programador_ficticio] = {}
            for j in range(self.num_tareas):
                self.costo_asignacion[programador_ficticio][self.tareas[j]] = 0
            self.oferta[programador_ficticio] = exceso

    def resolver_pulp(self):
        """
        Resuelve el problema de asignación utilizando PuLP.
        """
        # Definir las variables de decisión
        rutas = [(i, j) for i in self.programadores for j in self.tareas]
        cantidad = LpVariable.dicts('Cantidad_Asignada', (self.programadores, self.tareas), 0, None, LpInteger)
        
        # Definir la función objetivo (minimizar costo total)
        self.prob += lpSum(cantidad[i][j] * self.costo_asignacion[i][j] for (i, j) in rutas)
        
        # Restricciones de demanda: cada tarea debe recibir exactamente la cantidad de programadores requeridos
        for j in self.tareas:
            self.prob += lpSum(cantidad[i][j] for i in self.programadores) == self.demanda[j]
            
        # Restricciones de oferta: cada programador no puede exceder su capacidad máxima
        for i in self.programadores:
            self.prob += lpSum(cantidad[i][j] for j in self.tareas) <= self.oferta[i]
        
        # Resolver el problema
        self.prob.solve(PULP_CBC_CMD(msg=False))
        
        # Guardar las asignaciones y el costo total
        self.asignaciones = []
        for i in self.programadores:
            for j in self.tareas:
                if cantidad[i][j].value() > 0:
                    for _ in range(int(cantidad[i][j].value())):
                        self.asignaciones.append((i, j, self.costo_asignacion[i][j]))
        
        self.costo_total = value(self.prob.objective)
        
        return self.asignaciones, self.costo_total

    def generar_reporte(self):
        """
        Genera un reporte detallado de la optimización.
        """
        if self.asignaciones is None:
            return "Debe resolver el problema primero."
        
        reporte = "REPORTE DE ASIGNACIÓN DE PROGRAMADORES A TAREAS\n"
        reporte += "=" * 50 + "\n\n"
        
        reporte += "RESUMEN:\n"
        reporte += f"- Número de programadores: {self.num_programadores}\n"
        reporte += f"- Número de tareas: {self.num_tareas}\n"
        reporte += f"- Costo total mínimo: {self.costo_total}\n\n"
        
        reporte += "ASIGNACIONES DETALLADAS:\n"
        reporte += "-" * 50 + "\n"
        reporte += f"{'Programador':<15} | {'Tarea':<15} | {'Costo':<10}\n"
        reporte += "-" * 50 + "\n"
        
        for prog, tarea, costo in self.asignaciones:
            reporte += f"{prog:<15} | {tarea:<15} | {costo:<10.2f}\n"
        
        reporte += "-" * 50 + "\n\n"
        
        # Análisis por programador
        reporte += "ANÁLISIS POR PROGRAMADOR:\n"
        reporte += "-" * 50 + "\n"
        
        prog_stats = {}
        for prog, tarea, costo in self.asignaciones:
            if prog not in prog_stats:
                prog_stats[prog] = {"tareas": 0, "costo_total": 0}
            prog_stats[prog]["tareas"] += 1
            prog_stats[prog]["costo_total"] += costo
        
        for prog, stats in prog_stats.items():
            reporte += f"{prog}: {stats['tareas']} tareas asignadas, costo total: {stats['costo_total']:.2f}\n"
        
        reporte += "-" * 50 + "\n\n"
        
        # Análisis por tarea
        reporte += "ANÁLISIS POR TAREA:\n"
        reporte += "-" * 50 + "\n"
        
        tarea_stats = {}
        for prog, tarea, costo in self.asignaciones:
            if tarea not in tarea_stats:
                tarea_stats[tarea] = {"programadores": 0, "costo_total": 0}
            tarea_stats[tarea]["programadores"] += 1
            tarea_stats[tarea]["costo_total"] += costo
        
        for tarea, stats in tarea_stats.items():
            reporte += f"{tarea}: {stats['programadores']} programadores asignados, costo total: {stats['costo_total']:.2f}\n"
        
        return reporte



class MainProgramadores:
    def __init__(self):
        pass

    def validar_entero_positivo(self,mensaje):
        """
        Valida que la entrada sea un entero positivo.
        
        Args:
            mensaje (str): Mensaje a mostrar al usuario
            
        Returns:
            int: Entero positivo ingresado por el usuario
        """
        while True:
            try:
                valor = input(mensaje)
                valor_int = int(valor)
                if valor_int <= 0:
                    print("Error: Debe ingresar un número entero positivo.")
                    continue
                return valor_int
            except ValueError:
                print("Error: Debe ingresar un número entero válido.")
            except Exception as e:
                print(f"Error inesperado: {str(e)}. Por favor, intente de nuevo.")

    def validar_lista_numeros(self,mensaje, longitud_esperada, tipo="entero"):
        """
        Valida que la entrada sea una lista de números de la longitud esperada.
        
        Args:
            mensaje (str): Mensaje a mostrar al usuario
            longitud_esperada (int): Longitud esperada de la lista
            tipo (str): Tipo de números a validar ("entero" o "flotante")
            
        Returns:
            list: Lista de números ingresados por el usuario
        """
        while True:
            try:
                entrada = input(mensaje).strip().split()
                
                if len(entrada) != longitud_esperada:
                    print(f"Error: Se esperaban {longitud_esperada} valores, pero se ingresaron {len(entrada)}.")
                    continue
                
                if tipo == "entero":
                    valores = [int(x) for x in entrada]
                    # Verificar que sean positivos
                    if any(x < 0 for x in valores):
                        print("Error: Todos los valores deben ser enteros no negativos.")
                        continue
                else:  # flotante
                    valores = [float(x) for x in entrada]
                    # Verificar que sean positivos
                    if any(x < 0 for x in valores):
                        print("Error: Todos los valores deben ser números no negativos.")
                        continue
                    
                return valores
            except ValueError:
                print(f"Error: Todos los valores deben ser números {tipo}s válidos.")
            except Exception as e:
                print(f"Error inesperado: {str(e)}. Por favor, intente de nuevo.")

    def validar_opcion(self,mensaje, opciones_validas):
        """
        Valida que la entrada del usuario sea una de las opciones válidas.
        
        Args:
            mensaje (str): Mensaje a mostrar al usuario
            opciones_validas (list): Lista de opciones válidas
            
        Returns:
            str: Opción seleccionada por el usuario
        """
        while True:
            try:
                opcion = input(mensaje)
                if opcion in opciones_validas:
                    return opcion
                else:
                    print(f"Error: Opción no válida. Las opciones válidas son: {', '.join(opciones_validas)}")
            except Exception as e:
                print(f"Error inesperado: {str(e)}. Por favor, intente de nuevo.")

    def validar_ruta_archivo(self,mensaje):
        """
        Valida que la ruta del archivo exista.
        
        Args:
            mensaje (str): Mensaje a mostrar al usuario
            
        Returns:
            str: Ruta del archivo validada
        """
        while True:
            try:
                ruta = input(mensaje)
                carpeta_actual = os.path.dirname(os.path.abspath(__file__))
                ruta_completa = os.path.join(carpeta_actual, ruta)
                
                if not os.path.exists(ruta_completa):
                    print(f"Error: El archivo {ruta} no existe. Por favor, verifique la ruta e intente de nuevo.")
                    continue
                    
                return ruta_completa
            except Exception as e:
                print(f"Error inesperado: {str(e)}. Por favor, intente de nuevo.")

    def leer_datos_consola(self):
        
        print("=== MÓDULO DE ASIGNACIÓN DE PROGRAMADORES A TAREAS ===")
        
        N = self.validar_entero_positivo("Ingrese el número de programadores (N): ")
        M = self.validar_entero_positivo("Ingrese el número de tareas (M): ")
        
        print("\nIngrese la matriz de costos C[N][M]:")
        C = []
        for i in range(N):
            fila = self.validar_lista_numeros(f"Costos para programador {i}: ", M, "flotante")
            C.append(fila)
        
        print("\nIngrese la capacidad máxima de tareas para cada programador S[N]:")
        S = self.validar_lista_numeros("Capacidades (separadas por espacios): ", N, "entero")
        
        print("\nIngrese la cantidad de programadores requeridos por cada tarea D[M]:")
        D = self.validar_lista_numeros("Demandas (separadas por espacios): ", M, "entero")
        
        return N, M, C, S, D

    def leer_datos_archivo(self,ruta):
        
        try:
            with open(ruta, 'r') as f:
                lineas = [line.strip() for line in f.readlines() if line.strip()]
                
                if len(lineas) < 2:
                    raise ValueError("El archivo debe contener al menos 2 líneas (N y M).")
                    
                try:
                    N = int(lineas[0])  # Número de programadores
                    if N <= 0:
                        raise ValueError("El número de programadores (N) debe ser un entero positivo.")
                except ValueError:
                    raise ValueError("La primera línea debe contener un entero positivo (N).")
                    
                try:
                    M = int(lineas[1])  # Número de tareas
                    if M <= 0:
                        raise ValueError("El número de tareas (M) debe ser un entero positivo.")
                except ValueError:
                    raise ValueError("La segunda línea debe contener un entero positivo (M).")
                
                # Verificar que haya suficientes líneas en el archivo
                if len(lineas) < 2 + N + 2:  # N+M+2 líneas (N, M, matriz NxM, S, D)
                    raise ValueError(f"El archivo debe contener al menos {2 + N + 2} líneas.")
                
                # Leer matriz de costos
                C = []
                for i in range(2, 2 + N):
                    try:
                        if i >= len(lineas):
                            raise ValueError(f"Faltan líneas en el archivo para la matriz de costos.")
                        
                        fila = list(map(float, lineas[i].split()))
                        if len(fila) != M:
                            raise ValueError(f"La fila {i-2} de la matriz de costos tiene {len(fila)} valores, se esperaban {M}.")
                        
                        # Verificar que todos los valores sean no negativos
                        if any(x < 0 for x in fila):
                            raise ValueError(f"La fila {i-2} de la matriz de costos contiene valores negativos.")
                            
                        C.append(fila)
                    except ValueError as e:
                        if "could not convert string to float" in str(e):
                            raise ValueError(f"La fila {i-2} de la matriz de costos contiene valores no numéricos.")
                        else:
                            raise e
                
                # Leer capacidades de programadores
                try:
                    S = list(map(int, lineas[2 + N].split()))
                    if len(S) != N:
                        raise ValueError(f"Se esperaban {N} valores para las capacidades de los programadores.")
                    
                    # Verificar que todos los valores sean positivos
                    if any(x <= 0 for x in S):
                        raise ValueError("Las capacidades de los programadores deben ser enteros positivos.")
                except ValueError as e:
                    if "invalid literal for int" in str(e):
                        raise ValueError("Las capacidades de los programadores deben ser enteros.")
                    else:
                        raise e
                
                # Leer demandas de tareas
                try:
                    D = list(map(int, lineas[3 + N].split()))
                    if len(D) != M:
                        raise ValueError(f"Se esperaban {M} valores para las demandas de las tareas.")
                    
                    # Verificar que todos los valores sean positivos
                    if any(x <= 0 for x in D):
                        raise ValueError("Las demandas de las tareas deben ser enteros positivos.")
                except ValueError as e:
                    if "invalid literal for int" in str(e):
                        raise ValueError("Las demandas de las tareas deben ser enteros.")
                    else:
                        raise e
                
                return N, M, C, S, D
        except Exception as e:
            raise ValueError(f"Error al leer el archivo: {str(e)}")

    def main(self):
        
        print("¿Cómo desea ingresar los datos?\n1. Consola\n2. Archivo")
        opcion = self.validar_opcion("Seleccione una opción (1 o 2): ", ['1', '2'])
        
        try:
            if opcion == '1':
                N, M, C, S, D = self.leer_datos_consola()
            elif opcion == '2':
                ruta = self.validar_ruta_archivo("Ingrese la ruta del archivo: ")
                N, M, C, S, D = self.leer_datos_archivo(ruta)
            
            # Verificar balance entre oferta y demanda
            total_oferta = sum(S)
            total_demanda = sum(D)
            
            print(f"\nTotal de capacidad de programadores: {total_oferta}")
            print(f"Total de programadores requeridos: {total_demanda}")
            
            
            # Crear instancia del problema
            problema = AsignacionProgramadoresTareas(N, M, C, S, D)
            
            # Seleccionar método de resolución
            print("\nSeleccione el método de resolución inicial:")
            print("1. Resolver metodo de transporte con PuLP")
            
            metodo = self.validar_opcion("Seleccione una opción (1): ", ['1'])
            
            if metodo == '1':
                print("\nResolviendo directamente con PuLP...")
            
            # Resolver con PuLP
            asignaciones, costo_total = problema.resolver_pulp()
            
            # Mostrar resultados
            print("\n=== RESULTADOS DE LA OPTIMIZACIÓN ===")
            print(f"Costo total mínimo: {costo_total}")
            print(f"Número total de asignaciones: {len(asignaciones)}")
            
            # Preguntar si se desea ver el reporte detallado
            ver_reporte = self.validar_opcion("\n¿Desea ver el reporte detallado? (s/n): ", ['s', 'n'])
            if ver_reporte.lower() == 's':
                reporte = problema.generar_reporte()
                print("\n" + reporte)
            
            # Preguntar si se desea guardar el reporte
            guardar_reporte = self.validar_opcion("\n¿Desea guardar el reporte en un archivo? (s/n): ", ['s', 'n'])
            if guardar_reporte.lower() == 's':
                nombre_archivo = input("Ingrese el nombre del archivo (sin extensión): ")
                with open(f"{nombre_archivo}.txt", 'w') as f:
                    f.write(problema.generar_reporte())
                print(f"Reporte guardado en {nombre_archivo}.txt")
            
        except Exception as e:
            print(f"Error: {str(e)}")

