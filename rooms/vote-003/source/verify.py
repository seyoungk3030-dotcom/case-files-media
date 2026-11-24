"""VOTE 003 proof (가위로 두꺼운 종이): scissors are a lever pivoting at the screw. Hand force F at the handle, distance
a from the pivot; cutting force at distance b along the blade: F * a = f * b, so f = F * a / b. Closer to the pivot (small
b) gives a larger cutting force. Example: a = 7 cm, F = 30 N: at the tip b = 9 cm -> 23 N, near the pivot b = 2 cm -> 105 N."""
import json, os
F, A = 30.0, 7.0
f = {b: F * A / b for b in (9.0, 5.0, 2.0)}
assert f[2.0] > f[5.0] > f[9.0]
ANSWER = 'B'; OPTIONS = {'A': '날 끝', 'B': '날 안쪽', 'C': '똑같다'}
print({b: round(v) for b, v in f.items()}, 'answer', ANSWER)
if __name__ == '__main__':
    json.dump({'answer': ANSWER, 'options': OPTIONS, 'cut_force_N': {str(b): round(v, 1) for b, v in f.items()},
               'why': '가위는 지렛대예요. 나사(받침점)에 가까울수록 같은 손힘으로 더 세게 잘려요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
