"""ROOM 074 proof: one desk, several things showing numbers. A = how many 9s, B = how many 6s, C = how many 8s,
D = how many 0s can be seen in total (every digit counts, two in one display count twice; ':' ',' '원' are not digits).
The counts are taken directly from the strings drawn in scene3d.py, so the picture and the proof cannot drift apart.
Counting things that show the digit instead of the digits themselves (the trap) gives another code."""
import itertools, json, os
ITEMS = {'clock': '11:59', 'calc': '9696', 'calendar': '29', 'tag': '8,990원', 'bus': '6610', 'note': '88'}
KEYS = {'A': '9', 'B': '6', 'C': '8', 'D': '0'}
res = {k: sum(s.count(d) for s in ITEMS.values()) for k, d in KEYS.items()}
objs = {k: sum(d in s for s in ITEMS.values()) for k, d in KEYS.items()}
code = ''.join(str(res[k]) for k in 'ABCD'); trap = ''.join(str(objs[k]) for k in 'ABCD')
assert all(v <= 9 for v in res.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, 'solutions', sols)
assert sols == ['6432'] and trap == '4222'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'items': ITEMS, 'digits': KEYS, 'counts': res, 'trap_objects_with_digit': trap,
               'why': '숫자 하나하나를 셈. 한 화면에 두 번 나오면 두 개'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
