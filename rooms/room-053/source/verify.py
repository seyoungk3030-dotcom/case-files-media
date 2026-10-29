"""ROOM 053 proof: two level seesaws fix the weights (c = ball, s = cube, r = star; same shape = same weight), then
four seesaws A-D have only a '?' on the right: how many balls balance the left side. Every whole weight 1-30 for each
shape is tried; every fitting set gives the same four counts. The trap counts the objects on the left instead."""
import itertools, json, os
REFS = [('s', 'ccc'), ('r', 'scc')]
ASK = {'A': 'r', 'B': 'ssc', 'C': 'sc', 'D': 'rsc'}


def w(side, v): return sum(v[k] for k in side)


fits = [v for v in (dict(zip('csr', t)) for t in itertools.product(range(1, 31), repeat=3))
        if all(w(L, v) == w(R, v) for L, R in REFS)]
codes = set()
for v in fits:
    n = {k: w(L, v) / v['c'] for k, L in ASK.items()}
    codes.add(''.join(str(int(n[k])) if n[k] == int(n[k]) else 'x' for k in 'ABCD'))
need = [len({tuple(sorted({k: x[k] / x['c'] for k in 'csr'}.items())) for x in (dict(zip('csr', t)) for t in itertools.product(range(1, 31), repeat=3))
             if all(w(L, x) == w(R, x) for j, (L, R) in enumerate(REFS) if j != i)}) for i in range(len(REFS))]
code = codes.pop() if len(codes) == 1 else None; trap = ''.join(str(len(ASK[k])) for k in 'ABCD')
print(code, trap, len(fits), need)
assert code == '5749' and not codes and all(n > 1 for n in need) and trap == '1323'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'weights_tested': 30 ** 3, 'fitting_weight_sets': len(fits), 'refs': REFS, 'ask': ASK,
               'trap_object_count': trap, 'ratios_without_each_ref': need,
               'why': '상자 = 공 3 · 별 = 상자 + 공 2 = 공 5 → A 5 · B 3+3+1 = 7 · C 3+1 = 4 · D 5+3+1 = 9'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
