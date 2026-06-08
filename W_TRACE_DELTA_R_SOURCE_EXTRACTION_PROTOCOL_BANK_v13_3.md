# W_TRACE Standard Delta_r Source-Extraction Protocol Bank v13.3

Status: `P_w_delta_r_source_extraction_protocol`

This bank converts the v13.2 standard `Delta_r` source-candidate registry into a concrete extraction worksheet and validator. It is a physics-source acquisition layer, not a physical W export layer.

## Purpose

The protocol requires every standard electroweak `Delta_r` source candidate to document:

- canonical source locator and version/date,
- SHA-256 source/table digest,
- extractor and independent reviewer,
- source payload kind,
- input scheme and reference-policy fields,
- notation mapping from source symbols to the standard APF `Delta_r` source schema,
- extracted-quantity and uncertainty-field inventory,
- observed-W, APF-anchor, and target-fit exclusion attestations.

## Closed

The following is banked:

```text
source-extraction worksheet schema
candidate-to-payload-kind assignment
completed-worksheet preflight validator
template/default rejection
forbidden-token rejection
anti-observed-W and anti-APF-anchor attestations
no-export locked state
```

## Still open

```text
real completed extraction worksheet
real admitted Delta_r source payload
real finite-part / standard Delta_r rows
component-sum certificate
covariance / uncertainty propagation
physical W export
```

## Stop rule

A source candidate may not become an admitted `Delta_r` payload until a non-template completed worksheet passes this protocol and the downstream admission gates remain export-locked.
