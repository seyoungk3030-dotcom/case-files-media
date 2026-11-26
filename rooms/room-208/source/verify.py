"""ROOM 208 proof (그네 한 번 왕복): a playground swing is a pendulum. Its round-trip time is T = 2*pi*sqrt(L/g) times a
small amplitude correction (1 + th^2/16 + 11 th^4/3072), independent of the rider's mass. Each board gives the chain length,
who rides and how hard the push is (start angle). Digit = round-trip seconds rounded; every board is within 0.15 s of a
whole number even with the amplitude correction. All 10^4 codes compared; exactly one matches. Trap: 'heavier or harder
push = slower/faster'."""
import itertools, json, math, os

G = 9.81
# key: (rider, mass kg, chain length m, push angle deg)
BOARDS = {'A': ('어린이', 25, 2.25, 15), 'B': ('어른', 75, 2.25, 35), 'C': ('어린이', 25, 1.0, 15), 'D': ('어른', 75, 4.0, 30)}


def period(L, deg):
    th = math.radians(deg)
    return 2 * math.pi * math.sqrt(L / G) * (1 + th ** 2 / 16 + 11 * th ** 4 / 3072)


GOOD, EXACT = {}, {}
for k, (who, m, L, a) in BOARDS.items():
    T = period(L, a); EXACT[k] = round(T, 2); GOOD[k] = round(T)
    assert abs(T - GOOD[k]) < 0.15 and 0 <= GOOD[k] < 10, (k, T)
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, EXACT)
assert len(sols) == 1
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'g': G,
               'boards': {k: {'rider': w, 'mass_kg': m, 'chain_m': L, 'push_deg': a, 'period_s': EXACT[k]} for k, (w, m, L, a) in BOARDS.items()},
               'trap': '무거우면 느리다 / 세게 밀면 빨라진다', 'why': '그네(진자)의 왕복 시간은 줄 길이로만 정해져요: 약 2초 × √(줄 길이 m)'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
