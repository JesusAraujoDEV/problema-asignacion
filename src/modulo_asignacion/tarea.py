class Tarea:
    def __init__(self, id_tarea, nombre, ubicacion, programadores_requeridos):
        # Inicialización de los atributos básicos de la tarea
        self.id = id_tarea                    # Identificador único de la tarea
        self.nombre = nombre                  # Nombre descriptivo de la tarea
        self.ubicacion = ubicacion            # Lugar donde se realiza la tarea
        self.programadores_requeridos = programadores_requeridos  # Cantidad de programadores necesarios
        self.programadores_asignados = 0      # Contador de programadores ya asignados
        self.costos_desempeno = {}            # Almacena el costo de desempeño para cada programador

    def agregar_costo_desempeno(self, id_programador, costo):
        # Registra el costo de desempeño de un programador específico en esta tarea
        self.costos_desempeno[id_programador] = costo

    def necesita_mas_programadores(self):
        # Verifica si la tarea aún necesita más programadores para completarse
        return self.programadores_asignados < self.programadores_requeridos

    def asignar_programador(self):
        # Intenta asignar un programador a esta tarea
        # Retorna True si se pudo asignar, False si ya tiene todos los requeridos
        if self.necesita_mas_programadores():
            self.programadores_asignados += 1
            return True
        return False

    def get_costo_desempeno(self, id_programador):
        # Obtiene el costo de desempeño de un programador específico en esta tarea
        # Si no existe, retorna infinito para evitar esta asignación
        return self.costos_desempeno.get(id_programador, float('inf'))

    def __str__(self):
        # Representación en texto de la tarea con sus datos relevantes
        return f"Tarea {self.id}: {self.nombre} en {self.ubicacion} (Asignados: {self.programadores_asignados}/{self.programadores_requeridos})" 