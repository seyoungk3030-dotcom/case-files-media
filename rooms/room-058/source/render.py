"""ROOM 058 cards in the 3D style (kit/style3d.py), from the water-glass sprites made by scene3d.py."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 58, '2026.11.03'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']


def spr(fr, name, cx, cy, w):
    im = Image.open(f'{B}/{name}.png').convert('RGBA'); l, t, r, b = im.getchannel('A').point(lambda v: 255 if v > 90 else 0).getbbox()
    im = im.crop((max(l - 10, 0), max(t - 10, 0), r + 10, b + 10)); sc = w / im.width
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '1번 컵에 물을 부으면 어느 컵이 먼저 찰까?')
spr(fr, 'start', 540, 700, 700)
text_lines(fr, 540, 1090, [('가득 차는 순서대로 컵 번호 네 개', SOFT)], 32, center=True)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '관은 컵 옆에 붙어 아래 컵으로 이어진다')
fr.alpha_composite(panel(960, 230), (60, 290))
text_lines(fr, 100, 322, ['1. 물은 컵 안에서 처음 닿는 관(더 낮은 관)으로 흐른다', '2. 빨간 X 관은 막혀서 물이 못 지나간다',
                          ('3. 관 아래가 다 차야 물이 다음 관 높이까지 오른다', YEL)], 31)
spr(fr, 'start', 540, 840, 560)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', '가득 찬 순서대로 컵 번호 네 개')
for n, k in enumerate(['1번째', '2번째', '3번째', '4번째']):
    cx = 165 + n * 250; put(fr, pill(k, 36, INK, (244, 246, 250, 250), (20, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 7번, 4번, 3번, 6번 컵 순서로 찼다면', ('암호 7436', YEL), '',
                          ('끝까지 가득 찬 컵만 셉니다', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
spr(fr, 'start', 540, 690, 680)
fr.alpha_composite(panel(960, 110), (60, 1060))
text_lines(fr, 540, 1078, ['낮은 관 먼저 · 빨간 X는 막힘', ('암호 = 가득 찬 순서대로 컵 번호 4개', YEL)], 30, center=True)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '함정 주의', f'막힌 관을 못 보면 {PROOF["trap_ignore_blocked"]}', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('2번 컵의 왼쪽 관이 더 낮지만', WHITE), '빨간 X로 막혀 있어요.', '그래서 4번 컵에는 물이 한 방울도 안 가요.',
                          ('3번 컵은 1번 컵의 높은 관에 달려 있어요', YEL)], 35)
spr(fr, 'start', 540, 900, 460)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '낮은 관부터, 막힌 관은 건너뛰고')
fr.alpha_composite(panel(960, 250), (60, 280))
text_lines(fr, 540, 300, ['1번 컵의 낮은 관 → 2번 컵 → 막힌 관 대신 5번', '5번이 차고 2번도 차면 1번 물이 높은 관까지',
                          '3번 컵의 낮은 관 → 6번, 그다음 7번', ('5 → 2 → 6 → 7', YEL)], 31, center=True)
spr(fr, 'end', 540, 860, 600)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '5번 → 2번 → 6번 → 7번 컵 순서')
spr(fr, 'end', 540, 610, 560)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 960)
put(fr, text_layer(' '.join(CODE), 150, MINT, glow=MINT), 540, 1080)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
