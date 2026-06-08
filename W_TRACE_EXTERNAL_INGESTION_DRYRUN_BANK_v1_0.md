# W_TRACE External Ingestion Dry-Run Bank v1.0

Status: `[P_w_external_ingestion_dryrun]`

This bank layer sits after the v10.0 W_TRACE external source-pack adapter. It exercises parser fixtures for the three declared external input formats:

- `json_rows_v1`
- `csv_with_header_v1`
- `python_mapping_rows_v1`

The fixtures are synthetic shape rows only. They prove that a future external finite-part source pack can be parsed into the v10.0 `ExternalSourceRecord` contract and passed through the adapter admission report without weakening the no-smuggling guards.

Closed here:

- parser contract for JSON rows
- parser contract for CSV rows with exact header
- parser contract for Python mapping rows
- preservation of component order and symbols
- rejection of unsupported format, bad adapter version, bad CSV header
- rejection after parse of missing, duplicate, APF-anchor-consuming, observed-W-consuming, and residual-fit-consuming rows

Still open:

- real external finite-part numerical rows
- component-sum certificate
- covariance / uncertainty propagation
- physical W/on-shell export

The physical-export lock remains active.
