"""VOTE 001 proof (냉장고 문 열어두기): a fridge in a closed room with its door open. The fridge is a heat pump: it moves
heat Q from its inside to the coil, and the compressor adds its electric energy W, so the coil gives off Q + W. With the
door open, its "inside" is the room itself, so the room loses Q at the door and gains Q + W at the coil: net +W. The room
warms. Example: 150 W for 1 hour into the air of a 30 m^3 room (walls ignored) = +15 K of air heating budget."""
import json, os
W, HOURS, VOL, RHO, CP = 150.0, 1.0, 30.0, 1.2, 1005.0
Q = 400.0                                   # any heat moved at the door; it cancels
net = -Q + (Q + W)
assert abs(net - W) < 1e-9 and net > 0
dT_air = W * HOURS * 3600 / (VOL * RHO * CP)
ANSWER = 'C'
OPTIONS = {'A': '시원해진다', 'B': '그대로', 'C': '더워진다'}
print('net', net, 'W; air budget', round(dT_air, 1), 'K; answer', ANSWER)
if __name__ == '__main__':
    json.dump({'answer': ANSWER, 'options': OPTIONS, 'net_watts': net, 'air_dT_1h_K': round(dT_air, 1),
               'why': '문 앞에서 뺏은 열을 뒤쪽 코일로 다시 방에 버리고, 모터가 쓴 전기만큼 열이 더 나와요. 그래서 방은 더워져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
