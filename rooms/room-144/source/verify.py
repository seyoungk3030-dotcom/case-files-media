"""ROOM 144 proof: yut sticks (윷놀이). Each throw is four half-round sticks; a stick shows its flat side (배, F) or its
round back (등, R). Count of flat sides up: 1 도 (+1), 2 개 (+2), 3 걸 (+3), 4 윷 (+4), and ZERO flat sides is 모
(+5). One stick (index 0) carries the 빽도 mark: if it is the ONLY flat side up, the piece goes BACK one (-1).
Each board shows two throws; digit = total spaces the piece moves forward. All 10^4 codes compared; exactly one
matches. The trap: reading 모 as 0 and 빽도 as an ordinary 도 (+1)."""
import itertools, json, os
BOARDS = {'A': ['FRFF', 'RRRR'], 'B': ['RFRF', 'FRRR'], 'C': ['FFFF', 'RRFR'], 'D': ['FFRF', 'FFFF']}
NAME = {1: '도', 2: '개', 3: '걸', 4: '윷', 5: '모', -1: '빽도'}


def value(t, naive=False):
    n = t.count('F')
    if n == 0: return 0 if naive else 5
    if n == 1 and t[0] == 'F' and not naive: return -1
    return n


code = ''.join(str(sum(value(t) for t in BOARDS[k])) for k in 'ABCD')
trap = ''.join(str(sum(value(t, True) for t in BOARDS[k])) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, {k: [NAME[value(t)] for t in b] for k, b in BOARDS.items()})
assert sols == ['8157'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'throws': {k: [NAME[value(t)] for t in b] for k, b in BOARDS.items()},
               'trap_mo_zero_backdo_plus': trap, 'why': '배가 하나도 안 보이면 모(5칸), 빽도 표시 막대만 배가 보이면 한 칸 뒤로 가요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
