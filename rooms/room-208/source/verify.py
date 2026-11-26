"""ROOM 208 proof (김밥 자르는 시간): one kimbap roll is cut straight across, one cut at a time, every cut taking the same
time. n pieces need n - 1 cuts. Each board says how long n pieces took and asks for m pieces: seconds per cut =
T / (n - 1), answer = (m - 1) * T / (n - 1). Integer seconds on every board, checked exactly with fractions, and never equal
to the proportional trap T * m / n. All 10^4 codes compared; exactly one matches. Trap: 'pieces are proportional to time'."""
import itertools, json, os
from fractions import Fraction as Fr

# key: (pieces known n, seconds T, pieces asked m)
BOARDS = {'A': (3, 2, 6), 'B': (4, 3, 8), 'C': (5, 8, 3), 'D': (2, 3, 4)}


def secs(n, T, m):
    per = Fr(T, n - 1)
    return per, (m - 1) * per


GOOD, PER = {}, {}
for k, (n, T, m) in BOARDS.items():
    per, s = secs(n, T, m); assert s.denominator == 1 and per.denominator == 1 and 0 <= s < 10, (k, s)
    assert s != Fr(T * m, n), k            # the proportional answer is always wrong
    GOOD[k] = int(s); PER[k] = int(per)
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, PER)
assert len(sols) == 1
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000,
               'boards': {k: {'pieces_known': n, 'seconds': T, 'pieces_asked': m, 'sec_per_cut': PER[k], 'answer': GOOD[k]} for k, (n, T, m) in BOARDS.items()},
               'trap': '조각 수에 비례 (3조각 2초면 6조각 4초)', 'why': 'n조각은 칼질 n-1번. 칼질 한 번 시간 = 걸린 시간 ÷ (n-1)'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
