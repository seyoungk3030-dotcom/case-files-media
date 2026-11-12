"""ROOM 175 proof: reading a ruler. Each board is one object lying along a ruler with 1 cm ticks. Positions are in cm
measured from the ruler's physical left end. Each ruler is described by where its "0" mark would sit (zero_at) and the
direction its numbers run (+1 left-to-right, -1 reversed); the object spans [x0, x1]. Digit = true length x1 - x0.
All 10^4 codes compared; exactly one matches. The trap: reading the number under the object's right end."""
import itertools, json, os

# name: (ruler length cm, first printed number at the left, offset of that mark from the left end, direction, object x0, x1)
BOARDS = {
    'A': dict(obj='pencil', length=13, first=0, margin=1, dir=1, x0=3, x1=10),    # object starts at mark 2, not 0
    'B': dict(obj='crayon', length=8, first=4, margin=0, dir=1, x0=0, x1=6),      # broken ruler: starts at 4
    'C': dict(obj='eraser', length=7, first=0, margin=1, dir=1, x0=0, x1=4),      # pushed to the edge, 0 is 1 cm in
    'D': dict(obj='key', length=13, first=11, margin=1, dir=-1, x0=3, x1=11),     # ruler upside down: numbers fall
}


def mark_at(b, x):  # printed number at position x (cm from the left end)
    return b['first'] + b['dir'] * (x - b['margin'])


GOOD = {k: b['x1'] - b['x0'] for k, b in BOARDS.items()}
TRAPV = {k: mark_at(b, b['x1']) % 10 for k, b in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: (mark_at(b, b['x0']), mark_at(b, b['x1'])) for k, b in BOARDS.items()})
assert len(sols) == 1 and all(GOOD[k] < 10 and GOOD[k] != TRAPV[k] for k in 'ABCD')
assert all(0 <= b['x0'] < b['x1'] <= b['length'] for b in BOARDS.values())
assert GOOD == {k: abs(mark_at(b, b['x1']) - mark_at(b, b['x0'])) for k, b in BOARDS.items()}  # same as end mark - start mark
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'lengths_cm': GOOD, 'trap_end_mark': trap,
               'why': '길이는 끝 눈금이 아니라 (끝 눈금 - 시작 눈금). 부러진 자, 0 앞 여백, 거꾸로 놓인 자 모두 같아요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
