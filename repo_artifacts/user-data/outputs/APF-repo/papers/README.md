# Papers

## Paper 1 — The Enforceability of Distinction
**Status:** Under review (arXiv + SciPost)

`paper1/main.tex` — Main paper. Three-part structure:
- Part I (§1–7): Core derivation — A1 through Hilbert space
- Part II (§8–12): Worked examples and verifications
- Part III (§13–14): Discussion and scope

`paper1/supplement.tex` — Formal supplement (71 pages). Contains all proofs
with machine-checkable cross-references to `apf/core.py`. Organized into three
corresponding parts. Every boxed result in the supplement has a `check_` function
in the codebase.

## Paper 2 — The Structure of Admissible Physics
**Status:** Draft

`paper2/main.tex` — Derives Standard Model gauge content, fermion representations,
and cosmological density fractions from the Paper 1 foundation.

`paper2/supplement.tex` — Formal supplement. Companion to `apf/gauge.py`,
`apf/cosmology.py`, `apf/generations__8_.py`.

## Paper 13 — TLS Concordance Paper
**Status:** Draft

`paper13/main.tex` — Systematic comparison of all 47 APF predictions against
experiment. Organized by sector (gauge, bosons, fermion masses, mixing, cosmology).
The "scorecard" paper.

## Compilation

Each paper compiles as a standalone LaTeX document:

```bash
cd paper1  # (or paper2, paper13)
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
```

Three passes are required for cross-references and page numbers to converge.
Check for errors with: `grep -E "^!" main.log`
Check for undefined references: `grep "undefined" main.log | grep -v rerunfilecheck`

## Formatting Standards

All papers use the APF house style:
- `apfbox` environment (black!3 background, detached titles, `fancyhdr`)
- All lemmas include abbreviation + full name (e.g., $L_{\mathrm{loc}}$ (Locality))
- Plain-English introduction before every formal box
- Informative colon-style headings
- No version numbers in document text
