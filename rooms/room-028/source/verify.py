"""ROOM 028 proof: four 3x5 picture-logic panels (nonogram rules: each clue is a run of lit bulbs, in order, with at least
one dark bulb between runs). For each panel, enumerate all 2^15 bulb patterns, prove exactly one matches its row and
column clues, and read the lit shape as a digit in the board's 3x5 font. Also record the trap: panels A, B and D share
identical row clues, so only the column clues tell 5, 2 and 3 apart."""
import itertools, json, os
FONT = {'0': ['###', '#.#', '#.#', '#.#', '###'], '1': ['.#.', '##.', '.#.', '.#.', '###'], '2': ['###', '..#', '###', '#..', '###'],
        '3': ['###', '..#', '###', '..#', '###'], '4': ['#.#', '#.#', '###', '..#', '..#'], '5': ['###', '#..', '###', '..#', '###'],
        '6': ['###', '#..', '###', '#.#', '###'], '7': ['###', '..#', '.#.', '.#.', '.#.'], '8': ['###', '#.#', '###', '#.#', '###'],
        '9': ['###', '#.#', '###', '..#', '###']}
ANSWER = '5293'


def runs(s): return tuple(len(x) for x in s.split('.') if x)
def clues(g): return tuple(runs(r) for r in g), tuple(runs(''.join(r[c] for r in g)) for c in range(3))


patterns = [[''.join(b[i * 3:i * 3 + 3]) for i in range(5)] for b in itertools.product('.#', repeat=15)]
CLUES = [clues(FONT[d]) for d in ANSWER]
code, sols = '', []
for k, cl in enumerate(CLUES):
    m = [g for g in patterns if clues(g) == cl]
    assert len(m) == 1, k
    digit = [d for d, f in FONT.items() if f == m[0]]
    assert len(digit) == 1
    code += digit[0]; sols.append(m[0])
print(len(patterns), code)
assert code == ANSWER
assert CLUES[0][0] == CLUES[1][0] == CLUES[3][0] and len({CLUES[i][1] for i in (0, 1, 3)}) == 3
json.dump({'unique_answer': code, 'patterns_tested_per_panel': len(patterns),
           'panels': {k: {'rows': [list(r) for r in cl[0]], 'cols': [list(c) for c in cl[1]], 'solution': s}
                      for k, cl, s in zip('ABCD', CLUES, sols)},
           'trap': 'A, B, D have identical row clues; column clues decide 5 / 2 / 3'},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
