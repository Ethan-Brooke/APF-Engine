"""Exact reviewed append-only private mission administration; no scientific credit.

The mutation callback MUST read live mission state immediately before transport,
compare the reviewed baseline projection, recheck expiry, and send exact bytes.
This local file guard does not itself perform or authenticate that network read.
"""
from __future__ import annotations

import copy
from dataclasses import dataclass
from datetime import datetime, timezone
from uuid import UUID
from .evidence_gate import GateRejected, canonical_bytes, digest, require, _pin, _json, _time

MAX_RELEASE_SECONDS = 3600


def _fields(value, names):
    require(isinstance(value, dict) and set(value) == set(names.split()), "administrative_schema_fields")


def _record(pin, kind, fields):
    outer = _json(_pin(pin))
    _fields(outer, "administrative_gate")
    record = outer["administrative_gate"]
    _fields(record, "schema_version kind " + fields)
    require(type(record["schema_version"]) is int and record["schema_version"] == 1,
            "administrative_schema_version")
    require(record["kind"] == kind, "administrative_record_kind")
    return record


def _identity(value):
    require(isinstance(value, str) and bool(value.strip()), "administrative_identity_required")
    return value


def administrative_baseline_digest(mission_id, description, private):
    """Hash only verified live identity, exact description and explicit privacy.

    Map the actual API response to these fields in the independently reviewed
    adapter. Never default absent privacy/identity fields to their expected value.
    """
    require(isinstance(mission_id, str) and str(UUID(mission_id)) == mission_id,
            "administrative_canonical_mission_id")
    require(isinstance(description, str), "administrative_description_required")
    require(private is True, "administrative_private_baseline_required")
    return digest(canonical_bytes({"mission_id": mission_id, "description": description, "private": private}))


@dataclass(frozen=True)
class AdministrativeDecision:
    mission_id: str
    expires_at: datetime
    required_baseline_sha256: str
    foundation_credit_permitted: bool = False
    native_graph_completion_permitted: bool = False
    full_mission_completion_permitted: bool = False


def validate_administrative_request(authorization_pin, *, publisher_id, action,
                                    method, path, payload, content_type, now=None):
    """Deny unsupported operations or stale/mismatched independent evidence.

    The authorization SHA is provisioned separately by the authorized owner.
    A candidate must never be allowed to choose or refresh its own trust anchor.
    """
    try:
        require(action == "administrative_update", "administrative_action_only")
        require(method == "PATCH", "administrative_patch_only")
        require(content_type == "application/json", "administrative_json_only")
        require(type(payload) is bytes, "administrative_immutable_bytes_required")
        current = now if now is not None else datetime.now(timezone.utc)
        require(isinstance(current, datetime) and current.tzinfo is not None and current.utcoffset() is not None,
                "administrative_aware_clock_required")
        auth = _record(authorization_pin, "authorization",
                       "mission_id author_id reviewer_id publisher_id mission_contract basis baseline appendix payload review release authorized_at expires_at required_baseline_sha256")
        mission = auth["mission_id"]
        require(isinstance(mission, str) and str(UUID(mission)) == mission, "administrative_canonical_mission_id")
        require(path == "/missions/" + mission, "administrative_exact_mission_route")
        author, reviewer = _identity(auth["author_id"]), _identity(auth["reviewer_id"])
        require(author != reviewer, "administrative_independent_review_required")
        require(_identity(auth["publisher_id"]) == _identity(publisher_id), "administrative_wrong_publisher")
        # Current paths must remain pinned. Administrative changes require fresh
        # exact authorization/review; no attempt is made to interpret semantics.
        _pin(auth["mission_contract"])
        _pin(auth["basis"])
        baseline = _record(auth["baseline"], "baseline", "mission_id description private observed_at")
        require(baseline["mission_id"] == mission, "administrative_baseline_mission_mismatch")
        baseline_hash = administrative_baseline_digest(mission, baseline["description"], baseline["private"])
        require(auth["required_baseline_sha256"] == baseline_hash, "administrative_baseline_digest_mismatch")
        appendix = _pin(auth["appendix"]).decode("utf-8")
        require(appendix.startswith("\n\n") and bool(appendix.strip()), "administrative_separate_appendix_required")
        require(_pin(auth["payload"]) == payload, "administrative_exact_payload_required")
        body = _json(payload)
        _fields(body, "description")
        require(isinstance(body["description"], str) and body["description"] == baseline["description"] + appendix,
                "administrative_prior_description_must_be_preserved")
        review = _record(auth["review"], "review",
                         "author_id reviewer_id publisher_id mission_id mission_contract basis baseline appendix payload required_baseline_sha256 request verdict governance_only prior_description_preserved scientific_claims_added reviewed_at")
        release = _record(auth["release"], "release",
                          "publisher_id mission_id review request required_baseline_sha256 valid_from expires_at")
        for key in ("author_id", "reviewer_id", "publisher_id", "mission_id", "mission_contract", "basis", "baseline", "appendix", "payload", "required_baseline_sha256"):
            require(review[key] == auth[key], "administrative_review_evidence_mismatch")
        require(review["verdict"] == "accepted" and review["governance_only"] is True and
                review["prior_description_preserved"] is True and review["scientific_claims_added"] is False,
                "administrative_governance_review_required")
        for key in ("publisher_id", "mission_id", "review", "required_baseline_sha256"):
            require(release[key] == auth[key], "administrative_release_evidence_mismatch")
        request = {"action": action, "method": method, "path": path,
                   "content_type": content_type, "body_sha256": digest(payload)}
        require(review["request"] == request and release["request"] == request,
                "administrative_exact_reviewed_request_required")
        observed, reviewed = _time(baseline["observed_at"]), _time(review["reviewed_at"])
        authorized, authority_end = _time(auth["authorized_at"]), _time(auth["expires_at"])
        start, end = _time(release["valid_from"]), _time(release["expires_at"])
        require(observed <= reviewed <= authorized <= start <= current < end <= authority_end,
                "administrative_expired_or_invalid_chronology")
        require(0 < (authority_end - authorized).total_seconds() <= MAX_RELEASE_SECONDS,
                "administrative_release_window_too_long")
        return AdministrativeDecision(mission, end, baseline_hash)
    except GateRejected:
        raise
    except (KeyError, TypeError, ValueError, OSError, AttributeError, OverflowError, RecursionError) as exc:
        raise GateRejected("malformed_administrative_evidence") from exc


class GuardedAdministrativePublisher:
    def __init__(self, authorization_pin, publisher_id, mutation_callback, *, clock=None):
        self._authorization_pin = copy.deepcopy(authorization_pin)
        self._publisher_id = publisher_id
        self._mutation_callback = mutation_callback
        self._clock = clock or (lambda: datetime.now(timezone.utc))

    def mutate(self, *, action, method, path, payload, content_type):
        """Recheck each call; pass immutable exact bytes once, without retries.

        Callback integration owns live private-baseline verification immediately
        before PATCH and expiry after its GET. Direct transport bypasses this API.
        """
        decision = validate_administrative_request(
            self._authorization_pin, publisher_id=self._publisher_id, action=action,
            method=method, path=path, payload=payload, content_type=content_type, now=self._clock())
        if self._clock() >= decision.expires_at:
            raise GateRejected("administrative_expired_before_callback")
        return self._mutation_callback(method, path, payload, content_type)
