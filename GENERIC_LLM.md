# APF Orientation Guide — Generic LLM

*This guide is for any AI assistant being set up to work with the Admissibility Physics Framework. It is self-contained. You should be able to orient yourself from this document alone, then use the files in the repository to go deeper.*

---

## Overview in one paragraph

The Admissibility Physics Framework (APF) derives the structure of quantum mechanics and the Standard Model from a single primitive — finite enforcement capacity — plus a small set of regularity conditions. The result is one chain from a plain starting point ("maintaining a distinction costs something, and the budget is finite") through the gauge group, fermion content, the quantum formalism, Lorentzian spacetime, the Einstein field equations, and the cosmological constant, down to specific numbers. The engine in this repository is the machine-verifiable companion to that chain: it carries **3,745 bank-registered theorems across 422 typed modules (v24.3.249)**, every one a named check function, and the full suite verifies in well under a minute with exact rational arithmetic.

---

## The axiom and the argument

### A1 — finite enforcement capacity

> At every causally connected region, the total enforcement cost is bounded above by a finite capacity.

An *enforcement* is any physical process that maintains a distinction — a measurement, a boundary, a conservation law. The claim is that these processes are not free. They cost something, and the budget is finite. Three further conditions, packaged variationally as the **Principle of Least Enforcement Cost (PLEC)**, complete the foundation:

| Feature | Statement |
|---|---|
| **A1** (finiteness) | Total enforcement cost in any causally connected region is bounded above by a finite capacity. |
| **MD** (cost floor) | Each maintained distinction carries a positive cost floor μ\* > 0. |
| **A2** (argmin) | The realized configuration is the argmin of total enforcement cost over the admissible set. |
| **BW** (non-degeneracy) | The cost spectrum is non-degenerate, so the argmin is unique up to gauge equivalence. |

MD, A2, and BW are regularity conditions on the cost structure, not additional physics — closer to measurability or continuity assumptions in analysis than to new postulates about the world.

### Why this is not circular

A natural objection is that a cost function is already quantum-mechanical structure smuggled in. The cost here is pre-physical: it is a property of abstract distinctions, not of quantum states. The derivation runs cost structure → admissible state space → complex Hilbert space → quantum mechanics. The Hilbert space is the output, not the input. The space of maintained distinctions (the D-quotient) is a definitional commitment, openly adopted, not an import from quantum theory.

---

## What the framework forces

From A1 + MD + A2 + BW, the framework forces the SU(3) × SU(2) × U(1) gauge group, three generations of 45 fermions in the Standard Model representations, the capacity ledger C_total = 61, sin²θ_W = 3/13 as a ledger-share source value, Ω_Λ = 42/61, and the rest of the constants map — as discrete values, ratios, and identities rather than fitted inputs. There are zero free dimensionless parameters. One dimensional anchor remains: the Planck magnitude, equivalently the size of the universe.

### The layered chain

**Layer 0 — admissibility geometry.** The foundational lemmas fix the mathematical structure of enforcement cost: a positive minimum cost, locality, forced non-commutativity, and the cost-function form by a Cauchy-functional-equation argument.

**Layer I — quantum mechanics.** Enforcement geometry forces a complex Hilbert space (not real, not quaternionic); non-commuting observables; the Born rule as the unique enforcement-invariant probability assignment; and the Tsirelson bound from the enforcement budget.

**Layer II — the Standard Model.** Three carrier requirements identify what can carry the minimum viable enforcement structure; a scan over the compact simple Lie algebras leaves only the SU(N_c) × SU(2) × U(1) template; cost minimization fixes N_c = 3; and the fermion content comes out at 45 in the correct representations. The total enforcement cost C_total = 61 is rigid — altering any factor disturbs the whole prediction chain at once.

**Layer III — mass and mixing.** A single-channel Gram overlap x = 1/2 and a multiplicative-amplitude suppression law replace the Froggatt–Nielsen mechanism; the charged-fermion masses follow from a small number of anchors; the CKM and PMNS matrices come from capacity geometry.

**Layer IV — cosmology.** Horizon equipartition gives the density fractions; the dark budget gives Ω_Λ, Ω_DM, Ω_b; and the dark-energy equation of state sits at w₀ = −1.

---

## The code architecture

Every result is a `check_` function. Each returns a dict carrying at least a name, a status, its dependencies, and a one-line summary. Core results use `fractions.Fraction` for exact rational arithmetic — no floating-point "close enough" in the load-bearing checks. Modules register their checks at import; the bank composes them.

```
apf/                    the theorem bank — one module per result; registers at import
apf/_module_manifest.py the canonical module index + MODULE_TYPES taxonomy
scripts/                utilities and orchestration
standalone/             standalone lemma modules
examples/               worked examples
verify_all.py           runs the full bank and prints the scorecard
```

Naming: theorems are `T_…`, lemmas are `L_…`, and the public entry points are the matching `check_…` functions. `apf/_module_manifest.py` is the single source of truth for the module index and the expected registry size; `verify_all.py` prints the live count and the prediction scorecard. If you want to know the current state of the bank, run it — do not trust a count written into prose, including this paragraph.

### Epistemic ladder

Every claim carries a grade. `[P]` is proved from A1 (with MD/A2/BW). `[P_structural]` is proved up to a stated structural reading — closure on the present axioms, with the remaining seam named honestly. `[P+tool]` (or `[P+lattice]`) is proved but consumes an external import (a higher-loop runner, a lattice value). `[C]` is a conjecture, stated precisely and not yet proved. Read the grade before you read the result.

---

## How to run it

From a native shell (not a sandbox — see the storage note below):

```bash
git clone https://github.com/Ethan-Brooke/APF-Engine.git
cd APF-Engine
pip install -e .
python verify_all.py
```

`verify_all.py` runs the full bank and prints the scorecard: 48 quantitative predictions, 39 tested, 32/39 within 3σ, mean absolute error 3.83%, median 0.37%. Requirements: Python ≥ 3.8, numpy, and scipy (a small number of numerical checks need it — special functions, two-loop RG integrals, spectral-action moments); the exact-rational core uses only the standard library.

## Where the codebase lives

The live working tree is a git repository at `Dev/apf-codebase` on the principal machine, remote `Ethan-Brooke/APF-Engine`, branch `main`. The Google Drive copy under `__APF Library/Codebase/` is a frozen archival mirror — read-only. **Run every `git` operation (add, commit, push) in a native shell on the principal machine, never through a sandbox mount**: the bridge corrupts `.git/index`, and the remote is unreachable from inside a sandbox anyway. The commit is the archive; there is no separate zip-snapshot step for code.

---

## Key numbers to know

| Quantity | Value | Source |
|---|---|---|
| κ (enforcement multiplier) | 2 | T_kappa (derived) |
| x (Gram overlap) | 1/2 | L_Gram + T27c (derived) |
| C_total (enforcement cost) | 61 | L_count (rigid) |
| N_gen (generations) | 3 | derived |
| sin²θ_W (source / ledger share) | 3/13 ≈ 0.2308 | [P]; measured/effective angle stays [P_structural] |
| Ω_Λ | 42/61 | dark-budget partition |
| M_R spectrum | ≈ [31, 60, 174] GeV | low-scale seesaw |
| Σm_ν | ≈ 60 meV | within cosmological bounds |

---

## Honest accounting of open problems

| Problem | Status |
|---|---|
| Measured weak mixing angle | The source value 3/13 is `[P]` (ledger share). The measured/effective angle stays `[P_structural]`, behind the w ∝ g² observable dictionary — a structural feature on the present axioms, not a missing step. |
| Absolute Planck magnitude | The one dimensional anchor. Whether it is an output of a deeper finiteness condition, or irreducibly the one input a finite-capacity physics must accept, is open by design. |
| m_c at ≈ 2.6% | Charm-mass error is a Schur structural limit; multiple NNLO routes examined and rejected. Not a bug to fix. |
| Dark-sector empirical promotion | Theory side is parameter-free and closed; the live external gate is the DESI full-shape confrontation (exact runtime). Particle identity is not exported by design. |
| Two-loop electroweak precision | The native one-loop M_W is closed; two-loop precision is a `[P+tool]` import, not a native gap. |

---

## What APF is and is not

APF **is** a formal derivation program with machine-verified theorems, a claim that the quantum formalism and Standard Model structure follow from finite enforcement capacity, and a set of specific falsifiable predictions. It **is not** a theory of everything in the string-theory sense, it does not claim to derive Lagrangian dynamics from A1 alone, and it does not pretend its hardest seams are closed — the open problems above are stated rather than hidden.

---

## Common tasks

**Check whether a theorem is circular.** Read its `check_` function and its dependency list, then trace each dependency recursively, watching for any path that loops back — and for any input that is physics not yet derived from A1.

**Explain how the gauge group is derived.** Read, in order: the carrier-requirements check, the Lie-algebra-template scan, the cost-minimization to N_c = 3, and the fermion-content check, all in `apf/gauge.py`.

**Add a theorem.** State it precisely in plain English; list every import beyond A1+MD+BW; write the `check_` function with exact arithmetic; register it; run `verify_all.py` and confirm no regressions and that the expected count moved by exactly one.

**Find weak points.** Start with the adversarial checks and any `[C]` or `[P_structural]` grades; the open-problems table above points at the live seams.

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
