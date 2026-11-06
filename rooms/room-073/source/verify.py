"""ROOM 073 proof: parking-space numbers are painted for drivers coming from the far side, so from our side every number
is upside down and the row runs backwards. Turning a painted number 180 degrees maps 0->0, 1->1, 6->9, 8->8, 9->6 (and
reverses the digit order); the spaces are numbered consecutively for the driver. Every visible space is checked to turn
into the consecutive sequence, so the space under the car has exactly one possible number. A's two digits and B's two
digits are the code. Reading the painted digits as they are gives no consecutive sequence at all (the trap)."""
import itertools, json, os
ROT = {'0': '0', '1': '1', '6': '9', '8': '8', '9': '6'}
REAL = {'A': [66, 67, 68, 69], 'B': [6, 7, 8, 9, 10, 11]}
HIDDEN = {'A': 67, 'B': 7}


def paint(n):   # how the number looks from our side (rotated 180 degrees)
    s = f'{n:02d}'; return ''.join(ROT[c] for c in reversed(s))


def unpaint(p): return int(''.join(ROT[c] for c in reversed(p)))


SEEN = {k: [None if n == HIDDEN[k] else paint(n) for n in reversed(REAL[k])] for k in 'AB'}   # left→right from our side
for k in 'AB':
    vis = [(i, p) for i, p in enumerate(SEEN[k]) if p]
    n = len(SEEN[k]); real_lr = [unpaint(p) for _, p in vis]
    # from the driver the order is reversed: position i from our left is position n-1-i from theirs
    cands = [s for s in range(0, 100 - n) if all(unpaint(p) == s + (n - 1 - i) for i, p in vis)]
    assert len(cands) == 1, (k, cands); hid = cands[0] + (n - 1 - SEEN[k].index(None)); assert hid == HIDDEN[k]
    raw = [int(p) for _, p in vis]; assert any(b - a != raw[1] - raw[0] for a, b in zip(raw, raw[1:])) or raw[1] - raw[0] not in (1, -1)
code = f'{HIDDEN["A"]:02d}{HIDDEN["B"]:02d}'
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'seen', SEEN, 'solutions', sols)
assert sols == ['6707']
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'seen_from_our_side': SEEN, 'real_numbers_for_driver': REAL,
               'why': '번호는 반대편에서 들어오는 운전자 쪽으로 칠해져 있어서 우리 쪽에선 거꾸로 보임. 화면을 뒤집어 읽으면 A 66·[67]·68·69, B 06·[07]·08·09·10·11'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
