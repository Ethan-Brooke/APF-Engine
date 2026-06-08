# W_TRACE External Source Adapter Bank v1.0

Status: `[P_w_external_source_adapter]`

This bank layer defines the import contract for future independently sourced W finite-part component rows. It extends the v9.9 source-pack gate with external table/library export metadata: external pack URI, SHA-256 pack digest, adapter version, ingest format, and extraction-log digest.

Closed here:

- external finite-part source-pack adapter/import contract;
- supported formats: `json_rows_v1`, `csv_with_header_v1`, `python_mapping_rows_v1`;
- full eight-component coverage and symbol matching;
- anti-backsolve, anti-APF-anchor, anti-observed-W, and anti-residual-fit guards;
- preservation of the physical-export lock.

Still open:

- actual external numerical finite-part payload rows;
- component-sum certificate;
- covariance/uncertainty propagation;
- physical W/on-shell transport.

The module intentionally ships with an empty default adapter table. Shape-test rows exist only to verify the contract and are not data.
