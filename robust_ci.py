import json, math, numpy as np
exec(open('robust.py').read().split("out={}")[0])
rng=np.random.default_rng(7)
res={}
for name,(rows,xs) in spec.items():
    ind=[k for k,d in enumerate(rows) if d['iso']=='IND'][0]
    X=np.column_stack([np.ones(len(rows))]+[np.array([f(d) for d in rows]) for f in xs])
    xi=X[ind]
    res[name]={}
    for j,p in enumerate(P):
        y=np.array([d['pillars'][j] for d in rows])
        b,*_=np.linalg.lstsq(X,y,rcond=None); g=y[ind]-xi@b
        gs=[]
        for _ in range(2000):
            idx=np.append(rng.integers(0,len(rows),len(rows)),ind)
            bb,*_=np.linalg.lstsq(X[idx],y[idx],rcond=None); gs.append(y[ind]-xi@bb)
        res[name][p]=(round(float(g),1),round(float(np.percentile(gs,2.5)),1),round(float(np.percentile(gs,97.5)),1))
for n,v in res.items(): print(n, v)
json.dump(res,open('robust_ci_points.json','w'),indent=1)
