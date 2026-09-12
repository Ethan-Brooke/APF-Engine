"""Synthetic administrative boundary tests; never obtains credentials or HTTP."""
import copy
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import tempfile
import unittest

from apf.evidence_gate import GateRejected, canonical_bytes, digest
from apf.administrative_publisher import (GuardedAdministrativePublisher,
    validate_administrative_request, administrative_baseline_digest)

NOW = datetime(2026, 9, 12, 20, 0, tzinfo=timezone.utc)
MISSION = "11111111-2222-4333-8444-555555555555"


def stamp(seconds):
    return (NOW + timedelta(seconds=seconds)).isoformat()


class AdministrativeFixture:
    def __init__(self, root):
        self.root = Path(root)
        self.baseline = {"mission_id": MISSION, "description": "Existing scientific description.\n", "private": True, "observed_at": stamp(-30)}
        self.appendix = "\n\nGovernance appendix: reviewed local publishing checks only."
        self.body = {"description": self.baseline["description"] + self.appendix}
        self.payload = canonical_bytes(self.body)
        self.request_changes = {}
        self.review_changes = {}
        self.release_changes = {}
        self.auth_changes = {}

    def file(self, name, data):
        path = self.root / name
        path.write_bytes(data)
        return {"path": str(path.resolve()), "sha256": digest(data)}

    def record(self, name, kind, data):
        return self.file(name, canonical_bytes({"administrative_gate": {"schema_version": 1, "kind": kind, **data}}))

    def freeze(self):
        mission = self.file("mission.md", b"Synthetic current authorized mission contract.")
        basis = self.file("basis.json", b'{"basis":"unchanged synthetic basis"}')
        baseline = self.record("baseline.json", "baseline", self.baseline)
        appendix = self.file("appendix.md", self.appendix.encode())
        payload = self.file("payload.json", self.payload)
        # Compute expected private projection even in deliberately invalid fixtures.
        baseline_hash = digest(canonical_bytes({k: self.baseline[k] for k in ("mission_id", "description", "private")}))
        self.request = {"action": "administrative_update", "method": "PATCH", "path": "/missions/" + MISSION, "content_type": "application/json", "body_sha256": digest(self.payload), **self.request_changes}
        common = {"author_id": "author", "reviewer_id": "independent-reviewer", "publisher_id": "publisher", "mission_id": MISSION, "mission_contract": mission, "basis": basis, "baseline": baseline, "appendix": appendix, "payload": payload, "required_baseline_sha256": baseline_hash}
        review = self.record("review.json", "review", {**common, "request": self.request, "verdict": "accepted", "governance_only": True, "prior_description_preserved": True, "scientific_claims_added": False, "reviewed_at": stamp(-20), **self.review_changes})
        release = self.record("release.json", "release", {"publisher_id": "publisher", "mission_id": MISSION, "review": review, "request": self.request, "required_baseline_sha256": baseline_hash, "valid_from": stamp(-5), "expires_at": stamp(60), **self.release_changes})
        self.auth = {**common, "review": review, "release": release, "authorized_at": stamp(-10), "expires_at": stamp(60), **self.auth_changes}
        self.pin = self.record("authorization.json", "authorization", self.auth)
        return self.pin

    def kwargs(self):
        return {k: self.request[k] for k in ("action", "method", "path", "content_type")} | {"payload": self.payload}


class AdministrativePublisherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.f = AdministrativeFixture(self.temp.name)
        self.calls = []

    def callback(self, *args):
        self.calls.append(args)
        return "simulated update"

    def invoke(self, pin=None, publisher="publisher", clock=None, **changes):
        pin = pin or self.f.freeze()
        wrapper = GuardedAdministrativePublisher(pin, publisher, self.callback, clock=clock or (lambda: NOW))
        return wrapper.mutate(**(self.f.kwargs() | changes))

    def reject(self, pin=None, **changes):
        with self.assertRaises(GateRejected):
            self.invoke(pin, **changes)
        self.assertEqual(self.calls, [], "Rejected evidence must not enter mutation callback")

    def test_exact_reviewed_appendix_positive(self):
        self.assertEqual(self.invoke(), "simulated update")
        self.assertEqual(self.calls, [("PATCH", "/missions/" + MISSION, self.f.payload, "application/json")])

    def test_no_scientific_credit(self):
        pin = self.f.freeze()
        d = validate_administrative_request(pin, publisher_id="publisher", now=NOW, **self.f.kwargs())
        self.assertFalse(d.foundation_credit_permitted)
        self.assertFalse(d.native_graph_completion_permitted)
        self.assertFalse(d.full_mission_completion_permitted)
        self.assertEqual(d.required_baseline_sha256, administrative_baseline_digest(MISSION, self.f.baseline["description"], True))

    def test_scientific_and_public_actions_rejected_even_if_pinned(self):
        for action in ("private_stage", "foundation_promote", "native_graph_complete", "full_mission_complete", "public_release"):
            with self.subTest(action=action):
                self.f.request_changes = {"action": action}
                self.reject()

    def test_non_patch_methods_rejected_even_if_reviewed(self):
        for method in ("GET", "POST", "DELETE", "PUT", "patch"):
            with self.subTest(method=method):
                self.f.request_changes = {"method": method}
                self.reject()

    def test_routes_are_exact_not_normalized(self):
        for path in ("/verify", "/submit-problem", "/missions/other", "/missions/"+MISSION+"?trace=1", "/missions/"+MISSION+"/../other", "https://example.test/missions/"+MISSION, "/missions//"+MISSION):
            with self.subTest(path=path):
                self.f.request_changes = {"path": path}
                self.reject()

    def test_other_media_types_rejected(self):
        for media in ("application/merge-patch+json", "text/plain", "multipart/form-data", "application/json; charset=utf-8"):
            with self.subTest(media=media):
                self.f.request_changes = {"content_type": media}
                self.reject()

    def test_extra_payload_keys_rejected_even_when_reviewed(self):
        for key, value in (("private", False), ("visibility", "public"), ("status", "complete"), ("foundation", True), ("title", "changed")):
            with self.subTest(key=key):
                self.f.payload = canonical_bytes(self.f.body | {key: value})
                self.reject()

    def test_changed_prior_scientific_description_rejected(self):
        self.f.payload = canonical_bytes({"description": "Rewritten scientific content." + self.f.appendix})
        self.reject()

    def test_unreviewed_extra_appendix_rejected(self):
        self.f.payload = canonical_bytes({"description": self.f.body["description"] + " Extra unreviewed claim."})
        self.reject()

    def test_empty_or_unseparated_appendix_rejected(self):
        for appendix in ("", "\n\n", "unseparated governance"):
            with self.subTest(appendix=appendix):
                self.f.appendix = appendix
                self.f.payload = canonical_bytes({"description": self.f.baseline["description"] + appendix})
                self.reject()

    def test_public_or_implicit_private_baseline_rejected(self):
        for private in (False, None, 1, "true"):
            with self.subTest(private=private):
                self.f.baseline["private"] = private
                self.reject()

    def test_wrong_publisher_rejected(self):
        self.reject(publisher="someone-else")

    def test_self_review_rejected_even_consistent(self):
        self.f.review_changes["reviewer_id"] = "author"
        self.f.auth_changes["reviewer_id"] = "author"
        self.reject()

    def test_unaccepted_or_scientific_review_rejected(self):
        for key, value in (("verdict", "pending"), ("governance_only", False), ("prior_description_preserved", False), ("scientific_claims_added", True)):
            with self.subTest(key=key):
                self.f.review_changes = {key: value}
                self.reject()

    def test_review_identity_and_digest_mismatches(self):
        for key, value in (("author_id", "other"), ("publisher_id", "other"), ("reviewer_id", "other"), ("required_baseline_sha256", "0"*64)):
            with self.subTest(key=key):
                self.f.review_changes = {key: value}
                self.reject()

    def test_release_review_or_request_mismatch(self):
        self.f.release_changes["request"] = {"method": "PATCH"}
        self.reject()

    def test_changed_request_after_review_rejected(self):
        self.reject(payload=canonical_bytes({"description": "Changed after review"}))

    def test_changed_any_evidence_bytes_rejected(self):
        for key in ("mission_contract", "basis", "baseline", "appendix", "payload", "review", "release"):
            with self.subTest(key=key):
                pin = self.f.freeze()
                Path(self.f.auth[key]["path"]).write_bytes(b"changed")
                self.reject(pin)

    def test_changed_authorization_anchor_rejected(self):
        pin = self.f.freeze()
        Path(pin["path"]).write_bytes(b"changed authority")
        self.reject(pin)

    def test_missing_evidence_rejected(self):
        pin = self.f.freeze()
        Path(self.f.auth["review"]["path"]).unlink()
        self.reject(pin)

    def test_expired_release_rejected(self):
        self.f.release_changes["expires_at"] = stamp(0)
        self.reject()

    def test_future_or_reversed_chronology_rejected(self):
        for changes in ({"reviewed_at": stamp(10)}, {"reviewed_at": stamp(-40)}):
            with self.subTest(changes=changes):
                self.f.review_changes = changes
                self.reject()

    def test_unbounded_authorization_rejected(self):
        self.f.auth_changes["expires_at"] = stamp(7200)
        self.reject()

    def test_expiry_rechecked_before_callback(self):
        times = iter((NOW, NOW + timedelta(seconds=60)))
        self.reject(clock=lambda: next(times))

    def test_every_call_revalidates_evidence(self):
        pin = self.f.freeze()
        wrapper = GuardedAdministrativePublisher(pin, "publisher", self.callback, clock=lambda: NOW)
        wrapper.mutate(**self.f.kwargs())
        Path(self.f.auth["basis"]["path"]).write_bytes(b"weakened")
        with self.assertRaises(GateRejected):
            wrapper.mutate(**self.f.kwargs())
        self.assertEqual(len(self.calls), 1)

    def test_callback_failure_not_retried(self):
        pin = self.f.freeze()
        calls = []
        def failed(*args):
            calls.append(args)
            raise RuntimeError("transport failed")
        wrapper = GuardedAdministrativePublisher(pin, "publisher", failed, clock=lambda: NOW)
        with self.assertRaises(RuntimeError):
            wrapper.mutate(**self.f.kwargs())
        self.assertEqual(len(calls), 1)

    def test_duplicate_json_key_rejected(self):
        self.f.payload = b'{"description":"a","description":"b"}'
        self.reject()

    def test_scientific_schema_and_unknown_fields_rejected(self):
        self.f.auth_changes["foundation_credit"] = True
        self.reject()

    def test_mutable_payload_rejected(self):
        self.reject(payload=bytearray(self.f.payload))

    def test_auth_pin_is_copied(self):
        pin = self.f.freeze()
        wrapper = GuardedAdministrativePublisher(pin, "publisher", self.callback, clock=lambda: NOW)
        pin["sha256"] = "0" * 64
        self.assertEqual(wrapper.mutate(**self.f.kwargs()), "simulated update")

    def test_adapter_baseline_mismatch_prevents_transport(self):
        pin = self.f.freeze()
        d = validate_administrative_request(pin, publisher_id="publisher", now=NOW, **self.f.kwargs())
        transports = []
        def adapter(*args):
            actual = administrative_baseline_digest(MISSION, "Concurrent changed description", True)
            if actual != d.required_baseline_sha256:
                raise GateRejected("live_baseline_changed")
            transports.append(args)
        wrapper = GuardedAdministrativePublisher(pin, "publisher", adapter, clock=lambda: NOW)
        with self.assertRaises(GateRejected):
            wrapper.mutate(**self.f.kwargs())
        self.assertEqual(transports, [])

    def test_adapter_matching_private_baseline_permits_exact_transport(self):
        pin = self.f.freeze()
        d = validate_administrative_request(pin, publisher_id="publisher", now=NOW, **self.f.kwargs())
        def adapter(*args):
            actual = administrative_baseline_digest(MISSION, self.f.baseline["description"], True)
            if actual != d.required_baseline_sha256:
                raise GateRejected("live_baseline_changed")
            return self.callback(*args)
        wrapper = GuardedAdministrativePublisher(pin, "publisher", adapter, clock=lambda: NOW)
        self.assertEqual(wrapper.mutate(**self.f.kwargs()), "simulated update")
        self.assertEqual(self.calls[0][2], self.f.payload)


if __name__ == "__main__":
    unittest.main()
