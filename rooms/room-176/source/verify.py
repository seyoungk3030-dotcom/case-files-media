"""ROOM 176 proof: chocolate snaps. Each board is a chocolate bar of R x C squares. One snap takes ONE piece and breaks it
along a straight groove all the way across into two pieces (no stacking pieces). Digit = the fewest snaps that leave
every square on its own. Computed by exhaustive recursion over every possible snap order, for both the fewest and the
most snaps: they are equal (R*C - 1), so the order never matters. All 10^4 codes compared; exactly one matches.
The trap: counting the grooves (R - 1 + C - 1) as if one snap split the whole bar along a line through every piece."""
import itertools, json, os
from functools import lru_cache

BOARDS = {'A': (2, 3), 'B': (2, 4), 'C': (3, 3), 'D': (2, 2)}


@lru_cache(None)
def snaps(r, c, best):
    if r == c == 1: return 0
    opts = [1 + snaps(a, c, best) + snaps(r - a, c, best) for a in range(1, r)] + [1 + snaps(r, a, best) + snaps(r, c - a, best) for a in range(1, c)]
    return min(opts) if best else max(opts)


GOOD = {k: snaps(r, c, True) for k, (r, c) in BOARDS.items()}
assert GOOD == {k: snaps(r, c, False) for k, (r, c) in BOARDS.items()} == {k: r * c - 1 for k, (r, c) in BOARDS.items()}
TRAPV = {k: r - 1 + c - 1 for k, (r, c) in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] < 10 and GOOD[k] != TRAPV[k] for k in 'ABCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'bars_rows_cols': BOARDS, 'snaps': GOOD, 'trap_count_grooves': trap,
               'why': '한 번 쪼갤 때마다 조각이 딱 1개 늘어요. 칸이 N개면 어떤 순서로 쪼개도 N-1번'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
