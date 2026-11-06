"""ROOM 136 proof: a race down one ramp. Released together from rest, a body that rolls without slipping has
acceleration g sin(theta) / (1 + k), where k = I / (m r^2) depends only on its SHAPE: solid ball 0.4, solid cylinder
0.5, hollow ball 2/3, thin ring 1; an ice block slides without rolling or friction (k = 0). Mass and size cancel.
Digit = the number on the winner (smallest k). All 10^4 codes are compared; exactly one matches. The trap: 'the
heaviest wins'."""
import itertools, json, os

K = {'ice': 0.0, 'ball': 0.4, 'cyl': 0.5, 'shell': 2 / 3, 'ring': 1.0}
BOARDS = {'A': [{'n': 4, 'kind': 'ring', 'kg': 5, 'size': 1.0}, {'n': 7, 'kind': 'ball', 'kg': 0.2, 'size': 0.5}, {'n': 2, 'kind': 'cyl', 'kg': 1, 'size': 0.7}],
          'B': [{'n': 3, 'kind': 'shell', 'kg': 2, 'size': 0.9}, {'n': 5, 'kind': 'cyl', 'kg': 0.3, 'size': 0.5}, {'n': 8, 'kind': 'ring', 'kg': 4, 'size': 0.8}],
          'C': [{'n': 6, 'kind': 'ball', 'kg': 7, 'size': 1.0}, {'n': 1, 'kind': 'ice', 'kg': 0.5, 'size': 0.5}, {'n': 9, 'kind': 'cyl', 'kg': 2, 'size': 0.8}],
          'D': [{'n': 2, 'kind': 'shell', 'kg': 3, 'size': 1.0}, {'n': 0, 'kind': 'ring', 'kg': 0.5, 'size': 0.6}, {'n': 3, 'kind': 'cyl', 'kg': 1, 'size': 0.7}]}


def solve(b):
    w = min(b, key=lambda o: K[o['kind']]); assert sum(K[o['kind']] == K[w['kind']] for o in b) == 1
    h = max(b, key=lambda o: o['kg']); assert h is not w
    return w['n'], h['n']


RES = {k: solve(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) == solve(BOARDS[k])[0] for i, k in enumerate('ABCD'))]
print('answer', code, 'trap', trap)
assert sols == ['7513'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'k_values': K, 'boards': BOARDS, 'trap_heaviest': trap,
               'why': '굴러 내려가는 빠르기는 무게나 크기가 아니라 모양(무게가 바깥에 몰린 정도)으로 정해져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
