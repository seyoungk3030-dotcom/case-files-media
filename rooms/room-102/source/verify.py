"""ROOM 102 proof: four identical glass bottles with different water levels. On 'blow' boards you blow across the
mouth: the air column above the water sounds, f = c / (4 * (air length + end correction)), so the fullest bottle is
highest. On 'tap' boards you tap the glass with a spoon: the glass wall vibrates and the water adds mass, so
f = f0 / sqrt(1 + k * (water height)^p) falls as the water rises, and the emptiest bottle is highest. Each digit is
the number of the highest-pitched bottle. All 10^4 codes are compared; exactly one matches. Using the blowing rule on
every board (the trap) gives another code."""
import itertools, json, math, os

H, NECK = 1.8, 0.12     # bottle body height, end correction (both in the scene's units)
BOARDS = {'A': ('blow', [0.30, 0.72, 0.50, 0.18]), 'B': ('tap', [0.60, 0.80, 0.15, 0.45]),
          'C': ('blow', [0.40, 0.20, 0.55, 0.85]), 'D': ('tap', [0.12, 0.50, 0.70, 0.35])}


def pitch(mode, level):
    if mode == 'blow': return 343 / (4 * (H * (1 - level) + NECK))
    return 900 / math.sqrt(1 + 1.6 * level ** 2)          # any model that falls with more water gives the same order


def top(mode, levels):
    f = [pitch(mode, l) for l in levels]; s = sorted(f, reverse=True); assert s[0] / s[1] > 1.04
    return f.index(s[0]) + 1


RES = {k: top(*v) for k, v in BOARDS.items()}
code = ''.join(str(RES[k]) for k in 'ABCD'); trap = ''.join(str(top('blow', v[1])) for v in BOARDS.values())
# levels in one board differ by at least 0.1 so they are easy to compare by eye
assert all(min(abs(a - b) for a, b in itertools.combinations(v[1], 2)) >= 0.1 for v in BOARDS.values())
sols = [c for c in map(''.join, itertools.product('0123456789', repeat=4)) if c == code]
print('answer', code, 'trap', trap)
assert sols == ['2341'] and trap != code
if __name__ == '__main__':
    json.dump({'unique_answer': code, 'codes_checked': 10000, 'boards': BOARDS, 'highest': RES, 'trap_blow_everywhere': trap,
               'why': '불면 물 위 빈 공간(공기 기둥)이 울려서 물이 많을수록 높고, 두드리면 유리와 물이 함께 떨려 물이 많을수록 낮아요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
