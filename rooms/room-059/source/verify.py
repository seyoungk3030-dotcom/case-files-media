"""ROOM 059 proof: four pulley rigs. The rope end is pulled down by PULL tiles (mint arrow). How many tiles does the box rise?
The rope never stretches, so its total length stays the same: pulling the free end down by d shortens every rope
segment that holds the box by the same amount, d / n, where n = number of rope segments holding the box
(A one fixed pulley n=1, B movable pulley n=2, C fixed + movable + fixed n=3, D two fixed pulleys n=1).
The rise is found by solving the rope-length equation on a fine grid; all 10^4 codes are compared, exactly one matches.
Assuming the box rises as far as the rope is pulled gives the trap."""
import itertools, json, os
RIGS = {'A': ('fixed', 1, 3), 'B': ('movable', 2, 8), 'C': ('triple', 3, 6), 'D': ('double_fixed', 1, 7)}   # kind, segments, pull


def rise(n, pull, top=20.0, tail=5.0):
    """Box at height y hangs on n segments of length (top - y); the free end hangs tail + pull below the top.
    Find y (0.01-tile grid) that keeps the rope length equal to its length before the pull (y = 0, tail)."""
    L0 = top * n + tail
    return min((abs((top - i / 100) * n + tail + pull - L0), i / 100) for i in range(2001))[1]


res = {k: rise(n, p) for k, (_, n, p) in RIGS.items()}
code = ''.join(str(int(round(res[k]))) for k in 'ABCD')
assert all(abs(res[k] - RIGS[k][2] / RIGS[k][1]) < 1e-9 for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
trap = ''.join(str(RIGS[k][2]) for k in 'ABCD')
print('answer', code, 'rise', res, 'solutions', sols, 'trap', trap)
assert sols == ['3427'] and trap == '3867'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'rigs': {k: list(v) for k, v in RIGS.items()}, 'box_rise': res,
               'trap_same_as_pull': trap,
               'why': '상자를 잡고 있는 줄 가닥 수로 나눈다. A 고정 도르래 3÷1=3 · B 움직도르래 8÷2=4 · C 줄 세 가닥 6÷3=2 · D 고정 도르래 두 개 7÷1=7'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
