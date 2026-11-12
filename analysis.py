import json, math, statistics as st
rows=json.load(open('gari2025.json')); wb=json.load(open('wb.json'))
byname={}
for k,v in list(wb['gdp'].items())+list(wb['rd'].items()): byname.setdefault(v[0],k)
manual={'Bahamas':'BHS','Bolivia (Plurinational State of)':'BOL',"Côte D'Ivoire":'CIV','Egypt':'EGY','Eritrea':'ERI','Gambia (Republic of The)':'GMB','Guinea Bissau':'GNB','Iran (Islamic Republic of)':'IRN','Kyrgyzstan':'KGZ','Republic':'LAO','Nauru':'NRU','Republic of Korea':'KOR','Republic of Moldova':'MDA','Saint Kitts and Nevis':'KNA','Saint Lucia':'LCA','Grenadines':'VCT','Slovakia':'SVK','Somalia':'SOM','South Sudan':'SSD','State of Palestine':'PSE','Taiwan':None,'Türkiye':'TUR','Britain and Northern Ireland':'GBR','United Republic of Tanzania':'TZA','United States of America':'USA','Republic of':'VEN','Yemen':'YEM'}
P=['Policy Capacity','AI Infrastructure','Governance','Public Sector Adoption','Development & Diffusion','Resilience']
data=[]
for r in rows:
    n=r[0]
    if n=='Congo': iso='COG' if r[1]==178 else 'COD'
    else: iso=manual.get(n, byname.get(n))
    g=wb['gdp'].get(iso) if iso else None
    rd=wb['rd'].get(iso) if iso else None
    data.append(dict(name=n,iso=iso,rank=r[1],pillars=r[2:],gdp=g[2] if g else None,rd=rd[2] if rd else None))
withg=[d for d in data if d['gdp']]
print('countries',len(data),'with gdp',len(withg),'with rd',sum(1 for d in data if d['rd']))
def ols(x,y):
    mx,my=st.mean(x),st.mean(y); b=sum((a-mx)*(c-my) for a,c in zip(x,y))/sum((a-mx)**2 for a in x); a=my-b*mx
    res=[c-(a+b*v) for v,c in zip(x,y)]; sd=st.pstdev(res); r2=1-sum(e*e for e in res)/sum((c-my)**2 for c in y)
    return a,b,sd,r2
ind=[d for d in data if d['iso']=='IND'][0]
out={'pillars':P,'n':len(withg),'india':{}}
x=[math.log(d['gdp']) for d in withg]
for j,p in enumerate(P):
    y=[d['pillars'][j] for d in withg]
    a,b,sd,r2=ols(x,y)
    pred=a+b*math.log(ind['gdp']); act=ind['pillars'][j]
    pct=sum(1 for d in withg if d['pillars'][j]<act)/len(withg)*100
    out['india'][p]=dict(actual=act,expected=round(pred,1),gap=round(act-pred,1),z=round((act-pred)/sd,2),r2=round(r2,2),slope_per_doubling=round(b*math.log(2),1),pctile=round(pct))
    print(f"{p:25s} act {act:6.2f} exp {pred:6.1f} gap {act-pred:+6.1f} z {(act-pred)/sd:+.2f} R2 {r2:.2f} pct {pct:.0f}")
# composite: official rank vs income
y=[d['rank'] for d in withg]; a,b,sd,r2=ols(x,y); pr=a+b*math.log(ind['gdp'])
print('rank exp',round(pr),'actual',ind['rank'],'R2',round(r2,2))
out['rank']=dict(actual=ind['rank'],expected=round(pr),r2=round(r2,2))
# peers: countries within +-25% of India GDP pc
peers=[d for d in withg if 0.75*ind['gdp']<=d['gdp']<=1.25*ind['gdp']]
peers.sort(key=lambda d:d['rank'])
print('income peers',len(peers),[ (d['name'],d['rank']) for d in peers][:12])
out['peers']=[(d['name'],d['rank'],round(d['gdp'])) for d in peers]
out['india_gdp']=ind['gdp']; out['india_rd']=ind['rd']
# R&D vs Development & Diffusion
wr=[d for d in data if d['rd'] and d['gdp']]
xr=[math.log(d['gdp']) for d in wr]; yr=[d['rd'] for d in wr]
a,b,sd,r2=ols(xr,yr); pr=a+b*math.log(ind['gdp'])
print('R&D actual',ind['rd'],'expected',round(pr,2),'R2',round(r2,2),'n',len(wr))
out['rd']=dict(actual=round(ind['rd'],2),expected=round(pr,2),n=len(wr),r2=round(r2,2))
# corr R&D and D&D
import statistics
c=statistics.correlation([d['rd'] for d in wr],[d['pillars'][4] for d in wr]); print('corr RD vs D&D',round(c,2)); out['corr_rd_dd']=round(c,2)
json.dump({'out':out,'scatter':[(d['name'],round(math.log10(d['gdp']),3),d['pillars'][1],d['pillars'][4],d['rank']) for d in withg]},open('analysis_out.json','w'),indent=1)
