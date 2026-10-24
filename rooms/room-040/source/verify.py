"""ROOM 040 proof: marbles A B C D drop one at a time into a toggle tree. Every switch sends a marble the way its arrow
points, then flips to the other side. Top switch T feeds left switch L (bins 1, 2) and right switch R (bins 3, 4).
Code = the bin each marble lands in. All 4^4 codes are checked against the run; exactly one matches.
Flipping only the top switch (forgetting the lower ones) gives the trap."""
import itertools, json, os
START = {'T': 'L', 'L': 'R', 'R': 'L'}


def run(start, flip=('T', 'L', 'R')):
    s = dict(start); out = []; states = [dict(s)]
    for _ in 'ABCD':
        d1 = s['T']; low = 'L' if d1 == 'L' else 'R'; d2 = s[low]
        out.append(str((1 if low == 'L' else 3) + (0 if d2 == 'L' else 1)))
        for k, d in (('T', d1), (low, d2)):
            if k in flip: s[k] = 'R' if d == 'L' else 'L'
        states.append(dict(s))
    return ''.join(out), states


code, states = run(START)
sols = [c for c in map(''.join, itertools.product('1234', repeat=4)) if c == code]
trap, _ = run(START, flip=('T',))
print('answer', code, 'solutions', sols, 'trap', trap)
assert sols == ['2314'] and trap == '2323'
json.dump({'unique_answer': code, 'codes_checked': 256, 'start': START, 'states_after_each': states, 'trap_top_only': trap,
           'why': 'A: 위 왼쪽 → 왼쪽 칸막이 오른쪽 → 2 · B: 위 오른쪽 → 오른쪽 칸막이 왼쪽 → 3 · C: 왼쪽 → 왼쪽 → 1 · D: 오른쪽 → 오른쪽 → 4'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
