"""ROOM 071 proof: two candles lit at the same moment. The thin candle burns 2 tiles per hour, the thick one 1 tile per hour.
When the first one goes out, the digit is how many tiles of the other are left. Exact fractions; never a tie. Every
4-digit code is compared; exactly one matches. Assuming both burn equally fast (the trap) gives another code."""
import itertools, json, os
from fractions import Fraction as F
BOARDS = {'A': (6, 7), 'B': (9, 3), 'C': (2, 9), 'D': (9, 4)}   # (thin length, thick length) in tiles
SPEED = {'thin': 2, 'thick': 1}


def left(thin, thick, vt=SPEED['thin'], vk=SPEED['thick']):
    tt, tk = F(thin, vt), F(thick, vk); assert tt != tk
    return (thick - vk * tt, 'thin') if tt < tk else (thin - vt * tk, 'thick')


res = {k: left(*BOARDS[k]) for k in 'ABCD'}
for k, (v, _) in res.items(): assert v.denominator == 1 and 0 < v <= 9, k
code = ''.join(str(int(res[k][0])) for k in 'ABCD')
trap = ''.join(str(int(left(*BOARDS[k], 1, 1)[0])) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, 'solutions', sols, {k: v[1] for k, v in res.items()})
assert sols == ['4381'] and trap == '1675'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_thin_thick': BOARDS, 'speed_per_hour': SPEED,
               'first_out': {k: v[1] for k, v in res.items()}, 'trap_same_speed': trap,
               'why': '얇은 초는 1시간에 2칸, 굵은 초는 1칸. A 얇은 6칸 3시간에 꺼짐 → 굵은 7-3=4 · B 굵은 3칸 3시간 → 얇은 9-6=3 · C 얇은 2칸 1시간 → 굵은 9-1=8 · D 굵은 4칸 4시간 → 얇은 9-8=1'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
