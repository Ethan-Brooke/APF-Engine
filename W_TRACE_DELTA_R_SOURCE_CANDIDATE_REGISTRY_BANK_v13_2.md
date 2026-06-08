# W_TRACE Standard Delta_r Source-Candidate Registry Bank v13.2

## Status

`[P_w_delta_r_source_candidate_registry]`

This bank moves the W_TRACE physics phase from an abstract standard-Delta-r source mapping into a concrete source-candidate registry.  It does **not** admit source rows.  It records which sources should be acquired, what they may supply, and which checks must pass before payload admission.

## Candidate source classes

1. `ACFW_precision_MW_parametrization` — first-priority precision Standard Model W-mass / Delta-r parametrization candidate.  Candidate payload type: `standard_delta_r_parametrization` or `standard_delta_r_total`.
2. `Denner_on_shell_renormalization_structure` — on-shell electroweak renormalization and finite counterterm structure candidate.  Candidate payload type: `standard_delta_r_decomposition`.
3. `Sirlin_Delta_r_lineage` — definition-lineage source for the on-shell Delta-r relation.
4. `PDG_EW_review_summary` — constants and electroweak review cross-check source.
5. `NIST_CODATA_alpha_reference` — alpha input source.
6. `MuLan_GF_reference` — Fermi-constant input source.

## Guardrails

The registry remains candidate-only.  It forbids observed-W input, APF-anchor fitting, post-hoc residual fitting, and manual export requests.  The APF target

`Delta_r_APF_TRACE_target = 0.0364075266128216881`

is retained only as a downstream comparison target after independent source admission.

## Stop rule

Do not admit any literature candidate as a payload until extraction provenance, forbidden-input audit, and payload-kind mapping are complete.
