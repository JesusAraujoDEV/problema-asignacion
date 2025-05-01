
---

# 📊 Sistema de Optimización de Recursos

Este sistema interactivo resuelve problemas de asignación de recursos mediante técnicas de **programación lineal**. Incluye dos módulos principales:

1. **Asignación de Programadores a Tareas con Restricciones de Transporte**
2. **Asignación de Solicitudes a Servidores en la Nube**

---

## ⚙️ Requisitos

- Python 3.6 o superior
- Bibliotecas necesarias:

```bash
pip install numpy scipy pulp pandas
```

---

## 🚀 Ejecución

Ejecute el menú principal del sistema desde consola:

```bash
python main.py
```

Desde allí podrá acceder a cualquiera de los dos módulos de optimización.

---

## 🧠 Módulo 1: Asignación de Programadores a Tareas

Este módulo resuelve el problema de asignar programadores a tareas distribuidas geográficamente, considerando tanto su capacidad como los costos de transporte y desempeño.

### Características:

- Ingreso de datos por consola o desde archivo
- Métodos de solución inicial:
  - Esquina Noroeste
  - Costo Mínimo
  - Aproximación de Vogel
- Optimización final con **programación lineal** usando **PuLP**
- Generación de reportes detallados (por tarea y programador)
- Balanceo automático de oferta y demanda

---

## 🌐 Módulo 2: Asignación de Solicitudes a Servidores

Este módulo optimiza la asignación de solicitudes a servidores considerando **prioridades**, **tiempos de procesamiento** y **restricciones de capacidad**.

### Características:

- Ingreso de datos por consola o desde archivo
- Ajuste automático por prioridad de solicitudes
- Solución óptima mediante el **Método Húngaro**
- Verificación de:
  - Capacidad de servidores
  - Asignación coherente con las prioridades
- Reportes con distribución de carga y tiempo total

---

## 📂 Formato de Archivos de Entrada

### 📌 Módulo de Programadores (`programadores.txt`)

```txt
N               # Número de programadores
M               # Número de tareas
C[0][0] ... C[0][M-1]         # Fila 1 de matriz de costos
...
C[N-1][0] ... C[N-1][M-1]     # Fila N
S[0] S[1] ... S[N-1]          # Capacidades de programadores
D[0] D[1] ... D[M-1]          # Demandas de tareas
```

### 📌 Módulo de Servidores (`servidores.txt`)

```txt
S               # Número de servidores
R               # Número de solicitudes
C[0][0] ... C[0][R-1]         # Fila 1 de matriz de costos
...
C[S-1][0] ... C[S-1][R-1]     # Fila S
P[0] ... P[R-1]               # (Opcional) Prioridades de solicitudes
CAP[0] ... CAP[S-1]           # (Opcional) Capacidades de servidores
```

---

## 🧪 Archivos de Ejemplo

Incluidos en el repositorio:

- `programadores.txt` – datos para el módulo de tareas
- `servidores.txt` – datos para el módulo de servidores

---

## 📁 Estructura del Proyecto

```text
.
├── main.py                               # Menú principal del sistema
├── modulo_asignacion_programadores.py    # Módulo de Programadores
├── modulo_asignacion_servidores.py       # Módulo de Servidores
├── programadores.txt                     # Ejemplo de entrada para módulo 1
├── servidores.txt                        # Ejemplo de entrada para módulo 2
└── README.md                             # Este archivo
```

---

## 🧑‍💻 Autor

Desarrollado como parte de un proyecto de optimización y programación lineal. Para fines académicos y educativos.
