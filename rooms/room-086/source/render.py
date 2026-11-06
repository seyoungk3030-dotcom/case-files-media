"""ROOM 086 cards in the 3D style (kit/style3d.py): spot-the-difference between two desk renders (p1, p2); a2 shows
picture 2 with rings round every difference."""
import json, os, sys
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 86, '2026.11.12'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']
for n in ('p1', 'p2', 'a2'):
    im = Image.open(f'{B}/{n}.png').convert('RGBA'); m = Image.new('L', im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, im.width - 1, im.height - 1), 40, fill=255)
    im.putalpha(Image.fromarray(__import__('numpy').minimum(__import__('numpy').array(im.getchannel('A')), __import__('numpy').array(m)))); im.save(f'{B}/r{n}.png')


def pic(fr, n, cx, cy, w, tag=None, col=WHITE):
    im = Image.open(f'{B}/r{n}.png'); im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
    if tag: put(fr, pill(tag, 30, INK, (244, 246, 250, 245), (16, 6)), cx - im.width / 2 + 70, cy - im.height / 2 + 30)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
KINDS = [('A', '색이 바뀐 곳'), ('B', '사라진 것'), ('C', '자리를 옮긴 것'), ('D', '크기가 바뀐 것')]

fr = card(ROOM, DATE, 1, 7, '대부분 여기서 틀려요', '3D 틀린 그림 찾기 · 다른 곳은 몇 군데?')
pic(fr, 'p1', 540, 515, 820, '그림 1'); pic(fr, 'p2', 540, 940, 820, '그림 2')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '그림 2에서 달라진 곳을 종류별로 세요')
fr.alpha_composite(panel(960, 330), (60, 290))
text_lines(fr, 100, 322, ['A 색이 바뀐 곳 개수', 'B 사라진 것 개수', 'C 자리를 옮긴 것 개수', 'D 크기가 바뀐 것 개수', ('A B C D 개수를 이으면 암호!', YEL)], 34)
pic(fr, 'p2', 540, 880, 820, '그림 2')
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 종류별 개수')
for n, (k, t) in enumerate(KINDS):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 450); put(fr, text_layer(t, 26, SOFT, 'Bold'), cx, 510); put(fr, badge('?', 46), cx, 590)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 색 1 · 사라짐 2 · 이동 0 · 크기 3이면', ('암호 1203', YEL), '', ('한 물건은 한 가지만 바뀌었어요', SOFT)], 34, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', 'A 색 · B 사라짐 · C 이동 · D 크기')
pic(fr, 'p1', 540, 515, 820, '그림 1'); pic(fr, 'p2', 540, 940, 820, '그림 2')
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '작은 것과 벽에 걸린 것도 보세요', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('액자 속 그림도 물건이에요', WHITE), '책은 한 권씩 세어 보세요.', '옮긴 물건은 원래 자리가 비어 있어요.',
                          ('시계와 화분 크기도 비교해요!', YEL)], 35)
pic(fr, 'p1', 540, 880, 820, '그림 1')
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '달라진 곳 8군데에 노란 원')
pic(fr, 'a2', 540, 560, 900)
fr.alpha_composite(panel(960, 270), (60, 860))
text_lines(fr, 100, 885, ['A 색 2: 파란 책 → 빨강, 노란 공 → 초록', 'B 사라짐 3: 보라 책, 보라 큐브, 액자 속 해', 'C 이동 1: 머그컵',
                          'D 크기 2: 화분 커짐, 시계 작아짐'], 31)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', '색 2 · 사라짐 3 · 이동 1 · 크기 2')
pic(fr, 'a2', 540, 520, 760)
for n, (k, t) in enumerate(KINDS):
    cx = 165 + n * 250; put(fr, text_layer(t, 26, SOFT, 'Bold'), cx, 790); put(fr, badge(CODE[n], 46), cx, 860)
put(fr, text_layer(' '.join(CODE), 140, MINT, glow=MINT), 540, 1040)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
