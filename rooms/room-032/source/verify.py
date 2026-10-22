"""ROOM 032 proof: four lamps on the left of a 4x4 board shoot light to the right. Every mirror turns a beam 90 degrees
(both faces reflect); beams pass through each other. Code = the lamp number whose light reaches A, B, C, D.
Brute force: every 4-digit code with digits 1..4 is checked against the traced beams; exactly one survives.
Without the mirror rule (light goes straight) no lamp reaches A, B or D, so the rule is needed."""
import itertools, json, os
N = 4
MIRRORS = {(0, 1): '/', (0, 2): '\\', (1, 2): '/', (2, 0): '/', (2, 2): '/', (3, 0): '/'}   # (row, col); row 0 = far side
TARGETS = {'A': ('T', 0), 'B': ('T', 1), 'C': ('R', 1), 'D': ('B', 1)}                    # T/B: column, R: row
STEP = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}
TURN = {'/': {'R': 'U', 'U': 'R', 'L': 'D', 'D': 'L'}, '\\': {'R': 'D', 'D': 'R', 'L': 'U', 'U': 'L'}}


def trace(row, mirrors=MIRRORS):
    """Cells the beam from lamp row+1 visits (with the direction it leaves each), and where it exits."""
    r, c, d, path = row, -1, 'R', []
    while True:
        r += STEP[d][0]; c += STEP[d][1]
        if not (0 <= r < N and 0 <= c < N):
            return path, {'U': ('T', c), 'D': ('B', c), 'R': ('R', r), 'L': ('L', r)}[d]
        if (r, c) in mirrors: d = TURN[mirrors[(r, c)]][d]
        path.append((r, c, d))


def ok(code, mirrors=MIRRORS):
    return all(trace(int(code[i]) - 1, mirrors)[1] == TARGETS[k] for i, k in enumerate('ABCD'))


sols = [''.join(t) for t in itertools.product('1234', repeat=4) if ok(''.join(t))]
straight = [''.join(t) for t in itertools.product('1234', repeat=4) if ok(''.join(t), {})]
print('solutions', sols, 'without mirrors', straight)
assert sols == ['3142'] and straight == []
paths = {i + 1: trace(i) for i in range(4)}
for k, (p, e) in paths.items(): print(k, len([x for x in p if (x[0], x[1]) in MIRRORS]), 'bounces ->', e)
json.dump({'unique_answer': sols[0], 'codes_tested': 4 ** 4, 'mirrors': {f'{r},{c}': m for (r, c), m in MIRRORS.items()},
           'targets': TARGETS, 'exits': {k: e for k, (p, e) in paths.items()},
           'bounces': {k: len([x for x in p if (x[0], x[1]) in MIRRORS]) for k, (p, e) in paths.items()},
           'without_mirror_rule': straight, 'trap': '4번 빛이 처음 거울에서 위로 꺾인 뒤 멈춘다고 보면 C를 놓친다',
           'why': '1번은 거울 하나로 B, 3번은 거울 하나로 A, 2번은 거울 셋을 거쳐 D, 4번은 거울 넷을 거쳐 C'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
