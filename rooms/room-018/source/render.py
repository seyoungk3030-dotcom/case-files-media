import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 18, '2026.10.17', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS, MEMO = '1649', '3861'
CLUES = ['① 메모는 진짜 암호의 모든 자리를', '    같은 수(1~9)만큼 앞으로 민 것', '② 진짜 암호에 0은 없다', '③ 진짜 암호의 네 숫자 합은 20', '④ 진짜 암호는 홀수']


def memo(d, y, digits=MEMO, label='도윤의 메모', col=YEL, size=150):
    x0 = (W - size * 4) // 2
    f = F('Bold', 30); d.text(((W - d.textlength(label, font=f)) / 2, y - 50), label, font=f, fill=GRAY)
    for i, ch in enumerate(digits):
        cell(d, x0 + i * size, y, size, ch, col=col, fs=80)
    return y + size


def ring(d, y, hl=None):
    """0-9 strip showing that 9 wraps to 0."""
    size = 80; x0 = (W - size * 11) // 2
    for i in range(11):
        n = i % 10
        out = (hl or {}).get(i)
        d.rounded_rectangle([x0 + i * size + 4, y, x0 + (i + 1) * size - 4, y + 72], radius=12, fill=CELL,
                            outline=out or CELL_LINE, width=4 if out else 2)
        f = F('Bold', 36); s = str(n)
        d.text((x0 + i * size + size / 2 - d.textlength(s, font=f) / 2, y + 12), s, font=f, fill=WHITE if i < 10 else MINT)
    f = F('SemiBold', 26); s = '9 다음은 다시 0'
    d.text((x0 + 11 * size - d.textlength(s, font=f), y + 86), s, font=f, fill=MINT)
    return y + 120


def card1():
    im, d = base(ROOM, DATE, 1, N, '밀려 적힌 메모', '금고 옆 포스트잇의 숫자는 가짜였다.')
    bottom = memo(d, 380)
    lines(d, 80, bottom + 60, ['도윤은 암호를 그대로 적지 않았다.', '모든 자리를 똑같은 수만큼 밀어서 적었다.', '',
                               ('진짜 암호는 몇일까?', MINT)], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '미는 규칙', '네 자리 모두 같은 수만큼 앞으로.')
    ring(d, 300)
    d.text((100, 480), '예시 · 2만큼 밀기', font=F('Bold', 34), fill=YEL)
    lines(d, 100, 540, ['1 2 3 4  →  3 4 5 6', '7 8 9 5  →  9 0 1 7', '', ('8, 9는 한 바퀴 돌아 0, 1이 돼요.', MINT)], size=38, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '메모를 거꾸로 되돌리기', '메모에서 같은 수만큼 빼면 진짜 암호.')
    memo(d, 360, label='메모')
    d.text((W / 2 - 20, 520), '↓', font=F('Bold', 60), fill=MINT)
    memo(d, 650, digits='????', label='진짜 암호 (몇 칸 밀었을까?)', col=DIM)
    lines(d, 80, 860, ['밀 수 있는 수는 1부터 9까지 아홉 가지.', ('단서로 아홉 후보를 하나로 줄이세요.', MINT)], size=34, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '메모 3861 · 9 다음은 0.')
    memo(d, 330, size=130)
    d.rounded_rectangle([66, 520, 1014, 900], radius=24, fill=PANEL, outline=YEL, width=3)
    for i, c in enumerate(CLUES):
        d.text((100, 550 + i * 66), c, font=F('Bold', 34), fill=WHITE)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 후보는 아홉 개뿐', '1칸부터 9칸까지 하나씩 되돌려 보세요.', subcol=CORAL)
    rows = [('1칸', '2750'), ('2칸', '1649'), ('3칸', '0538'), ('4칸', '9427'), ('5칸', '8316')]
    for i, (k, c) in enumerate(rows):
        y = 290 + i * 80
        d.text((140, y + 10), k, font=F('Bold', 34), fill=YEL)
        d.text((320, y + 4), ' '.join(c), font=F('Black', 44), fill=WHITE)
    lines(d, 140, 700, ['… 6칸 · 7칸 · 8칸 · 9칸도 같은 방법으로.'], size=32, col=GRAY)
    lines(d, 80, 800, ['0이 있는 후보부터 지우고, 합이 20인 걸 찾으면', '후보가 둘 남아요.', ('6194? 마지막 단서 ④를 확인하세요!', CORAL)], size=33, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


ALL = [(1, '2750'), (2, '1649'), (3, '0538'), (4, '9427'), (5, '8316'), (6, '7205'), (7, '6194'), (8, '5083'), (9, '4972')]


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '도윤은 2칸씩 밀어서 적었습니다.')
    d.text((110, 280), '밀기', font=F('Bold', 26), fill=YEL)
    d.text((260, 280), '진짜 후보', font=F('Bold', 26), fill=YEL)
    d.text((560, 280), '0 없음 · 합 20 · 홀수', font=F('Bold', 26), fill=YEL)
    for i, (k, c) in enumerate(ALL):
        y = 324 + i * 64
        s = sum(map(int, c)); ok0 = '0' not in c; ok20 = s == 20; odd = int(c[-1]) % 2 == 1
        hit = ok0 and ok20 and odd
        d.rounded_rectangle([66, y, 1014, y + 56], radius=12, fill=PANEL, outline=MINT if hit else CELL_LINE, width=3 if hit else 1)
        d.text((110, y + 10), f'{k}칸', font=F('Bold', 30), fill=WHITE if hit else GRAY)
        d.text((260, y + 6), ' '.join(c), font=F('Black', 36), fill=MINT if hit else GRAY)
        marks = ['✓' if ok0 else '✗', '✓' if ok20 else '✗', '✓' if odd else '✗'] if ok0 else ['✗', '', '']
        for j, m in enumerate(marks):
            d.text((600 + j * 120, y + 8), m, font=F('Bold', 32), fill=MINT if m == '✓' else (CORAL if m == '✗' else GRAY))
    lines(d, 76, 920, ['0 없고 합이 20인 건 6194와 1649.', '그중 홀수는 1649 하나뿐!'], size=33)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '2칸 되돌리면 열리는 금고', '네 단서가 모두 1649를 가리켰습니다.')
    memo(d, 330, size=130, label='메모 3861')
    d.text((W / 2 - 60, 470), '↓ 2칸', font=F('Bold', 40), fill=MINT)
    big_answer(d, 540, ANS)
    lines(d, 80, 780, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '6194에 속았다면 댓글로 자수하기'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
