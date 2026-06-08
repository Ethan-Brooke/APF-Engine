# APF v35.5 — Categorical Uniqueness of TtS

Status: `G1_G6_CATEGORICAL_UNIQUENESS_PASS` (verifier passes).

This package closes the categorical-formalization assumption of v35.4 by characterizing $\mathbf{TtS}$ — the trace-to-scheme category — uniquely up to categorical equivalence among categories that capture the trace-to-scheme operation. With v35.5 landed, the gate framework reaches deductive completeness: G1–G6 are necessary, sufficient (two routes), minimal, and uniquely so via $\mathbf{TtS}$.

## Headline

The trace-to-scheme category $\mathbf{TtS}$ defined in v35.4 is *uniquely characterized* among operation-capturing categories by three properties applied to its morphism data:

- **Categorical necessity**: any category capturing the trace-to-scheme operation must include all six morphism-data pieces (target object, map graph, parameter set, probabilistic structure, role separation, comparison residual).
- **Categorical sufficiency**: a category with exactly these six morphism-data pieces captures the operation; no additional structure is required.
- **Categorical minimality**: no proper subset of the six pieces captures the operation; each piece corresponds to an A1-imposed cost-payment that cannot be absorbed into the others.

Together, these three properties characterize $\mathbf{TtS}$ up to categorical equivalence: any other category satisfying all three is equivalent to $\mathbf{TtS}$.

## What this package establishes

- **Categorical necessity of morphism data.** Any category $\mathbf{C}$ that captures the trace-to-scheme operation as morphism-shaped objects must include all six morphism-data pieces. Each piece corresponds to a structural surface the operation has by its categorical type; omitting any piece means the corresponding surface is unspecified, and the category fails to capture the operation as $\mathbf{TtS}$ does.

- **Categorical sufficiency of morphism data.** A category $\mathbf{C}$ with exactly the six morphism-data pieces captures the operation. The data exhausts the operation's structural specification (as proved in v35.4); $\mathbf{C}$ has all the pieces; therefore $\mathbf{C}$'s morphisms are admissible exports.

- **Categorical minimality of morphism data.** No proper subset of the six pieces captures the operation. Each piece corresponds to an A1-imposed cost-payment witnessed by a specific framework instance:
  - Target object missing → unnamed-codomain comparisons (G1 fail)
  - Map graph missing → no transport (G2 fail)
  - Parameter set missing → undeclared external content (G3 fail)
  - Probabilistic structure missing → zero-spread overclaim (G4 fail)
  - Role separation missing → smuggling (G5 fail; v18.0/v27/v32 witnesses)
  - Comparison residual missing → unassigned residuals (G6 fail; H0 Route-V)

- **Equivalence theorem.** Any category satisfying necessity + sufficiency + minimality is categorically equivalent to $\mathbf{TtS}$. The functor $F: \mathbf{TtS} \to \mathbf{C}$ that maps the morphism data piece-by-piece is fully faithful and essentially surjective.

## What this package upgrades from v35.4

v35.4 derived sufficiency by appealing to the categorical-formalization assumption: that $\mathbf{TtS}$ as defined captures the operation. v35.5 closes this assumption by characterizing $\mathbf{TtS}$ uniquely through necessity + sufficiency + minimality of its morphism data. The categorical-formalization assumption is no longer a load-bearing assumption — it follows from the uniqueness theorem.

## Joint state of the gate framework after v35.5

Six layers, deductively complete:

1. **Necessity of G1–G6** (v35.2): each gate is A1-derivable. Per-lemma deductive proofs.
2. **Sufficiency by enumeration** (v35.3): six surfaces enumerated; eleven candidate G7s reduce.
3. **Sufficiency by deduction** (v35.4): morphism-data exhaustion in $\mathbf{TtS}$; A1 forces gates by data correspondence.
4. **Minimality** (v35.3 corollary): each gate has independent witness.
5. **Categorical uniqueness** (this package, v35.5): $\mathbf{TtS}$ is unique up to categorical equivalence among operation-capturing categories.

The full theorem reads: *A trace-to-scheme route admits physical export if and only if the six gates G1–G6 (uniquely characterized by the morphism data of the categorically-unique trace-to-scheme category $\mathbf{TtS}$) all close in their appropriate (numerical or structural) interpretation.*

## What this package does NOT establish

- **Universality of A1 for the operation.** The proof characterizes $\mathbf{TtS}$ given that A1 is the foundational axiom. If a different foundational axiom were chosen, a different category and different gates would result. The gate framework is conditional on A1.
- **Bank module.** The package is paper-side only; codifying the categorical uniqueness theorem as bank-registered checks remains as a separate consideration.
- **Uniqueness of route-status determination.** The lemma that each gate-availability pattern leads to exactly one named status remains conjectural; it is empirically nine-for-nine but not deductively proved. Companion theorem to v35.5.

## Files

- `paper/g1_g6_categorical_uniqueness_v35_5.tex` — paper-section content with categorical necessity + sufficiency + minimality + equivalence theorem.
- `scripts/check_g1_g6_categorical_uniqueness_v35_5.py` — verifier.
- `reports/g1_g6_categorical_uniqueness_v35_5_data.json` — machine-readable record.

## Status

`P_g1_g6_categorical_uniqueness_pass`. Categorical uniqueness established via three-property characterization. The gate framework is now deductively complete modulo the choice of foundational axiom (A1).
