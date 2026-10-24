"""ROOM 040 cards in the 3D style (kit/style3d.py), from the marble-drop sprites made by scene3d.py."""
import json, math, os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 40, '2026.10.24'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
MC = {'A': (40, 200, 160), 'B': (255, 160, 40), 'C': (240, 100, 90), 'D': (150, 130, 255)}
GOLD = (255, 200, 60)


def spr(fr, name, cx, cy, w, marbles=True):
    im = Image.open(f'{B}/{name}.png').convert('RGBA')
    l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 60 else 0).getbbox()
    pts = json.load(open(f'{B}/{name}.json')); b = max(b, max(p['y'] for p in pts) + 30); t = min(t, min(p['y'] for p in pts) - 30)
    im = im.crop((l, t, r, b)); sc = w / im.width; im = im.resize((w, round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - w / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    for p in pts:
        x, y = x0 + (p['x'] - l) * sc, y0 + (p['y'] - t) * sc; k = p['key']
        if k.isdigit(): put(fr, pill(f'{k}번', 32, INK, (244, 246, 250, 245), (18, 5)), x, y)
        elif marbles: put(fr, pill(k, 28, INK, (*MC[k], 250), (14, 4)), x, y)
    return im.height


def dial(way, r=70, glow=False):
    lay = Image.new('RGBA', (2 * r + 8, 2 * r + 8), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); c = r + 4
    d.ellipse((4, 4, 2 * r + 4, 2 * r + 4), fill=(240, 242, 246, 255))
    a = math.radians(-45 if way == 'L' else 45); dx, dy = math.sin(a), math.cos(a)
    d.line((c - dx * r * .55, c - dy * r * .55, c + dx * r * .25, c + dy * r * .25), fill=(*GOLD, 255), width=round(r * .22))
    tip = (c + dx * r * .62, c + dy * r * .62); px, py = -dy, dx
    base = (c + dx * r * .12, c + dy * r * .12)
    d.polygon([tip, (base[0] + px * r * .35, base[1] + py * r * .35), (base[0] - px * r * .35, base[1] - py * r * .35)], fill=(*GOLD, 255))
    return lay


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '구슬 네 개를 차례로 떨어뜨리면', 'A B C D는 몇 번 통에 들어갈까?')
spr(fr, 'start', 540, 718, 740)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '구슬이 지나가면 화살표가 바뀐다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 구슬은 A, B, C, D 순서로 하나씩 떨어진다', '2. 갈림길에서는 화살표 방향으로 간다',
                          ('3. 구슬이 지나간 화살표는 반대로 바뀐다', YEL)], 34)
put(fr, text_layer('구슬이 지나가기 전', 32, SOFT, 'Bold'), 300, 600); put(fr, text_layer('지나간 뒤', 32, SOFT, 'Bold'), 780, 600)
put(fr, dial('L', 90), 300, 760); put(fr, dial('R', 90), 780, 760)
put(fr, text_layer('→', 90, YEL, 'Black'), 540, 760)
text_lines(fr, 540, 920, ['왼쪽으로 보낸 갈림길은', ('다음 구슬을 오른쪽으로 보낸다', YEL)], 36, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D가 들어간 통 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (*MC[k], 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: A가 3번, B가 1번, C가 4번, D가 2번 통이면', ('암호 3142', YEL), '',
                          ('통은 왼쪽부터 1, 2, 3, 4번', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
spr(fr, 'start', 540, 645, 640)
fr.alpha_composite(panel(960, 120), (60, 1000))
text_lines(fr, 540, 1022, ['A부터 하나씩 · 화살표 방향으로 · 지나가면 반대로', ('암호 = A B C D가 들어간 통 번호', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', f'맨 위 화살표만 바꾸면 {PROOF["trap_top_only"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('아래쪽 두 갈림길도', WHITE), '구슬이 지나갈 때마다 바뀌어요.', '세 화살표가 지금 어느 쪽인지',
                          ('구슬 하나마다 다시 확인하세요', YEL)], 35)
spr(fr, 'start', 540, 920, 440)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '구슬 하나마다 화살표를 바꿔 가면')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 540, 318, ['A  왼쪽 → 오른쪽 → 2번 통', 'B  오른쪽 → 왼쪽 → 3번 통', 'C  왼쪽 → 왼쪽 → 1번 통',
                          ('D  오른쪽 → 오른쪽 → 4번 통', YEL)], 36, center=True)
spr(fr, 'end', 540, 895, 470)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A는 2번, B는 3번, C는 1번, D는 4번 통')
spr(fr, 'end', 540, 575, 520)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 900)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1040)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
