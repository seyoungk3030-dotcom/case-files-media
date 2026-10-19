import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 25, '2026.10.19', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '1213'
CLUES = {('L', 0): 3, ('L', 2): 2, ('L', 3): 2, ('B', 2): 1, ('B', 3): 2}
STAR = {(0, 0): 'A', (1, 1): 'B', (2, 2): 'C', (3, 3): 'D'}
SOL = [(1, 3, 2, 4), (4, 2, 3, 1), (3, 4, 1, 2), (2, 1, 4, 3)]


def board(d, top, size=120, fill=None, hl=None, clue_hl=None, solved=False):
    """fill: {(r,c): value} in mint; hl: {(r,c): color} outlines; clue_hl: {key: color}."""
    x0 = (W - size * 4) // 2 + size // 4
    for r in range(4):
        for c in range(4):
            x, y = x0 + c * size, top + r * size
            star = STAR.get((r, c))
            out = (hl or {}).get((r, c)) or (YEL if star else None)
            d.rectangle([x, y, x + size, y + size], fill=CELL, outline=CELL_LINE, width=2)
            if out: d.rectangle([x + 6, y + 6, x + size - 6, y + size - 6], outline=out, width=5)
            v, col = None, MINT
            if solved: v, col = SOL[r][c], (MINT if star else GRAY)
            elif fill and (r, c) in fill: v = fill[(r, c)]
            if star: d.text((x + 12, y + 8), star, font=F('Bold', int(size * 0.2)), fill=YEL)
            if v is not None:
                f = F('Bold', int(size * 0.48)); s = str(v)
                d.text((x + size / 2 + (size * 0.06 if star else 0) - d.textlength(s, font=f) / 2, y + size / 2 - size * 0.31), s, font=f, fill=col)
    f = F('Bold', int(size * 0.42))
    for (side, i), v in CLUES.items():
        col = (clue_hl or {}).get((side, i), WHITE)
        if side == 'L': cx, cy = x0 - size * 0.45, top + i * size + size / 2
        else: cx, cy = x0 + i * size + size / 2, top + 4 * size + size * 0.45
        s = str(v)
        d.text((cx - d.textlength(s, font=f) / 2, cy - size * 0.29), s, font=f, fill=col)
    return top + 4 * size + int(size * 0.9)


def skyline(d, x, top, heights, unit=34, wcell=110, seen=()):
    """Side view of one row: bars of height h*unit standing on a common ground line."""
    ground = top + 4 * unit
    for k, h in enumerate(heights):
        bx = x + k * wcell
        col = MINT if k in seen else DIM
        d.rectangle([bx + 14, ground - h * unit, bx + wcell - 14, ground], fill=col)
        s = str(h); f = F('Bold', 34)
        d.text((bx + wcell / 2 - d.textlength(s, font=f) / 2, ground + 10), s, font=f, fill=WHITE)
    d.line([x, ground, x + 4 * wcell, ground], fill=GRAY, width=3)
    return ground + 60


def card1():
    im, d = base(ROOM, DATE, 1, N, '빌딩 숲의 암호', '가장자리 숫자 다섯 개만 남은 도시 모형.')
    bottom = board(d, 280)
    lines(d, 80, bottom + 10, ['4×4 도시 모형, 칸마다 1~4층 빌딩이 하나씩.', '바깥 숫자는 그쪽에서 보이는 빌딩 수.',
                               '노란 칸 A · B · C · D의 층수가 곧 암호.'], size=33, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '도시 모형의 규칙', '이 규칙은 항상 지켜집니다.')
    d.rounded_rectangle([66, 280, 1014, 520], radius=24, fill=PANEL)
    lines(d, 106, 308, ['① 가로줄 · 세로줄마다 1 · 2 · 3 · 4층이 한 번씩', '② 높은 빌딩 뒤의 낮은 빌딩은 가려져 안 보임',
                        '③ 바깥 숫자 = 그 방향에서 보이는 빌딩 수'], size=33, w='Bold', gap=1.75)
    d.text((100, 560), '예시 · 왼쪽에서 본 가로줄 2 1 4 3', font=F('Bold', 33), fill=YEL)
    y = skyline(d, 320, 630, [2, 1, 4, 3], seen=(0, 2))
    d.text((130, 690), '보임', font=F('Bold', 34), fill=MINT)
    d.text((200, 740), '2', font=F('Bold', 64), fill=MINT)
    lines(d, 100, y + 10, ['2층과 4층만 보이고 1층 · 3층은 가려져요.', ('그래서 왼쪽 숫자는 2.', MINT)], size=33)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호는 A → B → C → D', '대각선 노란 칸의 층수를 순서대로.')
    bottom = board(d, 300, size=110)
    lines(d, 80, bottom + 10, ['A는 왼쪽 위, D는 오른쪽 아래 칸.', '숫자가 없는 방향은 단서가 없는 것뿐,',
                               ('규칙 ①은 모든 줄에 적용돼요.', MINT)], size=33, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '줄마다 1~4층 한 번씩 · 바깥 숫자 = 보이는 수.')
    bottom = board(d, 280, size=135)
    lines(d, 80, bottom, ['왼쪽 숫자는 왼쪽에서, 아래 숫자는 아래에서 본 수.', '노란 칸 A → B → C → D의 층수를 이으세요.'], size=32, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 4층부터 찾기', '빌딩이 1개만 보인다면?', subcol=CORAL)
    bottom = board(d, 280, size=120, fill={(3, 2): 4}, hl={(3, 2): CORAL}, clue_hl={('B', 2): CORAL})
    lines(d, 80, bottom + 10, ['아래에서 1개만 보이면 맨 앞이 4층이라는 뜻.', '4층은 낮은 빌딩을 모두 가리니, 위치를 먼저!',
                               ('윗줄 왼쪽 3: 4층이 1 · 2번째 칸일 순 없어요.', CORAL)], size=32, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', 'A=1, B=2, C=1, D=3.')
    bottom = board(d, 275, size=125, solved=True)
    lines(d, 70, bottom + 5, ['4층 위치: 아랫줄 3번 → 윗줄 4번 · 셋째 줄 2번 · 둘째 줄 1번.', '오른쪽 세로줄 아래 2 → 맨 아래 칸 3 → 아랫줄 2 1 4 3.',
                              '윗줄 왼쪽 3 → 1 3 2 4. 나머지는 줄마다 1~4로 채우기.'], size=30)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '불이 켜진 빌딩 숲', '단서 다섯 개로 도시 전체가 정해졌습니다.')
    bottom = board(d, 275, size=115, solved=True)
    big_answer(d, bottom - 10, ANS)
    lines(d, 80, bottom + 170, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '몇 초 걸렸는지 댓글로 알려주세요.'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
