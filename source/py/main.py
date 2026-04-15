# main.py
import sys
import time
import math
from PIL import Image
import numpy as np

from AhoraenPython import encontrar_seam_backtracking
from AhoraenPython import encontrar_seam_pd


def calcular_energia(imagen):
    img = np.array(imagen.convert("RGB"), dtype=float)
    n, m, _ = img.shape
    energia = [[0.0] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            izq = img[i][j - 1] if j > 0 else img[i][j]
            der = img[i][j + 1] if j < m - 1 else img[i][j]
            grad_x = np.sum((der - izq) ** 2)
            arr = img[i - 1][j] if i > 0 else img[i][j]
            aba = img[i + 1][j] if i < n - 1 else img[i][j]
            grad_y = np.sum((aba - arr) ** 2)
            energia[i][j] = math.sqrt(grad_x + grad_y)
    return energia


def marcar_costura(imagen, seam, color=(255, 0, 0)):
    img = imagen.copy().convert("RGB")
    pixels = img.load()
    for fila, col in enumerate(seam):
        pixels[col, fila] = color
    return img


def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py <imagen> <algoritmo>")
        print("  algoritmo: bt  → Backtracking")
        print("             pd  → Programación Dinámica")
        print("             all → Ambos (compara tiempos)")
        sys.exit(1)

    path_imagen = sys.argv[1]
    algoritmo = sys.argv[2].lower()

    if algoritmo not in ("bt", "pd", "all"):
        print(f"Error: algoritmo '{algoritmo}' no reconocido. Usá bt, pd o all.")
        sys.exit(1)

    # Cargar imagen
    try:
        imagen = Image.open(path_imagen)
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{path_imagen}'")
        sys.exit(1)

    n, m = imagen.size[1], imagen.size[0]
    print(f"Imagen cargada: {m} columnas x {n} filas")

    print("Calculando energía...")
    energia = calcular_energia(imagen)

    base = path_imagen.rsplit(".", 1)[0]

    # --- Backtracking ---
    if algoritmo in ("bt", "all"):
        print("\n[Backtracking]")
        t0 = time.time()
        seam = encontrar_seam_backtracking(energia)
        t = time.time() - t0
        e_total = sum(energia[i][seam[i]] for i in range(n))
        print(f"  Tiempo:  {t:.4f} s")
        print(f"  Energía: {e_total:.4f}")
        print(f"  Costura: {[c + 1 for c in seam]}  (indexado desde 1)")
        img_resultado = marcar_costura(imagen, seam, color=(255, 0, 0))
        salida = f"{base}_costura_bt.png"
        img_resultado.save(salida)
        print(f"  Imagen guardada en: {salida}")

    # --- Programación Dinámica ---
    if algoritmo in ("pd", "all"):
        print("\n[Programación Dinámica]")
        t0 = time.time()
        seam = encontrar_seam_pd(energia)
        t = time.time() - t0
        e_total = sum(energia[i][seam[i]] for i in range(n))
        print(f"  Tiempo:  {t:.4f} s")
        print(f"  Energía: {e_total:.4f}")
        print(f"  Costura: {[c + 1 for c in seam]}  (indexado desde 1)")
        img_resultado = marcar_costura(imagen, seam, color=(0, 0, 255))
        salida = f"{base}_costura_pd.png"
        img_resultado.save(salida)
        print(f"  Imagen guardada en: {salida}")


if __name__ == "__main__":
    main()