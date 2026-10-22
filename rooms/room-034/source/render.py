"""ROOM 034 cards in the 3D style (kit/style3d.py), from sprites made by scene3d.py."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '../../../kit'))
from style3d import *
B = os.path.join(HERE, '..', '.build-3d'); OUT = os.path.join(HERE, '..', 'cards')
ROOM, DATE = 34, '2026.10.22'
CODE = json.load(open(os.path.join(HERE, '..', 'notes', 'proof.json')))['unique_answer']


def save(fr, n): fr.convert('RGB').save(f'{OUT}/card-{n:02d}.png')


CTA4 = '4장까지 풀고 댓글에 암호를 남겨주세요'
# 1 hook
fr = card(ROOM, DATE, 1, 7, '성냥 딱 한 개만 옮겨서', '만들 수 있는 가장 큰 수는?')
put(fr, sprite(f'{B}/start.png', width=980), 540, 700)
text_lines(fr, 540, 990, ['빼기만, 더하기만은 안 돼요', ('한 개를 집어서 다른 자리에 놓기', YEL)], 38, center=True)
cta(fr, '도전 → 4장까지  ·  정답 → 6~7장'); save(fr, 1)

# 2 rules + chart
fr = card(ROOM, DATE, 2, 7, '규칙은 세 가지', '숫자 모양은 아래 표 그대로')
fr.alpha_composite(panel(960, 220), (60, 290))
text_lines(fr, 100, 322, ['1. 성냥 한 개를 집어 다른 곳에 놓는다', '2. 네 자리 모두 아래 모양의 숫자여야 한다',
                          ('3. 암호 = 만들 수 있는 가장 큰 수', YEL)], 36)
put(fr, sprite(f'{B}/chart.png', width=820), 540, 790)
text_lines(fr, 540, 1110, [('7은 성냥 3개, 9는 성냥 6개예요', SOFT)], 34, center=True)
cta(fr, CTA4); save(fr, 2)

# 3 code
fr = card(ROOM, DATE, 3, 7, '암호 읽는 법', '만든 네 자리 수가 그대로 암호')
for n in range(4):
    cx = 165 + n * 250; put(fr, pill(f'{n + 1}번째 자리', 30, INK, (244, 246, 250, 245), (18, 8)), cx, 470); put(fr, badge('?', 46), cx, 580)
fr.alpha_composite(panel(960, 330), (60, 700))
text_lines(fr, 540, 735, ['예: 성냥을 옮겨 4321이 되었다면', ('암호는 4321', YEL), '',
                          ('맨 앞자리가 클수록 큰 수예요', SOFT)], 38, center=True)
cta(fr, CTA4); save(fr, 3)

# 4 everything
fr = card(ROOM, DATE, 4, 7, '네 자리 암호는?', '규칙과 그림은 이것이 전부')
put(fr, sprite(f'{B}/start.png', width=840), 540, 520)
put(fr, sprite(f'{B}/chart.png', width=460), 540, 880)
fr.alpha_composite(panel(960, 120), (60, 1045))
text_lines(fr, 540, 1068, ['성냥 딱 한 개를 옮겨 가장 큰 수 만들기', ('암호 = 그 네 자리 수', YEL)], 32, center=True, gap=1.45)
cta(fr, CTA4); save(fr, 4)

# 5 trap
fr = card(ROOM, DATE, 5, 7, '함정 주의', '6을 9로 바꾸면 1910, 하지만 더 큰 수가 있다', CORAL)
fr.alpha_composite(panel(960, 330), (60, 300))
text_lines(fr, 100, 330, [('한 숫자 안에서만 옮기면 1910이 최대예요.', WHITE), '성냥은 다른 자리로 옮겨도 돼요.',
                          '맨 앞자리 1을 키울 방법이', ('있는지 찾아보세요', YEL)], 36)
put(fr, sprite(f'{B}/start.png', width=760), 540, 870)
cta(fr, '다음 장부터 정답 · 먼저 멈춰서 풀어보세요', CORAL); save(fr, 5)

# 6 answer reasoning
fr = card(ROOM, DATE, 6, 7, f'정답 공개 · {CODE}', '6에서 빼서 1 위에 얹기')
put(fr, sprite(f'{B}/start.png', width=640), 540, 470)
put(fr, text_layer('↓', 70, MINT), 540, 640)
put(fr, sprite(f'{B}/answer.png', width=860), 540, 815)
fr.alpha_composite(panel(960, 130), (60, 1040))
text_lines(fr, 540, 1062, ['6의 왼쪽 아래 성냥을 빼면 5', ('그 성냥을 1 위에 얹으면 7 → 7510', YEL)], 33, center=True, gap=1.45)
cta(fr, '맞혔다면 댓글로 인증해 주세요'); save(fr, 6)

# 7 final
fr = card(ROOM, DATE, 7, 7, '탈출 성공', '다른 자리로 옮긴 사람만 정답')
put(fr, sprite(f'{B}/answer.png', width=900), 540, 600)
put(fr, text_layer('암호', 44, SOFT, 'Bold'), 540, 935)
put(fr, text_layer(' '.join(CODE), 160, MINT, glow=MINT), 540, 1060)
cta(fr, '맞혔다면 좋아요 · 다음 방은 팔로우!'); save(fr, 7)
print('cards ok')
