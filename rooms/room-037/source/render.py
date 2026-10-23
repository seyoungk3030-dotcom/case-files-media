"""ROOM 037 cards in the 3D style (kit/style3d.py), from the stick-pile sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 37, '2026.10.23'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
CCOL = {'A': (40, 200, 160), 'B': (255, 160, 40), 'C': (240, 100, 90), 'D': (150, 130, 255), 'G': (236, 238, 242)}
LAYER = {k: PROOF['order_top_to_bottom'].index(k) + 1 for k in 'ABCDG'}


def pile(fr, cx, cy, w, layers=False, name='pile', tags=True):
    im = Image.open(f'{B}/{name}.png').convert('RGBA')
    l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox(); l, t = max(0, l - 60), max(0, t - 50)
    im = im.crop((l, t, min(im.width, r + 60), min(im.height, b + 50))); sc = w / im.width
    im = im.resize((w, round(im.height * sc)), Image.LANCZOS); x0, y0 = cx - w / 2, cy - im.height / 2
    fr.alpha_composite(im, (int(x0), int(y0)))
    if not tags: return
    for p in json.load(open(f'{B}/{name}.json')):
        x, y = x0 + (p['x'] - l) * sc, y0 + (p['y'] - t) * sc; k = p['key']
        lab = '흰' if k == 'G' else k
        put(fr, pill(lab, round(w / 26), INK, (*CCOL[k], 250), (16, 6)), x, y)
        if layers: put(fr, badge(str(LAYER[k]), round(w / 30)), x + w / 22, y - w / 26)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '막대 다섯 개가 쌓인 더미', 'A B C D는 위에서부터 몇 번째 층?')
pile(fr, 540, 640, 940)
text_lines(fr, 540, 1030, [('겹친 곳에서 위에 보이는 막대가 더 위층', SOFT)], 34, center=True)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '겹친 곳을 보면 위아래가 보인다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 막대끼리 겹친 곳에서 위에 보이는 쪽이 더 위층', '2. 맨 위가 1층, 흰 막대도 한 층으로 센다',
                          ('3. 암호 = A B C D가 위에서부터 몇 번째인지', YEL)], 34)
pile(fr, 540, 790, 800, name='example', tags=False)
text_lines(fr, 540, 1040, [('예: 보라 막대가 빨강 막대 위에 있다', WHITE)], 36, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D의 층 번호')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (*CCOL[k], 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 330), (60, 700))
text_lines(fr, 540, 735, ['예: 위에서부터 D, C, 흰, B, A 순서라면', ('A는 5, B는 4, C는 2, D는 1 → 암호 5421', YEL), '',
                          ('층은 1부터 5까지, 흰 막대도 한 층', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
pile(fr, 540, 640, 940)
fr.alpha_composite(panel(960, 140), (60, 980))
text_lines(fr, 540, 1003, ['겹친 곳에서 위에 보이면 더 위층 · 맨 위가 1층', ('흰 막대도 한 층 · 암호 = A B C D의 층', YEL)], 32, center=True)
cta(fr, CTA4); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', f'흰 막대를 빼고 세면 {PROOF["trap_skip_gray"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('흰 막대에는 글자가 없지만', WHITE), '더미 속 한 층을 차지해요.', '흰 막대를 건너뛰면 그 아래 막대들의',
                          ('층 번호가 하나씩 작아져요', YEL)], 35)
pile(fr, 540, 900, 860)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '겹친 곳을 위에서부터 따라가면')
fr.alpha_composite(panel(960, 250), (60, 290))
text_lines(fr, 540, 318, ['C가 B 위 · B가 흰 막대 위', '흰 막대가 D 위 · D가 A 위', ('위에서부터  C  B  흰  D  A', YEL)], 36, center=True)
pile(fr, 540, 850, 960, layers=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', 'A는 5층, B는 2층, C는 1층, D는 4층')
pile(fr, 540, 560, 900, layers=True)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 920)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1050)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
