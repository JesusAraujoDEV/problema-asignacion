class Tarea:
    def __init__(self, id_tarea, nombre, ubicacion, programadores_requeridos):
        self.id = id_tarea
        self.nombre = nombre
        self.ubicacion = ubicacion
        self.programadores_requeridos = programadores_requeridos
        self.programadores_asignados = 0
        self.costos_desempeno = {}  # Diccionario {id_programador: costo_desempeno}

    def agregar_costo_desempeno(self, id_programador, costo):
        self.costos_desempeno[id_programador] = costo

    def necesita_mas_programadores(self):
        return self.programadores_asignados < self.programadores_requeridos

    def asignar_programador(self):
        if self.necesita_mas_programadores():
            self.programadores_asignados += 1
            return True
        return False

    def get_costo_desempeno(self, id_programador):
        return self.costos_desempeno.get(id_programador, float('inf'))

    def __str__(self):
        return f"Tarea {self.id}: {self.nombre} en {self.ubicacion} (Asignados: {self.programadores_asignados}/{self.programadores_requeridos})" 