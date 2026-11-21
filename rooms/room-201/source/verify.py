"""ROOM 201 proof (손전등 몇 개?): one torch 1 m from a poster gives brightness 1. Light spreads over an area that grows
with the square of the distance, so n identical torches at d metres give n / d^2. Each board asks how many torches at d m
give the brightness asked (same, double or half of the 1 m reference). Every n from 1 to 99 is tried; exactly one n per
board matches, and all 10^4 codes are compared. Trap: thinking brightness falls with the distance itself (2341)."""
import itertools, json, os
from fractions import Fraction as F

BOARDS = {'A': (2, F(1)), 'B': (3, F(1)), 'C': (2, F(2)), 'D': (2, F(1, 2))}  # distance m, target brightness


def bright(n, d): return F(n, d * d)


GOOD = {}
for k, (d, b) in BOARDS.items():
    ns = [n for n in range(1, 100) if bright(n, d) == b]; assert len(ns) == 1 and ns[0] < 10, (k, ns); GOOD[k] = ns[0]
code = ''.join(str(GOOD[k]) for k in 'ABCD')
trap = ''.join(str(int(d * b)) for d, b in (BOARDS[k] for k in 'ABCD'))
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(a != t for a, t in zip(code, trap))
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': {k: [d, str(b)] for k, (d, b) in BOARDS.items()}, 'torches': GOOD,
               'trap_linear_distance': trap, 'why': '빛은 거리의 제곱만큼 넓게 퍼져요. 2배 멀면 4배 넓게, 3배 멀면 9배 넓게'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
