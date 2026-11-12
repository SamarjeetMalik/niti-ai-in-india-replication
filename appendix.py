"""Diagnostics for the methodological appendix (Appendix A).

Run from this folder:  python appendix.py
Needs numpy. Reads gari2025.json and wb.json from this folder, writes
appendix_out.json and country_data.csv.
"""
import json, math, csv
import numpy as np

src = open('analysis.py').read().split("withg=[d for d in data if d['gdp']]")[0]
exec(src)  # builds `data`, `wb`, `P`
for d in data:
    iso = d['iso']
    d['pop'] = wb['pop'].get(iso, [None, None, None])[2] if iso else None
    d['inc'] = wb['inc'].get(iso) if iso else None

base = [d for d in data if d['gdp']]
IND = [k for k, d in enumerate(base) if d['iso'] == 'IND'][0]
lg = np.array([math.log(d['gdp']) for d in base])
n = len(base)


def ols(X, y):
    XtX_inv = np.linalg.inv(X.T @ X)
    b = XtX_inv @ X.T @ y
    e = y - X @ b
    k = X.shape[1]
    s2 = e @ e / (len(y) - k)
    se = np.sqrt(np.diag(XtX_inv) * s2)
    # HC1 robust standard errors
    meat = (X * e[:, None]).T @ (X * e[:, None])
    hc1 = np.sqrt(np.diag(XtX_inv @ meat @ XtX_inv) * len(y) / (len(y) - k))
    r2 = 1 - (e @ e) / np.sum((y - y.mean()) ** 2)
    h = np.einsum('ij,jk,ik->i', X, XtX_inv, X)  # leverage
    cook = e ** 2 / (k * s2) * h / (1 - h) ** 2
    return b, se, hc1, r2, e, h, cook


out = {'n': n, 'pillars': {}}
X1 = np.column_stack([np.ones(n), lg])
X2 = np.column_stack([np.ones(n), lg, lg ** 2])
Xlin = np.column_stack([np.ones(n), np.array([d['gdp'] for d in base]) / 1000])
for j, p in enumerate(P):
    y = np.array([d['pillars'][j] for d in base], float)
    b, se, hc1, r2, e, h, cook = ols(X1, y)
    gap = e[IND]
    infl = int((cook > 4 / n).sum())
    # India's gap with the influential observations removed
    keep = (cook <= 4 / n) | (np.arange(n) == IND)
    bk, *_ = ols(X1[keep], y[keep])
    gap_noinfl = y[IND] - X1[IND] @ bk
    # leave-one-out: drop each other country in turn
    loo = []
    for i in range(n):
        if i == IND:
            continue
        m = np.arange(n) != i
        bi = np.linalg.lstsq(X1[m], y[m], rcond=None)[0]
        loo.append(y[IND] - X1[IND] @ bi)
    # alternative functional forms
    b2, se2, *_r = ols(X2, y)
    r2q = _r[1]
    gap_q = y[IND] - X2[IND] @ b2
    bl, sel, _, r2l, *_ = ols(Xlin, y)
    gap_l = y[IND] - Xlin[IND] @ bl
    # rank-based: India's percentile of residuals from a lowess-free
    # nonparametric benchmark: mean score of the 20 nearest countries by income
    order = np.argsort(np.abs(lg - lg[IND]))
    nn = [i for i in order if i != IND][:20]
    gap_nn = y[IND] - y[nn].mean()
    out['pillars'][p] = dict(
        a=round(float(b[0]), 2), b=round(float(b[1]), 2), se=round(float(se[1]), 2),
        hc1=round(float(hc1[1]), 2), r2=round(float(r2), 2),
        gap=round(float(gap), 1),
        india_leverage=round(float(h[IND]), 3), india_cook=round(float(cook[IND]), 3),
        n_influential=infl, gap_excl_influential=round(float(gap_noinfl), 1),
        loo_min=round(float(min(loo)), 1), loo_max=round(float(max(loo)), 1),
        gap_quadratic=round(float(gap_q), 1), r2_quadratic=round(float(r2q), 2),
        quad_term_t=round(float(b2[2] / se2[2]), 2),
        gap_linear_level=round(float(gap_l), 1), r2_linear_level=round(float(r2l), 2),
        gap_20_nearest=round(float(gap_nn), 1),
    )

# R&D regression: D&D on R&D intensity, with and without log GDP per capita
wr = [d for d in base if d['rd']]
ir = [k for k, d in enumerate(wr) if d['iso'] == 'IND'][0]
yr = np.array([d['pillars'][4] for d in wr], float)
rd = np.array([d['rd'] for d in wr])
lgr = np.array([math.log(d['gdp']) for d in wr])
Xa = np.column_stack([np.ones(len(wr)), rd])
Xb = np.column_stack([np.ones(len(wr)), rd, lgr])
ba, sea, hca, r2a, ea, ha, ca = ols(Xa, yr)
bb, seb, hcb, r2b, eb, hb, cb = ols(Xb, yr)
keep = cb <= 4 / len(wr)
bbk, sebk, *_ = ols(Xb[keep], yr[keep])
loo = []
for i in range(len(wr)):
    m = np.arange(len(wr)) != i
    loo.append(np.linalg.lstsq(Xb[m], yr[m], rcond=None)[0][1])
out['rd'] = dict(
    n=len(wr),
    simple=dict(a=round(float(ba[0]), 2), b=round(float(ba[1]), 2), se=round(float(sea[1]), 2), hc1=round(float(hca[1]), 2), r2=round(float(r2a), 2)),
    with_income=dict(a=round(float(bb[0]), 2), b_rd=round(float(bb[1]), 2), se_rd=round(float(seb[1]), 2), hc1_rd=round(float(hcb[1]), 2),
                     b_lgdp=round(float(bb[2]), 2), se_lgdp=round(float(seb[2]), 2), r2=round(float(r2b), 2)),
    n_influential=int((~keep).sum()), b_rd_excl_influential=round(float(bbk[1]), 2),
    loo_b_rd_min=round(float(min(loo)), 2), loo_b_rd_max=round(float(max(loo)), 2),
)
json.dump(out, open('appendix_out.json', 'w'), indent=1)
print(json.dumps(out, indent=1))

with open('country_data.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['country', 'iso3', 'overall_rank'] + P + ['gdp_pc_ppp_2021', 'rd_pct_gdp', 'population', 'wb_income_group'])
    for d in data:
        w.writerow([d['name'], d['iso'] or '', d['rank']] + list(d['pillars']) +
                   [round(d['gdp'], 1) if d['gdp'] else '', round(d['rd'], 3) if d['rd'] else '',
                    int(d['pop']) if d['pop'] else '', d['inc'] or ''])

# Specification B (log GDP per capita + log population): the Governance finding
bp = [k for k, d in enumerate(base) if d['pop']]
rowsB = [base[k] for k in bp]
iB = [k for k, d in enumerate(rowsB) if d['iso'] == 'IND'][0]
lgB = np.array([math.log(d['gdp']) for d in rowsB]); lpB = np.array([math.log(d['pop']) for d in rowsB])
XB = np.column_stack([np.ones(len(rowsB)), lgB, lpB])
XBq = np.column_stack([np.ones(len(rowsB)), lgB, lgB ** 2, lpB, lpB ** 2])
specB = {'n': len(rowsB)}
for j, p in enumerate(P):
    y = np.array([d['pillars'][j] for d in rowsB], float)
    b, se, hc1, r2, e, h, cook = ols(XB, y)
    keep = (cook <= 4 / len(y)) | (np.arange(len(y)) == iB)
    bk = np.linalg.lstsq(XB[keep], y[keep], rcond=None)[0]
    loo = [y[iB] - XB[iB] @ np.linalg.lstsq(XB[np.arange(len(y)) != i], y[np.arange(len(y)) != i], rcond=None)[0]
           for i in range(len(y)) if i != iB]
    bq = np.linalg.lstsq(XBq, y, rcond=None)[0]
    specB[p] = dict(b_lgdp=round(float(b[1]), 2), se_lgdp=round(float(se[1]), 2), b_lpop=round(float(b[2]), 2),
                    se_lpop=round(float(se[2]), 2), hc1_lpop=round(float(hc1[2]), 2), r2=round(float(r2), 2),
                    gap=round(float(e[iB]), 1), india_cook=round(float(cook[iB]), 3),
                    gap_excl_influential=round(float(y[iB] - XB[iB] @ bk), 1),
                    loo_min=round(float(min(loo)), 1), loo_max=round(float(max(loo)), 1),
                    gap_quadratic=round(float(y[iB] - XBq[iB] @ bq), 1))
out['specB'] = specB
json.dump(out, open('appendix_out.json', 'w'), indent=1)
print(json.dumps(specB, indent=1))
