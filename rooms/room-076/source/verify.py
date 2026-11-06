"""ROOM 076 proof: four viral 'intuition trap' questions, each solved as a rate problem.
A: 3 shirts dry in 60 min side by side; drying is parallel, so 6 shirts (enough line) also take 60 min -> 1 hour.
B: 5 machines make 5 parts in 5 min -> one machine makes one part in 5 min; 100 machines make 100 parts in 5 min.
C: one egg boils in 6 min; three eggs in the same pot boil together -> 6 min.
D: you pass the runner in 2nd place -> you take 2nd place (the runner you passed is now 3rd).
Digits A..D in order; the intuitive traps (2, 100, 18, 1) give a different code."""
import json, os
from fractions import Fraction
A = 60 // 60                                         # parallel drying: time independent of count (hours)
rate = Fraction(5, 5 * 5)                             # parts per machine per minute
B = int(Fraction(100) / (100 * rate))                 # minutes for 100 machines to make 100 parts
C = 6                                                 # same pot, same water: eggs boil in parallel
runners = ['1st', '2nd', 'you']; runners.insert(1, runners.pop(2)); D = runners.index('you') + 1
code = f'{A}{B}{C}{D}'
print('answer', code)
assert code == '1562'
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'A_shirts_hours': A, 'B_machines_minutes': B, 'C_eggs_minutes': C, 'D_place': D,
               'traps': {'A': '2시간', 'B': '100분', 'C': '18분', 'D': '1등'},
               'why': {'A': '빨래는 동시에 말라요. 줄만 충분하면 6장도 1시간', 'B': '기계 1대가 5분에 1개. 100대면 5분에 100개',
                       'C': '한 냄비에서 같이 삶아요. 6분', 'D': '2등을 추월하면 내가 2등 (1등은 아직 앞에)'}},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
