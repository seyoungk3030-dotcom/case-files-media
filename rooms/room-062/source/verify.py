"""ROOM 062 proof: four locks, three keys each. A lock opens only when every pin top sits exactly on the yellow
shear line: pin length + tooth height under that pin = 5 steps, for all five pins.
Every key is checked against its lock; on each board exactly one key opens it. All 10^4 codes are compared with
the opening keys' numbers, exactly one matches. Picking the key whose teeth copy the pin lengths gives the trap."""
import itertools, json, os
H = 5
PINS = {'A': [1, 3, 2, 4, 2], 'B': [3, 1, 4, 2, 3], 'C': [2, 4, 1, 3, 1], 'D': [4, 2, 3, 1, 4]}
NUM = {'A': (7, 3, 5), 'B': (2, 8, 4), 'C': (9, 1, 6), 'D': (4, 6, 2)}   # (opens, copies pins, one tooth off)
ORDER = {'A': (1, 0, 2), 'B': (2, 1, 0), 'C': (0, 2, 1), 'D': (1, 2, 0)}  # which of the three is drawn top, middle, bottom
OFF = {'A': (3, +1), 'B': (0, +1), 'C': (4, -1), 'D': (2, -1)}         # tooth index and change of the decoy


def keys(k):
    p = PINS[k]; good = [H - x for x in p]; trap = list(p); dec = list(good); i, d = OFF[k]; dec[i] += d
    assert all(1 <= t <= 4 for t in good + trap + dec)
    ks = [(NUM[k][0], good), (NUM[k][1], trap), (NUM[k][2], dec)]
    return [ks[j] for j in ORDER[k]]


def opens(k, teeth): return all(p + t == H for p, t in zip(PINS[k], teeth))


res = {k: [n for n, t in keys(k) if opens(k, t)] for k in 'ABCD'}
assert all(len(v) == 1 for v in res.values()), res
code = ''.join(str(res[k][0]) for k in 'ABCD')
trap = ''.join(str(n) for k in 'ABCD' for n, t in keys(k) if t == PINS[k])
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, 'solutions', sols)
assert sols == ['7294'] and trap == '3816'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'pins': PINS, 'keys': {k: keys(k) for k in 'ABCD'},
               'trap_teeth_copy_pins': trap,
               'why': '핀 길이 + 그 밑 톱니 높이 = 5칸이어야 모든 핀이 노란 선에 맞는다. 긴 핀 밑엔 낮은 톱니. A 7 · B 2 · C 9 · D 4'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
