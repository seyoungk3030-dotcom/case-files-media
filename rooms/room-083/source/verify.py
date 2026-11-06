"""ROOM 083 proof: blocks made of 1 cm cubes (side 1, 2 or 3 cm, volume 1, 8 or 27 cm^3) with their weight in grams.
Water weighs 1 g per cm^3, so a block floats when its weight is less than its volume in grams and sinks when it is more
(no block is exactly equal). Each digit is how many blocks float in that tank. All 10^4 codes compared; exactly one
matches. 'Light blocks float' (under 10 g, the trap) gives another code."""
import itertools, json, os
TANKS = {'A': [(3, 20), (1, 2), (2, 6), (2, 9), (3, 30)], 'B': [(1, 5), (2, 7), (3, 25), (2, 3), (3, 12)],
         'C': [(2, 12), (1, 3), (3, 40), (1, 4), (2, 10)], 'D': [(3, 26), (2, 5), (3, 15), (2, 4), (1, 0.5)]}
FLOAT = {k: sum(1 for s, g in v if g < s ** 3) for k, v in TANKS.items()}
assert all(g != s ** 3 for v in TANKS.values() for s, g in v)
code = ''.join(str(FLOAT[k]) for k in 'ABCD'); trap = ''.join(str(sum(1 for s, g in TANKS[k] if g < 10)) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == [code] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'tanks_side_cm_weight_g': TANKS, 'trap_light_floats': trap,
               'why': '물 1 cm³ = 1 g. 블록 무게가 칸 수(부피)보다 가벼우면 떠요. 무거워 보여도 크면 떠요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
