"""ROOM 109 proof: the tide-and-ladder riddle. Each board has a rope ladder either nailed to a fixed pier post or hung
on the side of a floating boat. The water now is at z = 0 and the tide gauge's mint mark shows where it will be
(z = RISE). A rung counts if it is above the water after the tide comes in. A pier ladder stays put, so rungs below
the mint mark go under. A boat floats up with the water, so its ladder rises too and the count does not change.
Each digit is the number of rungs above water after the tide. All 10^4 codes are compared; exactly one matches.
Treating the boat like the pier (the trap) gives another code."""
import itertools, json, os

# kind, lowest rung height, rung gap, number of rungs, tide rise
BOARDS = {'A': ('pier', -0.45, 0.30, 10, 0.90), 'B': ('boat', -0.45, 0.30, 9, 0.90),
          'C': ('pier', -0.30, 0.30, 9, 1.65), 'D': ('boat', -0.40, 0.30, 8, 1.20)}


def rungs(k): kind, z0, g, n, _ = BOARDS[k]; return [round(z0 + g * i, 3) for i in range(n)]


def above(k, as_pier=False):
    kind, z0, g, n, rise = BOARDS[k]; zs = rungs(k)
    if kind == 'boat' and not as_pier: zs = [z + rise for z in zs]
    assert all(abs(z - rise) > 0.08 for z in zs)            # no rung sits on the water line
    return sum(z > rise for z in zs)


RES = {k: above(k) for k in 'ABCD'}; TR = {k: above(k, True) for k in 'ABCD'}
code = ''.join(str(RES[k]) for k in 'ABCD'); trap = ''.join(str(TR[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == [code] and trap != code and all(v <= 9 for v in RES.values())
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'rungs_above_after': RES, 'trap_boat_as_pier': trap,
               'why': '부두 사다리는 그대로라 물에 잠기고, 배는 물과 함께 떠오르니 물 위 칸 수가 그대로예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
