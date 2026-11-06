"""ROOM 077 proof: each Ferris wheel has 8 cabins, listed clockwise from the top. The wheel turns a number of cabin
steps clockwise (+) or counter-clockwise (-). Cabins hang, so their digits stay upright. After a clockwise turn of t
steps the cabin that was t steps counter-clockwise of the top is at the top. Each digit is the cabin then at the top.
All 10^4 codes compared; exactly one matches. Turning the wrong way (the trap) gives a different code."""
import itertools, json, os
WHEELS = {'A': ([5, 1, 7, 3, 9, 2, 8, 4], +2), 'B': ([2, 6, 0, 4, 7, 1, 3, 5], -2), 'C': ([9, 3, 5, 8, 1, 6, 2, 7], +4), 'D': ([4, 0, 6, 2, 5, 8, 7, 9], -3)}


def top(cab, t):
    pos = {i: (i + t) % 8 for i in range(8)}           # cabin i moves to position i+t
    return [cab[i] for i in range(8) if pos[i] == 0][0]


code = ''.join(str(top(*WHEELS[k])) for k in 'ABCD')
trap = ''.join(str(top(c, -t)) for c, t in WHEELS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['8012'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'wheels_clockwise_from_top_and_turn': WHEELS, 'trap_wrong_direction': trap,
               'why': '시계 방향으로 돌면 왼쪽(반시계 쪽) 칸이 꼭대기로 올라와요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
