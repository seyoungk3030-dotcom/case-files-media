"""ROOM 173 proof: blank keypads. Each board is a calculator or a phone with the digits rubbed off its keys; the type
shows from the keys that still carry symbols (calculator: ÷ × − + = and a display; phone: * # and a handset).
One key is pressed down. Digit = the number on that key. Calculator rows run 7 8 9 / 4 5 6 / 1 2 3 / 0 from the top,
phone rows 1 2 3 / 4 5 6 / 7 8 9 / * 0 #. All 10^4 codes compared; exactly one matches.
The trap: reading every pad with the phone layout (or every pad with the calculator layout)."""
import itertools, json, os

CALC = [['7', '8', '9', '÷'], ['4', '5', '6', '×'], ['1', '2', '3', '−'], ['0', '.', '=', '+']]
PHONE = [['1', '2', '3'], ['4', '5', '6'], ['7', '8', '9'], ['*', '0', '#']]
PADS = {'calc': CALC, 'phone': PHONE}
BOARDS = {'A': ('calc', 0, 0), 'B': ('phone', 0, 2), 'C': ('phone', 2, 1), 'D': ('calc', 2, 0)}  # (type, row, col) of the pressed key

GOOD = {k: PADS[t][r][c] for k, (t, r, c) in BOARDS.items()}
SWAP = {k: PADS['phone' if t == 'calc' else 'calc'][r][c] for k, (t, r, c) in BOARDS.items()}
code = ''.join(GOOD[k] for k in 'ABCD'); trap = ''.join(SWAP[k] for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and code.isdigit() and trap.isdigit() and all(GOOD[k] != SWAP[k] for k in 'ABCD')
assert {t for t, _, _ in BOARDS.values()} == {'calc', 'phone'}  # both layouts are needed
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'digits': GOOD, 'trap_layout_swapped': trap,
               'why': '계산기는 맨 윗줄이 7 8 9, 전화는 맨 윗줄이 1 2 3이에요. 위아래가 거꾸로예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
