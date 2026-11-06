"""ROOM 112 proof: the water-cup scale. A beaker of water sits on a kitchen scale that was set to 0 with the beaker on
it. Each board puts one object into the water in one way:
  hung  - held by a string from a stand that does not touch the scale; it goes in to the marked depth.
          The water pushes up on the object, so the object pushes down on the water just as hard:
          the scale gains the weight of the displaced water = 1 g per cm^3 under water.
  float - let go, it floats: the scale gains the object's whole weight (it is all carried by the water).
  sunk  - let go, it sinks and rests on the bottom: the scale gains the object's whole weight.
Each digit = the new reading / 100. All 10^4 codes are compared; exactly one matches. The trap: 'the scale always
gains the object's weight' (wrong for the hung ones)."""
import itertools, json, os

RHO = 1.0
# kind, mass g, volume cm^3, fraction under water for 'hung'
BOARDS = {'A': {'kind': 'hung', 'm': 700, 'V': 300, 'sub': 1.0, 'name': '돌'},
          'B': {'kind': 'float', 'm': 400, 'V': 900, 'name': '나무'},
          'C': {'kind': 'sunk', 'm': 800, 'V': 100, 'name': '쇠공'},
          'D': {'kind': 'hung', 'm': 600, 'V': 400, 'sub': 0.5, 'name': '돌'}}


def added(b):
    if b['kind'] == 'hung': return RHO * b['V'] * b['sub']
    if b['kind'] == 'float': assert b['m'] < RHO * b['V']; return b['m']
    assert b['m'] > RHO * b['V']; return b['m']


def sub_frac(b):
    return b['sub'] if b['kind'] == 'hung' else (b['m'] / (RHO * b['V']) if b['kind'] == 'float' else 1.0)


READ = {k: added(b) for k, b in BOARDS.items()}
assert all(v % 100 == 0 and 0 < v < 1000 for v in READ.values())
code = ''.join(str(int(READ[k] // 100)) for k in 'ABCD'); trap = ''.join(str(BOARDS[k]['m'] // 100) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['3482'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'reading_g': READ,
               'submerged_fraction': {k: sub_frac(b) for k, b in BOARDS.items()}, 'trap_always_weight': trap,
               'why': '매달린 물체는 밀어낸 물 무게만큼만, 놓아 버린 물체는 자기 무게 전부만큼 저울이 늘어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
