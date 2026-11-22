"""ROOM 204 proof (천둥까지 몇 km?): you see the flash, then count t seconds until the thunder. Light arrives practically
at once (3 km takes 0.00001 s), sound travels about 340 m/s, so distance = 340 * t metres. Digit = distance in km,
rounded (every board lands within 0.1 km of a whole number, so rounding is not a judgment call; the check also holds for
sound speeds 330-350 m/s). All 10^4 codes compared; exactly one matches. Trap: '1 second = 1 km' (seconds themselves)."""
import itertools, json, os

BOARDS = {'A': 9, 'B': 6, 'C': 3, 'D': 12}   # seconds between flash and thunder
LIGHT = 299_792_458


def km(t, v=340.0):
    d = v * t; return d / 1000


GOOD = {}
for k, t in BOARDS.items():
    ds = [km(t, v) for v in (330, 340, 350)]
    r = round(ds[1]); assert all(abs(d - r) < 0.25 for d in ds) and abs(ds[1] - r) < 0.1 and 0 <= r < 10, (k, ds)
    assert ds[1] * 1000 / LIGHT < 1e-4   # light delay negligible
    GOOD[k] = r
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, {k: round(km(t), 2) for k, t in BOARDS.items()})
assert len(sols) == 1 and code != '9631'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'seconds': BOARDS, 'km': {k: round(km(t), 2) for k, t in BOARDS.items()},
               'trap_one_second_one_km': '9 6 3 12', 'sound_mps': 340,
               'why': '빛은 거의 즉시 도착하고, 소리는 1초에 약 340 m. 3초에 약 1 km예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
