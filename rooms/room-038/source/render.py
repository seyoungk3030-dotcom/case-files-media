"""ROOM 038 cards in the 3D style (kit/style3d.py), from the dial-lock sprites made by scene3d.py."""
import json, os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 38, '2026.10.24'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
GREEN, AMBER, GRAY = (40, 220, 170), (255, 210, 40), (110, 118, 130)


def spr(fr, name, cx, cy, w):
    im = trim(Image.open(f'{B}/{name}.png').convert('RGBA')); im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - w / 2), int(cy - im.height / 2))); return im.height


def rows(fr, y0, w=800, labels=True):
    im = trim(Image.open(f'{B}/try1.png').convert('RGBA')); h = round(im.height * w / im.width); gap = h + 24
    for i in range(4):
        cy = y0 + i * gap + h / 2; spr(fr, f'try{i + 1}', 580, cy, w)
        if labels: put(fr, text_layer(f'{i + 1}차', 34, SOFT, 'Bold'), 110, cy)
    return y0 + 3 * gap + h


def lamp(d, cx, cy, col, r=17): d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*col, 255))


def legend(fr, y, size=32):
    lay = Image.new('RGBA', (1080, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    items = [(GREEN, '숫자와 자리 모두 맞음'), (AMBER, '숫자는 있지만 자리가 다름')]
    widths = [text_layer(t, size, WHITE, 'Bold').width + 60 for _, t in items]; x = 540 - (sum(widths) + 40) / 2
    for (c, t), wd in zip(items, widths):
        lamp(d, x + 18, 30, c); tl = text_layer(t, size, WHITE, 'Bold', shadow=False); lay.alpha_composite(tl, (int(x + 46), int(30 - tl.height / 2))); x += wd + 40
    fr.alpha_composite(lay, (0, int(y - 30)))


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '자물쇠를 네 번 돌려봤다', '불빛만 보고 네 자리 암호를 맞혀라')
end = rows(fr, 300, 820)
legend(fr, end + 50)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules
fr = card(ROOM, DATE, 2, 7, '불빛 읽는 법', '불의 색과 개수만 보인다')
fr.alpha_composite(panel(960, 265), (60, 290))
text_lines(fr, 100, 322, ['1. 암호는 0~9 중 서로 다른 숫자 네 개', ('2. 초록 불 = 숫자도 맞고 자리도 맞음', GREEN),
                          ('3. 노랑 불 = 숫자는 들어가지만 자리가 다름', AMBER), '4. 불이 어느 숫자 몫인지는 알려주지 않는다'], 34)
spr(fr, 'try1', 540, 760, 820)
text_lines(fr, 540, 880, ['예: 초록 두 개 = 이 네 숫자 중 두 개가 제자리', ('나머지 두 숫자는 암호에 없다', SOFT)], 34, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', '자물쇠 다이얼 왼쪽부터 네 자리')
spr(fr, 'lock', 540, 620, 620)
fr.alpha_composite(panel(960, 200), (60, 900))
text_lines(fr, 540, 932, ['왼쪽 다이얼부터 차례로 읽은 네 자리가 암호', ('예: 다이얼이 1 2 3 4라면 암호 1234', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '단서는 이 네 줄이 전부')
end = rows(fr, 300, 800)
legend(fr, end + 40, 30)
text_lines(fr, 540, end + 85, [('숫자는 서로 다름 · 회색 불은 꺼진 불', SOFT)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

# 5 hint
fr = card(ROOM, DATE, 5, 7, '힌트', '불이 하나도 안 켜진 줄부터', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('불이 전부 꺼진 줄은', WHITE), '그 네 숫자가 암호에 하나도 없다는 뜻이에요.', '그 숫자들을 지우고 나면',
                          ('초록 두 개 줄이 바로 풀려요', YEL)], 35)
spr(fr, 'try2', 540, 800, 820)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '꺼진 줄부터 지워 나가면')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 318, ['2차 9720 불 없음 → 9 7 2 0은 없다', ('1차 8395 초록 2 → 남은 8 3이 제자리', WHITE),
                          '4차 2805 노랑 1 → 8 확인 (2 0 5 없음)', '3차 6917 노랑 2 → 6과 1이 들어간다',
                          ('1은 3번 자리가 아니니 4번, 6은 3번 → 8361', YEL)], 33)
spr(fr, 'open', 540, 905, 400)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', '자물쇠가 열렸다')
spr(fr, 'open', 540, 545, 470)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 880)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1020)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
