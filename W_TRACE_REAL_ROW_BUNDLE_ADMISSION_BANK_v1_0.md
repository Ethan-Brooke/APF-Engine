# W_TRACE Real Row-Bundle Admission Bank v1.0

Status: `[P_w_real_row_bundle_admission]`

This bank adds the bundle-level gate after the v10.8 row schema adapter.  It
accepts a candidate collection of W finite-part rows, runs them through the row
schema, and emits one of three certificates:

- `EMPTY`: no real rows supplied in the shipped bank state;
- `REJECTED`: rows or metadata fail admission;
- `ADMITTED`: all row-schema and bundle metadata gates pass.

The shipped repository remains intentionally empty: no real external finite-part
rows are admitted, no component-sum certificate is issued, no covariance or
uncertainty certificate is issued, and physical W export remains locked.

The APF-anchor Delta_r target and observed/averaged physical W values are
comparison/export-side data only and are forbidden as row or bundle inputs.
