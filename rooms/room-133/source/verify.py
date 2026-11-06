"""ROOM 133 proof: pancake flipping. Each board is a stack of six numbered pancakes (listed top to bottom) and a list
of spatula moves: 'k' means slide the spatula under the k-th pancake from the top and flip everything above it over
in one go, which reverses the order of the top k. Digit = the number on the top pancake after all moves. All 10^4
codes are compared; exactly one matches. The trap: 'the pancake under the spatula jumps to the top and the rest stay
in order' (move the k-th to the top)."""
import itertools, json, os

BOARDS = {'A': {'stack': [4, 7, 1, 9, 2, 6], 'moves': [4, 3, 2]},
          'B': {'stack': [3, 8, 5, 0, 6, 1], 'moves': [5, 3]},
          'C': {'stack': [6, 2, 9, 4, 8, 3], 'moves': [3, 6, 4]},
          'D': {'stack': [1, 5, 3, 7, 4, 0], 'moves': [6, 2, 5]}}


def flip(s, k): return s[:k][::-1] + s[k:]


def jump(s, k): return [s[k - 1]] + s[:k - 1] + s[k:]


def run(b, f):
    s = list(b['stack'])
    for k in b['moves']: s = f(s, k)
    return s


RES = {k: run(b, flip) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(run(BOARDS[k], jump)[0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) == run(BOARDS[k], flip)[0] for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap, RES)
assert sols == [code] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'final_stacks': RES, 'trap_jump_to_top': trap,
               'why': '뒤집개로 뒤집으면 위에 있던 묶음의 순서가 통째로 거꾸로 돼요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
