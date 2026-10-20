import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 28, '2026.10.20', 7
OUT = os.path.join(HERE, '..', 'cards')
ANS = '5293'
FONT = {'2': ['###', '..#', '###', '#..', '###'], '3': ['###', '..#', '###', '..#', '###'], '5': ['###', '#..', '###', '..#', '###'],
        '7': ['###', '..#', '.#.', '.#.', '.#.'], '9': ['###', '#.#', '###', '..#', '###']}


def runs(s): return [len(x) for x in s.split('.') if x]


def panel(d, x, y, digit, s=52, lit=False, label=None, col_hl=False, row_hl=False, rc_w=74):
    """One 3x5 panel at (x, y) = top-left of the clue area. Returns (right edge, bottom)."""
    g = FONT[digit]; ch = 3 * 30
    gx, gy = x + rc_w, y + ch + 10
    if label:
        f = F('Black', 40); d.text((gx + 1.5 * s - d.textlength(label, font=f) / 2, y - 58), label, font=f, fill=YEL)
    f = F('Bold', 28)
    for c in range(3):
        rs = runs(''.join(r[c] for r in g))
        for i, v in enumerate(rs):
            t = str(v); yy = gy - 10 - (len(rs) - i) * 30
            d.text((gx + c * s + s / 2 - d.textlength(t, font=f) / 2, yy), t, font=f, fill=CORAL if col_hl else WHITE)
    for r in range(5):
        t = '  '.join(map(str, runs(g[r])))
        d.text((gx - 12 - d.textlength(t, font=f), gy + r * s + s / 2 - 17), t, font=f, fill=CORAL if row_hl else WHITE)
        for c in range(3):
            bx, by = gx + c * s, gy + r * s
            on = lit and g[r][c] == '#'
            d.rounded_rectangle([bx + 4, by + 4, bx + s - 4, by + s - 4], radius=8, fill=YEL if on else CELL, outline=CELL_LINE, width=2)
    return gx + 3 * s, gy + 5 * s


def boards(d, top, lit=False, s=52, col_hl=False, row_hl=False):
    w = 74 + 3 * s; gap = (948 - 4 * w) / 3
    bottom = 0
    for i, dg in enumerate(ANS):
        _, bottom = panel(d, 66 + i * (w + gap), top, dg, s=s, lit=lit, label='ABCD'[i], col_hl=col_hl, row_hl=row_hl)
    return bottom


def bulbs(d, x, y, pattern, s=60):
    for c, ch in enumerate(pattern):
        d.rounded_rectangle([x + c * s + 4, y + 4, x + (c + 1) * s - 4, y + s - 4], radius=10,
                            fill=YEL if ch == '#' else CELL, outline=CELL_LINE, width=2)


def card1():
    im, d = base(ROOM, DATE, 1, N, '꺼진 전광판의 숫자', '숫자 단서만 남은 네 칸짜리 전광판.')
    bottom = boards(d, 340)
    lines(d, 80, bottom + 40, ['엘리베이터 위 전광판의 전구가 모두 꺼졌다.', '칸 옆 숫자는 켜져야 할 전구 묶음의 길이.',
                               ('네 칸을 다시 켜면 나오는 숫자가 금고 암호.', MINT)], size=32, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '전구 켜는 규칙', '이 규칙은 항상 지켜집니다.')
    d.rounded_rectangle([66, 280, 1014, 560], radius=24, fill=PANEL)
    lines(d, 106, 306, ['① 숫자 = 이어서 켜진 전구 묶음의 길이', '② 숫자가 둘이면 묶음도 둘, 그 사이는 한 칸 이상 꺼짐',
                        '③ 왼쪽 숫자는 가로줄, 위 숫자는 세로줄 단서'], size=32, w='Bold', gap=1.8)
    d.text((100, 600), '예시 · 가로 세 칸', font=F('Bold', 34), fill=YEL)
    for i, (clue, pat, note) in enumerate([('3', '###', '세 칸 모두 켜짐'), ('1  1', '#.#', '양 끝만 켜짐'), ('2', '##.', '')]):
        y = 670 + i * 110
        f = F('Bold', 40); d.text((210 - d.textlength(clue, font=f), y + 8), clue, font=f, fill=WHITE)
        bulbs(d, 250, y, pat)
        if note: d.text((480, y + 12), note, font=F('SemiBold', 32), fill=MINT)
        else:
            d.text((480, y + 12), '또는', font=F('SemiBold', 32), fill=GRAY)
            bulbs(d, 560, y, '.##')
            d.text((760, y + 12), '두 가지', font=F('SemiBold', 32), fill=GRAY)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호는 A → B → C → D', '켜진 모양이 곧 숫자 한 자리.')
    panel(d, 100, 380, '7', s=80, lit=True, label='예시', rc_w=80)
    lines(d, 470, 500, ['단서대로 켜면', '전구가 숫자 모양이 돼요.', ('이 예시는 7.', MINT), '',
                        '네 칸을 모두 켜서', 'A → B → C → D', '순서로 읽으세요.'], size=33, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '가로 · 세로 단서를 모두 만족하게 켜세요.')
    bottom = boards(d, 350, s=56)
    lines(d, 80, bottom + 40, ['칸마다 켜는 방법은 단 하나.', '켜진 숫자를 A → B → C → D 순서로 이으세요.'], size=33, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 가로만 보면 함정', 'A · B · D는 가로 단서가 똑같아요.', subcol=CORAL)
    bottom = boards(d, 340, row_hl=True)
    lines(d, 80, bottom + 40, ['가로 단서만 보면 세 칸이 같은 숫자처럼 보여요.', '세로 단서 5는 그 세로줄 전체가 켜진다는 뜻.',
                               ('위 숫자들을 꼭 비교해 보세요!', CORAL)], size=32, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', 'A=5, B=2, C=9, D=3.')
    bottom = boards(d, 340, lit=True)
    lines(d, 70, bottom + 36, ['가로가 3 · 1 · 3 · 1 · 3이면 숫자 2 · 3 · 5 중 하나.', 'A: 첫 세로줄이 「3, 1」 → 왼쪽 위가 켜진 5.',
                               'B: 마지막 세로줄이 「3, 1」 → 오른쪽 위가 켜진 2.', 'D: 마지막 세로줄이 5 → 3.  C: 둘째 가로줄 「1, 1」 → 9.'], size=30)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '다시 켜진 전광판', '단서만으로 네 숫자가 모두 정해졌습니다.')
    bottom = boards(d, 340, lit=True)
    big_answer(d, bottom + 30, ANS)
    lines(d, 80, bottom + 220, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '몇 초 걸렸는지 댓글로 알려주세요.'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
