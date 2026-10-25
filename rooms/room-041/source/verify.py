"""ROOM 041 proof: four seesaws, some level, some tipped (the heavier side goes down). Shapes: c circle(ball), t triangle
(pyramid), s square(cube), r star. Same shape = same weight. Code = heaviness rank of A=ball, B=pyramid, C=cube, D=star
(1 = heaviest). Every weight assignment 1..30 that fits all four seesaws gives the same ranking.
Ranking from the lightest gives the trap 1432."""
import itertools, json, os
# (left, right, result) result: '=' level, 'L' left side down, 'R' right side down
SCALES = [(['s'], ['c', 'c'], '='), (['t'], ['s', 's'], 'R'), (['t'], ['c', 'c', 'c'], 'L'), (['r', 'r'], ['t'], '=')]
ORDER = 'ctsr'   # A B C D


def ok(w):
    for L, R, res in SCALES:
        a, b = sum(w[k] for k in L), sum(w[k] for k in R)
        if (res == '=' and a != b) or (res == 'L' and a <= b) or (res == 'R' and a >= b): return False
    return True


ranks = set(); n = 0
for vals in itertools.product(range(1, 31), repeat=4):
    w = dict(zip(ORDER, vals))
    if len(set(vals)) == 4 and ok(w):
        n += 1; srt = sorted(ORDER, key=lambda k: -w[k]); ranks.add(''.join(str(srt.index(k) + 1) for k in ORDER))
print('fitting weight sets', n, 'rankings', ranks)
assert ranks == {'4123'}
# each seesaw needed
for i in range(4):
    keep = SCALES[:i] + SCALES[i + 1:]; rs = set()
    for vals in itertools.product(range(1, 31), repeat=4):
        w = dict(zip(ORDER, vals))
        if len(set(vals)) == 4 and all(((sum(w[k] for k in L) > sum(w[k] for k in R)) - (sum(w[k] for k in L) < sum(w[k] for k in R))) == {'=': 0, 'L': 1, 'R': -1}[r] for L, R, r in keep):
            srt = sorted(ORDER, key=lambda k: -w[k]); rs.add(''.join(str(srt.index(k) + 1) for k in ORDER))
    assert len(rs) > 1, i
json.dump({'unique_answer': '4123', 'weight_sets_fitting': n, 'order': 'A ball, B pyramid, C cube, D star', 'trap_lightest_first': '1432',
           'why': '큐브 = 공 2개 · 피라미드는 공 3개보다 무겁고 큐브 2개(공 4개)보다 가볍다 · 별 2개 = 피라미드 → 별은 공 1.5~2개 → 피라미드 > 큐브 > 별 > 공'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
