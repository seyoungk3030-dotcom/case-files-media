"""ROOM 022 proof: three balanced seesaws. Every shape weighs a whole number of kg from 1 to 9, different shapes
weigh different amounts. Test every assignment (circle, triangle, square, star) in 1..9 and keep the ones that
balance all three seesaws; the code is circle-triangle-square-star."""
import itertools, json, os
SCALES = [  # (left, right) as shape counts: c=circle t=triangle s=square r=star
    ({'c': 3}, {'t': 1}),
    ({'t': 1, 'c': 1}, {'s': 2}),
    ({'r': 1, 's': 1}, {'t': 2, 'c': 1}),
]
ok = []
for c, t, s, r in itertools.product(range(1, 10), repeat=4):
    if len({c, t, s, r}) < 4: continue
    w = {'c': c, 't': t, 's': s, 'r': r}
    if all(sum(w[k] * n for k, n in L.items()) == sum(w[k] * n for k, n in R.items()) for L, R in SCALES):
        ok.append(f'{c}{t}{s}{r}')
print(ok)
assert ok == ['1325']
json.dump({'unique_answer': ok[0], 'assignments_tested': 9 ** 4, 'order': 'circle triangle square star',
           'scales': ['3 circles = triangle', 'triangle + circle = 2 squares', 'star + square = 2 triangles + circle'],
           'why_unique': 'everything is a multiple of the circle; star = 5 x circle, so circle = 2 would make star 10 > 9'},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
