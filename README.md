# Sistema de Optimización de Recursos

Este sistema implementa dos módulos de optimización basados en programación lineal para resolver problemas de asignación de recursos:

1. **Módulo de Asignación de Programadores a Tareas con Restricciones de Transporte**
2. **Optimización de la Asignación de Solicitudes a Servidores**

## Requisitos

- Python 3.6 o superior
- Bibliotecas requeridas:
  - numpy
  - scipy
  - pulp
  - pandas

Para instalar las dependencias:

\`\`\`
pip install numpy scipy pulp pandas
\`\`\`

## Uso

Ejecute el archivo principal para acceder al menú del sistema:

\`\`\`
python main.py
\`\`\`

### Módulo 1: Asignación de Programadores a Tareas

Este módulo resuelve el problema de asignar programadores a tareas considerando restricciones de transporte y ubicación geográfica.

**Características:**
- Permite ingresar datos por consola o desde archivo
- Implementa métodos de resolución de problemas de transporte:
  - Método de la Esquina Noroeste
  - Método de Costo Mínimo
  - Aproximación de Vogel
- Optimiza usando programación lineal (PuLP)
- Genera reportes detallados de la asignación

### Módulo 2: Asignación de Solicitudes a Servidores

Este módulo optimiza la asignación de solicitudes a servidores en un entorno de computación en la nube, minimizando el tiempo de respuesta y balanceando la carga de trabajo.

**Características:**
- Permite ingresar datos por consola o desde archivo
- Considera prioridades de solicitudes
- Implementa el Método Húngaro para optimización
- Verifica restricciones de capacidad y prioridad
- Genera reportes detallados de la asignación

## Formato de Archivos de Entrada

### Para el Módulo de Programadores:
\`\`\`
N           # Número de programadores
M           # Número de tareas
C[0][0] C[0][1] ... C[0][M-1]  # Matriz de costos (fila 1)
...
C[N-1][0] C[N-1][1] ... C[N-1][M-1]  # Matriz de costos (fila N)
S[0] S[1] ... S[N-1]  # Capacidades de programadores
D[0] D[1] ... D[M-1]  # Demandas de tareas
\`\`\`

### Para el Módulo de Servidores:
\`\`\`
S           # Número de servidores
R           # Número de solicitudes
C[0][0] C[0][1] ... C[0][R-1]  # Matriz de costos (fila 1)
...
C[S-1][0] C[S-1][1] ... C[S-1][R-1]  # Matriz de costos (fila S)
P[0] P[1] ... P[R-1]  # Prioridades de solicitudes (opcional)
CAP[0] CAP[1] ... CAP[S-1]  # Capacidades de servidores (opcional)
\`\`\`

## Ejemplos

El sistema incluye archivos de ejemplo para probar ambos módulos:
- `programadores.txt`
- `servidores.txt`

## Estructura del Proyecto

\`\`\`
.
├── main.py                         # Punto de entrada principal
├── modulo_asignacion_programadores.py  # Módulo 1
├── modulo_asignacion_servidores.py     # Módulo 2
├── programadores.txt     # Datos de ejemplo para el Módulo 1
├── servidores.txt        # Datos de ejemplo para el Módulo 2
└── README.md                       # Este archivo
