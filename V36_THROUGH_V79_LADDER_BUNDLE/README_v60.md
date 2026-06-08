# APF v60 — Top MSR Multiloop Numeric Evaluator Implementation

Status: `P_LO_numeric_evaluator_closed_fail_closed_multiloop_boundary`.

This package implements a runnable top MSR numeric evaluator. It evaluates the LO route and refuses L>=2 unless explicit sourced coefficients are supplied.

- LO pole witness: 172.506466595364 GeV
- Residual vs audit-only PDG direct top average: -0.053533404636 GeV
- Full multi-loop top final: not claimed

Run:

```bash
python scripts/check_top_msr_multiloop_numeric_evaluator_v60.py
```
