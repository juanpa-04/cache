# Función para leer y procesar el archivo trace.out (imprimir solo el total al final, ya que no tengo el cache xd)
def read_trace_file(trace_file):
    try:
        # Abre el archivo trace en modo de lectura
        with open(trace_file, 'r') as f:
            line_count = 0  # Contador de líneas procesadas
            for line in f:
                # Elimina espacios, carácter '#' al comienzo de cada línea
                line = line.strip().lstrip("#").strip()

                # Verifica que la línea no esté vacía después de eliminar el `#`
                if not line:
                    continue

                # Lee y separa los valores en cada línea
                parts = line.split()

                # Verifica que la línea tenga el formato correcto
                if len(parts) != 3:
                    continue

                # Obtiene cada valor del formato de traza
                ls = int(parts[0])  # Tipo de acceso (0 para load, 1 para store)
                address = parts[1]  # Dirección en hexadecimal
                ic = int(parts[2])  # Número de instrucciones (IC)

                # Incrementa el contador de líneas procesadas
                line_count += 1

            print(f"\nProcesamiento completado. Total de líneas leídas: {line_count}")
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{trace_file}'. Asegúrate de que el archivo está en la ubicación correcta.")
    except Exception as e:
        print(f"Error al leer el archivo '{trace_file}': {e}")

# Ejecuta la función de lectura con el archivo trace.out
trace_file = "trace.out"  # Nombre del archivo descomprimido
read_trace_file(trace_file)
