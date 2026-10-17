import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 17, '2026.10.17', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '7465'
CLUES = ['① 내린 순서: 유나 → 서연 → 도윤 → 민재', '② 민재는 유나보다 정확히 3층 위', '③ 네 사람이 내린 층을 더하면 22']
WHO = {7: '민재', 4: '유나', 6: '도윤', 5: '서연'}


def panel(d, x, top, w=300, owner=None, dim=None):
    """Elevator button panel, floors 9..2 top to bottom in one column."""
    h = 8 * 74 + 40
    d.rounded_rectangle([x, top, x + w, top + h], radius=28, fill=PANEL, outline=CELL_LINE, width=3)
    for i, fl in enumerate(range(9, 1, -1)):
        cy = top + 30 + i * 74 + 30
        name = (owner or {}).get(fl)
        r = 28
        d.ellipse([x + 40, cy - r, x + 40 + 2 * r, cy + r], fill=MINT if name else CELL, outline=MINT if name else CELL_LINE, width=3)
        f = F('Bold', 30); s = str(fl)
        d.text((x + 40 + r - d.textlength(s, font=f) / 2, cy - 20), s, font=f,
               fill=BG if name else (DIM if dim and fl in dim else WHITE))
        if name:
            d.text((x + 130, cy - 22), name, font=F('Bold', 34), fill=MINT)
        else:
            d.text((x + 130, cy - 20), f'{fl}층', font=F('SemiBold', 28), fill=DIM)
    return top + h


def card1():
    im, d = base(ROOM, DATE, 1, N, '엘리베이터 기록지', '네 사람이 각자 다른 층에서 내렸다.')
    bottom = panel(d, 110, 280)
    lines(d, 470, 320, ['퇴근길 엘리베이터.', '1층에서 탄 네 사람이', '위로만 올라가며', '한 명씩 내렸다.', '',
                        ('누가 몇 층에서 내렸을까?', MINT)], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '엘리베이터의 규칙', '이 규칙은 항상 지켜집니다.')
    d.rounded_rectangle([66, 290, 1014, 560], radius=24, fill=PANEL)
    lines(d, 110, 325, ['① 엘리베이터는 위로만 움직인다', '② 네 사람은 2~9층 중 서로 다른 층에서 내림', '③ 먼저 내린 사람일수록 낮은 층'],
          size=36, w='Bold', gap=1.75)
    d.text((100, 620), '예시', font=F('Bold', 34), fill=YEL)
    lines(d, 100, 680, ['A가 3층, B가 5층에서 내렸다면', '내린 순서는 A → B.', '', ('순서만으로는 층을 알 수 없어요!', MINT)], size=34)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호는 민재 → 유나 → 도윤 → 서연', '내린 순서가 아니라 이름 순서!')
    for i, p in enumerate(['민재', '유나', '도윤', '서연']):
        x = 120 + i * 220
        f = F('Bold', 34); d.text((x + 90 - d.textlength(p, font=f) / 2, 300), p, font=f, fill=YEL)
        cell(d, x + 20, 350, 140, '?', col=DIM, fs=64)
    lines(d, 80, 580, ['각자 내린 층 번호를 이 순서대로 붙입니다.', '예: 민재 9층, 유나 2층, 도윤 5층, 서연 3층', ('→ 암호 9253', YEL), '',
                       ('내린 순서대로 적으면 함정에 빠져요.', MINT)], size=34, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '민재 → 유나 → 도윤 → 서연 층 번호.')
    panel(d, 90, 280, w=280)
    lines(d, 410, 300, ['2~9층, 모두 다른 층.', '엘리베이터는 위로만.'], size=30, col=GRAY)
    d.rounded_rectangle([400, 420, 1014, 860], radius=24, fill=PANEL, outline=YEL, width=3)
    clue_lines = [['① 내린 순서', '유나 → 서연 → 도윤 → 민재'], ['② 민재는 유나보다', '정확히 3층 위'], ['③ 네 사람이 내린 층을', '더하면 22']]
    for i, (a, b) in enumerate(clue_lines):
        y = 450 + i * 136
        d.text((430, y), a, font=F('Bold', 32), fill=WHITE)
        d.text((430, y + 48), b, font=F('Bold', 32), fill=MINT)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 사이에 낀 두 사람', '유나와 민재 사이는 딱 3층.', subcol=CORAL)
    d.rounded_rectangle([66, 290, 1014, 590], radius=24, fill=PANEL, outline=CORAL, width=3)
    lines(d, 100, 325, ['유나와 민재 사이에 서연과 도윤이 내렸다.', '3층 차이 안에 두 명이 끼려면?',
                        ('→ 네 사람은 연속된 네 층!', CORAL), '유나 = □, 서연 = □+1, 도윤 = □+2, 민재 = □+3'], size=33, w='Bold', gap=1.6)
    lines(d, 80, 720, ['이제 합이 22가 되는 □를 찾으세요.', ('4567? 그건 내린 순서예요. 이름 순서로!', CORAL)], size=34, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '유나 4층, 서연 5층, 도윤 6층, 민재 7층.')
    rows = [('2 3 4 5', 14), ('3 4 5 6', 18), ('4 5 6 7', 22), ('5 6 7 8', 26), ('6 7 8 9', 30)]
    d.text((100, 290), '유나 서연 도윤 민재', font=F('Bold', 28), fill=YEL)
    d.text((620, 290), '합', font=F('Bold', 28), fill=YEL)
    for i, (fl, s) in enumerate(rows):
        y = 340 + i * 84; hit = s == 22
        d.rounded_rectangle([66, y, 1014, y + 70], radius=16, fill=PANEL, outline=MINT if hit else CELL_LINE, width=3)
        d.text((100, y + 12), fl, font=F('Black', 38), fill=WHITE if hit else GRAY)
        d.text((620, y + 14), str(s), font=F('Bold', 36), fill=MINT if hit else GRAY)
        d.text((760, y + 14), '✓' if hit else '✗', font=F('Bold', 36), fill=MINT if hit else DIM)
    lines(d, 76, 790, ['합이 22인 건 4·5·6·7층뿐.', '이름 순서로 다시 적으면', '민재 7 · 유나 4 · 도윤 6 · 서연 5 → 7465'], size=33)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '순서를 바꿔 적으면 열리는 금고', '내린 순서가 아니라 이름 순서였습니다.')
    panel(d, 90, 280, w=300, owner=WHO, dim={2, 3, 8, 9})
    f = F('Black', 110)
    s = ' '.join(ANS); d.text((720 - d.textlength(s, font=f) / 2, 420), s, font=f, fill=MINT)
    lines(d, 440, 600, ['맞혔다면 좋아요 ·', '다음 방은 팔로우!', '', '4567에 속았다면', '댓글로 자수하기'], size=34, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
