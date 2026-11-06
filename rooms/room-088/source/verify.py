"""ROOM 088 proof: a row of wheels joined by belts. An open belt makes the next wheel turn the same way; a crossed belt
(drawn as an X) makes it turn the opposite way. Wheel sizes change speed, never direction. Wheel 1 turns clockwise.
Each digit is how many wheels (wheel 1 included) turn clockwise. All 10^4 codes compared; exactly one matches.
Ignoring the crossed belts (the trap) gives another code."""
import itertools, json, os
BOARDS = {'A': ('OXOX', [1.0, 0.6, 0.9, 0.5, 0.8]), 'B': ('XOXXO', [0.7, 1.0, 0.5, 0.8, 0.6, 0.9]),
          'C': ('OOO', [0.9, 0.5, 1.0, 0.6]), 'D': ('XXXXX', [0.6, 0.8, 0.5, 0.9, 0.6, 0.7])}


def dirs(belts):
    d = [1]
    for b in belts: d.append(d[-1] if b == 'O' else -d[-1])
    return d


CW = {k: dirs(v[0]).count(1) for k, v in BOARDS.items()}
code = ''.join(str(CW[k]) for k in 'ABCD'); trap = ''.join(str(len(BOARDS[k][0]) + 1) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['3243'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_belts_sizes': BOARDS, 'trap_all_cw': trap,
               'why': '그냥 걸린 벨트는 같은 방향, X로 꼬인 벨트는 반대 방향. 바퀴 크기는 속도만 바꿔요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
