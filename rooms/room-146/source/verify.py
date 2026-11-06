"""ROOM 146 proof: bulbs, switches and a battery wired as a ladder. The battery sits between the top-left and
bottom-left corners. The top rail runs over columns 1-3 (each piece: W wire or L bulb); the bottom rail is plain wire.
Each column has a rung from top to bottom made of pieces in series (L bulb, S closed switch, O open switch). All bulbs
are identical. A bulb lights when current flows through it, i.e. there is a voltage across it. Node voltages are
solved exactly (wires and closed switches join nodes; bulbs are equal resistors). Digit = number of lit bulbs. All 10^4
codes compared; exactly one matches. The trap: counting every bulb whose own wire has no open switch - forgetting
that a closed switch on its own is a short cut that steals all the current."""
import itertools, json, os
from fractions import Fraction as F
BOARDS = {'A': {'top': 'WLW', 'rungs': ['LL', 'LL', 'S']},
          'B': {'top': 'LWW', 'rungs': ['S', 'LL', 'LL']},
          'C': {'top': 'LWL', 'rungs': ['LL', 'LL', 'SO']},
          'D': {'top': 'WLL', 'rungs': ['L', 'S', 'LL']}}


def build(b):
    """edges (a, b, kind, label); bulbs labelled ('top', i) or ('rung', j, t)."""
    E = []
    for i, e in enumerate(b['top']): E.append((f'T{i}', f'T{i + 1}', e, ('top', i)))
    for i in range(3): E.append((f'B{i}', f'B{i + 1}', 'W', None))
    for j, r in enumerate(b['rungs'], 1):
        prev = f'T{j}'
        for t, e in enumerate(r):
            nxt = f'B{j}' if t == len(r) - 1 else f'R{j}{t}'; E.append((prev, nxt, e, ('rung', j, t))); prev = nxt
    return E


def solve(b):
    E = build(b); par = {}
    def f(x):
        par.setdefault(x, x)
        while par[x] != x: x = par[x]
        return x
    for a, c, e, _ in E:
        f(a); f(c)
        if e in 'WS': par[f(a)] = f(c)
    P, M = f('T0'), f('B0'); assert P != M, 'battery shorted'
    nodes = sorted({f(x) for x in par}); free = [n for n in nodes if n not in (P, M)]
    R = [(f(a), f(c)) for a, c, e, _ in E if e == 'L' and f(a) != f(c)]
    # Gauss elimination with fractions on the free nodes (V(P)=1, V(M)=0); a node with no bulb link is left at 0 (no current)
    V = {P: F(1), M: F(0)}; idx = {n: i for i, n in enumerate(free)}; m = len(free)
    A = [[F(0)] * m for _ in range(m)]; y = [F(0)] * m
    for a, c in R:
        for u, v in ((a, c), (c, a)):
            if u in idx:
                A[idx[u]][idx[u]] += 1
                if v in idx: A[idx[u]][idx[v]] -= 1
                else: y[idx[u]] += V[v]
    for i in range(m):
        if A[i][i] == 0: A[i][i] = F(1)  # isolated node
    for i in range(m):
        p = next(r for r in range(i, m) if A[r][i] != 0); A[i], A[p] = A[p], A[i]; y[i], y[p] = y[p], y[i]
        for r in range(m):
            if r != i and A[r][i] != 0:
                k = A[r][i] / A[i][i]; A[r] = [x - k * z for x, z in zip(A[r], A[i])]; y[r] -= k * y[i]
    for n, i in idx.items(): V[n] = y[i] / A[i][i]
    return {lab: V[f(a)] != V[f(c)] for a, c, e, lab in E if e == 'L'}


LIT = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(sum(LIT[k].values())) for k in 'ABCD')
trap = ''.join(str(b['top'].count('L') + sum(r.count('L') for r in b['rungs'] if 'O' not in r)) for k, b in BOARDS.items())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: [lab for lab, on in v.items() if on] for k, v in LIT.items()})
assert sols == ['3152'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'lit': {k: [list(l) for l, on in v.items() if on] for k, v in LIT.items()},
               'trap_ignore_short': trap, 'why': '닫힌 스위치만 있는 줄은 저항이 없는 지름길이라 전류가 전부 그쪽으로 빠져요. 그 너머 전구는 꺼져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
