"""ROOM 106 cards in the 3D style (kit/style3d.py), from the water-jet bottle sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 106, '2026.11.19'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 24)
    if val: put(fr, badge(val, 44), x0 + im.width - 50, y0 + 60)


POS = [(282, 490), (798, 490), (282, 912), (798, 912)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '가장 멀리 나가는 물줄기', '마개를 모두 뽑으면 바닥에 가장 멀리 닿는 구멍은?')
four(fr, 'q', 520)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '물병 구멍 규칙', '물병 옆에 마개 막힌 구멍 4개')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['마개를 한꺼번에 뽑아요 (물 높이는 그대로)', '깊은 구멍일수록 물이 세게 나와요',
                          '높은 구멍일수록 바닥까지 오래 날아가요', ('받침대 높이도 바닥까지 거리에 들어가요', YEL)], 33)
one(fr, 'qA', 540, 900, 640, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 가장 멀리 가는 구멍 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 4번 · 4번 · 2번 · 1번이면', ('암호 4421', YEL), '', ('맨 아래 구멍이 늘 1등은 아니에요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '세기와 높이, 둘 다 생각하세요')
four(fr, 'q', 520)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '물 깊이 × 바닥까지 높이', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('날아가는 거리는 (물 깊이 × 바닥까지 높이)로 정해져요', WHITE), '두 값이 비슷할 때 가장 멀리 가요',
                          '받침대가 높으면 아래 구멍이 유리해요', ('늘 맨 아래 구멍? 함정!', YEL)], 32)
one(fr, 'qC', 540, 900, 640, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 물줄기가 가장 멀리 닿아요')
four(fr, 'r', 520, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {PROOF['trap_lowest_hole']}")
one(fr, 'qA', 300, 520, 470, tag=False); one(fr, 'rA', 790, 520, 470, tag=False)
fr.alpha_composite(panel(960, 230), (60, 800))
text_lines(fr, 100, 830, ['A는 물 높이의 절반쯤인 1번 구멍이 1등', '맨 아래 구멍은 세지만 금방 바닥에 떨어져요'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1120)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
