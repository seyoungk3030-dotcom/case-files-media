"""ROOM 162 proof: a pile of logs seen from the end. Row 0 lies on the ground; a log in row r at slot i rests on the two
logs below it, (r-1, i) and (r-1, i+1). The marked log is pulled out from the front. Any log that has lost one of its
two supports rolls off, and so does everything that rested on that log, and so on. Digit = how many logs roll off
(the pulled log not counted). All 10^4 codes compared; exactly one matches. The trap: only the logs touching the pulled
log from above."""
import itertools, json, os
# rows from the ground up: list of slots present; PULL = (row, slot)
BOARDS = {'A': {'rows': [[0, 1, 2, 3, 4], [0, 1, 2, 3], [1, 2], [1]], 'pull': (0, 2)},
          'B': {'rows': [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4], [0, 1, 2, 3], [1, 2], [1]], 'pull': (1, 1)},
          'C': {'rows': [[0, 1, 2, 3, 4], [0, 1, 2, 3], [0, 1, 2], [0, 1], [0]], 'pull': (0, 4)},
          'D': {'rows': [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4], [1, 2, 3], [1, 2], [1]], 'pull': (0, 1)}}


def fall(b):
    have = {(r, i) for r, row in enumerate(b['rows']) for i in row}
    for r, i in have:
        assert r == 0 or ((r - 1, i) in have and (r - 1, i + 1) in have), (r, i)
    gone = {b['pull']}; ch = True
    while ch:
        ch = False
        for r, i in sorted(have - gone):
            if r and ((r - 1, i) in gone or (r - 1, i + 1) in gone): gone.add((r, i)); ch = True
    pr, pi = b['pull']; direct = {(pr + 1, pi - 1), (pr + 1, pi)} & have
    return sorted(gone - {b['pull']}), len(direct)


RES = {k: fall(b) for k, b in BOARDS.items()}
code = ''.join(str(len(RES[k][0])) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'falling': {k: r[0] for k, r in RES.items()},
               'trap_direct_only': trap, 'why': '받침 하나만 빠져도 굴러떨어져요. 떨어진 통나무 위에 있던 통나무도 줄줄이 떨어져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
