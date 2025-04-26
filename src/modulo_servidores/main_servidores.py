from .servidor import Servidor
from .solicitud import Solicitud
from .optimizacion_servidores import OptimizacionServidores

def crear_datos_ejemplo():
    """
    Crea datos de ejemplo para el problema de optimización de servidores.
    
    Returns:
        tuple: (servidores, solicitudes)
    """
    # Creación de servidores con sus capacidades de recursos
    # Los parámetros son: id, nombre, capacidad_cpu(GHz), capacidad_memoria(GB), capacidad_ancho_banda(Mbps)
    servidores = [
        Servidor(1, "Servidor Principal", 16, 32, 1000),    # Servidor de alta capacidad
        Servidor(2, "Servidor Secundario", 8, 16, 500),     # Servidor de capacidad media
        Servidor(3, "Servidor de Respaldo", 4, 8, 250)      # Servidor de baja capacidad
    ]
    
    # Creación de solicitudes con sus requerimientos de recursos y prioridades
    # Los parámetros son: id, nombre, req_cpu, req_memoria, req_ancho_banda, prioridad(1-5), tiempo_max
    solicitudes = [
        Solicitud(1, "Procesamiento de Datos", 4, 8, 100, 1, 30),   # Prioridad crítica (1)
        Solicitud(2, "Servicio Web", 2, 4, 50, 2, 60),              # Prioridad alta (2)
        Solicitud(3, "Base de Datos", 6, 12, 200, 1, 45),           # Prioridad crítica (1)
        Solicitud(4, "Análisis de Datos", 3, 6, 75, 3, 90),         # Prioridad media (3)
        Solicitud(5, "Servicio de Caché", 1, 2, 25, 4, 120)         # Prioridad baja (4)
    ]
    
    # Asignación de costos de procesamiento para cada combinación servidor-solicitud
    for servidor in servidores:
        for solicitud in solicitudes:
            # Cálculo simple del costo basado en los IDs
            # En un caso real, estos costos podrían depender de factores como
            # la eficiencia del servidor para ciertos tipos de tareas
            costo_base = 1 + (servidor.id + solicitud.id) % 10
            servidor.agregar_costo_procesamiento(solicitud.id, costo_base)
    
    return servidores, solicitudes

def leer_entero_positivo(mensaje, minimo=1):
    """
    Lee un número entero positivo desde la consola con validación.
    
    Args:
        mensaje: Texto a mostrar para solicitar el dato
        minimo: Valor mínimo aceptable
        
    Returns:
        int: Número entero validado
    """
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
    """
    Lee un número decimal positivo desde la consola con validación.
    
    Args:
        mensaje: Texto a mostrar para solicitar el dato
        minimo: Valor mínimo aceptable
        
    Returns:
        float: Número decimal validado
    """
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
    """
    Solicita al usuario ingresar todos los datos necesarios para el problema de optimización de servidores.
    
    Returns:
        tuple: (servidores, solicitudes)
    """
    try:
        print("\n=== Ingreso de datos para la optimización de servidores ===")
        
        # Leer número de servidores y solicitudes
        n_servidores = leer_entero_positivo("Ingrese el número de servidores (N): ")
        n_solicitudes = leer_entero_positivo("Ingrese el número de solicitudes (M): ")
        
        # Crear servidores
        print("\n--- Datos de los servidores ---")
        servidores = []
        for i in range(1, n_servidores + 1):
            print(f"\nServidor {i}:")
            nombre = input(f"Nombre del servidor {i}: ")
            while not nombre.strip():
                print("Error: El nombre no puede estar vacío.")
                nombre = input(f"Nombre del servidor {i}: ")
                
            cpu = leer_float_positivo(f"Capacidad de CPU (GHz) para {nombre}: ")
            memoria = leer_float_positivo(f"Capacidad de memoria (GB) para {nombre}: ")
            ancho_banda = leer_float_positivo(f"Capacidad de ancho de banda (Mbps) para {nombre}: ")
            
            servidores.append(Servidor(i, nombre, cpu, memoria, ancho_banda))
        
        # Crear solicitudes
        print("\n--- Datos de las solicitudes ---")
        solicitudes = []
        for j in range(1, n_solicitudes + 1):
            print(f"\nSolicitud {j}:")
            nombre = input(f"Nombre de la solicitud {j}: ")
            while not nombre.strip():
                print("Error: El nombre no puede estar vacío.")
                nombre = input(f"Nombre de la solicitud {j}: ")
                
            req_cpu = leer_float_positivo(f"Requerimiento de CPU (GHz) para {nombre}: ")
            req_memoria = leer_float_positivo(f"Requerimiento de memoria (GB) para {nombre}: ")
            req_ancho_banda = leer_float_positivo(f"Requerimiento de ancho de banda (Mbps) para {nombre}: ")
            
            prioridad = leer_entero_positivo(f"Prioridad (1-5, donde 1 es la más alta) para {nombre}: ", 1)
            while prioridad > 5:
                print("Error: La prioridad debe estar entre 1 y 5.")
                prioridad = leer_entero_positivo(f"Prioridad (1-5) para {nombre}: ", 1)
                
            tiempo_max = leer_float_positivo(f"Tiempo máximo de procesamiento (segundos) para {nombre}: ")
            
            solicitudes.append(Solicitud(j, nombre, req_cpu, req_memoria, req_ancho_banda, prioridad, tiempo_max))
        
        # Verificar si es posible procesar todas las solicitudes
        es_posible = False
        for solicitud in solicitudes:
            for servidor in servidores:
                if servidor.puede_procesar_solicitud(solicitud):
                    es_posible = True
                    break
            if not es_posible:
                print(f"\nADVERTENCIA: La solicitud '{solicitud.nombre}' no puede ser procesada por ningún servidor.")
                print("Es posible que el problema no tenga solución.")
                if input("¿Desea continuar de todos modos? (s/n): ").lower() != 's':
                    print("Operación cancelada. Volviendo al menú principal.")
                    return None, None
                es_posible = True  # Resetear para la siguiente solicitud
        
        # Ingresar costos de procesamiento
        print("\n--- Costos de procesamiento ---")
        for servidor in servidores:
            for solicitud in solicitudes:
                costo = leer_float_positivo(
                    f"Costo de procesamiento de {solicitud.nombre} en {servidor.nombre}: "
                )
                servidor.agregar_costo_procesamiento(solicitud.id, costo)
        
        return servidores, solicitudes
        
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
        return None, None
    except Exception as e:
        print(f"\nError inesperado: {str(e)}")
        return None, None

def main():
    """
    Función principal que ejecuta el módulo de optimización de servidores.
    Crea los datos, resuelve el problema y muestra los resultados.
    """
    print("\n=== Módulo de Optimización de Servidores ===")
    
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
        servidores, solicitudes = crear_datos_ejemplo()
    else:
        servidores, solicitudes = ingresar_datos_por_consola()
    
    # Verificar si se obtuvieron datos válidos
    if servidores is None or solicitudes is None or len(servidores) == 0 or len(solicitudes) == 0:
        print("\nNo hay datos suficientes para realizar la optimización.")
        return
    
    # Inicializamos el optimizador y ejecutamos el algoritmo de asignación
    try:
        print("\nResolviendo el problema de optimización...")
        optimizacion = OptimizacionServidores(servidores, solicitudes)
        optimizacion.resolver_problema_asignacion()
        
        # Generamos un reporte detallado con los resultados de la optimización
        reporte = optimizacion.generar_reporte()
        print(reporte)  # Mostramos el reporte en la consola
    except Exception as e:
        print(f"\nError al resolver el problema de optimización: {str(e)}")

if __name__ == "__main__":
    main() 