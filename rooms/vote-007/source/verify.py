"""VOTE 007 proof (얼음 한 덩이 vs 부순 얼음): same mass of ice (100 g) in the same drink, as one big cube or crushed into
small pieces. Heat flows into the ice through its surface, so the cooling rate scales with the total surface area. Cutting
a cube of side L into n^3 cubes of side L/n multiplies the surface by n: 100 g cube (L = 4.8 cm) has 138 cm^2; crushed
into 1 cm pieces about 657 cm^2, ~4.8x. Same mass also means the same total cooling in the end (same latent heat), but
the crushed ice gets there much faster."""
import json, os
RHO = 0.917; M = 100.0
L = (M / RHO) ** (1 / 3); big = 6 * L * L
n = L / 1.0; small = 6 * L * L * n
assert small > 4 * big
ANSWER = 'B'; OPTIONS = {'A': '큰 덩이', 'B': '부순 얼음', 'C': '똑같다'}
print('surface', round(big), 'vs', round(small), 'cm2; answer', ANSWER)
if __name__ == '__main__':
    json.dump({'answer': ANSWER, 'options': OPTIONS, 'surface_cm2': {'big': round(big), 'crushed_1cm': round(small)},
               'why': '열은 얼음 겉면으로 들어가요. 같은 양이라도 잘게 부수면 겉넓이가 몇 배라 훨씬 빨리 차가워져요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
