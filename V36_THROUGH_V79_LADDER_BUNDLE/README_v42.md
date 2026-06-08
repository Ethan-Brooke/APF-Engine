# APF v42 — Charged-Lepton QED Residual Transport Witness

This package extends v41 with a QED/pole residual-shape witness.

Stamp: `CHARGED_LEPTON_QED_RESIDUAL_SHAPE_WITNESS_PASS`

New object:

```text
Z_l^wit = exp((1/28) H1 + (3/584) H2)
H1 = diag(-1,0,1)
H2 = diag(1,-2,1)
```

The witness gives:

```text
(e, mu, tau) = (0.510901716931, 105.637377342972, 1776.565905410953) MeV
```

Residuals against the supplied pole references are nearly common:

```text
(-0.019028%, -0.019874%, -0.020490%)
```

Not claimed: final charged-lepton physical masses, QED running closure, scalar normalization closure, or a proof that `28` and `584` are forced denominators rather than APF-count witnesses.

Run:

```bash
python scripts/check_charged_lepton_qed_residual_witness_v42.py
```
