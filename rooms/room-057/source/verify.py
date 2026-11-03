"""ROOM 057 proof: a plank lies on two round rollers on a tiled floor. The rollers roll without slipping, on the floor
and under the plank. The ground arrow shows how many tiles the rollers' centres travel (k). Simulate a roller of radius r
turning by angle t: its centre moves r*t, and its top point (touching the plank) moves r*t + r*t, so the plank moves 2k.
Code = tiles the plank moves for A-D. All 10^4 codes are checked against the simulation; exactly one matches.
Assuming the plank moves as far as the rollers gives the trap."""
import itertools, json, math, os
ROLL = {'A': 1, 'B': 3, 'C': 2, 'D': 4}   # tiles the roller centres travel (ground arrow)
R = 0.42


def plank_shift(k, r=R, steps=1000):
    t_total = k / r; x_c = 0.0; x_top = 0.0
    for _ in range(steps):   # integrate small rolls: centre speed r*w, top point speed centre + r*w
        dt = t_total / steps; x_c += r * dt; x_top += r * dt + r * dt
    return round(x_top, 6), round(x_c, 6)


res = {k: plank_shift(v) for k, v in ROLL.items()}
code = ''.join(str(int(round(res[k][0]))) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
trap = ''.join(str(ROLL[k]) for k in 'ABCD')
print('answer', code, 'solutions', sols, 'trap', trap)
assert sols == ['2648'] and trap == '1324'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'roller_tiles': ROLL, 'plank_tiles': {k: res[k][0] for k in 'ABCD'},
               'trap_same_as_rollers': trap,
               'why': '롤러 중심이 k칸 가는 동안 롤러 윗면은 중심보다 k칸 더 앞으로 가요. 판자는 그 윗면에 붙어 움직이니 2k칸. A 1→2, B 3→6, C 2→4, D 4→8'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
