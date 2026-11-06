"""ROOM 105 proof: a chess knight on a 6x6 board (rows 0-5 from the far side, columns 0-5 from the left). It jumps
in an L (2 + 1 squares) and may pass over anything, but it can never land on a square holding one of its own pawns
(not even on the middle stop). Four squares are numbered; each digit is the number of the one square the knight can
reach in exactly two jumps. All 10^4 codes are compared; exactly one matches. The trap: ignoring the pawns gives
another code (a square whose only middle stops all hold pawns). Boards from gen105 (seed 105), checked here."""
import itertools, json, os

N = 6
JUMPS = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
BOARDS = {'A': {'knight': (2, 1), 'pawns': [(1, 0), (1, 3), (1, 4), (4, 2)], 'num': {1: (4, 0), 2: (4, 5), 3: (0, 5), 4: (3, 1)}},
          'B': {'knight': (5, 0), 'pawns': [(1, 2), (2, 4), (3, 0), (3, 4), (4, 2)], 'num': {1: (5, 4), 2: (4, 1), 3: (3, 1), 4: (1, 0)}},
          'C': {'knight': (5, 1), 'pawns': [(0, 3), (2, 4), (3, 1), (3, 2), (5, 4)], 'num': {1: (5, 5), 2: (5, 2), 3: (4, 3), 4: (1, 3)}},
          'D': {'knight': (2, 4), 'pawns': [(4, 2), (4, 3), (5, 0), (5, 4)], 'num': {1: (0, 3), 2: (1, 4), 3: (2, 0), 4: (5, 5)}}}


def jumps(p, block): return [(p[0] + a, p[1] + b) for a, b in JUMPS if 0 <= p[0] + a < N and 0 <= p[1] + b < N and (p[0] + a, p[1] + b) not in block]


def two(k, block): return {q for m in jumps(k, block) for q in jumps(m, block)}


def answer(k, pawns=True):
    b = BOARDS[k]; block = set(b['pawns']) if pawns else set()
    assert b['knight'] not in b['pawns'] and not set(b['num'].values()) & set(b['pawns'])
    return [n for n, c in b['num'].items() if c in two(b['knight'], block)]


RES = {k: answer(k) for k in 'ABCD'}; assert all(len(v) == 1 for v in RES.values())
TR = {k: [n for n in answer(k, False) if n not in RES[k]] for k in 'ABCD'}; assert all(len(v) == 1 for v in TR.values())
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(TR[k][0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['2413'] and trap != code
if __name__ == '__main__':
    mids = {k: [m for m in jumps(BOARDS[k]['knight'], set(BOARDS[k]['pawns'])) if BOARDS[k]['num'][RES[k][0]] in jumps(m, set(BOARDS[k]['pawns']))] for k in 'ABCD'}
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'reach_two': RES, 'middle_stops': mids, 'trap_ignore_pawns': trap,
               'why': '말은 L자로 뛰어 넘지만 자기 폰이 있는 칸에는 내릴 수 없어요. 첫 번째 착지 칸이 막히면 그 길은 끝'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
