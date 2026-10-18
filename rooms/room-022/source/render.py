import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 22, '2026.10.18', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '1325'
WT = {'c': 1, 't': 3, 's': 2, 'r': 5}
COL = {'c': MINT, 't': YEL, 's': CORAL, 'r': WHITE}
NAME = {'c': '●', 't': '▲', 's': '■', 'r': '★'}
SCALES = [(['c', 'c', 'c'], ['t']), (['t', 'c'], ['s', 's']), (['r', 's'], ['t', 't', 'c'])]


def shape(d, k, cx, bottom, s, num=None):
    col = COL[k]; top = bottom - s
    if k == 'c': d.ellipse([cx - s / 2, top, cx + s / 2, bottom], fill=col)
    if k == 's': d.rectangle([cx - s / 2, top, cx + s / 2, bottom], fill=col)
    if k == 't': d.polygon([(cx, top - 4), (cx - s / 2 - 4, bottom), (cx + s / 2 + 4, bottom)], fill=col)
    if k == 'r':
        R, r = s * 0.58, s * 0.25; ccy = bottom - s * 0.52
        pts = [(cx + (R if i % 2 == 0 else r) * math.sin(i * math.pi / 5), ccy - (R if i % 2 == 0 else r) * math.cos(i * math.pi / 5)) for i in range(10)]
        d.polygon(pts, fill=col)
    if num is not None:
        f = F('Black', int(s * 0.5)); t = str(num)
        yy = bottom - s * (0.42 if k == 't' else 0.52) - s * 0.3
        d.text((cx - d.textlength(t, font=f) / 2, yy), t, font=f, fill=BG)


def seesaw(d, y, left, right, s=58, w=860, nums=False, tag=None, hl=None):
    """y = beam top. Returns bottom of fulcrum."""
    cx = W // 2; x0, x1 = cx - w // 2, cx + w // 2
    d.rounded_rectangle([x0, y, x1, y + 12], radius=6, fill=hl or GRAY)
    d.polygon([(cx, y + 12), (cx - 34, y + 62), (cx + 34, y + 62)], fill=DASH)
    for side, items in ((-1, left), (1, right)):
        gap = s + 22; tot = gap * (len(items) - 1)
        mid = cx + side * w // 4
        for i, k in enumerate(items):
            shape(d, k, mid - tot / 2 + i * gap, y - 4, s, WT[k] if nums else None)
    d.text((cx - 13, y - 52), '=', font=F('Bold', 40), fill=DIM)
    if tag: d.text((x0 - 2, y + 22), tag, font=F('Bold', 26), fill=DIM)
    return y + 62


def all_scales(d, top, s=56, step=170, nums=False, hl=None):
    y = top + s + 10
    for i, (L, R) in enumerate(SCALES):
        seesaw(d, y, L, R, s=s, nums=nums, tag=f'저울 {i + 1}', hl=(hl or {}).get(i))
        y += step
    return y - step + 62


def legend(d, y, nums=False, s=64):
    for i, k in enumerate('ctsr'):
        shape(d, k, 210 + i * 220, y + s, s, WT[k] if nums else None)


def card1():
    im, d = base(ROOM, DATE, 1, N, '수평을 이룬 세 저울', '추 네 종류, 저울 세 개.')
    bottom = all_scales(d, 290)
    lines(d, 80, bottom + 50, ['창고 금고 옆에 저울 세 개가 수평을 이루고 있다.', '●▲■★ 추의 무게가 곧 네 자리 암호.'], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '저울의 규칙', '수평 = 양쪽 무게가 같다.')
    d.rounded_rectangle([66, 290, 1014, 600], radius=24, fill=PANEL)
    lines(d, 110, 322, ['① 같은 모양의 추는 무게가 같다', '② 모양이 다르면 무게도 다르다', '③ 추는 모두 1~9kg, 정수 kg',
                        '④ 수평인 저울은 양쪽 합이 같다'], size=34, w='Bold', gap=1.6)
    d.text((100, 640), '예시', font=F('Bold', 34), fill=YEL)
    seesaw(d, 790, ['c', 'c'], ['t'], s=50, w=600)
    lines(d, 100, 900, ['●● 와 ▲ 가 수평이면 ▲ = ● 두 개 무게.', ('9kg를 넘는 추는 없다는 걸 기억하세요!', MINT)], size=32)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호 = ● ▲ ■ ★', '네 추의 무게를 이 순서대로.')
    legend(d, 330)
    for i, k in enumerate('ctsr'):
        f = F('Bold', 40); s = '?'
        d.text((210 + i * 220 - d.textlength(s, font=f) / 2, 420), s, font=f, fill=GRAY)
    lines(d, 80, 540, ['● 무게 → ▲ 무게 → ■ 무게 → ★ 무게', '네 자리를 이으면 금고가 열립니다.'], size=34, w='Bold')
    d.rounded_rectangle([66, 700, 1014, 900], radius=22, fill=PANEL)
    d.text((100, 726), '읽는 법 예시', font=F('Bold', 30), fill=YEL)
    lines(d, 100, 784, ['● 4kg, ▲ 7kg, ■ 2kg, ★ 9kg 라면 → 4729'], size=31)
    lines(d, 80, 960, [('세 저울이 모두 수평이라는 걸 이용하세요.', MINT)], size=34, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '규칙과 단서는 이것이 전부.')
    bottom = all_scales(d, 280)
    d.rounded_rectangle([66, bottom + 40, 1014, bottom + 250], radius=22, fill=PANEL)
    lines(d, 96, bottom + 64, ['같은 모양 = 같은 무게, 다른 모양 = 다른 무게', '모든 추는 1~9kg 정수, 세 저울 모두 수평',
                               ('암호 = ● ▲ ■ ★ 무게 순서', YEL)], size=31, w='SemiBold', gap=1.5)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 전부 ●로 바꾸기', '모든 추를 ● 몇 개인지로 세어 보세요.', subcol=CORAL)
    bottom = all_scales(d, 280, hl={2: CORAL})
    lines(d, 80, bottom + 40, ['저울 1: ▲ = ● 3개.  저울 2: ■ = ● 2개.', '저울 3에서 ★은 ● 몇 개일까?',
                               ('그리고 9kg를 넘는 추는 없다!', CORAL)], size=33, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '● 1 · ▲ 3 · ■ 2 · ★ 5.')
    bottom = all_scales(d, 280, nums=True)
    lines(d, 76, bottom + 40, ['▲ = ●×3, ■ = (▲+●)÷2 = ●×2.', '★ + ●×2 = ●×7 이니 ★ = ●×5.',
                               '● = 2면 ★ = 10kg로 초과 → ● = 1. 암호 1325.'], size=31)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '9kg 제한이 연 금고', '모든 추는 ● 하나의 배수였습니다.')
    legend(d, 310, nums=True, s=110)
    big_answer(d, 560, ANS)
    lines(d, 80, 790, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '● = 2부터 넣어 봤다면 댓글로 알려주세요.'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
