"""ROOM 120 proof: loop the loop. A smooth track drops from a tall ramp into a vertical loop of diameter D (in ruler
units). Start marks 1-9 on the ramp are 1 unit apart in height. A little ice sled let go from a mark (no push, no friction; it slides, it does not roll)
makes it round the loop only if it is still fast enough at the top: there gravity alone must bend its path, so
v_top^2 >= g r, and energy gives g (h - D) = v_top^2 / 2 -> h >= D + r/2 = 1.25 D. Digit = the LOWEST mark that
makes it. All 10^4 codes are compared; exactly one matches. The trap: 'just higher than the loop top' (h >= D)."""
import itertools, json, math, os

BOARDS = {'A': {'D': 3}, 'B': {'D': 6}, 'C': {'D': 2}, 'D': {'D': 5}}


def lowest(d): return math.ceil(1.25 * d - 1e-9)


for b in BOARDS.values(): assert 1.25 * b['D'] != int(1.25 * b['D'])
code = ''.join(str(lowest(BOARDS[k]['D'])) for k in 'ABCD'); trap = ''.join(str(BOARDS[k]['D']) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['4837'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'need_height': {k: 1.25 * b['D'] for k, b in BOARDS.items()},
               'trap_just_above_loop': trap, 'why': '고리 꼭대기에서도 충분히 빨라야 떨어지지 않아요. 시작 높이가 지름의 1.25배 이상이어야 해요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
