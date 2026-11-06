"""ROOM 102 cards in the 3D style (kit/style3d.py), from the bottle-pitch sprites. All sprites are cropped to one
shared box (q*/r*.png) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 102, '2026.11.18'
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
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 10)
    if val: put(fr, badge(val, 40), x0 + 86, y0 + 12)


POS = [(292, 505), (788, 505), (292, 910), (788, 910)]


def four(fr, pre, w=515, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '대부분 반대로 말해요', '가장 높은 소리가 나는 병은 몇 번?')
four(fr, 'q')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '물병 연주', '똑같은 유리병 4개, 물 높이만 달라요')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['후~ 판: 병 입구를 입으로 불어요', '톡! 판: 숟가락으로 병을 두드려요', '판마다 가장 높은 소리가 나는 병을 찾아요',
                          ('같은 물병인데 방법만 달라요', YEL)], 33)
one(fr, 'qA', 540, 860, 960, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 가장 높은 소리의 병 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 4번 · 1번 · 1번 · 3번이면', ('암호 4113', YEL), '', ('불 때와 두드릴 때는 달라요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '무엇이 떨리는지 생각해 보세요')
four(fr, 'q')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '떨리는 게 공기냐, 유리냐', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('불면 물 위의 빈 공기가 울려요', WHITE), '공기 기둥이 짧을수록 높은 소리', '두드리면 유리와 물이 같이 떨려요',
                          ('물이 많을수록 무거워서 낮은 소리!', YEL)], 33)
one(fr, 'qB', 540, 860, 960, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '빛나는 물병이 가장 높은 소리')
four(fr, 'r', vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {PROOF['trap_blow_everywhere']}")
fr.alpha_composite(panel(960, 290), (60, 300))
text_lines(fr, 110, 335, ['후~ 불기: 물이 가장 많은 병이 가장 높아요', '톡! 두드리기: 물이 가장 적은 병이 가장 높아요',
                          '모두 물 많은 병을 고르면 함정 답', ('집에서 빈 병으로 직접 해 보세요!', YEL)], 33)
one(fr, 'rB', 540, 830, 680, tag=False)
put(fr, text_layer(' '.join(CODE), 90, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
