import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 13, '2026.10.15', 7
OUT = os.path.join(HERE, '..', 'cards')
CLUES = ['① 두 날은 같은 요일', '② 두 번째 날은 금요일', '③ 두 번째 날은 20일 이후', '④ 네 자리 숫자는 모두 다르다']
ANS = '1327'
DAYS = '일월화수목금토'


def calendar(d, top, cell=118, marks=None, dim=None, fri=False, circle=None):
    """November 2026 (starts Sunday). marks: {day: color} filled, circle: {day: color} outline."""
    left = (W - cell * 7) // 2
    d.text((left, top - 6), '2026년 11월', font=F('Bold', 34), fill=WHITE)
    hy = top + 52
    for i, n in enumerate(DAYS):
        col = CORAL if i == 0 else (MINT if (fri and i == 5) else GRAY)
        f = F('Bold', 28)
        d.text((left + i * cell + cell / 2 - d.textlength(n, font=f) / 2, hy), n, font=f, fill=col)
    gy = hy + 50
    for day in range(1, 31):
        i = day - 1; r, c = divmod(i, 7)
        x, y = left + c * cell, gy + r * (cell - 22)
        h = cell - 30
        fill = (marks or {}).get(day)
        out = (circle or {}).get(day)
        d.rounded_rectangle([x + 5, y + 4, x + cell - 5, y + h], radius=12, fill=fill or CELL,
                            outline=out or CELL_LINE, width=4 if out else 2)
        col = WHITE
        if day < 10 or (dim and day in dim): col = DIM
        if fill: col = BG
        f = F('Bold', 38); s = str(day)
        d.text((x + cell / 2 - d.textlength(s, font=f) / 2, y + h / 2 - 24), s, font=f, fill=col)
    return gy + 5 * (cell - 22)


def clues(d, y, size=34, hl=None, col=WHITE):
    for i, c in enumerate(CLUES):
        d.text((90, y + i * size * 1.6), c, font=F('Bold', size), fill=MINT if hl and i in hl else col)


def card1():
    im, d = base(ROOM, DATE, 1, N, '달력에서 지워진 두 개의 별', '금고 암호는 ★ 두 날짜를 이어 붙인 것.')
    bottom = calendar(d, 300)
    lines(d, 80, bottom + 40, ['도윤이 달력에 ★ 두 개를 그려두었는데', '누군가 지워버렸다. 남은 건 메모 네 줄뿐.'], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '암호 만드는 법', '두 날짜를 순서대로 이어 붙입니다.')
    d.rounded_rectangle([66, 290, 1014, 560], radius=24, fill=PANEL)
    lines(d, 110, 325, ['★ 두 날짜는 모두 2026년 11월', '두 날 모두 10일 이후 (두 자리 날짜)', '앞선 날짜 + 뒤의 날짜 = 네 자리 암호'],
          size=36, w='Bold', gap=1.75)
    d.text((100, 630), "예시", font=F('Bold', 34), fill=YEL)
    lines(d, 100, 690, ['★가 12일과 19일이라면 → 암호는 1219', '★가 25일과 11일이라면 → 1125 (앞선 날짜부터)'], size=34)
    x0 = 250
    for i in range(4):
        x = x0 + i * 130 + (60 if i >= 2 else 0)
        cell(d, x, 880, 130, '?', col=DIM, fs=60)
    d.text((x0 + 262, 908), '+', font=F('Bold', 60), fill=YEL)
    for lab, cx in (('앞선 ★', x0 + 130), ('뒤의 ★', x0 + 450)):
        f = F('Bold', 28); d.text((cx - d.textlength(lab, font=f) / 2, 1022), lab, font=f, fill=YEL)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '도윤의 메모 네 줄', '네 줄 모두 사실입니다.')
    d.rounded_rectangle([66, 300, 1014, 640], radius=24, fill=PANEL, outline=YEL, width=3)
    clues(d, 340, size=40)
    lines(d, 80, 720, ['메모를 하나씩 적용해서', '달력 속 후보를 지워 나가 보세요.', '', ('마지막 한 줄이 함정을 걸러냅니다.', MINT)],
          size=34, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '두 날짜 모두 11월 10일 이후, 앞선 날부터.')
    bottom = calendar(d, 290, cell=112)
    clues(d, bottom + 30, size=32)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 연도처럼 보이는 함정', '①~③만 쓰면 후보가 둘 남습니다.', subcol=CORAL)
    bottom = calendar(d, 290, cell=112, fri=True, circle={13: CORAL, 20: CORAL, 27: MINT}, dim={6})
    lines(d, 80, bottom + 30, ['두 번째 날 = 20일 이후 금요일 → 27일.', '첫 날도 금요일 → 13일 또는 20일.',
                               ('2027은 연도 같지만… 메모 ④를 다시 보세요!', CORAL)], size=32, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '★는 13일(금)과 27일(금)이었습니다.')
    bottom = calendar(d, 290, cell=112, fri=True, marks={13: MINT, 27: MINT}, circle={20: CORAL})
    lines(d, 76, bottom + 30, ['20일 이후 금요일은 27일 하나뿐.', '같은 요일인 첫 날은 13일 또는 20일.',
                               '2027은 2가 두 번 → 메모 ④ 위반!', '그래서 13일 + 27일 = 1327'], size=31)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '메모 네 줄을 모두 지켜야 탈출', '마지막 한 줄까지 확인한 사람만 열 수 있었습니다.')
    bottom = calendar(d, 290, cell=112, fri=True, marks={13: MINT, 27: MINT})
    big_answer(d, bottom + 20, ANS)
    lines(d, 80, bottom + 190, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '2027에 속았다면 댓글로 자수하기 🙂'.replace(' 🙂', '')], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
