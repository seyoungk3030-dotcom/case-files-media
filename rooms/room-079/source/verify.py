"""ROOM 079 proof: each card shows a seven-segment '8' whose segments are printed in red or blue ink, and a coloured
cellophane. Through a coloured cellophane only that colour's light passes: ink of the filter's own colour is as bright
as the paper there and vanishes, ink of the other colour turns dark. The digit seen is the set of segments whose ink
channel (red channel for a red filter, blue for blue) is dark. All 10^4 codes compared; exactly one matches. Reading the
filter's own colour (the trap) gives no digit for most cards."""
import itertools, json, os
RED, BLUE, PAPER = (232, 64, 64), (44, 96, 232), (246, 244, 238)
SEG = {0: 'abcdef', 1: 'bc', 2: 'abged', 3: 'abgcd', 4: 'fgbc', 5: 'afgcd', 6: 'afgedc', 7: 'abc', 8: 'abcdefg', 9: 'abcdfg'}
# filter colour, segments printed in BLUE (the rest of the '8' is red)
CARDS = {'A': ('red', 'abc'), 'B': ('blue', 'be'), 'C': ('red', 'abged'), 'D': ('blue', 'g')}
CH = {'red': 0, 'blue': 2}


def seen(k):
    flt, blue = CARDS[k]; dark = set()
    for s in 'abcdefg':
        ink = BLUE if s in blue else RED
        if ink[CH[flt]] < PAPER[CH[flt]] / 2: dark.add(s)
    return [d for d, segs in SEG.items() if set(segs) == dark]


SEEN = {k: seen(k) for k in 'ABCD'}
code = ''.join(str(SEEN[k][0]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if all(int(c[i]) in SEEN[k] for i, k in enumerate('ABCD'))]
print('answer', code, sols)
assert sols == ['7520']
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'cards_filter_blue_segments': CARDS,
               'why': '빨간 셀로판으로 보면 빨간 잉크는 종이처럼 밝아져 사라지고 파란 잉크만 검게 보여요. 파란 셀로판은 반대'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
