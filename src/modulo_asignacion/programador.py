class Programador:
    def __init__(self, id_programador, nombre, capacidad_maxima):
        self.id = id_programador
        self.nombre = nombre
        self.capacidad_maxima = capacidad_maxima
        self.tareas_asignadas = 0
        self.costos_transporte = {}  # Diccionario {id_tarea: costo_transporte}

    def agregar_costo_transporte(self, id_tarea, costo):
        self.costos_transporte[id_tarea] = costo

    def puede_asumir_tarea(self):
        return self.tareas_asignadas < self.capacidad_maxima

    def asignar_tarea(self):
        if self.puede_asumir_tarea():
            self.tareas_asignadas += 1
            return True
        return False

    def get_costo_transporte(self, id_tarea):
        return self.costos_transporte.get(id_tarea, float('inf'))

    def __str__(self):
        return f"Programador {self.id}: {self.nombre} (Capacidad: {self.tareas_asignadas}/{self.capacidad_maxima})" 