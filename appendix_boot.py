"""Bootstrap intervals for India's gaps under the quadratic form of specification B."""
import json, math
import numpy as np
exec(open('appendix.py').read().split("out = {'n': n")[0])
rows = [d for d in base if d['pop']]
i0 = [k for k, d in enumerate(rows) if d['iso'] == 'IND'][0]
lg = np.array([math.log(d['gdp']) for d in rows]); lp = np.array([math.log(d['pop']) for d in rows])
X = np.column_stack([np.ones(len(rows)), lg, lg ** 2, lp, lp ** 2])
rng = np.random.default_rng(7); res = {}
for j, p in enumerate(P):
    y = np.array([d['pillars'][j] for d in rows], float)
    g = y[i0] - X[i0] @ np.linalg.lstsq(X, y, rcond=None)[0]; gs = []
    for _ in range(2000):
        idx = np.append(rng.integers(0, len(rows), len(rows)), i0)
        gs.append(y[i0] - X[i0] @ np.linalg.lstsq(X[idx], y[idx], rcond=None)[0])
    res[p] = (round(float(g), 1), round(float(np.percentile(gs, 2.5)), 1), round(float(np.percentile(gs, 97.5)), 1))
print(res); json.dump(res, open('appendix_boot_out.json', 'w'), indent=1)
