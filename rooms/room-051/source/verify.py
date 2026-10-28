"""ROOM 051 proof: four 3D objects A (ball) B (cube) C (pyramid) D (star) in four picture equations.
Every whole value 0-39 for each object is tried (40^4 combinations, multiplication before addition); exactly one fits all four
lines, and dropping any line leaves more than one. The trap reads line 4 left to right ((D + C) x A)."""
import itertools, json, os
LINES = [('A + A + A', 12), ('A + B', 6), ('B + C + C', 16), ('D + C × A', 36)]


def val(expr, v, left_to_right=False):
    p = expr.split(); terms = [[v[p[0]]]]
    for op, k in zip(p[1::2], p[2::2]):
        if left_to_right: terms = [[sum(map(lambda t: t[0] * (t[1] if len(t) > 1 else 1), terms)) * v[k]]] if op == '×' else terms + [[v[k]]]
        elif op == '×': terms[-1].append(v[k])
        else: terms.append([v[k]])
    out = 0
    for t in terms:
        r = 1
        for n in t: r *= n
        out += r
    return out


def fits(v, idx, ltr=False): return all(val(LINES[i][0], v, ltr) == LINES[i][1] for i in idx)


ALL = [dict(zip('ABCD', c)) for c in itertools.product(range(40), repeat=4)]
sols = [v for v in ALL if fits(v, range(4))]
need = [len([v for v in ALL if fits(v, [j for j in range(4) if j != i])]) for i in range(4)]
trap_sols = [v for v in ALL if fits(v, range(4), True)]
code = ''.join(str(sols[0][k]) for k in 'ABCD'); trap = ''.join(str(trap_sols[0][k]) for k in 'ABCD')
print(code, trap, need, len(trap_sols))
assert len(sols) == 1 and code == '4278' and all(n > 1 for n in need) and len(trap_sols) == 1 and trap == '4272'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'combinations_tested': len(ALL), 'lines': LINES, 'trap_left_to_right': trap,
               'solutions_without_each_line': need,
               'why': 'A+A+A=12 → A=4 · 4+B=6 → B=2 · 2+C+C=16 → C=7 · D+7×4=36 → D+28=36 → D=8'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
