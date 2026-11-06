"""ROOM 110 cards in the 3D style (kit/style3d.py), from the switch-and-bulb sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 116, '2026.11.22'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_warm_cold_swapped']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    bd = PROOF['boards'][n[1]]; f = c.width / 470
    put(c, pill(f"① {bd['first']}번 10분 켰다 끄기", round(24 * f), INK, (246, 200, 70, 255), (round(12 * f), round(4 * f))), 0.25 * c.width, 0.09 * c.height)
    put(c, pill(f"② {bd['second']}번 켜기", round(24 * f), INK, (130, 230, 190, 255), (round(12 * f), round(4 * f))), 0.25 * c.width, 0.09 * c.height + 40 * f)
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 34)
    if val: put(fr, badge(val, 44), x0 + im.width - 40, y0 + 40)


POS = [(292, 530), (788, 530), (292, 930), (788, 930)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '어느 스위치일까?', '방에는 딱 한 번만 들어갈 수 있어요')
four(fr, 'q', 490)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '스위치 규칙', '스위치 3개, 전구 3개')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['① 첫 스위치를 10분 켰다가 꺼요', '② 두 번째 스위치를 켜요', '③ 방에 들어가서 전구를 확인해요', ('남은 하나는 건드리지 않아요', YEL)], 33)
one(fr, 'qA', 540, 900, 600, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 ? 전구의 스위치 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['전구 상태: 켜짐 · 꺼졌지만 뜨거움 · 차가움', ('? 전구의 스위치 번호를 이으면 암호', YEL), '', ('유명한 전구 퀴즈를 3D로', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '뜨거운 전구는 무슨 뜻일까요?')
four(fr, 'q', 490)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '꺼진 전구도 만져 보면 달라요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('켜진 전구 = ② 지금 켠 스위치', WHITE), '꺼졌는데 뜨거움 = ① 10분 켰다 끈 스위치', '꺼졌고 차가움 = 안 건드린 스위치', ('뜨거운 걸 안 건드린 거라 하면 함정!', YEL)], 32)
one(fr, 'qA', 540, 900, 600, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '? 전구는 이 번호 스위치 거예요')
four(fr, 'r', 490, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qB', 300, 520, 450, tag=False); one(fr, 'rB', 790, 520, 450, tag=False)
fr.alpha_composite(panel(960, 230), (60, 830))
text_lines(fr, 100, 860, ['B: 차가운 전구는 한 번도 안 켠 1번', '10분 켰다 끈 6번 전구는 아직 뜨거워요'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
