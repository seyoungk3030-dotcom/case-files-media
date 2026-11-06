"""ROOM 146 proof: the two-balloon paradox. Identical rubber balloons, blown up to different sizes, hang on one air pipe;
each has its own tap. Rubber pressure as a function of stretch L = r / r0 follows the standard thin-rubber law
P(L) = C (1/L - 1/L^7): it RISES while a balloon is small and FALLS once it passes L = 7^(1/6) ~ 1.38, so a bigger
balloon has LOWER pressure. Every balloon here starts beyond the peak. When the open taps are opened, air flows from
high to low pressure; the flow is integrated numerically (air volume kept) until it settles. Digit = the label of the
one balloon that ends up BIGGER than it started (balloons behind a closed tap do not take part). All 10^4 codes
compared; exactly one matches. The trap: 'air flows from big to small until they are even' - the smallest open
balloon would grow."""
import itertools, json, os
PEAK = 7 ** (1 / 6)
# label -> (start stretch L, tap open?)
BOARDS = {'A': {1: (1.6, True), 4: (2.2, True), 7: (1.8, True)},
          'B': {2: (2.4, False), 5: (1.7, True), 8: (2.0, True), 3: (1.5, True)},
          'C': {6: (1.9, True), 9: (1.6, True), 1: (2.5, False)},
          'D': {3: (1.6, True), 7: (2.1, True), 2: (1.8, True), 5: (1.5, True)}}


def P(L): return 1 / L - 1 / L ** 7


def settle(b):
    open_ = [k for k, (L, o) in b.items() if o]; V = {k: b[k][0] ** 3 for k in open_}
    for _ in range(200000):
        L = {k: v ** (1 / 3) for k, v in V.items()}; pm = sum(P(L[k]) for k in open_) / len(open_)
        dV = {k: 0.02 * (P(L[k]) - pm) for k in open_}  # flow out of high pressure into the shared pipe, back into low
        for k in open_: V[k] = max(V[k] - dV[k], 1.0001)
        if max(abs(x) for x in dV.values()) < 1e-9: break
    return {k: V[k] ** (1 / 3) for k in open_}


for b in BOARDS.values(): assert all(L > PEAK for L, _ in b.values())
END = {k: settle(b) for k, b in BOARDS.items()}
GROW = {k: [lab for lab, L in END[k].items() if L > BOARDS[k][lab][0] + 1e-3] for k in BOARDS}
for k in BOARDS: assert len(GROW[k]) == 1 and GROW[k][0] == max((L, lab) for lab, (L, o) in BOARDS[k].items() if o)[1], k
code = ''.join(str(GROW[k][0]) for k in 'ABCD')
trap = ''.join(str(min((L, lab) for lab, (L, o) in BOARDS[k].items() if o)[1]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: {l: round(v, 2) for l, v in e.items()} for k, e in END.items()})
assert sols == ['4867'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': {k: {str(l): v for l, v in b.items()} for k, b in BOARDS.items()},
               'end_stretch': {k: {str(l): round(v, 3) for l, v in e.items()} for k, e in END.items()}, 'trap_smallest_grows': trap,
               'why': '작은 풍선일수록 고무가 더 세게 조여서 압력이 높아요. 그래서 공기가 작은 풍선에서 큰 풍선으로 넘어가요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
