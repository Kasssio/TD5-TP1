import sys
import time
import math
from PIL import Image
import numpy as np

from AhoraenPhython import encontrar_seam_backtracking
from AhoraenPhython import encontrar_seam_pd

def calcular_energia(imagen):
    """
    Calcula la energía de cada píxel usando el gradiente (diferencias entre píxeles vecinos).
    Devuelve una matriz 2D de floats.
    """
    img = np.array(imagen.convert("RGB"), dtype=float)
    n, m, _ = img.shape

    energia = [[0.0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            # Gradiente horizontal
            izq = img[i][j - 1] if j > 0 else img[i][j]
            der = img[i][j + 1] if j < m - 1 else img[i][j]
            grad_x = np.sum((der - izq) ** 2)

            # Gradiente vertical
            arr = img[i - 1][j] if i > 0 else img[i][j]
            aba = img[i + 1][j] if i < n - 1 else img[i][j]
            grad_y = np.sum((aba - arr) ** 2)

            energia[i][j] = math.sqrt(grad_x + grad_y)

    return energia


def marcar_costura(imagen, seam, color=(255, 0, 0)):
    """Devuelve una copia de la imagen con la costura marcada en el color dado."""
    img = imagen.copy().convert("RGB")
    pixels = img.load()
    for fila, col in enumerate(seam):
        pixels[col, fila] = color
    return img


def guardar_resultado(img_original, seam_bt, seam_pd, path_salida_bt, path_salida_pd):
    img_bt = marcar_costura(img_original, seam_bt, color=(255, 0, 0))
    img_pd = marcar_costura(img_original, seam_pd, color=(0, 0, 255))
    img_bt.save(path_salida_bt)
    img_pd.save(path_salida_pd)
    print(f"Imagen BT guardada en: {path_salida_bt}")
    print(f"Imagen PD guardada en: {path_salida_pd}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <imagen.png>")
        sys.exit(1)

    path_imagen = sys.argv[1]

    # Cargar imagen
    try:
        imagen = Image.open(path_imagen)
    except FileNotFoundError:
        print(f"Error: no se encontró el archivo '{path_imagen}'")
        sys.exit(1)

    n, m = imagen.size[1], imagen.size[0]
    print(f"Imagen cargada: {m} columnas x {n} filas")

    # Calcular energía
    print("Calculando energía...")
    energia = calcular_energia(imagen)

    # --- Backtracking ---
    print("\n[Backtracking]")
    t0 = time.time()
    seam_bt = encontrar_seam_backtracking(energia)
    t_bt = time.time() - t0
    energia_bt = sum(energia[i][seam_bt[i]] for i in range(n))
    print(f"  Tiempo:  {t_bt:.4f} s")
    print(f"  Energía: {energia_bt:.4f}")
    print(f"  Costura: {[c + 1 for c in seam_bt]}  (indexado desde 1)")

    # --- Programación Dinámica ---
    print("\n[Programación Dinámica]")
    t0 = time.time()
    seam_pd = encontrar_seam_pd(energia)
    t_pd = time.time() - t0
    energia_pd = sum(energia[i][seam_pd[i]] for i in range(n))
    print(f"  Tiempo:  {t_pd:.4f} s")
    print(f"  Energía: {energia_pd:.4f}")
    print(f"  Costura: {[c + 1 for c in seam_pd]}  (indexado desde 1)")

    # --- Comparación ---
    print("\n[Comparación]")
    if abs(energia_bt - energia_pd) < 1e-6:
        print("  ✓ Ambos algoritmos encontraron la misma energía mínima.")
    else:
        print("  ✗ ADVERTENCIA: los algoritmos devolvieron energías distintas.")
        print(f"    BT: {energia_bt:.4f}  |  PD: {energia_pd:.4f}")

    if t_pd > 0:
        print(f"  BT fue {t_bt / t_pd:.1f}x más lento que PD.")

    # --- Guardar imágenes ---
    base = path_imagen.rsplit(".", 1)[0]
    guardar_resultado(
        imagen,
        seam_bt,
        seam_pd,
        path_salida_bt=f"{base}_costura_bt.png",
        path_salida_pd=f"{base}_costura_pd.png",
    )


if __name__ == "__main__":
    main()