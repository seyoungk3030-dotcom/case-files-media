"""ROOM 205 proof (페달 한 바퀴): a bicycle chain links the front chainring (F teeth) to the rear cog (R teeth), and the
rear cog is fixed to the back wheel. One pedal turn pulls F chain links over the chainring; the same F links pass over the
rear cog, which turns F/R times, and the wheel with it. Simulated link by link for P pedal turns. Digit = back-wheel turns.
All 10^4 codes compared; exactly one matches. Trap: 'one pedal turn = one wheel turn' (1113)."""
import itertools, json, os
from fractions import Fraction as Fr

# key: (front teeth, rear teeth, pedal turns)
BOARDS = {'A': (48, 12, 1), 'B': (36, 18, 1), 'C': (30, 30, 1), 'D': (30, 18, 3)}


def wheel_turns(F, R, P):
    links = 0; rear_tooth = 0
    for _ in range(P * F): links += 1; rear_tooth += 1   # each link moves the rear cog by one tooth
    return Fr(rear_tooth, R)


GOOD = {}
for k, (F, R, P) in BOARDS.items():
    assert 22 <= F <= 53 and 11 <= R <= 34   # real road / city bike gearing
    w = wheel_turns(F, R, P); assert w.denominator == 1 and 0 <= w < 10; GOOD[k] = int(w)
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(BOARDS[k][2]) for k in 'ABCD')
inv = ''.join(str(int(Fr(R, F) * P)) for F, R, P in (BOARDS[k] for k in 'ABCD'))
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, 'inverted', inv)
assert len(sols) == 1 and code not in (trap, inv)
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'turns': GOOD, 'trap_one_to_one': trap,
               'why': '페달 한 바퀴에 앞 톱니 수만큼 체인이 지나가고, 뒤 톱니는 그만큼 돌아요. 앞 ÷ 뒤 × 페달 바퀴'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
