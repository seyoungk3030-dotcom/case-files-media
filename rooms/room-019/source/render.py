import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 19, '2026.10.17', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '1344'
GIVEN = {(0, 1): 3, (0, 3): 2, (1, 2): 1, (2, 0): 2, (3, 1): 1, (3, 2): 2}
STAR = {(0, 0): 'A', (1, 3): 'B', (2, 1): 'C', (3, 3): 'D'}
SOL = [(1, 3, 4, 2), (4, 2, 1, 3), (2, 4, 3, 1), (3, 1, 2, 4)]


def board(d, top, size=130, fill=None, hl=None, solved=False):
    """fill: {(r,c): value} extra numbers in mint; hl: {(r,c): color} outlines."""
    x0 = (W - size * 4) // 2
    for r in range(4):
        for c in range(4):
            x, y = x0 + c * size, top + r * size
            star = STAR.get((r, c))
            out = (hl or {}).get((r, c)) or (YEL if star else None)
            d.rectangle([x, y, x + size, y + size], fill=CELL, outline=CELL_LINE, width=2)
            if out: d.rectangle([x + 6, y + 6, x + size - 6, y + size - 6], outline=out, width=5)
            v, col = None, WHITE
            if (r, c) in GIVEN: v = GIVEN[(r, c)]
            elif solved: v, col = SOL[r][c], (MINT if star else GRAY)
            elif fill and (r, c) in fill: v, col = fill[(r, c)], MINT
            if star: d.text((x + 14, y + 8), star, font=F('Bold', 28), fill=YEL)
            if v is not None:
                f = F('Bold', 64); s = str(v)
                d.text((x + size / 2 - d.textlength(s, font=f) / 2, y + size / 2 - 42), s, font=f, fill=col)
    for k in range(0, 5, 2):
        d.line([x0 + k * size, top, x0 + k * size, top + 4 * size], fill=GRAY, width=6)
        d.line([x0, top + k * size, x0 + 4 * size, top + k * size], fill=GRAY, width=6)
    return top + 4 * size


def card1():
    im, d = base(ROOM, DATE, 1, N, '4×4 숫자 금고', '숫자 여섯 개만 남은 금고 문.')
    bottom = board(d, 290)
    lines(d, 80, bottom + 40, ['금고 문에 4×4 숫자판이 붙어 있다.', '노란 칸 A · B · C · D의 숫자가 곧 암호.'], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '숫자판의 규칙', '이 규칙은 항상 지켜집니다.')
    d.rounded_rectangle([66, 290, 1014, 580], radius=24, fill=PANEL)
    lines(d, 110, 325, ['① 모든 가로줄에 1 · 2 · 3 · 4가 한 번씩', '② 모든 세로줄에 1 · 2 · 3 · 4가 한 번씩', '③ 굵은 선 2×2 칸에도 1~4가 한 번씩'],
          size=36, w='Bold', gap=1.75)
    d.text((100, 640), '예시', font=F('Bold', 34), fill=YEL)
    lines(d, 100, 700, ['가로줄이 3 _ 1 4 라면 빈칸은 2.', '', ('미니 스도쿠예요. 여섯 숫자면 충분합니다!', MINT)], size=34)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호는 A → B → C → D', '노란 칸의 숫자를 순서대로.')
    board(d, 300, size=110)
    lines(d, 80, 790, ['A는 맨 윗줄, D는 맨 아랫줄에 있어요.', '네 칸만 채워도 되지만,', ('판 전체를 채우면 실수가 없어요.', MINT)], size=34, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '가로 · 세로 · 2×2 칸에 1~4가 한 번씩.')
    bottom = board(d, 290, size=140)
    lines(d, 80, bottom + 40, ['노란 칸 A → B → C → D의 숫자를 이으세요.'], size=34, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 맨 윗줄부터', '윗줄의 빈칸은 1과 4 두 개뿐.', subcol=CORAL)
    bottom = board(d, 290, size=120, hl={(0, 2): CORAL, (1, 2): CORAL})
    lines(d, 80, bottom + 30, ['세 번째 세로줄에는 이미 1이 있다.', '→ 윗줄 세 번째 칸은 4, 그러니 A는?',
                               ('2×2 칸 규칙도 잊지 마세요!', CORAL)], size=33, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', 'A=1, B=3, C=4, D=4.')
    bottom = board(d, 280, size=120, solved=True)
    lines(d, 76, bottom + 30, ['윗줄: 세 번째 열에 1이 있으니 1 3 4 2 → A=1.', '둘째 줄 첫 칸은 4 → 아랫줄 첫 칸 3 → D=4.',
                               '나머지도 가로 · 세로 · 2×2로 채우면 B=3, C=4.'], size=31)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '숫자판을 채우면 열리는 금고', '여섯 숫자만으로 판 전체가 정해졌습니다.')
    bottom = board(d, 280, size=110, solved=True)
    big_answer(d, bottom + 20, ANS)
    lines(d, 80, bottom + 200, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '몇 초 걸렸는지 댓글로 알려주세요.'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
