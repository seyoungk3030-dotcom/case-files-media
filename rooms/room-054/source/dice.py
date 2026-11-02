"""A standard die and its 24 orientations. Base: 1 up, 2 toward the viewer (front, -y), 3 on the right (+x);
opposite faces add up to 7. An orientation is a 3x3 rotation matrix; face_on(R, n) is the number facing direction n."""
import itertools
import numpy as np

BASE = {(0, 0, 1): 1, (0, 0, -1): 6, (0, -1, 0): 2, (0, 1, 0): 5, (1, 0, 0): 3, (-1, 0, 0): 4}
UP, DOWN, FRONT, BACK, RIGHT, LEFT = (0, 0, 1), (0, 0, -1), (0, -1, 0), (0, 1, 0), (1, 0, 0), (-1, 0, 0)


def rotations():
    out = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            R = np.zeros((3, 3), int)
            for r, (c, s) in enumerate(zip(perm, signs)): R[r, c] = s
            if round(np.linalg.det(R)) == 1: out.append(R)
    return out


def face_on(R, n):
    """Number shown in world direction n after rotating the base die by R."""
    local = tuple(int(v) for v in R.T @ np.array(n))
    return BASE[local]


def view(R):
    return face_on(R, UP), face_on(R, FRONT), face_on(R, RIGHT)


def find(top, front, right):
    m = [R for R in rotations() if view(R) == (top, front, right)]
    assert len(m) == 1, (top, front, right, len(m))
    return m[0]
