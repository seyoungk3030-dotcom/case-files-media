"""ROOM 100 proof: ropes lying on a table, seen from above; if both ends are pulled, does a real knot stay? Each rope
is a closed curve opened at its outermost point (the loose ends point away, so closing them adds no crossings). Its
crossings come from the drawing and the over/under choice is set per crossing. For every rope the Kauffman bracket is
computed exactly from the crossing code (state sum over all 2^n smoothings): a rope with at most 4 crossings is
unknotted exactly when its bracket is a single term +-A^m (the Jones polynomial detects every knot this small).
Each digit is the number of ropes that stay knotted. All 10^4 codes compared; exactly one matches. Counting the ropes
with 3 or more crossings (the trap) gives another code."""
import itertools, json, math, os
from collections import Counter
N = 1600


def base(kind, t):
    if kind == 'tref': return (math.sin(t) + 2 * math.sin(2 * t), math.cos(t) - 2 * math.cos(2 * t))
    if kind == 'fig8': return ((2 + math.cos(2 * t)) * math.cos(3 * t), (2 + math.cos(2 * t)) * math.sin(3 * t))
    if kind == 'loop1': r = 1.0 + 2.0 * math.cos(t); return (r * math.cos(t) - 1.0, r * math.sin(t))
    raise ValueError(kind)


def crossings(kind):
    P = [base(kind, 2 * math.pi * i / N) for i in range(N)]; out = []
    for i in range(N):
        a, b = P[i], P[(i + 1) % N]
        for j in range(i + 2, N):
            if i == 0 and j == N - 1: continue
            c, d = P[j], P[(j + 1) % N]
            den = (b[0] - a[0]) * (d[1] - c[1]) - (b[1] - a[1]) * (d[0] - c[0])
            if abs(den) < 1e-12: continue
            s = ((c[0] - a[0]) * (d[1] - c[1]) - (c[1] - a[1]) * (d[0] - c[0])) / den
            u = ((c[0] - a[0]) * (b[1] - a[1]) - (c[1] - a[1]) * (b[0] - a[0])) / den
            if 0 <= s < 1 and 0 <= u < 1:
                out.append(((i + s) / N * 2 * math.pi, (j + u) / N * 2 * math.pi, (b[0] - a[0], b[1] - a[1]), (d[0] - c[0], d[1] - c[1])))
    return out


def bracket(kind, over_first):
    X = crossings(kind); assert len(X) == len(over_first), (kind, len(X))
    occ = sorted([(t1, ci, 0) for ci, (t1, t2, _, _) in enumerate(X)] + [(t2, ci, 1) for ci, (t1, t2, _, _) in enumerate(X)])
    n2 = len(occ); pos = {(ci, w): m for m, (_, ci, w) in enumerate(occ)}
    PD = []
    for ci, (t1, t2, d1, d2) in enumerate(X):
        ov = 0 if over_first[ci] else 1; un = 1 - ov; du, dv = (d1, d2) if un == 0 else (d2, d1)
        mu, mo = pos[(ci, un)], pos[(ci, ov)]
        ends = [(math.atan2(-du[1], -du[0]), (mu - 1) % n2), (math.atan2(du[1], du[0]), mu),
                (math.atan2(-dv[1], -dv[0]), (mo - 1) % n2), (math.atan2(dv[1], dv[0]), mo)]
        a0 = ends[0][0]; ends.sort(key=lambda e: (e[0] - a0) % (2 * math.pi)); PD.append([e[1] for e in ends])
    poly = Counter()
    for st in itertools.product((0, 1), repeat=len(PD)):
        par = list(range(n2))
        def f(x):
            while par[x] != x: par[x] = par[par[x]]; x = par[x]
            return x
        for (i, j, k, l), s in zip(PD, st):
            pairs = ((i, j), (k, l)) if s == 0 else ((i, l), (j, k))
            for a, b in pairs: par[f(a)] = f(b)
        loops = len({f(x) for x in range(n2)}); na = st.count(0); nb = len(st) - na
        d = Counter({0: 1})
        for _ in range(loops - 1):
            nd = Counter()
            for e, c in d.items(): nd[e + 2] -= c; nd[e - 2] -= c
            d = nd
        for e, c in d.items(): poly[e + na - nb] += c
    return {e: c for e, c in poly.items() if c}


# board -> ropes: (shape, over pattern per crossing in crossing order; True = first-visited strand on top)
BOARDS = {'A': [('tref', (True, False, True)), ('fig8', (True, False, True, True))],
          'B': [('tref', (True, True, True)), ('fig8', (True, True, False, True))],
          'C': [('fig8', (True, True, True, True)), ('loop1', (False,))],
          'D': [('fig8', (False, True, False, False)), ('tref', (False, True, False))]}


def knotted(kind, ov): return len(bracket(kind, ov)) > 1


RES = {k: [knotted(*r) for r in v] for k, v in BOARDS.items()}
code = ''.join(str(sum(RES[k])) for k in 'ABCD'); trap = ''.join(str(sum(len(o) >= 3 for _, o in v)) for v in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, RES)
assert sols == ['2102'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'knotted': RES,
               'brackets': {k: [sorted(bracket(*r).items()) for r in v] for k, v in BOARDS.items()}, 'trap_3plus_crossings': trap,
               'why': '겹친 곳이 많아도 위·아래가 번갈아 엮이지 않으면 당기면 풀려요. 카우프만 괄호(존스 다항식)로 하나하나 확인'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
