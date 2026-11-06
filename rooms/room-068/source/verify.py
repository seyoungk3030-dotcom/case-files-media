"""ROOM 068 proof: tilt mazes. A 5x5 tray with blocks; a ball slides in the tilt direction until a block or the rim
stops it (it never stops half-way). After the three tilts shown, the number printed on the ball's cell is that board's
digit. The slide is simulated for every board, every 4-digit code is compared, exactly one matches. Moving one cell per
tilt (the trap) lands on another numbered cell."""
import itertools, json, os
N = 5
DIR = {'L': (-1, 0), 'R': (1, 0), 'U': (0, -1), 'D': (0, 1)}   # U = towards the far rim (top of the picture)
# blocks, ball start (col,row), tilts, printed numbers {cell: digit}
BOARDS = {
    'A': ({(2, 0), (0, 3), (3, 2)}, (4, 4), 'ULD', {(3, 1): 5, (3, 4): 8, (4, 0): 3, (3, 0): 1, (1, 1): 6}),
    'B': ({(1, 1), (4, 2), (2, 4)}, (0, 4), 'RUL', {(0, 2): 7, (0, 3): 4, (1, 4): 2, (1, 2): 9, (3, 3): 6}),
    'C': ({(3, 2), (1, 3), (0, 0)}, (4, 0), 'DLU', {(0, 1): 2, (3, 0): 6, (4, 4): 3, (0, 4): 8, (2, 2): 5}),
    'D': ({(2, 2), (4, 1), (1, 0)}, (0, 2), 'RUR', {(3, 1): 9, (2, 1): 1, (1, 2): 4, (1, 1): 7, (3, 3): 2}),
}


def slide(blocks, start, moves, one_step=False):
    c, r = start
    for m in moves:
        dc, dr = DIR[m]
        while 0 <= c + dc < N and 0 <= r + dr < N and (c + dc, r + dr) not in blocks:
            c, r = c + dc, r + dr
            if one_step: break
    return c, r


for k, (bl, st, mv, num) in BOARDS.items():
    assert st not in bl and st not in num and not (set(num) & bl), k
res = {k: BOARDS[k][3].get(slide(*BOARDS[k][:3])) for k in 'ABCD'}
one = {k: BOARDS[k][3].get(slide(*BOARDS[k][:3], one_step=True)) for k in 'ABCD'}
code = ''.join(str(res[k]) for k in 'ABCD'); trap = ''.join(str(one[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, 'solutions', sols)
assert sols == ['5729'] and trap == '8461'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'trap_one_cell_per_tilt': trap,
               'boards': {k: {'blocks': sorted(b[0]), 'start': b[1], 'tilts': b[2], 'numbers': {f'{c},{r}': d for (c, r), d in b[3].items()},
                              'path_end': slide(*b[:3])} for k, b in BOARDS.items()},
               'why': '구슬은 기울인 방향으로 벽이나 블록에 막힐 때까지 끝까지 굴러감. A 위→왼→아래 5 · B 오른→위→왼 7 · C 아래→왼→위 2 · D 오른→위→오른 9'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
