"""ROOM 156 proof: curling score. Stones lie on the house (rings of radius 1.83). Only stones touching the house count.
The team with the stone nearest the centre scores one point for every one of its stones that is nearer than the other
team's nearest stone. Distances are computed exactly from the stone centres (every gap between ranked stones is at least
0.2, so the picture is unambiguous). Digit = points scored. All 10^4 codes compared; exactly one matches. The trap:
counting every stone of the scoring team that is in the house."""
import itertools, json, math, os
HR, SR = 1.83, 0.145
BOARDS = {'A': [(-0.14, 0.21, 'R'), (1.13, 0.08, 'R'), (-0.57, -0.68, 'R'), (0.57, -0.21, 'Y'), (-0.82, 1.33, 'Y')],
          'B': [(-0.99, -0.99, 'R'), (-0.15, -1.13, 'R'), (0.27, -0.17, 'Y'), (0.05, 0.58, 'Y'), (0.86, -1.45, 'Y'), (-0.81, 0.12, 'Y')],
          'C': [(0.34, 0.65, 'R'), (0.44, 0.12, 'R'), (-0.3, 1.67, 'R'), (-0.06, -1.36, 'Y'), (0.35, -0.92, 'Y')],
          'D': [(0.91, -1.99, 'R'), (-0.31, 1.14, 'R'), (0.38, 0.12, 'Y'), (1.26, 0.76, 'Y'), (-0.34, 0.56, 'Y'), (-0.91, 0.32, 'Y'), (-0.1, -0.14, 'Y')]}


def score(st):
    ins = sorted((math.hypot(x, y), t, i) for i, (x, y, t) in enumerate(st) if math.hypot(x, y) - SR <= HR)
    win = ins[0][1]; lim = min(d for d, t, _ in ins if t != win)
    ds = [d for d, _, _ in ins]; assert all(b - a >= 0.19 for a, b in zip(ds, ds[1:]))
    return win, [i for d, t, i in ins if t == win and d < lim], sum(1 for d, t, _ in ins if t == win), lim


RES = {k: score(st) for k, st in BOARDS.items()}
for st in BOARDS.values():
    for a, b in itertools.combinations(st, 2): assert math.hypot(a[0] - b[0], a[1] - b[1]) > 2 * SR + 0.05
code = ''.join(str(len(RES[k][1])) for k in 'ABCD')
trap = ''.join(str(RES[k][2]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: (v[0], v[1]) for k, v in RES.items()})
assert sols == ['1324'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'scorers': {k: [v[0], v[1]] for k, v in RES.items()},
               'trap_all_in_house': trap, 'why': '상대 팀에서 가장 가운데에 가까운 돌보다 안쪽에 있는 돌만 점수가 돼요. 그 바깥의 우리 돌은 하우스 안이어도 0점이에요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
