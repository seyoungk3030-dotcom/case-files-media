"""ROOM 048 proof: a wall clock is seen only in a mirror (numbers reversed). Code = the real time HHMM (12-hour, 4
digits). Every one of the 720 times is mirrored and compared with the hand angles shown; exactly one real time fits.
The trap reads the mirror as it is."""
import json, os
REAL = (10, 37)   # the real time; the picture shows its mirror image


def angles(h, m):            # clockwise from 12, degrees
    return ((h % 12) * 30 + m * 0.5) % 360, m * 6 % 360


def mirror(a): return (-a) % 360


SHOWN = tuple(mirror(a) for a in angles(*REAL))           # hand angles drawn in the mirror
fits = [(h, m) for h in range(1, 13) for m in range(60)
        if all(abs((mirror(a) - s + 180) % 360 - 180) < 1e-9 for a, s in zip(angles(h, m), SHOWN))]
as_is = [(h, m) for h in range(1, 13) for m in range(60) if all(abs((a - s + 180) % 360 - 180) < 1e-9 for a, s in zip(angles(h, m), SHOWN))]
code = f'{fits[0][0]:02d}{fits[0][1]:02d}'; trap = f'{as_is[0][0]:02d}{as_is[0][1]:02d}'
print(SHOWN, fits, as_is, code, trap)
assert len(fits) == 1 and len(as_is) == 1 and code == '1037' and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'trap_read_as_is': trap, 'shown_angles': SHOWN,
               'why': '거울 속 시침·분침을 좌우로 뒤집으면 진짜 시각. 12시 기준으로 보면 거울 속 1:23 = 진짜 10:37 (12:00 - 1:23).'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
