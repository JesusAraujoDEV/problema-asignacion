class Servidor:
    def __init__(self, id_servidor, nombre, capacidad_cpu, capacidad_memoria, capacidad_ancho_banda):
        # Inicialización de atributos básicos del servidor
        self.id = id_servidor                          # Identificador único del servidor
        self.nombre = nombre                           # Nombre descriptivo del servidor
        self.capacidad_cpu = capacidad_cpu             # Capacidad total de CPU en GHz
        self.capacidad_memoria = capacidad_memoria     # Capacidad total de memoria en GB
        self.capacidad_ancho_banda = capacidad_ancho_banda # Capacidad total de ancho de banda en Mbps
        
        # Inicialización de contadores de recursos utilizados
        self.cpu_utilizado = 0                         # CPU actualmente en uso
        self.memoria_utilizada = 0                     # Memoria actualmente en uso
        self.ancho_banda_utilizado = 0                 # Ancho de banda actualmente en uso
        
        # Diccionario para almacenar los costos de procesamiento por solicitud
        self.costos_procesamiento = {}                 # Estructura: {id_solicitud: costo}

    def agregar_costo_procesamiento(self, id_solicitud, costo):
        # Registra el costo de procesamiento para una solicitud específica
        self.costos_procesamiento[id_solicitud] = costo

    def puede_procesar_solicitud(self, solicitud):
        # Verifica si hay recursos suficientes para procesar la solicitud
        # Comprueba CPU, memoria y ancho de banda disponibles
        return (self.cpu_utilizado + solicitud.requerimiento_cpu <= self.capacidad_cpu and
                self.memoria_utilizada + solicitud.requerimiento_memoria <= self.capacidad_memoria and
                self.ancho_banda_utilizado + solicitud.requerimiento_ancho_banda <= self.capacidad_ancho_banda)

    def asignar_solicitud(self, solicitud):
        # Intenta asignar una solicitud a este servidor
        # Actualiza los contadores de recursos si es posible
        if self.puede_procesar_solicitud(solicitud):
            self.cpu_utilizado += solicitud.requerimiento_cpu
            self.memoria_utilizada += solicitud.requerimiento_memoria
            self.ancho_banda_utilizado += solicitud.requerimiento_ancho_banda
            return True
        return False

    def get_costo_procesamiento(self, id_solicitud):
        # Obtiene el costo de procesamiento para una solicitud específica
        # Si no existe, retorna infinito para evitar esta asignación
        return self.costos_procesamiento.get(id_solicitud, float('inf'))

    def get_utilizacion_recursos(self):
        # Calcula el porcentaje de utilización de cada recurso
        # Retorna un diccionario con los porcentajes de CPU, memoria y ancho de banda
        return {
            'cpu': (self.cpu_utilizado / self.capacidad_cpu) * 100,
            'memoria': (self.memoria_utilizada / self.capacidad_memoria) * 100,
            'ancho_banda': (self.ancho_banda_utilizado / self.capacidad_ancho_banda) * 100
        }

    def __str__(self):
        # Genera una representación en texto del servidor con sus datos de utilización
        utilizacion = self.get_utilizacion_recursos()
        return (f"Servidor {self.id}: {self.nombre}\n"
                f"  CPU: {self.cpu_utilizado:.2f}/{self.capacidad_cpu:.2f} GHz ({utilizacion['cpu']:.1f}%)\n"
                f"  Memoria: {self.memoria_utilizada:.2f}/{self.capacidad_memoria:.2f} GB ({utilizacion['memoria']:.1f}%)\n"
                f"  Ancho de banda: {self.ancho_banda_utilizado:.2f}/{self.capacidad_ancho_banda:.2f} Mbps ({utilizacion['ancho_banda']:.1f}%)") 