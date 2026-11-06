"""ROOM 154 proof: a 3x3 lamp-button panel (Lights Out). Pressing a button flips its own lamp and the lamps directly
above/below/left/right of it (on <-> off). Goal: every lamp off. All 2^9 press sets are tried for each panel (pressing a
button twice undoes it, and order does not matter, so a set is a full plan). Digit = fewest presses that switch every
lamp off. All 10^4 codes compared; exactly one matches. The trap: one press per lit lamp (count the lit lamps)."""
import itertools, json, os
N = 3
BOARDS = {'A': ['111', '111', '110'], 'B': ['111', '000', '111'], 'C': ['000', '010', '000'], 'D': ['101', '111', '101']}


def apply(g, presses):
    g = [[int(ch) for ch in row] for row in g]
    for r, c in presses:
        for dr, dc in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= r + dr < N and 0 <= c + dc < N: g[r + dr][c + dc] ^= 1
    return g


CELLS = [(r, c) for r in range(N) for c in range(N)]
SOL = {}
for k, g in BOARDS.items():
    ok = [s for n in range(10) for s in itertools.combinations(CELLS, n) if not any(map(any, apply(g, s)))]
    best = min(map(len, ok)); SOL[k] = [s for s in ok if len(s) == best]; assert len(SOL[k]) == 1
code = ''.join(str(len(SOL[k][0])) for k in 'ABCD')
trap = ''.join(str(sum(row.count('1') for row in g)) for g in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, SOL)
assert sols == ['4253'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'press': {k: v[0] for k, v in SOL.items()},
               'trap_lit_count': trap, 'why': '버튼 하나가 십자 모양으로 다섯 개까지 뒤집어서, 켜진 램프 수와 눌러야 할 횟수는 전혀 달라요. 누를 버튼은 십자들이 겹쳐서 켜진 모양을 만드는 자리예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
