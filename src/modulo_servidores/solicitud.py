# Clase Solicitud
class Solicitud:
    def __init__(self, id_solicitud, nombre, requerimiento_cpu, requerimiento_memoria, 
                 requerimiento_ancho_banda, prioridad, tiempo_maximo_procesamiento):
        self.id = id_solicitud
        self.nombre = nombre
        self.requerimiento_cpu = requerimiento_cpu
        self.requerimiento_memoria = requerimiento_memoria
        self.requerimiento_ancho_banda = requerimiento_ancho_banda
        self.prioridad = prioridad
        self.tiempo_maximo_procesamiento = tiempo_maximo_procesamiento
        
        # Estado de la solicitud
        self.asignada = False
        self.servidor_asignado = None
        self.tiempo_procesamiento = 0

    def asignar_servidor(self, servidor):
        if not self.asignada and servidor.puede_procesar_solicitud(self):
            self.servidor_asignado = servidor
            self.asignada = True
            return True
        return False

    def get_costo_procesamiento(self, servidor):
        return servidor.get_costo_procesamiento(self.id)

    def get_prioridad_texto(self):
        prioridades = {
            1: "Crítica",
            2: "Alta",
            3: "Media",
            4: "Baja",
            5: "Mínima"
        }
        return prioridades.get(self.prioridad, "Desconocida")

    def __str__(self):
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