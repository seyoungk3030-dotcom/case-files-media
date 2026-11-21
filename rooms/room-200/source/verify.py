"""ROOM 200 proof (강물에 떨어진 모자): a hat falls off a rowing boat into a river at t = 0 and floats with the current.
The rower keeps rowing (up- or downstream) for t1 minutes, then turns round at once and rows back to the hat. The boat's
speed through the WATER is v going out and v2 coming back. The positions are simulated on the bank (ground frame) with exact
fractions; the catch-up time is t1 * v / v2, whatever the current. Each board is also re-run with currents 0..9 to prove the
current never matters. Digit = minutes from turning round to picking up the hat. All 10^4 codes compared; exactly one
matches. Trap: adding/subtracting the current (e.g. thinking going back upstream takes longer)."""
import itertools, json, os
from fractions import Fraction as F

# key: (direction rowed after the hat fell, current c, rowing speed out v, minutes t1, rowing speed back v2)  (m/min, any unit)
BOARDS = {'A': ('up', 20, 30, 4, 30), 'B': ('down', 30, 40, 7, 40), 'C': ('up', 10, 20, 6, 40), 'D': ('down', 20, 60, 2, 30)}


def catch(d, c, v, t1, v2):
    s = -1 if d == 'up' else 1                    # flow is +x
    boat = F((s * v + c) * t1); hat = F(c * t1)
    vb = -s * v2 + c                              # boat ground speed after turning round
    tau = (boat - hat) / (c - vb)                 # hat ground speed is c
    assert tau > 0; return tau


GOOD = {}
for k, (d, c, v, t1, v2) in BOARDS.items():
    t = catch(d, c, v, t1, v2); assert t.denominator == 1 and 0 < t < 10; GOOD[k] = int(t)
    assert all(catch(d, cc, v, t1, v2) == t for cc in range(0, 10)), k   # the current never matters
code = ''.join(str(GOOD[k]) for k in 'ABCD')


def naive(d, c, v, t1, v2):  # bank-frame mistake: hat treated as standing still where it fell
    s = -1 if d == 'up' else 1; boat = (s * v + c) * t1; vb = -s * v2 + c
    return F(abs(boat), abs(vb))


trap = ''.join(str(int(naive(*BOARDS[k])) % 10) for k in 'ABCD')
sols = [x for x in map(''.join, itertools.product('0123456789', repeat=4)) if x == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and code != trap
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'minutes': GOOD, 'trap_hat_stays_put': trap,
               'why': '모자와 배는 같은 물 위에 있어요. 물과 함께 보면 물살은 둘 다 똑같이 밀어서 없는 것과 같아요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
