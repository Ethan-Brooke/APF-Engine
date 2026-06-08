# W_TRACE Finite-Part Evaluator Gate Bank v1.0

Status: `[P_w_finite_part_evaluator_gate]`.

This bank layer follows the v9.4 finite-part ledger.  It does **not** evaluate
loop or counterterm finite parts.  It banks the independent evaluator and
component-sum certificate gate required before the W_TRACE on-shell route can
export a physical W comparison.

Closed here:

- every v9.4 finite-part component receives an independent source requirement;
- the APF-anchor Delta_r target is allowed only as a post-evaluation comparison
  target, not as an input to any component;
- observed physical `M_W`, W residuals, residual-fitted `Delta_r`, and tuned
  counterterms remain forbidden inputs;
- the component-sum predicate is executable and refuses certification when
  independent component values are absent;
- the physical-export gate remains locked.

Still open:

- independent finite-part numerical values;
- finite on-shell counterterm convention;
- component-sum certificate against the APF-anchor Delta_r target;
- covariance and uncertainty propagation;
- physical W/on-shell export.

Master verifier:

```bash
python scripts/check_w_trace_finite_part_evaluator_gate.py
```

Expected result:

```text
W_TRACE_FINITE_PART_EVALUATOR_GATE_BANK_PASS
```
