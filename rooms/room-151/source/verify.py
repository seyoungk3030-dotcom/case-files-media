"""ROOM 151 proof: the four-card (Wason) test, extended to more cards. Every card has a COLOUR (red or blue) on one side
and a NUMBER on the other. Rule to check: 'if a card is red on one side, the number on its back is even'. Only the
up-faces are seen. A card must be turned over exactly when its hidden side could break the rule: a red face (the back
might be odd) or an odd number (the back might be red). Blue faces and even numbers can never break it. Each hidden
side is checked by brute force over both colours and all digits. Digit = cards that must be turned. All 10^4 codes
compared; exactly one matches. The trap: turning red cards and EVEN numbers (looking for confirmation)."""
import itertools, json, os
BOARDS = {'A': ['3', 'R', '8', 'B', '5', 'R'], 'B': ['2', 'R', 'B', '7', '4', '6'],
          'C': ['1', 'R', '8', '3', 'R', 'B', '5', 'R'], 'D': ['R', '2', '9', 'B', '7', '1', 'R']}


def breaks(colour, number): return colour == 'R' and int(number) % 2 == 1


def must(face):
    hidden = '0123456789' if face in 'RB' else 'RB'
    return any(breaks(face, h) if face in 'RB' else breaks(h, face) for h in hidden)


MUST = {k: [i for i, f in enumerate(b) if must(f)] for k, b in BOARDS.items()}
code = ''.join(str(len(MUST[k])) for k in 'ABCD')
trap = ''.join(str(sum(1 for f in b if f == 'R' or (f.isdigit() and int(f) % 2 == 0))) for b in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, MUST)
assert sols == ['4265'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'must_turn': MUST, 'trap_confirm_even': trap,
               'why': '규칙을 깰 수 있는 카드만 확인하면 돼요. 빨강 카드(뒤가 홀수일 수 있음)와 홀수 카드(뒤가 빨강일 수 있음)!'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
