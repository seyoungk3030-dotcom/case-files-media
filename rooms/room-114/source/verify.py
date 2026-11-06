"""ROOM 114 proof: the water-glass arrow flip. A card with 2 rows x 4 columns of arrows (R = right, L = left, U = up)
hangs on the wall. A round glass stands in front, covering two neighbouring columns. Water is poured up to a marked
row level: rows behind the water are seen through a water cylinder, which acts as a lens and flips the picture left
to right (the card is far enough behind it). So behind the water R and L swap; U stays U; arrows above the water or
outside the glass do not change. Digit = how many arrows point RIGHT as seen after pouring. All 10^4 codes are
compared; exactly one matches. The trap: the count before pouring."""
import itertools, json, os, random

# rows: index 0 = top row, 1 = bottom row. water: how many rows from the bottom are under water (1 or 2).
BOARDS = {'A': {'rows': ['URLU', 'LLLL'], 'glass': (1, 2), 'water': 1},
          'B': {'rows': ['RLUR', 'RRRR'], 'glass': (1, 2), 'water': 2},
          'C': {'rows': ['ULUL', 'RULR'], 'glass': (0, 1), 'water': 1},
          'D': {'rows': ['LLLR', 'RLLR'], 'glass': (1, 2), 'water': 2}}
FLIP = {'R': 'L', 'L': 'R', 'U': 'U'}


def seen(b):
    out = []
    for r, row in enumerate(b['rows']):
        wet = r >= 2 - b['water']; g = b['glass']
        cols = list(row)
        if wet:   # the lens flips the covered strip left to right: positions swap and each arrow turns around
            seg = [FLIP[c] for c in cols[g[0]:g[1] + 1]][::-1]; cols[g[0]:g[1] + 1] = seg
        out.append(''.join(cols))
    return out


S = {k: seen(b) for k, b in BOARDS.items()}
code = ''.join(str(sum(r.count('R') for r in S[k])) for k in 'ABCD')
trap = ''.join(str(sum(r.count('R') for r in BOARDS[k]['rows'])) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, S)
if __name__ == '__main__':
    assert sols == ['3517'] and trap != code and all(a != b for a, b in zip(code, trap))
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'seen': S, 'trap_before_water': trap,
               'why': '물이 든 둥근 컵은 볼록렌즈처럼 뒤의 그림을 좌우로 뒤집어 보여줘요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
