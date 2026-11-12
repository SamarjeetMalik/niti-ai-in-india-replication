"""R&D sensitivity to the observation year (Appendix A.6). Needs numpy."""
import json, math
from collections import Counter
import numpy as np
exec(open('appendix.py').read().split("out = {'n': n")[0])
yr = {k: int(v[1]) for k, v in wb['rd'].items()}
wr = [d for d in base if d['rd']]
print('R&D year distribution', sorted(Counter(yr[d['iso']] for d in wr).items()))
rng = np.random.default_rng(11)
def fit(rows, india_rd=None, boot=True):
    y = np.array([d['pillars'][4] for d in rows], float)
    rd = np.array([d['rd'] for d in rows]); lg = np.array([math.log(d['gdp']) for d in rows])
    X = np.column_stack([np.ones(len(rows)), rd, lg])
    b = np.linalg.lstsq(X, y, rcond=None)[0]
    e = y - X @ b; XtXi = np.linalg.inv(X.T @ X); se = math.sqrt(XtXi[1, 1] * (e @ e) / (len(y) - 3))
    # partial correlation of D&D and R&D given log income
    ry = y - np.column_stack([np.ones(len(y)), lg]) @ np.linalg.lstsq(np.column_stack([np.ones(len(y)), lg]), y, rcond=None)[0]
    rr = rd - np.column_stack([np.ones(len(y)), lg]) @ np.linalg.lstsq(np.column_stack([np.ones(len(y)), lg]), rd, rcond=None)[0]
    pc = float(np.corrcoef(ry, rr)[0, 1])
    ci = None
    if boot:
        bs = []
        for _ in range(2000):
            idx = rng.integers(0, len(y), len(y)); bs.append(np.linalg.lstsq(X[idx], y[idx], rcond=None)[0][1])
        ci = (round(float(np.percentile(bs, 2.5)), 1), round(float(np.percentile(bs, 97.5)), 1))
    out = dict(n=len(rows), delta=round(float(b[1]), 2), se=round(se, 2), ci=ci, partial_r=round(pc, 2))
    ind = [d for d in rows if d['iso'] == 'IND']
    if ind:
        d = ind[0]; xi = np.array([1, india_rd or d['rd'], math.log(d['gdp'])])
        out['india_pred'] = round(float(xi @ b), 1); out['india_gap'] = round(float(d['pillars'][4] - xi @ b), 1)
    return out
res = {}
res['all'] = fit(wr)
res['2020_2024'] = fit([d for d in wr if 2020 <= yr[d['iso']] <= 2024])
res['2022_2024'] = fit([d for d in wr if 2022 <= yr[d['iso']] <= 2024] + [d for d in wr if d['iso'] == 'IND'], india_rd=0.84)
# year-of-observation fixed effects (all countries)
y = np.array([d['pillars'][4] for d in wr], float)
years = sorted(set(yr[d['iso']] for d in wr)); yrs = [yr[d['iso']] for d in wr]
grp = lambda t: 'old' if t < 2020 else str(t)
gs = sorted(set(grp(t) for t in yrs))
X = np.column_stack([np.ones(len(wr)), [d['rd'] for d in wr], [math.log(d['gdp']) for d in wr]] + [[1.0 if grp(t) == g else 0.0 for t in yrs] for g in gs[1:]])
b = np.linalg.lstsq(X, y, rcond=None)[0]; e = y - X @ b
se = math.sqrt(np.linalg.inv(X.T @ X)[1, 1] * (e @ e) / (len(y) - X.shape[1]))
res['year_fe'] = dict(n=len(wr), delta=round(float(b[1]), 2), se=round(se, 2), groups=gs)
print(json.dumps(res, indent=1)); json.dump(res, open('appendix_rd_window_out.json', 'w'), indent=1)
