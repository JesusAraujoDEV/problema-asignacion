class Programador:
    def __init__(self, id_programador, nombre, capacidad_maxima):
        # Inicialización de los atributos básicos del programador
        self.id = id_programador          # Identificador único del programador
        self.nombre = nombre              # Nombre del programador
        self.capacidad_maxima = capacidad_maxima  # Número máximo de tareas que puede asumir
        self.tareas_asignadas = 0         # Contador de tareas actualmente asignadas
        self.costos_transporte = {}       # Diccionario para almacenar el costo de transporte a cada tarea

    def agregar_costo_transporte(self, id_tarea, costo):
        # Registra el costo de transporte asociado a una tarea específica
        self.costos_transporte[id_tarea] = costo

    def puede_asumir_tarea(self):
        # Verifica si el programador puede asumir más tareas según su capacidad
        return self.tareas_asignadas < self.capacidad_maxima

    def asignar_tarea(self):
        # Intenta asignar una nueva tarea al programador
        # Retorna True si fue posible, False si ya está en su capacidad máxima
        if self.puede_asumir_tarea():
            self.tareas_asignadas += 1
            return True
        return False

    def get_costo_transporte(self, id_tarea):
        # Obtiene el costo de transporte hacia una tarea específica
        # Si no existe, retorna infinito para evitar esta asignación
        return self.costos_transporte.get(id_tarea, float('inf'))

    def __str__(self):
        # Representación en texto del programador con sus datos relevantes
        return f"Programador {self.id}: {self.nombre} (Capacidad: {self.tareas_asignadas}/{self.capacidad_maxima})" 