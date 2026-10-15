"""ROOM 013 proof: two November-2026 dates (10th or later, first < second), code = DD+DD."""
import datetime, json, os
FRI = 4
def wd(d): return datetime.date(2026, 11, d).weekday()
CLUES = [('두 날은 같은 요일', lambda a, b: wd(a) == wd(b)),
         ('두 번째 날은 금요일', lambda a, b: wd(b) == FRI),
         ('두 번째 날은 20일 이후', lambda a, b: b > 20),
         ('네 자리 숫자는 모두 다르다', lambda a, b: len(set(f'{a}{b}')) == 4)]
tested, sols = 0, []
for a in range(10, 31):
    for b in range(a + 1, 31):
        tested += 1
        if all(f(a, b) for _, f in CLUES): sols.append(f'{a}{b}')
trap = [f'{a}{b}' for a in range(10, 31) for b in range(a + 1, 31) if all(f(a, b) for _, f in CLUES[:3])]
print(tested, sols, 'without clue 4:', trap)
assert sols == ['1327']
json.dump({'unique_answer': sols[0], 'tested_pairs': tested, 'clues': [c for c, _ in CLUES],
           'rules': 'November 2026 calendar, both dates 10-30, first < second, code = first DD + second DD',
           'candidates_without_distinct_digit_clue': trap},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
