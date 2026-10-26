"""ROOM 045 proof: in each setup A-D a row of meshing gears. The first (driver) gear turns a quarter turn clockwise
(seen from above). Meshing gears turn the opposite way, by (teeth of the gear before) / (own teeth) times as much.
The last gear's arrow starts at 1 (up); dial 1 up, 2 right, 3 down, 4 left. Code = where the arrow ends in A-D.
Ignoring the direction flips (everything clockwise) gives the trap."""
import json, os
from fractions import Fraction
SETUPS = {'A': [16, 8, 8], 'B': [24, 8, 8, 8], 'C': [8, 8], 'D': [32, 8, 8]}   # teeth along the row, driver first
DIAL = {0: 1, 1: 2, 2: 3, 3: 4}                                    # clockwise quarter turns from up -> dial number


def final_turn(teeth):
    """Signed quarter turns of the last gear (+ = clockwise), simulated gear by gear."""
    q = Fraction(1)
    for a, b in zip(teeth, teeth[1:]): q = -q * Fraction(a, b)
    assert q.denominator == 1
    return int(q)


res = {k: final_turn(v) for k, v in SETUPS.items()}
code = ''.join(str(DIAL[res[k] % 4]) for k in 'ABCD')
trap = ''.join(str(DIAL[abs(res[k]) % 4]) for k in 'ABCD')
print(res, code, trap)
assert code == '3241' and trap != code
json.dump({'unique_answer': code, 'teeth': SETUPS, 'final_quarter_turns_clockwise': res, 'trap_ignore_direction': trap,
           'why': '맞물린 톱니는 반대로 돈다. 회전량 = 첫 톱니 수 / 마지막 톱니 수. A 16/8=2칸 시계(3), B 24/8=3칸 반시계(2), C 8/8=1칸 반시계(4), D 32/8=4칸=한 바퀴(1). 중간 기어는 방향만 바꾼다'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
