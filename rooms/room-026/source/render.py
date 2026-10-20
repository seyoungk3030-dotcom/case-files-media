import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 26, '2026.10.20', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '3142'
CLUES = ['① 레몬에이드는 1번 자리', '② 도윤은 끝자리', '③ 녹차는 도윤 바로 옆자리',
         '④ 유나는 레몬에이드', '⑤ 라떼는 4번 자리', '⑥ 유나는 서진의 바로 왼쪽']
SOLVED = {1: ('유나', '레몬에이드'), 2: ('서진', '아메리카노'), 3: ('민재', '녹차'), 4: ('도윤', '라떼')}


def seats(d, top, info=None, hl=None, sw=200):
    """Window band, bar counter and four seats. info: {seat: (name, drink)} (either may be None); hl: {seat: color}."""
    gap = 24; x0 = (W - (4 * sw + 3 * gap)) // 2
    d.rounded_rectangle([x0 - 20, top, x0 + 4 * sw + 3 * gap + 20, top + 46], radius=10, fill=(30, 58, 84))
    for k in (1, 2, 3, 5, 6, 7):
        xx = x0 - 20 + k * (4 * sw + 3 * gap + 40) / 8
        d.line([xx, top + 6, xx, top + 40], fill=(52, 86, 116), width=3)
    f = F('SemiBold', 22); s = '창가'
    d.text((x0 + 2 * sw + 1.5 * gap - d.textlength(s, font=f) / 2, top + 10), s, font=f, fill=GRAY)
    d.rectangle([x0 - 20, top + 62, x0 + 4 * sw + 3 * gap + 20, top + 78], fill=DASH)
    for i in range(4):
        n = i + 1; x = x0 + i * (sw + gap); y = top + 100
        out = (hl or {}).get(n, CELL_LINE)
        d.rounded_rectangle([x, y, x + sw, y + 210], radius=22, fill=CELL, outline=out, width=5 if n in (hl or {}) else 2)
        f = F('Black', 44); s = str(n)
        d.text((x + sw / 2 - d.textlength(s, font=f) / 2, y + 14), s, font=f, fill=YEL)
        name, drink = (info or {}).get(n, (None, None))
        f = F('Bold', 38); s = name or '?'
        d.text((x + sw / 2 - d.textlength(s, font=f) / 2, y + 82), s, font=f, fill=MINT if name else DIM)
        f = F('SemiBold', 26); s = drink or ''
        d.text((x + sw / 2 - d.textlength(s, font=f) / 2, y + 148), s, font=f, fill=WHITE)
    return top + 330


def memo(d, top, hot=(), col=CORAL):
    d.rounded_rectangle([66, top, 1014, top + 300], radius=24, fill=PANEL)
    d.text((100, top + 22), '영수증 메모', font=F('Bold', 28), fill=GRAY)
    for i, c in enumerate(CLUES):
        x, y = 100 + (i // 3) * 460, top + 80 + (i % 3) * 66
        d.text((x, y), c, font=F('Bold', 30), fill=col if i in hot else DIM)


def order_row(d, top):
    d.rounded_rectangle([66, top, 1014, top + 190], radius=24, fill=PANEL)
    for i, (nm, n) in enumerate(zip(['민재', '유나', '도윤', '서진'], ANS)):
        cx = 66 + 948 * (2 * i + 1) / 8
        f = F('Bold', 34); d.text((cx - d.textlength(nm, font=f) / 2, top + 30), nm, font=f, fill=WHITE)
        f = F('Black', 60); s = n + '번'
        d.text((cx - d.textlength(s, font=f) / 2, top + 88), s, font=f, fill=MINT)
        if i < 3: d.text((66 + 948 * (i + 1) / 4 - 14, top + 100), '→', font=F('Bold', 36), fill=GRAY)


def card1():
    im, d = base(ROOM, DATE, 1, N, '창가석 네 자리의 영수증', '자리 번호를 이으면 금고 암호.')
    bottom = seats(d, 290)
    lines(d, 80, bottom + 30, ['카페 창가 바에 민재 · 유나 · 도윤 · 서진이 앉았다.', '음료는 네 사람 모두 달랐다.',
                               '남은 건 점원이 영수증에 적은 메모 여섯 줄.', ('네 사람의 자리 번호가 곧 금고 암호.', MINT)], size=33, w='Bold')
    d.text((80, bottom + 290), '음료: 아메리카노 · 라떼 · 녹차 · 레몬에이드', font=F('SemiBold', 30), fill=GRAY)
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '자리 읽는 법', '이 규칙은 항상 지켜집니다.')
    d.rounded_rectangle([66, 280, 1014, 530], radius=24, fill=PANEL)
    lines(d, 106, 308, ['① 자리마다 한 명, 음료도 모두 다름', '② 1번이 가장 왼쪽, 4번이 가장 오른쪽',
                        '③ 끝자리 = 1번 또는 4번'], size=34, w='Bold', gap=1.75)
    d.text((100, 570), '예시', font=F('Bold', 34), fill=YEL)
    seats(d, 630, hl={1: MINT, 3: MINT}, info={2: ('기준', None)})
    lines(d, 100, 980, ['2번의 「바로 옆자리」는 1번과 3번.', '「바로 왼쪽」은 붙어 있는 왼쪽 한 칸만.'], size=33)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호는 민재 → 유나 → 도윤 → 서진', '각자 앉은 자리 번호를 순서대로.')
    d.rounded_rectangle([66, 290, 1014, 640], radius=24, fill=PANEL)
    for i, (nm, k) in enumerate(zip(['민재', '유나', '도윤', '서진'], 'ABCD')):
        x = 110 + i * 225
        d.text((x, 330), k, font=F('Black', 44), fill=YEL)
        d.text((x, 410), nm, font=F('Bold', 44), fill=WHITE)
        d.text((x, 500), '?번', font=F('Bold', 44), fill=DIM)
    lines(d, 80, 700, ['예: 민재 2번, 유나 4번, 도윤 1번, 서진 3번이면', ('암호는 2413.', MINT), '',
                       '음료는 암호에 들어가지 않지만,', '자리를 찾는 데 꼭 필요해요.'], size=34, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '영수증 메모 여섯 줄이 전부입니다.')
    d.rounded_rectangle([66, 280, 1014, 760], radius=24, fill=PANEL)
    lines(d, 110, 312, CLUES, size=36, w='Bold', gap=1.95)
    d.text((110, 800), '음료: 아메리카노 · 라떼 · 녹차 · 레몬에이드', font=F('SemiBold', 32), fill=GRAY)
    lines(d, 110, 880, ['1번이 가장 왼쪽, 4번이 가장 오른쪽.', ('민재 → 유나 → 도윤 → 서진의 자리 번호를 이으세요.', MINT)], size=33, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 유나부터 앉히기', '메모 ①과 ④를 함께 보세요.', subcol=CORAL)
    bottom = seats(d, 290, info={1: ('유나', '레몬에이드')}, hl={1: CORAL})
    lines(d, 80, bottom + 30, ['레몬에이드는 1번, 유나는 레몬에이드 → 유나는 1번.', '그러면 ⑥으로 서진의 자리가 바로 나와요.',
                               ('함정: 끝자리는 1번 또는 4번. 1번은 이미 찼어요!', CORAL)], size=32, w='Bold')
    memo(d, bottom + 200, hot=(0, 3, 5))
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '민재 3번, 유나 1번, 도윤 4번, 서진 2번.')
    bottom = seats(d, 290, info=SOLVED)
    lines(d, 70, bottom + 30, ['①④ 유나 1번 → ⑥ 서진 2번.', '② 도윤은 끝자리, 1번은 찼으니 4번 → 민재 3번.',
                               '③ 녹차는 3번, ⑤ 라떼는 4번 → 아메리카노는 2번.'], size=32)
    order_row(d, bottom + 230)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '영수증이 맞춰진 창가석', '메모 여섯 줄로 네 자리가 모두 정해졌습니다.')
    bottom = seats(d, 290, info=SOLVED)
    order_row(d, bottom + 20)
    big_answer(d, bottom + 240, ANS)
    lines(d, 80, bottom + 430, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '몇 초 걸렸는지 댓글로 알려주세요.'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
