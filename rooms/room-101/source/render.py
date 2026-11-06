"""ROOM 101 cards in the 3D style (kit/style3d.py), from the shadow-digit sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 101, '2026.11.17'
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
    if val: put(fr, badge(val, 44), x0 + im.width - 40, y0 + 40)


POS = [(292, 500), (788, 500), (292, 935), (788, 935)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '그림자 속 숫자', '정면에서 빛을 비추면 벽에 뜨는 숫자는?')
four(fr, 'q', 480)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙', '왼쪽 아래 손전등이 벽을 정면으로 비춰요')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['막대는 공중에 떠 있고 앞뒤 깊이가 제각각', '빛은 벽을 향해 곧게 날아가요',
                          '바닥 그림자 = 천장 조명이 만든 위치 힌트', ('민트 선 두 줄 = 숫자의 왼쪽·오른쪽 끝', YEL)], 33)
one(fr, 'qA', 540, 900, 560, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 벽에 뜨는 숫자')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 7 · 2 · 0 · 8 이 뜨면', ('암호 7208', YEL), '', ('숫자는 계산기 같은 7칸 숫자', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '손전등 자리에 눈을 대고 상상해 보세요')
four(fr, 'q', 480)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '깊이는 그림자에서 사라져요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('앞뒤로 멀리 떨어진 막대도 벽에선 한 줄', WHITE), '빛을 향해 꽂힌 막대는 그림자가 점 하나',
                          '점은 숫자의 획이 아니에요', ('그 막대를 획으로 세면 함정!', YEL)], 35)
one(fr, 'qD', 540, 900, 560, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '불을 켜면 벽에 숫자가 떠요')
four(fr, 'r', 480, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {PROOF['trap_count_decoys']}")
one(fr, 'qB', 300, 520, 480, tag=False); one(fr, 'rB', 790, 520, 480, tag=False)
fr.alpha_composite(panel(960, 300), (60, 800))
text_lines(fr, 100, 830, ['B의 아래쪽 막대는 빛을 향해 꽂혀 점만 남아요', '그래서 6이 아니라 5, 깊이는 상관없어요'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1010)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
