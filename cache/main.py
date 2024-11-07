from cache import Cache
from process_trace_file import read_trace_file


# Ejecuta la función de lectura con el archivo trace.out
trace_file = "trace.out"  # Nombre del archivo descomprimido
read_trace_file(trace_file)

# Specs del cache
capacity = 32*(2**10)
cache_line = 64
ways = 16

# Crea nuevo cache
cache = Cache(capacity, cache_line, ways)


# Accessa al cache
cache.access(0x30003770)
cache.access(0x30003bf8)
cache.access(0x30003720)
cache.access(0x30103bf8)

cache.reportar_estadisticas()
