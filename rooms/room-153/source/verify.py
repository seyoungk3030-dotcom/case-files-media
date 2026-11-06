"""ROOM 153 proof: ants on a 10 cm stick. Every ant walks at 1 cm per second. When two ants meet head-on they both turn
around at once. An ant that reaches either end (0 or 10) falls off. Question: after how many seconds does the red ant
fall off? Simulated exactly in half-second steps (meetings can happen halfway between marks). Digit = that time.
All 10^4 codes compared; exactly one matches. The trap: the red ant's own distance to the end it faces (ignoring the
turn-arounds)."""
import itertools, json, os
L = 10
BOARDS = {'A': {'pos': [2, 3, 6, 7], 'dir': [1, 1, 1, -1], 'red': 2},
          'B': {'pos': [1, 5, 7, 8], 'dir': [-1, 1, 1, -1], 'red': 3},
          'C': {'pos': [2, 3, 4, 9], 'dir': [-1, -1, 1, -1], 'red': 2},
          'D': {'pos': [2, 3, 5, 6, 7], 'dir': [1, -1, 1, -1, -1], 'red': 4}}


def sim(b):
    a = [[2 * p, d, i] for i, (p, d) in enumerate(zip(b['pos'], b['dir']))]; t = 0
    while True:
        t += 1
        for x in a: x[0] += x[1]
        at = {}
        for x in a: at.setdefault(x[0], []).append(x)
        for v in at.values():
            assert len(v) <= 2
            if len(v) == 2: v[0][1], v[1][1] = v[1][1], v[0][1]
        for x in a:
            if x[2] == b['red'] and not 0 < x[0] < 2 * L: return t / 2, ('L' if x[0] <= 0 else 'R')
        a = [x for x in a if 0 < x[0] < 2 * L]


RES = {k: sim(b) for k, b in BOARDS.items()}
assert all(t == int(t) for t, _ in RES.values())
code = ''.join(str(int(RES[k][0])) for k in 'ABCD')
trap = ''.join(str(b['pos'][b['red']] if b['dir'][b['red']] < 0 else L - b['pos'][b['red']]) for b in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, RES)
assert sols == ['7395'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'falls': RES, 'trap_own_distance': trap,
               'why': '부딪혀서 돌아서는 건 두 개미가 그냥 스쳐 지나가는 것과 똑같아 보여요. 그래서 개미들의 순서는 절대 안 바뀌고, 빨간 개미는 자기 순서에 맞는 시간에 떨어져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
