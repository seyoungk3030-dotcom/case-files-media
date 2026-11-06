"""ROOM 132 proof: a weather vane's arrow points INTO the wind (toward where the wind comes from): its broad tail is
pushed downwind, the arrow head swings round to face the wind. Each board has a compass rose with eight numbered
directions and a wind sign: A a flag (cloth streams downwind), B chimney smoke (drifts downwind), C a windsock (its
open mouth faces the wind, the sock streams downwind), D still air but the car carrying the vane drives east, so the
air rushes at it from the east. Digit = the number in the direction the vane's arrow points. All 10^4 codes are
compared; exactly one matches. The trap: 'the arrow points where the wind goes' (the downwind number)."""
import itertools, json, os

DIRS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
BOARDS = {'A': {'sign': 'flag', 'downwind': 'E', 'labels': [5, 2, 8, 7, 0, 4, 3, 1]},
          'B': {'sign': 'smoke', 'downwind': 'W', 'labels': [7, 4, 9, 1, 5, 2, 8, 6]},
          'C': {'sign': 'sock', 'downwind': 'N', 'labels': [4, 8, 2, 3, 6, 7, 1, 0]},
          'D': {'sign': 'car', 'downwind': 'W', 'labels': [3, 6, 1, 5, 9, 8, 7, 2]}}


def solve(b):
    assert len(set(b['labels'])) == 8
    d = DIRS.index(b['downwind']); return b['labels'][(d + 4) % 8], b['labels'][d], DIRS[(d + 4) % 8]


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) == solve(BOARDS[k])[0] for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap)
assert sols == ['3961'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'vane_points': {k: v[2] for k, v in RES.items()},
               'trap_downwind': trap, 'why': '풍향계는 넓은 꼬리가 바람에 밀려서 화살촉이 바람이 불어오는 쪽을 가리켜요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
