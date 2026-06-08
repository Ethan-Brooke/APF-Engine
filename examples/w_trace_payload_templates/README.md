# W_TRACE finite-part payload templates

These files are **shape-only parser fixtures** for the W_TRACE external finite-part payload pipeline.

They are not reviewed external finite-part data, not physical evidence, and must not be used to unlock physical W/on-shell export.

Allowed uses:

- verify JSON/CSV parser shape;
- demonstrate the `apf.w_trace_payload_import_cli` loader path;
- provide a copy-editable template for future independently sourced finite-part rows.

Forbidden uses:

- consuming observed `M_W`, W world averages, W residuals, or the APF-anchor `Delta r` target;
- treating template rows as real finite-part values;
- enabling physical W export.
