"""ROOM 059 cards in the 3D style (kit/style3d.py), from the pulley sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 59, '2026.11.03'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']


def spr(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()
    im = im.crop((max(l - 10, 0), max(t - 10, 0), r + 10, b + 10)); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag:
        put(fr, pill(name[1], 38, INK, (244, 246, 250, 245), (20, 6)), x0 + 10, y0 + 20)
        if val: put(fr, badge(val, 38), x0 + 80, y0 + 20)


def grid(fr, pre, y0, w=380, gap=380, vals=None):
    for i, k in enumerate('ABCD'):
        spr(fr, pre + k, 300 + (i % 2) * 480, y0 + (i // 2) * gap, w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '줄을 당기면 상자는 몇 칸 올라갈까?')
grid(fr, 'p', 500, 260, 430)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '줄은 늘어나지도 미끄러지지도 않는다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 고리 달린 줄 끝을 민트 화살표만큼 당긴다', '2. 위 나무판에 달린 도르래는 움직이지 않는다',
                          ('3. 상자는 몇 칸 올라갈까?', YEL)], 34)
spr(fr, 'pB', 540, 830, 420, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 상자가 올라간 칸 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 상자가 A 5칸, B 1칸, C 6칸, D 2칸 올라갔다면', ('암호 5162', YEL), '',
                          ('당긴 칸 수와 같을까요?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'p', 470, 240, 380)
fr.alpha_composite(panel(960, 110), (60, 1060))
text_lines(fr, 540, 1078, ['민트 화살표 = 줄 끝을 당긴 칸 수', ('암호 = 상자가 올라간 칸 수 A B C D', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'당긴 만큼 올라간다고 하면 {PROOF["trap_same_as_pull"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('상자를 붙잡고 있는 줄이 몇 가닥인지 세 보세요.', WHITE), '당긴 줄 길이가', '그 가닥들에 똑같이 나뉘어요.',
                          ('C는 상자를 잡은 줄이 세 가닥이에요', YEL)], 35)
spr(fr, 'pC', 540, 900, 300, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '당긴 칸 ÷ 상자를 잡은 줄 가닥 수')
fr.alpha_composite(panel(960, 160), (60, 280))
text_lines(fr, 540, 300, ['A 3÷1=3 · B 8÷2=4', ('C 6÷3=2 · D 7÷1=7 (도르래가 두 개여도 한 가닥)', YEL)], 31, center=True)
grid(fr, 'a', 640, 220, 370, list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A 3칸 · B 4칸 · C 2칸 · D 7칸')
grid(fr, 'a', 440, 190, 300, list(CODE))
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 975)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
