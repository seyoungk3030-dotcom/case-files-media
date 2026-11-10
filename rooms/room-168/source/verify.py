"""ROOM 168 proof: bookworm. Books stand on a shelf in order (vol 1 at the left), spines facing us, each t cm thick
(covers ignored). Seen this way, a book's first page lies at its RIGHT edge and its last page at its LEFT edge. A worm
bores straight from the first page of vol a to the last page of vol b. Each book spans [x, x + t]; the worm's path is
|left edge of b - right edge of a| cm. Digit = that distance. All 10^4 codes compared; exactly one matches. The trap:
adding up every book from a to b (as if page 1 were on the left)."""
import itertools, json, os

BOARDS = {'A': {'t': [2, 2, 2], 'a': 1, 'b': 3}, 'B': {'t': [3, 1, 2, 3], 'a': 1, 'b': 4},
          'C': {'t': [2, 2, 1, 3, 2], 'a': 2, 'b': 5}, 'D': {'t': [1, 2, 3, 2], 'a': 4, 'b': 2}}


def edges(t):
    x = 0; E = []
    for w in t: E.append((x, x + w)); x += w
    return E


GOOD = {}; TRAPV = {}
for k, b in BOARDS.items():
    E = edges(b['t']); first = E[b['a'] - 1][1]; last = E[b['b'] - 1][0]
    GOOD[k] = abs(last - first)
    lo, hi = sorted((b['a'], b['b'])); TRAPV[k] = sum(b['t'][lo - 1:hi])
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and code != trap and all(v < 10 for v in GOOD.values())
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'cm': GOOD, 'trap_whole_books': trap,
               'why': '책등이 보이게 꽂힌 책은 1쪽이 오른쪽 끝, 마지막 쪽이 왼쪽 끝에 있어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
