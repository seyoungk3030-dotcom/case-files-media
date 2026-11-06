"""ROOM 101 proof: shadow digit. Bars float in front of a wall at y = WALL. A lamp shines parallel light straight
along +y onto the wall, so a bar's shadow is the bar with its y (depth) dropped. Real bars lie along x or z, each in
one seven-segment slot but at its own depth, so from the camera's angled view they look scrambled. Decoy bars point
straight at the lamp (along y): their shadow is only a dot. Each board's digit is the seven-segment digit the shadow
shows. All 10^4 codes are compared: exactly one matches. Reading the decoys as the segment they sit on (the trap)
gives a different code."""
import itertools, json, os

SEG = {'a': ((0, 2), (1, 2)), 'b': ((1, 1), (1, 2)), 'c': ((1, 0), (1, 1)), 'd': ((0, 0), (1, 0)),
       'e': ((0, 0), (0, 1)), 'f': ((0, 1), (0, 2)), 'g': ((0, 1), (1, 1))}
DIG = {'abcdef': 0, 'bc': 1, 'abdeg': 2, 'abcdg': 3, 'bcfg': 4, 'acdfg': 5, 'acdefg': 6, 'abc': 7, 'abcdefg': 8, 'abcdfg': 9}
WALL = 2.6
# board: real bars (slot, depth y) and decoys (slot whose midpoint they pierce, y from, y to)
BOARDS = {'A': {'real': [('b', -1.4), ('c', 1.2)], 'decoy': [('a', -1.6, 0.2)]},
          'B': {'real': [('a', 0.9), ('f', -1.3), ('g', 1.5), ('c', -0.4), ('d', -1.6)], 'decoy': [('e', -0.6, 1.2)]},
          'C': {'real': [('a', -1.5), ('b', 0.6), ('g', -0.2), ('c', 1.4), ('d', -0.9)], 'decoy': [('f', -1.2, 0.6)]},
          'D': {'real': [('f', 1.3), ('g', -1.4), ('b', 0.1), ('c', -0.8)], 'decoy': [('a', -0.2, 1.5), ('d', -1.7, 0.0)]}}


def bars(k):
    """3D bars as ((x, y, z), (x, y, z)) in template units."""
    out = []
    for s, y in BOARDS[k]['real']:
        (x0, z0), (x1, z1) = SEG[s]; out.append(((x0, y, z0), (x1, y, z1)))
    for s, y0, y1 in BOARDS[k]['decoy']:
        (x0, z0), (x1, z1) = SEG[s]; xm, zm = (x0 + x1) / 2, (z0 + z1) / 2; out.append(((xm, y0, zm), (xm, y1, zm)))
    return out


def shadow(k):
    lit = set()
    for p, q in bars(k):
        assert max(p[1], q[1]) < WALL
        a, b = (p[0], p[2]), (q[0], q[2])
        if abs(a[0] - b[0]) + abs(a[1] - b[1]) < 1e-9: continue          # a dot
        for s, ends in SEG.items():
            if {a, b} == set(ends): lit.add(s)
    return ''.join(sorted(lit))


def digit(segs): return DIG.get(segs)


RES = {k: digit(shadow(k)) for k in 'ABCD'}
TRAP = {k: digit(''.join(sorted(set(shadow(k)) | {s for s, *_ in BOARDS[k]['decoy']}))) for k in 'ABCD'}
code = ''.join(str(RES[k]) for k in 'ABCD'); trap = ''.join(str(TRAP[k]) for k in 'ABCD')
assert all(v is not None for v in RES.values()) and all(v is not None for v in TRAP.values())
# depth matters only for the camera: no two real bars of one board share a depth, so none line up by accident
assert all(len({y for _, y in v['real']}) == len(v['real']) for v in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: shadow(k) for k in 'ABCD'})
assert sols == ['1534'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'shadow_segments': {k: shadow(k) for k in 'ABCD'},
               'trap_count_decoys': trap,
               'why': '빛이 정면에서 곧게 오니 그림자는 앞뒤 깊이를 지운 모양. 빛을 향해 꽂힌 막대는 점 그림자라 획이 안 돼요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
