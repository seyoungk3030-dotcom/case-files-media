"""ROOM 033 proof: a hanging mobile. Every bar hangs level, so on each bar (weight x arm length) left = right; bars and
strings weigh nothing, and a bar weighs everything hanging below it. The weight K is 9. Code = weights of A, B, C, D.
Brute force over weights 1..9 for A, B, C, D: exactly one assignment survives. Counting only the object hanging
directly from a sub-bar (not its whole load) leaves no solution, so that rule is needed."""
import itertools, json, os
K = 9
# bar: (left item, left arm, right item, right arm); items are objects or other bars
BARS = {'T': ('P', 2, 'Q', 1), 'P': ('B', 3, 'A', 1), 'Q': ('C', 3, 'R', 1), 'R': ('D', 3, 'K', 1)}


def load(x, w, whole=True):
    if x not in BARS: return w[x]
    l, _, r, _ = BARS[x]
    return load(l, w, whole) + load(r, w, whole) if whole else 0


def ok(w, whole=True):
    for l, a, r, b in BARS.values():
        lw = load(l, w, whole) if (whole or l not in BARS) else first(l, w)
        rw = load(r, w, whole) if (whole or r not in BARS) else first(r, w)
        if lw * a != rw * b: return False
    return True


def first(bar, w):   # the trap: a sub-bar counted as only the object on its left end
    l = BARS[bar][0]
    return first(l, w) if l in BARS else w[l]


sols, trap = [], []
for t in itertools.product(range(1, 10), repeat=4):
    w = dict(zip('ABCD', t)); w['K'] = K
    if ok(w): sols.append(''.join(map(str, t)))
    if ok(w, whole=False): trap.append(''.join(map(str, t)))
print('solutions', sols, 'counting one object per sub-bar', trap)
assert sols == ['6243'] and trap == []
json.dump({'unique_answer': sols[0], 'assignments_tested': 9 ** 4, 'K': K, 'bars': BARS, 'without_whole_load_rule': trap,
           'why': 'D x 3 = 9 x 1 so D = 3; C x 3 = (3 + 9) x 1 so C = 4; (A + B) x 2 = (4 + 3 + 9) x 1 so A + B = 8; B x 3 = A x 1 so B = 2, A = 6'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
