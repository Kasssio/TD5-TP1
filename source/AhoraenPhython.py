import math

def _backtracking(energia, i, j, curr_path, curr_energy, best):
    n = len(energia)
    m = len(energia[0])

    curr_path.append(j)
    curr_energy += energia[i][j]

    if curr_energy >= best[1]:  # Poda de optimalidad
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
    best = [[], math.inf]  # [camino, energía mínima]

    for j in range(m):
        _backtracking(energia, 0, j, [], 0.0, best)

    return best[0]


"""Programación Dinámica:"""


def encontrar_seam_pd(energia):
    n = len(energia)
    m = len(energia[0])

    # Tabla bottom-up
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

    # Buscar mínimo en última fila
    min_energy = math.inf
    min_pos = 0
    for j in range(m):
        if solution[n-1][j] <= min_energy:
            min_energy = solution[n-1][j]
            min_pos = j

    # Reconstruir camino
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