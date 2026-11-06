"""ROOM 092 proof: music-box drums. Each pin sits under one numbered comb tooth (1-9) at an angle th measured from the
top of the drum toward the viewer (0 = top, 90 = front middle, 180 = bottom); only the front half has pins. A pin
plays when it reaches the comb at the top. 'up' = the front of the drum moves up, so the smallest th plays first;
'down' = the front moves down, the pin goes under and up the back, so the largest th plays first. Each digit is the
tooth number of the THIRD note. All 10^4 codes compared; exactly one matches. Reading the pins left to right (the trap)
gives another code."""
import itertools, json, os
BOARDS = {'A': ('up', [(2, 120), (4, 40), (6, 150), (7, 80), (9, 60)]),
          'B': ('down', [(1, 50), (3, 100), (5, 120), (8, 30), (9, 150)]),
          'C': ('up', [(1, 90), (3, 30), (4, 130), (6, 60), (8, 110)]),
          'D': ('down', [(2, 70), (3, 150), (5, 40), (7, 120), (9, 95)])}


def order(k):
    d, pins = BOARDS[k]; return [t for t, a in sorted(pins, key=lambda p: p[1], reverse=(d == 'down'))]


for k, (d, pins) in BOARDS.items():
    angs = sorted(a for _, a in pins); assert all(b - a >= 15 for a, b in zip(angs, angs[1:])) and 0 < angs[0] and angs[-1] < 180
code = ''.join(str(order(k)[2]) for k in 'ABCD'); trap = ''.join(str(sorted(BOARDS[k][1])[2][0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: order(k) for k in 'ABCD'})
assert sols == ['7319'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'play_order': {k: order(k) for k in 'ABCD'},
               'trap_left_to_right': trap, 'why': '빗살은 위에 있어요. 앞면이 위로 돌면 위쪽 핀부터, 아래로 돌면 아래쪽 핀부터(뒤로 돌아 올라감) 울려요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
