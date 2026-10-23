"""ROOM 037 proof: five sticks lie in a pile (A B C D and one gray stick G). Where two sticks cross, the picture
shows which one is on top. Code = the layer of A, B, C, D counted from the top (top = 1, the gray stick counts).
All 5! stackings are tested against every crossing; exactly one fits. Skipping the gray stick gives the trap."""
import itertools, json, os
# stick: (x1, y1, x2, y2) on the floor plane; TRUE order is top -> bottom
STICKS = {'A': (-3.6, -1.7, 3.6, -0.7), 'D': (-2.9, 2.0, 1.7, -2.5), 'G': (-3.7, 0.5, 3.6, 1.5),
          'B': (2.9, 2.5, 0.5, -2.5), 'C': (-2.2, -2.5, 3.7, 0.3)}
TRUE = 'CBGDA'


def cross(p, q):
    (x1, y1, x2, y2), (x3, y3, x4, y4) = p, q
    d = (x2 - x1) * (y4 - y3) - (y2 - y1) * (x4 - x3)
    if abs(d) < 1e-9: return None
    t = ((x3 - x1) * (y4 - y3) - (y3 - y1) * (x4 - x3)) / d
    u = ((x3 - x1) * (y2 - y1) - (y3 - y1) * (x2 - x1)) / d
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1)) if 0.08 < t < 0.92 and 0.08 < u < 0.92 else None


pairs = {}
for a, b in itertools.combinations(STICKS, 2):
    pt = cross(STICKS[a], STICKS[b])
    if pt: pairs[(a, b)] = (a if TRUE.index(a) < TRUE.index(b) else b, pt)   # which one is seen on top
sols = [o for o in map(''.join, itertools.permutations(TRUE))
        if all(o.index(top) < o.index(b if top == a else a) for (a, b), (top, _) in pairs.items())]
code = lambda o: ''.join(str(o.index(c) + 1) for c in 'ABCD')
print('crossings', sorted(pairs), 'solutions', sols, [code(s) for s in sols])
assert sols == [TRUE]
trap = code(TRUE.replace('G', ''))
# each adjacent pair must cross, else the order between them would be free
assert all(tuple(sorted(p)) in {tuple(sorted(k)) for k in pairs} for p in zip(TRUE, TRUE[1:]))
print('answer', code(TRUE), 'trap', trap)
assert code(TRUE) == '5214' and trap == '4213'
json.dump({'unique_answer': code(TRUE), 'stackings_tested': 120, 'order_top_to_bottom': TRUE, 'trap_skip_gray': trap,
           'crossings': [f'{top} 위 ({a}-{b})' for (a, b), (top, _) in pairs.items()],
           'why': 'C가 B 위, B가 회색 위, 회색이 D 위, D가 A 위 → 위에서부터 C B 회색 D A'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
