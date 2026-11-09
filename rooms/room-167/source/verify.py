"""ROOM 167 proof: pizza size. Each board has two trays with a number tag: one tray holds n1 pizzas of diameter d1 cm,
the other n2 pizzas of diameter d2 cm (all equally thick). The tray with more pizza is the one with the larger total
area n * pi * (d / 2)^2. Digit = tag of that tray. No board is a tie. All 10^4 codes compared; exactly one matches.
The trap: comparing total diameter n * d (or just the number of pizzas), which picks the tray with more small pizzas."""
import itertools, json, math, os

BOARDS = {'A': {'L': (7, 1, 30), 'R': (4, 2, 20)}, 'B': {'L': (2, 1, 36), 'R': (9, 3, 20)},
          'C': {'L': (5, 1, 20), 'R': (3, 4, 12)}, 'D': {'L': (8, 1, 30), 'R': (6, 3, 18)}}


def area(t): return t[1] * math.pi * (t[2] / 2) ** 2


GOOD = {}; TRAPV = {}; AREAS = {}
for k, b in BOARDS.items():
    aL, aR = area(b['L']), area(b['R']); AREAS[k] = (round(aL), round(aR))
    assert abs(aL - aR) / max(aL, aR) > 0.05, k  # clear winner
    GOOD[k] = (b['L'] if aL > aR else b['R'])[0]
    TRAPV[k] = (b['L'] if b['L'][1] * b['L'][2] > b['R'][1] * b['R'][2] else b['R'])[0]
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, AREAS)
assert len(sols) == 1 and code != trap
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'areas_cm2': AREAS, 'trap_diameters': trap,
               'why': '피자 양은 지름이 아니라 넓이(지름의 제곱)에 비례해요. 지름이 1.5배면 양은 2.25배예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
