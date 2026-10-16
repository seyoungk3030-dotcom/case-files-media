import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 15, '2026.10.16', 7
OUT = os.path.join(HERE, '..', 'cards')
CLUES = ['① 민재는 가운데 세로줄', '② 유나는 민재 바로 오른쪽 칸', '③ 도윤은 유나 바로 아래 칸',
         '④ 서연은 도윤과 같은 가로줄, 네 모서리 칸 중 하나']
ANS = '5697'
PEOPLE = ['민재', '유나', '도윤', '서연']


def grid(d, top, size=150, owner=None, mark=None, dim=None, corners=False):
    """3x3 lockers 1..9. owner: {n: name} filled mint; mark: {n: color} outline; dim: set of numbers greyed."""
    x0 = (W - size * 3) // 2
    for n in range(1, 10):
        r, c = divmod(n - 1, 3)
        x, y = x0 + c * size, top + r * size
        name = (owner or {}).get(n)
        out = (mark or {}).get(n)
        if corners and n in (1, 3, 7, 9) and not out: out = YEL
        d.rounded_rectangle([x + 8, y + 8, x + size - 8, y + size - 8], radius=14, fill=MINT if name else CELL,
                            outline=out or CELL_LINE, width=5 if out else 2)
        nc = BG if name else (DIM if dim and n in dim else WHITE)
        f = F('Bold', 34 if name else 60); s = str(n)
        if name:
            d.text((x + 22, y + 18), s, font=f, fill=BG)
            f2 = F('Black', 40)
            d.text((x + size / 2 - d.textlength(name, font=f2) / 2, y + size / 2 - 10), name, font=f2, fill=BG)
        else:
            d.text((x + size / 2 - d.textlength(s, font=f) / 2, y + size / 2 - 38), s, font=f, fill=nc)
    return top + 3 * size


def clues(d, y, size=34, x=100, col=WHITE):
    for i, c in enumerate(CLUES):
        d.text((x, y + i * size * 1.55), c, font=F('Bold', size), fill=col)


def card1():
    im, d = base(ROOM, DATE, 1, N, '사물함 네 칸의 주인', '이름표는 떨어지고, 메모 네 줄만 남았다.')
    bottom = grid(d, 290, size=150)
    lines(d, 80, bottom + 40, ['민재 · 유나 · 도윤 · 서연의 사물함 번호를', '순서대로 이으면 금고 암호가 된다.'], size=34, w='Bold')
    lines(d, 80, bottom + 170, [('누가 어느 칸을 쓰고 있을까?', MINT)], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '사물함의 규칙', '이 규칙은 항상 지켜집니다.')
    d.rounded_rectangle([66, 290, 1014, 560], radius=24, fill=PANEL)
    lines(d, 110, 325, ['① 사물함은 1~9번, 3칸씩 세 줄', '② 네 사람은 서로 다른 칸을 하나씩 쓴다', '③ “바로 옆/아래” = 붙어 있는 칸'],
          size=36, w='Bold', gap=1.75)
    d.text((100, 620), '예시', font=F('Bold', 34), fill=YEL)
    lines(d, 100, 680, ['4번의 바로 오른쪽은 5번, 바로 아래는 7번.', '3번의 바로 오른쪽 칸은 없다.', '',
                        ('모서리 칸은 1 · 3 · 7 · 9번 네 개뿐!', MINT)], size=34)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호는 민재 → 유나 → 도윤 → 서연', '네 사람의 사물함 번호를 순서대로.')
    x0 = 120
    for i, p in enumerate(PEOPLE):
        x = x0 + i * 220
        f = F('Bold', 34); d.text((x + 90 - d.textlength(p, font=f) / 2, 300), p, font=f, fill=YEL)
        cell(d, x + 20, 350, 140, '?', col=DIM, fs=64)
    lines(d, 80, 580, ['예를 들어 민재 1번, 유나 2번, 도윤 5번,', '서연 9번이라면', ('암호는 1259', YEL), '',
                       '메모 네 줄을 하나씩 칸에 대 보세요.'], size=36, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '민재 → 유나 → 도윤 → 서연 순서.')
    bottom = grid(d, 280, size=140)
    d.rounded_rectangle([66, bottom + 30, 1014, bottom + 300], radius=24, fill=PANEL, outline=YEL, width=3)
    clues(d, bottom + 58, size=34, x=100)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 민재는 어느 줄?', '가운데 세로줄은 2 · 5 · 8번.', subcol=CORAL)
    bottom = grid(d, 280, size=140, mark={2: CORAL, 5: CORAL, 8: CORAL})
    lines(d, 80, bottom + 40, ['민재가 8번이면 도윤이 들어갈 아랫칸이 없다.', '민재가 2번이면 도윤은 6번, 서연은 4번이나 5번.',
                               ('4번은 모서리가 아니에요! 2364는 함정.', CORAL)], size=32, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '민재 5번, 유나 6번, 도윤 9번, 서연 7번.')
    bottom = grid(d, 280, size=140, owner={5: '민재', 6: '유나', 9: '도윤', 7: '서연'}, dim={1, 2, 3, 4, 8})
    lines(d, 76, bottom + 40, ['민재가 8번이면 아랫칸 없음, 2번이면 서연 자리 없음.', '그래서 민재는 5번 → 유나 6번 → 도윤 9번.',
                               '아랫줄 모서리 중 남은 칸은 7번 → 서연.'], size=32)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '이름표를 되찾은 사물함', '메모 네 줄이 모두 들어맞았습니다.')
    bottom = grid(d, 280, size=130, owner={5: '민재', 6: '유나', 9: '도윤', 7: '서연'}, dim={1, 2, 3, 4, 8})
    big_answer(d, bottom + 20, ANS)
    lines(d, 80, bottom + 200, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '2364에 속았다면 댓글로 자수하기'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
