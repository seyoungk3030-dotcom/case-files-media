"""ROOM 017 proof: four people got off a going-up elevator on different floors 2-9. Code = floors of 민재 유나 도윤 서연."""
import itertools, json, os
CL = [('① 내린 순서: 유나 → 서연 → 도윤 → 민재', lambda m, y, d, s: y < s < d < m),
      ('② 민재는 유나보다 정확히 3층 위', lambda m, y, d, s: m == y + 3),
      ('③ 네 사람이 내린 층을 더하면 22', lambda m, y, d, s: m + y + d + s == 22)]
cands = list(itertools.permutations(range(2, 10), 4))
sols = [''.join(map(str, x)) for x in cands if all(f(*x) for _, f in CL)]
first2 = [''.join(map(str, x)) for x in cands if all(f(*x) for _, f in CL[:2])]
print(sols, first2)
assert sols == ['7465']
json.dump({'unique_answer': sols[0], 'tested_codes': len(cands), 'candidates_clues_1_2': first2,
           'trap_floors_in_exit_order': '4567', 'clues': [c for c, _ in CL],
           'rules': 'floors 2-9, all different, elevator only goes up; code = 민재 유나 도윤 서연 floors'},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
