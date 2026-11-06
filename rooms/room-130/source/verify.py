"""ROOM 130 proof: a density column. A tall jar holds layers (bottom to top) of honey 1.4, dish soap 1.1, water 1.0 and
oil 0.9 (g/cm3), each a whole number of ruler marks thick (ruler 0-9, the top surface at 9). A small object with a
given density is dropped in from the top. It sinks through every layer lighter than itself and comes to rest on top
of the first layer (from the top) that is denser than itself; if even the top layer is denser it floats at 9.
Digit = the ruler mark where it rests. All 10^4 codes are compared; exactly one matches. The trap: 'compare only
with water' (heavier than water -> bottom 0, lighter -> top 9)."""
import itertools, json, os

LIQ = [('꿀', 1.4), ('세제', 1.1), ('물', 1.0), ('기름', 0.9)]
BOARDS = {'A': {'h': [2, 2, 3, 2], 'obj': ('포도', 1.05)}, 'B': {'h': [1, 3, 2, 3], 'obj': ('플라스틱 구슬', 0.95)},
          'C': {'h': [3, 1, 3, 2], 'obj': ('고무 공', 1.2)}, 'D': {'h': [1, 2, 4, 2], 'obj': ('나무 구슬', 0.97)}}


def rest(b):
    assert sum(b['h']) == 9; d = b['obj'][1]; top = 9
    for i in range(3, -1, -1):
        if LIQ[i][1] > d: return top
        top -= b['h'][i]
    return 0


RES = {k: rest(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k]) for k in 'ABCD'); trap = ''.join('0' if b['obj'][1] > 1 else '9' for b in (BOARDS[k] for k in 'ABCD'))
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) == rest(BOARDS[k]) for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap)
assert sols == ['4637'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'liquids': LIQ, 'boards': BOARDS, 'trap_water_only': trap,
               'why': '물체는 자기보다 가벼운 층은 뚫고 내려가고, 자기보다 무거운 층 위에서 멈춰요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
