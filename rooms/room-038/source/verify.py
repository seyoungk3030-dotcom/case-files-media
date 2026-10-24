"""ROOM 038 proof: a 4-dial lock, four tries with lamp feedback. Green lamp = right digit in the right place,
amber lamp = right digit in the wrong place. Digits in the code don't repeat. All 5040 codes are tested; exactly one
fits every try, and dropping any one try leaves more than one code, so each try is needed."""
import itertools, json, os
TRIES = ['8395', '9720', '6917', '2805']
CODE = '8361'
C = [''.join(p) for p in itertools.permutations('0123456789', 4)]


def fb(g, a):
    r = sum(x == y for x, y in zip(g, a)); return r, len(set(g) & set(a)) - r


LAMPS = [fb(t, CODE) for t in TRIES]
fits = lambda c, idx: all(fb(TRIES[i], c) == LAMPS[i] for i in idx)
sols = [c for c in C if fits(c, range(4))]
need = [len([c for c in C if fits(c, [j for j in range(4) if j != i])]) for i in range(4)]
trap = '8316'
print('lamps', LAMPS, 'solutions', sols, 'without each try', need, 'trap fails', [i for i in range(4) if fb(TRIES[i], trap) != LAMPS[i]])
assert sols == [CODE] and all(n > 1 for n in need) and not fits(trap, range(4))
json.dump({'unique_answer': CODE, 'codes_tested': len(C), 'tries': TRIES, 'lamps_green_amber': LAMPS,
           'codes_left_without_each_try': need, 'trap': trap,
           'why': '9720 → 9 7 2 0 없음 · 8395 → 8 3 제자리, 9 5 없음 · 2805 → 8 하나 (0 2 5 없음) · 6917 → 6 1 자리 다름 → 8 3 6 1'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
