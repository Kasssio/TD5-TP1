#!/usr/bin/env python3

import sys
import time
from PIL import Image

from BT import seam_carving_bt
from DP import seam_carving_pd


def main():
    if len(sys.argv) < 4:
        print("Uso: python main.py <imagen> <algoritmo> <costuras>")
        print("  algoritmo: bt  → Backtracking")
        print("             pd  → Programación Dinámica")
        print("             all → Ambos")
        print("  costuras:  cantidad de costuras a eliminar (entero positivo)")
        print("")
        print("Ejemplo: python main.py foto.jpg pd 50")
        sys.exit(1)

    path_imagen = sys.argv[1]
    algoritmo   = sys.argv[2].lower()
    try:
        k = int(sys.argv[3])
        assert k > 0
    except:
        print("Error: <costuras> debe ser un entero positivo.")
        sys.exit(1)

    if algoritmo not in ("bt", "pd", "all"):
        print(f"Error: algoritmo '{algoritmo}' no reconocido. Usá bt, pd o all.")
        sys.exit(1)

    try:
        imagen = Image.open(path_imagen)
    except FileNotFoundError:
        print(f"Error: no se encontró '{path_imagen}'")
        sys.exit(1)

    n, m = imagen.size[1], imagen.size[0]
    print(f"Imagen cargada: {m} columnas x {n} filas")
    print(f"Costuras a eliminar: {k}")

    if k >= m:
        print(f"Error: no se pueden eliminar {k} costuras de una imagen de {m} columnas.")
        sys.exit(1)

    base = path_imagen.rsplit(".", 1)[0]

    # Advertencia BT en imágenes grandes
    if algoritmo in ("bt", "all") and (n > 50 or m > 50):
        print(f"\n⚠ ADVERTENCIA: BT es muy lento para imágenes de {m}x{n}.")
        print("  Se recomienda máximo 50x50 para Backtracking.")
        resp = input("  ¿Querés continuar igual? (s/n): ")
        if resp.lower() != "s":
            print("  Backtracking cancelado.")
            if algoritmo == "bt":
                sys.exit(0)
            algoritmo = "pd"  # Si era "all", seguimos solo con PD

    # --- Backtracking ---
    if algoritmo in ("bt", "all"):
        print("\n[Backtracking]")
        t0 = time.time()
        img_bt = seam_carving_bt(imagen, k)
        t = time.time() - t0
        salida = f"{base}bt{k}costuras.png"
        img_bt.save(salida)
        print(f"  Tiempo total: {t*1000:.4f} ms")
        print(f"  Imagen guardada en: {salida}")

    # --- Programación Dinámica ---
    if algoritmo in ("pd", "all"):
        print("\n[Programación Dinámica]")
        t0 = time.time()
        img_pd = seam_carving_pd(imagen, k)
        t = time.time() - t0
        salida = f"{base}pd{k}costuras.png"
        img_pd.save(salida)
        print(f"  Tiempo total: {t*1000:.4f} ms")
        print(f"  Imagen guardada en: {salida}")


if __name__ == "__main__":
    main()
