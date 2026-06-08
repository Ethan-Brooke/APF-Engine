# APF v34 — Trace-Sector Evidence Section

This package consolidates the electroweak-sector closure and fermion-sector master closure into one publication-facing evidence section.

Main claim:

> APF closes the electroweak trace sector and the fermion trace sector locally; physical export is admitted only route by route.

Key admitted export-candidate branches:

- `M_W^{APF -> OS}`: reviewed same-input DIZET on-shell transport, row/covariance route, about `1.09 sigma` residual.
- `m_b^{APF -> MSbar}(m_b)`: bottom self-scale MSbar export candidate, about `-0.787 sigma` residual.

Key obstruction branches:

- top: terminal scheme closeout; external MSR codomain pass only.
- charged leptons: six-channel normalization candidate plus generation residual obstruction.
- charm: self-scale MSbar route knockout.
- light quarks: low-energy QCD/chiral/lattice obstruction.

Files:

- `paper/TRACE_SECTOR_EVIDENCE_SECTION_v34.tex` — publication-facing consolidated section.
- `tables/trace_sector_master_evidence_table_v34.csv` — master evidence table.
- `tables/trace_sector_claim_ladder_v34.csv` — safe/forbidden claim ladder.
- `tables/trace_sector_no_smuggling_audit_v34.csv` — consolidated audit table.
- `reports/trace_sector_evidence_summary_v34.md` — short summary.
- `reports/trace_sector_evidence_v34_data.json` — machine-readable data.
- `scripts/check_trace_sector_evidence_v34.py` — verifier used for the pass report.
