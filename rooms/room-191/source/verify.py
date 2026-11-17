"""ROOM 191 proof: a rope wrapped tight around a ball's equator is made longer by L and lifted evenly all round. The new
circle has circumference C + L, so its radius grows by L / (2*pi) whatever the ball's size: an orange and the Earth both
get the same gap. Digit = gap in whole cm (decimals dropped). Every gap sits at least 0.4 cm from a whole number, so
using pi = 3.14 or 3.1416 gives the same digits. All 10^4 codes compared; exactly one matches. The trap: thinking a
huge ball (Earth, Moon) would barely move (gap 0)."""
import itertools, json, math, os

BOARDS = {'A': ('귤', 8, 'cm', 22), 'B': ('볼링공', 22, 'cm', 35), 'C': ('지구', 12742, 'km', 9), 'D': ('달', 3474, 'km', 53)}  # name, diameter, unit, rope +cm


def gap(L, pi=math.pi): return L / (2 * pi)


GOOD = {}
for k, (n, d, u, L) in BOARDS.items():
    g = gap(L); assert 0.4 <= g - int(g) <= 0.6, (k, g); assert int(gap(L, 3.14)) == int(g); GOOD[k] = int(g)
TRAPV = {k: (0 if BOARDS[k][2] == 'km' else GOOD[k]) for k in 'ABCD'}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and code != trap
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'gap_cm': {k: round(gap(BOARDS[k][3]), 2) for k in 'ABCD'},
               'trap_big_ball_barely_moves': trap,
               'why': '새 둘레 = 원래 둘레 + L 이니까 반지름은 L ÷ (2 × 3.14) 만큼만 커져요. 공 크기와 상관없어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
