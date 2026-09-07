# W_TRACE Release Attestation / Immutable Manifest Digest Bank v1.0

Status: `[P_w_release_attestation_manifest_digest]`.

This bank adds the signed-attestation and immutable-manifest-digest contract above the v12.3 release packet validator. It does not ship a real signature, does not validate a real release packet, and does not enable physical W export.

The attestation contract requires a SHA-256 release-packet digest, a SHA-256 immutable-manifest digest, signer identity, supported signature scheme, signature payload digest, signature reference/bundle, timestamp, release-packet validator version, runbook version, and explicit export-lock acknowledgement.

The immutable manifest binds the terminal artifacts: release packet, review packet, source candidate, payload, session log, session replay, row bundle, component-sum certificate, covariance certificate, uncertainty certificate, counterterm convention, and final export readiness digest.

Template/default packets are rejected. Any occurrence of observed physical W mass, world-average W mass, residual-fit fields, APF-anchor Delta_r consumption, manual unlock, force export, or physical-M_W override is rejected.

The shipped state remains locked: physical W export remains locked until real finite-part rows, component-sum certification, covariance, uncertainty propagation, release packet validation, immutable manifest binding, and real signature verification are all supplied in the proper order.
