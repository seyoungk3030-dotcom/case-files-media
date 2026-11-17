"""ROOM 177 cards in the 3D style (kit/style3d.py), from the staircase sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png)."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 177, '2026.12.13'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_straight_slope']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
for key in 'ABCD':
    bb = [ims[f'{s}{key}'].getchannel('A').getbbox() for s in 'pa']
    BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
    for s in 'pa':
        c = ims[f'{s}{key}'].crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
        c.save(f'{B}/{"q" if s == "p" else "r"}{key}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (18, 6)), x0 + 30, y0 + 20)
    if val: put(fr, badge(val, 46), x0 + 115, y0 + 25)


POS = [(292, 515), (788, 515), (292, 935), (788, 935)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '계단 카펫', '카펫은 몇 m가 필요할까요?')
four(fr, 'q', 470)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '카펫 규칙', '계단에 카펫을 빈틈없이 붙여요')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['1. 카펫은 계단 윗면과 세로면을 모두 덮어요', '2. 맨 아래부터 맨 위까지 한 줄로 이어져요', '3. 흰 표시 = 전체 높이와 전체 깊이',
                          '4. 계단 높이는 서로 달라도 돼요', ('카펫 길이는 몇 m일까요?', YEL)], 33)
one(fr, 'qB', 540, 870, 600, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 카펫 길이(m)')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 5m · 1m · 7m · 3m면', ('암호 5173', YEL), '', ('계단 수가 많으면 더 길까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '윗면과 세로면을 모두 덮는 카펫')
four(fr, 'q', 470)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '카펫 조각을 옆으로 밀어 모아 보세요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('세로면 조각을 모두 모으면 전체 높이,', WHITE), '윗면 조각을 모두 모으면 전체 깊이가 돼요.', '계단이 몇 개든, 높이가 들쭉날쭉하든 같아요.',
                          (f'비스듬한 대각선으로 재면 함정 {TRAP}', YEL)], 33)
one(fr, 'qD', 540, 880, 560, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '카펫 = 전체 높이 + 전체 깊이')
four(fr, 'r', 470, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '계단이 8개여도 2개여도 똑같아요')
one(fr, 'rA', 300, 560, 470, tag=False); one(fr, 'rD', 790, 560, 470, tag=False)
fr.alpha_composite(panel(960, 300), (60, 800))
text_lines(fr, 100, 830, ['A와 D: 높이 1m + 깊이 1m = 카펫 2m', '대각선 1.4m가 아니에요!'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1010)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
