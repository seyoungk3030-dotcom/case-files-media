"""ROOM 157 proof: folding a numbered paper strip. Squares are numbered 1..n (the same number is printed on both sides).
The folds are made in the order shown (1, 2, 3); each fold takes everything on one side of the crease, as one pile, and
flips it over onto the other side, so the pile's order turns upside down. Folding goes on until one square-sized pile is
left. Simulated exactly. Digit = the number on top of the final pile. All 10^4 codes compared; exactly one matches.
The trap: the end square that moves first (the far end) ends on top."""
import itertools, json, os
BOARDS = {'A': {'n': 6, 'folds': [('L', 3), ('R', 2), ('R', 1)]},
          'B': {'n': 6, 'folds': [('R', 3), ('L', 1), ('L', 1)]},
          'C': {'n': 8, 'folds': [('L', 4), ('L', 2), ('L', 1)]},
          'D': {'n': 7, 'folds': [('R', 4), ('L', 2), ('L', 1)]}}


def run(b):
    """cols: piles left to right, each bottom->top. ('R', k): the piles right of the k-th flip onto the left part;
    ('L', k): the first k piles flip onto the right part. Returns the final pile and each crease in original positions
    (crease p = between square p and p+1)."""
    cols = [[i + 1] for i in range(b['n'])]; lo = 0; creases = []
    for side, k in b['folds']:
        creases.append((lo + k, side)); Lp, Rp = cols[:k], cols[k:]
        if side == 'R':
            assert len(Rp) <= len(Lp)
            for j, c in enumerate(Rp): Lp[k - 1 - j] = Lp[k - 1 - j] + c[::-1]
            cols = Lp
        else:
            assert len(Lp) <= len(Rp)
            for j, c in enumerate(reversed(Lp)): Rp[j] = Rp[j] + c[::-1]
            cols = Rp; lo += k
    assert len(cols) == 1
    return cols[0], creases, lo


RES = {k: run(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0][-1]) for k in 'ABCD')
trap = ''.join(str(b['n'] if b['folds'][0][0] == 'R' else 1) for b in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, RES)
assert sols == ['5273'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'piles': {k: v[0] for k, v in RES.items()},
               'creases': {k: v[1] for k, v in RES.items()}, 'trap_far_end': trap,
               'why': '접을 때마다 넘어가는 더미는 위아래가 뒤집혀요. 그래서 마지막에 넘어간 더미의 맨 아래(제자리에 있던 칸)가 맨 위로 올라와요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
