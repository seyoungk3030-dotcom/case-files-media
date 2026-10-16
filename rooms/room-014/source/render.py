import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 14, '2026.10.16', 7
OUT = os.path.join(HERE, '..', 'cards')
CLUES = ['① 윗줄 A + B = 12', '② 아랫줄 C + D = 7', '③ 왼쪽 줄 A + C = 10', '④ 가장 큰 숫자는 B']
ANS = '4861'


def dial(d, top, size=170, vals=None, col=WHITE, hl=None, col2='?'):
    """2x2 dial with sums: row sums on the right, left-column sum below. hl: set of cell letters to outline."""
    x0 = (W - size * 2) // 2 - 70
    for i, L in enumerate('ABCD'):
        r, c = divmod(i, 2)
        x, y = x0 + c * size, top + r * size
        cell(d, x, y, size, vals[i] if vals else '?', col=col if vals else DIM, fs=80)
        if hl and L in hl:
            d.rounded_rectangle([x + 8, y + 8, x + size - 8, y + size - 8], radius=14, outline=CORAL, width=5)
        d.text((x + 20, y + 16), L, font=F('Bold', 26), fill=YEL)
    f = F('Bold', 50)
    for r, s in enumerate(('= 12', '= 7')):
        d.text((x0 + 2 * size + 24, top + r * size + size / 2 - 32), s, font=f, fill=MINT)
    s = '= 10'
    d.text((x0 + size / 2 - d.textlength(s, font=f) / 2, top + 2 * size + 6), s, font=f, fill=MINT)
    s = col2
    d.text((x0 + size * 1.5 - d.textlength(s, font=f) / 2, top + 2 * size + 6), s, font=f, fill=DIM if s == '?' else MINT)
    return top + 2 * size + 70


def clues(d, y, size=36, hl=None, col=WHITE, x=100):
    for i, c in enumerate(CLUES):
        d.text((x, y + i * size * 1.55), c, font=F('Bold', size), fill=CORAL if hl and i in hl else col)


def card1():
    im, d = base(ROOM, DATE, 1, N, '합만 남은 금고 다이얼', '숫자는 지워지고, 줄의 합만 남았다.')
    bottom = dial(d, 300)
    lines(d, 80, bottom + 50, ['민재가 금고 다이얼 네 칸을 돌려놓고 퇴근했다.', '남은 건 줄마다 적힌 합, 그리고 메모 한 줄.'], size=34, w='Bold')
    d.rounded_rectangle([66, bottom + 190, 1014, bottom + 290], radius=20, fill=PANEL, outline=YEL, width=3)
    ctext(d, bottom + 218, '메모  “가장 큰 숫자는 B 칸에 있다”', col=YEL, font=F('Bold', 36))
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '다이얼의 규칙', '이 규칙은 항상 지켜집니다.')
    d.rounded_rectangle([66, 290, 1014, 570], radius=24, fill=PANEL)
    lines(d, 110, 325, ['① 네 칸에는 1~9 중 숫자 하나씩', '② 네 숫자는 모두 다르다', '③ 줄 옆의 숫자 = 그 줄 두 칸의 합'],
          size=38, w='Bold', gap=1.75)
    d.text((100, 680), '예시', font=F('Bold', 34), fill=YEL)
    lines(d, 100, 740, ['윗줄이 = 9 라면 A + B = 9', 'A가 4면 B는 5. (A가 3이면 B는 6)', '',
                        ('합 하나로는 부족해요. 줄을 겹쳐 보세요!', MINT)], size=34)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호는 A → B → C → D', '왼쪽 위부터 오른쪽으로, 윗줄 다음 아랫줄.')
    x0, size, y = 300, 120, 320
    for i, L in enumerate('ABCD'):
        r, c = divmod(i, 2)
        cell(d, x0 + c * size * 2.2, y + r * 150, size, L, col=YEL, fs=56)
    d.text((x0 + 150, y + 26), '→', font=F('Bold', 56), fill=MINT)
    d.text((x0 + 150, y + 176), '→', font=F('Bold', 56), fill=MINT)
    lines(d, 80, 680, ['예를 들어 A=1, B=2, C=3, D=4 라면', ('암호는 1234', YEL), '',
                       '메모 한 줄 ④가 마지막 열쇠입니다.'], size=36, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '1~9, 네 숫자 모두 다름. A → B → C → D')
    bottom = dial(d, 290, size=150)
    d.rounded_rectangle([66, bottom + 20, 1014, bottom + 300], radius=24, fill=PANEL, outline=YEL, width=3)
    clues(d, bottom + 50, size=36, x=110)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 겹치는 칸은 A', '①과 ③은 둘 다 A를 지나갑니다.', subcol=CORAL)
    bottom = dial(d, 290, size=150, hl={'A'})
    lines(d, 80, bottom + 30, ['A를 정하면 B = 12 - A, C = 10 - A, D = 7 - C.', 'D가 1 이상이려면 A는 4 이상. 하나씩 넣어 보세요.',
                               ('5752? 숫자 5가 두 번! 규칙 ②를 잊지 마세요.', CORAL)], size=32, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '후보 넷 중 B가 가장 큰 건 하나뿐.')
    rows = [('A = 4', '4 8 6 1', 'B=8 가장 큼 ✓', MINT), ('A = 7', '7 5 3 4', 'A가 더 큼 ✗', GRAY),
            ('A = 8', '8 4 2 5', 'A가 더 큼 ✗', GRAY), ('A = 9', '9 3 1 6', 'A가 더 큼 ✗', GRAY)]
    for i, (a, code, why, c) in enumerate(rows):
        y = 300 + i * 112
        d.rounded_rectangle([66, y, 1014, y + 96], radius=18, fill=PANEL, outline=MINT if i == 0 else CELL_LINE, width=3)
        d.text((100, y + 24), a, font=F('Bold', 36), fill=YEL)
        d.text((300, y + 20), code, font=F('Black', 44), fill=WHITE if i == 0 else GRAY)
        d.text((620, y + 26), why, font=F('Bold', 34), fill=c)
    lines(d, 76, 790, ['A가 5면 C도 5, A가 6이면 B도 6 → 규칙 ② 위반.', '남은 후보 4861 · 7534 · 8425 · 9316.',
                       '메모 ④ “가장 큰 숫자는 B” → 4861만 통과!'], size=32)
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '줄을 겹치면 열리는 금고', '세 줄의 합과 메모 한 줄이 딱 맞았습니다.')
    bottom = dial(d, 290, size=150, vals=list(ANS), col=MINT, col2='= 9')
    big_answer(d, bottom + 10, ANS)
    ctext(d, bottom + 175, '4+8=12 ✓   6+1=7 ✓   4+6=10 ✓   B=8 최대 ✓', col=GRAY, font=F('Bold', 30))
    lines(d, 80, bottom + 250, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '5752에 속았다면 댓글로 자수하기'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
