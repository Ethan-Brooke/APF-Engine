# W_TRACE Payload Template Pack Bank v1.0

Status: `[P_w_payload_template_pack]`

This module ships safe JSON/CSV example templates for the W_TRACE finite-part payload import CLI. The templates are shape-only parser fixtures. They are not reviewed external finite-part evidence and do not certify the component sum, covariance, uncertainty propagation, or physical W/on-shell export.

Closed by this layer:

- template files are present and digest-addressed;
- JSON and CSV templates parse through the v11.3 loader path;
- component order is preserved;
- template rows consume neither observed `M_W` nor the APF-anchor `Delta r` target;
- export remains locked even when the templates are loaded.

Still open:

- real reviewed external finite-part rows;
- component-sum certificate;
- covariance / uncertainty propagation;
- physical W/on-shell export.
