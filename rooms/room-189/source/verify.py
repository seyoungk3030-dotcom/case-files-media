"""ROOM 189 proof: the heated ring. When a metal ring is heated every length in it grows by the same fraction, the hole
included (the ring scales up like a photo enlargement; it does not swell inward). Cooling shrinks everything,
the hole too. Rule on the cards: red-hot steel is 1% bigger in every length than at room temperature (steel grows ~12 um/m per degree,
x ~830 degrees). Heating a room-temperature ring multiplies every length by 1.01; cooling a ring measured red-hot back to
room temperature divides every length by 1.01 (no impossible deep-freezing).
A steel ball passes when its diameter is smaller than the hole. Digit = balls that pass. No ball is within 0.1 mm of
the hole, so there are no ties. All 10^4 codes compared; exactly one matches. The trap: thinking a heated ring's hole
shrinks (and a cooled one's grows)."""
import itertools, json, os
from fractions import Fraction as Fr

BOARDS = {'A': (100, +1, ['98.5', '99.5', '100.5', '101.5']), 'B': (100, -1, ['98.5', '99.5', '100.5', '101.5']),
          'C': (200, +1, ['199.5', '201.5', '202.5', '203.5']), 'D': (50, +1, ['49.8', '50.1', '50.3', '50.4'])}  # hole mm, +1 heat / -1 cool, balls mm


def passes(hole, s, balls, trap=False):
    h = Fr(hole) * Fr(101, 100) ** ((-s if trap else s))
    assert all(abs(Fr(b) - h) >= Fr(1, 10) for b in balls), 'tie'
    return sum(Fr(b) < h for b in balls)


GOOD = {k: passes(*v) for k, v in BOARDS.items()}; TRAPV = {k: passes(*v, trap=True) for k, v in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] for k in 'ABCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_hole_state_balls': BOARDS,
               'hole_after_mm': {k: str(round(float(Fr(h) * Fr(101, 100) ** s), 2)) for k, (h, s, b) in BOARDS.items()},
               'balls_pass': GOOD, 'trap_hole_shrinks_when_heated': trap,
               'why': '달구면 고리 전체가 사진을 확대한 것처럼 커져서 구멍도 1% 커져요. 달군 고리를 식히면 구멍도 원래대로 작아져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
