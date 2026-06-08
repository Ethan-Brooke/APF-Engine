# APF Core Model Package — for AI Upload

This package is a **tight subset** of the full APF codebase (v7.5; ~70 files) — the load-bearing model spine + the executable witnesses + the orientation doc. It is intended for upload to an AI assistant with limited file-count budget. The full codebase has phenomenology / cosmology / session-specific modules that aren't in this package; if the AI needs those, point it at the GitHub release.

## What's in this package (15 files)

### Orientation
- `GENERIC_LLM.md` — start here. Self-contained AI orientation guide.
- `README.md` — codebase overview.

### Foundational primitives + bedrock
- `apf/core.py` — A1, MD, A2, BW. The four constitutive features of the framework on FD1 (admissibility space's bedrock). Foundational lemmas (`L_nc`, `L_irr`, `L_col`, `L_count`, `L_ε*`), `T_alg`, monogamy `T_M` biconditional, Theorem R sub-clauses. ~6,200 lines, ~50 bank-registered checks.
- `apf/aps.py` — Admissible Possibility Space primitive (Paper 1 Supplement v7.1). Continuation preorder. The set-theoretic substrate per FD1.
- `apf/plec.py` — Principle of Least Enforcement Cost: Regime R + the five-type regime-exit taxonomy.

### Executable witnesses (small finite models)
- `apf/paper1_kernel.py` — FD1 executable witness on a 4-element substrate, capacity C = 5, MD floor μ* = 1.
- `apf/formal_kernel.py` — V_61 executable witness at the Standard-Model interface (G_SM representation, V_Λ uniqueness).

### Standard Model + cosmology bridges
- `apf/gauge.py` — Theorem R, `L_gauge_template_uniqueness`, `T_gauge` (the SU(3) × SU(2) × U(1) selection result). ~4,300 lines.
- `apf/unification.py` — Admissibility-Capacity Ledger (ACC record, six π-projections, four consistency identities I1/I2/I3/I4, composed `T_ACC_unification`).

### Phase 22 quantum derivations (Paper 5 supplement landing)
- `apf/quantum_admissibility.py` — Phase 22b. SepStr/SepAdm/IJCStr/IJCAdm/IJCPres branch taxonomy, κ_Bool minimum, capacity lower-bound certificate, Quantum Admissibility Condition, ℂ-field selection (uniform-defect form), Born trace rule.
- `apf/closed_world_completeness.py` — Phase 22c + 22d. The closed-world ledger conservation + no-phantom-records derivation chain that derives the three formerly-axiom-class regime gates (reciprocal calibration, stable simple-record completeness, APF-complete composite closure) from a deeper APF primitive. Headline meta-theorem: `T_closed_world_completeness_derives_three_gates`.

### Registry + runner
- `apf/bank.py` — global theorem registry, `EXPECTED_THEOREM_COUNT = 454`.
- `apf/__init__.py` — module init.
- `verify_all.py` — runner. `python verify_all.py` runs all 471 checks.
- `setup.py` — package metadata, version 7.5.0.

## Counts (v7.5, post-Phase-22d)

- 454 bank-registered theorems
- 471 total verify_all checks (467 PASS; 4 pre-existing scipy-import failures)
- 39 registered modules + apf/standalone/
- 48 quantitative predictions, 0 free parameters

## What is NOT in this package

The full codebase has additional modules covering: cosmology details (cosmology.py, lambda_absolute.py, fractional_reading.py, thermal_absolute.py, lambda_operator_derivation.py), spacetime (spacetime.py), gravity / horizon (gravity.py, horizon_joint_bridge.py), generations / fermion masses (generations.py, majorana.py), internalization / spectral action (internalization.py, internalization_geo.py), extensions (extensions.py), red-team adversarial checks (red_team.py), Enforcement Crystal mechanization (crystal.py, crystal_metrics.py, crystal_axiom_roots.py), three-level identity refinements (unification_three_levels.py, unification_projection_essentiality.py, subspace_functors.py, i4_composition.py), session-specific deltas (session_*.py), validation suite (validation.py, supplements.py, test_no_smuggling.py), and standalone scripts (apf/standalone/).

If the AI needs any of these, fetch from the GitHub release at https://github.com/Ethan-Brooke (paper-companion repos) or the canonical Engine repo.

## How to read this package

1. Load `GENERIC_LLM.md` first — it self-orients an AI.
2. Then `README.md` for the codebase overview.
3. Then `apf/core.py` for the foundational primitives.
4. Then `apf/aps.py` and `apf/plec.py` for the bedrock-and-regime structure.
5. Then `apf/paper1_kernel.py` and `apf/formal_kernel.py` for the executable witnesses (these are the smallest, run-them-by-hand demonstrations).
6. Then `apf/gauge.py` and `apf/unification.py` for the Standard-Model and ACC-ledger structure.
7. Then `apf/quantum_admissibility.py` and `apf/closed_world_completeness.py` for the quantum-derivation chain.
8. `apf/bank.py` and `verify_all.py` are runtime; `python verify_all.py` exercises the whole package.

## Version

v7.5 (2026-04-29 evening, post-Phase-22d). Folder still named `APF_Codebase_v7.3` due to mount-rename limitation; functional state is v7.5.
