"""ROOM 206 proof (배에서 돌을 던지면?): a toy boat floats in a square tank (20 x 20 cm inside) carrying one object. The
object goes overboard. Floating, the boat+object displace their weight of water: an object on board displaces m/1 cm^3
(water 1 g/cm^3). Overboard, a sinking object displaces only its own volume V; a floating one still displaces m. Level
change = (displaced after - displaced before) / tank area. Digit = how many mm the water goes DOWN. Integer mm on every
board, checked exactly with fractions. All 10^4 codes compared; exactly one matches. Trap: 'a splash, so it rises'."""
import itertools, json, os
from fractions import Fraction as Fr

AREA = 400            # cm^2
# key: (name, volume cm^3, density g/cm^3)
BOARDS = {'A': ('돌', 80, Fr(5, 2)), 'B': ('나무토막', 40, Fr(3, 5)), 'C': ('쇠 너트', 40, Fr(8)), 'D': ('구리 추', 40, Fr(9))}
BOAT_G = 100


def drop_mm(V, rho):
    m = V * rho
    before = m                       # on board: displaces its weight
    after = V if rho > 1 else m      # overboard: sinks -> own volume, floats -> its weight
    d = Fr(before - after, AREA) * 10
    return d


GOOD = {}
for k, (nm, V, rho) in BOARDS.items():
    d = drop_mm(V, rho); assert d.denominator == 1 and 0 <= d < 10, (k, d); GOOD[k] = int(d)
    assert (BOAT_G + V * rho) / 112 < 5.5       # boat (14 x 8 cm, 6 cm tall) stays afloat with the load
code = ''.join(str(GOOD[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, {k: (BOARDS[k][0], float(BOARDS[k][1] * BOARDS[k][2]), 'g') for k in BOARDS})
assert len(sols) == 1
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'area_cm2': AREA,
               'boards': {k: {'name': n, 'volume_cm3': V, 'density': str(r), 'mass_g': str(V * r)} for k, (n, V, r) in BOARDS.items()},
               'drop_mm': GOOD, 'trap': '물이 튀니 올라간다 / 그대로다',
               'why': '배 위에서는 무게만큼(무거울수록 많이) 물을 밀어내고, 가라앉으면 자기 부피만큼만 밀어내요. 그래서 물이 내려가요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
