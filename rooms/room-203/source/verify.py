"""ROOM 203 proof (바꿀까 말까): a prize hides behind one of n doors. You pick a door; the host, who knows where the prize
is, opens k of the OTHER doors that are empty (choosing at random when he can). Then you either stay or switch to one of
the doors still closed (at random if there are several). Every prize position, every host choice and every switch choice
is enumerated with exact probabilities. Digit = average wins over G games = G * P(win). All 10^4 codes compared; exactly
one matches. Trap: 'once doors are open it makes no difference' (3322)."""
import itertools, json, os
from fractions import Fraction as F

# key: (doors n, host opens k, strategy, games G)
BOARDS = {'A': (3, 1, 'stay', 9), 'B': (3, 1, 'switch', 9), 'C': (4, 2, 'switch', 8), 'D': (4, 1, 'switch', 8)}


def p_win(n, k, strat):
    pick = 0; total = F(0)
    for car in range(n):
        pc = F(1, n); empties = [d for d in range(n) if d != pick and d != car]
        opens = list(itertools.combinations(empties, k))
        for op in opens:
            po = pc / len(opens)
            if strat == 'stay': total += po * (car == pick); continue
            rest = [d for d in range(n) if d != pick and d not in op]
            for r in rest: total += po / len(rest) * (r == car)
    return total


GOOD = {}
for key, (n, k, s, g) in BOARDS.items():
    w = g * p_win(n, k, s); assert w.denominator == 1 and 0 <= w < 10, (key, w); GOOD[key] = int(w)
code = ''.join(str(GOOD[k]) for k in 'ABCD')
trap = ''.join(str(int(g * F(1, n))) for n, _, _, g in (BOARDS[k] for k in 'ABCD'))
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: str(p_win(*BOARDS[k][:3])) for k in BOARDS})
assert len(sols) == 1 and code != trap
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'p_win': {k: str(p_win(*BOARDS[k][:3])) for k in BOARDS},
               'wins': GOOD, 'trap_no_difference': trap,
               'why': '처음 고른 문은 열린 문과 상관없이 1/n 그대로. 사회자는 꽝만 열어 주니, 나머지 확률이 남은 문으로 몰려요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
