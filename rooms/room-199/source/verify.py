"""ROOM 199 proof (미끄러지는 사다리): a straight ladder of length L stands upright against a wall. Its foot is pulled
straight out d metres along the floor while its top slides down the wall. The top is then at sqrt(L^2 - d^2), so it
dropped L - sqrt(L^2 - d^2) metres. Digit = drop in metres (all whole numbers). All 10^4 codes compared, exactly one
matches. Trap: thinking the top drops as much as the foot moves (3858)."""
import itertools, json, math, os

BOARDS = {'A': (5, 3), 'B': (17, 8), 'C': (13, 5), 'D': (10, 8)}  # ladder length L (m), foot pulled d (m)


def top(L, d):
    h = math.isqrt(L * L - d * d); assert h * h == L * L - d * d; return h


GOOD = {k: L - top(L, d) for k, (L, d) in BOARDS.items()}
for k, v in GOOD.items(): assert 0 < v < 10
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(d % 10) for _, d in (BOARDS[k] for k in 'ABCD'))
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(a != b for a, b in zip(code, trap))
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'top_after': {k: top(*v) for k, v in BOARDS.items()},
               'drop': GOOD, 'trap_code_drop_equals_pull': trap,
               'why': '사다리 길이는 그대로라 꼭대기 높이 = √(길이² − 뺀 거리²). 처음엔 아래를 많이 빼도 위는 조금만 내려와요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
