"""ROOM 075 proof: Korean city buses drive on the right and have their doors on the right-hand side. The bus body is
drawn symmetric (front and back look alike). Seen from the side: if the doors face us we see its right side, so its
front points to our right; with no doors we see its left side and it heads to our left. Each board has a stop at each
end; the digit is the number of the stop the bus drives to. All 10^4 codes compared; exactly one matches. Guessing the
opposite way everywhere (the trap) gives the other stop numbers."""
import itertools, json, os
BOARDS = {'A': (False, 3, 8), 'B': (True, 5, 2), 'C': (True, 1, 9), 'D': (False, 4, 6)}   # doors visible, left stop, right stop
res = {k: (r if d else l) for k, (d, l, r) in BOARDS.items()}
trap = ''.join(str(l if d else r) for d, l, r in BOARDS.values())
code = ''.join(str(res[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, 'solutions', sols)
assert sols == ['3294'] and trap == '8516'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards_doors_left_right': BOARDS, 'trap_opposite': trap,
               'why': '한국 버스는 오른쪽 차선, 문은 오른쪽 옆면에. 문이 보이면 오른쪽 옆면 → 오른쪽으로 감, 문이 안 보이면 왼쪽 옆면 → 왼쪽으로 감'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
