import math
from PIL import Image
import numpy as np

def _calcular_energia(imagen):
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

def encontrar_seam_pd(energia):
    n = len(energia)
    m = len(energia[0])
    solution = [[0.0] * m for _ in range(n)]
    solution[0] = energia[0][:]
    for i in range(1, n):
        for j in range(m):
            e = energia[i][j]
            if j == 0:
                solution[i][j] = e + min(solution[i-1][j], solution[i-1][j+1])
            elif j == m - 1:
                solution[i][j] = e + min(solution[i-1][j-1], solution[i-1][j])
            else:
                solution[i][j] = e + min(solution[i-1][j-1], solution[i-1][j], solution[i-1][j+1])
    min_energy = math.inf
    min_pos = 0
    for j in range(m):
        if solution[n-1][j] <= min_energy:
            min_energy = solution[n-1][j]
            min_pos = j
    res = [0] * n
    res[n-1] = min_pos
    for i in range(n-1, 0, -1):
        prev = solution[i][min_pos] - energia[i][min_pos]
        if min_pos > 0 and math.isclose(solution[i-1][min_pos-1], prev):
            min_pos -= 1
        elif min_pos < m - 1 and math.isclose(solution[i-1][min_pos+1], prev):
            min_pos += 1
        res[i-1] = min_pos
    return res

def _eliminar_costura(imagen, seam):
    """Devuelve una nueva imagen con la costura eliminada."""
    img = np.array(imagen.convert("RGB"))
    n, m, c = img.shape
    nueva = np.zeros((n, m - 1, c), dtype=img.dtype)
    for i in range(n):
        col = seam[i]
        nueva[i] = np.delete(img[i], col, axis=0)
    return Image.fromarray(nueva)

def seam_carving_pd(imagen, k):
    """
    Recibe una imagen PIL y un entero k.
    Elimina k costuras de mínima energía usando Programación Dinámica.
    Devuelve la imagen resultante.
    """
    img_actual = imagen.copy()
    for i in range(k):
        print(f"  PD: eliminando costura {i + 1}/{k}...")
        energia = _calcular_energia(img_actual)
        seam = encontrar_seam_pd(energia)
        img_actual = _eliminar_costura(img_actual, seam)
    return img_actual