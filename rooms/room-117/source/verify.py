"""ROOM 117 proof: melting ice. Each glass has marks; one mark = 100 cm^3 of water (equal glass widths). Ice is
shown with its weight. 1 g of ice melts into 1 cm^3 of water. After all the ice melts, where is the water level?
  floating ice: it already pushes away exactly its own weight of water, so melting changes nothing.
  ice on the rack above the glass (not touching the water): its melt water is all new -> + m / 100 marks.
  floating ice with a stone frozen inside: while floating it pushes away (ice + stone) weight of water; after
  melting the stone sinks and takes only its own volume -> level falls by (stone g - stone cm^3) / 100.
Digit = the final mark. All 10^4 codes are compared; exactly one matches. The trap: 'melting ice always raises
the water by its weight'."""
import itertools, json, os

BOARDS = {'A': {'level': 5, 'items': [{'kind': 'float', 'ice': 400}]},
          'B': {'level': 4, 'items': [{'kind': 'rack', 'ice': 300}]},
          'C': {'level': 6, 'items': [{'kind': 'stone', 'ice': 200, 'stone_g': 300, 'stone_cc': 100}]},
          'D': {'level': 2, 'items': [{'kind': 'float', 'ice': 200}, {'kind': 'rack', 'ice': 100}]}}


def final(b):
    lv = b['level'] * 100
    for it in b['items']:
        if it['kind'] == 'rack': lv += it['ice']
        if it['kind'] == 'stone': lv -= it['stone_g'] - it['stone_cc']
    return lv / 100


def naive(b): return (b['level'] * 100 + sum(it['ice'] for it in b['items'])) / 100


FIN = {k: final(b) for k, b in BOARDS.items()}
assert all(v == int(v) and 0 <= v <= 9 for v in FIN.values())
code = ''.join(str(int(FIN[k])) for k in 'ABCD'); trap = ''.join(str(int(naive(BOARDS[k]))) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['5743'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'final': FIN, 'trap_always_rises': trap,
               'why': '떠 있는 얼음은 이미 자기 무게만큼 물을 밀어내고 있어서 녹아도 수위가 그대로예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
