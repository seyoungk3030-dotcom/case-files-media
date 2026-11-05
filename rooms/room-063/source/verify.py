"""ROOM 063 proof: four pairs of discs with holes at eight clock positions (1 at the top, counting clockwise).
The top disc turns clockwise by K clicks (one click = one position) and is laid on the bottom disc.
Light passes only where a top hole sits over a bottom hole. For every board exactly one position lets light through.
All 10^4 codes are compared with those positions, exactly one matches. Turning the other way gives the trap."""
import itertools, json, os
BOARDS = {'A': ({1, 4, 6}, {3, 5, 7}, 2), 'B': ({2, 5, 8}, {1, 7, 8}, 3), 'C': ({1, 3, 7}, {1, 4, 6}, 1), 'D': ({3, 6, 7}, {2, 4, 7}, 3)}


def turn(S, k): return {(p - 1 + k) % 8 + 1 for p in S}


def through(k, cw=True):
    T, B, n = BOARDS[k]; return sorted(turn(T, n if cw else -n) & B)


res = {k: through(k) for k in 'ABCD'}; tr = {k: through(k, False) for k in 'ABCD'}
assert all(len(v) == 1 for v in res.values()) and all(len(v) == 1 for v in tr.values()), (res, tr)
code = ''.join(str(res[k][0]) for k in 'ABCD'); trap = ''.join(str(tr[k][0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, 'solutions', sols)
assert sols == ['3842'] and trap == '7764'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': {k: [sorted(t), sorted(b), n] for k, (t, b, n) in BOARDS.items()},
               'trap_counter_clockwise': trap,
               'why': '위 판 구멍 번호 + 돌린 칸 수 (8 넘으면 8 빼기)와 아래 판 구멍이 겹치는 곳. A 3 · B 8 · C 4 · D 2'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
