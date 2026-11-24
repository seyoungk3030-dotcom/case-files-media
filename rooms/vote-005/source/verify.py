"""VOTE 005 proof (컵 밑 종이 휙 당기기): a full cup (m = 0.3 kg) stands on a paper strip; the strip is yanked out in
t = 0.05 s. Kinetic friction mu_k = 0.3 drags the cup only while the paper slides under it: a = mu_k * g = 2.94 m/s^2,
so in 0.05 s the cup moves a t^2 / 2 = 3.7 mm and gains v = 0.15 m/s, then slides on the table and stops within
v^2 / (2 mu g) = 3.7 mm more. Total ~7 mm: the cup stays practically in place (inertia). Pulled slowly, static friction
keeps the cup on the paper and it comes along. It does not tip: friction at the base is far below what tipping a
cup 10 cm tall and 7 cm wide needs (mu < w/h = 0.7)."""
import json, os
MU, G, T, W, H = 0.3, 9.81, 0.05, 0.07, 0.10
a = MU * G; d1 = a * T * T / 2; v = a * T; d2 = v * v / (2 * MU * G); total = d1 + d2
assert total < 0.01 and MU < W / H
ANSWER = 'B'; OPTIONS = {'A': '컵도 딸려온다', 'B': '컵은 거의 제자리', 'C': '컵이 넘어진다'}
print('cup moves', round(total * 1000, 1), 'mm; answer', ANSWER)
if __name__ == '__main__':
    json.dump({'answer': ANSWER, 'options': OPTIONS, 'cup_moves_mm': round(total * 1000, 1),
               'why': '아주 짧은 시간만 마찰이 작용해서 컵은 거의 움직이지 못해요(관성). 천천히 당기면 컵이 따라와요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
