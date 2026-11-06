"""ROOM 137 cards in the 3D style (kit/style3d.py), from the bimetal-thermostat sprites made by scene3d.py. All
sprites are cropped to one shared box (q*/r*.png); four tall boards sit in one row; a heat pill is baked in."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 137, '2026.11.29'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_other_lamp']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    f = c.width / 255; hot = PROOF['boards'][n[1]]['temp'] == 'hot'
    put(c, pill('촛불로 데우기' if hot else '얼음으로 식히기', round(22 * f), INK, (250, 160, 90, 255) if hot else (150, 200, 255, 255), (round(10 * f), round(4 * f))), 0.5 * c.width, 0.97 * c.height)
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 34)
    if val: put(fr, badge(val, 44), x0 + im.width - 40, y0 + 40)


POS = [(150 + 260 * i, 740) for i in range(4)]


def four(fr, pre, w=255, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '어느 전구가 켜질까?', '두 금속을 붙인 띠를 데우거나 식혀요')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '바이메탈 규칙', '금색 = 놋쇠 · 회색 = 철 (딱 붙어 있어요)')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['열을 받으면 놋쇠가 철보다 더 많이 늘어나요', '식으면 놋쇠가 철보다 더 많이 줄어들어요',
                          '띠가 휘어 닿는 쪽 전구의 숫자는?', ('많이 늘어나는 쪽으로 휠까요?', YEL)], 33)
one(fr, 'qA', 540, 880, 220, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 켜진 전구 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 · 6 · 0 · 9번이 켜지면', ('암호 2609', YEL), '', ('옛날 다리미와 전기장판 속 온도 스위치', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '길어진 쪽은 휜 띠의 안쪽일까, 바깥쪽일까?')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '휜 띠는 바깥쪽이 더 길어요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('데우면 길어진 놋쇠가 바깥 → 철 쪽으로 휘어요', WHITE), '식히면 짧아진 놋쇠가 안쪽 → 놋쇠 쪽으로',
                          '놋쇠와 철이 어느 쪽에 있는지 확인!', ('놋쇠 쪽으로 휜다고 하면 함정!', YEL)], 33)
one(fr, 'qB', 540, 880, 220, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '휜 띠가 닿은 쪽 전구가 켜져요')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qA', 400, 600, 230, tag=False); one(fr, 'rA', 680, 600, 230, tag=False)
fr.alpha_composite(panel(960, 180), (60, 900))
text_lines(fr, 100, 927, ['A: 놋쇠가 왼쪽, 데우면 놋쇠가 바깥이 되게', '오른쪽(철 쪽)으로 휘어서 6번이 켜져요'], 31)
put(fr, text_layer(' '.join(CODE), 72, MINT, glow=MINT), 540, 1128)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
