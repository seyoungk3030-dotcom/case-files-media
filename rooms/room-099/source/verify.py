"""ROOM 099 proof: paper loops with n half twists, cut all the way round along k dashed lines that split the width
into k + 1 equal lanes. Going once round the loop, lane j comes back as lane j (n even) or lane k - j (n odd, the paper
is flipped). Lanes that turn into each other are one piece of paper, so the number of loops after cutting is the
number of orbits of that map. Checked by walking the lanes round the loop. Each digit is the number of loops. All
10^4 codes compared; exactly one matches. Counting the lanes, k + 1 (the trap), gives another code."""
import itertools, json, os
BOARDS = {'A': (1, 1), 'B': (0, 3), 'C': (1, 2), 'D': (2, 2)}   # (half twists n, cut lines k)


def loops(n, k):
    lanes = list(range(k + 1)); seen = set(); orbits = []
    for j in lanes:
        if j in seen: continue
        orb = []; x = j
        while x not in orb: orb.append(x); x = x if n % 2 == 0 else k - x
        seen |= set(orb); orbits.append(orb)
    return orbits


RES = {k: loops(*v) for k, v in BOARDS.items()}
code = ''.join(str(len(RES[k])) for k in 'ABCD'); trap = ''.join(str(v[1] + 1) for v in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, RES)
assert sols == ['1423'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'half_twists_and_cuts': BOARDS, 'lane_orbits': RES, 'trap_lanes': trap,
               'why': '꼬임이 홀수면 한 바퀴 돌 때 종이가 뒤집혀서 바깥 줄과 반대쪽 줄이 한 고리로 이어져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
