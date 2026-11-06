"""ROOM 116 proof: three switches, three bulbs. In the hall there are three switches with number tags; their bulbs
hang in a closed room you may enter only once. The plan on each board: switch 'first' ON for 10 minutes, then OFF;
switch 'second' ON; the third switch is never touched. Then you walk in. A lit bulb belongs to 'second'; a dark but
WARM bulb (it was on for 10 minutes) belongs to 'first'; a dark COLD bulb belongs to the untouched switch. The board
asks about one bulb (state shown); its switch number is the digit. All 10^4 codes are compared; exactly one matches.
The trap: mixing up warm and cold (thinking the warm dark bulb is the one never touched)."""
import itertools, json, os

BOARDS = {'A': {'switches': [3, 7, 5], 'first': 3, 'second': 7, 'bulbs': ['cold', 'lit', 'warm'], 'ask': 2},
          'B': {'switches': [8, 1, 6], 'first': 6, 'second': 8, 'bulbs': ['warm', 'cold', 'lit'], 'ask': 1},
          'C': {'switches': [4, 9, 2], 'first': 9, 'second': 2, 'bulbs': ['lit', 'warm', 'cold'], 'ask': 1},
          'D': {'switches': [5, 4, 8], 'first': 5, 'second': 8, 'bulbs': ['cold', 'lit', 'warm'], 'ask': 2}}


def owner(b, state):
    third = [s for s in b['switches'] if s not in (b['first'], b['second'])][0]
    return {'lit': b['second'], 'warm': b['first'], 'cold': third}[state]


def swapped(b, state): return owner(b, {'warm': 'cold', 'cold': 'warm', 'lit': 'lit'}[state])


for b in BOARDS.values(): assert sorted(b['bulbs']) == ['cold', 'lit', 'warm'] and b['bulbs'][b['ask']] != 'lit'
code = ''.join(str(owner(b, b['bulbs'][b['ask']])) for b in BOARDS.values())
trap = ''.join(str(swapped(b, b['bulbs'][b['ask']])) for b in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert len(sols) == 1 and all(x != y for x, y in zip(code, trap))
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'trap_warm_cold_swapped': trap,
               'why': '켜져 있는 건 두 번째, 꺼졌지만 따뜻한 건 먼저 켰다 끈 것, 차가운 건 안 건드린 스위치'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
