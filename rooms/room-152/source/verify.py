"""ROOM 152 proof: one move of mancala (Kalah rules). Your six pits are the bottom row (left to right), your store is
the right end, the opponent's six pits are the top row and their store the left end. You lift every seed from the
starred pit and sow them one per pit counter-clockwise: rightwards along your row, into YOUR store, leftwards along the
top row, past the opponent's store WITHOUT dropping one there, then on along your row. Capture: if the last seed lands
in one of your own pits that was empty, that seed and every seed in the opposite top pit go to your store. Your store
starts empty. Digit = seeds in your store after the move. All 10^4 codes compared; exactly one matches. The trap:
forgetting the capture rule (only the seeds sown straight into the store)."""
import itertools, json, os
BOARDS = {'A': {'me': [0, 0, 2, 0, 0, 0], 'op': [0, 1, 0, 1, 4, 1], 'pick': 2},
          'B': {'me': [1, 1, 0, 1, 0, 0], 'op': [0, 1, 2, 0, 1, 0], 'pick': 1},
          'C': {'me': [1, 0, 0, 1, 10, 1], 'op': [0, 4, 1, 0, 1, 0], 'pick': 4},
          'D': {'me': [0, 0, 1, 1, 9, 0], 'op': [3, 0, 0, 2, 0, 0], 'pick': 4}}


def sow(b, capture=True):
    me, op, i = b['me'][:], b['op'][:], b['pick']; n = me[i]; me[i] = 0; store = 0; assert 0 < n < 13
    seq = [('m', j) for j in range(i + 1, 6)] + [('S', 0)] + [('o', j) for j in range(5, -1, -1)] + [('m', j) for j in range(0, i)]
    last = None; capd = None
    for p in seq[:n]:
        last = p
        if p[0] == 'm': me[p[1]] += 1
        elif p[0] == 'o': op[p[1]] += 1
        else: store += 1
    if capture and last[0] == 'm' and me[last[1]] == 1 and op[last[1]] > 0:
        capd = last[1]; store += op[capd] + 1; op[capd] = 0; me[capd] = 0
    return store, me, op, capd, last


RES = {k: sow(b) for k, b in BOARDS.items()}
code = ''.join(str(RES[k][0]) for k in 'ABCD'); trap = ''.join(str(sow(BOARDS[k], False)[0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: (r[3], r[4]) for k, r in RES.items()})
assert sols == ['5376'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'after': {k: {'store': r[0], 'me': r[1], 'op': r[2], 'captured_pit': r[3]} for k, r in RES.items()},
               'trap_no_capture': trap, 'why': '마지막 씨앗이 내 쪽 빈 칸에 떨어지면 맞은편 씨앗까지 통째로 내 창고로 와요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
