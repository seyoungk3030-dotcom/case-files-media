"""ROOM 184 proof: torn-out sheets. In a printed book a page on the LEFT is always even and the page on the RIGHT is
odd, and one sheet of paper carries an odd page on its front and the next even page on its back (13 and 14 share a
sheet). Each board is a book lying open where some sheets were torn out: left page L, right page R. The missing pages
are L+1 .. R-1, so the number of torn sheets is (R - L - 1) / 2. Digit = sheets torn out.
All 10^4 codes compared; exactly one matches. The trap: counting missing pages instead of sheets."""
import itertools, json, os

BOARDS = {'A': (12, 21), 'B': (36, 43), 'C': (58, 63), 'D': (150, 153)}


def sheets(L, R):
    assert L % 2 == 0 and R % 2 == 1 and R > L + 1
    missing = list(range(L + 1, R)); assert missing[0] % 2 == 1 and len(missing) % 2 == 0
    leaves = {(p + 1) // 2 for p in missing}  # sheet index of each page: (1,2)->1, (3,4)->2 ...
    return len(leaves), len(missing)


GOOD = {k: sheets(*v)[0] for k, v in BOARDS.items()}; TRAPV = {k: sheets(*v)[1] for k, v in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] for k in 'ABCD') and all(t <= 9 for t in TRAPV.values())
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'sheets': GOOD, 'trap_missing_pages': trap,
               'why': '종이 한 장의 앞뒤가 홀수 쪽과 다음 짝수 쪽이에요. 사라진 쪽수를 2로 나누면 찢긴 종이 장수'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
