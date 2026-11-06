"""ROOM 128 proof: the jeweller's chain puzzle. Each board is a pile of chain pieces (lengths in links). The jeweller
joins ALL pieces into one closed loop (necklace). Opening and closing one link counts as one. Every join needs one
open link; a fully opened piece gives all its links as joiners. So for a set S of pieces taken fully apart, the cost
is max(links in S, pieces left), and the answer is the minimum over every S (searched exhaustively). Digit = minimum
number of links to open. All 10^4 codes are compared; exactly one matches. The trap: 'one link per piece' (= the
number of pieces)."""
import itertools, json, os

BOARDS = {'A': [3, 3, 3, 3], 'B': [1, 5, 5, 5, 5, 5], 'C': [2, 2, 2, 2, 2, 2], 'D': [1, 1, 3, 4]}


def best(L):
    out = None
    for r in range(len(L)):
        for S in itertools.combinations(range(len(L)), r):
            c = max(sum(L[i] for i in S), len(L) - r)
            if out is None or c < out[0]: out = (c, list(S))
    return out


RES = {k: best(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(len(BOARDS[k])) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) == best(BOARDS[k])[0] for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap, RES)
assert sols == ['3542'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'take_apart': {k: v[1] for k, v in RES.items()},
               'trap_one_per_piece': trap,
               'why': '짧은 조각 하나를 통째로 풀면 그 고리들로 나머지를 이을 수 있어요. 조각 수만큼 열 필요가 없어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
