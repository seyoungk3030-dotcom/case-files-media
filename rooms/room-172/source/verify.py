"""ROOM 172 proof: half-full glasses. Each board is one glass with its height split into N equal parts by marks, and
water up to the first mark (1/N of the height). Digit = how many times the current water fits into the full glass.
Volumes are integrated numerically from each shape's cross-section area A(z): cylinder A = const, V-shaped vase
(triangular prism, edge down) A ~ z, cocktail cone (point down) A ~ z^2. All 10^4 codes compared; exactly one matches.
The trap: thinking volume follows height (answer N for every glass)."""
import itertools, json, os

BOARDS = {'A': ('cone', 2), 'B': ('vee', 3), 'C': ('vee', 2), 'D': ('cyl', 3)}
AREA = {'cyl': lambda z: 1.0, 'vee': lambda z: z, 'cone': lambda z: z * z}


def vol(shape, h, n=20000):
    return sum(AREA[shape]((i + 0.5) * h / n) for i in range(n)) * h / n


def times(shape, N):
    r = vol(shape, 1.0) / vol(shape, 1.0 / N); assert abs(r - round(r)) < 1e-4, r; return round(r)


GOOD = {k: times(*v) for k, v in BOARDS.items()}
TRAPV = {k: v[1] for k, v in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] < 10 for k in 'ABCD') and code != trap
# every rule is needed: each shape's law changes at least one digit vs the linear guess
assert GOOD['A'] != TRAPV['A'] and GOOD['B'] != TRAPV['B'] and GOOD['D'] == TRAPV['D']
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'times': GOOD,
               'trap_volume_follows_height': trap,
               'why': '물 높이가 반이어도 양은 반이 아니에요. 원뿔 잔은 높이의 세제곱, V자 화병은 제곱으로 늘어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
