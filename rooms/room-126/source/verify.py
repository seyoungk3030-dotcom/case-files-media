"""ROOM 126 proof: a nut on a threaded rod beside a ruler marked 0-9. The thread ridges are packed q to one ruler
step, so one full turn of the nut moves it 1/q of a step (one thread). Each board shows the start mark, the number of
turns and the direction (down or up). Digit = the ruler mark the nut's pointer ends on = start -/+ turns/q.
All 10^4 codes are compared; exactly one matches. The trap: 'one turn = one ruler step' (start -/+ turns)."""
import itertools, json, os

BOARDS = {'A': {'start': 9, 'q': 2, 'turns': 6, 'dir': -1},
          'B': {'start': 7, 'q': 3, 'turns': 6, 'dir': -1},
          'C': {'start': 1, 'q': 2, 'turns': 6, 'dir': 1},
          'D': {'start': 9, 'q': 3, 'turns': 3, 'dir': -1}}


def solve(b):
    assert b['turns'] % b['q'] == 0 and b['q'] > 1
    end = b['start'] + b['dir'] * b['turns'] // b['q']; trap = b['start'] + b['dir'] * b['turns']
    assert 0 <= end <= 9 and 0 <= trap <= 9
    return end, trap


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4))
        if all(int(c[i]) == BOARDS[k]['start'] + BOARDS[k]['dir'] * BOARDS[k]['turns'] / BOARDS[k]['q'] for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap)
assert sols == ['6548'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'trap_one_turn_one_step': trap,
               'why': '너트는 한 바퀴에 나사산 한 칸만 움직여요. 눈금 한 칸에 나사산이 2개면 두 바퀴에 한 칸이에요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
