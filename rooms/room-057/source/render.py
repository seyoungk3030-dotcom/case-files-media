"""ROOM 057 cards in the 3D style (kit/style3d.py), from the roller-plank sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 57, '2026.11.03'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']


def spr(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()
    im = im.crop((max(l - 10, 0), max(t - 10, 0), r + 10, b + 10)); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 36, INK, (244, 246, 250, 245), (20, 6)), x0 + 10, y0 + 18)
        if val: put(fr, badge(val, 36), x0 + 80, y0 + 18)


def rows(fr, pre, y0, w=900, gap=200, vals=None):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 540, y0 + i * gap, w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '롤러가 굴러가면 판자는 몇 칸 갈까?')
rows(fr, 'p', 400, 900, 190)
text_lines(fr, 540, 1095, [('롤러는 미끄러지지 않고 굴러가요', SOFT)], 32, center=True)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '판자 아래에 둥근 롤러 두 개')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 롤러는 바닥과 판자 위에서 미끄러지지 않는다', '2. 민트 화살표 = 롤러가 굴러간 칸 수',
                          ('3. 판자는 몇 칸 움직일까?', YEL)], 34)
spr(fr, 'pB', 540, 760, 960, tag=False)
text_lines(fr, 540, 960, ['판자는 롤러 위에 올려져 있을 뿐', ('롤러와 같이 움직일까, 아닐까?', YEL)], 34, center=True)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 판자가 움직인 칸 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 판자가 A 5칸, B 1칸, C 7칸, D 3칸 갔다면', ('암호 5173', YEL), '',
                          ('판자 앞쪽 끝이 움직인 거리로 세요', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
rows(fr, 'p', 390, 900, 185)
fr.alpha_composite(panel(960, 110), (60, 1060))
text_lines(fr, 540, 1078, ['민트 화살표 = 롤러가 굴러간 칸 · 미끄러짐 없음', ('암호 = 판자가 움직인 칸 수 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'롤러만큼 간다고 하면 {PROOF["trap_same_as_rollers"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('롤러가 굴러가면', WHITE), '롤러의 윗부분은 중심보다 더 빨리 앞으로 가요.', '판자는 그 윗부분에 붙어서 움직여요.',
                          ('롤러 따라 같은 칸 수가 아니에요', YEL)], 35)
spr(fr, 'pC', 540, 880, 960)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '판자는 롤러의 두 배를 간다')
fr.alpha_composite(panel(960, 200), (60, 280))
text_lines(fr, 540, 300, ['롤러가 1칸 구르면 바닥 위로 1칸,', '판자는 롤러 위에서 또 1칸 → 합쳐서 2칸',
                          ('A 1→2 · B 3→6 · C 2→4 · D 4→8', YEL)], 32, center=True)
rows(fr, 'a', 580, 880, 175, list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 2칸 · B 6칸 · C 4칸 · D 8칸')
rows(fr, 'a', 370, 780, 150, list(CODE))
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 960)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
