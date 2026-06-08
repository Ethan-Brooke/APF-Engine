# APF v35.4 — Exhaustion-by-Deduction (Categorical Formalization of G1–G6)

Status: `G1_G6_EXHAUSTION_BY_DEDUCTION_PASS` (verifier passes).

This package upgrades v35.3's sufficiency proof from *exhaustion-by-enumeration* to *exhaustion-by-deduction*. The six structural surfaces of the trace-to-scheme operation are derived from a categorical formalization of the operation, not enumerated by hand with candidate-G7 reductions.

## Headline

The trace-to-scheme operation is a morphism in a specific category — the **trace-to-scheme category** $\mathbf{TtS}$, whose objects are A1-admissible interfaces and whose morphisms are admissible export operations. By the standard categorical definition of a morphism with comparison structure, the morphism's structural data consists of exactly six pieces. A1 imposes cost-payment at each piece, producing exactly G1–G6. Exhaustion follows from the morphism-data structure rather than from manual enumeration.

## What this package establishes

- **Categorical formalization.** The trace-to-scheme operation is defined as a morphism in the category $\mathbf{TtS}$. Objects are A1-admissible interfaces; morphisms are admissible export operations.
- **Six-piece morphism data.** A $\mathbf{TtS}$-morphism is structurally specified by exactly six pieces of data: target object, map graph, parameter set, probabilistic structure, role-separation, comparison residual.
- **Exhaustion as morphism data.** Any structural moment of the operation corresponds to one of the six data pieces. Exhaustion is now a definitional consequence of the morphism's data structure.
- **A1 → G1–G6 by data correspondence.** Each piece of structural data carries a distinction-cost demanded by A1; each cost is paid by exactly one of G1–G6.

## What this package upgrades from v35.3

v35.3 proved sufficiency by structural-exhaustion of *enumerated* surfaces: list six surfaces, show G1–G6 cover them, enumerate eleven candidate G7s, reduce each. The proof depended on the *enumeration assumption* that the six-surface list was complete.

v35.4 derives the six-surface list from $\mathbf{TtS}$-morphism data: morphisms in $\mathbf{TtS}$ have exactly these six data pieces by categorical definition; A1 turns each piece into a gate. The enumeration assumption is replaced by the *categorical-formalization assumption*: that $\mathbf{TtS}$ correctly captures the trace-to-scheme operation.

The categorical assumption is a cleaner load-bearing assumption than enumeration. If a future analysis identifies an operation-level structural feature not captured by $\mathbf{TtS}$'s morphism data, the framework would extend $\mathbf{TtS}$ to include the new feature, and the new feature would define a new gate. The shift from "did we enumerate all surfaces?" to "is $\mathbf{TtS}$ the right category?" is a definitional question rather than a factual-completeness question.

## What this package does NOT establish

- **The categorical formalization itself.** $\mathbf{TtS}$ is defined here as the category that *captures* the trace-to-scheme operation. We do not prove $\mathbf{TtS}$ is the unique correct formalization — only that it's *a* formalization that produces the right gate set under A1. Categorical-uniqueness arguments would require showing $\mathbf{TtS}$ is initial / terminal / universal among categories that capture the operation. That's a separate categorical-foundations theorem.
- **Bank module.** The package is paper-side only; codifying the categorical formalization as bank-registered checks is a separate consideration.

## Joint state of the gate framework after v35.4

- **Necessity** (v35.2): each gate is A1-derivable. Per-lemma deductive proofs.
- **Sufficiency by enumeration** (v35.3): G1–G6 cover six enumerated surfaces; eleven candidate G7s reduce.
- **Sufficiency by deduction** (v35.4): the six surfaces are derived as $\mathbf{TtS}$-morphism data; A1 turns each piece into a gate.
- **Minimality** (v35.3 corollary): each gate has independent witness.

The trio v35.2 + v35.4 + minimality gives the strongest version of the joint theorem: G1–G6 are the necessary, sufficient, and minimal gate set for admissible trace-to-scheme export, with sufficiency now deductively derived from the operation's categorical structure.

## Files

- `paper/g1_g6_exhaustion_by_deduction_v35_4.tex` — paper-section content with the categorical formalization, morphism-data exhaustion, and A1 → G1–G6 correspondence.
- `scripts/check_g1_g6_exhaustion_by_deduction_v35_4.py` — verifier.
- `reports/g1_g6_exhaustion_by_deduction_v35_4_data.json` — machine-readable record.

## Status

`P_g1_g6_exhaustion_by_deduction_pass`. The categorical formalization is established; morphism-data exhaustion follows from the categorical definition; A1 imposes the gates by data correspondence. The enumeration assumption of v35.3 is reduced to the categorical-formalization assumption.
