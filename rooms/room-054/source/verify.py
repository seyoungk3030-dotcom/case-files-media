"""ROOM 054 proof: four standard dice (opposite faces add up to 7) are rolled along the arrows on their tiles.
→ = one roll to the right, ↓ = one roll toward the viewer. Code = the number on top after the rolls, dice A-D.
Each die's start is fixed by its visible top, front and right faces (dice.find asserts exactly one orientation), so
the top after rolling is fixed. Rolling the wrong way (left / away) gives the trap."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dice
ROLL = {'R': np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]), 'F': np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]])}
DICE = {'A': ((6, 5, 3), 'F'), 'B': ((2, 3, 1), 'FR'), 'C': ((3, 2, 6), 'RRF'), 'D': ((5, 3, 6), 'RF')}


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
assert sols == ['2654'] and trap != code
json.dump({'unique_answer': code, 'dice_top_front_right_and_rolls': {k: [list(v), s] for k, (v, s) in DICE.items()},
           'trap_wrong_direction': trap,
           'why': 'A ↓ 뒷면(7-5=2) · B ↓ 뒷면 4, → 왼쪽 면(7-1=6) · C →→ 왼쪽 면 1, 다시 왼쪽 면 4, ↓ 뒷면(7-2=5) · D → 왼쪽 면 1, ↓ 뒷면(7-3=4)'},
          open(os.path.join(HERE, '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
