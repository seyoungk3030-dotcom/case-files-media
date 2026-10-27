"""ROOM 047 proof: four cube nets A-D lie flat; each has one star face and five numbered faces. Folded into a cube,
which number ends up opposite the star? Code = that number for A, B, C, D. The fold is computed by rolling the net
face by face (fold.py), so each answer is forced. The trap picks the face farthest from the star on the flat net."""
import json, os
from fold import fold
STAR = '*'
NETS = {   # (col, row) -> label; row grows downward on the card
 'A': {(1, 0): STAR, (0, 1): 3, (1, 1): 1, (2, 1): 8, (3, 1): 4, (2, 2): 7},
 'B': {(0, 0): STAR, (1, 0): 6, (1, 1): 8, (2, 1): 2, (3, 1): 3, (3, 2): 5},
 'C': {(0, 0): 4, (1, 0): STAR, (2, 0): 1, (2, 1): 7, (3, 1): 5, (4, 1): 9},
 'D': {(0, 0): STAR, (1, 0): 2, (1, 1): 6, (2, 1): 9, (2, 2): 4, (3, 2): 1},
}


def solve(net):
    s = next(c for c, v in net.items() if v == STAR)
    N = fold(list(net), s)
    opp = next(c for c in net if N[c] == (0, 0, 1))
    d = lambda c: abs(c[0] - s[0]) + abs(c[1] - s[1])
    far = [net[c] for c in net if d(c) == max(map(d, net))]
    return s, opp, net[opp], far


res = {k: solve(n) for k, n in NETS.items()}
for k, n in NETS.items():
    vals = [v for v in n.values() if v != STAR]
    assert len(n) == 6 and len(set(vals)) == 5 and list(n.values()).count(STAR) == 1
code = ''.join(str(res[k][2]) for k in 'ABCD')
trap = ''.join(str(next(v for v in res[k][3] if v != res[k][2])) for k in 'ABCD')
print(code, trap, {k: (r[1], r[3]) for k, r in res.items()})
assert code == '7259' and all(res[k][2] not in res[k][3] for k in 'BCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'trap_farthest_face': trap,
               'nets': {k: {f'{c[0]},{c[1]}': v for c, v in n.items()} for k, n in NETS.items()},
               'opposite_cell': {k: list(r[1]) for k, r in res.items()},
               'why': '별 면을 바닥에 두고 전개도를 한 칸씩 접어 올리면 윗면이 별의 반대편. 한 줄에서 한 칸 건너뛴 면이 마주 보는 면.'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'),
              ensure_ascii=False, indent=1)
