"""ROOM 034 proof: the matchstick number 1610. Move exactly one match (anywhere, any digit) so that every place still
shows a proper digit in the chart's shapes, and make the number as large as possible. Code = that number.
Every single move is enumerated; the largest result is unique by construction and is checked here. Moving a match
only inside one digit (the tempting 6 -> 9) gives a smaller number, so the cross-digit move is needed."""
import json, os
SEG = {0: 'abcdef', 1: 'bc', 2: 'abdeg', 3: 'abcdg', 4: 'bcfg', 5: 'acdfg', 6: 'acdefg', 7: 'abc', 8: 'abcdefg', 9: 'abcdfg'}
INV = {frozenset(v): k for k, v in SEG.items()}
START = '1610'


def moves(n):
    ds = [set(SEG[int(c)]) for c in n]; out = {}
    for i in range(len(n)):
        for s in ds[i]:
            for j in range(len(n)):
                for t in 'abcdefg':
                    nd = [set(x) for x in ds]; nd[i].discard(s)
                    if t in nd[j] or (i == j and t == s): continue
                    nd[j].add(t)
                    if all(frozenset(x) in INV for x in nd):
                        out.setdefault(''.join(str(INV[frozenset(x)]) for x in nd), []).append((i, s, j, t))
    return out


m = moves(START)
best = max(m); within = max(k for k, v in m.items() if any(i == j for i, s, j, t in v))
print(sorted(m, reverse=True), 'best', best, m[best], 'within one digit', within)
assert best == '7510' and len(m[best]) == 1 and within == '1910'
json.dump({'unique_answer': best, 'start': START, 'all_one_move_results': sorted(m, reverse=True), 'move': m[best][0],
           'trap_within_one_digit': within,
           'why': '6의 왼쪽 아래 성냥을 빼면 5, 그 성냥을 1 위에 얹으면 7 → 7510. 6을 9로 바꾸면 1910이라 더 작다'},
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
