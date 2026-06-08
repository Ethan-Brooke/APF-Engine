# Companion: APF Lattice Constraint Manifest v0.1

This companion document explains the manifest's semantics and scope categories. The structured data lives in `../manifest.json`; this doc explains how to read it.

## The lattice as the second-epsilon commitment space

Per `check_T_kappa` (apf/core.py), every enforcement channel spends exactly $2\varepsilon$: the first $\varepsilon$ at $\Gamma_S$ (own existence, $L_{nc}$), the second $\varepsilon$ at $\Gamma_E$ (environment record, $L_{irr}$). The second-$\varepsilon$ has 102 commitment options per channel:

- **60 options** committing to a specific partner channel $j \neq i$ (Sector A; bilateral matching targets in $V_{61} \setminus \{\text{self}}$);
- **42 options** committing to a specific vacuum mode in $V_{\rm global}$ (Sector B; the global-interface stratum from $T_{12}$).

The (61, 102) lattice is the lookup table for these commitment propositions. A *flow configuration* is an assignment of values $\in [0, 1]$ to every cell, encoding the rate or probability that each commitment is active. **Admissibility constraints determine which flow configurations are physically realizable.**

The framework's predictive power lives entirely in the constraints. A generic 61 × 102 matrix with arbitrary entries is *not* an APF state — it's just a matrix. The manifest catalogs the rules that distinguish APF-admissible configurations from arbitrary ones.

## Scope categories

Every constraint in the manifest has a `scope` field. The categories and their semantics:

| Scope | Meaning | Validator action |
|---|---|---|
| `global` | Constrains a configuration-level invariant (sum, ratio, entropy, partition function) | Reduce the lattice to a scalar, compare against bank-witnessed expected value |
| `cell_level` | Constrains a single cell's value independently | Check each cell against the rule |
| `row_constraint` | Constrains a single row's structure (sum, sparsity, non-zero count) | Reduce each row to its invariant, check |
| `block_constraint` | Constrains a submatrix (e.g., Sector A block, Sector B block) | Extract the submatrix, run checks |
| `block_coupling` | Couples cells across a submatrix (e.g., symmetry, twin identity) | Check the coupling holds element-by-element |
| `row_block` | Constrains a contiguous set of rows (e.g., visible rows 0–2) | Extract rows, run sector-specific checks |
| `cross_sector` | Couples flows in different sector partitions | Compute the cross-sector invariant, check |
| `composed` | A consistency check across multiple lower-level constraints | Verify all components hold simultaneously |
| `dimension_fix` | Fixes the lattice's row or column count itself | Trivial: confirm shape matches |
| `per_export_route` | Applies per scheme-export route (G1–G6) | Check route-specific certificate |

## Categories

| Category | Count | Purpose |
|---|---:|---|
| `foundational` | 5 | A1 + PLEC anchors (the deductive root) |
| `structural` | 8 | Lattice geometry (dimensions, partitions, identities) |
| `coupling` | 6 | Cross-sector consistency identities (I1–I4 unification) |
| `sector_specific` | 9 | Per-sector content (gauge template, sin²θ_W, dark-CDM, w_2(x)) |
| `admissibility` | 1 | Rigidity bounds beyond the foundational layer (κ_int) |
| `export` | 8 | Trace-to-scheme gates (G1–G6 + codomain_type + registry) |

## How a Stage 1 validator reads this

```python
import json, numpy as np
from pathlib import Path

manifest = json.loads(Path("manifest.json").read_text())

def validate_flow(flow: np.ndarray) -> dict:
    assert flow.shape == tuple(manifest["lattice"]["shape"])
    report = {"passed": [], "violated": [], "warnings": []}
    for c in manifest["constraints"]:
        result = check_constraint(c, flow)  # dispatched by scope+id
        bucket = "passed" if result["ok"] else "violated"
        report[bucket].append({"id": c["id"], "details": result})
    return report
```

The validator implementation lives in `apf/lattice_validator.py` (Stage 1, not yet built). The dispatch table for `check_constraint` maps each constraint `id` to its computational routine.

## Gaps in lattice expressibility

The audit surfaced gaps where the (61, 102) representation is partial:

### kinematic_DoF_not_lattice_cell

**Description.** Helicities, polarizations, and propagation degrees of freedom are KINEMATIC and do not contribute to capacity-channel count (check_L_count Step 3). The (61, 102) lattice represents STRUCTURAL enforcement, not kinematic motion.

**Implication.** Lattice does not directly carry propagation dynamics — those live in the action-internalization layer (Paper 7). A full engineering tool may need a second lattice for the kinematic layer, coupled to this one through Paper 7.

### global_constraints_not_per_cell

**Description.** A1 (finite capacity) is a global sum bound. ACC = K ln(d_eff) is a global accounting identity. I1–I4 unification identities are cross-sector. These constraints don't pinpoint specific cells but constrain configurations as wholes.

**Implication.** Validator must compute global invariants (sums, ratios, von Neumann entropy at max mixing, partition function limit) alongside per-cell rules and report violations at the configuration level, not the cell level.

### kappa_int_residual_bounded_not_predicted

**Description.** The cross-interface residual κ_int(S) is bounded structurally (two-sided rigidity) but its exact value within the bounds isn't predicted — the saturation regime is an open empirical question.

**Implication.** Cross-interface flow couplings have an envelope, not a point value. The validator should accept any value inside the envelope as admissible and surface where the envelope itself is the constraint.

### robust_empirical_P_pending_dark

**Description.** Dark-sector w(z) is at [P_internal_2FCR + P_DESI+CMB+DESY5_95]; robust empirical P pending MCMC + DESI gates 3/4 (full-shape exact runtime + full-growth likelihood).

**Implication.** Vacuum-sector flow constraints have an empirical-promotion queue. The validator should mark vacuum-row flow predictions with their current export status, not treat them as fully closed.

### second_lattice_for_interface_dynamics

**Description.** The current lattice represents one interface (one capacity-allocation snapshot). Dynamics ACROSS multiple interfaces (e.g., how matter at one interface couples to matter at another) require a multi-lattice / interface-graph representation, not captured in (61, 102) alone.

**Implication.** Stage 1 validator handles single-interface admissibility. Multi-interface coupling is a Stage 2+ object that requires an extended representation (lattice × graph).

### non_SM_engineered_systems_unmapped

**Description.** The (61, 102) lattice is SM-specific: 61 = 45+4+12 is the SM channel count, 42 is the V_global dimension at the SM cosmological partition. For non-SM engineered systems (QEC codes, communication channels, distributed systems), the analog lattice dimensions would differ.

**Implication.** Stage 3 (engineering generalization) requires re-deriving the lattice dimensions and constraint cascade for each target engineered system. The Stage 0 manifest is the template, not the instance.


## Design notes for Stage 1

- Read this manifest as the constraint rule-set. For each entry with category=foundational/structural/coupling, implement a check function that takes a (61, 102) numpy array and returns ConstraintResult{passed, violations_at_cells, details}.
- Sector-specific entries can be lifted to validator functions when the user wants per-sector validation; not required for v0.1 validator (only the cross-cutting rules are mandatory for admissibility).
- Export gates (G1–G6) are per-route, not per-cell; the validator's export mode takes a route name plus the lattice configuration and checks the 6 gates against the route's existing certificate.
- Global constraints (A1, ACC unification, I1–I4) require computing configuration-level invariants. Implementation: compute these as sum/log/entropy reductions over the lattice; check against the bank-witnessed expected values.
- MD floor + BW ceiling are per-cell and trivial to check.
- Sector A bilateral + monogamy require the canonical channel→column index map. The map is: column j in Sector A (j ∈ [0, 59]) corresponds to channel f(j) where f handles self-exclusion; in the cleanest convention f(j) = j for j < i, and (j+1) for j >= i, parameterized by row i. The validator implementation must fix this convention explicitly.

## Versioning + update discipline

This is **v0.1**. Update triggers:

- A new load-bearing bank check lands → add a constraint entry.
- A constraint promotes from `[P_structural]` to `[P]` or vice versa → update `epistemic_tag`.
- A lattice gap closes (e.g., a Stage 2 representation extends to multi-interface coupling) → remove or update the gap entry.
- A new export route registers in `apf/codomain_transport_schema.py` → reflect in the export-gates section.

Major schema breaks bump to v0.2, v0.3, etc. The schema is not yet frozen; expect iteration through Stage 1.

## Provenance

Built from the v24.1 codebase via in-conversation audit. Bank docstrings read for: `apf/core.py`, `apf/gauge.py`, `apf/gravity.py`, `apf/plec.py`, `apf/unification.py`, `apf/unification_three_levels.py`, `apf/foundation_inputs.py`, `apf/kappa_int_bounds.py`, `apf/codomain_transport_schema.py`, `apf/cosmology.py`, `apf/generations.py`. Build script: `outputs/build_lattice_manifest.py`.
