"""ROOM 103 proof: block tower (three blocks per layer, layers crossed). Some blocks are already gone. A layer stands
when it still has its middle block, or both side blocks; a layer left with one side block (or none) tips and the
tower above falls. Four blocks are numbered 1-4 in each tower (never in the top layer). Pulling exactly one of them
keeps every layer standing; each digit is that block's number. All 10^4 codes are compared; exactly one matches.
The trap: 'middle blocks are always the safe pull' picks each tower's one numbered middle block, another code."""
import itertools, json, os

# tower: layers bottom -> top, each a 3-char string over L M R ('#' = present, '.' = gone);
# numbered: block number -> (layer index, position 0/1/2)
BOARDS = {'A': {'layers': ['###', '##.', '#.#', '.##', '###', '###'], 'num': {1: (1, 1), 2: (2, 0), 3: (3, 2), 4: (2, 2)}},
          'B': {'layers': ['#.#', '###', '.##', '###', '##.', '###'], 'num': {1: (4, 0), 2: (0, 2), 3: (2, 1), 4: (0, 0)}},
          'C': {'layers': ['.##', '#.#', '###', '##.', '#.#', '###'], 'num': {1: (1, 0), 2: (3, 1), 3: (4, 2), 4: (0, 2)}},
          'D': {'layers': ['##.', '###', '#.#', '.##', '###', '###'], 'num': {1: (2, 2), 2: (0, 0), 3: (3, 1), 4: (2, 0)}}}


def stands(row): return row[1] == '#' or (row[0] == '#' and row[2] == '#')


def safe(layers, li, pos, rule=stands):
    assert layers[li][pos] == '#' and li < len(layers) - 1
    new = layers[li][:pos] + '.' + layers[li][pos + 1:]
    return all(rule(r) for r in layers[:li] + [new] + layers[li + 1:])


def pick(k, rule=stands):
    b = BOARDS[k]; assert all(stands(r) for r in b['layers'])
    ok = [n for n, (li, p) in b['num'].items() if safe(b['layers'], li, p, rule)]
    return ok


RES = {k: pick(k) for k in 'ABCD'}
assert all(len(v) == 1 for v in RES.values()), RES
code = ''.join(str(RES[k][0]) for k in 'ABCD')
TR = {k: [n for n, (li, p) in BOARDS[k]['num'].items() if p == 1] for k in 'ABCD'}
assert all(len(v) == 1 for v in TR.values()); trap = ''.join(str(TR[k][0]) for k in 'ABCD')
print('answer', code, 'trap', trap)
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
assert sols == ['3142'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'safe': RES, 'trap_middle_block': trap,
               'why': '한 층은 가운데 블록이 있거나 양쪽 끝 두 개가 있어야 버텨요. 한쪽 끝만 남으면 기울어 무너져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
