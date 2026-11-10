"""ROOM 169 proof: a train and a tunnel (or bridge). The train is T m long and runs at v m per second; the tunnel is L m
long. Simulating the front of the train second by second (0.01 s steps): 'pass' = from the moment the front enters
until the tail leaves (front moves L + T); 'hidden' = how long the whole train is inside at once (front moves L - T).
Digit = those seconds. All 10^4 codes compared; exactly one matches. The trap: L / v, forgetting the train's own
length."""
import itertools, json, os

BOARDS = {'A': {'kind': 'tunnel', 'L': 40, 'T': 20, 'v': 10, 'ask': 'pass'},
          'B': {'kind': 'bridge', 'L': 30, 'T': 15, 'v': 5, 'ask': 'pass'},
          'C': {'kind': 'tunnel', 'L': 60, 'T': 20, 'v': 20, 'ask': 'pass'},
          'D': {'kind': 'tunnel', 'L': 80, 'T': 20, 'v': 20, 'ask': 'hidden'}}


def sim(b):
    dt = 0.01; t = 0.0; first = None; last = None
    while t < 100:
        front = b['v'] * t  # front at the entrance at t = 0, tunnel spans [0, L]
        tail = front - b['T']
        cond = (front > 0 and tail < b['L']) if b['ask'] == 'pass' else (tail >= 0 and front <= b['L'])
        if cond:
            first = t if first is None else first; last = t
        t = round(t + dt, 2)
    return round(last - first + (0 if b['ask'] == 'hidden' else dt))


GOOD = {k: sim(b) for k, b in BOARDS.items()}
TRAPV = {k: b['L'] // b['v'] for k, b in BOARDS.items()}
code = ''.join(str(GOOD[k]) for k in 'ABCD'); trap = ''.join(str(TRAPV[k]) for k in 'ABCD')
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap, GOOD)
assert len(sols) == 1 and all(GOOD[k] != TRAPV[k] for k in 'ABCD')
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'seconds': GOOD, 'trap_no_train_length': trap,
               'why': '기차가 다 지나가려면 꼬리까지 나와야 해서 터널 + 기차 길이만큼 달려요. 완전히 숨는 시간은 터널 - 기차 길이예요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
