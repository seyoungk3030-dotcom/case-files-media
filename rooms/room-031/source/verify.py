"""ROOM 031 proof: a gear train. The start gear S (24 teeth) turns exactly once. Meshing gears move the same number
of teeth (teeth x turns is equal); gears on one axle turn together. Code = whole turns of A, B, C, D.
Brute force: every assignment of 1..9 turns to A, B, C, D (and to B's upper gear) is checked against the two rules;
exactly one survives. Dropping the axle rule leaves B's upper gear free, so C and D are no longer fixed."""
import itertools, json, os
TEETH = {'S': 36, 'A': 12, 'B': 18, 'B2': 9, 'C': 6, 'D': 18}
MESH = [('S', 'A'), ('A', 'B'), ('B2', 'C'), ('C', 'D')]
AXLE = [('B', 'B2')]


def ok(turns, axle=True):
    if any(TEETH[a] * turns[a] != TEETH[b] * turns[b] for a, b in MESH): return False
    return not axle or all(turns[a] == turns[b] for a, b in AXLE)


sols, free = [], set()
for t in itertools.product(range(1, 10), repeat=5):
    turns = dict(zip(['A', 'B', 'B2', 'C', 'D'], t)); turns['S'] = 1
    if ok(turns): sols.append(''.join(str(turns[k]) for k in 'ABCD'))
for t in itertools.product(range(1, 31), repeat=5):    # without the axle rule, allowing any whole number of turns
    turns = dict(zip(['A', 'B', 'B2', 'C', 'D'], t)); turns['S'] = 1
    if ok(turns, axle=False): free.add(tuple(turns[k] for k in 'ABCD'))
print('solutions', sols, 'without axle rule', sorted(free))
assert sols == ['3231'] and len(free) > 1
trap = '3262'   # comparing every gear straight with the start gear: C = 36/6, D = 36/18
json.dump({'unique_answer': sols[0], 'assignments_tested': 9 ** 5, 'teeth': TEETH, 'mesh': MESH, 'axle': AXLE,
           'without_axle_rule': sorted(free), 'trap_start_gear_only': trap,
           'why': 'A = 36/12 = 3, B = 36/18 = 2, the small gear on B turns 2 too, so C = 2*9/6 = 3 and D = 2*9/18 = 1'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
