# Admissibility Physics Framework (APF) — Engine

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18529115.svg)](https://doi.org/10.5281/zenodo.18529115)
[![Zenodo community](https://img.shields.io/badge/Zenodo-admissibility__physics-1f77b4)](https://zenodo.org/communities/admissibility_physics)
[![checks](https://img.shields.io/badge/bank--registered-3745%20PASS-success)](verify_all.py)
[![free dimensionless params](https://img.shields.io/badge/free%20dimensionless%20params-0-brightgreen)](#prediction-scorecard)

A machine-verifiable theorem bank that derives the Standard Model gauge group, fermion
content, electroweak coupling structure, and the cosmological capacity partition from a
single primitive — finite enforcement capacity — with **zero free dimensionless
parameters** (one dimensional anchor: the Planck magnitude, equivalently the size of the
universe).

This repository is the canonical codebase behind the Admissibility Physics corpus. Every
load-bearing claim in the papers traces to a named check function in the `apf/` package,
and the full suite verifies in well under a minute.

> **Cite the engine:** Brooke, E. *Admissibility Physics: Unified Theorem Bank and
> Verification Engine.* Zenodo. Concept DOI **[10.5281/zenodo.18529115](https://doi.org/10.5281/zenodo.18529115)**
> (always resolves to the latest version). The whole corpus is collected in the Zenodo
> community **[admissibility_physics](https://zenodo.org/communities/admissibility_physics)**.

```bash
git clone https://github.com/Ethan-Brooke/APF-Engine.git
cd APF-Engine
pip install -e .
python verify_all.py
```

The bank carries **3,745 registered theorems across 422 typed modules** (v24.3.249).

## What is this?

APF takes finite enforcement seriously as a physical quantity. The **Principle of Least
Enforcement Cost (PLEC)** has four constitutive features:

| Feature | Statement |
|---------|-----------|
| **A1** (finiteness) | At every causally connected region, total enforcement cost is bounded above by a finite capacity. |
| **MD** (cost floor) | Each maintained distinction carries a positive cost floor μ\* > 0. |
| **A2** (argmin) | The realized configuration is the argmin of total enforcement cost over the admissible set. |
| **BW** (non-degeneracy) | The cost spectrum is non-degenerate, so the argmin is unique up to gauge equivalence. |

From these, the framework forces the SU(3) × SU(2) × U(1) gauge group, three generations
of 45 fermions, the capacity ledger C_total = 61, sin²θ_W = 3/13, Ω_Λ = 42/61, and the
rest of the constants map — as discrete values, ratios, and identities rather than fitted
inputs.

## Prediction scorecard

49 quantitative predictions, zero free dimensionless parameters (one dimensional anchor).
40 tested; 33/40 within 3σ; mean error 3.77%, median 0.51%.

## The corpus

Every paper is on Zenodo under the [admissibility_physics](https://zenodo.org/communities/admissibility_physics)
community. DOIs below are concept DOIs — they always resolve to the latest version.

| # | Title | DOI | Technical Supplement |
|--:|-------|-----|----------------------|
| 0 | What Physics Permits — A Constraint-First Framework for Physics | [18439523](https://doi.org/10.5281/zenodo.18439523) | — |
| 1 | The Enforceability of Distinction | [18439200](https://doi.org/10.5281/zenodo.18439200) | [19714957](https://doi.org/10.5281/zenodo.19714957) |
| 2 | Finite Admissibility and the Failure of Global Description | [18439274](https://doi.org/10.5281/zenodo.18439274) | [19714959](https://doi.org/10.5281/zenodo.19714959) |
| 3 | Entropy, Time, and Accumulated Cost | [18439363](https://doi.org/10.5281/zenodo.18439363) | [19714961](https://doi.org/10.5281/zenodo.19714961) |
| 4 | Admissibility Constraints and Structural Saturation | [18439397](https://doi.org/10.5281/zenodo.18439397) | [19714963](https://doi.org/10.5281/zenodo.19714963) |
| 5 | Quantum Structure from Finite Enforceability | [18439433](https://doi.org/10.5281/zenodo.18439433) | [19908706](https://doi.org/10.5281/zenodo.19908706) |
| 6 | Dynamics and Geometry as Optimal Admissible Reallocation | [18439445](https://doi.org/10.5281/zenodo.18439445) | [19714967](https://doi.org/10.5281/zenodo.19714967) |
| 7 | A Minimal Quantum of Action from Finite Admissibility | [18439513](https://doi.org/10.5281/zenodo.18439513) | [19714969](https://doi.org/10.5281/zenodo.19714969) |
| 8 | The Admissibility-Capacity Ledger | [19721384](https://doi.org/10.5281/zenodo.19721384) | [19714971](https://doi.org/10.5281/zenodo.19714971) |
| 9 | The Geometric Substrate as Cost Structure of Comparison Continuations | [20041675](https://doi.org/10.5281/zenodo.20041675) | — |
| 10 | The Calculus of Finite Continuability | [20041680](https://doi.org/10.5281/zenodo.20041680) | — |
| 11 | Forced Universality from Capacity-Bounded Admissibility | [20684198](https://doi.org/10.5281/zenodo.20684198) | [20684204](https://doi.org/10.5281/zenodo.20684204) |
| 13 | The Minimal Admissibility Core | [18361446](https://doi.org/10.5281/zenodo.18361446) | — |
| 16 | Markov Breakdown and the Hard Problems | [20684207](https://doi.org/10.5281/zenodo.20684207) | — |
| 18 | The Electroweak Sector as a Capacity Equilibrium | [20684209](https://doi.org/10.5281/zenodo.20684209) | — |
| 20 | The Enforcement Crystal | [18531732](https://doi.org/10.5281/zenodo.18531732) | — |
| 21 | APF Engine — Unified Theorem Bank and Verification Engine | [18529115](https://doi.org/10.5281/zenodo.18529115) | — |
| 24 | The Recruitment-Radius Extension — Foundations | [20684211](https://doi.org/10.5281/zenodo.20684211) | [20684213](https://doi.org/10.5281/zenodo.20684213) |
| 28 | Absolute Mass Scales from Electroweak Capacity Saturation | [20684215](https://doi.org/10.5281/zenodo.20684215) | — |
| 29 | Plaquette Representation Dominance and Confinement | [20684218](https://doi.org/10.5281/zenodo.20684218) | — |
| 30 | A Tube Mechanism for the Lattice Mass Gap | [20684220](https://doi.org/10.5281/zenodo.20684220) | — |
| 31 | Osterwalder–Schrader Structure of Lattice Yang–Mills | [20684222](https://doi.org/10.5281/zenodo.20684222) | — |
| 33 | Trace-to-Scheme Export Architecture | [20684224](https://doi.org/10.5281/zenodo.20684224) | [20684226](https://doi.org/10.5281/zenodo.20684226) |
| 35 | The Dark Sector as a Two-Role Capacity Decomposition | [20684228](https://doi.org/10.5281/zenodo.20684228) | [20684232](https://doi.org/10.5281/zenodo.20684232) |
| 40 | Between Symmetry and the Void — The Thermodynamics of Finite Distinction | [20684235](https://doi.org/10.5281/zenodo.20684235) | [20684239](https://doi.org/10.5281/zenodo.20684239) |
| 41 | The Horizon as a Continuation Ledger | [20684241](https://doi.org/10.5281/zenodo.20684241) | [20684243](https://doi.org/10.5281/zenodo.20684243) |
| 42 | The Weak Mixing Angle Is Not Free | [20684245](https://doi.org/10.5281/zenodo.20684245) | — |

## Repository layout

```
apf/                 the theorem bank — one module per result; registers at import
apf/_module_manifest.py   the canonical module index + MODULE_TYPES taxonomy
scripts/             utilities and orchestration
standalone/          standalone lemma modules
examples/            worked examples
verify_all.py        runs the full bank and prints the scorecard
```

## License

CC-BY-4.0. Author: Ethan Brooke, Independent Researcher, San Anselmo, California, USA.
ORCID [0009-0001-2261-4682](https://orcid.org/0009-0001-2261-4682) ·
[LinkedIn](https://www.linkedin.com/in/ethanbrooke/) ·
[GitHub](https://github.com/Ethan-Brooke) · brooke.ethan@gmail.com
