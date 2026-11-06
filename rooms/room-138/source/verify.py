"""ROOM 138 proof: river crossing. A farmer must take every item from the left bank to the right bank in a boat that
holds the farmer plus up to `cap` items; only the farmer can row. An arrow X -> Y means X eats Y when the farmer is
not on that bank. Breadth-first search over all states gives the least number of one-way crossings. Digit = that
number. All 10^4 codes are compared; exactly one matches. The trap: 'one trip per item' (number of items, there and
back counted as 2 per item minus the last return: 2n - 1)."""
import itertools, json, os
from collections import deque

BOARDS = {'A': {'items': ['늑대', '염소', '양배추'], 'eats': [['늑대', '염소'], ['염소', '양배추']], 'cap': 1},
          'B': {'items': ['늑대', '염소', '양배추'], 'eats': [['늑대', '염소'], ['염소', '양배추']], 'cap': 2},
          'C': {'items': ['고양이', '쥐', '쌀'], 'eats': [['고양이', '쥐']], 'cap': 1},
          'D': {'items': ['여우', '닭', '옥수수', '수박'], 'eats': [['여우', '닭'], ['닭', '옥수수']], 'cap': 1}}


def safe(bank, eats): return not any(a in bank and b in bank for a, b in eats)


def solve(b):
    items = frozenset(b['items']); start = (items, 0); goal = (frozenset(), 1); seen = {start: 0}; q = deque([start])
    while q:
        left, f = q.popleft(); d = seen[(left, f)]
        if (left, f) == goal: return d
        here = left if f == 0 else items - left
        for r in range(b['cap'] + 1):
            for load in itertools.combinations(sorted(here), r):
                nl = left - set(load) if f == 0 else left | set(load); nf = 1 - f
                stay = nl if nf == 1 else items - nl
                if not safe(stay, b['eats']): continue
                st = (frozenset(nl), nf)
                if st not in seen: seen[st] = d + 1; q.append(st)
    raise ValueError('no solution')


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k]) for k in 'ABCD'); trap = ''.join(str(min(9, 2 * len(BOARDS[k]['items']) - 1)) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) == solve(BOARDS[k]) for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap)
assert sols == [code] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'trap_simple_trips': trap,
               'why': '먹히는 짝이 둘만 남지 않게 하려면, 가끔 건너간 것을 다시 데려와야 해요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
