"""ROOM 137 proof: a bimetal strip (brass bonded to iron) stands clamped at the bottom between two contacts; each
contact lights its own numbered lamp. Brass expands and shrinks more than iron for the same temperature change. Heated
(candle), the brass side gets longer, so the strip curls with brass on the OUTSIDE, i.e. it bends toward the iron
side; cooled (ice), the brass side gets shorter and the strip bends toward the brass side. Digit = the number of the
lamp on the side it bends to. All 10^4 codes are compared; exactly one matches. The trap: 'it bends toward the metal
that expands more' when heated (and the reverse when cooled), i.e. the other lamp."""
import itertools, json, os

BOARDS = {'A': {'brass': 'L', 'temp': 'hot', 'lamps': {'L': 2, 'R': 6}},
          'B': {'brass': 'R', 'temp': 'cold', 'lamps': {'L': 7, 'R': 4}},
          'C': {'brass': 'R', 'temp': 'hot', 'lamps': {'L': 9, 'R': 3}},
          'D': {'brass': 'L', 'temp': 'cold', 'lamps': {'L': 1, 'R': 8}}}


def side(b):
    other = 'R' if b['brass'] == 'L' else 'L'
    return other if b['temp'] == 'hot' else b['brass']


def solve(b):
    s = side(b); o = 'R' if s == 'L' else 'L'; return b['lamps'][s], b['lamps'][o], s


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) == solve(BOARDS[k])[0] for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap)
assert sols == [code] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'bends_to': {k: v[2] for k, v in RES.items()}, 'trap_other_lamp': trap,
               'why': '데우면 놋쇠 쪽이 더 길어져서 바깥으로 둥글게, 즉 철 쪽으로 휘어요. 식히면 반대예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
