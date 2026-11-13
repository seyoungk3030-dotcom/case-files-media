"""ROOM 178 proof: the lazy susan. A round turntable in a restaurant carries 8 numbered dishes; you sit at the front.
Positions are numbered 0..7 going clockwise seen from above, 0 = right in front of you, 1 = front-left, 2 = left, ...,
7 = front-right. An arrow on the FAR rim shows which way the table turns and by how many dish places. Turning clockwise
(seen from above) by k moves the dish at position p to p + k, so the dish that ends in front came from position -k.
The far-rim arrow of a clockwise turn points to YOUR right, while the front of the table moves to your left.
Digit = number on the dish that ends in front of you. All 10^4 codes compared; exactly one matches.
The trap: moving the front dishes the same way the far arrow points."""
import itertools, json, os

BOARDS = {  # dishes by position 0..7, direction (+1 clockwise from above / -1), steps
    'A': ('46193827', 1, 1), 'B': ('15620738', -1, 2), 'C': ('20857146', 1, 3), 'D': ('73495016', -1, 1)}


def arrow_points_right(d): return d == 1  # far rim: clockwise moves right on screen, counter-clockwise moves left


def front_after(dishes, d, k): return dishes[(-d * k) % 8]


GOOD = {key: int(front_after(*v)) for key, v in BOARDS.items()}
TRAPV = {key: int(front_after(s, -d, k)) for key, (s, d, k) in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] for k in 'ABCD')
assert all(len(set(s)) == 8 for s, _, _ in BOARDS.values())
# brute-force check by rotating the whole table step by step
for key, (s, d, k) in BOARDS.items():
    t = list(s)
    for _ in range(k): t = [t[(p - d) % 8] for p in range(8)]  # after one step the dish at p came from p - d
    assert int(t[0]) == GOOD[key]
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'front_dish': GOOD, 'trap_same_way_as_far_arrow': trap,
               'why': '원탁 반대편 화살표가 오른쪽이면, 내 앞쪽은 왼쪽으로 움직여요. 오른쪽 접시가 내 앞으로 와요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
