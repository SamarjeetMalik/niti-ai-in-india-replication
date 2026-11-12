"""Additional calculations for the report (Sections 4.1-4.6, 8). All inputs are cited in the report."""
# 1. IndiaAI absorption (Rs crore). Union Budget: FY25 actual 19.24; FY26 RE 800; FY27 BE 1000. Outlay 10,371.92 (Mar 2024, 5 years: FY25-FY29).
outlay=10371.92; spent_fy25=19.24; fy26_re=800.0; fy27_be=1000.0
cum=spent_fy25+fy26_re+fy27_be
remaining=outlay-cum
print(f"Absorption: cumulative through FY27 (if RE/BE fully spent) {cum:,.2f}; share of outlay {cum/outlay:.1%}")
print(f"  remaining {remaining:,.2f} over FY28-FY29 -> {remaining/2:,.0f} per year = {remaining/2/fy27_be:.1f}x FY27 BE, {remaining/2/spent_fy25:,.0f}x FY25 actual")
print(f"  FY25 actual/BE {19.24/551.75:.1%}; actual/RE {19.24/173:.1%}; FY26 RE cut {(2000-800)/2000:.0%}; RDI cut {(20000-3000)/20000:.0%}")
# 2. GERD growth (PIB/DST): Rs crore
g={'2019-20':132567.01,'2020-21':127380.96,'2021-22':194810.83,'2022-23':213378.12,'2023-24':244767.81}
c4=(g['2023-24']/g['2019-20'])**(1/4)-1; c2=(g['2023-24']/g['2021-22'])**(1/2)-1
gdp26=357.14e5; gdp30=gdp26*1.09**4; target=0.01*gdp30
req=(target/g['2023-24'])**(1/6)-1
print(f"GERD CAGR FY20-FY24 {c4:.1%}; FY22-FY24 {c2:.1%}; required FY24->FY30 for 1% {req:.1%}; FY30 target {target/1e5:.2f} lakh cr")
for gr in (c2,):
    v=g['2023-24']*(1+gr)**6; print(f"  at {gr:.1%}/yr GERD FY30 = {v/1e5:.2f} lakh cr = {v/gdp30:.2%} of GDP")
# 3. Private investment (AI Index 2026, US$bn, 2025)
inv={'United States':285.88,'China':12.41,'United Kingdom':5.90,'France':4.36,'Canada':4.28,'India':4.09,'Germany':3.89,'Israel':3.58}
print(f"India/US {inv['India']/inv['United States']:.2%}; India growth 2024->2025 {4.09/1.16:.2f}x; per newly funded co 2025 US${4.09e3/108:.1f}m")
# 4. Compute subsidy split (ThePrint analysis of IndiaAI portal, Oct 2026), Rs crore
tot=1275; fm=1058; res=10.14; gov=38.97; self_=13.24
other=tot-fm-res-gov-self_
for k,v in [('foundation-model builders',fm),('government bodies',gov),('IndiaAI itself',self_),('researchers/students/fellows',res),('all other approvals',other)]:
    print(f"  {k}: {v:,.2f} ({v/tot:.1%})")
# 5. Public budget vs pledges (US$bn); IndiaAI outlay at ~Rs 84/US$
print(f"IndiaAI outlay ~US${outlay/84/100:.2f}bn (Rs 84/$)")
