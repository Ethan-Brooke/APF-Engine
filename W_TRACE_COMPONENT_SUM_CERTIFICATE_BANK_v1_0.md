# W_TRACE Component-Sum Certificate Harness Bank v1.0

Status: `[P_w_component_sum_certificate_harness]`

This bank layer defines the certificate harness for comparing admitted independent
W finite-part component rows against the APF/W_TRACE anchor-implied
`Delta r` target. It closes the schema, decimal summation, tolerance,
covariance/uncertainty prerequisites, and anti-smuggling guards.

It does **not** ship admitted real external finite-part rows and does **not**
export a physical W mass.

Closed here:

- exact component order and symbol matching for the eight finite-part slots;
- decimal component summation contract;
- absolute-tolerance comparison contract against the APF/W_TRACE anchor target;
- covariance and uncertainty prerequisites for certification;
- explicit rejection of observed-W, APF-anchor-as-input, residual-fit, and
  physical-export inputs.

Still open:

- admitted real external finite-part rows;
- certified component sum;
- covariance/uncertainty propagation;
- physical W/on-shell export.
