# Problema de Asignación - Universidad José Antonio Paez

Este proyecto implementa dos módulos principales:

1. Módulo de Asignación de Programadores a Tareas con Restricciones de Transporte
2. Módulo de Optimización de la Asignación de Solicitudes a Servidores

## Requisitos

- Python 3.8 o superior
- Dependencias listadas en `requirements.txt`

## Instalación

1. Clonar el repositorio
2. Crear un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```
3. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Estructura del Proyecto

```
problema-asignacion/
├── src/
│   ├── modulo_asignacion/
│   │   ├── programador.py
│   │   ├── tarea.py
│   │   ├── asignacion_transporte.py
│   │   └── main_asignacion.py
│   └── modulo_servidores/
│       ├── servidor.py
│       ├── solicitud.py
│       ├── optimizacion_servidores.py
│       └── main_servidores.py
├── requirements.txt
└── README.md
```

## Uso

Cada módulo puede ser ejecutado independientemente:

```bash
# Para el módulo de asignación de programadores
python src/modulo_asignacion/main_asignacion.py

# Para el módulo de optimización de servidores
python src/modulo_servidores/main_servidores.py
```
