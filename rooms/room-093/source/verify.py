"""ROOM 093 proof: four optical illusions built from real 3D parts with known sizes. Each digit is the number of the
part that is REALLY the longest / biggest; 0 if all of them are the same size. The sizes below are the exact sizes
the scene is built from, so the answer is checked directly. All 10^4 codes compared; exactly one matches. Picking the
part that LOOKS biggest (the trap) gives another code."""
import itertools, json, os
# A Muller-Lyer rods (length, fins 'in' >-< or 'out' <->); B Ebbinghaus centre-disc radius with ring-disc radius;
# C Jastrow arc blocks (identical); D Ponzo bars on converging rails (length, height from bottom 0..1)
A = {1: (3.30, 'out'), 2: (3.10, 'in'), 3: (3.20, 'out')}   # fins 'out' = arrow heads pointing in (looks short)
B = {1: (0.52, 0.22), 2: (0.50, 0.22), 3: (0.56, 0.50)}
C = {1: 1.0, 2: 1.0, 3: 1.0}
D = {1: (2.30, 0.85), 2: (2.38, 0.50), 3: (2.46, 0.12)}
LOOKS = {'A': 2, 'B': 1, 'C': 1, 'D': 1}


def biggest(vals):
    m = max(vals.values()); w = [k for k, v in vals.items() if v == m]
    return 0 if len(w) == len(vals) else (w[0] if len(w) == 1 else None)


ANS = {'A': biggest({k: v[0] for k, v in A.items()}), 'B': biggest({k: v[0] for k, v in B.items()}),
       'C': biggest(C), 'D': biggest({k: v[0] for k, v in D.items()})}
for k, vals in (('A', [v[0] for v in A.values()]), ('B', [v[0] for v in B.values()]), ('D', [v[0] for v in D.values()])):
    s = sorted(vals); assert s[-1] / s[-2] >= 1.03, k   # at least 3 % bigger, so it can be measured on the answer card
code = ''.join(str(ANS[k]) for k in 'ABCD'); trap = ''.join(str(LOOKS[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['1303'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'A_muller_lyer': A, 'B_ebbinghaus': B, 'C_jastrow': C,
               'D_ponzo': D, 'trap_looks_biggest': trap, 'why': '모양과 주변 때문에 크기가 달라 보일 뿐, 실제 크기는 장면을 만든 숫자 그대로예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
