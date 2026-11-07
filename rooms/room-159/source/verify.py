"""ROOM 159 proof: a train of 5 numbered cars rolls left toward the exit tunnel, front car first. At the turntable each
car without a star goes straight on to the exit; each starred car is turned into the dead-end side track and waits.
When the whole train has passed, the waiting cars come back out one by one (the one that went in last is at the open
end, so it comes out first) and follow to the exit. Digit = the number on the 3rd car through the exit.
All 10^4 codes compared; exactly one matches. The trap: the waiting cars leave in the order they arrived (a queue)."""
import itertools, json, os
BOARDS = {'A': [(2, 0), (7, 1), (4, 1), (9, 1), (1, 0)],
          'B': [(6, 1), (3, 0), (8, 1), (5, 1), (2, 0)],
          'C': [(4, 1), (1, 1), (7, 0), (6, 1), (3, 1)],
          'D': [(5, 1), (8, 0), (2, 1), (9, 0), (4, 0)]}


def run(cars, stack=True):
    out, side = [], []
    for n, s in cars:
        (side if s else out).append(n)
    return out + (side[::-1] if stack else side)


ORDER = {k: run(c) for k, c in BOARDS.items()}
code = ''.join(str(ORDER[k][2]) for k in 'ABCD'); trap = ''.join(str(run(BOARDS[k], False)[2]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, ORDER)
assert sols == ['9564'] and trap != code and sum(a != b for a, b in zip(code, trap)) == 3
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'exit_order': ORDER, 'trap_queue': trap,
               'why': '막다른 옆 선로는 들어간 입구로 다시 나와요. 마지막에 들어간 칸이 입구 쪽에 있어서 가장 먼저 나와요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
