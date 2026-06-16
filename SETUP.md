# Setup and Verification

## Requirements

- Python 3.8 or later
- **numpy** — linear algebra and array operations, used across most of the bank
- **scipy** — special functions, two-loop RG integrals, and spectral-action moments; required by a small number of numerical checks
- The Python standard library (`fractions`, `math`, `itertools`, `functools`) carries the exact-rational core

`pip install -e .` reads the dependencies from `setup.py`. The engine is not stdlib-only — the numerical checks need numpy and scipy.

## Installation

```bash
git clone https://github.com/Ethan-Brooke/APF-Engine.git
cd APF-Engine
pip install -e .
python -c "import apf; print('APF package loaded successfully')"
```

The `apf/` directory is a standard Python package. After `pip install -e .` it imports from anywhere as `import apf` or `from apf.core import ...`. If you prefer not to install, put the repo root on `PYTHONPATH` and run from there:

```bash
export PYTHONPATH=/path/to/APF-Engine:$PYTHONPATH
python verify_all.py
```

## Where the codebase lives

The live working tree is a git repository at `Dev/apf-codebase` on the principal machine, remote `Ethan-Brooke/APF-Engine`, branch `main`. The Google Drive copy under `__APF Library/Codebase/` is a frozen archival mirror — read-only.

**Run every `git` operation (add, commit, push) in a native shell on the principal machine, never through a sandbox mount.** The sandbox bridge corrupts `.git/index`, and the remote is unreachable from inside a sandbox. A session may edit files and stage a commit message; the actual push runs natively. The commit is the archive.

## Running the full suite

```bash
python verify_all.py
```

This runs the full bank and prints the scorecard. As of v24.3.249 the bank carries **3,745 registered theorems across 422 typed modules**, and the prediction scorecard reads:

```
Prediction scorecard
--------------------
Quantitative predictions:   48
Tested:                     39
Within 3σ:                  32 / 39
Mean absolute error:        3.83%
Median error:               0.37%
```

The whole suite runs in well under a minute on a modern laptop. `apf/_module_manifest.py` is the canonical module index and the source of the expected registry size; treat the live `verify_all.py` count as ground truth over any number written into prose.

## Running individual modules

```python
# A single core check
from apf.core import check_T2
r = check_T2()
print(r['name'], '—', r['status'])

# The gauge-group derivation
from apf.gauge import check_L_gauge_template_uniqueness
print(check_L_gauge_template_uniqueness()['summary'])
```

Each `check_` function returns a dict with at least a name, a status, its dependencies, and a one-line summary. Core checks use `fractions.Fraction` for exact rational arithmetic.

## Troubleshooting

**`No module named 'apf'`** — run `pip install -e .` from the repo root, or add the root to `PYTHONPATH`.

**A check fails on a clean clone** — the error names the failing check and assertion. This should not happen on a clean clone of `main`; if it does, the bank count and the narrative have likely drifted, or a module failed to register at import. Compare the printed count against the `EXPECTED` figure in the `Codebase:` header of `__APF Library/CLAUDE.md` and surface the mismatch before doing further work.

**Slow runtime** — the full suite still finishes in under a minute; the largest mass-sector module (Gram-matrix computations) takes the longest.

<!-- FOOTER:start -->
---

## About the APF series

The Admissibility Physics Framework is a constraint-first derivation of the Standard Model and cosmological structure from a single primitive — finite enforcement capacity. The corpus runs from the foundational papers through the gauge sector, the quantum formalism, Lorentzian spacetime and the Einstein field equations, the cosmological constant, the electroweak and dark sectors, and the lattice Yang–Mills program. Each paper's main text and Technical Supplement is deposited separately on Zenodo and collected in the **[admissibility_physics](https://zenodo.org/communities/admissibility_physics)** community. The engine in this repository is the machine-verifiable companion to all of it (v24.3.249 — 3,745 bank-registered theorems across 422 typed modules, 48 quantitative predictions).

| # | Title | Concept DOI |
|---|---|---|
| Engine | Admissibility Physics — Unified Theorem Bank & Verification Engine | [10.5281/zenodo.18529115](https://doi.org/10.5281/zenodo.18529115) |
| 0 | What Physics Permits: A Constraint-First Framework for Physics | [10.5281/zenodo.18439523](https://doi.org/10.5281/zenodo.18439523) |
| 1 | The Enforceability of Distinction | [10.5281/zenodo.18439200](https://doi.org/10.5281/zenodo.18439200) |
| 2 | Finite Admissibility and the Failure of Global Description | [10.5281/zenodo.18439274](https://doi.org/10.5281/zenodo.18439274) |
| 3 | Entropy, Time, and Accumulated Cost | [10.5281/zenodo.18439363](https://doi.org/10.5281/zenodo.18439363) |
| 4 | Admissibility Constraints and Structural Saturation | [10.5281/zenodo.18439397](https://doi.org/10.5281/zenodo.18439397) |
| 5 | Quantum Structure from Finite Enforceability | [10.5281/zenodo.18439433](https://doi.org/10.5281/zenodo.18439433) |
| 6 | Dynamics and Geometry as Optimal Admissible Reallocation | [10.5281/zenodo.18439445](https://doi.org/10.5281/zenodo.18439445) |
| 7 | A Minimal Quantum of Action from Finite Admissibility | [10.5281/zenodo.18439513](https://doi.org/10.5281/zenodo.18439513) |
| 8 | The Admissibility-Capacity Ledger | [10.5281/zenodo.19721384](https://doi.org/10.5281/zenodo.19721384) |
| 9 | The Geometric Substrate as Cost Structure of Comparison Continuations | [10.5281/zenodo.20041675](https://doi.org/10.5281/zenodo.20041675) |
| 10 | The Calculus of Finite Continuability | [10.5281/zenodo.20041680](https://doi.org/10.5281/zenodo.20041680) |
| 11 | Forced Universality from Capacity-Bounded Admissibility | [10.5281/zenodo.20684198](https://doi.org/10.5281/zenodo.20684198) |
| 13 | The Minimal Admissibility Core | [10.5281/zenodo.18361446](https://doi.org/10.5281/zenodo.18361446) |
| 16 | Markov Breakdown and the Hard Problems | [10.5281/zenodo.20684207](https://doi.org/10.5281/zenodo.20684207) |
| 18 | The Electroweak Sector as a Capacity Equilibrium | [10.5281/zenodo.20684209](https://doi.org/10.5281/zenodo.20684209) |
| 20 | The Enforcement Crystal | [10.5281/zenodo.18531732](https://doi.org/10.5281/zenodo.18531732) |
| 21 | APF Engine — Unified Theorem Bank and Verification Engine | [10.5281/zenodo.18529115](https://doi.org/10.5281/zenodo.18529115) |
| 24 | The Recruitment-Radius Extension — Foundations | [10.5281/zenodo.20684211](https://doi.org/10.5281/zenodo.20684211) |
| 28 | Absolute Mass Scales from Electroweak Capacity Saturation | [10.5281/zenodo.20684215](https://doi.org/10.5281/zenodo.20684215) |
| 29 | Plaquette Representation Dominance and Confinement | [10.5281/zenodo.20684218](https://doi.org/10.5281/zenodo.20684218) |
| 30 | A Tube Mechanism for the Lattice Mass Gap | [10.5281/zenodo.20684220](https://doi.org/10.5281/zenodo.20684220) |
| 31 | Osterwalder–Schrader Structure of Lattice Yang–Mills | [10.5281/zenodo.20684222](https://doi.org/10.5281/zenodo.20684222) |
| 33 | Trace-to-Scheme Export Architecture | [10.5281/zenodo.20684224](https://doi.org/10.5281/zenodo.20684224) |
| 35 | The Dark Sector as a Two-Role Capacity Decomposition | [10.5281/zenodo.20684228](https://doi.org/10.5281/zenodo.20684228) |
| 40 | Between Symmetry and the Void — The Thermodynamics of Finite Distinction | [10.5281/zenodo.20684235](https://doi.org/10.5281/zenodo.20684235) |
| 41 | The Horizon as a Continuation Ledger | [10.5281/zenodo.20684241](https://doi.org/10.5281/zenodo.20684241) |
| 42 | The Weak Mixing Angle Is Not Free | [10.5281/zenodo.20684245](https://doi.org/10.5281/zenodo.20684245) |

Concept DOIs always resolve to the latest version. Technical Supplements are deposited as linked records — `isSupplementTo` the main paper, `isDocumentedBy` the companion repository.

## Author

Ethan Brooke — Independent Researcher, San Anselmo, California, USA.

- ORCID: [0009-0001-2261-4682](https://orcid.org/0009-0001-2261-4682)
- LinkedIn: [linkedin.com/in/ethanbrooke](https://www.linkedin.com/in/ethanbrooke/)
- GitHub: [github.com/Ethan-Brooke](https://github.com/Ethan-Brooke)
- Contact: brooke.ethan@gmail.com

License: CC-BY-4.0.
<!-- FOOTER:end -->
