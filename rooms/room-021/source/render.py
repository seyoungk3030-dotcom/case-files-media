import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 21, '2026.10.18', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '4318'
NET = {(0, 0): 3, (0, 1): 8, (1, 1): 5, (1, 2): 1, (1, 3): 6, (2, 3): 4}
MARK = {(0, 1): 'A', (1, 2): 'B', (0, 0): 'C', (2, 3): 'D'}
PAIR = {1: MINT, 3: MINT, 4: YEL, 8: YEL, 5: CORAL, 6: CORAL}


def net(d, top, size=150, cells=NET, marks=MARK, hl=None, pairs=False, cols=4):
    x0 = (W - size * cols) // 2
    for (r, c), v in cells.items():
        x, y = x0 + c * size, top + r * size
        col = PAIR[v] if pairs else None
        out = (hl or {}).get((r, c)) or col
        d.rectangle([x, y, x + size, y + size], fill=CELL, outline=CELL_LINE, width=3)
        if out: d.rectangle([x + 7, y + 7, x + size - 7, y + size - 7], outline=out, width=6)
        f = F('Bold', int(size * 0.44)); s = str(v)
        d.text((x + size / 2 - d.textlength(s, font=f) / 2, y + size / 2 - size * 0.3), s, font=f,
               fill=col or WHITE)
        m = marks.get((r, c)) if marks else None
        if m: d.text((x + 20, y + 15), m, font=F('Bold', int(size * 0.2)), fill=YEL)
    return top + 3 * size


def card1():
    im, d = base(ROOM, DATE, 1, N, '접히지 않은 주사위', '전개도 한 장, 숫자 여섯 개.')
    bottom = net(d, 300, size=150)
    lines(d, 80, bottom + 50, ['금고 위에 정육면체 전개도가 놓여 있다.', '접었을 때 마주 보는 면이 암호를 쥐고 있다.'], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '전개도의 규칙', '접는 선을 따라 접으면 정육면체.')
    d.rounded_rectangle([66, 290, 1014, 545], radius=24, fill=PANEL)
    lines(d, 110, 325, ['① 여섯 칸이 정육면체의 여섯 면이 된다', '② 서로 마주 보는 두 면이 「맞은편」', '③ 칸을 자르거나 겹치지 않는다'],
          size=35, w='Bold', gap=1.75)
    d.text((100, 600), '예시', font=F('Bold', 34), fill=YEL)
    ex = {(0, 0): 'a', (0, 1): 'b', (0, 2): 'c'}
    x0 = 120; s = 90
    for (r, c), v in ex.items():
        d.rectangle([x0 + c * s, 660, x0 + c * s + s, 660 + s], fill=CELL, outline=CELL_LINE, width=3)
        f = F('Bold', 40); d.text((x0 + c * s + s / 2 - d.textlength(v, font=f) / 2, 680), v, font=f, fill=WHITE)
    lines(d, 440, 668, ['한 줄로 이어진 세 칸에서', '양 끝 a와 c는 맞은편이 된다.'], size=32)
    lines(d, 100, 800, [('그런데 줄에서 꺾여 나간 칸은?', MINT)], size=34)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호 = 맞은편 숫자', 'A → B → C → D 순서로.')
    bottom = net(d, 300, size=130)
    lines(d, 80, bottom + 50, ['노란 글자 A · B · C · D가 적힌 칸을 보고', '접었을 때 그 칸의 맞은편 면 숫자를 적으세요.',
                               ('A칸 숫자가 아니라, A의 맞은편 숫자!', MINT)], size=33, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '규칙과 단서는 이것이 전부.')
    bottom = net(d, 290, size=140)
    d.rounded_rectangle([66, bottom + 40, 1014, bottom + 270], radius=22, fill=PANEL)
    lines(d, 96, bottom + 66, ['전개도를 접어 정육면체를 만든다', '암호 = A, B, C, D칸 각각의 맞은편 숫자',
                               '숫자는 면마다 하나, 모두 다르다', ('A → B → C → D 순서로 네 자리', YEL)], size=31, w='SemiBold', gap=1.5)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 가운데 줄부터', '5 · 1 · 6은 한 줄로 이어진 세 칸.', subcol=CORAL)
    bottom = net(d, 290, size=140, hl={(1, 1): CORAL, (1, 3): CORAL})
    lines(d, 80, bottom + 40, ['5와 6은 양 끝이라 서로 맞은편.', '8과 4는 그 줄의 위아래 뚜껑이 된다.',
                               ('그럼 8 옆에 꺾여 붙은 3은 어디로 갈까?', CORAL)], size=33, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '맞은편 짝: 5-6 · 8-4 · 3-1.')
    bottom = net(d, 280, size=130, pairs=True)
    lines(d, 76, bottom + 40, ['5 · 1 · 6 줄이 띠처럼 감기고, 8과 4가 양쪽 뚜껑.', '3은 띠의 남은 한 면을 채워 1의 맞은편.',
                               'A(8)→4, B(1)→3, C(3)→1, D(4)→8.'], size=31)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '접으면 보이는 맞은편', '같은 색끼리 마주 봅니다.')
    bottom = net(d, 280, size=115, pairs=True)
    big_answer(d, bottom + 40, ANS)
    lines(d, 80, bottom + 220, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '종이 없이 머릿속으로 접었다면 댓글로 자랑해 주세요.'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
