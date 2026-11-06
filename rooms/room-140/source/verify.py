"""ROOM 140 proof: peg solitaire on a 10-hole triangle (bowling-pin layout, holes 1-10 from the top, row by row; hole 10
reads as 0). A move: a peg jumps over a neighbouring peg in a straight line (along a row or either slanted side) into
an empty hole, and the jumped peg is removed. Keep jumping until ONE peg is left. Every jump order is searched; on each
board every order that ends with one peg ends in the same hole, so the digit is that hole number. All 10^4 codes are
compared; exactly one matches. The trap: 'the last peg falls into the first empty hole' (lowest empty hole)."""
import functools, itertools, json, os
P = [(r, i) for r in range(4) for i in range(r + 1)]
LAB = {p: n + 1 for n, p in enumerate(P)}; POS = {v: k for k, v in LAB.items()}
DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1)]
BOARDS = {'A': [1, 2, 3, 5, 8, 10], 'B': [1, 2, 4, 5, 6, 10], 'C': [1, 2, 3, 4, 5, 6, 8], 'D': [1, 2, 3, 4, 5, 6, 9]}


def moves(s):
    for (r, i) in sorted(s):
        for dr, di in DIRS:
            m, t = (r + dr, i + di), (r + 2 * dr, i + 2 * di)
            if m in s and t in LAB and t not in s: yield (LAB[(r, i)], LAB[m], LAB[t]), frozenset(s - {(r, i), m} | {t})


@functools.lru_cache(None)
def ends(s):
    if len(s) == 1: return frozenset(s)
    o = set()
    for _, n in moves(s): o |= ends(n)
    return frozenset(o)


def path(s):
    if len(s) == 1: return []
    for mv, n in moves(s):
        if ends(n): return [mv] + path(n)


RES = {}
for k, b in BOARDS.items():
    s = frozenset(POS[x] for x in b); e = ends(s); assert len(e) == 1, k
    RES[k] = (LAB[next(iter(e))] % 10, path(s))
code = ''.join(str(RES[k][0]) for k in 'ABCD')
trap = ''.join(str(min(h for h in range(1, 11) if h not in BOARDS[k]) % 10) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: v[1] for k, v in RES.items()})
assert sols == ['8264'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'solution': {k: v[1] for k, v in RES.items()},
               'trap_first_empty_hole': trap, 'why': '어떤 순서로 뛰어도 마지막 한 개는 같은 구멍에 남아요. 직접 한 번 따라가 보면 보여요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
