"""ROOM 148 proof: a sandpile that collapses (the Abelian sandpile). A 5x5 tray holds stacks of 0-3 sand blocks. One
block is added on the starred square. Any square that reaches 4 blocks collapses: it loses 4 and pushes one block onto
each square above/below/left/right (a block pushed off the edge is lost). Collapses keep going until every square holds
3 or fewer. Simulated exactly. Digit = how many collapses happen in total. All 10^4 codes compared; exactly one matches.
The trap: counting only the first wave (the starred square plus its neighbours that already held 3)."""
import itertools, json, os
N = 5
BOARDS = {'A': {'g': ['03110', '33001', '13330', '32000', '10131'], 'star': (2, 3)},
          'B': {'g': ['22011', '32301', '33300', '00333', '02200'], 'star': (3, 3)},
          'C': {'g': ['03031', '13311', '03020', '00101', '20010'], 'star': (0, 1)},
          'D': {'g': ['23002', '03210', '23333', '00003', '01001'], 'star': (0, 1)}}
NB = ((1, 0), (-1, 0), (0, 1), (0, -1))


def run(b):
    g = [[int(ch) for ch in row] for row in b['g']]; r0, c0 = b['star']; g[r0][c0] += 1; order = []
    while True:
        top = [(r, c) for r in range(N) for c in range(N) if g[r][c] >= 4]
        if not top: return order, g
        for r, c in top:
            g[r][c] -= 4; order.append((r, c))
            for dr, dc in NB:
                if 0 <= r + dr < N and 0 <= c + dc < N: g[r + dr][c + dc] += 1


RES = {k: run(b) for k, b in BOARDS.items()}
code = ''.join(str(len(RES[k][0])) for k in 'ABCD')
trap = ''.join(str(1 + sum(1 for dr, dc in NB if 0 <= b['star'][0] + dr < N and 0 <= b['star'][1] + dc < N and b['g'][b['star'][0] + dr][b['star'][1] + dc] == '3')) for b in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['6948'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'collapsed': {k: r[0] for k, r in RES.items()},
               'final': {k: [''.join(map(str, row)) for row in r[1]] for k, r in RES.items()}, 'trap_first_wave': trap,
               'why': '무너진 칸이 옆 칸에 하나씩 얹어 주면, 3개였던 옆 칸도 4개가 돼서 연달아 무너져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
