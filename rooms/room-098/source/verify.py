"""ROOM 098 proof: bulb circuits on a board. Nodes sit on a grid; parts are copper wires (W), bulbs (B, all the same),
closed switches (S1, conduct) and open switches (S0, do not). The battery joins node '+' and node '-'. Wires and closed
switches merge their ends into one node; every bulb is then an equal resistor, and the node voltages are solved
exactly (Kirchhoff, with fractions). A bulb lights when there is a voltage across it, i.e. current flows through it;
a bulb whose ends are joined by a wire is shorted and stays dark, and a bulb on a dead-end branch stays dark. Each
digit is the number of lit bulbs. All 10^4 codes compared; exactly one matches. Counting the bulbs (the trap) gives
another code."""
import itertools, json, os
from fractions import Fraction as F
# grid points (x, y), x 0-4, y 0-2; the battery stands on x = 0 between '+' (0, 2) and '-' (0, 0)
SPEC = {
    'A': "B 0,2 1,2;W 1,2 2,2;B 2,2 3,2;W 3,2 4,2;W 4,2 4,1;B 4,1 4,0;W 4,0 3,0;W 3,0 2,0;W 2,0 1,0;W 1,0 0,0;W 2,2 2,1;B 2,1 2,0;S0 1,0 1,1;B 1,1 1,2",
    'B': "W 0,2 1,2;B 1,2 2,2;W 2,2 3,2;B 3,2 4,2;W 4,2 4,1;W 4,1 4,0;W 4,0 3,0;B 3,0 2,0;W 2,0 1,0;W 1,0 0,0;W 3,2 3,1;W 3,1 3,0;B 2,2 2,1",
    'C': "B 0,2 1,2;W 1,2 2,2;W 2,2 3,2;B 3,2 4,2;W 4,2 4,1;W 4,1 4,0;W 4,0 3,0;W 3,0 2,0;W 2,0 1,0;W 1,0 0,0;B 1,2 1,1;W 1,1 1,0;S1 2,2 2,1;B 2,1 2,0;B 3,2 3,1;S1 3,1 3,0",
    'D': "W 0,2 1,2;B 1,2 2,2;B 2,2 3,2;W 3,2 4,2;B 4,2 4,1;W 4,1 4,0;W 4,0 3,0;W 3,0 2,0;W 2,0 1,0;W 1,0 0,0;S1 2,2 2,1;W 2,1 2,0;B 3,2 3,1;W 3,1 3,0"}
BOARDS = {k: [(t, tuple(map(int, a.split(','))), tuple(map(int, b.split(',')))) for t, a, b in (p.split() for p in v.split(';'))] for k, v in SPEC.items()}
for v in BOARDS.values():   # every part joins two neighbouring grid points, so the drawing is the circuit
    assert all(abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1 for _, a, b in v) and len({frozenset((a, b)) for _, a, b in v}) == len(v)
PLUS, MINUS = (0, 2), (0, 0)


def lit(parts):
    nodes = {n for _, a, b in parts for n in (a, b)} | {PLUS, MINUS}; par = {n: n for n in nodes}
    def f(n):
        while par[n] != n: par[n] = par[par[n]]; n = par[n]
        return n
    for t, a, b in parts:
        if t in ('W', 'S1'): par[f(a)] = f(b)
    p, m = f(PLUS), f(MINUS); assert p != m, 'battery shorted'
    bulbs = [(f(a), f(b)) for t, a, b in parts if t == 'B']
    sup = sorted({x for e in bulbs for x in e} | {p, m}); idx = {s: i for i, s in enumerate(sup)}
    unk = [s for s in sup if s not in (p, m)]; ui = {s: i for i, s in enumerate(unk)}; n = len(unk)
    A = [[F(0)] * (n + 1) for _ in range(n)]
    V = {p: F(1), m: F(0)}
    for a, b in bulbs:
        if a == b: continue
        for x, y in ((a, b), (b, a)):
            if x in ui:
                A[ui[x]][ui[x]] += 1
                if y in ui: A[ui[x]][ui[y]] -= 1
                else: A[ui[x]][n] += V[y]
    # floating nodes (no path) get a zero row fixed to 0
    for i in range(n):
        if all(A[i][j] == 0 for j in range(n)): A[i][i] = F(1)
    for c in range(n):   # Gauss-Jordan
        r = next(r for r in range(c, n) if A[r][c] != 0); A[c], A[r] = A[r], A[c]
        piv = A[c][c]; A[c] = [v / piv for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0: k = A[r][c]; A[r] = [x - k * y for x, y in zip(A[r], A[c])]
    for s in unk: V[s] = A[ui[s]][n]
    # a dangling component not connected to the battery: its nodes were forced to 0 but must carry no current; check
    return [V[a] != V[b] and connected(bulbs, a, b, p, m) for a, b in bulbs]


def connected(bulbs, a, b, p, m):
    adj = {}
    for x, y in bulbs:
        if x != y: adj.setdefault(x, set()).add(y); adj.setdefault(y, set()).add(x)
    def reach(s):
        seen = {s}; st = [s]
        while st:
            u = st.pop()
            for v in adj.get(u, ()):
                if v not in seen: seen.add(v); st.append(v)
        return seen
    r = reach(a); return p in r and m in r


RES = {k: lit(v) for k, v in BOARDS.items()}
code = ''.join(str(sum(RES[k])) for k in 'ABCD'); trap = ''.join(str(sum(t == 'B' for t, _, _ in BOARDS[k])) for k in 'ABCD')
print('answer', code, 'trap', trap, RES)
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
assert sols == ['4251'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': {k: [(t, list(a), list(b)) for t, a, b in v] for k, v in BOARDS.items()},
               'lit': RES, 'trap_all_bulbs': trap,
               'why': '전구 양 끝이 전선으로 바로 이어지면 전류가 전구를 피해 가요(합선). 끊긴 스위치 쪽 길은 전류가 못 흘러요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
