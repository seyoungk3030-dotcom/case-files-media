import itertools, random
L='ABCD'
codes=[c for c in itertools.product(range(1,10),repeat=4) if len(set(c))==4]
def mk():
    t=random.choice(['sum2','dbl','gt','par','max','min','diff','eq'])
    i,j,k=random.sample(range(4),3)
    if t=='sum2': return (f'{L[i]} + {L[j]} = {L[k]}', lambda c,i=i,j=j,k=k:c[i]+c[j]==c[k])
    if t=='dbl': return (f'{L[i]}는 {L[j]}의 두 배', lambda c,i=i,j=j:c[i]==2*c[j])
    if t=='gt': return (f'{L[i]}는 {L[j]}보다 크다', lambda c,i=i,j=j:c[i]>c[j])
    if t=='par':
        e=random.choice([0,1]); return (f'{L[i]}는 {"짝수" if e==0 else "홀수"}', lambda c,i=i,e=e:c[i]%2==e)
    if t=='max': return (f'{L[i]}가 가장 크다', lambda c,i=i:c[i]==max(c))
    if t=='min': return (f'{L[i]}가 가장 작다', lambda c,i=i:c[i]==min(c))
    if t=='diff':
        d=random.randint(1,5); return (f'{L[i]} - {L[j]} = {d}', lambda c,i=i,j=j,d=d:c[i]-c[j]==d)
    if t=='eq':
        v=random.randint(1,9); return (f'{L[i]} = {v}', lambda c,i=i,v=v:c[i]==v)
random.seed(12)
best=[]
for trial in range(200000):
    st=[mk() for _ in range(5)]
    if len({s[0] for s in st})<5: continue
    if sum(1 for s in st if s[0].split()[0] in L and '=' in s[0] and s[0].count(' ')==2)>0: continue  # no direct X = v
    sols=[]
    for c in codes:
        truth=[s[1](c) for s in st]
        if truth.count(False)==1: sols.append((c,truth.index(False)))
        if len(sols)>1: break
    if len(sols)!=1: continue
    if any(all(s[1](c) for s in st) for c in codes): continue
    # a directly contradictory pair
    pairs=[(a,b) for a,b in itertools.combinations(range(5),2) if not any(st[a][1](c) and st[b][1](c) for c in codes)]
    if not pairs: continue
    best.append(([s[0] for s in st],sols[0],pairs))
    if len(best)>=12: break
for b in best: print(b)
