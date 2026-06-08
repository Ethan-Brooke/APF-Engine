# W_TRACE standard Delta-r extraction worksheet v15.1

Status: `P_w_standard_delta_r_extraction_worksheet`

Verifier: `W_TRACE_STANDARD_DELTA_R_EXTRACTION_WORKSHEET_PASS`

Checks: `16/16 PASS`

## Closed in this phase

The ACFW standard electroweak W-mass parametrization path is now represented as a reproducible standard-total `Delta_r` worksheet/payload. It evaluates a declared non-W input vector, obtains the independent source prediction, and inverts the on-shell `G_F-M_W-M_Z-Delta_r` relation.

Numerical source-total result:

```text
M_W^source = 80.358678992326 GeV
Delta_r^source,total = 0.036614529324049294
Delta_r^source,total - Delta_r^APF_TRACE = 0.000207002711227609
|M_W^source - M_W^APF_TRACE| = 3.485342 MeV
```

## Still blocked

This is a standard-total Delta-r payload, not an APF eight-slot finite-part component-row bundle. It therefore cannot certify physical W export. The route remains blocked by:

```text
SOURCE_TOTAL_HAS_NO_APF_EIGHT_SLOT_COMPONENT_DECOMPOSITION
NO_REAL_FINITE_PART_COMPONENT_ROWS_ADMITTED
NO_COMPONENT_SUM_CERTIFICATE
NO_COVARIANCE_CERTIFICATE
NO_DELTA_R_TO_MW_UNCERTAINTY_PROPAGATION_CERTIFICATE
PHYSICAL_W_EXPORT_LOCK_REMAINS_CLOSED
```

## Claim boundary

Closed: source-total worksheet for comparison.
Open: physical W/on-shell export.
