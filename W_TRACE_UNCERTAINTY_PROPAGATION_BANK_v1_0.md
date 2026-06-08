# W_TRACE Uncertainty Propagation Harness Bank v1.0

Status: `[P_w_uncertainty_propagation_harness]`

This layer follows the v10.4 component-sum certificate harness. It banks the covariance and uncertainty-propagation contract for the W_TRACE -> on-shell route without admitting real finite-part rows or exporting a physical W value.

Closed now:

- exact covariance record schema over the eight finite-part components;
- component-order and symbol preservation;
- symmetry and non-negative diagonal requirements;
- `sigma_Delta_r = sqrt(1^T Cov 1)` push-forward mechanics;
- symbolic W uncertainty push-forward contract through `dM_W/dDelta_r`;
- explicit rejection of observed-W, APF-anchor, W-residual, and physical-export inputs.

Still open:

- real covariance payload from an admitted external source pack;
- certified component sum from real finite-part rows;
- numerical W uncertainty;
- physical W/on-shell export.

Master result: `W_TRACE_UNCERTAINTY_PROPAGATION_BANK_PASS`.
