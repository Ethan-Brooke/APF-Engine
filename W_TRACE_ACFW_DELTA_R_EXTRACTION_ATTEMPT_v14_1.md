# W_TRACE ACFW Standard Delta_r Extraction Attempt — v14.1

This sprint is the first real physics-source extraction after the v14.0 source-acquisition pivot.

## Result

`W_TRACE_ACFW_DELTA_R_EXTRACTION_ATTEMPT_BANK_PASS`

## Source path

The module encodes the Awramik--Czakon--Freitas--Weiglein Standard Model W-mass parametrization as an independent source path and inverts the on-shell relation

```math
M_W^2\left(1-M_W^2/M_Z^2ight)=rac{\pilpha}{\sqrt{2}G_F}rac{1}{1-\Delta r}
```

to obtain a standard total `Delta_r_source` candidate.

## Extracted candidate

For the declared non-W input scenario in `apf/w_trace_acfw_delta_r_extraction_attempt.py`:

```text
M_W_source_GeV          = 80.358678992326
Delta_r_source_total    = 0.036614529324049294
Delta_r_APF_TRACE_target = 0.036407526612821688
Delta_r_source_minus_APF = +0.000207002711227609
abs_M_W_gap_MeV          = 3.485342
```

## Verdict

We got there in the limited but important sense: a real standard-electroweak total-Delta-r payload candidate is now extracted and compared.

This is **not** a physical W export, not a component-sum certificate, and not a covariance/uncertainty closure.

## Guardrails

Forbidden as source inputs:

```text
observed_M_W
M_W_world_average
CDF_II_M_W
PDG_observed_M_W
Delta_r_target_backsolve
fit_to_M_W_TRACE
APF anchor as input/component
physical export request
```

## Next physics step

Stress-test input conventions and source a second independent standard-W prediction / Delta-r source path.
