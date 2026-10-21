"""ROOM 030 proof: four standard dice; each shows its top, front and right faces. Rule: opposite faces add up
to 7. The code is the number on the face touching the floor, dice A to D. Check 1: every orientation of a
standard die that shows the same three faces has the same bottom. Check 2: without the 7 rule (any die with
1..6 on its faces) the bottom is not determined, so the rule is needed."""
import itertools, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import dice
DICE = {'A': (3, 2, 6), 'B': (6, 4, 5), 'C': (1, 5, 4), 'D': (5, 1, 3)}   # top, front, right as seen
res = {}
for k, (t, f, r) in DICE.items():
    bottoms = sorted({dice.face_on(R, dice.DOWN) for R in dice.rotations() if dice.view(R) == (t, f, r)})
    free = sorted({p[3] for p in itertools.permutations(range(1, 7)) if p[:3] == (t, f, r)})
    res[k] = {'top_front_right': [t, f, r], 'bottom': bottoms, 'bottom_without_rule': free}
    print(k, res[k]); assert len(bottoms) == 1 and len(free) > 1
code = ''.join(str(res[k]['bottom'][0]) for k in 'ABCD'); trap = ''.join(str(DICE[k][0]) for k in 'ABCD')
print('code', code, 'trap (top faces)', trap); assert code == '4162' and trap != code
json.dump({'unique_answer': code, 'orientations_tested_per_die': 24, 'dice': res, 'trap_top_faces': trap,
           'why': 'the bottom is opposite the top, so bottom = 7 - top; front and right only confirm the die is standard'},
          open(os.path.join(HERE, '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
