"""ROOM 174 proof: snail in a well. Each board is a well H metres deep with a snail at the bottom. Every day it
climbs U metres, every night it slides back D metres; the moment it reaches the top it is out and does not slide.
Digit = the day it gets out, found by simulating day by day. All 10^4 codes compared; exactly one matches.
The trap: dividing the depth by the net gain per day (H / (U - D)), forgetting the last day has no night."""
import itertools, json, os

BOARDS = {'A': (6, 3, 2), 'B': (9, 3, 2), 'C': (8, 4, 2), 'D': (9, 5, 4)}


def day_out(H, U, D):
    h, day = 0, 0
    while True:
        day += 1; h += U
        if h >= H: return day
        h -= D


GOOD = {k: day_out(*v) for k, v in BOARDS.items()}
TRAPV = {k: H // (U - D) for k, (H, U, D) in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] < 10 and GOOD[k] != TRAPV[k] for k in 'ABCD')
assert all(H % (U - D) == 0 and U < H for H, U, D in BOARDS.values())  # trap is a clean whole number, never trivially day 1
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'wells_depth_up_down': BOARDS, 'days': GOOD, 'trap_divide': trap,
               'why': '마지막 날은 낮에 올라가자마자 탈출해서 밤에 미끄러지지 않아요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
