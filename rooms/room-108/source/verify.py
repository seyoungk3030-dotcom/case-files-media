"""ROOM 108 proof: mental rotation (Shepard-Metzler style). Each board has a reference block shape (unit cubes) and
four numbered shapes. Exactly one numbered shape is the reference turned in space (one of the 24 rotations); one is
its mirror image (turned too), which no rotation can produce because the reference is chiral; two have one cube
moved. Each digit is the number of the turned copy. All 10^4 codes are compared; exactly one matches. Picking the
mirror image (the trap) gives another code. Shapes are built from a seed and every claim is re-checked here."""
import itertools, json, os, random

def rots():
    out = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product((1, -1), repeat=3):
            m = [[0] * 3 for _ in range(3)]
            for i in range(3): m[i][perm[i]] = sg[i]
            det = (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                   + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
            if det == 1: out.append(m)
    return out


ROTS = rots(); assert len(ROTS) == 24


def app(m, p): return tuple(sum(m[i][j] * p[j] for j in range(3)) for i in range(3))


def norm(s):
    mn = [min(p[i] for p in s) for i in range(3)]; return tuple(sorted(tuple(p[i] - mn[i] for i in range(3)) for p in s))


def canon(s): return min(norm([app(m, p) for p in s]) for m in ROTS)


def mirror(s): return [(-x, y, z) for x, y, z in s]


# reference arms: list of (axis, length) walked from the origin, Shepard-Metzler style
ARMS = {'A': [(0, 3), (1, 2), (2, 2), (0, -2)], 'B': [(2, 3), (0, 2), (1, 3), (2, -1)],
        'C': [(1, 3), (0, -2), (2, 2), (1, 2)], 'D': [(0, 2), (2, 3), (1, -2), (0, 2)]}
ORDER = {'A': 'MDRD', 'B': 'DRMD', 'C': 'RMDD', 'D': 'DDMR'}     # what sits at numbers 1-4: R turned, M mirror, D decoy


def walk(arms):
    p = [0, 0, 0]; out = [tuple(p)]
    for ax, n in arms:
        for _ in range(abs(n)): p[ax] += 1 if n > 0 else -1; out.append(tuple(p))
    assert len(set(out)) == len(out); return out


def board(k, seed):
    rng = random.Random(seed); ref = walk(ARMS[k]); assert canon(ref) != canon(mirror(ref))
    shapes = []; decoy_i = 0
    for t in ORDER[k]:
        if t == 'R': s = ref
        elif t == 'M': s = mirror(ref)
        else:
            arms = [list(a) for a in ARMS[k]]; j = [1, 2][decoy_i]; decoy_i += 1
            arms[j][1] += 1 if arms[j][1] > 0 else -1; s = walk([tuple(a) for a in arms])
        m = rng.choice(ROTS[1:]); shapes.append(norm([app(m, p) for p in s]))
    return norm(ref), shapes


SEEDS = {'A': 81, 'B': 82, 'C': 83, 'D': 84}
B = {k: board(k, SEEDS[k]) for k in 'ABCD'}


def judge(k):
    ref, shapes = B[k]; same = [i + 1 for i, s in enumerate(shapes) if canon(s) == canon(ref)]
    mir = [i + 1 for i, s in enumerate(shapes) if canon(s) == canon(mirror(ref))]
    for i, s in enumerate(shapes):
        assert s != ref, 'a candidate may not be shown unturned'
    return same, mir


RES = {k: judge(k) for k in 'ABCD'}
assert all(len(v[0]) == 1 and len(v[1]) == 1 for v in RES.values())
code = ''.join(str(RES[k][0][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1][0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['3214'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'arms': ARMS, 'order': ORDER, 'shapes': {k: {'ref': B[k][0], 'cands': B[k][1]} for k in 'ABCD'},
               'trap_mirror': trap, 'why': '돌려서 겹치는 건 하나뿐. 거울에 비친 모양은 아무리 돌려도 겹치지 않아요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
