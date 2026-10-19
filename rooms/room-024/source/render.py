import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 24, '2026.10.19', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '4251'
REG = ['BBBAA', 'BBBAC', 'BBBBC', 'DDDCC', 'DEEEC']
SOL = [3, 1, 4, 0, 2]
FILL = {'A': (44, 104, 96), 'B': (44, 64, 104), 'C': (118, 76, 56), 'D': (88, 64, 118), 'E': (104, 96, 44)}
NAME = {'A': '청록', 'B': '파랑', 'C': '갈색', 'D': '보라', 'E': '올리브'}
ROWL = ['A', 'B', 'C', 'D', '']


def star(d, cx, cy, R, col=YEL):
    r = R * 0.42
    pts = [(cx + (R if i % 2 == 0 else r) * math.sin(i * math.pi / 5), cy - (R if i % 2 == 0 else r) * math.cos(i * math.pi / 5)) for i in range(10)]
    d.polygon(pts, fill=col)


def grid(d, top, size=120, stars=None, dim=None, labels=True):
    """stars: list of (r,c); dim: set of region letters to keep bright (others faded)."""
    x0 = (W - size * 5) // 2 + (20 if labels else 0)
    if labels:
        for c in range(5):
            f = F('Bold', 28); s = str(c + 1)
            d.text((x0 + c * size + size / 2 - d.textlength(s, font=f) / 2, top - 44), s, font=f, fill=GRAY)
    for r in range(5):
        if labels and ROWL[r]:
            f = F('Bold', 34); d.text((x0 - 50, top + r * size + size / 2 - 22), ROWL[r], font=f, fill=YEL)
        for c in range(5):
            k = REG[r][c]; col = FILL[k]
            if dim and k not in dim: col = tuple(int(v * 0.45 + 18 * 0.55) for v in col)
            d.rectangle([x0 + c * size, top + r * size, x0 + (c + 1) * size, top + (r + 1) * size], fill=col, outline=BG, width=2)
    for r in range(5):
        for c in range(5):
            x, y = x0 + c * size, top + r * size
            if c < 4 and REG[r][c] != REG[r][c + 1]: d.line([x + size, y, x + size, y + size], fill=WHITE, width=6)
            if r < 4 and REG[r][c] != REG[r + 1][c]: d.line([x, y + size, x + size, y + size], fill=WHITE, width=6)
    d.rectangle([x0, top, x0 + 5 * size, top + 5 * size], outline=WHITE, width=6)
    for r, c in (stars or []):
        star(d, x0 + c * size + size / 2, top + r * size + size / 2 + 3, size * 0.36)
    return top + 5 * size


def card1():
    im, d = base(ROOM, DATE, 1, N, '별 다섯 개의 금고', '색칠된 판에 별을 숨겨라.')
    bottom = grid(d, 340, size=118)
    lines(d, 80, bottom + 44, ['금고 문에 다섯 색으로 칠한 5×5 판이 있다.', '규칙대로 별 다섯 개를 놓으면 암호가 보인다.'], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '별 놓기 규칙', '네 가지 규칙을 모두 지킵니다.')
    d.rounded_rectangle([66, 290, 1014, 610], radius=24, fill=PANEL)
    lines(d, 110, 322, ['① 가로줄마다 별이 정확히 1개', '② 세로줄마다 별이 정확히 1개', '③ 같은 색 구역마다 별이 정확히 1개',
                        '④ 별끼리는 닿지 않는다 (대각선도 금지)'], size=34, w='Bold', gap=1.6)
    d.text((100, 660), '예시 · 이렇게 놓으면 안 돼요', font=F('Bold', 32), fill=YEL)
    s = 90; x0 = 120; y0 = 720
    for r in range(2):
        for c in range(2):
            d.rectangle([x0 + c * s, y0 + r * s, x0 + (c + 1) * s, y0 + (r + 1) * s], fill=CELL, outline=CELL_LINE, width=2)
    star(d, x0 + s / 2, y0 + s / 2 + 2, 30); star(d, x0 + 1.5 * s, y0 + 1.5 * s + 2, 30)
    d.line([x0 + 10, y0 + 10, x0 + 2 * s - 10, y0 + 2 * s - 10], fill=CORAL, width=6)
    lines(d, 330, 740, ['대각선으로 맞닿은 별 두 개.', ('④번 규칙 위반!', CORAL)], size=32, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호 = 별의 세로 번호', 'A줄 → B줄 → C줄 → D줄 순서로.')
    bottom = grid(d, 360, size=104)
    lines(d, 80, bottom + 40, ['A~D줄에서 별이 몇 번 세로줄에 있는지 읽으세요.', '예: A줄 별이 2번 칸이면 첫 자리는 2.',
                               ('맨 아랫줄은 확인용이에요.', MINT)], size=33, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '규칙과 단서는 이것이 전부.')
    bottom = grid(d, 330, size=106)
    d.rounded_rectangle([66, bottom + 30, 1014, bottom + 210], radius=22, fill=PANEL)
    lines(d, 96, bottom + 52, ['가로줄 · 세로줄 · 색 구역마다 별 1개씩', '별끼리 닿으면 안 된다 (대각선 포함)',
                               ('암호 = A~D줄 별의 세로줄 번호', YEL)], size=31, w='SemiBold', gap=1.5)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 작은 구역부터', '올리브 · 보라 · 청록 구역을 먼저 보세요.', subcol=CORAL)
    bottom = grid(d, 330, size=106, dim={'D', 'E', 'A'})
    lines(d, 80, bottom + 34, ['올리브 구역은 맨 아랫줄에만 있다 → 5번째 줄 별은 올리브.', '그럼 보라 구역의 별은 어느 줄에 놓일까?',
                               ('청록 구역은 3칸뿐. 별이 들어갈 자리는?', CORAL)], size=31, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', 'A 4번 · B 2번 · C 5번 · D 1번.')
    bottom = grid(d, 330, size=106, stars=list(enumerate(SOL)))
    lines(d, 76, bottom + 30, ['5줄은 올리브, D줄은 보라 → 갈색은 B·C줄의 5번 칸.', '청록이 B줄이면 갈색(C줄)과 대각선으로 닿으니 A줄 4번.',
                               '갈색은 C줄 5번, 파랑은 B줄 2번, 보라 D줄 1번 → 4251.'], size=29, gap=1.5)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '별이 가리킨 암호', '다섯 구역, 다섯 별, 한 가지 답.')
    bottom = grid(d, 330, size=96, stars=list(enumerate(SOL)))
    big_answer(d, bottom + 30, ANS)
    lines(d, 80, bottom + 210, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '어느 색 구역부터 풀었는지 댓글로 알려주세요.'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
