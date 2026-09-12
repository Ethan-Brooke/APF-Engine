"""Prospective publisher boundary. No credentials, network calls or legacy edits.

A future publisher supplies its transport (JSON or already-built multipart bytes).
Every write must use mutate; calling that transport directly bypasses this gate.
"""
from __future__ import annotations

import copy
from datetime import datetime, timezone
from .evidence_gate import GateRejected, validate_request


class GuardedPrivatePublisher:
    def __init__(self, authorization_pin, publisher_id, mutation_callback, *, clock=None):
        self._authorization_pin = copy.deepcopy(authorization_pin)
        self._publisher_id = publisher_id
        self._mutation_callback = mutation_callback
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def mutate(self, *, action, method, path, payload, content_type):
        """Reject before callback. Exact immutable request is passed to transport.

        No cached permit: files and expiry are rechecked on every invocation.
        A transport exception propagates; this boundary never retries a write.
        """
        decision = validate_request(
            self._authorization_pin, publisher_id=self._publisher_id, action=action,
            method=method, path=path, payload=payload, content_type=content_type,
            now=self._clock(),
        )
        if self._clock() >= decision.expires_at:
            raise GateRejected("release_expired_before_mutation")
        return self._mutation_callback(method, path, payload, content_type)
