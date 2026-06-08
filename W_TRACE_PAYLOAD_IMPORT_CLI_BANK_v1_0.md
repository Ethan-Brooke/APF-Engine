# W_TRACE Payload Import CLI / Fixture-File Loader Bank v1.0

Status: `P_w_payload_import_cli_loader`

This layer adds a concrete command-line/file-loader interface for W_TRACE finite-part candidate payloads. It supports JSON and CSV payload files routed through the existing external ingestion, candidate-attempt, row-bundle, and final-readiness gates.

The shipped state contains no real finite-part numerical payload file. Synthetic fixtures are useful for parser and file-loader verification only; they cannot certify component sums or unlock physical W export.

Master verifier:

```text
scripts/check_w_trace_payload_import_cli.py
W_TRACE_PAYLOAD_IMPORT_CLI_BANK_PASS
```

Closed here:

```text
W_TRACE payload import CLI / fixture-file loader: [P_w_payload_import_cli_loader]
```

Still open:

```text
real reviewed external finite-part payload rows
real component-sum certificate
real covariance / uncertainty propagation
physical W/on-shell export
```
