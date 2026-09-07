# W_TRACE Review Packet Validator Bank v1.0

This bank adds the completed source-review packet validator / import preflight
for the W_TRACE finite-part source-acquisition route.

No real completed packet is shipped.  The default state is template-only and
fails closed.  A synthetic promoted witness proves the validator logic, but it
is not a real external finite-part source and does not import rows.

The validator rejects packets that consume observed M_W, a world-average W mass,
a W residual, an APF-anchor Delta r target, or any post-hoc backsolve token.  The
APF-anchor is comparison-only downstream, not an input to source acquisition.

The physical W export remains locked.  Real finite-part rows, component-sum
certification, covariance/uncertainty propagation, and physical W export remain
open.
