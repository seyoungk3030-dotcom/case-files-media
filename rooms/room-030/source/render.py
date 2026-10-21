"""ROOM 030 cards in the 3D style (kit/style3d.py), from sprites made by scene3d.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE, T = 30, '2026.10.21', '바닥에 닿은 숫자'
CODE = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))['unique_answer']
COUNTS = dict(zip('ABCD', CODE))
COLS = {'A': (109, 218, 197), 'B': (255, 180, 70), 'C': (160, 150, 255), 'D': (240, 120, 110)}


def letter(k): return pill(k, 34, INK, (*COLS[k], 245), (24, 8))


def grid(fr, kind, y0, w, gap_y, show=None):
    for n, k in enumerate('ABCD'):
        sp = sprite(f'{B}/{kind}-{k}.png', width=w)
        cx = 290 + (n % 2) * 500; cy = y0 + (n // 2) * gap_y
        put(fr, sp, cx, cy)
        put(fr, letter(k), cx - w / 2 + 10, cy - sp.height / 2 + 20)
        if show: put(fr, badge(COUNTS[k] if show == 'num' else '?', 44), cx + w / 2 - 20, cy - sp.height / 2 + 30)


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


# 1 hook
fr = card(ROOM, DATE, 1, 7, '바닥에 닿은 숫자는?', '보이는 숫자를 읽으면 틀린다')
grid(fr, 'die', 520, 400, 470, '?')
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules + example
fr = card(ROOM, DATE, 2, 7, '규칙은 하나', '마주 보는 두 면의 합은 항상 7')
fr.alpha_composite(panel(960, 220), (60, 290))
text_lines(fr, 100, 322, ['1. 네 개 모두 평범한 주사위 (1~6)', '2. 마주 보는 면: 1과 6, 2와 5, 3과 4',
                          ('3. 암호 = 땅에 닿은 바닥 면의 숫자', YEL)], 36)
put(fr, sprite(f'{B}/die-ex.png', width=430), 290, 790); put(fr, sprite(f'{B}/bottom-ex.png', width=330), 790, 790)
put(fr, text_layer('→', 80, YEL), 540, 790)
put(fr, text_layer('윗면이 2라면', 36, WHITE, 'Bold'), 290, 1040)
put(fr, text_layer('바닥은 5', 36, YEL, 'Bold'), 790, 1040)
put(fr, text_layer('2 + 5 = 7', 30, SOFT, 'Bold'), 790, 1090)
cta(fr, '4장까지 풀고 댓글에 암호를 남겨주세요'); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', 'A → B → C → D 순서로 바닥 면 숫자')
for n, k in enumerate('ABCD'):
    sp = sprite(f'{B}/die-{k}.png', width=240); cx = 165 + n * 250
    put(fr, sp, cx, 560); put(fr, letter(k), cx, 760); put(fr, badge('?', 40), cx, 860)
fr.alpha_composite(panel(960, 220), (60, 960))
text_lines(fr, 540, 990, ['예: 바닥이 A 2, B 5, C 3, D 6이라면', ('암호는 2536', YEL)], 38, center=True)
cta(fr, '4장까지 풀고 댓글에 암호를 남겨주세요'); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
grid(fr, 'die', 445, 380, 360)
fr.alpha_composite(panel(960, 180), (60, 990))
text_lines(fr, 100, 1012, ['평범한 주사위 · 마주 보는 면의 합은 7', '1↔6  ·  2↔5  ·  3↔4', ('암호 = A B C D 바닥 면 숫자', YEL)], 34, gap=1.5)
cta(fr, '4장까지 풀고 댓글에 암호를 남겨주세요'); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', '윗면만 읽으면 3615', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('묻는 건 보이는 면이 아니라 바닥이에요.', WHITE), '바닥은 윗면의 바로 반대쪽 면.',
                          '앞면과 옆면 숫자는 신경 쓰지 않아도 돼요.', ('바닥 = 7 - 윗면', YEL)], 36)
put(fr, sprite(f'{B}/die-B.png', width=460), 540, 890)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer reasoning
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '노랗게 빛나는 면이 바닥')
grid(fr, 'bottom', 480, 270, 370, 'num')
fr.alpha_composite(panel(960, 150), (60, 1010))
text_lines(fr, 540, 1030, ['윗면 3·6·1·5를 7에서 빼면', ('바닥은 4·1·6·2', YEL)], 36, center=True)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', '보이지 않는 면을 읽은 사람만 정답')
for n, k in enumerate('ABCD'):
    sp = sprite(f'{B}/bottom-{k}.png', width=210); cx = 165 + n * 250
    put(fr, sp, cx, 520); put(fr, badge(COUNTS[k], 44), cx, 700)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 830)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 960)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
