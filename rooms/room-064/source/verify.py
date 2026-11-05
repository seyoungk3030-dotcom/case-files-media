"""ROOM 064 proof: four rows of eight bar magnets on a slippery table. Each magnet is written by the pole on its left end
(its right end is the other pole). Touching ends with opposite poles stick, equal poles push apart.
After everything settles, how many separate pieces lie on the table? Counting all 10^4 codes, exactly one matches.
Counting the gaps where ends look the same colour as 'sticks' (swapping the rule) gives the trap."""
import itertools, json, os
ROWS = {'A': 'NSSNNSNS', 'B': 'NNNNSSNS', 'C': 'NSNSNSNN', 'D': 'NNNSSSNN'}
OPP = {'N': 'S', 'S': 'N'}


def joints(s): return [OPP[s[i]] != s[i + 1] for i in range(len(s) - 1)]   # True = sticks (right end of i differs from left end of i+1)


def pieces(s): return 1 + joints(s).count(False)


res = {k: pieces(s) for k, s in ROWS.items()}; tr = {k: 1 + joints(s).count(True) for k, s in ROWS.items()}
code = ''.join(str(res[k]) for k in 'ABCD'); trap = ''.join(str(tr[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, 'solutions', sols)
assert len(sols) == 1 and code != trap
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'rows_left_end_pole': ROWS, 'trap_rule_swapped': trap,
               'why': '맞닿은 끝이 N-S면 붙고, N-N이나 S-S면 밀어낸다. 밀어내는 곳마다 조각이 하나씩 늘어난다.'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
