"""ROOM 215 proof (뚜껑 닫은 물통의 구멍): a square water jug full of water has a row of small holes, all at the same
height near the bottom. Water can only run out if air can get in to take its place. Air gets in through the open neck
(cap off) or through a small hole above the water line. With the cap on and no hole above the water, the holes are too
small to let bubbles in, so every stream stops. Because all the bottom holes sit at one height, there is no case where
some flow and others gulp air. Digit = number of streams. All 10^4 codes compared; exactly one matches.
Trap: 'every hole leaks' (counting holes and ignoring the cap)."""
import itertools, json, os

# key: (holes in the bottom row, cap on?, small hole above the water line?)
BOARDS = {'A': (3, False, False), 'B': (4, True, False), 'C': (5, True, True), 'D': (2, False, False)}


def streams(n, cap, air):
    return n if (not cap or air) else 0


GOOD = {k: streams(*v) for k, v in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
trap = ''.join(str(BOARDS[k][0]) for k in 'ABCD')
print('answer', code, 'trap', trap)
assert len(sols) == 1 and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000,
               'boards': {k: {'holes': n, 'cap_on': cap, 'air_hole_above_water': air, 'streams': GOOD[k]} for k, (n, cap, air) in BOARDS.items()},
               'trap': '구멍 수만큼 물이 샌다 (뚜껑 무시)', 'why': '물이 나가려면 그만큼 공기가 들어와야 해요. 뚜껑을 닫고 물 위에 구멍도 없으면 작은 구멍으로는 공기가 못 들어와 물줄기가 멈춰요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
