"""ROOM 014 proof: 2x2 dial A B / C D, digits 1-9 all different, read A->B->C->D."""
import itertools, json, os
CL = [('① 윗줄 A + B = 12', lambda a, b, c, d: a + b == 12),
      ('② 아랫줄 C + D = 7', lambda a, b, c, d: c + d == 7),
      ('③ 왼쪽 줄 A + C = 10', lambda a, b, c, d: a + c == 10),
      ('④ 가장 큰 숫자는 B', lambda a, b, c, d: b > max(a, c, d))]
def solve(distinct):
    pool = itertools.permutations(range(1, 10), 4) if distinct else itertools.product(range(1, 10), repeat=4)
    return [''.join(map(str, x)) for x in pool if all(f(*x) for _, f in CL)]
sols = solve(True)
first3 = [''.join(map(str, x)) for x in itertools.permutations(range(1, 10), 4) if all(f(*x) for _, f in CL[:3])]
trap = [s for s in solve(False) if s not in sols]
print(sols, first3, trap)
assert sols == ['4861']
json.dump({'unique_answer': sols[0], 'tested_codes': 3024, 'candidates_clues_1_to_3': first3,
           'extra_solutions_if_digits_may_repeat': trap, 'clues': [c for c, _ in CL],
           'rules': 'A B / C D each 1-9, all different, code = A B C D'},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
