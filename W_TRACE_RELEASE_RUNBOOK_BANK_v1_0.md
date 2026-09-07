# W_TRACE Release Runbook Bank v1.0

Status: `[P_w_release_runbook]`.

This is an operator runbook and release checklist for the reviewed W_TRACE payload pipeline. It sits above the v12.1 end-to-end import pipeline manifest and tells a future operator which artifacts must exist before the reviewed W finite-part payload path can be considered release-ready.

This document and its examples are **template only**. They are not real finite-part evidence, do not contain reviewed numerical rows, and do not unlock physical W export.

The physical W/on-shell export remains OPEN until real reviewed external finite-part rows, component-sum certification, covariance certification, uncertainty propagation, counterterm convention review, and no-target-observable-consumption certification are all supplied and checked together.

## Required artifact classes

- completed review packet JSON
- review packet digest
- source candidate digest
- payload file URI
- payload SHA-256 digest
- extraction log digest
- import session log JSON
- replay report JSON
- row-bundle admission report JSON
- component-sum certificate JSON
- covariance certificate JSON
- uncertainty propagation certificate JSON
- final export readiness report JSON

## Operator runbook sequence

1. Collect artifacts.
2. Compute and record digests.
3. Run the review-packet validator.
4. Run the reviewed-source handoff.
5. Run the payload import CLI.
6. Write the import session log.
7. Replay the import session.
8. Run row-bundle admission.
9. Run component-sum certification.
10. Run covariance certification.
11. Run uncertainty propagation.
12. Run final export readiness.

Forbidden inputs remain observed `M_W`, W world averages, residual-fit columns, APF-anchor target used as a component input, and manual export override requests.
