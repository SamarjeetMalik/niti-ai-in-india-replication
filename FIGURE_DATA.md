# Data behind the charts and tables

Every chart is drawn directly in `main.tex` (pgfplots), with the data written inline. This file lists where each number comes from.

| Figure | Data | Source |
|---|---|---|
| Fig 1 (readiness vs income) | `figures/readiness_income.dat` | Oxford Insights GAIRI 2025; World Bank NY.GDP.PCAP.PP.KD |
| Fig 2, Tables 2–3 | regressions in `analysis.py`, `robust.py` | as above |
| Fig 3 (R&D vs D&D) | `figures/rd_dd.dat`; India 2023–24 = 0.84% | World Bank GB.XPD.RSDV.GD.ZS; PIB PRID 2291139 (DST) |
| Fig 4 (GPUs) | 10,000 target (Mar 2024); 18,693 (Jan 2025); 34,333 (May 2025); 38,000 (Oct 2025); 45,000+ (Jun 2026); 100,000 target | PIB PRIDs 2012375, 2097709, 2132817, 2177598; PIB factsheet 150860; PIB explainer 15 Feb 2026 |
| Fig 5 (compute subsidy) | 1,275 total; 1,058 foundation models; 38.97 government; 13.24 IndiaAI; 10.14 researchers; 154.65 residual | ThePrint, 20 Oct 2026, analysis of IndiaAI Compute Portal (8 Oct 2026) |
| Fig 6a, Table 4 (budget) | IndiaAI BE/RE/Actual; RDI; NRF | Union Budget Notes on Demands: MeitY D27 (2025-26, 2026-27), DST D89 (2026-27). Extracts in `sources/` |
| Fig 6b (pillars) | 4,563.36 / 1,971.37 / 1,942.50 / 882.94 / 689.05 / 199.55 / 102.69 / 20.46 | Rajya Sabha Unstarred Q 2935, 20 Dec 2024 |
| Fig 7a (private investment) | 2025, US$ bn | Stanford AI Index 2026, Fig 4.2.x (Quid) |
| Fig 7b (pledges) | IndiaAI outlay converted at Rs 84/US$; MS 17.5; Google 15; Summit >250 | Microsoft release 9 Dec 2025; Adani release 28 Apr 2026; PIB PRID 2238195 |
| Fig 8 (talent) | skill penetration (Fig 7.4.1); AI authors/inventors (Fig 1.8.1) | Stanford AI Index 2026 |
| Fig 9 (R&D trend) | GERD % GDP and private share, 2019-20 to 2023-24 | PIB PRID 2291139 (DST R&D Statistics 2025-26) |
| Section 4.2 / 8 calculations | absorption, GERD CAGR | `extra_analysis.py`, `costing.py` |

## Figures added 12 Nov 2026
| Figure | Data | Source |
|---|---|---|
| Framework diagram (Fig 1) | The report's own diagnosis → recommendations → indicators | Sections 3–9 |
| Robustness dot plot | Gaps in points with 95% bootstrap intervals (2,000 resamples), specs A–E | `robust_ci.py` → `robust_ci_points.json` |
| Governance timeline | Guidelines Nov 2025; DPDP Rules Nov 2025; IT Rules Feb 2026; Summit 18–19 Feb 2026; AIGEG/TPEC 13 Apr 2026; Board ad 6 Jun 2026; AISI reply 27 Jul 2026; LS Q3960 12 Aug 2026; consent-manager phase Nov 2026; full effect May 2027 | PIB releases; Lok Sabha Q3960; MeitY |
| Recommendation roadmap | Targets in Section 7 | Authors' proposals |
