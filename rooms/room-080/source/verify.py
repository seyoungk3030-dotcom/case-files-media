"""ROOM 080 proof: a row of seesaws, each touching the next end to end. 'U' = this seesaw's right end is UNDER the next
one's left end (it can only push it up); 'O' = it rests ON TOP of it (it can only push it down). The left end of
seesaw 1 is pushed down, so its right end rises. A rising end under the next lifts it (the next one's right end goes
down); a falling end on top presses it (the next one's right end goes up); any other move just separates and the chain
stops. Each digit is how many seesaws move. All 10^4 codes compared; exactly one matches. 'All of them move' (the trap)
gives another code."""
import itertools, json, os
BOARDS = {'A': 'UOUOU', 'B': 'UOO', 'C': 'OUO', 'D': 'UOUOOU'}


def moving(contacts):
    n, d = 1, +1                                   # seesaw 1 moves, right end goes up
    for c in contacts:
        if (c == 'U' and d > 0) or (c == 'O' and d < 0): n += 1; d = -d
        else: break
    return n


code = ''.join(str(moving(BOARDS[k])) for k in 'ABCD')
trap = ''.join(str(len(BOARDS[k]) + 1) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['6315'] and trap == '6447'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'contacts': BOARDS, 'trap_all_move': trap,
               'why': '아래에서 받친 끝은 올라갈 때만, 위에 얹힌 끝은 내려갈 때만 다음 시소를 움직여요. 반대로 움직이면 떨어지고 멈춰요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
