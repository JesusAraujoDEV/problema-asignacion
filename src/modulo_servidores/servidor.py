class Servidor:
    def __init__(self, id_servidor, nombre, capacidad_cpu, capacidad_memoria, capacidad_ancho_banda):
        self.id = id_servidor
        self.nombre = nombre
        self.capacidad_cpu = capacidad_cpu
        self.capacidad_memoria = capacidad_memoria
        self.capacidad_ancho_banda = capacidad_ancho_banda
        
        # Recursos actualmente utilizados
        self.cpu_utilizado = 0
        self.memoria_utilizada = 0
        self.ancho_banda_utilizado = 0
        
        # Costos de procesamiento para cada solicitud
        self.costos_procesamiento = {}  # Diccionario {id_solicitud: costo}

    def agregar_costo_procesamiento(self, id_solicitud, costo):
        self.costos_procesamiento[id_solicitud] = costo

    def puede_procesar_solicitud(self, solicitud):
        return (self.cpu_utilizado + solicitud.requerimiento_cpu <= self.capacidad_cpu and
                self.memoria_utilizada + solicitud.requerimiento_memoria <= self.capacidad_memoria and
                self.ancho_banda_utilizado + solicitud.requerimiento_ancho_banda <= self.capacidad_ancho_banda)

    def asignar_solicitud(self, solicitud):
        if self.puede_procesar_solicitud(solicitud):
            self.cpu_utilizado += solicitud.requerimiento_cpu
            self.memoria_utilizada += solicitud.requerimiento_memoria
            self.ancho_banda_utilizado += solicitud.requerimiento_ancho_banda
            return True
        return False

    def get_costo_procesamiento(self, id_solicitud):
        return self.costos_procesamiento.get(id_solicitud, float('inf'))

    def get_utilizacion_recursos(self):
        return {
            'cpu': (self.cpu_utilizado / self.capacidad_cpu) * 100,
            'memoria': (self.memoria_utilizada / self.capacidad_memoria) * 100,
            'ancho_banda': (self.ancho_banda_utilizado / self.capacidad_ancho_banda) * 100
        }

    def __str__(self):
        utilizacion = self.get_utilizacion_recursos()
        return (f"Servidor {self.id}: {self.nombre}\n"
                f"  CPU: {self.cpu_utilizado:.2f}/{self.capacidad_cpu:.2f} GHz ({utilizacion['cpu']:.1f}%)\n"
                f"  Memoria: {self.memoria_utilizada:.2f}/{self.capacidad_memoria:.2f} GB ({utilizacion['memoria']:.1f}%)\n"
                f"  Ancho de banda: {self.ancho_banda_utilizado:.2f}/{self.capacidad_ancho_banda:.2f} Mbps ({utilizacion['ancho_banda']:.1f}%)") 