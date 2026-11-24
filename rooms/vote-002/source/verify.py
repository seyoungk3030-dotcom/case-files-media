"""VOTE 002 proof (얼음에 소금): ice at 0 C with salt sprinkled on it. Salt water freezes lower than 0 C (freezing point
depression, ~ -1.86 C per mol/kg of dissolved particles; NaCl gives 2 particles). Ice touching the brine melts, and the
latent heat for that melting (334 J/g) comes from the mixture itself, so its temperature drops until it reaches the brine's
freezing point (down to the NaCl-water eutectic, about -21 C). This is how old-style ice-cream makers freeze cream."""
import json, os
KF, I = 1.86, 2
for m in (1.0, 2.0, 3.0):           # mol NaCl per kg water
    fp = -KF * I * m; assert fp < 0
EUTECTIC = -21.1
ANSWER = 'B'; OPTIONS = {'A': '올라간다', 'B': '내려간다', 'C': '그대로'}
print('fp at 1 mol/kg', -KF * I, 'C; eutectic', EUTECTIC, 'C; answer', ANSWER)
if __name__ == '__main__':
    json.dump({'answer': ANSWER, 'options': OPTIONS, 'eutectic_C': EUTECTIC,
               'why': '소금물은 0도보다 낮아야 얼어요. 얼음이 녹으면서 주변 열을 빼앗아, 영하 20도 근처까지 내려가요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
