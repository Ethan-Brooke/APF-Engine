# W_TRACE Reviewed-Source Import Handoff Bank v1.0

This banked layer connects the completed source-review packet validator to the
W_TRACE payload import CLI. The closure is only the handoff boundary: a payload
file may be routed to the loader only after a validated review packet preflight.

No real reviewed source is shipped in this release. No real finite-part rows are
imported or admitted. The physical W export remains locked.

## Closed here

- validated review packet -> payload import CLI handoff contract
- template/default packet rejection before loader invocation
- review-attestation propagation only after validation
- JSON/CSV fixture dry-run through the loader
- loader failure propagation into the handoff report
- physical-export request rejection

## Still open

- real reviewed external finite-part rows
- admitted row bundle
- component-sum certificate
- covariance / uncertainty propagation
- physical W/on-shell export

Guardrails include explicit rejection of observed M_W, APF-anchor Delta_r target
consumption, residual-fit paths, and direct physical-W export requests.
