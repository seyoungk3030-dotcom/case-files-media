"""VOTE 004 proof (얼음물 컵의 물방울): water beads on the outside of a glass of ice water. Glass is watertight, so it is not
seeping (A wrong). The ice is inside and the outer wall stays dry if the glass is empty but cold (an empty glass taken
from the freezer also fogs), so it is not the ice (C wrong). Air holds water vapour; on the cold wall the air cools below
its dew point and the vapour condenses (B). Check with Magnus formula: room 25 C at 60 % RH has a dew point ~16.7 C,
and the glass wall sits near 5 C, well below it."""
import json, math, os
a, b = 17.62, 243.12
def dew(T, rh): g = math.log(rh / 100) + a * T / (b + T); return b * g / (a - g)
dp = dew(25, 60); WALL = 5.0
assert WALL < dp
ANSWER = 'B'; OPTIONS = {'A': '컵 속 물이 스며나옴', 'B': '공기 속 수증기', 'C': '얼음이 녹아서'}
print('dew point', round(dp, 1), 'C; answer', ANSWER)
if __name__ == '__main__':
    json.dump({'answer': ANSWER, 'options': OPTIONS, 'dew_point_C': round(dp, 1), 'wall_C': WALL,
               'why': '차가운 컵 표면에서 공기가 이슬점 아래로 식어, 공기 속 수증기가 물방울로 맺혀요. 유리는 물이 새지 않아요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
