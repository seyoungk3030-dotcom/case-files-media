"""ROOM 170 proof: clock hands. A wall clock has 60 small ticks. At h:m the minute hand points at tick m and the hour
hand at tick 5 * (h % 12) + m / 12 (it creeps forward one tick every 12 minutes; every time here is a multiple of 12
minutes, so it sits exactly on a tick). Digit = number of tick gaps between the two hands the short way round.
All 10^4 codes compared; exactly one matches. The trap: leaving the hour hand on the hour number (5 * h)."""
import itertools, json, os

BOARDS = {'A': (3, 12), 'B': (6, 36), 'C': (9, 48), 'D': (1, 12)}


def gap(a, b): d = abs(a - b) % 60; return min(d, 60 - d)


def ticks(h, m): return 5 * (h % 12) + m // 12, m


GOOD = {k: gap(*ticks(h, m)) for k, (h, m) in BOARDS.items()}
TRAPV = {k: gap(5 * (h % 12), m) for k, (h, m) in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] and GOOD[k] < 10 for k in 'ABCD') and all(m % 12 == 0 for h, m in BOARDS.values())
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'times': BOARDS, 'gaps': GOOD, 'hands_ticks': {k: ticks(*v) for k, v in BOARDS.items()},
               'trap_hour_hand_still': trap, 'why': '시침은 가만히 있지 않고 12분마다 작은 눈금 한 칸씩 움직여요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
