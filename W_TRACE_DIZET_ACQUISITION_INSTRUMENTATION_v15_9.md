# W_TRACE DIZET/ZFITTER Acquisition and Instrumentation Sprint v15.9

This bank layer identifies DIZET v6.45 / ZFITTER as the concrete external acquisition path for the W on-shell route.

Closed:

- DIZET v6.45 acquisition channels located.
- DIZET default flag set captured.
- APF same-input route deck specified.
- Instrumentation and covariance protocol specified.
- Old monolithic evaluator blocker split into total-evaluator and row/covariance gates.

Not closed:

- DIZET source is not vendored in this repository.
- DIZET has not been compiled or run here.
- No DIZET output table is imported.
- Physical W export remains locked.

Targeted verifier: `W_TRACE_DIZET_ACQUISITION_INSTRUMENTATION_PASS`.
