"""ROOM 193 proof (마른 수박): produce is weighed, then dried until its water share drops a few points. The dry part never
changes, so new weight = weight x (1 - old water %) / (1 - new water %). Water 92% -> 84% means the dry 8% becomes 16%
of the whole: the weight halves. Digit = new weight in kg (all exact). All 10^4 codes compared; exactly one matches.
The trap: thinking the weight drops only by the water points (10 kg x 0.92 = 9.2 kg)."""
import itertools, json, os
from fractions import Fraction as F

BOARDS = {'A': ('수박', 10, 92, 84), 'B': ('오이', 9, 96, 88), 'C': ('토마토', 8, 95, 90), 'D': ('배추', 18, 95, 90)}  # name, kg, water % before, after


def after(w, p0, p1): return F(w) * (100 - p0) / (100 - p1)


GOOD = {}
for k, (n, w, p0, p1) in BOARDS.items():
    a = after(w, p0, p1); assert a.denominator == 1 and 0 < a < 10, (k, a); GOOD[k] = int(a)
TRAPV = {k: round(BOARDS[k][1] * (100 - (BOARDS[k][2] - BOARDS[k][3])) / 100, 2) for k in 'ABCD'}
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', TRAPV)
assert len(sols) == 1 and len(set(code)) == 4
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'kg_after': GOOD,
               'trap_minus_water_points_kg': TRAPV,
               'why': '마른 부분 무게는 그대로. 수박 10kg의 8%(0.8kg)가 마른 부분인데, 말린 뒤엔 그게 16%라서 전체는 5kg'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
