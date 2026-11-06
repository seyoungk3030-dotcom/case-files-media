"""ROOM 152 cards in the 3D style (kit/style3d.py), from the mancala sprites made by scene3d.py. All sprites are
cropped to one shared box (q*/r*.png)."""
import json, os, sys
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit')); sys.path.insert(0, HERE)
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 152, '2026.12.04'
PROOF = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))
CODE = PROOF['unique_answer']; TRAP = PROOF['trap_no_capture']
ims = {f'{s}{k}': Image.open(f'{B}/{s}{k}.png').convert('RGBA') for s in 'pa' for k in 'ABCD'}
bb = [im.getchannel('A').getbbox() for im in ims.values()]
BOX = (min(b[0] for b in bb) - 10, min(b[1] for b in bb) - 10, max(b[2] for b in bb) + 10, max(b[3] for b in bb) + 10)
for n, im in ims.items():
    c = im.crop(BOX); c.putpixel((0, 0), (255, 255, 255, 44)); c.putpixel((c.width - 1, c.height - 1), (255, 255, 255, 44))
    c.save(f'{B}/{"q" if n[0] == "p" else "r"}{n[1]}.png')


def one(fr, name, cx, cy, w, tag=True, val=None):
    im = Image.open(f'{B}/{name}.png'); sc = w / im.width; im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    x0, y0 = cx - im.width / 2, cy - im.height / 2; fr.alpha_composite(im, (int(x0), int(y0)))
    if tag: put(fr, pill(name[1], 32, INK, (244, 246, 250, 245), (16, 5)), x0 + 22, y0 + 34)
    if val: put(fr, badge(val, 44), x0 + im.width - 40, y0 + 40)


POS = [(540, 410), (540, 625), (540, 840), (540, 1055)]


def four(fr, pre, w=470, vals=None):
    for i, k in enumerate('ABCD'): one(fr, pre + k, POS[i][0], POS[i][1], w, val=vals[i] if vals else None)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'

fr = card(ROOM, DATE, 1, 7, '내 창고에 씨앗이 몇 개?', '노란 고리 칸의 씨앗을 모두 집어 뿌려요')
four(fr, 'q', 700)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

fr = card(ROOM, DATE, 2, 7, '만칼라 규칙', '아래 줄이 내 칸, 오른쪽 끝이 내 창고')
fr.alpha_composite(panel(960, 300), (60, 290))
text_lines(fr, 100, 322, ['집은 씨앗을 오른쪽으로 한 칸에 하나씩 (시계 반대)', '내 창고엔 넣고, 상대 창고는 건너뛰어요',
                          '마지막 씨앗이 내 쪽 빈 칸에 떨어지면 → 그 씨앗과', ('맞은편 씨앗을 모두 내 창고로! 창고 씨앗 수가 숫자', YEL)], 30)
one(fr, 'qA', 540, 880, 900, tag=False)
cta(fr, CTA4); save(fr, 2)

fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A B C D 순서로 내 창고 씨앗 수')
for n, k in enumerate('ABCD'):
    cx = 165 + n * 250; put(fr, pill(k, 40, INK, (244, 246, 250, 250), (26, 10)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 300), (60, 700))
text_lines(fr, 540, 735, ['예: 2 · 6 · 0 · 9개면', ('암호 2609', YEL), '', ('수천 년 된 아프리카 씨앗 게임', SOFT)], 36, center=True)
cta(fr, CTA4); save(fr, 3)

fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '마지막 씨앗이 어디에 떨어지는지가 핵심')
four(fr, 'q', 700)
cta(fr, CTA4); save(fr, 4)

fr = card(ROOM, DATE, 5, 7, '힌트', '빈 칸 + 마지막 씨앗 = 따먹기', CORAL)
fr.alpha_composite(panel(960, 300), (60, 300))
text_lines(fr, 100, 330, [('A: 씨앗 2개 → 오른쪽 두 칸에 하나씩', WHITE), '마지막이 빈 칸! 맞은편 4개 + 자기 1개',
                          '= 내 창고에 5개', ('창고에 직접 넣은 것만 세면 함정!', YEL)], 33)
one(fr, 'qA', 540, 880, 900, tag=False)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '빨간 고리 = 따먹은 칸 · 민트 숫자 = 내 창고')
four(fr, 'r', 700, vals=list(CODE))
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

fr = card(ROOM, DATE, 7, 7, '탈출 성공', f"함정 답은 {TRAP}")
one(fr, 'qC', 540, 430, 780, tag=False); one(fr, 'rC', 540, 680, 780, tag=False)
fr.alpha_composite(panel(960, 230), (60, 830))
text_lines(fr, 100, 860, ['C: 10개가 한 바퀴 돌아 내 둘째 칸에 끝', '창고 1개 + 따먹기 6개 = 7개!'], 31)
put(fr, text_layer(' '.join(CODE), 96, MINT, glow=MINT), 540, 1135)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
