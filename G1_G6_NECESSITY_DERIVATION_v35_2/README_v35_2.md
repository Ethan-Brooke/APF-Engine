# APF v35.2 — G1–G6 Necessity Derivation from A1

Status: `G1_G6_NECESSITY_DERIVATION_PASS` (verifier passes).

This package packages the in-chat G1–G6 necessity derivation (2026-05-10 LATEST-17) as a paper-side .tex artifact, sibling to the v35 export-theorem pack (`TRACE_TO_SCHEME_EXPORT_THEOREM_v35/`) and the v35.1 structural-extension pack (`STRUCTURAL_EXTENSION_v35_1/`).

## Headline

The six gates G1–G6 of the trace-to-scheme export theorem are *necessary* conditions, derivable from APF's foundational axiom A1 plus its corpus-derived corollaries (MD: distinction floor; BW: cost-spectrum non-degeneracy) and the categorical structure of trace and physical-scheme categories. Each gate is the structural form of a single A1 commitment applied to one moment of the export operation.

## What this package establishes

- **G1–G6 are necessary conditions on any admissible trace-to-scheme export.** Each lemma proves that violating its gate leads to a violation of A1 (or an A1-derived corollary). The derivation is deductive at lemma granularity.

- **The framework's audit-first refusals of fits — v18.0 W-route numeric projection, v27 charged-lepton three-mode reconstruction, v32 light-quark uniform scaling — are now theorem-required, not stylistic.** Each refusal corresponds to a specific gate (G5 and/or G6) the fit would fail. Under A1, the framework had no choice.

- **The route-by-route epistemic specificity emerged on 2026-05-10 (W and bottom at `[P_export_candidate]`, top at `[P_trace + ext-MSR codomain]`, charm and light-quark at `[P_obstruction_named]`, charged-lepton at `[P_trace + norm + residual_closeout]`) is now *derived* from which subset of G1–G6 each route closes, not just observed empirically.**

## What this package does not establish

- **Sufficiency** — that closing all of G1–G6 *guarantees* admissible export — remains open. The empirical six-for-six (mass routes) plus three-for-three (closed RPs) is consistent with sufficiency but is not a proof. A sufficiency proof would proceed by structural exhaustion of the trace-to-scheme operation's surfaces (cf. v35.1's gate-list discussion). Sufficiency is the next theorem program after this artifact lands.

- **Uniqueness of route status determination** — that each gate-availability pattern leads to exactly one named status — remains conjectural. Empirically nine-for-nine (six mass routes + RP1 + RP3 + RP6) but not deductively proved.

## Files

- `paper/g1_g6_necessity_derivation_v35_2.tex` — paper-section content suitable for absorption into a Paper 1 supplement (load-bearing structural theorem) or a Paper 32-class supplement adjacent to the v35 export-theorem section.
- `scripts/check_g1_g6_necessity_derivation_v35_2.py` — verifier checking lemma statements + audit-first-refusal mapping (v18.0 → G5/G6, v27 → G5/G6, v32 → G2/G5).
- `reports/g1_g6_necessity_derivation_v35_2_data.json` — machine-readable lemma + foundation + audit-refusal records.

## Status

`P_g1_g6_necessity_derivation_pass`. Necessity established at lemma granularity. Sufficiency open as next theorem program.

## Not claimed

- This package does not register any new bank module. Adding a bank module that codifies the six lemmas as tier-3 [P_structural] checks is a separate consideration; the current package is paper-side only.
- The deductive proof here covers necessity, not sufficiency.
- Uniqueness of status determination is not addressed.
