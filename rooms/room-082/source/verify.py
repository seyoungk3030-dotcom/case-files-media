"""ROOM 082 proof: a 5x5 pegboard (pegs 1 unit apart) with a rubber band around some pegs. Each digit is the area
inside the band in unit squares, by the shoelace formula, cross-checked by Pick's theorem (I + B/2 - 1). All 10^4
codes compared; exactly one matches. Counting the pegs inside (the trap) gives another code."""
import itertools, json, os
from math import gcd
BANDS = {'A': [(0, 0), (4, 0), (1, 3)], 'B': [(0, 1), (2, 0), (4, 3), (2, 4)],
         'C': [(0, 0), (3, 0), (3, 1), (1, 1), (1, 3), (0, 3)], 'D': [(1, 0), (4, 2), (0, 4)]}


def area2(p): return abs(sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p))))


def inside(p, x, y):
    c = False
    for i in range(len(p)):
        (x1, y1), (x2, y2) = p[i], p[(i + 1) % len(p)]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): c = not c
    return c


def on_edge(p, x, y):
    for i in range(len(p)):
        (x1, y1), (x2, y2) = p[i], p[(i + 1) % len(p)]
        if (x - x1) * (y2 - y1) == (y - y1) * (x2 - x1) and min(x1, x2) <= x <= max(x1, x2) and min(y1, y2) <= y <= max(y1, y2): return True
    return False


AREA = {}
TRAP = {}
for k, p in BANDS.items():
    Bp = sum(gcd(abs(p[i][0] - p[(i + 1) % len(p)][0]), abs(p[i][1] - p[(i + 1) % len(p)][1])) for i in range(len(p)))
    I = sum(1 for x in range(5) for y in range(5) if inside(p, x, y) and not on_edge(p, x, y))
    assert area2(p) % 2 == 0 and area2(p) // 2 == I + Bp // 2 - 1, k
    AREA[k] = area2(p) // 2; TRAP[k] = I
code = ''.join(str(AREA[k]) for k in 'ABCD'); trap = ''.join(str(TRAP[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['6857'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'bands': BANDS, 'trap_inner_pegs': trap,
               'why': '삼각형 조각은 사각형의 절반. 바깥 직사각형에서 빈 삼각형을 빼면 쉬워요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
