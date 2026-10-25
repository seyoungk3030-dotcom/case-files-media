"""ROOM 043 proof: a small coin (radius r) rolls without slipping once around the outside of a fixed coin (radius R).
How many turns does the small coin make (seen from above)? Simulated: the contact point moves along the fixed rim;
the small coin's own angle = angle of its centre around the fixed coin + rolled arc / r. After one lap the total is
(R + r) / r turns. Code = turns for setups A-D. Counting only the rolled distance (R / r) gives the trap."""
import json, math, os
r = 1.0
SIZES = {'A': 1, 'B': 3, 'C': 2, 'D': 4}      # R as a multiple of r
N = 200000


def turns(R):
    spin = 0.0
    for i in range(N):
        dphi = 2 * math.pi / N                      # centre moves dphi around the fixed coin
        rolled = R * dphi                           # arc length of fixed rim passed = arc on the small coin
        spin += dphi + rolled / r                   # carried around once + rolling
    return spin / (2 * math.pi)


res = {k: turns(v * r) for k, v in SIZES.items()}
code = ''.join(str(round(res[k])) for k in 'ABCD'); trap = ''.join(str(SIZES[k]) for k in 'ABCD')
print({k: round(v, 6) for k, v in res.items()}, 'code', code, 'trap', trap)
assert all(abs(res[k] - SIZES[k] - 1) < 1e-6 for k in res) and code == '2435' and trap != code
json.dump({'unique_answer': code, 'big_coin_radius_in_small_coins': SIZES, 'turns': res, 'trap_rolled_distance_only': trap,
           'why': '작은 동전의 중심은 반지름 R+r인 원을 돈다 → 회전 수 = (R+r)/r = R/r + 1. 같은 크기면 1이 아니라 2바퀴'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
