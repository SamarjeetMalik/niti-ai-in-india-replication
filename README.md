# Replication files: *Artificial Intelligence in India*

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24165211.svg)](https://doi.org/10.5281/zenodo.24165211)

Data and code that reproduce every computed number in the report **"Artificial Intelligence in India: Readiness, Gaps and Policy Priorities for Viksit Bharat"** by Samarjeet Malik and Kanishk Hooda (research conducted at the Economics and Finance Vertical, NITI Aayog, January–March 2025; revised by the authors, November 2026). The figures cover Section 3 (income-adjusted readiness and robustness), Section 8 (costs) and Appendix A (methods) of the report.

The views in the report are the authors' own and do not necessarily reflect those of NITI Aayog or the Government of India.

## Requirements

Python 3.10 or later, and numpy:

```bash
pip install -r requirements.txt
```

`analysis.py` and `costing.py` need only the standard library. Tested with Python 3.12 and numpy 2.2.6.

## Run

From this folder, in this order:

| Script | Reproduces | Output |
|---|---|---|
| `analysis.py` | Sections 3.2–3.3: income benchmark, India's gaps, income peers, R&D correlation | `analysis_out.json` |
| `robust.py` | Section 3.4: specifications A–E | `robust_out.json` |
| `robust_ci.py` | Figure 5: bootstrap intervals (2,000 resamples) | `robust_ci_points.json` |
| `appendix.py` | Appendix A, Tables A1–A2: standard errors, Cook's distance, leave-one-out, functional forms, R&D regressions | `appendix_out.json`, `country_data.csv` |
| `appendix_boot.py` | Appendix A, Table A2: bootstrap intervals for the flexible form | `appendix_boot_out.json` |
| `appendix_rd_window.py` | Appendix A.6: R&D results by observation year | `appendix_rd_window_out.json` |
| `costing.py` | Section 8: costs of R3, R4 and R6 and the R4 sensitivity grid | printed |
| `extra_analysis.py` | supporting calculations for Section 4 (spending shares, GERD growth) | printed |

Random seeds are fixed, so each JSON output is identical to its counterpart in `expected/`. To check:

```bash
for f in expected/*.json; do cmp "$f" "$(basename "$f")" && echo "OK $f"; done
```

## Data

- `gari2025.json`: overall rank and six pillar scores from the Oxford Insights *Government AI Readiness Index 2025* (validated January 2026 edition, "Full Rankings and Pillar Scores" table). Columns: name, rank, Policy Capacity, AI Infrastructure, Governance, Public Sector Adoption, Development & Diffusion, Resilience. It holds 193 of the 195 governments: North Korea (167th) and Micronesia (172nd) were lost in parsing. North Korea has no World Bank income data, and adding Micronesia changes none of India's gaps by more than 0.6 points (Appendix A.1).
- `wb.json`: World Bank World Development Indicators, retrieved November 2026, latest year per country, stored as `[name, year, value]`. `gdp` = NY.GDP.PCAP.PP.KD (GDP per capita, PPP, constant 2021 international $), `gdpusd` = NY.GDP.PCAP.CD, `pop` = SP.POP.TOTL, `rd` = GB.XPD.RSDV.GD.ZS (R&D, % of GDP), `inc` = income group.
- `country_data.csv`: the merged country-level dataset, one row per government (written by `appendix.py`).
- `sources/`: text extracts of the Union Budget 2026–27 Notes on Demands for Grants (MeitY, Demand 27; DST, Demand 89) used in Table 2.
- `FIGURE_DATA.md`: the source of the data behind each figure in the report.

## Licences

- **Code** (`*.py`): MIT License, see `LICENSE`.
- **Data** (`gari2025.json`, `wb.json`, `country_data.csv`, `expected/`): CC BY-SA 4.0, see `LICENSE-DATA.md`. The Oxford Insights index is published under CC BY-SA 4.0, so derived data carry the same licence. World Bank data are CC BY 4.0.
- `sources/` contains extracts of public Government of India budget documents, reproduced for reference.

## Citation

Malik, S. and Hooda, K. (2026). *Replication files for "Artificial Intelligence in India: Readiness, Gaps and Policy Priorities for Viksit Bharat"* (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.24165211

See also `CITATION.cff`.
