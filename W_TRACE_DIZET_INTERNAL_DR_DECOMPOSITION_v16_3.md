# W_TRACE DIZET Internal Delta-r Decomposition v16.3

Status: `P_w_trace_dizet_internal_dr_decomposition`.

The locally compiled DIZET v6.45 `SEARCH`/`NEWDR` path was instrumented at the APF same-input deck. The run exposes implementation-local variables for `DR`, `DRBIG`, `DRREM`, `DR1FER`, `DR1BOS`, running-alpha terms, QCD terms, rho/top locators, and `NEWDR` remainder pieces. The exported DIZET total evaluator remains closed; the new gate closed is an internal reviewed-code decomposition snapshot.

Boundary: these variables are not admitted APF finite-part component rows with covariance. Physical W export remains blocked.
