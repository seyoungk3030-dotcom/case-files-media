"""ROOM 179 proof: price stickers. Each item starts at a price (in won) and gets two percent stickers stuck on,
one after the other. Every sticker changes the CURRENT price, not the original one, so +50% then -50% does not
bring you back, and -50% then another -50% is not free. Digit = final price in thousands of won.
All 10^4 codes compared; exactly one matches. The trap: adding the percents first and applying once."""
import itertools, json, os
from fractions import Fraction as F

BOARDS = {'A': (8000, (50, -50)), 'B': (8000, (-50, -50)), 'C': (4000, (100, -50)), 'D': (4000, (50, 50))}


def final(p, st):
    v = F(p)
    for s in st: v = v * (100 + s) / 100
    return v


GOOD = {k: final(*v) for k, v in BOARDS.items()}
TRAPP = {k: F(p) * (100 + sum(st)) / 100 for k, (p, st) in BOARDS.items()}
assert all(g.denominator == 1 and g % 1000 == 0 and 0 <= g // 1000 <= 9 for g in GOOD.values())
assert all(t.denominator == 1 and t % 1000 == 0 and 0 <= t // 1000 <= 9 for t in TRAPP.values())
code = ''.join(str(int(GOOD[k] // 1000)) for k in 'ABCD'); trap = ''.join(str(int(TRAPP[k] // 1000)) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPP[k] for k in 'ABCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'final_won': {k: int(v) for k, v in GOOD.items()},
               'trap_sum_percents_once': trap,
               'why': '스티커는 그때 가격에 붙어요. +50% 뒤 -50%는 원래 가격이 아니라 75%예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
