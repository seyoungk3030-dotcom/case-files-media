"""ROOM 110 proof: domino covering. A wooden board of R x C squares has some squares already cut out (holes). Four
squares are numbered. Take out exactly one numbered square; can the rest be covered exactly by 1x2 dominoes (no
overlap, nothing hanging over)? Exactly one numbered square works; its number is the digit. Covering is checked with
a bipartite matching on the checkerboard colouring (a full matching = a full domino cover). All 10^4 codes are
compared; exactly one matches. The trap: the other square that leaves equal 'black' and 'white' counts but still
can't be covered (a corner gets cut off). Boards from gen110 (seed 110)."""
import itertools, json, os

BOARDS = {'A': {'size': (6, 5), 'holes': [(0, 2), (1, 0), (5, 1)], 'num': [(1, 1), (2, 4), (0, 1), (3, 2)]},
          'B': {'size': (5, 6), 'holes': [(1, 0), (2, 0), (4, 2)], 'num': [(0, 1), (2, 5), (4, 0), (0, 2)]},
          'C': {'size': (5, 6), 'holes': [(1, 0), (4, 2), (4, 4)], 'num': [(0, 0), (0, 4), (1, 2), (0, 1)]},
          'D': {'size': (5, 6), 'holes': [(3, 4), (4, 1), (4, 4)], 'num': [(3, 1), (3, 5), (3, 0), (2, 5)]}}


def cover(cells):
    cells = set(cells); black = [c for c in cells if (c[0] + c[1]) % 2 == 0]; white = cells - set(black)
    if len(black) != len(white): return None
    match = {}
    def aug(u, seen):
        for d in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            v = (u[0] + d[0], u[1] + d[1])
            if v in white and v not in seen:
                seen.add(v)
                if v not in match or aug(match[v], seen): match[v] = u; return True
        return False
    if not all(aug(b, set()) for b in black): return None
    return sorted((u, v) for v, u in match.items())


def free(k):
    (R, C), holes = BOARDS[k]['size'], set(BOARDS[k]['holes'])
    return [(r, c) for r in range(R) for c in range(C) if (r, c) not in holes]


def solve(k):
    f = free(k); nums = BOARDS[k]['num']; assert not set(nums) & set(BOARDS[k]['holes'])
    ok = [i + 1 for i, n in enumerate(nums) if cover(set(f) - {n})]
    par = [i + 1 for i, n in enumerate(nums) if sum((a + b) % 2 == 0 for a, b in set(f) - {n}) * 2 == len(f) - 1]
    return ok, [p for p in par if p not in ok]


RES = {k: solve(k) for k in 'ABCD'}
assert all(len(v[0]) == 1 and len(v[1]) == 1 for v in RES.values())
code = ''.join(str(RES[k][0][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1][0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['4231'] and trap != code
if __name__ == '__main__':
    tiles = {k: cover(set(free(k)) - {BOARDS[k]['num'][RES[k][0][0] - 1]}) for k in 'ABCD'}
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'tiling': tiles, 'trap_parity_only': trap,
               'why': '체스판처럼 색칠하면 도미노 하나는 늘 검정 1칸 + 흰색 1칸. 두 색 수가 같아야 하고, 갇힌 칸이 없어야 해요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
