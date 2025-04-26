from .servidor import Servidor
from .solicitud import Solicitud
from .optimizacion_servidores import OptimizacionServidores

def crear_datos_ejemplo():
    """
    Crea datos de ejemplo para el problema de optimización de servidores.
    
    Returns:
        tuple: (servidores, solicitudes)
    """
    # Crear servidores
    servidores = [
        Servidor(1, "Servidor Principal", 16, 32, 1000),
        Servidor(2, "Servidor Secundario", 8, 16, 500),
        Servidor(3, "Servidor de Respaldo", 4, 8, 250)
    ]
    
    # Crear solicitudes
    solicitudes = [
        Solicitud(1, "Procesamiento de Datos", 4, 8, 100, 1, 30),
        Solicitud(2, "Servicio Web", 2, 4, 50, 2, 60),
        Solicitud(3, "Base de Datos", 6, 12, 200, 1, 45),
        Solicitud(4, "Análisis de Datos", 3, 6, 75, 3, 90),
        Solicitud(5, "Servicio de Caché", 1, 2, 25, 4, 120)
    ]
    
    # Asignar costos de procesamiento
    for servidor in servidores:
        for solicitud in solicitudes:
            # Costo base aleatorio entre 1 y 10
            costo_base = 1 + (servidor.id + solicitud.id) % 10
            servidor.agregar_costo_procesamiento(solicitud.id, costo_base)
    
    return servidores, solicitudes

def main():
    """
    Función principal que ejecuta el módulo de optimización de servidores.
    """
    print("\n=== Módulo de Optimización de Servidores ===")
    
    # Crear datos de ejemplo
    servidores, solicitudes = crear_datos_ejemplo()
    
    # Crear y resolver el problema de optimización
    optimizacion = OptimizacionServidores(servidores, solicitudes)
    optimizacion.resolver_problema_asignacion()
    
    # Generar y mostrar el reporte
    reporte = optimizacion.generar_reporte()
    print(reporte)

if __name__ == "__main__":
    main() 