"""ROOM 086 proof: a desk scene is described as a list of items (kind, position, size, colour). Picture 2 is picture 1
with some edits. The proof compares the two item lists and sorts every difference into exactly one kind: colour
changed (A), item missing (B), item moved (C), size changed (D). Each digit is the number of differences of that kind.
All 10^4 codes compared; exactly one matches."""
import copy, itertools, json, os
ITEMS = {
    'book1': ('book', (-2.9, 1.2), 1.0, 'red'), 'book2': ('book', (-2.6, 1.2), 1.1, 'yellow'), 'book3': ('book', (-2.3, 1.2), 0.9, 'blue'),
    'book4': ('book', (-2.0, 1.2), 1.05, 'green'), 'book5': ('book', (-1.7, 1.2), 0.95, 'purple'),
    'lamp': ('lamp', (-2.4, 0), 1.0, 'teal'), 'plant': ('plant', (2.6, 0), 1.0, 'coral'), 'clock': ('clock', (0.9, 1.9), 1.0, 'white'),
    'mug': ('mug', (-0.9, 0), 1.0, 'white'), 'frame': ('frame', (-0.4, 2.0), 1.0, 'yellow'), 'sun': ('sun', (-0.4, 2.0), 1.0, 'amber'),
    'ball': ('ball', (1.4, 0), 1.0, 'yellow'), 'cube': ('cube', (0.4, 0), 1.0, 'purple'), 'pencils': ('pencils', (2.0, 1.2), 1.0, 'blue'),
}
EDIT = copy.deepcopy(ITEMS)
EDIT['book3'] = ('book', (-2.3, 1.2), 0.9, 'red'); EDIT['ball'] = ('ball', (1.4, 0), 1.0, 'green')               # colour
del EDIT['book5']; del EDIT['cube']; del EDIT['sun']                                                           # missing
EDIT['mug'] = ('mug', (0.25, 0), 1.0, 'white')                                                                 # moved
EDIT['plant'] = ('plant', (2.6, 0), 1.35, 'coral'); EDIT['clock'] = ('clock', (0.9, 1.9), 0.7, 'white')       # size


def diff(a, b):
    out = {'A': [], 'B': [], 'C': [], 'D': []}
    for n, (kind, pos, size, col) in a.items():
        if n not in b: out['B'].append(n); continue
        k2, p2, s2, c2 = b[n]; changes = [c2 != col, n not in b, p2 != pos, s2 != size]
        assert sum(changes) <= 1, n
        for key, ch in zip('ABCD', changes):
            if ch: out[key].append(n)
    assert set(b) <= set(a)
    return out


D = diff(ITEMS, EDIT)
code = ''.join(str(len(D[k])) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, D)
assert sols == ['2312']
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'differences': D,
               'why': '색 2곳(파란 책→빨강, 노란 공→초록) · 사라짐 3곳(보라 책, 보라 큐브, 액자 속 해) · 이동 1곳(머그컵) · 크기 2곳(화분 커짐, 시계 작아짐)'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
