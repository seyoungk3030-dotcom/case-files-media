"""ROOM 081 proof: a 3x3 puzzle cube with a digit on every sticker. Each sticker is a (position, normal, up) triple on
the cube [-1.5, 1.5]^3. One layer turns 90 degrees in the arrow's direction: U = top layer, clockwise seen from above
(right face -> front); F / F' = front layer clockwise / counter-clockwise seen from the front; R' = right layer, top ->
front. The star cell is a fixed place on the front face; each digit is the sticker that lands there. Only stickers
that start on the visible faces (front, right, top) can land on the star, so the puzzle is fair. All 10^4 codes
compared; exactly one matches."""
import itertools, json, os, random
import numpy as np
FACES = {'F': ((0, -1, 0), (1, 0, 0), (0, 0, 1)), 'B': ((0, 1, 0), (-1, 0, 0), (0, 0, 1)), 'R': ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
         'L': ((-1, 0, 0), (0, -1, 0), (0, 0, 1)), 'U': ((0, 0, 1), (1, 0, 0), (0, 1, 0)), 'D': ((0, 0, -1), (1, 0, 0), (0, -1, 0))}
VISIBLE = 'FRU'


def rot(axis, deg):
    t = np.radians(deg); c, s = round(np.cos(t)), round(np.sin(t))
    if axis == 'x': return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == 'y': return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


MOVES = {'U': (lambda p: p[2] > 0.5, rot('z', -90)), 'F': (lambda p: p[1] < -0.5, rot('y', 90)),
         "F'": (lambda p: p[1] < -0.5, rot('y', -90)), "R'": (lambda p: p[0] > 0.5, rot('x', 90))}
BOARDS = {'A': ('U', (-1, 1), 11), 'B': ('F', (-1, 1), 22), 'C': ("R'", (1, -1), 33), 'D': ("F'", (1, 0), 44)}   # move, star (x, z) on front, seed


def stickers(seed):
    rnd = random.Random(seed); out = []
    for f, (n, a, b) in FACES.items():
        n, a, b = map(np.array, (n, a, b))
        for i, j in itertools.product((-1, 0, 1), repeat=2):
            out.append({'face': f, 'pos': n * 1.5 + a * i + b * j, 'n': n, 'up': b, 'd': rnd.randint(0, 9)})
    return out


def turn(st, move):
    sel, R = MOVES[move]; out = []
    for s in st:
        s = dict(s)
        if sel(s['pos']): s['pos'], s['n'], s['up'] = R @ s['pos'], R @ s['n'], R @ s['up']
        out.append(s)
    return out


def at_star(st, star):
    want = np.array([star[0], -1.5, star[1]])
    return [s for s in st if np.allclose(s['pos'], want) and np.allclose(s['n'], (0, -1, 0))][0]


def solve(k):
    move, star, seed = BOARDS[k]; st = stickers(seed); new = at_star(turn(st, move), star)
    src = [s for s in st if s['d'] == new['d'] and s['face'] == new['face'] and s['d'] == new['d']][0]
    assert new['face'] in VISIBLE, k
    return new


RES = {k: solve(k) for k in 'ABCD'}
code = ''.join(str(RES[k]['d']) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, {k: (RES[k]['face'], list(RES[k]['up'])) for k in 'ABCD'},
      'before', ''.join(str(at_star(stickers(BOARDS[k][2]), BOARDS[k][1])['d']) for k in 'ABCD'))
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_move_star_seed': BOARDS,
               'why': '화살표대로 한 줄만 90도 돌려요. 별 칸에 들어오는 스티커를 거꾸로 따라가 보세요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
