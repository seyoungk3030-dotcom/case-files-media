"""ROOM 131 proof: polarising sheets (the three-polariser paradox). Each board is a light box with three windows; each
window is covered by a stack of polarising sheets whose axes are drawn as lines (0, 45, 90 or 135 degrees), listed
in stack order. Light gets through a stack unless two NEIGHBOURING sheets are at right angles (Malus: cos^2 90 = 0;
45 degrees passes half). A digit is printed on the lamp behind each window; only the lit window's digit can be read.
Exactly one window per board is lit. Digit = that window's digit. All 10^4 codes are compared; exactly one matches.
The trap: 'fewer sheets let more light through' (the digit of the window with the fewest sheets)."""
import itertools, json, os

BOARDS = {'A': [{'d': 3, 's': [0, 90]}, {'d': 7, 's': [0, 45, 90]}, {'d': 1, 's': [0, 90, 45]}],
          'B': [{'d': 5, 's': [45, 135, 90]}, {'d': 8, 's': [90, 0]}, {'d': 2, 's': [90, 45, 0, 45]}],
          'C': [{'d': 9, 's': [0, 45, 90, 135]}, {'d': 4, 's': [135, 45]}, {'d': 6, 's': [0, 45, 135]}],
          'D': [{'d': 1, 's': [45, 90, 0]}, {'d': 3, 's': [45, 135]}, {'d': 6, 's': [0, 135, 90]}]}


def lit(s): return all((a - b) % 180 != 90 for a, b in zip(s, s[1:]))


def solve(b):
    on = [w['d'] for w in b if lit(w['s'])]; assert len(on) == 1
    few = min(b, key=lambda w: len(w['s'])); assert sum(len(w['s']) == len(few['s']) for w in b) == 1
    return on[0], few['d']


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4))
        if all(int(c[i]) in [w['d'] for w in BOARDS[k] if lit(w['s'])] for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap)
assert sols == ['7296'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'trap_fewest_sheets': trap,
               'why': '편광판은 서로 직각인 판이 붙어 있으면 빛을 막아요. 사이에 45도 판을 끼우면 오히려 빛이 지나가요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
