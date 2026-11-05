"""ROOM 065 proof: pairs of pendulums hung from one beam. A small swing's period is T = 2*pi*sqrt(L/g): it depends on the
string length only, not on the bob's weight. While the left pendulum (length a) makes n full swings, the right one
(length b) makes n * sqrt(a/b). Period is computed directly and the right count is checked to be a whole number.
All 10^4 codes are compared, exactly one matches. Assuming both swing the same number of times gives the trap."""
import itertools, json, math, os
G = 9.81
BOARDS = {'A': (1, 8, 4), 'B': (4, 3, 1), 'C': (1, 9, 9), 'D': (4, 4, 16)}   # left length (tiles), left swings, right length
U = 0.25   # metres per tile


def T(L): return 2 * math.pi * math.sqrt(L * U / G)


res = {}
for k, (a, n, b) in BOARDS.items():
    x = n * T(a) / T(b); assert abs(x - round(x)) < 1e-9, (k, x); res[k] = round(x)
code = ''.join(str(res[k]) for k in 'ABCD'); trap = ''.join(str(BOARDS[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, 'solutions', sols)
assert sols == ['4632'] and trap == '8394'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_left_len_left_swings_right_len': BOARDS, 'right_swings': res,
               'trap_same_count': trap,
               'why': '진자 주기는 줄 길이의 제곱근에 비례, 추 무게와 무관. 길이 4배 → 2배 느림, 9배 → 3배 느림. A 8÷2=4 · B 3×2=6 · C 9÷3=3 · D 4÷2=2'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
