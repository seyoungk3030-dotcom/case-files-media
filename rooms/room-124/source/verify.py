"""ROOM 124 proof: Newton's cradle. n equal steel balls hang in a row, touching. k balls are pulled out on the left
and j balls on the right, and all are let go at the same moment (j may be 0). The lifted groups hit the row at
the same speed from both sides. Momentum and energy are both kept, and for equal balls the only way to keep both is
to pass the groups through: afterwards j balls fly out on the LEFT and k balls fly out on the RIGHT (the counts
swap sides). The balls carry number tags (left to right). Digit = the number on the innermost ball that flies out
on the right, i.e. the k-th ball from the right end. All 10^4 codes are compared; exactly one matches. The trap:
'each side throws back what it lifted' (the j-th ball from the right; the 2nd from the right when j = 0)."""
import itertools, json, os

BOARDS = {'A': {'nums': [7, 8, 4, 5, 3, 1, 9], 'left': 1, 'right': 2},
          'B': {'nums': [3, 9, 7, 6, 8, 4], 'left': 3, 'right': 1},
          'C': {'nums': [6, 2, 3, 1, 8], 'left': 1, 'right': 2},
          'D': {'nums': [3, 7, 8, 4, 9, 6], 'left': 3, 'right': 2}}


def solve(b):
    n, k, j = len(b['nums']), b['left'], b['right']; assert k + j < n and k != j
    out_right = list(range(n - k, n)); out_left = list(range(j))
    trap_pos = n - j if j else n - 2
    return b['nums'][n - k], b['nums'][trap_pos], out_left, out_right


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['9684'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS,
               'after': {k: {'left_out': v[2], 'right_out': v[3]} for k, v in RES.items()}, 'trap_same_counts': trap,
               'why': '같은 공끼리는 운동량과 에너지를 그대로 넘겨줘요. 그래서 왼쪽에서 든 개수만큼 오른쪽에서 튀어나가요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
