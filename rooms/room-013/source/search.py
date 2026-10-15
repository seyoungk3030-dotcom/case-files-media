import itertools, datetime
WD='월화수목금토일'
def wd(d): return datetime.date(2026,11,d).weekday()
pairs=[(a,b) for a in range(10,31) for b in range(10,31) if a<b]
C={
 'same_wd':('두 날짜는 같은 요일', lambda a,b: wd(a)==wd(b)),
 'gap14':('두 날짜는 정확히 2주 차이', lambda a,b: b-a==14),
 'gap7':('두 날짜는 정확히 1주 차이', lambda a,b: b-a==7),
 'weekend1':('첫 날은 주말', lambda a,b: wd(a)>=5),
 'weekday1':('첫 날은 평일', lambda a,b: wd(a)<5),
 'wed1':('첫 날은 수요일', lambda a,b: wd(a)==2),
 'fri2':('두 번째 날은 금요일', lambda a,b: wd(b)==4),
 'sum_digits_eq':('두 날짜의 숫자 합이 같다', lambda a,b: sum(map(int,str(a)))==sum(map(int,str(b)))),
 'b_even':('두 번째 날짜는 짝수', lambda a,b: b%2==0),
 'a_odd':('첫 날짜는 홀수', lambda a,b: a%2==1),
 'distinct':('네 숫자가 모두 다르다', lambda a,b: len(set(f'{a}{b}'))==4),
 'no_zero':('0은 쓰지 않는다', lambda a,b: '0' not in f'{a}{b}'),
 'a_lt_20':('첫 날은 20일 전', lambda a,b: a<20),
 'b_gt_20':('두 번째 날은 20일 이후', lambda a,b: b>20),
 'last_week':('두 번째 날은 마지막 주', lambda a,b: b>=29 or (b>=23 and wd(b)>=0 and b>=23)),
 'sum_40':('두 날짜를 더하면 40', lambda a,b: a+b==40),
 'digsum_a_eq_last_b':('첫 날짜 숫자 합 = 두 번째 날짜 끝자리', lambda a,b: sum(map(int,str(a)))==b%10),
}
keys=list(C)
res=[]
for n in (3,4):
  for comb in itertools.combinations(keys,n):
    s=[p for p in pairs if all(C[k][1](*p) for k in comb)]
    if len(s)==1:
        # minimal: each clue necessary
        if all(len([p for p in pairs if all(C[k][1](*p) for k in comb if k!=x)])>1 for x in comb):
            res.append((comb,s[0]))
for r in res[:60]: print(r[1],[C[k][0] for k in r[0]])
print(len(res))
