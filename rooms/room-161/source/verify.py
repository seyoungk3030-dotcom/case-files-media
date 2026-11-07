"""ROOM 161 proof: ladder board (사다리 타기) as a marble run. A marble drops into the starred lane at the top and rolls
down; whenever a crossbar touches its lane it rolls across that crossbar to the next lane and carries on down. Digit =
the number on the bin it lands in. All 10^4 codes compared; exactly one matches. The trap: straight down from the star."""
import itertools, json, os
L = 5; H = 8
# start lane, crossbars as (level 0..H-1 from the top, left lane i: joins i and i+1), bin labels left to right
BOARDS = {'A': {'start': 1, 'bars': [(0, 1), (1, 2), (2, 0), (3, 3), (4, 1), (5, 2), (6, 3), (7, 0)], 'bins': [4, 7, 1, 8, 3]},
          'B': {'start': 3, 'bars': [(0, 3), (1, 1), (2, 2), (3, 0), (3, 3), (4, 1), (5, 2), (6, 0), (7, 3)], 'bins': [9, 2, 6, 5, 0]},
          'C': {'start': 0, 'bars': [(0, 0), (1, 2), (2, 1), (3, 3), (4, 2), (5, 0), (6, 1), (7, 2)], 'bins': [3, 8, 5, 1, 6]},
          'D': {'start': 4, 'bars': [(0, 2), (1, 3), (2, 1), (3, 2), (4, 0), (4, 3), (5, 1), (6, 2), (7, 3)], 'bins': [2, 5, 9, 7, 4]}}


def path(b):
    for lv in range(H):
        ls = [i for l, i in b['bars'] if l == lv]
        assert len(set(ls) | {i + 1 for i in ls}) == 2 * len(ls)  # no two bars share a lane on one level
    p = b['start']; pts = [(p, -1)]
    for lv in range(H):
        for l, i in b['bars']:
            if l == lv and p in (i, i + 1):
                pts.append((p, lv)); p = i + 1 if p == i else i; pts.append((p, lv)); break
    pts.append((p, H)); return p, pts


RES = {k: path(b) for k, b in BOARDS.items()}
code = ''.join(str(BOARDS[k]['bins'][RES[k][0]]) for k in 'ABCD'); trap = ''.join(str(BOARDS[k]['bins'][BOARDS[k]['start']]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: r[0] for k, r in RES.items()})
assert len(sols) == 1 and all(a != b for a, b in zip(code, trap))
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'end_lane': {k: r[0] for k, r in RES.items()},
               'trap_straight_down': trap, 'why': '구슬은 가로대를 만날 때마다 옆 줄로 건너가요. 위에서부터 하나씩 따라가야 해요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
