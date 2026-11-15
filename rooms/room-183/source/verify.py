"""ROOM 183 proof: push or pull? A hallway of closed doors seen from your side. A door swings toward the side where
its hinge knuckles (the round barrels on the hinge edge) are visible, so visible hinges = PULL; no hinges on your
side = PUSH. The handle style does not decide it (some doors have a pull handle but must be pushed, or a flat push
plate but must be pulled). Digit = number of doors you must pull. All 10^4 codes compared; exactly one matches.
The trap: counting the doors that have a pull handle."""
import itertools, json, os

# each door: hinges visible on your side (True = pull), handle 'bar' (pull handle) or 'plate' (push plate), hinge edge 'L'/'R'
BOARDS = {'A': [(True, 'plate', 'L'), (False, 'bar', 'R'), (True, 'bar', 'R'), (False, 'bar', 'L'), (False, 'plate', 'R')],
          'B': [(True, 'plate', 'R'), (True, 'plate', 'L'), (False, 'bar', 'L'), (True, 'bar', 'L'), (True, 'plate', 'R')],
          'C': [(False, 'bar', 'L'), (False, 'bar', 'R'), (False, 'plate', 'L'), (False, 'bar', 'L')],
          'D': [(True, 'bar', 'L'), (False, 'plate', 'R'), (True, 'plate', 'R'), (False, 'bar', 'L'), (True, 'plate', 'L')]}
GOOD = {k: sum(d[0] for d in v) for k, v in BOARDS.items()}
TRAPV = {k: sum(d[1] == 'bar' for d in v) for k, v in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] for k in 'ABCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'pull_count': GOOD, 'trap_count_pull_handles': trap,
               'why': '문은 경첩(동그란 마디)이 보이는 쪽으로 열려요. 경첩이 보이면 당기고, 안 보이면 밀어요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
