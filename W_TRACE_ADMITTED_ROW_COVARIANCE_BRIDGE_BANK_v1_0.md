# W_TRACE Admitted-Row Covariance Bridge Bank v1.0

Status: `[P_w_admitted_row_covariance_bridge]`

This bank layer connects the real row-bundle admission state to the covariance /
uncertainty propagation harness.  It does not admit real finite-part values and
it does not export a physical W mass.

Closed here:

- admitted row bundle -> covariance-record construction contract
- row uncertainty -> diagonal covariance adapter
- exact component-order preservation over the eight finite-part components
- bridge to the v10.5 uncertainty propagation harness
- anti-smuggling guards for observed W inputs, APF-anchor target inputs,
  residual-fit inputs, and physical-export requests
- proof that EMPTY/REJECTED bundles cannot certify covariance

Still open:

- real finite-part row payloads
- real covariance payload / full covariance matrix
- real numerical component-sum certificate
- real uncertainty propagation from admitted data
- physical W/on-shell export

The shipped default state remains:

```text
real_row_bundle_supplied = False
real_row_bundle_admitted = False
row_bundle_covariance_bridged = False
covariance_certified = False
uncertainty_propagation_certified = False
physical_W_export_enabled = False
exports_physical_M_W = False
```
