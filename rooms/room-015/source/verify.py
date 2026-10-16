"""ROOM 015 proof: lockers 1-9 in a 3x3 grid; 민재 유나 도윤 서연 each own a different one; code = their numbers in that order."""
import itertools, json, os
rc = lambda n: divmod(n - 1, 3)
CORNER = {1, 3, 7, 9}
CL = [('① 민재는 가운데 세로줄', lambda m, y, d, s: rc(m)[1] == 1),
      ('② 유나는 민재 바로 오른쪽 칸', lambda m, y, d, s: rc(y) == (rc(m)[0], rc(m)[1] + 1)),
      ('③ 도윤은 유나 바로 아래 칸', lambda m, y, d, s: rc(d) == (rc(y)[0] + 1, rc(y)[1])),
      ('④ 서연은 도윤과 같은 가로줄, 네 모서리 칸 중 하나', lambda m, y, d, s: rc(s)[0] == rc(d)[0] and s in CORNER)]
sols = [''.join(map(str, x)) for x in itertools.permutations(range(1, 10), 4) if all(f(*x) for _, f in CL)]
first3 = [''.join(map(str, x)) for x in itertools.permutations(range(1, 10), 4) if all(f(*x) for _, f in CL[:3])]
print(sols, first3)
assert sols == ['5697']
json.dump({'unique_answer': sols[0], 'tested_codes': 3024, 'candidates_clues_1_to_3': first3, 'clues': [c for c, _ in CL],
           'rules': 'grid 1 2 3 / 4 5 6 / 7 8 9; four different lockers; code = 민재 유나 도윤 서연'},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
