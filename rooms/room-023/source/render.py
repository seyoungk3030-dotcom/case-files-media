import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 23, '2026.10.19', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '8976'
PEOPLE = ['민재', '유나', '도윤', '서진']
PCOL = {'민재': MINT, '유나': YEL, '도윤': CORAL, '서진': (176, 156, 255)}
HOUR = {'민재': 8, '유나': 9, '도윤': 7, '서진': 6}
SAY = [('민재', '유나는 첫 번째로 오지 않았어.'), ('유나', '도윤은 처음도 마지막도 아니었어.'),
       ('도윤', '민재랑 서진은 딱 두 시간 차이로 왔어.'), ('서진', '나는 민재보다 먼저 왔어.')]


def badge(d, cx, cy, name, r=34, fs=26):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=PCOL[name])
    f = F('Bold', fs)
    d.text((cx - d.textlength(name, font=f) / 2, cy - fs * 0.62), name, font=f, fill=BG)


def log(d, top, filled=None, hl=None, row=96, w=700):
    """Door log: one row per hour; filled = {hour: name}."""
    x0 = (W - w) // 2
    d.rounded_rectangle([x0, top, x0 + w, top + 70 + row * 4], radius=22, fill=PANEL)
    d.text((x0 + 36, top + 18), '출입 기록 · 야근 출근', font=F('Bold', 30), fill=GRAY)
    for i, h in enumerate((6, 7, 8, 9)):
        y = top + 70 + i * row
        d.line([x0 + 30, y, x0 + w - 30, y], fill=DASH, width=2)
        d.text((x0 + 40, y + row / 2 - 22), f'오후 {h}시', font=F('Bold', 36), fill=WHITE)
        bx = x0 + w - 300
        out = (hl or {}).get(h)
        d.rounded_rectangle([bx, y + 14, bx + 260, y + row - 14], radius=16, fill=CELL, outline=out or CELL_LINE, width=5 if out else 2)
        name = (filled or {}).get(h)
        if name: badge(d, bx + 130, y + row / 2, name, r=28, fs=24)
        else:
            f = F('Bold', 36); d.text((bx + 130 - d.textlength('?', font=f) / 2, y + row / 2 - 24), '?', font=f, fill=DIM)
    return top + 70 + row * 4


def testimony(d, top, size=30, gap=74):
    for i, (n, s) in enumerate(SAY):
        y = top + i * gap
        badge(d, 110, y + 26, n, r=30, fs=22)
        d.rounded_rectangle([160, y, 1014, y + 54], radius=18, fill=PANEL)
        d.text((186, y + 9), s, font=F('SemiBold', size), fill=WHITE)
    return top + 4 * gap


def card1():
    im, d = base(ROOM, DATE, 1, N, '지워진 출입 기록', '네 명, 네 개의 출근 시각.')
    bottom = log(d, 290)
    lines(d, 80, bottom + 50, ['밤사이 금고가 열렸고, 출입 기록의 이름이 지워졌다.', '남은 건 네 사람의 증언뿐.'], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '증언의 규칙', '오늘은 아무도 거짓말을 하지 않습니다.')
    d.rounded_rectangle([66, 290, 1014, 520], radius=24, fill=PANEL)
    lines(d, 110, 322, ['① 네 명이 오후 6 · 7 · 8 · 9시에 한 명씩 왔다', '② 같은 시각에 온 사람은 없다', '③ 네 사람의 증언은 모두 사실이다'],
          size=34, w='Bold', gap=1.7)
    d.text((100, 620), '예시', font=F('Bold', 34), fill=YEL)
    lines(d, 100, 680, ['"A는 B보다 먼저 왔어" → A의 시각이 더 이르다.', '"두 시간 차이" → 6시와 8시, 또는 7시와 9시.', '',
                        ('경우를 나눠 보면 하나만 살아남아요.', MINT)], size=33)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호 = 출근 시각', '민재 → 유나 → 도윤 → 서진 순서로.')
    for i, n in enumerate(PEOPLE):
        cx = 210 + i * 220
        badge(d, cx, 380, n, r=62, fs=36)
        f = F('Bold', 44); d.text((cx - d.textlength('?시', font=f) / 2, 470), '?시', font=f, fill=GRAY)
    lines(d, 80, 600, ['네 사람이 온 시각의 숫자를 이 순서대로 이으면', '네 자리 암호가 됩니다.'], size=34, w='Bold')
    d.rounded_rectangle([66, 740, 1014, 920], radius=22, fill=PANEL)
    d.text((100, 764), '읽는 법 예시', font=F('Bold', 30), fill=YEL)
    lines(d, 100, 822, ['민재 7시, 유나 6시, 도윤 9시, 서진 8시 → 7698'], size=31)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '6 · 7 · 8 · 9시에 한 명씩, 증언은 모두 사실.')
    bottom = log(d, 280, row=80, w=640)
    end = testimony(d, bottom + 40)
    lines(d, 80, end + 16, [('암호 = 민재 → 유나 → 도윤 → 서진의 출근 시각', YEL)], size=31, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 경우는 둘뿐', '서진이 먼저, 민재가 두 시간 뒤.', subcol=CORAL)
    d.rounded_rectangle([66, 290, 1014, 470], radius=22, fill=PANEL)
    lines(d, 100, 316, ['경우 1: 서진 6시 · 민재 8시', '경우 2: 서진 7시 · 민재 9시'], size=36, w='Bold', gap=1.6)
    lines(d, 80, 530, ['경우 2라면 남은 시각은 6시와 8시.', '도윤은 처음이 아니니 8시, 유나가 6시가 되는데…',
                       ('민재의 증언과 맞을까요?', CORAL)], size=33, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '민재 8 · 유나 9 · 도윤 7 · 서진 6.')
    bottom = log(d, 280, filled={v: k for k, v in HOUR.items()}, row=84, w=640)
    lines(d, 76, bottom + 40, ['경우 2는 유나가 6시가 되어 민재의 증언과 충돌.', '경우 1: 서진 6시, 민재 8시. 도윤은 마지막이 아니니 7시,',
                               '유나는 9시. 민재 → 유나 → 도윤 → 서진 = 8976.'], size=31)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '기록을 되살린 네 개의 증언', '두 시간 차이가 경우를 둘로 줄였습니다.')
    for i, n in enumerate(PEOPLE):
        cx = 210 + i * 220
        badge(d, cx, 370, n, r=62, fs=36)
        f = F('Bold', 44); s = f'{HOUR[n]}시'
        d.text((cx - d.textlength(s, font=f) / 2, 460), s, font=f, fill=PCOL[n])
    big_answer(d, 580, ANS)
    lines(d, 80, 800, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '경우 2부터 따져 봤다면 댓글로 알려주세요.'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
