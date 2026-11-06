"""ROOM 096 proof: ball races on three tracks per board. Every track starts at the same height H and ends at the same
point (L across, height 0); only the shape differs: y(x) = H(1 - x/L) - a sin(pi x/L) - b sin(2 pi x/L). Released from
rest without friction, the time is the integral of ds / sqrt(2 g (H - y)) (a rolling ball only scales every time by
the same factor, so the order is the same). Each digit is the number of the track that finishes first; the winner is
at least 4 % faster than the next. All 10^4 codes compared; exactly one matches. Picking the shortest track (the trap)
gives another code."""
import itertools, json, math, os
L, H, G = 2.0, 1.2, 9.81
BOARDS = {'A': [(0, 0), (0.6, 0), (1.0, 0)], 'B': [(0.2, 0.4), (0, 0), (0.4, 0)],
          'C': [(0.6, 0), (1.0, 0.4), (0.2, 0)], 'D': [(0, 0), (-0.2, 0), (0, 0.2)]}


def y(a, b, x): return H * (1 - x / L) - a * math.sin(math.pi * x / L) - b * math.sin(2 * math.pi * x / L)


def run(a, b, n=20000):
    t = s = 0; px, py = 0, y(a, b, 0)
    for i in range(1, n + 1):
        x = L * i / n; yy = y(a, b, x); ds = math.hypot(x - px, yy - py); ym = (yy + py) / 2
        assert ym < H or i == 1
        t += ds / math.sqrt(max(1e-12, 2 * G * (H - ym))); s += ds; px, py = x, yy
    return t, s


RES = {k: [run(a, b) for a, b in v] for k, v in BOARDS.items()}
for k, r in RES.items():
    ts = sorted(t for t, _ in r); assert ts[1] / ts[0] >= 1.04, k
code = ''.join(str(min(range(3), key=lambda i: RES[k][i][0]) + 1) for k in 'ABCD')
trap = ''.join(str(min(range(3), key=lambda i: RES[k][i][1]) + 1) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: [round(t, 3) for t, _ in RES[k]] for k in 'ABCD'})
assert sols == ['2313'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'tracks_a_b': BOARDS,
               'times_s': {k: [round(t, 3) for t, _ in RES[k]] for k in 'ABCD'}, 'lengths': {k: [round(s, 3) for _, s in RES[k]] for k in 'ABCD'},
               'trap_shortest_track': trap, 'why': '처음에 많이 떨어지는 길이 빨리 속도를 얻어요. 가장 짧은 직선이 가장 빠르지 않아요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
