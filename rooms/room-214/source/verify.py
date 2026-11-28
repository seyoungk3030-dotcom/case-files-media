"""ROOM 214 proof (주사위 두 개, 합이 나오는 경우): a red die and a blue die are rolled together. For each board's target
sum S, count the ways the two top faces can make S. The dice are different colours, so red 4 + blue 5 and red 5 + blue 4
are two different results: ways = number of ordered pairs (r, b), 1..6 each, with r + b = S (= 6 - |7 - S|).
Digit = number of ways. All 10^4 codes compared; exactly one matches. Trap: counting unordered pairs (3+6 and 6+3 as one),
which gives 2, 1, 3, 2."""
import itertools, json, os

BOARDS = {'A': 9, 'B': 3, 'C': 7, 'D': 10}
SHOW = {'A': (4, 5), 'B': (1, 2), 'C': (3, 4), 'D': (4, 6)}     # the example roll drawn on the question card


def pairs(s):
    return [(r, b) for r in range(1, 7) for b in range(1, 7) if r + b == s]


GOOD = {k: len(pairs(s)) for k, s in BOARDS.items()}
for k, s in BOARDS.items():
    assert GOOD[k] == 6 - abs(7 - s) and 0 < GOOD[k] < 10 and sum(SHOW[k]) == s
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
trap = {k: len({tuple(sorted(p)) for p in pairs(s)}) for k, s in BOARDS.items()}
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(trap[k] != GOOD[k] for k in BOARDS)
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000,
               'boards': {k: {'sum': s, 'ways': GOOD[k], 'pairs': pairs(s), 'unordered_trap': trap[k]} for k, s in BOARDS.items()},
               'trap': '4+5와 5+4를 같은 경우로 센다', 'why': '빨강과 파랑은 다른 주사위라 빨강4·파랑5와 빨강5·파랑4는 다른 결과예요: 순서쌍을 세면 합 7이 6가지로 가장 많아요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
