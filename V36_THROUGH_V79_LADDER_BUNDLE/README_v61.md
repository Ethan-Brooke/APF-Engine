# APF v61 — Top MSR Coefficient Ingestion and Four-Loop Audit

Stamp: `TOP_MSR_COEFFICIENT_INGESTION_AND_4LOOP_AUDIT_PASS`

v61 ingests sourced MSR-to-pole coefficients through four-loop order and runs a coefficient-ingested evaluator.

## Main result

- alpha_s(R*) = `0.119084611158869`
- terms = `[4.339316649273, 1.016095141009, 0.343387582223, 0.148749217342]` GeV
- m_t^pole,4loop witness = `174.016604383647` GeV
- residual vs audit-only 172.56 GeV = `1.456604383647` GeV
- conservative envelope = `0.449435570715` GeV
- residual/envelope = `3.240963729972`

## Status

Closed:
- coefficient ingestion through c4
- executable four-loop pole witness evaluator
- no-smuggling audit

Not closed:
- physical-final top mass
- exact pole mass
- MC equality
- stable agreement under full QCD conversion

Conclusion: the full coefficient-ingested pole route does **not** finish the top branch. It sharpens the boundary: the LO agreement is not stable under sourced higher-order QCD coefficients.
