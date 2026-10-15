# Exhaustive proof: ROOM 011 clues -> unique grid
import itertools,json
P=list(itertools.permutations([1,2,3,4]))
def vis(s):
    m=c=0
    for x in s:
        if x>m:m=x;c+=1
    return c
CL={('T',0):2,('T',2):3,('R',0):1,('R',2):4}
sols=[];tested=0
for g in itertools.product(P,repeat=4):
    tested+=1
    cols=list(zip(*g))
    if any(sorted(c)!=[1,2,3,4] for c in cols):continue
    d={}
    for i in range(4):
        d[('T',i)]=vis(cols[i]);d[('R',i)]=vis(g[i][::-1])
    if all(d[k]==v for k,v in CL.items()): sols.append(g)
print(tested,sols)
ans=''.join(map(str,sols[0][1]))
json.dump({"unique_answer":ans,"tested_grids":tested,"clues":{f"{k[0]}{k[1]}":v for k,v in CL.items()},"solutions":sols,"answer_row":"row 2 (★), read left to right"},open('/tmp/claude-0/-home-user/ff5d81e2-b122-5317-9c96-5741cd50015f/scratchpad/r11/proof.json','w'),indent=1)
print(ans)
