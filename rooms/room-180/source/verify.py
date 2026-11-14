"""ROOM 180 proof: which note is the pressed piano key? Each board shows 10 white keys of a piano that does NOT start
at 도(C). Black keys sit after 도 레 / 파 솔 라 (groups of 2 and 3); 도 is the white key just left of a 2-black group.
Digit = solfege number of the pressed (glowing) white key: 도1 레2 미3 파4 솔5 라6 시7.
Checks: the black-key pattern in view fixes the start note uniquely, a whole 2-group and 3-group are visible,
all 10^4 codes compared and exactly one matches. The trap: calling the leftmost key 도."""
import itertools, json, os

N = 10
BLACK_AFTER = {0, 1, 3, 4, 5}  # 도 레 파 솔 라 have a black key on their right
BOARDS = {'A': (2, 3), 'B': (5, 4), 'C': (1, 5), 'D': (6, 2)}  # start note index (도=0), pressed white key from the left


def pattern(start): return tuple((start + i) % 7 in BLACK_AFTER for i in range(N - 1))


def groups(start):  # black groups fully inside the view (bounded by a gap on both sides)
    p = pattern(start); out, run = [], 0; started = False
    for i, b in enumerate(p):
        if b: run += 1
        else:
            if run and started: out.append(run)
            run = 0; started = True
    return out


GOOD = {k: (s + i) % 7 + 1 for k, (s, i) in BOARDS.items()}
TRAPV = {k: i % 7 + 1 for k, (s, i) in BOARDS.items()}
for k, (s, i) in BOARDS.items():
    assert s != 0 and [t for t in range(7) if pattern(t) == pattern(s)] == [s], k
    assert 2 in groups(s) and 3 in groups(s), (k, groups(s))
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] for k in 'ABCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'note': GOOD, 'trap_leftmost_is_do': trap,
               'why': '도는 검은 건반 2개 묶음 바로 왼쪽 흰 건반이에요. 맨 왼쪽 건반이 도가 아니에요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
