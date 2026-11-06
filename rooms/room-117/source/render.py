"""ROOM 110 cards in the 3D style (kit/style3d.py), from the melting-ice sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png, with faint corner pixels) so every board keeps the same scale, also in the reel."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 117, '2026.11.23'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_always_rises']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    bd = PROOF['boards'][n[1]]; f = c.width / 470; y = 0.05 * c.height
    for it in bd['items']:
        lab = {'float': f"떠 있는 얼음 {it['ice']} g", 'rack': f"받침 위 얼음 {it['ice']} g", 'stone': f"돌 든 얼음 {it['ice']} g"}[it['kind']]
        put(c, pill(lab, round(24 * f), INK, (200, 230, 255, 255), (round(12 * f), round(4 * f))), 0.3 * c.width, y); y += 40 * f
        if it['kind'] == 'stone':
            put(c, pill(f"돌 {it['stone_g']} g · {it['stone_cc']} cm³", round(24 * f), INK, (246, 200, 70, 255), (round(12 * f), round(4 * f))), 0.3 * c.width, y); y += 40 * f
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 34)
    if val: put(fr, badge(val, 44), x0 + im.width - 40, y0 + 40)


POS = [(292, 520), (788, 520), (292, 935), (788, 935)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '얼음이 다 녹으면?', '물의 높이는 몇 눈금이 될까요?')
four(fr, 'q', 440)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '얼음 규칙', '얼음 1 g이 녹으면 물 1 cm³')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['컵의 한 눈금 = 물 100 cm³', '떠 있는 얼음, 받침 위 얼음, 돌 든 얼음', '얼음이 전부 녹은 뒤의 눈금을 구하세요',
                          ('녹으면 무조건 올라갈까요?', YEL)], 33)
one(fr, 'qA', 540, 900, 560, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 다 녹은 뒤 눈금')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 눈금이 2 · 9 · 4 · 0이면', ('암호 2940', YEL), '', ('빙하가 녹으면 바다는 얼마나 오를까?', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '떠 있는 얼음은 이미 무엇을 하고 있을까요?')
four(fr, 'q', 440)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '떠 있는 얼음은 자기 무게만큼 물을 밀어내요', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('떠 있는 얼음: 녹아도 수위 그대로', WHITE), '받침 위 얼음: 녹은 물이 전부 더해져요',
                          '돌 든 얼음: 돌이 가라앉으면 오히려 내려가요', ('녹으면 다 올라간다고 하면 함정!', YEL)], 32)
one(fr, 'qC', 540, 900, 560, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '민트 선 = 다 녹은 뒤 · 회색 선 = 처음')
four(fr, 'r', 440, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qC', 300, 520, 450, tag=False); one(fr, 'rC', 790, 520, 450, tag=False)
fr.alpha_composite(panel(960, 230), (60, 830))
text_lines(fr, 100, 860, ['C: 떠 있을 땐 돌 300 g만큼 물을 밀어내다가', '가라앉으면 돌 부피 100 cm³만 차지해요 → 2눈금 ↓'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
