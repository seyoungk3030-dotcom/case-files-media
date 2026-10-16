import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 16, '2026.10.16', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '1950'
CLUES = ['① CCTV 속 벽시계는 거울에 비친 모습', '② 금고가 열린 시각 = 시계의 실제 시각', '③ 사건은 퇴근 후 저녁에 일어났다',
         '④ 암호 = 24시간제 시각 네 자리 (예: 21:05 → 2105)']


def clock(d, cx, cy, r, ang_h, ang_m, frame=CELL_LINE, tag=None, tagcol=YEL):
    """Analog clock without numerals; thick mint mark at 12. Angles in degrees clockwise from 12."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PANEL, outline=frame, width=6)
    for i in range(60):
        a = math.radians(i * 6); big = i % 5 == 0
        r1 = r - (34 if big else 18)
        col = GRAY if big else DASH
        d.line([cx + r1 * math.sin(a), cy - r1 * math.cos(a), cx + (r - 10) * math.sin(a), cy - (r - 10) * math.cos(a)],
               fill=col, width=6 if big else 2)
    d.rounded_rectangle([cx - 9, cy - r + 8, cx + 9, cy - r + 56], radius=6, fill=MINT)
    for ang, ln, w, col in ((ang_h, r * 0.5, 16, WHITE), (ang_m, r * 0.78, 9, YEL)):
        a = math.radians(ang)
        d.line([cx, cy, cx + ln * math.sin(a), cy - ln * math.cos(a)], fill=col, width=w)
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=WHITE)
    if tag:
        f = F('Bold', 30); d.text((cx - d.textlength(tag, font=f) / 2, cy + r + 18), tag, font=f, fill=tagcol)


def ang(h, m): return ((h % 12) + m / 60) * 30, m * 6
def mir(h, m): a, b = ang(h, m); return (360 - a) % 360, (360 - b) % 360


def cctv(d, top, r=230, sub='CAM 03 · 사무실 거울'):
    d.rounded_rectangle([96, top, 984, top + 2 * r + 110], radius=24, fill=CELL, outline=CELL_LINE, width=2)
    d.ellipse([126, top + 28, 146, top + 48], fill=CORAL)
    d.text((160, top + 20), sub, font=F('Bold', 28), fill=GRAY)
    f = F('Bold', 26); lg = '흰 바늘 시침 · 노란 바늘 분침'
    d.text((954 - d.textlength(lg, font=f), top + 22), lg, font=f, fill=YEL)
    clock(d, W // 2, top + 80 + r, r, *mir(19, 50))
    return top + 2 * r + 110


def card1():
    im, d = base(ROOM, DATE, 1, N, '거울 속 벽시계', '금고가 열린 순간, CCTV에 시계가 찍혔다.')
    bottom = cctv(d, 280)
    lines(d, 80, bottom + 40, ['그런데 카메라가 찍은 건 진짜 시계가 아니라', ('거울에 비친 벽시계였다.', MINT)], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '거울의 규칙', '거울은 왼쪽과 오른쪽만 뒤집습니다.')
    clock(d, 300, 470, 150, *ang(3, 0), tag='진짜 3:00')
    clock(d, 780, 470, 150, *mir(3, 0), tag='거울 속 모습')
    d.text((512, 440), '→', font=F('Bold', 60), fill=MINT)
    lines(d, 90, 720, ['12시 자리(민트 표시)와 6시 자리는 그대로.', '3시 쪽과 9시 쪽이 서로 바뀐다.',
                       '분침도 똑같이 좌우로 뒤집힌다.', '', ('노란 바늘 = 분침, 흰 바늘 = 시침', YEL)], size=34)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호 = 24시간제 네 자리', '실제 시각을 시·분 순서로 붙입니다.')
    d.rounded_rectangle([66, 300, 1014, 560], radius=24, fill=PANEL)
    lines(d, 110, 335, ['오전 9:05 → 0905', '오후 9:05 = 21:05 → 2105', '오후 6:30 = 18:30 → 1830'], size=40, w='Bold', gap=1.6)
    lines(d, 80, 640, ['거울 속 시각을 그대로 읽으면 안 됩니다.', '진짜 시계가 가리키는 시각을 찾은 뒤,',
                       ('오전인지 오후인지도 꼭 따져 보세요.', MINT)], size=36, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '거울을 되돌려 실제 시각을 찾으세요.')
    bottom = cctv(d, 270, r=190)
    d.rounded_rectangle([66, bottom + 24, 1014, bottom + 280], radius=24, fill=PANEL, outline=YEL, width=3)
    for i, c in enumerate(CLUES):
        d.text((96, bottom + 46 + i * 54), c, font=F('Bold', 31), fill=WHITE)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 4시 10분이 아니다', '화면에 보이는 그대로 읽으면 함정!', subcol=CORAL)
    clock(d, 300, 480, 160, *mir(19, 50), frame=CORAL, tag='거울 속: 4:10처럼 보임', tagcol=CORAL)
    clock(d, 780, 480, 160, *ang(19, 50), frame=MINT, tag='좌우를 되돌리면?', tagcol=MINT)
    lines(d, 80, 760, ['분침이 2(10분) 자리 → 거울을 되돌리면 10(50분) 자리.', '시침이 4와 5 사이 → 되돌리면 7과 8 사이.',
                       ('그런데 오전일까, 오후일까? 메모 ③을 보세요.', CORAL)], size=32, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '실제 시각은 저녁 7시 50분이었습니다.')
    clock(d, W // 2, 520, 210, *ang(19, 50), frame=MINT)
    lines(d, 76, 800, ['거울은 좌우만 바꾼다 → 10분 자리는 50분 자리.', '시침은 7과 8 사이 → 실제 시각은 7:50.',
                       '퇴근 후 저녁이니 오후 7:50 = 19:50.', ('0410, 0750은 함정 → 정답 1950', MINT)], size=32)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '거울을 뒤집으면 열리는 금고', '좌우를 되돌리고, 저녁까지 챙긴 사람만 탈출.')
    clock(d, W // 2, 470, 170, *ang(19, 50), frame=MINT, tag='19 : 50', tagcol=MINT)
    big_answer(d, 720, ANS)
    lines(d, 80, 920, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '0410에 속았다면 댓글로 자수하기'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
