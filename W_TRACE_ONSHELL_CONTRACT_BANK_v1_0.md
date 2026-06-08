# W_TRACE On-Shell Contract Bank v1.0

Status: `P_w_trace_contract`

This push is the first concrete route-specific layer after the v8.9 terminal
completion gate.  It selects the least-burden route named by v8.9:

```text
w_trace_on_shell_route
```

## Closed here

- The W_TRACE route is selected from the v8.9 recommended completion order.
- The W on-shell target-contract template is banked.
- Required EW input-basis slots are enumerated.
- Required finite radiative/counterterm conversion slots are enumerated.
- Required uncertainty/provenance slots are enumerated.
- Observed physical `M_W`, target residuals, and identity transport are forbidden as inputs.
- The v8.9 physical-export gate remains locked.

## Not closed here

- No EW external constants are evaluated.
- No radiative correction or finite-part map is evaluated.
- No uncertainty propagation is evaluated.
- No physical `M_W` prediction is exported.

## Targeted verifier

```bash
python scripts/check_w_trace_onshell_transport.py
```

Expected result:

```text
W_TRACE_ONSHELL_CONTRACT_BANK_PASS
```

## Claim discipline

Correct claim:

```text
W_TRACE -> on-shell route contract: [P_w_trace_contract]
```

Incorrect claim:

```text
M_W physical/on-shell transport closed
```
