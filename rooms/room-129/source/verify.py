"""ROOM 129 proof: a spirit level lies on a shelf whose two ends rest on stacks of equal blocks. The vial is marked
1-9 from left to right, 5 in the middle. The air bubble is lighter than the liquid, so it rises to the HIGHER end:
each block of height difference moves it one mark (the rule card says so). Digit = the mark under the bubble =
5 + (right blocks - left blocks). All 10^4 codes are compared; exactly one matches. The trap: 'the bubble rolls down
like a marble' (5 - difference)."""
import itertools, json, os

BOARDS = {'A': {'left': 1, 'right': 4}, 'B': {'left': 3, 'right': 1}, 'C': {'left': 0, 'right': 1}, 'D': {'left': 3, 'right': 0}}


def mark(b, s=1): return 5 + s * (b['right'] - b['left'])


code = ''.join(str(mark(BOARDS[k])) for k in 'ABCD'); trap = ''.join(str(mark(BOARDS[k], -1)) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) == mark(BOARDS[k]) for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap)
assert sols == ['8362'] and trap != code and all(1 <= mark(b) <= 9 for b in BOARDS.values())
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'trap_rolls_down': trap,
               'why': '거품은 물보다 가벼워서 높은 쪽으로 올라가요. 구슬과 반대로 움직여요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
