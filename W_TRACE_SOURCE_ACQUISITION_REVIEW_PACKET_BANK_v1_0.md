# W_TRACE Source-Acquisition Review Packet Bank v1.0

Status: `[P_w_source_acquisition_review_packet]`.

This bank layer sits above the v11.5 source-candidate registry and below any real W finite-part payload import. It supplies the concrete acquisition worksheet and review packet required before a source candidate may be promoted into an import attempt.

No real external source is acquired in this release. No real finite-part rows are imported or admitted. No component-sum, covariance, or uncertainty certificate is issued. Physical W export remains locked.

The review packet must document source identity, source class, component coverage, scheme/gauge/counterterm alignment, extraction method, digest plan, license/access notes, review attestation, and a forbidden-input audit.

Forbidden inputs include observed M_W, W world averages, residual fits, APF-anchor Delta r targets, post-hoc counterterm fits, and physical export requests. The APF-anchor target may only be used downstream as a comparison target after independent components have been admitted.

The shipped templates are worksheet scaffolds only. They are not evidence, not source payloads, and not reviewed finite-part data.

For audit-string compatibility: physical W export remains locked.
