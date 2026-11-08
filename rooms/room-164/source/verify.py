"""ROOM 164 proof: jigsaw. A 3x3 jigsaw has one empty slot. Every side of a piece is flat (F, on the frame edge), a tab
(T, sticks out) or a blank (B, cut in). A piece fits the slot when, after turning it (0/90/180/270 degrees, never
flipped face-down), each of its sides is the opposite of the neighbour it touches (tab against blank) and flat on the
frame edge. Sides are listed top, right, bottom, left. Four numbered loose pieces lie beside the board; digit = the
number on the one that fits. All 10^4 codes compared; exactly one matches. The trap: the mirror-image piece (fits only
if flipped over)."""
import itertools, json, os, random
OPP = {'T': 'B', 'B': 'T'}


def rot(p, k):  # turn clockwise k times: new top = old left
    p = list(p)
    for _ in range(k): p = [p[3], p[0], p[1], p[2]]
    return tuple(p)


def mirror(p): return (p[0], p[3], p[2], p[1])


def make(seed, hole):
    rnd = random.Random(seed)
    h = [[rnd.choice('TB') for c in range(2)] for r in range(3)]  # edge right of (r,c)
    v = [[rnd.choice('TB') for c in range(3)] for r in range(2)]  # edge below (r,c)
    P = {}
    for r in range(3):
        for c in range(3):
            top = 'F' if r == 0 else OPP[v[r - 1][c]]; bot = 'F' if r == 2 else v[r][c]
            right = 'F' if c == 2 else h[r][c]; left = 'F' if c == 0 else OPP[h[r][c - 1]]
            P[(r, c)] = (top, right, bot, left)
    return P


def fits(need, p): return [k for k in range(4) if rot(p, k) == need]


SPEC0 = {'A': (11, (1, 0), [5, 2, 8, 3], 2), 'B': (23, (0, 1), [7, 1, 4, 9], 0), 'C': (37, (1, 2), [6, 0, 3, 5], 3), 'D': (41, (2, 1), [2, 9, 4, 7], 1)}
SPEC = {}
for k, (seed, hole, digits, good) in SPEC0.items():  # first seed from the given one whose empty slot is mirror-asymmetric
    while True:
        n = make(seed, hole)[hole]
        if mirror(n) not in {rot(n, i) for i in range(4)}: break
        seed += 1
    SPEC[k] = (seed, hole, digits, good)
BOARDS = {}
for k, (seed, hole, digits, good) in SPEC.items():
    P = make(seed, hole); need = P[hole]; rnd = random.Random(seed * 7)
    assert mirror(need) not in {rot(need, i) for i in range(4)}, (k, need)  # chiral, so the mirror is a real trap
    loose = []
    trap_i = (good + 2) % 4
    for i in range(4):
        if i == good: p = rot(need, rnd.randrange(1, 4))
        elif i == trap_i: p = rot(mirror(need), rnd.randrange(4))
        else:
            while True:
                p = tuple(rnd.choice('TBF') for _ in range(4))
                if p.count('F') <= need.count('F') and not fits(need, p) and not fits(need, mirror(p)) and p not in loose: break
        loose.append(p)
    BOARDS[k] = {'grid': {f'{r}{c}': ''.join(P[(r, c)]) for r in range(3) for c in range(3)}, 'hole': list(hole),
                 'loose': [''.join(p) for p in loose], 'digits': digits, 'need': ''.join(need)}
GOOD = {}; TRAPD = {}
for k, b in BOARDS.items():
    ok = [i for i, p in enumerate(b['loose']) if fits(tuple(b['need']), tuple(p))]
    fl = [i for i, p in enumerate(b['loose']) if not fits(tuple(b['need']), tuple(p)) and fits(tuple(b['need']), mirror(tuple(p)))]
    assert len(ok) == 1 and len(fl) == 1, (k, ok, fl)
    GOOD[k] = ok[0]; TRAPD[k] = fl[0]
code = ''.join(str(BOARDS[k]['digits'][GOOD[k]]) for k in 'ABCD'); trap = ''.join(str(BOARDS[k]['digits'][TRAPD[k]]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: (b['need'], b['loose']) for k, b in BOARDS.items()})
assert len(sols) == 1 and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'fit_index': GOOD, 'trap_flipped': trap,
               'why': '조각은 돌릴 수만 있고 뒤집을 수는 없어요. 거울처럼 뒤집어야 맞는 조각이 함정이에요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
