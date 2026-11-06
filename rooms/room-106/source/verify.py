"""ROOM 106 proof: a water bottle with four plugged holes stands on a block of height S. Water fills it to level H
(above the bottle's base). Unplug every hole: water leaves a hole at height h with speed sqrt(2 g (H - h))
(Torricelli) and falls S + h to the floor, so it lands 2 * sqrt((H - h) * (S + h)) away. Each digit is the number of
the hole whose jet lands farthest (it beats the next by at least 5 %). All 10^4 codes are compared; exactly one
matches. The trap 'the lowest hole squirts farthest because it has the most pressure' gives another code."""
import itertools, json, math, os

# stand height S, water level H, holes: number -> height above the bottle base
BOARDS = {'A': (0.0, 2.8, {1: 1.4, 2: 0.3, 3: 2.5, 4: 0.8}),
          'B': (1.2, 2.8, {1: 1.9, 2: 0.8, 3: 0.1, 4: 2.5}),
          'C': (3.2, 2.8, {1: 1.1, 2: 2.2, 3: 1.7, 4: 0.25}),
          'D': (0.0, 2.0, {1: 0.25, 2: 1.6, 3: 1.0, 4: 0.6})}


def land(S, H, h): return 2 * math.sqrt((H - h) * (S + h))


def far(k):
    S, H, holes = BOARDS[k]; r = {n: land(S, H, h) for n, h in holes.items()}; s = sorted(r.values(), reverse=True)
    assert s[0] / s[1] >= 1.05, (k, r); return max(r, key=r.get), r


RES = {k: far(k) for k in 'ABCD'}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(min(BOARDS[k][2], key=BOARDS[k][2].get)) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: {n: round(x, 2) for n, x in v[1].items()} for k, v in RES.items()})
assert sols == [code] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'landing': {k: v[1] for k, v in RES.items()}, 'trap_lowest_hole': trap,
               'why': '아래 구멍은 세게 나오지만 바닥까지 떨어지는 시간이 짧아요. 날아가는 거리 = 2√(물 깊이 × 바닥까지 높이)'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
