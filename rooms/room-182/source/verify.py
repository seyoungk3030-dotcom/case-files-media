"""ROOM 182 proof: shoes left at the front door. Every board is a top view of scattered sneakers. A pair needs one
LEFT and one RIGHT shoe of the same colour (a left shoe has its big-toe bulge on the right side when the toe points
up). Digit = how many complete pairs can be made. All 10^4 codes compared; exactly one matches.
The trap: halving the number of shoes of each colour without checking left and right."""
import itertools, json, os

# each shoe: colour, side, x, y (grid units), heading in degrees (0 = toe points up / away from the viewer)
BOARDS = {
    'A': [('red', 'L', 0, 0, 20), ('red', 'L', 1, 0.1, -35), ('red', 'R', 2, -0.1, 160), ('blue', 'L', 3, 0, 75),
          ('blue', 'R', 0.2, -1, -110), ('blue', 'R', 1.2, -1.1, 10), ('blue', 'R', 2.4, -0.9, 200)],
    'B': [('red', 'L', 0, 0, -20), ('red', 'R', 1, 0, 140), ('red', 'R', 2, 0.1, 30), ('red', 'L', 3, 0.05, 250),
          ('blue', 'L', 0, -1, 95), ('blue', 'R', 1, -1.1, -160), ('yellow', 'L', 2, -1, 10), ('yellow', 'L', 3.1, -0.95, 190)],
    'C': [('red', 'L', 0, 0, 200), ('red', 'R', 1.1, 0, -40), ('blue', 'R', 2.2, 0.1, 15), ('blue', 'R', 0.3, -1, 120),
          ('yellow', 'L', 1.3, -1.1, -15), ('yellow', 'L', 2.4, -0.9, 165)],
    'D': [('red', 'L', 0, 0, 0), ('red', 'L', 1, 0.1, 180), ('red', 'L', 2, -0.1, -60), ('blue', 'R', 3, 0, 30),
          ('blue', 'R', 0.4, -1, 150), ('blue', 'R', 1.5, -1, -100), ('blue', 'R', 2.6, -1.1, 15)]}


def pairs(shoes):
    cols = {c for c, *_ in shoes}
    return sum(min(sum(1 for c2, s, *_ in shoes if c2 == c and s == 'L'), sum(1 for c2, s, *_ in shoes if c2 == c and s == 'R')) for c in cols)


def naive(shoes):
    cols = {c for c, *_ in shoes}
    return sum(sum(1 for c2, *_ in shoes if c2 == c) // 2 for c in cols)


GOOD = {k: pairs(v) for k, v in BOARDS.items()}; TRAPV = {k: naive(v) for k, v in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] for k in 'ABCD')
for v in BOARDS.values():  # shoes never overlap: centres at least 0.85 apart (shoe length 0.72)
    for a, b in itertools.combinations(v, 2): assert ((a[2] - b[2]) ** 2 + (a[3] - b[3]) ** 2) ** 0.5 >= 0.85, (a, b)
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'pairs': GOOD, 'trap_half_of_each_colour': trap,
               'why': '같은 색이라도 왼쪽 한 짝과 오른쪽 한 짝이 있어야 한 켤레예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
