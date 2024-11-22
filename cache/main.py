from cache import Cache
from process_trace_file import read_trace_file

# Archivo de traza
trace_file = "./cache/trace.out"

def run_test_suite():
    print("== Ejecución de pruebas con y sin optimización avanzada ==")
    
    # Prueba 1: Barrido de tamaño (32, 64, 128 KB), línea de caché 64 bytes, 16 ways
    print("\nPrueba 1: Barrido de tamaño del caché (32, 64, 128 KB)")
    for size_kb in [32, 64, 128]:
        print(f"\n--- Tamaño del caché: {size_kb} KB, Línea de caché: 64 bytes, Asociatividad: 16 ways ---")
        # Sin optimización (sin way prediction)
        simulate_cache(trace_file, size_kb * 1024, 64, 16, way_prediction=False)
        # Con optimización (con way prediction)
        simulate_cache(trace_file, size_kb * 1024, 64, 16, way_prediction=True)

    # Prueba 2: Barrido de asociatividad (4, 8, 16 ways), tamaño de caché 32KB, línea de caché 64 bytes
    print("\nPrueba 2: Barrido de asociatividad (4, 8, 16 ways)")
    for ways in [4, 8, 16]:
        print(f"\n--- Tamaño del caché: 32 KB, Línea de caché: 64 bytes, Asociatividad: {ways} ways ---")
        # Sin optimización (sin way prediction)
        simulate_cache(trace_file, 32 * 1024, 64, ways, way_prediction=False)
        # Con optimización (con way prediction)
        simulate_cache(trace_file, 32 * 1024, 64, ways, way_prediction=True)

    # Prueba 3: Barrido de línea de caché (32, 64, 128 bytes), tamaño de caché 32KB, asociatividad 8 ways
    print("\nPrueba 3: Barrido de tamaño de línea de caché (32, 64, 128 bytes)")
    for line_size in [32, 64, 128]:
        print(f"\n--- Tamaño del caché: 32 KB, Línea de caché: {line_size} bytes, Asociatividad: 8 ways ---")
        # Sin optimización (sin way prediction)
        simulate_cache(trace_file, 32 * 1024, line_size, 8, way_prediction=False)
        # Con optimización (con way prediction)
        simulate_cache(trace_file, 32 * 1024, line_size, 8, way_prediction=True)

def simulate_cache(trace_file, capacity, block_size, associativity, way_prediction):
    """
    Función para simular el caché con una configuración específica y reportar resultados.
    """
    # Crear una instancia de caché con o sin predicción de sentido
    cache = Cache(capacity, block_size, associativity, way_prediction=way_prediction)
    
    # Leer y procesar el archivo de trazas
    read_trace_file(trace_file, cache)
    
    # Determinar si la simulación es optimizada o no
    optimization_status = "Con optimización avanzada (Way Prediction)" if way_prediction else "Sin optimización avanzada"
    
    # Imprimir resultados
    print(f"\nConfiguración: {associativity} ways, {capacity // 1024} KB, línea de {block_size} bytes ({optimization_status})")
    cache.reportar_estadisticas()

# Ejecutar la suite de pruebas
run_test_suite()