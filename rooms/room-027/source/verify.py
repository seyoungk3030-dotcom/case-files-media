"""ROOM 027 proof: a robot vacuum on a 5x5 floor starts at the top-left cell, moves one cell up/down/left/right at a time,
cleans every cell exactly once and must finish on the centre charger. Thick walls block four moves.
Enumerate every such route, prove exactly one survives the walls and every wall is needed, then read the code from the
four numbered tiles in the order the robot reaches them."""
import json, os
N = 5
START, END = (0, 0), (2, 2)
WALLS = [((0, 0), (1, 0)), ((0, 2), (0, 3)), ((1, 3), (2, 3)), ((3, 3), (3, 4))]
TILES = {(1, 3): 6, (4, 1): 2, (1, 1): 8, (3, 3): 5}


def routes(walls):
    blocked = {frozenset(w) for w in walls}
    out = []

    def go(p, seen):
        r, c = p[-1]
        if len(p) == N * N:
            if p[-1] == END: out.append(tuple(p))
            return
        for b in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= b[0] < N and 0 <= b[1] < N and b not in seen and b != END and frozenset((p[-1], b)) not in blocked:
                seen.add(b); p.append(b); go(p, seen); p.pop(); seen.remove(b)
        if len(p) == N * N - 1 and abs(r - END[0]) + abs(c - END[1]) == 1 and frozenset((p[-1], END)) not in blocked:
            out.append(tuple(p + [END]))

    go([START], {START})
    return out


free = routes([])
match = routes(WALLS)
print(len(free), len(match))
assert len(free) == 48 and len(match) == 1
for w in WALLS:
    assert len(routes([x for x in WALLS if x != w])) > 1, w
path = match[0]
code = ''.join(str(TILES[c]) for c in path if c in TILES)
reading = ''.join(str(TILES[c]) for c in sorted(TILES))
print(path, code, 'reading-order trap', reading)
assert code == '6285' and reading != code
json.dump({'unique_answer': code, 'routes_without_walls': len(free), 'routes_with_walls': 1, 'every_wall_needed': True,
           'route': [f'r{r+1}c{c+1}' for r, c in path], 'tiles': {f'r{r+1}c{c+1}': v for (r, c), v in TILES.items()},
           'reading_order_trap': reading},
          open(os.path.join(os.path.dirname(__file__), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
