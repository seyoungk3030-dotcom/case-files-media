"""ROOM 044 proof: a square sheet [-1,1]^2 is folded in half (right half onto the left, crease x=0) and, for B and D,
folded again (top half onto the bottom, crease y=0), then punched. Unfolding reflects every hole across each crease;
holes that land on a crease are their own mirror image and stay one hole. Code = number of holes after unfolding A-D.
Counting 'holes x layers' (ignoring holes cut on a crease) gives the trap."""
import json, os
SETUPS = {   # creases, punched hole centres on the folded piece (x <= 0, and y <= 0 when folded twice)
    'A': (('x',), [(-0.5, 0.2)]),
    'B': (('x', 'y'), [(-0.5, -0.3), (-0.3, -0.75)]),
    'C': (('x',), [(0.0, 0.4), (-0.5, -0.4)]),
    'D': (('x', 'y'), [(0.0, 0.0), (-0.5, -0.5)]),
}


def unfold(creases, holes):
    pts = {(round(x, 6), round(y, 6)) for x, y in holes}
    for c in reversed(creases):
        pts |= {(-x, y) if c == 'x' else (x, -y) for x, y in pts}
        pts = {(round(x, 6) + 0.0, round(y, 6) + 0.0) for x, y in pts}
    return sorted(pts)


res = {k: unfold(*v) for k, v in SETUPS.items()}
code = ''.join(str(len(res[k])) for k in 'ABCD')
trap = ''.join(str(len(SETUPS[k][1]) * 2 ** len(SETUPS[k][0])) for k in 'ABCD')
print(code, trap, res)
assert code == '2835' and trap == '2848' and code != trap
json.dump({'unique_answer': code, 'holes_after_unfolding': {k: len(v) for k, v in res.items()}, 'hole_positions': res,
           'trap_layers_times_holes': trap,
           'why': '접힌 선 위에 뚫은 구멍은 펼쳐도 하나. A 1x2=2, B 2x4=8, C 1+2=3, D 1+4=5'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
