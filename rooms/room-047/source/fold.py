import numpy as np
RY = np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]])     # roll east: bottom (0,0,-1) -> +x, east (1,0,0) -> top
RX = np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])     # roll north (+y): bottom -> +y


def fold(cells, start):
    """Fold a cube net lying flat: start cell is the bottom face. Returns {cell: outward normal}."""
    R = {start: np.eye(3, dtype=int)}; todo = [start]
    steps = {(1, 0): RY, (-1, 0): RY.T, (0, 1): RX, (0, -1): RX.T}
    while todo:
        c = todo.pop()
        for (dx, dy), M in steps.items():
            n = (c[0] + dx, c[1] + dy)
            if n in cells and n not in R: R[n] = R[c] @ M; todo.append(n)
    N = {c: tuple(int(v) for v in R[c] @ np.array([0, 0, -1])) for c in cells}
    assert len(R) == 6 and len(set(N.values())) == 6, 'not a cube net'
    return N
