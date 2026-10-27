"""ROOM 049 proof: four taps A-D at the top, six cups 1-6 at the bottom, and four tangled pipes of the same colour.
Code = the cup each tap's pipe pours into, A B C D. Each pipe is traced by sampling its smooth curve (the same NURBS
the render uses) from the tap down to its open end; the cup under that end is the answer. The trap picks the cup
straight below each tap."""
import json, os
import numpy as np
CUPS = {n: x for n, x in zip(range(1, 7), (-3.75, -2.25, -0.75, 0.75, 2.25, 3.75))}
TAPS = {'A': -3.75, 'B': -0.75, 'C': 0.75, 'D': 3.75}
Z = [2.7, 2.2, 1.3, 0.4, -0.5, -1.4, -1.9]
PIPES = {   # x of each waypoint, top to bottom (first = tap, last two = above the cup it pours into)
 'A': [-3.75, -3.75, -1.5, 1.6, 2.6, 0.75, 0.75],
 'B': [-0.75, -0.75, 1.8, -2.4, 0.2, 3.75, 3.75],
 'C': [0.75, 0.75, -2.8, -0.2, 2.9, -3.75, -3.75],
 'D': [3.75, 3.75, 3.3, 2.4, -2.8, -0.75, -0.75],
}


def bspline(pts, n=400, k=3):
    """Clamped uniform B-spline (what Blender's NURBS with endpoint on draws)."""
    pts = np.asarray(pts, float); m = len(pts)
    t = np.concatenate([[0] * k, np.linspace(0, 1, m - k + 1), [1] * k])
    def N(i, p, u):
        if p == 0: return 1.0 if (t[i] <= u < t[i + 1]) or (u == 1 and t[i] < t[i + 1] == 1) else 0.0
        a = 0 if t[i + p] == t[i] else (u - t[i]) / (t[i + p] - t[i]) * N(i, p - 1, u)
        b = 0 if t[i + p + 1] == t[i + 1] else (t[i + p + 1] - u) / (t[i + p + 1] - t[i + 1]) * N(i + 1, p - 1, u)
        return a + b
    return np.array([sum(N(i, k, u) * pts[i] for i in range(m)) for u in np.linspace(0, 1, n)])


def trace(k):
    c = bspline(list(zip(PIPES[k], Z)))
    end = c[-1]; cup = min(CUPS, key=lambda n: abs(CUPS[n] - end[0]))
    assert abs(CUPS[cup] - end[0]) < 0.2 and abs(c[0][0] - TAPS[k]) < 1e-6
    return cup, c


res = {k: trace(k)[0] for k in 'ABCD'}
code = ''.join(str(res[k]) for k in 'ABCD')
trap = ''.join(str(min(CUPS, key=lambda n: abs(CUPS[n] - TAPS[k]))) for k in 'ABCD')
print(res, code, trap)
assert len(set(res.values())) == 4 and code == '4613' and all(a != b for a, b in zip(code, trap))
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'trap_straight_down': trap, 'taps_to_cups': res,
               'why': '파이프 네 개를 수도꼭지부터 끝까지 따라가면 A→4, B→6, C→1, D→3. 바로 아래 컵(1346)은 함정.'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
