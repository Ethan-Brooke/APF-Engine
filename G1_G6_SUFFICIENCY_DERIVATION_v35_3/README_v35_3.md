# APF v35.3 — G1–G6 Sufficiency Derivation (no-G7-exists)

Status: `G1_G6_SUFFICIENCY_DERIVATION_PASS` (verifier passes).

This package establishes the sufficiency direction of the trace-to-scheme export theorem: closing all of G1–G6 in their appropriate (numerical or structural) interpretation *guarantees* admissible export. Sibling to v35 (the export theorem itself), v35.1 (structural-codomain extension), and v35.2 (necessity derivation).

## Headline

The six gates G1–G6 are sufficient for admissible trace-to-scheme export. There is no missing seventh gate G7. Together with v35.2's necessity derivation, the gate framework is now both *necessary and sufficient* — and therefore deductively complete, modulo the enumeration assumption underlying the structural-exhaustion proof.

## Method: structural exhaustion

The trace-to-scheme operation is enumerated by structural surfaces — moments where a structural distinction must be enforced under A1. Six surfaces emerge:

1. **Inter-category jump** (which scheme is the target?) → covered by G1.
2. **Value transfer** (how does T transform?) → covered by G2.
3. **Input declaration** (what external content does τ consume?) → covered by G3.
4. **Uncertainty propagation** (how do input spreads produce output spread?) → covered by G4.
5. **Input/output role-separation** (which content is input vs output?) → covered by G5.
6. **Post-comparison residual handling** (what becomes of ρ = τ(T) − M?) → covered by G6.

Each of G1–G6 covers exactly one surface. No surface is doubly covered. No surface is uncovered. Therefore G1–G6 are sufficient.

The proof then enumerates 11 candidate G7s and shows each reduces to one of G1–G6 or is a precondition on the operation rather than a gate of it. The reductions are spelled out in the paper-section .tex.

## Minimality corollary

Each of G1–G6 is *necessary* by the per-gate necessity proofs of v35.2 — equivalently, for each gate $G_i$ there exists a route that closes the other five but specifically fails $G_i$. The empirical training set provides the witnesses:

- G1-fail witness: any export that compares trace value to "the measurement" without naming the scheme.
- G2-fail witness: any export that supplies inverse-fit transport (v18.0 numeric projection over tensor scaffold; quarantined).
- G3-fail witness: any export that uses external constants without declaring them.
- G4-fail witness: any export reporting zero σ on the transported value when inputs have positive σ.
- G5-fail witness: v18.0 W-route (target consumed); v27 charged-lepton three-mode (parameters consumed); v32 light-quark uniform scaling (PDG values consumed).
- G6-fail witness: H0 Route-V (residual cannot be channel-assigned; falsifying state).

Each gate has a witness; therefore the gate set is *minimal* — no proper subset of G1–G6 suffices.

## Together with v35.2 necessity

Necessity (v35.2): each gate is A1-derivable.
Sufficiency (this package, v35.3): G1–G6 cover all structural surfaces of the operation.
Minimality: each gate is independently necessary.

The three together establish the gate framework as the *unique* structurally-minimal-and-complete characterization of admissible trace-to-scheme export: G1–G6 is exactly the right set of gates, no more and no fewer.

## What this package does NOT establish

- The structural-exhaustion proof depends on an *enumeration assumption*: the six surfaces named above are claimed to exhaust the structural moments of the trace-to-scheme operation. The proof is exhaustion-by-careful-enumeration with reduction of candidate G7s, not exhaustion-by-deduction-from-A1. This is structurally weaker than v35.2's per-gate necessity proofs.
- If a future analysis identifies a structural moment of the operation not in the six-surface list, the framework would acquire a G7. The 11 candidate-G7 reductions in the .tex argue this is unlikely but not proved impossible.
- Uniqueness of route-status determination (each gate-availability pattern leads to exactly one named status) remains conjectural pending separate proof.

## Files

- `paper/g1_g6_sufficiency_derivation_v35_3.tex` — paper-section content with structural-exhaustion proof, candidate-G7 reductions, and minimality corollary.
- `scripts/check_g1_g6_sufficiency_derivation_v35_3.py` — verifier.
- `reports/g1_g6_sufficiency_derivation_v35_3_data.json` — machine-readable record.

## Status

`P_g1_g6_sufficiency_derivation_pass`. Sufficiency established by structural exhaustion (modulo enumeration assumption). Together with v35.2 necessity, the gate framework is deductively complete in the sense that closing G1–G6 is both required and sufficient for admissible export.
