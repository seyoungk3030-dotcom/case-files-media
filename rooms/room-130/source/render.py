"""ROOM 130 cards in the 3D style (kit/style3d.py), from the density-column sprites made by scene3d.py. All sprites
are cropped to one shared box (q*/r*.png); four tall jars sit in one row."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 130, '2026.11.27'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_water_only']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
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

fr = card(ROOM, DATE, 1, 7, '어디에서 멈출까?', '액체 층 위로 떨어뜨린 작은 공')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '액체 층 규칙', '숫자는 밀도 (g/cm³) · 클수록 무거워요')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['층은 섞이지 않고 그대로 있어요', '공은 위에서 떨어져 가라앉기 시작해요',
                          '공이 멈추는 높이의 눈금은?', ('물보다 무거우면 바닥까지 갈까요?', YEL)], 33)
one(fr, 'qA', 540, 870, 200, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 공이 멈춘 눈금')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 · 6 · 0 · 9 눈금이면', ('암호 2609', YEL), '', ('부엌 재료로 만드는 무지개 탑', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '공과 층의 숫자를 하나씩 비교해 보세요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '자기보다 가벼운 층은 뚫고 내려가요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('자기보다 무거운 층을 만나면 그 위에서 멈춰요', WHITE), '위에서부터 한 층씩 비교해 보세요',
                          '맨 위 층부터 무거우면 수면에 떠요', ('물하고만 비교하면 함정!', YEL)], 33)
one(fr, 'qC', 540, 880, 200, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 동그라미 = 공이 멈춘 자리')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qA', 400, 590, 230, tag=False); one(fr, 'rA', 680, 590, 230, tag=False)
fr.alpha_composite(panel(960, 180), (60, 900))
text_lines(fr, 100, 927, ['A: 포도 1.05는 기름·물을 뚫고 내려가', '세제 1.1 위에서 멈춰요 → 4'], 31)
put(fr, text_layer(' '.join(CODE), 72, MINT, glow=MINT), 540, 1128)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
