# W_TRACE Release Packet Validator Bank v1.0

Status: `P_w_release_packet_validator`

This bank layer validates a completed W_TRACE release packet before it can be
used as an operator checklist preflight artifact. It sits above the v12.2
release runbook and below any future real finite-part row admission.

The release packet validator rejects template/default packets, missing reviewers, missing
artifacts, missing or malformed SHA-256 digests, missing release-predicate
attestations, missing operator-action attestations, forbidden W-target tokens,
and manual export override attempts.

The physical W/on-shell export remains OPEN. This module does not ship real
finite-part evidence, admit real payload rows, certify a component sum, certify
covariance, certify uncertainty propagation, or export a physical W mass.

## Locked shipped state

```text
real_completed_release_packet_shipped = False
real_completed_release_packet_validated = False
real_payload_rows_admitted = False
real_component_sum_certified = False
real_covariance_certified = False
real_uncertainty_certified = False
physical_W_export_enabled = False
exports_physical_M_W = False
```

## Template/default packets

The template packet is for operator structure only. It is not real finite-part
evidence and must not be promoted to a real release packet.
