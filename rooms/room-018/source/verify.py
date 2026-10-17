"""ROOM 018 proof: memo 3861 is the real code with every digit pushed forward by the same k (1-9, 9 wraps to 0).
Brute force every 4-digit code 0000-9999 against all clues."""
import json, os
MEMO = '3861'
def shift_of(code):
    ks = {(int(m) - int(c)) % 10 for m, c in zip(MEMO, code)}
    return ks.pop() if len(ks) == 1 else None
CL = [('① 메모 = 진짜 암호의 모든 자리를 같은 수(1~9)만큼 앞으로 민 것', lambda c: shift_of(c) not in (None, 0)),
      ('② 진짜 암호에 0은 없다', lambda c: '0' not in c),
      ('③ 진짜 암호의 네 숫자를 더하면 20', lambda c: sum(map(int, c)) == 20),
      ('④ 진짜 암호는 홀수', lambda c: int(c[-1]) % 2 == 1)]
codes = [f'{i:04d}' for i in range(10000)]
sols = [c for c in codes if all(f(c) for _, f in CL)]
first3 = [c for c in codes if all(f(c) for _, f in CL[:3])]
print(sols, first3)
assert len(sols) == 1
json.dump({'unique_answer': sols[0], 'tested_codes': 10000, 'candidates_clues_1_to_3': first3, 'memo': MEMO,
           'clues': [c for c, _ in CL], 'rules': 'each digit shifted forward by the same k in 1-9, 9 wraps to 0'},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
