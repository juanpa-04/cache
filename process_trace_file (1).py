# process_trace_file.py
def read_trace_file(trace_file, cache):
    try:
        with open(trace_file, 'r') as f:
            line_count = 0
            for line in f:
                line = line.strip().lstrip("#").strip()
                if not line:
                    continue

                parts = line.split()
                if len(parts) != 3:
                    continue

                ls = int(parts[0])         # Tipo de acceso (0 para load, 1 para store)
                address = int(parts[1], 16) # Dirección en hexadecimal
                ic = int(parts[2])          # Número de instrucciones (IC)

                # Acceso al caché con la dirección extraída
                cache.access(address)
                line_count += 1

            print(f"\nProcesamiento completado. Total de líneas leídas: {line_count}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{trace_file}'.")
    except Exception as e:
        print(f"Error al leer el archivo '{trace_file}': {e}")