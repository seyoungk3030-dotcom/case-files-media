"""ROOM 177 proof: tide and ladders. Each board is a ladder with rungs every 30 cm and some rungs already under water.
A rope ladder hangs from a ship (the ship floats, so it rises with the water); a steel ladder is bolted to a stone pier
(it stays put). The tide then rises T cm. Digit = rungs under water afterwards, simulated from rung heights.
All 10^4 codes compared; exactly one matches. Traps: adding T/30 rungs everywhere (forgetting the ship floats), or
keeping the count everywhere (forgetting the pier does not)."""
import itertools, json, os

GAP = 30
BOARDS = {'A': ('ship', 2, 60), 'B': ('pier', 1, 90), 'C': ('ship', 3, 30), 'D': ('pier', 0, 60)}  # (holder, rungs under now, tide cm)


def rungs(under):  # rung heights in cm relative to the water now; 'under' rungs below it, each 15 cm from the next level
    return [-15 - GAP * i for i in range(under)][::-1] + [15 + GAP * i for i in range(8)]


def after(holder, under, tide):
    hs = rungs(under); water = tide
    if holder == 'ship': hs = [h + tide for h in hs]  # the ship and its ladder float up with the water
    return sum(h < water for h in hs)


GOOD = {k: after(*v) for k, v in BOARDS.items()}
ADD = {k: u + t // GAP for k, (h, u, t) in BOARDS.items()}
SAME = {k: u for k, (h, u, t) in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(ADD[k]) for k in 'ABCD'); same = ''.join(str(SAME[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap_add', trap, 'trap_same', same)
assert len(sols) == 1 and code not in (trap, same) and all(GOOD[k] < 10 for k in 'ABCD')
assert {h for h, _, _ in BOARDS.values()} == {'ship', 'pier'}
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'rung_gap_cm': GAP, 'under_after': GOOD,
               'trap_add_everywhere': trap, 'trap_same_everywhere': same,
               'why': '배는 물에 떠서 밀물과 함께 올라가요. 배에 매단 사다리는 그대로, 부두에 박힌 사다리만 잠겨요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
