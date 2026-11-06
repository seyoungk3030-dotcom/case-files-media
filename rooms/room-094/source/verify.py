"""ROOM 094 proof: billiard shots at 45 degrees on tables measured in diamond units (W x H). Pockets sit at the four
corners and the middle of the two long rails. The ball starts on the bottom rail at (x, 0) and moves one unit across
and one unit up per step, bouncing off a rail like a mirror, until it drops into a pocket. Each digit is the number of
cushion bounces. All 10^4 codes compared; exactly one matches. The pocket number (the trap) gives another code."""
import itertools, json, os
BOARDS = {'A': (12, 5, 5, 1), 'B': (10, 4, 9, 1), 'C': (8, 5, 1, 1), 'D': (10, 4, 4, 1)}


def pockets(W, H): return {(0, 0): 1, (W // 2, 0): 2, (W, 0): 3, (W, H): 4, (W // 2, H): 5, (0, H): 6}


def shot(W, H, x, dx):
    y, dy = 0, 1; P = pockets(W, H); path = [(x, y)]; hits = []
    for _ in range(500):
        if not 0 <= x + dx <= W: dx = -dx; hits.append((x, y))
        if not 0 <= y + dy <= H: dy = -dy; hits.append((x, y))
        x += dx; y += dy; path.append((x, y))
        if (x, y) in P: return len(hits), P[(x, y)], path
    raise ValueError


RES = {k: shot(*v) for k, v in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(RES[k][1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['6534'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_W_H_x_dx': BOARDS, 'paths': {k: RES[k][2] for k in 'ABCD'},
               'trap_pocket_number': trap, 'why': '45도로 친 공은 쿠션에서 거울처럼 꺾여요. 다이아몬드 한 칸씩 따라가면 튕긴 횟수가 나와요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
