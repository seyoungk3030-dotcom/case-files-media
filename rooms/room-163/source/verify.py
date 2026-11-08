"""ROOM 163 proof: socks in a drawer, pulled out one at a time without looking (single socks, any two of one colour make
a pair). Digit = the least number of socks you must pull to be SURE of the goal on the tag. For every n, every possible
handful of n socks (all colour-count vectors allowed by the drawer) is checked; the digit is the first n for which all
of them meet the goal. All 10^4 codes compared; exactly one matches. The trap: the goal's own number of socks (as if
you were lucky)."""
import itertools, json, os
COL = ['R', 'B', 'Y', 'G']
BOARDS = {'A': {'socks': {'R': 4, 'B': 4, 'G': 4}, 'goal': ('same', 2), 'tag': '같은 색 2개'},
          'B': {'socks': {'R': 3, 'B': 5, 'Y': 2}, 'goal': ('color', 'R', 2), 'tag': '빨강 2개'},
          'C': {'socks': {'R': 5, 'B': 5}, 'goal': ('same', 3), 'tag': '같은 색 3개'},
          'D': {'socks': {'R': 6, 'B': 2, 'G': 1}, 'goal': ('diff', 2), 'tag': '다른 색 2개'}}


def ok(goal, hand):
    if goal[0] == 'same': return max(hand.values()) >= goal[1]
    if goal[0] == 'color': return hand.get(goal[1], 0) >= goal[2]
    return sum(1 for v in hand.values() if v) >= goal[1]


def least(b):
    ks = list(b['socks']); tot = sum(b['socks'].values())
    for n in range(1, tot + 1):
        hands = [dict(zip(ks, v)) for v in itertools.product(*[range(b['socks'][k] + 1) for k in ks]) if sum(v) == n]
        if all(ok(b['goal'], h) for h in hands): return n


def worst(b):
    s = b['socks']; g = b['goal']
    if g[0] == 'same':
        seq = [c for c in s for _ in range(min(s[c], g[1] - 1))]; seq.append(next(c for c in s if s[c] >= g[1]))
    elif g[0] == 'color':
        seq = [c for c in s if c != g[1] for _ in range(s[c])] + [g[1]] * g[2]
    else:
        big = max(s, key=s.get); seq = [big] * s[big] + [next(c for c in s if c != big)]
    return seq


RES = {k: least(b) for k, b in BOARDS.items()}
SEQ = {k: worst(b) for k, b in BOARDS.items()}
for k, b in BOARDS.items():
    assert len(SEQ[k]) == RES[k]
    h = {}; 
    for i, c in enumerate(SEQ[k]):
        h[c] = h.get(c, 0) + 1
        assert ok(b['goal'], h) == (i == len(SEQ[k]) - 1)  # the goal is met only with the last sock
code = ''.join(str(RES[k]) for k in 'ABCD')
trap = ''.join(str(b['goal'][-1]) for b in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, SEQ)
assert len(sols) == 1 and all(a != t for a, t in zip(code, trap))
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'worst_case_draw': SEQ, 'trap_lucky': trap,
               'why': '운이 가장 나쁜 경우를 생각해야 해요. 원하지 않는 양말이 먼저 다 나온다고 보고 세요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
