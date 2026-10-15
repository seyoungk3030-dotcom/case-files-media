import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'kit'))
from style import *

ROOM, DATE, N = 12, '2026.10.15', 7
OUT = os.path.join(HERE, '..', 'cards')
ST = [('민재', 'A는 B의 두 배'), ('유나', 'C + D = A'), ('도윤', 'C가 가장 크다'),
      ('서연', 'D가 가장 작다'), ('하준', 'C는 D의 두 배')]
ANS = '6342'


def slots(d, y, vals=None, col=WHITE, size=150):
    x0 = (W - size * 4) // 2
    for i, L in enumerate('ABCD'):
        x = x0 + i * size
        d.text((x + size / 2 - d.textlength(L, font=F('Bold', 34)) / 2, y - 48), L, font=F('Bold', 34), fill=YEL)
        cell(d, x, y, size, vals[i] if vals else '?', col=col if vals else DIM, fs=72)


def statements(d, y, h=84, hl=None, strike=None, fs=36, x0=110, w=860):
    for i, (n, s) in enumerate(ST):
        yy = y + i * (h + 14)
        out = MINT if hl and i in hl else (CORAL if strike == i else CELL_LINE)
        d.rounded_rectangle([x0, yy, x0 + w, yy + h], radius=18, fill=PANEL, outline=out, width=3)
        d.text((x0 + 30, yy + h / 2 - fs * 0.62), n, font=F('Bold', fs), fill=YEL)
        d.text((x0 + 170, yy + h / 2 - fs * 0.62), f'“{s}”', font=F('Bold', fs), fill=WHITE)
        if strike == i:
            d.text((x0 + w - 130, yy + h / 2 - 22), '거짓', font=F('Black', 34), fill=CORAL)
            tw = d.textlength(f'“{s}”', font=F('Bold', fs))
            d.line([x0 + 170, yy + h / 2, x0 + 170 + tw, yy + h / 2], fill=CORAL, width=4)


def card1():
    im, d = base(ROOM, DATE, 1, N, '다섯 명 중 한 명이 거짓말', '진술 다섯 개. 거짓은 딱 하나.')
    slots(d, 330)
    statements(d, 520, h=70, fs=34)
    lines(d, 80, 1000, ['금고 암호를 아는 경비원 다섯 명.', ('네 명은 진실, 한 명은 거짓을 말했다.', MINT)], size=34, w='Bold')
    ctext(d, 1160, CTA_START.format(a='6~7'))
    return im


def card2():
    im, d = base(ROOM, DATE, 2, N, '금고의 규칙', '이 규칙은 거짓 없이 항상 참입니다.')
    d.rounded_rectangle([66, 300, 1014, 650], radius=24, fill=PANEL)
    lines(d, 110, 340, ['① 암호는 네 자리 A B C D', '② 각 자리는 1~9, 네 숫자는 모두 다르다', '③ 다섯 진술 중 정확히 하나만 거짓',
                        '④ 나머지 네 진술은 모두 참'], size=38, w='Bold', gap=1.75)
    d.text((100, 720), '예시', font=F('Bold', 34), fill=YEL)
    lines(d, 100, 780, ['“C가 가장 크다” = C가 A·B·D 모두보다 크다.', '“C는 D의 두 배” = D가 2면 C는 4.', '', ('하나만 거짓이니, 모순을 만드는 진술을 찾자!', MINT)], size=34)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card3():
    im, d = base(ROOM, DATE, 3, N, '암호는 A → B → C → D', '진술을 모두 믿으면 답이 없습니다.')
    slots(d, 330)
    statements(d, 520, h=70, fs=34)
    lines(d, 80, 1010, ['누가 거짓말쟁이인지 찾으면', '네 자리가 한 번에 풀린다.'], size=34, w='Bold')
    ctext(d, 1160, CTA_SOLVE)
    return im


def card4():
    im, d = base(ROOM, DATE, 4, N, '네 자리 암호는?', '거짓말쟁이 한 명을 찾으세요.')
    lines(d, 76, 270, ['A·B·C·D는 1~9, 모두 다른 숫자.', '다섯 진술 중 정확히 하나만 거짓.'], size=32, col=(214, 220, 228))
    slots(d, 440, size=140)
    statements(d, 640, h=76, fs=34)
    ctext(d, 1160, CTA_SOLVE)
    return im


def card5():
    im, d = base(ROOM, DATE, 5, N, '힌트 · 함께 참일 수 없는 둘', '두 진술을 나란히 놓아보세요.', subcol=CORAL)
    statements(d, 320, h=84, hl={1, 2}, fs=36)
    d.rounded_rectangle([66, 840, 1014, 1110], radius=24, fill=PANEL, outline=CORAL, width=3)
    lines(d, 100, 870, ['C + D = A 이면 A가 C보다 크다.', '그럼 “C가 가장 크다”는 틀린다.', ('→ 거짓말쟁이는 유나 아니면 도윤!', CORAL)],
          size=34, w='Bold')
    ctext(d, 1160, CTA_HINT, col=CORAL)
    return im


def card6():
    im, d = base(ROOM, DATE, 6, N, f'정답 공개 · {ANS}', '거짓말쟁이는 도윤이었습니다.')
    statements(d, 290, h=70, strike=2, fs=32)
    lines(d, 76, 820, ['유나가 거짓이면 A=2B, C=2D에 C가 가장 커야 해서', 'B < D가 된다. D가 가장 작다는 말과 모순!',
                       '→ 거짓은 도윤. 나머지를 합치면 3D = 2B.', 'D = 2, B = 3 → C = 4, A = 6'], size=31)
    ctext(d, 1150, 'A B C D  →  6 3 4 2', font=F('Bold', 44))
    return im


def card7():
    im, d = base(ROOM, DATE, 7, N, '거짓 하나만 지우면 탈출', '네 진술이 모두 정확히 맞아떨어졌습니다.')
    slots(d, 330, vals=list(ANS), col=MINT)
    lines(d, 120, 560, ['민재  6은 3의 두 배 ✓', '유나  4 + 2 = 6 ✓', ('도윤  C가 가장 크다 ✗', CORAL), '서연  2가 가장 작다 ✓',
                        '하준  4는 2의 두 배 ✓'], size=34, w='Bold', gap=1.5)
    big_answer(d, 840, ANS)
    lines(d, 80, 1040, ['맞혔다면 좋아요 · 다음 방은 팔로우!', '몇 초 걸렸는지 댓글로 알려주세요.'], size=32, w='Bold')
    return im


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for i, fn in enumerate([card1, card2, card3, card4, card5, card6, card7], 1):
        fn().save(f'{OUT}/card-{i:02d}.png', optimize=True)
    print('ok')
