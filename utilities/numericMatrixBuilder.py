import random

# Dimensiones
n = int(input("Rows: "))
m = int(input("Columns: "))

# Nombre del archivo
filename = "matriz.txt"

with open(filename, "w") as f:
    # Primera línea: n y m
    f.write(f"{n} {m}\n")
    
    # Siguientes líneas: matriz (una fila por línea)
    for i in range(n):
        fila = [f"{random.uniform(0.0, 10.0):.6f}" for _ in range(m)]
        f.write(" ".join(fila) + "\n")

print(f"Archivo '{filename}' generado correctamente.")