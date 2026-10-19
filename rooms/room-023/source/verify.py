"""ROOM 023 proof: four people badged in at 6, 7, 8 and 9 pm, one each. All four testimonies are true. Test every
way to hand out the four hours and keep those that satisfy all testimonies; the code is the arrival hour of
민재, 유나, 도윤, 서진 in that order."""
import itertools, json, os
P = ['민재', '유나', '도윤', '서진']
CLUES = {
    '민재: 유나는 첫 번째로 오지 않았어': lambda t: t['유나'] != 6,
    '유나: 도윤은 처음도 마지막도 아니었어': lambda t: t['도윤'] not in (6, 9),
    '도윤: 민재와 서진은 딱 두 시간 차이': lambda t: abs(t['민재'] - t['서진']) == 2,
    '서진: 나는 민재보다 먼저 왔어': lambda t: t['서진'] < t['민재'],
}
ok = []
for perm in itertools.permutations([6, 7, 8, 9]):
    t = dict(zip(P, perm))
    if all(f(t) for f in CLUES.values()): ok.append(''.join(str(t[p]) for p in P))
print(ok)
assert ok == ['8976']
# every clue is needed: dropping any one leaves more than one answer
for k in CLUES:
    rest = [f for c, f in CLUES.items() if c != k]
    n = sum(all(f(dict(zip(P, perm))) for f in rest) for perm in itertools.permutations([6, 7, 8, 9]))
    assert n > 1, k
json.dump({'unique_answer': ok[0], 'assignments_tested': 24, 'clues': list(CLUES), 'every_clue_needed': True},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
