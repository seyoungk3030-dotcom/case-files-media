import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 27, '2026.10.20', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '6285'
WALLS = [((0, 0), (1, 0)), ((0, 2), (0, 3)), ((1, 3), (2, 3)), ((3, 3), (3, 4))]
TILES = {(1, 3): 6, (4, 1): 2, (1, 1): 8, (3, 3): 5}
ROUTE = [(0, 0), (0, 1), (0, 2), (1, 2), (1, 3), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0),
         (3, 0), (2, 0), (1, 0), (1, 1), (2, 1), (3, 1), (3, 2), (3, 3), (2, 3), (2, 2)]


def floor(d, top, size=124, upto=0, hl=None, badges=False, dim_tiles=False):
    """upto: draw the route through its first `upto` cells; hl: {(r,c): color} outlines; badges: order circles on tiles."""
    x0 = (W - size * 5) // 2
    ctr = lambda rc: (x0 + rc[1] * size + size / 2, top + rc[0] * size + size / 2)
    for r in range(5):
        for c in range(5):
            x, y = x0 + c * size, top + r * size
            d.rectangle([x, y, x + size, y + size], fill=CELL, outline=CELL_LINE, width=2)
            if (r, c) in (hl or {}):
                d.rectangle([x + 6, y + 6, x + size - 6, y + size - 6], outline=hl[(r, c)], width=5)
    if upto > 1:
        pts = [ctr(p) for p in ROUTE[:upto]]
        d.line(pts, fill=MINT, width=12, joint='curve')
    sx, sy = ctr((0, 0)); ex, ey = ctr((2, 2))
    d.ellipse([sx - 34, sy - 34, sx + 34, sy + 34], fill=PANEL, outline=WHITE, width=4)
    f = F('Bold', 24); s = '출발'; d.text((sx - d.textlength(s, font=f) / 2, sy - 15), s, font=f, fill=WHITE)
    d.rounded_rectangle([ex - 40, ey - 34, ex + 40, ey + 34], radius=12, fill=PANEL, outline=MINT, width=4)
    s = '충전'; d.text((ex - d.textlength(s, font=f) / 2, ey - 15), s, font=f, fill=MINT)
    for (r, c), v in TILES.items():
        cx, cy = ctr((r, c))
        d.rounded_rectangle([cx - 36, cy - 36, cx + 36, cy + 36], radius=12, fill=PANEL, outline=DIM if dim_tiles else YEL, width=4)
        f = F('Black', 50); s = str(v)
        d.text((cx - d.textlength(s, font=f) / 2, cy - 33), s, font=f, fill=DIM if dim_tiles else YEL)
    if badges:
        k = 0
        for p in ROUTE:
            if p in TILES:
                k += 1; cx, cy = ctr(p); bx, by = cx + size / 2 - 22, cy - size / 2 + 22
                d.ellipse([bx - 18, by - 18, bx + 18, by + 18], fill=MINT)
                f = F('Bold', 24); s = str(k); d.text((bx - d.textlength(s, font=f) / 2, by - 15), s, font=f, fill=BG)
    for a, b in WALLS:
        (r1, c1), (r2, c2) = a, b
        if r1 == r2:
            x = x0 + max(c1, c2) * size; y = top + r1 * size
            d.rectangle([x - 7, max(top, y - 4), x + 7, min(top + 5 * size, y + size + 4)], fill=CORAL)
        else:
            y = top + max(r1, r2) * size; x = x0 + c1 * size
            d.rectangle([max(x0, x - 4), y - 7, min(x0 + 5 * size, x + size + 4), y + 7], fill=CORAL)
    d.rectangle([x0, top, x0 + 5 * size, top + 5 * size], outline=GRAY, width=4)
    return top + 5 * size


def mini(d, x0, top, rows, cols, size, route, tiles=None, walls=(), hl=None):
    """Small example grid: route is a list of (r,c); tiles {(r,c): digit}; walls [((r,c),(r,c))]."""
    ctr = lambda rc: (x0 + rc[1] * size + size / 2, top + rc[0] * size + size / 2)
    for r in range(rows):
        for c in range(cols):
            x, y = x0 + c * size, top + r * size
            d.rectangle([x, y, x + size, y + size], fill=CELL, outline=CELL_LINE, width=2)
            if (r, c) in (hl or {}): d.rectangle([x + 5, y + 5, x + size - 5, y + size - 5], outline=hl[(r, c)], width=5)
    if len(route) > 1: d.line([ctr(p) for p in route], fill=MINT, width=10, joint='curve')
    for (r, c), v in (tiles or {}).items():
        cx, cy = ctr((r, c))
        d.rounded_rectangle([cx - 30, cy - 30, cx + 30, cy + 30], radius=10, fill=PANEL, outline=YEL, width=4)
        f = F('Black', 40); t = str(v); d.text((cx - d.textlength(t, font=f) / 2, cy - 27), t, font=f, fill=YEL)
    for (r1, c1), (r2, c2) in walls:
        if r1 == r2:
            x = x0 + max(c1, c2) * size; y = top + r1 * size; d.rectangle([x - 6, y, x + 6, y + size], fill=CORAL)
        else:
            y = top + max(r1, r2) * size; x = x0 + c1 * size; d.rectangle([x, y - 6, x + size, y + 6], fill=CORAL)
    d.rectangle([x0, top, x0 + cols * size, top + rows * size], outline=GRAY, width=3)


def card1():
    im, d = base(ROOM, DATE, 1, N, '로봇 청소기의 마지막 경로', '지나간 순서대로 숫자를 주우면 암호.')
    bottom = floor(d, 280)
    lines(d, 80, bottom + 30, ['출발한 로봇이 모든 칸을 딱 한 번씩 청소하고', '가운데 충전기에서 멈췄다. 빨간 선은 벽.',
                               ('노란 숫자를 지나간 순서대로 이으면 금고 암호.', MINT)], size=32, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '로봇의 규칙', '이 규칙은 항상 지켜집니다.')
    d.rounded_rectangle([66, 280, 1014, 600], radius=24, fill=PANEL)
    lines(d, 106, 306, ['① 위 · 아래 · 왼쪽 · 오른쪽으로 한 칸씩 이동', '② 모든 칸을 정확히 한 번씩 지나감',
                        '③ 빨간 벽은 통과할 수 없음', '④ 출발 칸에서 시작해 충전기에서 끝'], size=33, w='Bold', gap=1.72)
    d.text((100, 640), '예시', font=F('Bold', 34), fill=YEL)
    mini(d, 100, 700, 3, 3, 100, [(1, 0), (0, 0), (0, 1)], hl={(0, 0): YEL})
    lines(d, 440, 720, ['구석 칸은 나가는 길이 두 개뿐.', '들어오고 나가려면', ('두 길을 모두 써야 해요.', MINT),
                        '(출발 · 충전기 칸은 예외)'], size=32, w='Bold')
    lines(d, 100, 1030, ['대각선 이동은 없고, 지나간 칸은 다시 못 가요.'], size=32)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호는 지나간 순서대로', '왼쪽 위부터 읽는 순서가 아니에요.')
    d.text((100, 300), '예시 · 2×4 바닥', font=F('Bold', 34), fill=YEL)
    mini(d, 190, 370, 2, 4, 175, [(0, 0), (1, 0), (1, 1), (0, 1), (0, 2), (1, 2), (1, 3), (0, 3)], tiles={(0, 1): 7, (1, 0): 3})
    lines(d, 80, 760, ['왼쪽 위부터 읽으면 7 → 3이지만,', '로봇은 3을 먼저 지나가요.', ('그래서 이 예시의 암호는 37.', MINT),
                       '네 숫자를 지나간 순서로 이으세요.'], size=32, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '모든 칸을 한 번씩 · 벽은 통과 불가 · 끝은 충전기.')
    bottom = floor(d, 280, size=132)
    lines(d, 80, bottom + 30, ['출발에서 충전기까지 가는 길은 단 하나.', '노란 숫자를 지나간 순서대로 이으세요.'], size=33, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 막다른 칸부터', '길이 두 개뿐인 칸은 두 길을 다 씁니다.', subcol=CORAL)
    bottom = floor(d, 280, size=120, hl={(0, 2): CORAL, (0, 3): CORAL, (0, 4): CORAL})
    lines(d, 80, bottom + 30, ['출발 칸 아래는 벽 → 첫 이동은 오른쪽.', '윗줄 3번째 칸은 벽 때문에 아래로만 나갈 수 있어요.',
                               ('오른쪽 위 구석은? 함정: 왼쪽 위부터 읽은 8652!', CORAL)], size=31, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '6 → 2 → 8 → 5 순서로 지나갑니다.')
    bottom = floor(d, 270, size=124, upto=25, badges=True)
    lines(d, 70, bottom + 26, ['출발 → 오른쪽 → 벽 앞에서 아래로 내려가 6.', '오른쪽 위 구석을 돌아 테두리를 크게 한 바퀴 → 2.',
                               '왼쪽 줄을 올라와 안쪽 8 → 5 → 충전기.'], size=31)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '충전기에 도착한 로봇', '벽 네 개로 길이 딱 하나만 남았습니다.')
    bottom = floor(d, 270, size=112, upto=25, badges=True)
    big_answer(d, bottom + 20, ANS)
    lines(d, 80, bottom + 210, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '몇 초 걸렸는지 댓글로 알려주세요.'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
