"""ROOM 067 proof: identical springs; one spring holding one weight stretches 1 tile (Hooke's law, stretch = load / k).
Springs one under another (series) each carry the whole load, so their stretches add. Two springs side by side holding a
bar (parallel) share the load, half each. The weight drops by the sum of every stage's stretch. Every 4-digit code is
compared; exactly one matches. Counting only the weights, or treating side-by-side springs as one under another, fails."""
import itertools, json, os
from fractions import Fraction as F
BOARDS = {'A': (('s', 's'), 3), 'B': (('p',), 4), 'C': (('s', 's', 's'), 3), 'D': (('p', 's'), 2)}   # stages top→bottom, weights


def drop(stages, w, parallel_shares=True):
    return sum(F(w, 2 if (st == 'p' and parallel_shares) else 1) for st in stages)


res = {}
for k, (st, w) in BOARDS.items():
    d = drop(st, w); assert d.denominator == 1, (k, d); res[k] = int(d)
code = ''.join(str(res[k]) for k in 'ABCD'); trap = ''.join(str(BOARDS[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
nosh = [int(drop(st, w, False)) for st, w in BOARDS.values()]
print('answer', code, 'trap', trap, 'solutions', sols, 'parallel-as-series', nosh)
assert sols == ['6293'] and trap == '3432' and nosh != [res[k] for k in 'ABCD']
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_stages_weights': BOARDS, 'drop_tiles': res,
               'trap_count_weights': trap, 'parallel_as_series': nosh,
               'why': '스프링 하나에 추 1개 = 1칸. 위아래로 이으면 각자 전부 받아서 더하기, 나란히 매달면 반씩 나눠 받음. A 3+3=6 · B 4÷2=2 · C 3+3+3=9 · D 2÷2+2=3'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
