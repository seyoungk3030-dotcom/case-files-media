"""ROOM 069 proof: identical cups nest in a stack. One cup is H tiles tall and every extra cup adds only its rim, h tiles:
height(n) = H + (n-1)*h. Each board shows two stacks with their heights; H and h are solved from them (whole numbers,
h > 0, H > h) and must be the only solution in 1..9; the third stack's height is the digit. Scaling the height in
proportion to the number of cups (the trap) is not even a whole number on A, and gives other values elsewhere."""
import itertools, json, os
from fractions import Fraction as Fr
BOARDS = {'A': ((2, 4), (4, 6), 5), 'B': ((1, 4), (3, 8), 2), 'C': ((2, 6), (3, 7), 4), 'D': ((3, 4), (5, 6), 2)}
res, prop = {}, {}
for k, ((n1, t1), (n2, t2), q) in BOARDS.items():
    sol = [(H, h) for H in range(1, 10) for h in range(1, 10) if H > h and H + (n1 - 1) * h == t1 and H + (n2 - 1) * h == t2]
    assert len(sol) == 1, (k, sol); H, h = sol[0]; res[k] = H + (q - 1) * h; assert res[k] <= 9
    prop[k] = Fr(t2 * q, n2)
code = ''.join(str(res[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'solutions', sols, 'proportional', {k: str(v) for k, v in prop.items()})
assert sols == ['7683'] and all(prop[k] != res[k] for k in 'ABCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_ref1_ref2_ask': BOARDS, 'heights': res,
               'trap_proportional': {k: str(v) for k, v in prop.items()},
               'why': '컵은 겹쳐지니까 한 개 더 쌓을 때마다 테두리만큼만 높아짐. A 2개4·4개6 → 1개3, 테두리1 → 5개7 · B 1개4, 테두리2 → 2개6 · C 1개5, 테두리1 → 4개8 · D 1개2, 테두리1 → 2개3'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
