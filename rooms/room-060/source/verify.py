"""ROOM 060 proof: four domino boards. The first domino at the bottom is pushed. A falling domino knocks over the next one
only when the spacing is shorter than a domino is tall, so a gap (missing dominoes) stops the chain on that run.
Every board has three bells (left / straight / right); the chain also runs sideways across bridge runs.
Breadth-first search over the runs finds which bells ring: on every board exactly one rings.
All 10^4 codes are compared with that result, exactly one matches. Picking the bell straight ahead gives the trap."""
import itertools, json, os

NODES = {'S': (0, 0), 'F': (0, 1.5), 'Lf': (-2, 1.5), 'Rf': (2, 1.5), 'Lm': (-2, 3.5), 'Mm': (0, 3.5), 'Rm': (2, 3.5),
         'L': (-2, 5.2), 'M': (0, 5.2), 'R': (2, 5.2)}
BASE = [('S', 'F'), ('F', 'Lf'), ('F', 'Rf'), ('F', 'Mm'), ('Lf', 'Lm'), ('Lm', 'L'), ('Mm', 'M'), ('Rf', 'Rm'), ('Rm', 'R')]
BOARDS = {   # gaps (runs with missing dominoes), bridges (extra sideways runs), bell digits L M R
    'A': {'gaps': [('F', 'Mm'), ('Rf', 'Rm')], 'bridges': [], 'bells': {'L': 4, 'M': 8, 'R': 1}},
    'B': {'gaps': [('F', 'Lf'), ('Mm', 'M')], 'bridges': [('Mm', 'Rm')], 'bells': {'L': 2, 'M': 7, 'R': 9}},
    'C': {'gaps': [('F', 'Rf'), ('F', 'Mm'), ('Lm', 'L'), ('Mm', 'M')], 'bridges': [('Lm', 'Mm'), ('Mm', 'Rm')], 'bells': {'L': 6, 'M': 3, 'R': 5}},
    'D': {'gaps': [('F', 'Lf'), ('Rm', 'R'), ('Mm', 'M')], 'bridges': [('Mm', 'Lm')], 'bells': {'L': 7, 'M': 2, 'R': 8}},
}


def runs(k):
    b = BOARDS[k]; g = {frozenset(e) for e in b['gaps']}
    return [(u, v, frozenset((u, v)) in g) for u, v in BASE + b['bridges']]


def fall(k):
    """Returns (order of fallen runs as (from, to), rung bells). Dominoes topple both ways along a run once one end falls."""
    rs = runs(k); seen = {'S'}; q = ['S']; order = []
    while q:
        n = q.pop(0)
        for u, v, gap in rs:
            if gap or n not in (u, v): continue
            o = v if n == u else u
            if o in seen: continue
            seen.add(o); q.append(o); order.append((n, o))
    return order, sorted(x for x in 'LMR' if x in seen)


rung = {k: fall(k)[1] for k in 'ABCD'}
assert all(len(v) == 1 for v in rung.values()), rung
code = ''.join(str(BOARDS[k]['bells'][rung[k][0]]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
trap = ''.join(str(BOARDS[k]['bells']['M']) for k in 'ABCD')
print('answer', code, 'rung', rung, 'solutions', sols, 'trap', trap)
assert sols == ['4957'] and trap == '8732'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'rung_bell': {k: v[0] for k, v in rung.items()},
               'boards': BOARDS, 'trap_straight_ahead': trap,
               'why': '빈틈이 있는 줄은 멈추고, 옆으로 이어진 다리 줄로 돌아서 간다. A 왼쪽 4 · B 오른쪽 9 · C 왼쪽→다리 두 번→오른쪽 5 · D 가운데→다리→왼쪽 7'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1, default=list)
