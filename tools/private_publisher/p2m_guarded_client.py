"""Maintained successor to the P2M JSON and multipart publishing transports.

All content mutations enter GuardedPrivatePublisher on every call. GET and the
fixed token-refresh endpoint remain separate. Legacy frozen runners are evidence,
not an alternate entry point for new releases. No credentials are read on import.
"""
from __future__ import annotations

import json
import copy
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from apf.evidence_gate import GateRejected, canonical_bytes, validate_request
from apf.private_publisher import GuardedPrivatePublisher

BASE = "https://prove2.me/api/v1"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    """An approved route cannot redirect a write or bearer token elsewhere."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def build_verify_payload(theorem_id, proof_bytes, explanation, *, boundary):
    """Build once BEFORE review; freeze the returned bytes and media type."""
    if type(proof_bytes) is not bytes:
        raise ValueError("immutable proof bytes required")
    if not isinstance(boundary, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,70}", boundary):
        raise ValueError("invalid multipart boundary")
    values = {"theorem_id": theorem_id, "proof_type": "prove", "explanation": explanation}
    if not all(isinstance(v, str) for v in values.values()):
        raise ValueError("multipart fields must be strings")
    marker = b"--" + boundary.encode("ascii")
    if any(marker in v.encode("utf-8") for v in values.values()) or marker in proof_bytes:
        raise ValueError("multipart boundary collides with content")
    chunks = []
    for name, value in values.items():
        chunks.append((f'--{boundary}\r\nContent-Disposition: form-data; name="{name}"\r\n\r\n{value}\r\n').encode("utf-8"))
    chunks.append((f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="solution.lean"\r\nContent-Type: application/octet-stream\r\n\r\n').encode("ascii"))
    chunks.extend((proof_bytes, f"\r\n--{boundary}--\r\n".encode("ascii")))
    return b"".join(chunks), "multipart/form-data; boundary=" + boundary


class P2MClient:
    def __init__(self, authorization_pin, publisher_id, *, opener=None, clock=None,
                 before_mutation=None):
        self._token = None
        self._opener = opener if opener is not None else urllib.request.build_opener(NoRedirect())
        self._before_mutation = before_mutation
        self._authority = copy.deepcopy(authorization_pin)
        self._publisher_id = publisher_id
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def connect(self, credentials_path):
        """Explicit fixed-endpoint refresh; this does not authorize any write."""
        credentials = json.loads(Path(credentials_path).read_text(encoding="utf-8-sig"))
        raw = canonical_bytes({"api_key": credentials["api_key"]})
        result = self._http("POST", "/agent/refresh", raw, "application/json", authenticated=False)
        if result.get("version") != "0.10.3":
            raise RuntimeError("P2M API version changed; refresh the platform contract")
        token = result.get("access_token")
        if not isinstance(token, str) or not token:
            raise RuntimeError("P2M refresh did not return an access token")
        self._token = token
        return result["version"]

    def _http(self, method, path, payload, content_type, *, authenticated=True, before_open=None):
        if not isinstance(path, str) or not path.startswith("/") or path.startswith("//"):
            raise ValueError("relative P2M API path required")
        if any(ch in path for ch in ("\\", "\r", "\n", "#")):
            raise ValueError("invalid P2M API path")
        headers = {"Content-Type": content_type}
        if authenticated and self._token:
            headers["Authorization"] = "Bearer " + self._token
        request = urllib.request.Request(BASE + path, data=payload, headers=headers, method=method)
        # Exactly one open. No retry or redirect. Exceptions propagate to the
        # caller for read-only reconciliation; never retry an uncertain write.
        if before_open is not None:
            before_open()
        with self._opener.open(request, timeout=30) as response:
            return json.load(response)

    def _mutation_transport(self, method, path, payload, content_type, *, final_validation):
        if self._before_mutation is not None:
            self._before_mutation(method, path, payload, content_type)
        # The final gate runs AFTER journal I/O and Request construction, directly
        # before opener.open. The callback cannot leave a cached permit behind.
        return self._http(method, path, payload, content_type, before_open=final_validation)

    def send_reviewed(self, method, path, payload, content_type, *, action="private_stage"):
        """Exact scientific action and bytes are checked again at actual send."""
        def final_check():
            decision = validate_request(
                self._authority, publisher_id=self._publisher_id, action=action,
                method=method, path=path, payload=payload, content_type=content_type,
                now=self._clock())
            if self._clock() >= decision.expires_at:
                raise GateRejected("release_expired_before_network_send")
        def transport(m, p, b, c):
            return self._mutation_transport(m, p, b, c, final_validation=final_check)
        publisher = GuardedPrivatePublisher(
            self._authority, self._publisher_id, transport, clock=self._clock)
        return publisher.mutate(action=action, method=method, path=path,
                                payload=payload, content_type=content_type)

    def call(self, method, path, body=None, *, action="private_stage"):
        """Successor to the legacy call branch; all non-GET calls are guarded."""
        if method == "GET":
            if body is not None:
                raise ValueError("GET must not carry a mutation body")
            return self._http("GET", path, None, "application/json")
        return self.send_reviewed(method, path, canonical_bytes(body),
                                  "application/json", action=action)

    def multipart(self, payload, content_type, *, action="private_stage"):
        """Successor to the separate /verify branch; no post-review rebuilding."""
        return self.send_reviewed("POST", "/verify", payload, content_type, action=action)


class AdministrativeP2MClient(P2MClient):
    """Separate description-only lane; scientific calls retain the original gate."""
    def __init__(self, authorization_pin, publisher_id, *, opener=None, clock=None,
                 before_mutation=None):
        super().__init__(authorization_pin, publisher_id, opener=opener, clock=clock,
                         before_mutation=before_mutation)
        from apf.administrative_publisher import GuardedAdministrativePublisher
        self._admin_authority = copy.deepcopy(authorization_pin)
        self._admin_publisher_id = publisher_id
        self._admin_clock = clock or (lambda: datetime.now(timezone.utc))
        self._admin_publisher = GuardedAdministrativePublisher(
            authorization_pin, publisher_id, self._administrative_transport, clock=clock)

    def _read_current_mission(self, mission_id):
        # P2M serves full mission descriptions on list pages; single-id GET is 405.
        for offset in range(0, 10000, 100):
            page = self.call("GET", f"/missions?limit=100&offset={offset}")
            rows = page["missions"]
            if not isinstance(rows, list):
                raise GateRejected("invalid_live_mission_readback")
            matches = [m for m in rows if m.get("id") == mission_id]
            if len(matches) > 1:
                raise GateRejected("ambiguous_live_mission_identity")
            if matches:
                return matches[0]
            if len(rows) < 100:
                break
        raise GateRejected("live_mission_not_found")

    def _administrative_transport(self, method, path, payload, content_type):
        from apf.administrative_publisher import (
            validate_administrative_request, administrative_baseline_digest)
        mission_id = path.removeprefix("/missions/")
        live = self._read_current_mission(mission_id)
        if live.get("id") != mission_id or live.get("visibility") != "private" or not isinstance(live.get("description"), str):
            raise GateRejected("live_mission_identity_or_privacy_mismatch")
        observed = administrative_baseline_digest(mission_id, live["description"], True)
        def final_check():
            # After both GET and journal I/O, directly before opener.open.
            decision = validate_administrative_request(
                self._admin_authority, publisher_id=self._admin_publisher_id,
                action="administrative_update", method=method, path=path, payload=payload,
                content_type=content_type, now=self._admin_clock())
            if observed != decision.required_baseline_sha256:
                raise GateRejected("live_mission_baseline_mismatch")
            if self._admin_clock() >= decision.expires_at:
                raise GateRejected("administrative_release_expired_before_mutation")
        return self._mutation_transport(method, path, payload, content_type,
                                        final_validation=final_check)

    def send_administrative(self, method, path, payload, content_type, *, action="administrative_update"):
        return self._admin_publisher.mutate(action=action, method=method, path=path,
                                           payload=payload, content_type=content_type)
