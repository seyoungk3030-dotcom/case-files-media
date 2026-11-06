"""ROOM 084 proof: an hourglass holding N minutes of sand starts with all of it on top. A step 'run t' lets sand fall
for t minutes (never below 0 on top); 'flip' swaps top and bottom. Each digit is the minutes of sand left on top at the
end. All 10^4 codes compared; exactly one matches. Ignoring the flips (the trap) gives another code."""
import itertools, json, os
GLASSES = {'A': (8, [5, 'flip', 2]), 'B': (7, [2, 'flip', 1, 'flip']), 'C': (5, [3, 'flip', 4]), 'D': (9, [6, 'flip', 2, 'flip', 3])}


def run(cap, steps, flips=True):
    top, bot = cap, 0
    for s in steps:
        if s == 'flip':
            if flips: top, bot = bot, top
        else:
            f = min(top, s); top -= f; bot += f
    return top, bot


END = {k: run(*v) for k, v in GLASSES.items()}
code = ''.join(str(END[k][0]) for k in 'ABCD'); trap = ''.join(str(run(*GLASSES[k], flips=False)[0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, END)
assert sols == ['3602'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'glasses_minutes_steps': GLASSES, 'end_top_bottom': END, 'trap_no_flips': trap,
               'why': '뒤집으면 위아래 모래가 자리를 바꿔요. 윗칸이 비면 더 떨어지지 않아요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
