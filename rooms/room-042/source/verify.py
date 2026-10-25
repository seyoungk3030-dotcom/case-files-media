"""ROOM 042 proof: four standard dice (opposite faces add up to 7) are rolled along the arrows on their tiles.
→ = one roll to the right, ↓ = one roll toward the viewer. Code = the number on top after the rolls, dice A-D.
Each die's start is fixed by its visible top, front and right faces (dice.find asserts exactly one orientation), so
the top after rolling is fixed. Rolling the wrong way (left / away) gives the trap."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dice
ROLL = {'R': np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]), 'F': np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])}
DICE = {'A': ((1, 4, 2), 'R'), 'B': ((1, 3, 5), 'F'), 'C': ((4, 1, 5), 'RR'), 'D': ((3, 5, 1), 'FR')}


def roll(R, seq, back=False):
    for s in seq: R = (ROLL[s].T if back else ROLL[s]) @ R
    return R


START = {k: dice.find(*v) for k, (v, _) in DICE.items()}
END = {k: roll(START[k], DICE[k][1]) for k in DICE}
code = ''.join(str(dice.face_on(END[k], dice.UP)) for k in 'ABCD')
trap = ''.join(str(dice.face_on(roll(START[k], DICE[k][1], True), dice.UP)) for k in 'ABCD')
# every candidate 4-digit code except one disagrees with the simulation
sols = [c for c in (f'{a}{b}{c}{d}' for a in range(1, 7) for b in range(1, 7) for c in range(1, 7) for d in range(1, 7)) if c == code]
print('answer', code, 'trap', trap, 'solutions', sols)
assert sols == ['5436'] and trap != code
json.dump({'unique_answer': code, 'dice_top_front_right_and_rolls': {k: [list(v), s] for k, (v, s) in DICE.items()},
           'trap_wrong_direction': trap,
           'why': 'A → 왼쪽 면(7-2=5)이 위로 · B ↓ 뒷면(7-3=4)이 위로 · C →→ 바닥(7-4=3)이 위로 · D ↓→ 오른쪽 면은 그대로, → 에서 왼쪽 면(7-1=6)이 위로'},
          open(os.path.join(HERE, '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
