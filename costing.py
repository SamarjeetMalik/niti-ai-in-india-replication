# All money in Rs crore unless noted. 1 crore = 1e7; 1 lakh = 1e5.
cr=1e7
# R3 compute subsidy
L1_avg, L1_high, sub = 115.85, 150.0, 0.40
s_lo, s_hi = L1_avg*sub, L1_high*sub
cap_hours = 100_000*8760
print(f"R3 subsidy/hr {s_lo:.1f}-{s_hi:.1f}; capacity hours {cap_hours/1e6:.0f}M")
r3={}
for u in (0.05,0.15,0.30):
    h=cap_hours*u; r3[u]=(h/1e6, h*s_lo/cr, h*s_hi/cr); print(f"  u={u:.0%} hours {h/1e6:.0f}M cost {h*s_lo/cr:,.0f}-{h*s_hi/cr:,.0f} cr/yr")
acad=10e6*L1_high/cr; print(f"  academic window 10M h at full Rs150: {acad:.0f} cr/yr")
# R4 R&D
gdp26=357.14e5  # Rs crore (357.14 lakh crore)
g=0.09
gdp30=gdp26*(1+g)**4
print(f"R4 GDP FY30 {gdp30/1e5:.1f} lakh cr")
base=0.0084; gov=0.482
for t in (0.010,0.012):
    add=(t-base)*gdp30; print(f"  target {t:.1%}: GERD {t*gdp30/1e5:.2f} lakh cr; extra vs 0.84% {add/1e3:,.0f}k cr; public share {add*gov/1e3:,.0f}k cr")
print(f"  GERD at 0.84% FY30 {base*gdp30/1e5:.2f} lakh cr")
print("  AI earmark 10% of RDI: 10,000 cr over 6 yrs =", round(10000/6), "cr/yr")
# check FY24 consistency: 244767.81 / 0.0084
print("  implied FY24 GDP", round(244767.81/0.0084/1e5,1), "lakh cr")
# R6 talent
ram=(1.35e5*12 + 7e5 + 0.6e5)/1e5  # lakh per year
print(f"R6 Ramanujan per fellow {ram:.1f} lakh/yr; 500 fellows {500*ram*1e5/cr:.0f} cr/yr; 5-yr {500*ram*5*1e5/cr:.0f} cr")
pm_total=((70+70+75+80+80)*1e3*12 + 10e5)/1e5  # lakh per fellow over 5 yrs
print(f"  PMRF per fellow 5yr {pm_total:.0f} lakh; 1000 fellows {1000*pm_total*1e5/cr:.0f} cr per cohort; per yr {1000*pm_total/5*1e5/cr:.0f}")

# R4 sensitivity: nominal GDP growth x public share of the extra R&D
print("R4 sensitivity (extra GERD in FY30 for 1% vs 0.84%; public part; required GERD growth FY24->FY30)")
gerd24 = 244767.81  # Rs crore, 2023-24 (DST)
for gg in (0.07, 0.09, 0.11):
    g30 = gdp26 * (1 + gg) ** 4
    add = (0.010 - base) * g30
    need = (0.010 * g30 / gerd24) ** (1 / 6) - 1
    pubs = {sh: add * sh for sh in (0.40, 0.482, 0.55)}
    print(f"  g={gg:.0%}: GDP30 {g30/1e5:.0f} lakh cr; extra {add/1e3:,.0f}k cr; public at 40/48.2/55%: "
          + ", ".join(f"{v/1e3:,.0f}k" for v in pubs.values()) + f"; required GERD growth {need:.1%}")
