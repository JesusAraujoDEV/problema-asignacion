# Clase Solicitud
class Solicitud:
    def __init__(self, id_solicitud, nombre, requerimiento_cpu, requerimiento_memoria, 
                 requerimiento_ancho_banda, prioridad, tiempo_maximo_procesamiento):
        # Inicialización de atributos básicos de la solicitud
        self.id = id_solicitud                      # Identificador único
        self.nombre = nombre                        # Nombre descriptivo de la solicitud
        self.requerimiento_cpu = requerimiento_cpu  # CPU necesaria en GHz
        self.requerimiento_memoria = requerimiento_memoria  # Memoria necesaria en GB
        self.requerimiento_ancho_banda = requerimiento_ancho_banda  # Ancho de banda en Mbps
        self.prioridad = prioridad                  # Nivel de prioridad (1-5, donde 1 es la más alta)
        self.tiempo_maximo_procesamiento = tiempo_maximo_procesamiento  # Tiempo máximo en segundos
        
        # Estado inicial de la solicitud
        self.asignada = False                       # Indica si ya fue asignada a un servidor
        self.servidor_asignado = None               # Referencia al servidor asignado
        self.tiempo_procesamiento = 0               # Tiempo actual de procesamiento

    def asignar_servidor(self, servidor):
        # Intenta asignar la solicitud a un servidor específico
        # Verifica que no esté ya asignada y que el servidor pueda procesarla
        if not self.asignada and servidor.puede_procesar_solicitud(self):
            self.servidor_asignado = servidor
            self.asignada = True
            return True
        return False

    def get_costo_procesamiento(self, servidor):
        # Obtiene el costo de procesamiento de esta solicitud en un servidor específico
        return servidor.get_costo_procesamiento(self.id)

    def get_prioridad_texto(self):
        # Convierte el nivel numérico de prioridad a su representación textual
        prioridades = {
            1: "Crítica",
            2: "Alta",
            3: "Media",
            4: "Baja",
            5: "Mínima"
        }
        return prioridades.get(self.prioridad, "Desconocida")

    def __str__(self):
        # Genera una representación en texto de la solicitud con sus detalles
        estado = "Asignada" if self.asignada else "Pendiente"
        servidor = f" al servidor {self.servidor_asignado.id}" if self.asignada else ""
        return (f"Solicitud {self.id}: {self.nombre}\n"
                f"  Estado: {estado}{servidor}\n"
                f"  Requerimientos:\n"
                f"    CPU: {self.requerimiento_cpu:.2f} GHz\n"
                f"    Memoria: {self.requerimiento_memoria:.2f} GB\n"
                f"    Ancho de banda: {self.requerimiento_ancho_banda:.2f} Mbps\n"
                f"  Prioridad: {self.get_prioridad_texto()}\n"
                f"  Tiempo máximo: {self.tiempo_maximo_procesamiento:.2f} segundos") 