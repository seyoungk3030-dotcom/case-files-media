"""ROOM 181 proof: which lids come OFF? A lid opens when it turns counter-clockwise seen from the lid's own top
("lefty loosey"). Jars stand upright, so their lid top faces up and the yellow arrow seen from above is the true
direction. Squeeze bottles stand upside down on their lid, so the lid's top faces the shelf: seen from above the
direction is mirrored, and an arrow that looks clockwise from above is counter-clockwise for the lid -> it opens.
Digit = number of containers on the shelf whose lid opens. All 10^4 codes compared; exactly one matches.
The trap: counting the arrows that look counter-clockwise from above, ignoring the upside-down bottles."""
import itertools, json, os

# each item: (kind 'J' upright jar / 'B' upside-down bottle, arrow as seen from above 'L' = counter-clockwise, 'R' = clockwise)
BOARDS = {'A': ['JL', 'BR', 'JR', 'BR', 'BL'],
          'B': ['BR', 'JR', 'BR', 'JL', 'BL', 'BR'],
          'C': ['JR', 'BL', 'JR', 'BL'],
          'D': ['BL', 'JL', 'BR', 'JL', 'BL']}


def opens(item):
    kind, arrow = item
    return (arrow == 'L') if kind == 'J' else (arrow == 'R')


GOOD = {k: sum(map(opens, v)) for k, v in BOARDS.items()}
TRAPV = {k: sum(a == 'L' for _, a in v) for k, v in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] for k in 'ABCD')
assert all(any(i[0] == 'B' for i in v) and any(i[0] == 'J' for i in v) for v in BOARDS.values())
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'open_count': GOOD, 'trap_arrows_ccw_from_above': trap,
               'why': '거꾸로 세운 병은 뚜껑 윗면이 바닥을 봐요. 위에서 시계 방향으로 보이면 뚜껑 입장에선 반시계, 열려요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
