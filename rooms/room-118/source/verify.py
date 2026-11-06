"""ROOM 118 proof: two hinged mirrors. Two flat mirrors stand on their edges, joined at a hinge, opening at angle T.
A small toy stands on the middle line between them. Reflections of reflections fill the circle around the hinge
with 360/T equal wedges; one wedge holds the real toy, every other wedge shows one image. So the number of toys you
see IN the mirrors is 360/T - 1 (for T dividing 360; the toy on the middle line keeps it exact for odd 360/T too).
Digit = that count. All 10^4 codes are compared; exactly one matches. The trap: 360/T (counting the real toy too)."""
import itertools, json, os

BOARDS = {'A': {'angle': 60}, 'B': {'angle': 90}, 'C': {'angle': 45}, 'D': {'angle': 72}}


def images(t): assert 360 % t == 0; return 360 // t - 1


code = ''.join(str(images(BOARDS[k]['angle'])) for k in 'ABCD'); trap = ''.join(str(360 // BOARDS[k]['angle']) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['5374'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'trap_count_real_too': trap,
               'why': '거울 사이 각도로 360을 나눈 수만큼 칸이 생기고, 그중 한 칸은 진짜 장난감이에요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
