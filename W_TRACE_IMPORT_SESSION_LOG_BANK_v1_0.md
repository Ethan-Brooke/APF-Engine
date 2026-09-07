# W_TRACE Import Session Log Bank v1.0

Status: `[P_w_import_session_log]`.

This bank layer records a reviewed payload import session audit trail above the reviewed-source import handoff gate. It is an audit-log contract, not an evidence payload.

No real finite-part rows are shipped in this module. The shipped state records no real external rows imported, no rows admitted, no component-sum certificate, no covariance certificate, no uncertainty propagation certificate, and physical W export remains OPEN.

The APF/W_TRACE anchor and observed physical W values are forbidden as import-session inputs. Session logs may record payload digests, review-packet digests, source-candidate digests, extraction-log digests, loader status, failure reasons, and export-lock state.

Required lock invariant:

```text
real_external_rows_imported = False
real_external_rows_admitted = False
component_sum_certified = False
covariance_certified = False
uncertainty_propagation_certified = False
physical_W_export_enabled = False
exports_physical_M_W = False
```
