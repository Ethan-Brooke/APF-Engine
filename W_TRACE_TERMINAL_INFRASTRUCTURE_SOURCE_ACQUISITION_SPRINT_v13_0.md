# W_TRACE Terminal Infrastructure + Source Acquisition Sprint v13.0

Status: `P_w_v13_terminal_infrastructure_sprint`

This sprint deliberately replaces micro-gate cadence with a consolidated push.  It closes the remaining W_TRACE release-infrastructure scaffolding in one bundle and declares the stop condition for further W-route scaffolding.

## Closed in this sprint

- detached-signature verification adapter contract
- signed release replay contract
- terminal release evidence bundle
- terminal open/closed state report
- next-payload requirements and physics handoff

## Preserved anchors

- `M_W_TRACE_GeV = 80.362164334`
- `Delta r_APF_TRACE_target = 3.64075266128216881e-2`

## Hard stop condition

No further W_TRACE scaffolding should be added before real reviewed finite-part payload rows are supplied, unless this terminal infrastructure reveals a blocker.

## Still open

- real reviewed external finite-part rows
- real component-sum certificate
- real covariance payload
- real uncertainty propagation
- physical W/on-shell export

## Next phase

Turn to physics/source acquisition: identify independent electroweak finite-part sources, map standard on-shell `Delta r` notation into the APF eight-slot row schema, and attempt admission of real rows through the v13.0 pipeline.
