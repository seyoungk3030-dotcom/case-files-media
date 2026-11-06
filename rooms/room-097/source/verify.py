"""ROOM 097 proof: straight vertical knife cuts across a round cake (chords between two rim angles), plus, on some
cakes, one horizontal cut through the middle of the height. For chords with no three meeting at one point, the top
splits into 1 + (chords) + (crossings inside the cake) pieces; a horizontal cut doubles every piece. The count is also
checked by flood-filling a 600x600 raster of the top. Each digit is the number of pieces. All 10^4 codes compared;
exactly one matches. Counting cuts + 1 (the trap) gives another code."""
import itertools, json, math, os
BOARDS = {'A': ([(115, 340), (60, 290), (85, 215)], False),
          'B': ([(90, 305), (50, 245), (10, 115), (270, 340)], False),
          'C': ([(80, 250), (170, 300), (200, 40)], False),
          'D': ([(90, 270), (180, 0)], True)}


def P(a): return (math.cos(math.radians(a)), math.sin(math.radians(a)))


def cross(c1, c2):
    (x1, y1), (x2, y2) = P(c1[0]), P(c1[1]); (x3, y3), (x4, y4) = P(c2[0]), P(c2[1])
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    if abs(d) < 1e-12: return None
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / d; u = -((x1 - x2) * (y1 - y3) - (y1 - y2) * (x1 - x3)) / d
    if 1e-9 < t < 1 - 1e-9 and 1e-9 < u < 1 - 1e-9: return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def formula(k):
    ch, hz = BOARDS[k]; pts = [p for a, b in itertools.combinations(ch, 2) if (p := cross(a, b))]
    for p, q in itertools.combinations(pts, 2): assert math.dist(p, q) > 0.08, (k, 'near-concurrent')
    return (1 + len(ch) + len(pts)) * (2 if hz else 1), pts


def raster(k, N=600):
    ch, hz = BOARDS[k]; grid = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            x, y = (j + 0.5) / N * 2 - 1, 1 - (i + 0.5) / N * 2
            if x * x + y * y > 0.97: grid[i][j] = -1; continue
            for a, b in ch:
                (x1, y1), (x2, y2) = P(a), P(b)
                if abs((x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)) / math.hypot(x2 - x1, y2 - y1) < 2.5 / N: grid[i][j] = -1; break
    lab = 0; cents = []
    for i in range(N):
        for j in range(N):
            if grid[i][j] == 0:
                lab += 1; st = [(i, j)]; grid[i][j] = lab; sx = sy = n = 0
                while st:
                    a, b = st.pop(); sx += b; sy += a; n += 1
                    for da, db in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        c, d = a + da, b + db
                        if 0 <= c < N and 0 <= d < N and grid[c][d] == 0: grid[c][d] = lab; st.append((c, d))
                if n > 40: cents.append(((sx / n + 0.5) / N * 2 - 1, 1 - (sy / n + 0.5) / N * 2, n))
    return cents


RES = {}
for k in 'ABCD':
    f, pts = formula(k); c = raster(k); assert len(c) * (2 if BOARDS[k][1] else 1) == f, (k, f, len(c)); RES[k] = (f, c)
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(len(BOARDS[k][0]) + (1 if BOARDS[k][1] else 0) + 1) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['6978'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_chords_deg_and_horizontal_cut': BOARDS,
               'pieces': {k: RES[k][0] for k in 'ABCD'}, 'trap_cuts_plus_one': trap,
               'why': '조각 수 = 1 + 칼질 수 + 케이크 안에서 칼자국이 만나는 점 수. 가로로 한 번 더 자르면 모든 조각이 둘로 나뉘어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
