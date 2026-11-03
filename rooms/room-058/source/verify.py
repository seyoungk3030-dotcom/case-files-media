"""ROOM 058 proof: water pours into glass 1. Each glass has side pipes at a height (fraction of the glass) that lead
down into another glass; a red X pipe is blocked. Model: water rises in a glass until it reaches the lowest open pipe,
then all of it runs down that pipe. When everything below that pipe is full, the level rises to the next pipe, and when
no open pipe is left the glass fills to the rim. So glasses fill in depth-first order, lowest pipe first.
Code = the first four glasses to be completely full. A level-by-level simulation checks the order; all 10^4 codes are
compared and exactly one matches. Ignoring the blocked pipe gives the trap."""
import itertools, json, os
H = 1.0
PIPES = {1: [(0.25, 2, False), (0.7, 3, False)],   # glass: [(pipe height, child glass, blocked)]
         2: [(0.6, 5, False), (0.3, 4, True)],
         3: [(0.2, 6, False), (0.5, 7, False)]}
GLASSES = range(1, 8)


def simulate(ignore_blocks=False, dv=0.01, stop=99):
    level = {g: 0.0 for g in GLASSES}; full = []

    def pour(g, v):   # pour volume v into glass g; returns volume that could not be taken (overflow)
        while v > 1e-9:
            if level[g] >= H - 1e-9: return v
            outs = sorted((h, c) for h, c, b in PIPES.get(g, []) if (ignore_blocks or not b))
            open_out = [(h, c) for h, c in outs if level[g] >= h - 1e-9]
            sent = False
            for h, c in open_out:   # water reaching a pipe runs down it while the glass below takes it
                left = pour(c, v)
                if left < v: v = left; sent = True; break
            if sent: continue
            nxt = [h for h, c in outs if h > level[g] + 1e-9]
            cap = (min(nxt) if nxt else H) - level[g]
            take = min(v, cap); level[g] += take; v -= take
            if level[g] >= H - 1e-9 and g not in full: full.append(g)
        return 0.0

    for _ in range(100000):
        if pour(1, dv) > 0 or len(full) >= stop: break
    return full, level


order, _ = simulate()
code = ''.join(map(str, order[:4]))
trap = ''.join(map(str, simulate(True)[0][:4]))
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'full order', order, 'solutions', sols, 'trap', trap)
assert sols == ['5267'] and trap == '4526'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'full_order': order, 'pipes': {g: [list(p) for p in v] for g, v in PIPES.items()},
               'trap_ignore_blocked': trap,
               'why': '1번 컵은 낮은 관(2번 쪽)부터 · 2번 컵의 낮은 관은 막혀서 5번으로 → 5번, 2번이 차고 · 1번 물이 높은 관까지 올라 3번으로 → 3번의 낮은 관 6번, 그다음 7번'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
