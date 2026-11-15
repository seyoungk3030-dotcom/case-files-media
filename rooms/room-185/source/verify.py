"""ROOM 185 proof: elevator buttons that lie. Many buildings have no button 4 (and some no 13), and there is no
floor 0 between B1 and 1. The building's real floors are exactly the buttons on the panel, stacked in order, so a
trip from the red-ringed button to the lit button climbs as many real floors as there are buttons after the start
up to and including the destination. Digit = real floors climbed. All 10^4 codes compared; exactly one matches.
The trap: subtracting the button numbers (B1 counted as -1)."""
import itertools, json, os

def lab(v): return f'B{-v}' if v < 0 else str(v)

BOARDS = {  # buttons in the building (bottom to top) as numbers (B1 = -1), start, destination
    'A': ([-1, 1, 2, 3, 5, 6, 7, 8, 9], 2, 7),
    'B': ([-2, -1, 1, 2, 3, 5, 6, 7], -1, 6),
    'C': ([1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16], 12, 15),
    'D': ([1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16], 9, 16)}


def climbed(btn, s, d): return btn.index(d) - btn.index(s)


GOOD = {k: climbed(*v) for k, v in BOARDS.items()}; TRAPV = {k: v[2] - v[1] for k, v in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] for k in 'ABCD') and all(0 < g < 10 for g in GOOD.values())
assert all(0 not in b and b == sorted(b) for b, _, _ in BOARDS.values())
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': {k: ([lab(x) for x in b], lab(s), lab(d)) for k, (b, s, d) in BOARDS.items()},
               'floors_climbed': GOOD, 'trap_button_difference': trap,
               'why': '4층·13층 버튼이 없는 건물은 그 층이 없어요. 0층도 없어요. 지나가는 버튼 수가 실제 층수예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
