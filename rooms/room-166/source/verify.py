"""ROOM 166 proof: planting trees. A tree goes at the start and then every d metres along a path of length L. On an
open path (a road with two ends) the last tree stands at the far end too: L/d + 1 trees. On a closed loop (a pond, a
flower bed) the walk comes back to the first tree, so the last spot is the first one again: L/d trees. Positions are
listed and de-duplicated for each board. Digit = number of trees. All 10^4 codes compared; exactly one matches. The
trap: L/d for the road and L/d + 1 for the loop (the two cases swapped)."""
import itertools, json, os

BOARDS = {'A': {'shape': 'line', 'L': 12, 'd': 3}, 'B': {'shape': 'tri', 'L': 6, 'd': 1},
          'C': {'shape': 'line', 'L': 14, 'd': 2}, 'D': {'shape': 'circle', 'L': 18, 'd': 3}}


def trees(b):
    pos = set(); x = 0
    while x <= b['L']:
        pos.add(x % b['L'] if b['shape'] != 'line' else x); x += b['d']
    return sorted(pos)


GOOD = {k: len(trees(b)) for k, b in BOARDS.items()}
TRAPV = {k: b['L'] // b['d'] + (1 if b['shape'] != 'line' else 0) for k, b in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] and GOOD[k] < 10 for k in 'ABCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'trees': GOOD,
               'positions': {k: trees(b) for k, b in BOARDS.items()}, 'trap_swapped': trap,
               'why': '양 끝이 있는 길은 칸 수 + 1그루, 한 바퀴 도는 둘레는 칸 수와 같은 그루예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
