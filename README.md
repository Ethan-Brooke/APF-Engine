# Admissibility Physics Framework (APF) -- v24.3.192

[![Verify](https://img.shields.io/badge/checks-3675%20PASS-success)](verify_all.py)
[![Bank](https://img.shields.io/badge/bank--registered-3675-blue)](apf/bank.py)
[![Free dimensionless parameters](https://img.shields.io/badge/free%20dimensionless%20params-0-brightgreen)](#prediction-scorecard)

A machine-verifiable theorem bank deriving the Standard Model gauge group,
fermion content, and cosmological capacity partition from finite enforcement
(PLEC) with **zero free dimensionless parameters** (one dimensional anchor: the Planck magnitude, equivalently the size of the universe).

This repository is the **canonical codebase** that backs the Admissibility
Physics Framework corpus (Papers 0-8 + 13 + 20). Every load-bearing claim in
the papers traces to a named check function in the `apf/` package. The full
verification suite runs in ~30 seconds on a laptop.

```bash
git clone https://github.com/Ethan-Brooke/APF-Engine-Repo.git
cd APF-Engine-Repo
pip install -e .
python verify_all.py
```

Expected output:

```
APF v7.1 -- Full Verification
=======================================================
... (per-module pass lines) ...

Total checks:     448
  Theorems  [T]:  144  pass    0  fail    0  flag
  Lemmas    [L]:  222  pass    0  fail    0  flag
  Red-team [RT]:   24  pass    0  fail    0  flag
  Other:           58  pass    0  fail    0  flag

(check) All 448 checks PASSED  (~30s)

Prediction scorecard
--------------------------------------------
48 quantitative predictions, zero free dimensionless parameters (one dimensional anchor).
39 tested. 32/39 within 3 sigma. Mean error 3.83%.
Median error 0.37%.
```

---

## What is this?

APF takes finite enforcement seriously as a physical quantity. The framework's
referent -- enforcement, the maintenance of distinctions at every interface --
is named in Paper 0. The **Principle of Least Enforcement Cost (PLEC)** with
its four constitutive features

| Feature | Statement |
|---------|-----------|
| **A1** (finiteness) | At every causally connected region, total enforcement cost is bounded above by a finite capacity. |
| **MD** (cost floor) | Each maintained distinction has a positive cost floor `mu* > 0`. |
| **A2** (argmin) | The realized configuration is the argmin of total enforcement cost over the admissible set. |
| **BW** (non-degeneracy) | The cost spectrum is non-degenerate. |

generates the Standard Model and cosmological structure with no free
parameters. The paper corpus (Paper 0 = ontology, Papers 1-8 = derivations,
Paper 13 = the minimal core, Paper 20 = the Enforcement Crystal) develops
the mathematics; this codebase certifies every step algorithmically.

---

## The APF corpus

| Paper | Title | Version | Zenodo DOI |
|------:|-------|---------|------------|
| Engine | Unified Theorem Bank & Verification Engine | v7.1 | [10.5281/zenodo.18529115](https://doi.org/10.5281/zenodo.18529115) |
| 0 | What Physics Permits: A Constraint-First Framework for Physics | v4.14 | [10.5281/zenodo.18439523](https://doi.org/10.5281/zenodo.18439523) |
| 1 | The Enforceability of Distinction | v4.8 | [10.5281/zenodo.18439200](https://doi.org/10.5281/zenodo.18439200) |
| 2 | Finite Admissibility and the Failure of Global Description | v5.8 | [10.5281/zenodo.18439274](https://doi.org/10.5281/zenodo.18439274) |
| 3 | Entropy, Time, and Accumulated Cost | v3.7 | [10.5281/zenodo.18439363](https://doi.org/10.5281/zenodo.18439363) |
| 4 | Admissibility Constraints and Structural Saturation | v2.3 | [10.5281/zenodo.18439397](https://doi.org/10.5281/zenodo.18439397) |
| 5 | Quantum Structure from Finite Enforceability | v2.4 | [10.5281/zenodo.18439433](https://doi.org/10.5281/zenodo.18439433) |
| 6 | Dynamics and Geometry as Optimal Admissible Reallocation | v2.5 | [10.5281/zenodo.18439445](https://doi.org/10.5281/zenodo.18439445) |
| 7 | A Minimal Quantum of Action from Finite Admissibility | v2.5 | [10.5281/zenodo.18439513](https://doi.org/10.5281/zenodo.18439513) |
| 8 | The Admissibility-Capacity Ledger | v2.11 | [10.5281/zenodo.19721384](https://doi.org/10.5281/zenodo.19721384) |
| 13 | The Minimal Admissibility Core | v8.12 | [10.5281/zenodo.18361446](https://doi.org/10.5281/zenodo.18361446) |
| 20 | The Enforcement Crystal | v3.3 | (deposit pending) |

A standalone derivation paper -- *The Weak Mixing Angle as a Capacity
Equilibrium* -- carries Zenodo DOI [10.5281/zenodo.18603208](https://doi.org/10.5281/zenodo.18603208).

---

## Repository layout

```
APF-Engine-Repo/
|-- README.md                     <- you are here
|-- LICENSE                       <- MIT
|-- CHANGELOG.md                  <- per-version delta log
|-- setup.py                      <- legacy install entry
|-- pyproject.toml                <- modern install entry
|-- verify_all.py                 <- runs all 448 checks
|-- run_checks.py                 <- thin convenience wrapper
|-- quick_demo.py                 <- 5-minute headline tour
|-- main.tex                      <- engine paper manuscript
|-- supplement.tex                <- engine paper supplement
|-- apf/                          <- the package (23 registered modules)
|   |-- __init__.py
|   |-- bank.py                   <- registry + EXPECTED_THEOREM_COUNT
|   |-- core.py                   <- A1, MD, BW, the keystone, T_alg, IJC
|   |-- gauge.py                  <- SU(3) x SU(2) x U(1) uniqueness
|   |-- generations.py            <- N_gen = 3
|   |-- gravity.py                <- horizon, Bekenstein, T_interface_sector_bridge
|   |-- cosmology.py              <- Omega_Lambda, Omega_b, dark budget
|   |-- plec.py                   <- Regime R + five-type exit taxonomy
|   |-- unification.py            <- T_ACC ledger, six regime projections
|   |-- crystal.py                <- Enforcement Crystal walker (Paper 20)
|   |-- crystal_metrics.py        <- Brandes betweenness, SCC path attribution
|   |-- formal_kernel.py          <- V_61 + G_SM executable witness
|   |-- paper1_kernel.py          <- FD1 4-element substrate witness
|   |-- numeric_fallback.py       <- pure-numpy expm/solve_ivp/quad
|   |-- test_no_smuggling.py      <- adversarial mutation tests (9/9)
|   |-- red_team.py               <- 19 self-audit checks
|   |-- standalone/               <- Cauchy uniqueness, Gram, etc.
|   |-- session_v63c.py           <- neutrino closure (research-grade)
|   |-- ... (additional modules)  <- see verify_all.py MODULES list
|-- ai_context/                   <- (engine repo only) AI-onboarding pack
|-- papers/                       <- (engine repo only) full corpus
|-- docs/                         <- (engine repo only) interactive DAG
|-- research_scripts/             <- (engine repo only) one-offs preserved
```

The clean codebase is the union of (`apf/` package + `verify_all.py` +
`setup.py` + `quick_demo.py` + `main.tex` + `supplement.tex`). Anything
under `research_scripts/` in the engine repo is preserved-but-not-load-bearing
session work.

---

## Verification

### Full run

```bash
python verify_all.py
```

Runs all 448 checks across 23 registered modules + standalone files. Exits
with status 0 only if every check returns PASS (no FAIL, no FLAG).

The runner distinguishes three statuses:

* **PASS** -- function returned without raising and (where it returns a dict)
  did not return `passed=False`.
* **FAIL** -- function raised an exception.
* **FLAG** -- function returned `{"passed": False, ...}`. This is the case
  for red-team checks that detect a discrepancy without raising. FLAG is
  treated as a non-zero exit so wrappers and CI can detect it.

### Filtered run

```bash
python verify_all.py --module core      # only apf.core
python verify_all.py --module gauge     # only apf.gauge
python verify_all.py --verbose          # full tracebacks on FAIL
python verify_all.py --no-scorecard     # skip prediction scorecard
```

Filtered runs auto-pre-run upstream DAG-producing modules so downstream
consumers see populated cache (e.g. `--module unification` pre-runs gauge
to populate `C_total`).

### Adversarial / red-team

```bash
python -m apf.red_team
python -m apf.red_team --detailed
```

19 self-audit checks (sensitivity, adversarial counter-models, regression
tests, expected theorem count, tolerance audit). Designed to fail loudly
if a future commit silently widens a tolerance, drops a module, or
introduces a circular dependency.

The tolerance audit ships with an explicit phenomenological-tolerance
whitelist (`PHENOMENOLOGICAL_TOLERANCE_WHITELIST` in `apf/red_team.py`).
Each whitelisted entry carries a documented reason; reviewers who disagree
can attack any single entry.

### Anti-smuggling test suite

```bash
python -m apf.test_no_smuggling
```

State-mutating adversarial tests that verify load-bearing results don't
depend on hardcoded constants alone. 9/9 pass.

### Quick demo

```bash
python quick_demo.py
```

5-minute tour: ten headline checks with derivation-chain context.

---

## Prediction scorecard

48 quantitative predictions, zero free dimensionless parameters (one dimensional anchor). 39 tested. 32/39 within
3-sigma. Mean error 3.83%. Median error 0.37%.

Selected:

| Quantity | APF | Observed | Error |
|----------|-----|----------|-------|
| sin^2 theta_W | 3/13 = 0.23077 | 0.23122 | 0.19% |
| Cabibbo angle | 13.07 deg | 13.16 deg | 0.6% |
| Omega_Lambda | 0.6888 | 0.6889 (Planck 2018) | 0.01% |
| Omega_b | 0.0492 | 0.0493 | 0.2% |
| Omega_c | 0.2620 | 0.2618 | 0.07% |
| Delta m^2_21 / Delta m^2_31 | 0.02952 | 0.02938 | 0.5% |
| H_0 (APF) | 67.76 km/s/Mpc | 67.4 +/- 0.5 (Planck 2018) | 0.5% |

Open-tension: H0DN 2026 (`73.50 +/- 0.81 km/s/Mpc`) sits 7.09-sigma from
the APF prediction. The framework states this as a falsifier in
Paper 6 §11.4 and identifies Route V (local inhomogeneity) as the only
APF-admissible accommodation, currently insufficient by ~2x.

Full catalog: `python -c "from apf.validation import check_L_prediction_catalog; print(check_L_prediction_catalog()[\'summary\'])"`.

---

## Install

```bash
git clone https://github.com/Ethan-Brooke/APF-Engine-Repo.git
cd APF-Engine-Repo
python -m pip install -e .
```

Requirements: Python 3.8+, NumPy 1.20+, SciPy 1.7+.

SciPy is technically optional. Modules that use `scipy.linalg.expm`,
`scipy.integrate.solve_ivp`, or `scipy.integrate.quad` import them via a
try/except pattern with pure-numpy fallbacks in `apf/numeric_fallback.py`.
The canonical run path uses SciPy; the fallback is for environments where
it isn't available.

---

## Citation

If you cite this codebase:

```bibtex
@software{Brooke_APF_v7_1_2026,
  author       = {Brooke, E. S.},
  title        = {{Admissibility Physics: Unified Theorem Bank
                   and Verification Engine, v7.1}},
  year         = {2026},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.18529115},
  url          = {https://github.com/Ethan-Brooke/APF-Engine-Repo}
}
```

For paper-level citations see each paper's Zenodo deposit (table above).

---

## Author

E. S. Brooke -- brooke.ethan@gmail.com  
ORCID: [0009-0001-2261-4682](https://orcid.org/0009-0001-2261-4682)  
LinkedIn: [ethanbrooke](https://www.linkedin.com/in/ethanbrooke/)

---

## License

MIT. See `LICENSE`.

---

## Status

This is research code. The 448-check verification suite is the spec; the
papers are the prose guides. The framework is falsifiable on each of its
48 quantitative predictions; the H_0 tension is stated explicitly in
Paper 6 §11.4 as the most pressing live falsifier.

For AI agents loading this repo cold: the engine-repo build (sibling repo)
ships an `ai_context/` pack with a corpus-level claims ledger, anti-
hallucination guards, and a curated wiki subset. This codebase repo
intentionally keeps its scope to the executable content; the corpus-level
orientation lives in the engine repo.
