# v42 charged-lepton QED residual transport witness

Status: `CHARGED_LEPTON_QED_RESIDUAL_SHAPE_WITNESS_PASS`.

v42 keeps v41's pole-LO export candidate and adds a determinant-preserving APF-count residual-shape witness:

`Z_l^wit = exp((1/28) H1 + (3/584) H2)`

with `H1=diag(-1,0,1)` and `H2=diag(1,-2,1)`.

Predicted witness vector:

- e: `0.510901716931` MeV
- mu: `105.637377342972` MeV
- tau: `1776.565905410953` MeV

Diagnostic residuals versus supplied pole references:

- e: `-0.019028%`
- mu: `-0.019874%`
- tau: `-0.020490%`

This collapses the generation-dependent residual to an approximately common scalar offset near `2e-4`. It does **not** claim final physical charged-lepton masses, QED running closure, a closed scalar eta0, or a forced-denominator proof for 28 and 584.

Next theorem: `APF_QED_SCALAR_NORMALIZATION_AND_COUNT_SOURCE_THEOREM`.
