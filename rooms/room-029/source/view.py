"""Which cubes of a 3x3 stack can be seen from the camera (orthographic, from the front-right-top).
A stack is a heightmap h[row][col], row 0 = front, col 0 = left; columns are solid (no floating cubes).
Same camera as kit/b3d.stack_camera(): azimuth AZ from the front, elevation EL."""
import itertools, math
import numpy as np

N, HMAX, AZ, EL = 3, 3, 33.0, 30.0
D = np.array([math.sin(math.radians(AZ)) * math.cos(math.radians(EL)), -math.cos(math.radians(AZ)) * math.cos(math.radians(EL)),
              math.sin(math.radians(EL))])                    # unit vector from the stack towards the camera
CELLS = [(i, j, k) for k in range(HMAX) for j in range(N) for i in range(N)]
IDX = {c: n for n, c in enumerate(CELLS)}


def _samples(i, j, k, m=4):
    g = [(a + 0.5) / m for a in range(m)]
    for u, v in itertools.product(g, g):
        yield (i + 1, j + u, k + v)        # right face (+x)
        yield (i + u, j, k + v)            # front face (-y)
        yield (i + u, j + v, k + 1)        # top face (+z)


def _occluders(p, own):
    out, t = set(), 0.01
    while t < 12:
        q = np.array(p) + D * t; c = (int(math.floor(q[0])), int(math.floor(q[1])), int(math.floor(q[2])))
        if c in IDX and c != own: out.add(IDX[c])
        t += 0.02
    return sorted(out)


OCC = [[_occluders(p, c) for p in _samples(*c)] for c in CELLS]


def filled(hs):
    """hs: flat heights row by row. Returns a bool per cell of CELLS."""
    return [hs[j * N + i] > k for (i, j, k) in CELLS]


def visible(hs):
    f = filled(hs)
    return {CELLS[n] for n in range(len(CELLS)) if f[n] and any(not any(f[o] for o in occ) for occ in OCC[n])}


def all_visible_sets():
    """Vectorised: for every heightmap (4^9), the frozen set of visible cells. Returns (heightmaps, list of sets)."""
    H = np.array(list(itertools.product(range(HMAX + 1), repeat=N * N)), dtype=np.int8)
    F = np.stack([H[:, j * N + i] > k for (i, j, k) in CELLS], axis=1)
    V = np.zeros_like(F)
    for n, occs in enumerate(OCC):
        seen = np.zeros(len(H), bool)
        for occ in occs:
            seen |= ~F[:, occ].any(axis=1) if occ else True
        V[:, n] = F[:, n] & seen
    return H, F, V
