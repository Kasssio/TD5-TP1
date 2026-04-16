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

def _backtracking(energia, i, j, curr_path, curr_energy, best):
    n = len(energia)
    m = len(energia[0])
    curr_path.append(j)
    curr_energy += energia[i][j]
    if curr_energy >= best[1]:
        curr_path.pop()
        return
    if i == n - 1:
        best[0] = curr_path[:]
        best[1] = curr_energy
        curr_path.pop()
        return
    for k in [-1, 0, 1]:
        col = j + k
        if 0 <= col < m:
            _backtracking(energia, i + 1, col, curr_path, curr_energy, best)
    curr_path.pop()

def encontrar_seam_backtracking(energia):
    m = len(energia[0])
    best = [[], math.inf]
    for j in range(m):
        _backtracking(energia, 0, j, [], 0.0, best)
    return best[0]

def _eliminar_costura(imagen, seam):
    """Devuelve una nueva imagen con la costura eliminada."""
    img = np.array(imagen.convert("RGB"))
    n, m, c = img.shape
    nueva = np.zeros((n, m - 1, c), dtype=img.dtype)
    for i in range(n):
        col = seam[i]
        nueva[i] = np.delete(img[i], col, axis=0)
    return Image.fromarray(nueva)

def seam_carving_bt(imagen, k):
    """
    Recibe una imagen PIL y un entero k.
    Elimina k costuras de mínima energía usando Backtracking.
    Devuelve la imagen resultante.
    """
    img_actual = imagen.copy()
    for i in range(k):
        print(f"  BT: eliminando costura {i + 1}/{k}...")
        energia = _calcular_energia(img_actual)
        seam = encontrar_seam_backtracking(energia)
        img_actual = _eliminar_costura(img_actual, seam)
    return img_actual