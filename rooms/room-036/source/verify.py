"""ROOM 036 proof: cups A B C D stand on spots 1-4. Four swaps are made, each swapping the cups standing on two SPOTS.
Code = the spot where A, B, C, D end up. All 4! end arrangements are tested against the swaps; exactly one fits.
Reading the swaps as swapping LETTERS (the cups first named on those spots) gives a different code, so the rule matters."""
import itertools, json, os
SWAPS = [(1, 2), (1, 3), (1, 4), (3, 4)]


def run(swaps, by_letter=False):
    spot = {1: 'A', 2: 'B', 3: 'C', 4: 'D'}
    for a, b in swaps:
        if by_letter:   # wrong reading: swap the cups whose ORIGINAL spots were a and b
            x, y = 'ABCD'[a - 1], 'ABCD'[b - 1]
            pa = next(k for k, v in spot.items() if v == x); pb = next(k for k, v in spot.items() if v == y)
            spot[pa], spot[pb] = y, x
        else:
            spot[a], spot[b] = spot[b], spot[a]
    return ''.join(str(next(k for k, v in spot.items() if v == c)) for c in 'ABCD')


truth = run(SWAPS)
sols = [''.join(p) for p in itertools.permutations('1234') if ''.join(p) == truth]
trap = run(SWAPS, by_letter=True)
print('solutions', sols, 'trap', trap)
assert sols == ['2431'] and trap != sols[0]
json.dump({'unique_answer': sols[0], 'arrangements_tested': 24, 'swaps': SWAPS, 'trap_swap_letters': trap,
           'steps': ['BACD', 'CABD', 'DABC', 'DACB'],
           'why': '자리 1-2: B A C D → 자리 1-3: C A B D → 자리 1-4: D A B C → 자리 3-4: D A C B'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
