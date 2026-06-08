# APF v50 — Charm Trace-to-MSbar Normalization Transport

Run:

```bash
python scripts/check_charm_trace_to_msbar_normalization_transport_v50.py
```

Expected stamp:

```text
CHARM_TRACE_TO_MSBAR_NORMALIZATION_TRANSPORT_PASS
```

This package promotes charm from `P_MSbar_knockout` to `P_export_candidate_MSBAR_self_scale_v50` by deriving

```text
kappa_c = sqrt(7/2)
```

from APF counts only. The external PDG ledger is used only after route construction for audit.

It does **not** claim `P_physical_final`, zero residual, a pole mass, or full QCD covariance finalization.
