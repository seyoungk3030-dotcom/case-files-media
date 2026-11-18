"""ROOM 192 proof: cut a sheet of paper (0.1 mm thick) in half and lay one half on the other, then cut that pile in half
and stack again, and so on. After n cuts the pile has 2^n sheets, 0.1 * 2^n mm tall: it doubles every time instead of
growing by one sheet. Digit = the fewest cuts that make the pile taller than the object (strictly). Every object sits
well away from a power-of-two height (no ties). All 10^4 codes compared; exactly one matches. The trap: adding one
sheet per cut (that would take 50 to 400 cuts)."""
import itertools, json, os

BOARDS = {'A': ('각설탕', 16), 'B': ('콩', 8), 'C': ('탁구공', 40), 'D': ('알약', 5)}  # object, height mm (pill lying flat)
SHEET = 0.1


def cuts(h):
    n = 0
    while SHEET * 2 ** n <= h: n += 1
    assert SHEET * 2 ** n > h * 1.05 and SHEET * 2 ** (n - 1) < h; return n


GOOD = {k: cuts(v[1]) for k, v in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
TRAPV = {k: int(v[1] / SHEET) for k, v in BOARDS.items()}
print('answer', code, 'trap', TRAPV)
assert len(sols) == 1 and all(1 <= g <= 9 for g in GOOD.values())
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_object_mm': BOARDS, 'cuts': GOOD,
               'pile_mm': {k: round(SHEET * 2 ** GOOD[k], 1) for k in 'ABCD'}, 'trap_one_sheet_per_cut': TRAPV,
               'why': '자르고 겹칠 때마다 장수가 두 배: 1, 2, 4, 8, 16 ... 10번이면 1,024장(10cm)'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
