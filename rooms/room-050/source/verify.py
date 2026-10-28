"""ROOM 050 proof: four matchstick figures A-D on a unit grid. Code = how many squares of any size each figure has
(a k x k square counts when all 4k of its edge matches are there). Squares are counted by checking every position and
size. The trap counts only the smallest squares."""
import json, os


def grid(w, h, drop=()):
    s = {('h', x, y) for x in range(w) for y in range(h + 1)} | {('v', x, y) for x in range(w + 1) for y in range(h)}
    return s - set(drop)


FIGS = {
 'A': grid(2, 2, drop=[('h', 0, 1)]),
 'B': grid(3, 2),
 'C': grid(3, 3, drop=[('v', 1, 1), ('v', 2, 1), ('h', 1, 1), ('h', 1, 2)]),
 'D': grid(3, 3, drop=[('v', 1, 0), ('v', 2, 0)]),
}


def squares(S):
    xs = max(x for _, x, _ in S) + 2; ys = max(y for _, _, y in S) + 2; out = []
    for k in range(1, 6):
        for x in range(xs):
            for y in range(ys):
                need = [('h', x + i, y) for i in range(k)] + [('h', x + i, y + k) for i in range(k)] + \
                       [('v', x, y + j) for j in range(k)] + [('v', x + k, y + j) for j in range(k)]
                if all(e in S for e in need): out.append((x, y, k))
    return out


res = {k: squares(S) for k, S in FIGS.items()}
code = ''.join(str(len(res[k])) for k in 'ABCD')
trap = ''.join(str(sum(1 for q in res[k] if q[2] == 1)) for k in 'ABCD')
print(code, trap, {k: len(S) for k, S in FIGS.items()})
assert all(len(v) < 10 for v in res.values()) and code == '3859' and all(a != b for a, b in zip(code, trap))
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'trap_small_only': trap, 'matches': {k: len(S) for k, S in FIGS.items()},
               'squares': {k: [list(q) for q in v] for k, v in res.items()}},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
