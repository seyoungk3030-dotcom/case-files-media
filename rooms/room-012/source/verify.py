"""ROOM 012 proof: exactly one of five statements is false; code ABCD digits 1-9 all different."""
import itertools, json, os
ST = [('민재', 'A는 B의 두 배', lambda a, b, c, d: a == 2 * b),
      ('유나', 'C + D = A', lambda a, b, c, d: c + d == a),
      ('도윤', 'C가 가장 크다', lambda a, b, c, d: c == max(a, b, c, d)),
      ('서연', 'D가 가장 작다', lambda a, b, c, d: d == min(a, b, c, d)),
      ('하준', 'C는 D의 두 배', lambda a, b, c, d: c == 2 * d)]
sols, tested, all_true = [], 0, 0
for code in itertools.permutations(range(1, 10), 4):
    tested += 1
    t = [f(*code) for _, _, f in ST]
    if all(t): all_true += 1
    if t.count(False) == 1: sols.append((''.join(map(str, code)), ST[t.index(False)][0]))
print(tested, all_true, sols)
assert len(sols) == 1 and all_true == 0
json.dump({'unique_answer': sols[0][0], 'liar': sols[0][1], 'tested_codes': tested, 'solutions_if_all_true': all_true,
           'statements': [[n, s] for n, s, _ in ST], 'rules': 'ABCD each 1-9, all different, exactly one statement false'},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
