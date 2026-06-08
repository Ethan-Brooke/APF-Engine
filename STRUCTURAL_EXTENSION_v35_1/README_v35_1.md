# APF v35.1 — Structural-Codomain Extension of the Trace-to-Scheme Export Theorem

Status: `STRUCTURAL_EXTENSION_PASS` (worked-example verifier passes).

This package extends the v35 trace-to-scheme export theorem to cover *structural-codomain* routes — routes whose target codomain is theorem-shape rather than number-shape. The mass routes (W on-shell, bottom MSbar, top, charm, light-quark, charged-lepton) are all numerical-codomain routes; the framework's `closed` Reconstruction Programs (RP1 spacetime emergence, RP3 baryogenesis, RP6 inflation) include both numerical (RP3, RP6) and structural (RP1) codomains.

## Headline

The six gates G1–G6 of the export theorem (v35) read uniformly across the codomain-transport program when G4 and G6 are interpreted in their *structural form* for theorem-shape codomains:

- **G4 numerical form:** uncertainty/covariance propagated through transport.
- **G4 structural form:** *domain of validity declared* — the regime in which the structural derivation holds is named, with parked or excluded regimes explicit.
- **G6 numerical form:** residual assigned to a named covariance/operator/scheme/theory channel.
- **G6 structural form:** *named edge cases at the derivation's boundary* — regimes where the structural closure does not extend are explicitly named (parked, excluded, future theorem programs).

G1, G2, G3, G5 read identically in both forms.

## Worked example: RP1 spacetime emergence

The framework's tier-5 [P] closure of Riemannian/Lorentzian geometry from A1 + algebraic data is a structural-codomain route. Walking the gates:

- G1: GR-shape geometry (metric, conformal class, linearized Einstein equations) declared as codomain.
- G2: algebraic data → causal order → `[g]` (HKM 1976); algebraic data → metric (entanglement-first-law structure); first law → linearized Einstein. Non-inverse.
- G3: manifold theory + entanglement-entropy framework declared as mathematical inputs.
- G4 (structural): domain of validity = finite-physical regime; quantum-gravity scale parked as RP5 long-term capstone; far-from-equilibrium named as Paper 25 H4 boundary.
- G5: GR structure not consumed — derived from A1 + algebraic data.
- G6 (structural): edge cases named — quantum-gravity (RP5), far-from-equilibrium (Paper 25 H4), non-Lorentzian structure (out of scope).

All six close in their appropriate form. RP1 instantiates the structural-codomain reading of the export theorem.

## Schema extension implication

The codomain-transport schema (`apf/codomain_transport_schema.py`, banked at v9.6) currently encodes route status without distinguishing numerical from structural codomains. The structural extension implies a schema-level addition:

- New per-route field: `codomain_type ∈ {numerical, structural}`
- The gate-pattern check runs the appropriate G4 / G6 interpretation per route based on this field.
- Existing routes are typed: mass routes + RP3 + RP6 = numerical; RP1 = structural; RP-CT.H0 = numerical (Paper 6 §11.4 quotes a numerical falsifier).

This is a focused schema-extension task — bank-side modification with one new field, no new module, EXPECTED bumps by one new check (`check_T_codomain_type_declared`).

## Files

- `paper/structural_extension_v35_1.tex` — paper-section content suitable for absorption into a Paper 32-class supplement adjacent to the v35 export-theorem section.
- `scripts/check_structural_extension_v35_1.py` — verifier for the worked-example RP1 walk; passes if RP1's six gates close in the appropriate structural-form interpretation.
- `reports/structural_extension_v35_1_data.json` — machine-readable gate-walk record for RP1 + the existing six mass routes from v22-v35.

## Status

`P_structural_codomain_extension_pass`. The extension is empirically validated by the RP1/RP3/RP6 walk done 2026-05-10 LATEST-17 in chat (nine-for-nine across all articulated routes). Deductive uniqueness (no other status patterns possible) remains open as a separate theorem program.

## Not claimed

- This package does NOT modify the live bank or `apf/codomain_transport_schema.py`. Schema modification is queued as a follow-on Tier-1 task.
- Sufficiency of G1–G6 (no-G7-exists) remains open from v35.
- The route-status determination uniqueness lemma remains conjectural pending deductive proof.
