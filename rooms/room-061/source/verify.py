"""ROOM 061 proof: four pairs of transparent films with squares on a 3x5 grid. The right film is turned over left-to-right
(mirror) and laid on the left film; the squares of both together show one digit of the 3x5 font.
For every board the overlay is compared with all ten font digits: exactly one matches. All 10^4 codes are then compared,
exactly one equals the overlay digits. Laying the right film on without turning it over gives a different digit (the trap)."""
import itertools, json, os
FONT = {0: '111101101101111', 1: '010110010010111', 2: '111001111100111', 3: '111001111001111', 4: '101101111001001',
        5: '111100111001111', 6: '111100111101111', 7: '111001001001001', 8: '111101111101111', 9: '111101111001111'}
bits = lambda s: frozenset(i for i, c in enumerate(s) if c == '1')
mirror = lambda S: frozenset((i // 3) * 3 + 2 - i % 3 for i in S)
INV = {bits(v): k for k, v in FONT.items()}
WANT = {'A': (6, 2), 'B': (8, 6), 'C': (2, 3), 'D': (9, 5)}   # (answer digit, trap digit)


def pick(d, t):
    """Deterministic split of digit d into left film L and right film R (as printed) so that L + mirror(R) = d,
    L + R = t, neither film alone (or turned over) is a digit, each film has 5..7 squares, as even as possible."""
    P = sorted(bits(FONT[d])); best = None
    for m in range(1 << len(P)):
        L = frozenset(P[i] for i in range(len(P)) if m >> i & 1); R = mirror(frozenset(P) - L)
        if not (5 <= len(L) <= 7 and 5 <= len(R) <= 7): continue
        if L in INV or R in INV or mirror(R) in INV or mirror(L) in INV: continue
        if INV.get(L | R) != t: continue
        key = (abs(len(L) - len(R)), sorted(L))
        if best is None or key < best[0]: best = (key, L, R)
    return sorted(best[1]), sorted(best[2])


FILMS = {k: pick(*WANT[k]) for k in 'ABCD'}


def overlay(k, flip=True):
    L, R = map(frozenset, FILMS[k]); return [d for d, v in FONT.items() if bits(v) == (L | (mirror(R) if flip else R))]


res = {k: overlay(k) for k in 'ABCD'}; tr = {k: overlay(k, False) for k in 'ABCD'}
assert all(len(v) == 1 for v in res.values()) and all(len(v) == 1 for v in tr.values())
code = ''.join(str(res[k][0]) for k in 'ABCD'); trap = ''.join(str(tr[k][0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, 'films', FILMS, 'solutions', sols)
assert sols == ['6829'] and trap == '2635'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'films_left_right_cells_row_major_3x5': FILMS,
               'trap_no_flip': trap,
               'why': '오른쪽 필름을 좌우로 뒤집어 겹쳐야 숫자가 된다. 그대로 겹치면 2635가 보이는 함정. A 6 · B 8 · C 2 · D 9'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
