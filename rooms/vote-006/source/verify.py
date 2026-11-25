"""VOTE 006 proof (체중계 위 한 발): a person stands still on a bathroom scale, first on two feet, then on one foot.
Standing still, the forces on the person balance: the scale's push N equals the weight m g however it is spread over
the feet (one foot: the same N on a smaller area, so more pressure, not more force). The scale reads N / g = m.
Only moving (bending, hopping) changes the reading for a moment."""
import json, os
m, g = 60.0, 9.81
for feet in (2, 1):
    per_foot = m * g / feet; N = per_foot * feet
    assert abs(N - m * g) < 1e-9
ANSWER = 'B'; OPTIONS = {'A': '한 발이 더 무겁다', 'B': '똑같다', 'C': '두 발이 더 무겁다'}
print('reading', m, 'kg either way; answer', ANSWER)
if __name__ == '__main__':
    json.dump({'answer': ANSWER, 'options': OPTIONS, 'reading_kg': m,
               'why': '가만히 서 있으면 체중계가 받치는 힘은 몸무게와 같아요. 한 발이면 누르는 넓이만 줄어 압력이 커질 뿐이에요'},
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'notes', 'proof.json'), 'w'), ensure_ascii=False, indent=1)
