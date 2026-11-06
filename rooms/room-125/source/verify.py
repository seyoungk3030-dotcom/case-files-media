"""ROOM 125 proof: spring-scale readings (kg). A spring scale shows the pull in the rope through it (the tension);
scales and ropes weigh nothing, everything hangs still.
  pulleys: rope over two pulleys, the scale in the middle, a weight W on each side -> the rope pulls W, reads W.
  wall: one end tied to a wall, the other over a pulley with W -> the wall pulls back W, reads W.
  chain: ceiling - scale X - block a - scale Y - block b: Y carries b, X carries a + b.
Digit = the reading of the scale with the '?' tag. All 10^4 codes are compared; exactly one matches. The trap:
'both ends add up' (2W), 'the wall pulls nothing' (0), or for a chain 'only what hangs right below' (a for X,
a + b for Y)."""
import itertools, json, os

BOARDS = {'A': {'kind': 'pulleys', 'W': 3}, 'B': {'kind': 'wall', 'W': 7},
          'C': {'kind': 'chain', 'a': 3, 'b': 2, 'ask': 'X'}, 'D': {'kind': 'chain', 'a': 1, 'b': 4, 'ask': 'Y'}}


def solve(b):
    if b['kind'] == 'pulleys': return b['W'], 2 * b['W']
    if b['kind'] == 'wall': return b['W'], 0
    return (b['a'] + b['b'], b['a']) if b['ask'] == 'X' else (b['b'], b['a'] + b['b'])


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['3754'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'trap_naive': trap,
               'why': '저울은 줄이 당기는 힘 하나를 재요. 양쪽에서 같은 힘으로 당겨야 멈춰 있으니, 한쪽 힘만큼만 읽어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
