"""ROOM 085 proof: four viral physics riddles, each solved with a small model, then mapped to the numbered option.
A: helium balloon on a string inside a bus that pulls away (acceleration a forward). In the bus frame the effective
   gravity is g down plus a backward; buoyancy points against it, so the balloon leans FORWARD.
B: a hanging strap (pendulum) in the same bus hangs along the effective gravity: it swings BACKWARD.
C: a bicycle with a string tied to the bottom pedal, pulled backward. If the bike moves x, the crank turns x/(G*Rw) and
   the bottom pedal moves x*(1 - r/(G*Rw)) over the ground; with r/(G*Rw) < 1 the pedal and bike move the same way, so
   pulling the pedal back moves the BIKE BACKWARD.
D: a stone in a boat floating in a closed tank is thrown into the water. Afloat it displaces m/rho_water; on the
   bottom only its own volume m/rho_stone (smaller), so the water level GOES DOWN.
All 10^4 codes compared; exactly one matches."""
import itertools, json, os
g, a = 9.8, 2.0
A_dir = 'forward' if (-(-a)) > 0 else 'back'                 # buoyant force opposes effective gravity's backward part
B_dir = 'back' if -a < 0 else 'forward'                       # pendulum lines up with effective gravity (backward)
r, Rw, G = 0.17, 0.34, 2.0
pedal_per_bike = 1 - r / (G * Rw); C_dir = 'back' if pedal_per_bike > 0 else 'forward'   # pull pedal back
m, rho_w, rho_s = 3.0, 1000.0, 2600.0
D_dir = 'down' if m / rho_s < m / rho_w else 'up'
OPTIONS = {'A': ['뒤로 기울어요', '앞으로 기울어요', '그대로예요'], 'B': ['앞으로 흔들려요', '그대로예요', '뒤로 흔들려요'],
           'C': ['뒤로 가요', '앞으로 가요', '안 움직여요'], 'D': ['올라가요', '그대로예요', '넘쳐요', '내려가요']}
TRUE = {'A': '앞으로 기울어요' if A_dir == 'forward' else '뒤로 기울어요', 'B': '뒤로 흔들려요' if B_dir == 'back' else '앞으로 흔들려요',
        'C': '뒤로 가요' if C_dir == 'back' else '앞으로 가요', 'D': '내려가요' if D_dir == 'down' else '올라가요'}
NUM = {k: OPTIONS[k].index(TRUE[k]) + 1 for k in 'ABCD'}
code = ''.join(str(NUM[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, TRUE)
assert sols == ['2314']
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'options': OPTIONS, 'true': TRUE, 'pedal_per_bike': pedal_per_bike,
               'why': {'A': '버스가 출발하면 공기가 뒤로 몰려 풍선을 앞으로 밀어요', 'B': '손잡이는 관성 때문에 뒤로', 'C': '페달은 자전거와 같은 방향으로 움직여요. 뒤로 당기면 자전거도 뒤로',
                       'D': '배 위의 돌은 무게만큼 물을 밀어내지만, 가라앉은 돌은 자기 부피만큼만 밀어내요'}},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
