import json, math, numpy as np
exec(open('analysis.py').read().split("withg=[d for d in data if d['gdp']]")[0])
for d in data:
    iso=d['iso']; d['pop']=wb['pop'].get(iso,[None,None,None])[2] if iso else None
    d['usd']=wb['gdpusd'].get(iso,[None,None,None])[2] if iso else None
    d['inc']=wb['inc'].get(iso) if iso else None
P=['Policy Capacity','AI Infrastructure','Governance','Public Sector Adoption','Development & Diffusion','Resilience']
rng=np.random.default_rng(42)
def fit(rows, xs, j):
    X=np.column_stack([np.ones(len(rows))]+[np.array([f(d) for d in rows]) for f in xs])
    y=np.array([d['pillars'][j] if j is not None else -d['rank'] for d in rows])
    b,*_=np.linalg.lstsq(X,y,rcond=None); res=y-X@b; return b,res,X,y
def india_gap(rows, xs, j):
    b,res,X,y=fit(rows,xs,j); ind=[k for k,d in enumerate(rows) if d['iso']=='IND'][0]
    g=res[ind]; sd=res.std(); pct=(res<g).mean()*100
    return g, g/sd, pct
lg=lambda d: math.log(d['gdp']); lp=lambda d: math.log(d['pop']); lu=lambda d: math.log(d['usd'])
base=[d for d in data if d['gdp']]
spec={}
spec['A. Baseline: log GDPpc (PPP)']=(base,[lg])
spec['B. + log population']=([d for d in base if d['pop']],[lg,lp])
spec['C. Income in current US$']=([d for d in data if d['usd']],[lu])
spec['D. Excl. small states (<1m pop)']=([d for d in base if d['pop'] and d['pop']>=1e6],[lg,lp])
spec['E. Low & middle income only']=([d for d in base if d['pop'] and d['inc'] in ('Low income','Lower middle income','Upper middle income')],[lg,lp])
out={}
for name,(rows,xs) in spec.items():
    out[name]={'n':len(rows)}
    for j,p in enumerate(P):
        g,z,pct=india_gap(rows,xs,j); out[name][p]=(round(g,1),round(z,2),round(pct))
    g,z,pct=india_gap(rows,xs,None); out[name]['rank_resid_pct']=round(pct)
for name,v in out.items():
    print(name,'n=',v['n']); print('   ',{p[:12]:v[p] for p in P}, 'overall pct',v['rank_resid_pct'])
# bootstrap CI for baseline and spec B gaps
for name in ['A. Baseline: log GDPpc (PPP)','B. + log population']:
    rows,xs=spec[name]; ind=[k for k,d in enumerate(rows) if d['iso']=='IND'][0]
    cis={}
    for j,p in enumerate(P):
        gs=[]
        for _ in range(2000):
            idx=rng.integers(0,len(rows),len(rows)); idx=np.append(idx,ind)
            sub=[rows[i] for i in idx]
            X=np.column_stack([np.ones(len(sub))]+[np.array([f(d) for d in sub]) for f in xs]); y=np.array([d['pillars'][j] for d in sub])
            b,*_=np.linalg.lstsq(X,y,rcond=None)
            xi=np.array([1]+[f(rows[ind]) for f in xs]); gs.append(rows[ind]['pillars'][j]-xi@b)
        cis[p]=(round(np.percentile(gs,2.5),1),round(np.percentile(gs,97.5),1))
    print('CI',name,cis); out[name]['ci']=cis
# rank of governance among pillars by z in each spec
for name,v in out.items():
    zs={p:v[p][1] for p in P}; print(name,'lowest z:',min(zs,key=zs.get), zs[min(zs,key=zs.get)])
# income peers at different bands
ind=[d for d in base if d['iso']=='IND'][0]
for band in (0.25,0.5):
    peers=[d for d in base if (1-band)*ind['gdp']<=d['gdp']<=(1+band)*ind['gdp']]
    peers.sort(key=lambda d:d['rank']); print('band',band,len(peers),'India pos',[d['iso'] for d in peers].index('IND')+1, 'gov rank among peers',sorted([-d['pillars'][2] for d in peers]).index(-ind['pillars'][2])+1)
# lower-middle income group
lmi=[d for d in data if d['inc']=='Lower middle income']; lmi.sort(key=lambda d:d['rank'])
print('LMI n',len(lmi),'India pos',[d['iso'] for d in lmi].index('IND')+1,'top3',[(d['name'],d['rank']) for d in lmi[:3]])
gov=sorted(lmi,key=lambda d:-d['pillars'][2]); print('India gov rank in LMI',[d['iso'] for d in gov].index('IND')+1,'of',len(lmi))
# populous countries (>100m)
big=[d for d in data if d['pop'] and d['pop']>1e8]; big.sort(key=lambda d:d['rank']); print('pop>100m',[(d['name'][:14],d['rank']) for d in big])
# R&D vs D&D controlling income
wr=[d for d in data if d['rd'] and d['gdp'] and d['pop']]
X=np.column_stack([np.ones(len(wr)),[d['rd'] for d in wr],[math.log(d['gdp']) for d in wr]]); y=np.array([d['pillars'][4] for d in wr])
b,*_=np.linalg.lstsq(X,y,rcond=None); res=y-X@b
# partial correlation
def resid(v,Z): bb,*_=np.linalg.lstsq(Z,v,rcond=None); return v-Z@bb
Z=np.column_stack([np.ones(len(wr)),[math.log(d['gdp']) for d in wr]])
r1=resid(np.array([d['rd'] for d in wr]),Z); r2=resid(y,Z); pc=np.corrcoef(r1,r2)[0,1]
raw=np.corrcoef([d['rd'] for d in wr],y)[0,1]
# bootstrap coefficient on R&D
bs=[]
for _ in range(2000):
    idx=rng.integers(0,len(wr),len(wr)); bb,*_=np.linalg.lstsq(X[idx],y[idx],rcond=None); bs.append(bb[1])
print('RD->DD n',len(wr),'raw r',round(raw,2),'partial r|income',round(pc,2),'coef per 1pp R&D',round(b[1],1),'CI',round(np.percentile(bs,2.5),1),round(np.percentile(bs,97.5),1),'income coef',round(b[2],1))
xs_rank_mean=None
json.dump(out,open('robust_out.json','w'),indent=1,default=str)
