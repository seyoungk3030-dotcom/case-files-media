"""ROOM 026 proof: four people sit in window seats 1-4 (1 is leftmost), each with a different drink.
Enumerate all 24 x 24 seat/drink assignments, keep those matching the six receipt clues, prove the match is unique
and every clue is needed. Code = seat numbers of 민재, 유나, 도윤, 서진 in that order."""
import itertools, json, os
P = ['민재', '유나', '도윤', '서진']
D = ['아메리카노', '라떼', '녹차', '레몬에이드']
AM, LA, GT, LE = range(4); MJ, YN, DY, SJ = range(4)
CLUES = [
    ('레몬에이드는 1번 자리', lambda p, d: d[LE] == 1),
    ('도윤은 끝자리', lambda p, d: p[DY] in (1, 4)),
    ('녹차는 도윤 바로 옆자리', lambda p, d: abs(d[GT] - p[DY]) == 1),
    ('유나는 레몬에이드', lambda p, d: p[YN] == d[LE]),
    ('라떼는 4번 자리', lambda p, d: d[LA] == 4),
    ('유나는 서진의 바로 왼쪽', lambda p, d: p[YN] + 1 == p[SJ]),
]
cands = [(p, d) for p in itertools.permutations(range(1, 5)) for d in itertools.permutations(range(1, 5))]
match = [c for c in cands if all(f(*c) for _, f in CLUES)]
print(len(cands), match)
assert len(cands) == 576 and len(match) == 1
for k in range(len(CLUES)):
    assert sum(all(f(*c) for i, (_, f) in enumerate(CLUES) if i != k) for c in cands) > 1, CLUES[k][0]
p, d = match[0]
code = ''.join(str(s) for s in p)
print(code)
assert code == '3142'
json.dump({'unique_answer': code, 'assignments_tested': len(cands), 'every_clue_needed': True,
           'seats': {P[i]: p[i] for i in range(4)}, 'drinks_by_seat': {d[j]: D[j] for j in range(4)},
           'clues': [c for c, _ in CLUES]},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
