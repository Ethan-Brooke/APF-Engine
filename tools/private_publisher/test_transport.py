"""Captured urllib boundary tests. Synthetic evidence only; no credentials/network."""
import io
import json
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from apf.evidence_gate import GateRejected, canonical_bytes, digest
from test_evidence_gate import Fixture, NOW
from p2m_guarded_client import P2MClient, NoRedirect, build_verify_payload, BASE


class Capture:
    def __init__(self, failure=None):
        self.requests = []
        self.failure = failure

    def open(self, request, timeout):
        if request.has_header("Authorization"):
            raise AssertionError("No credentials, even synthetic ones, belong in these tests")
        self.requests.append(request)
        if self.failure:
            raise self.failure
        return io.BytesIO(b'{"captured":true}')


class TransportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.fixture = Fixture(self.temp.name)
        self.capture = Capture()
        self.instant = NOW

    def client(self, pin=None):
        return P2MClient(pin or self.fixture.freeze(), "publisher", opener=self.capture,
                         clock=lambda: self.instant)

    def invoke(self, client=None, **overrides):
        args = self.fixture.kwargs()
        args.update(overrides)
        return (client or self.client()).send_reviewed(**args)

    def denied(self, invoke):
        count = len(self.capture.requests)
        with self.assertRaises(GateRejected):
            invoke()
        self.assertEqual(len(self.capture.requests), count)

    def test_exact_reviewed_json_bytes_reach_urllib_unchanged(self):
        self.assertTrue(self.invoke()["captured"])
        req, = self.capture.requests
        self.assertIs(req.data, self.fixture.payload)
        self.assertEqual(req.full_url, BASE + self.fixture.request["path"])
        self.assertEqual(req.get_method(), "PATCH")
        self.assertEqual(req.get_header("Content-type"), "application/json")

    def test_reviewed_delete_accepts_empty_204_once(self):
        self.fixture.action = "private_stage"
        self.fixture.payload = b"{}"
        self.fixture.request.update(method="DELETE", path="/milestones/9a54f1bf-66eb-4f87-9c57-3cca8b584baf",
                                    body_sha256=digest(b"{}"))
        requests = self.capture.requests
        class Empty204:
            def open(self, request, timeout):
                requests.append(request)
                response = io.BytesIO(b"")
                response.status = 204
                return response
        self.capture = Empty204()
        client = self.client()
        self.assertEqual(self.invoke(client), {"http_status": 204, "body": None})
        self.assertEqual(len(requests), 1)
        self.assertEqual(requests[0].data, b"{}")
        self.assertEqual(requests[0].get_method(), "DELETE")
        with self.assertRaises(GateRejected):
            self.invoke(client, path="/theorems/9a54f1bf-66eb-4f87-9c57-3cca8b584baf")
        self.assertEqual(len(requests), 1)

    def test_unexpected_empty_json_success_is_still_an_error(self):
        class Empty200:
            def open(self, request, timeout):
                response = io.BytesIO(b"")
                response.status = 200
                return response
        self.capture = Empty200()
        with self.assertRaises(json.JSONDecodeError):
            self.invoke()

    def test_204_with_unexpected_body_is_still_an_error(self):
        self.fixture.action = "private_stage"
        self.fixture.payload = b"{}"
        self.fixture.request.update(method="DELETE", path="/milestones/9a54f1bf-66eb-4f87-9c57-3cca8b584baf",
                                    body_sha256=digest(b"{}"))
        class Bad204:
            def open(self, request, timeout):
                response = io.BytesIO(b"unexpected")
                response.status = 204
                return response
        self.capture = Bad204()
        with self.assertRaisesRegex(RuntimeError, "unexpectedly contained"):
            self.invoke()

    def test_all_json_mutation_methods_use_guard(self):
        for method in ("POST", "PUT", "PATCH"):
            with self.subTest(method=method):
                body = {"description": "Unicode — exact", "visibility": "private"}
                self.fixture.payload = canonical_bytes(body)
                self.fixture.request.update(method=method, body_sha256=digest(self.fixture.payload))
                client = self.client()
                client.call(method, self.fixture.request["path"], body, action=self.fixture.action)
                self.assertEqual(self.capture.requests[-1].data, self.fixture.payload)
                self.denied(lambda: client.call(method, self.fixture.request["path"], {"description": "changed"}, action=self.fixture.action))

    def test_multipart_verify_reaches_same_guarded_transport(self):
        payload, media = build_verify_payload("theorem", b"-- frozen proof\n", "Scoped evidence", boundary="frozen-boundary")
        self.fixture.payload = payload
        self.fixture.request.update(method="POST", path="/verify", content_type=media, body_sha256=digest(payload))
        client = self.client()
        client.multipart(payload, media, action=self.fixture.action)
        req, = self.capture.requests
        self.assertIs(req.data, payload)
        self.assertEqual(req.full_url, BASE + "/verify")
        self.assertEqual(req.get_header("Content-type"), media)
        self.denied(lambda: client.multipart(payload + b"changed", media, action=self.fixture.action))

    def test_missing_authorization_never_opens_network(self):
        client = P2MClient(None, "publisher", opener=self.capture, clock=lambda: NOW)
        self.denied(lambda: self.invoke(client))

    def test_invalid_trust_hash_never_opens_network(self):
        pin = self.fixture.freeze()
        pin["sha256"] = "0" * 64
        self.denied(lambda: self.invoke(self.client(pin)))

    def test_stale_source_after_success_is_rechecked(self):
        client = self.client()
        self.invoke(client)
        Path(self.fixture.code["path"]).write_bytes(b"changed code")
        self.denied(lambda: self.invoke(client))

    def test_expiry_after_success_is_rechecked(self):
        client = self.client()
        self.invoke(client)
        self.instant = NOW + timedelta(minutes=2)
        self.denied(lambda: self.invoke(client))

    def test_stale_release_after_success_is_rechecked(self):
        client = self.client()
        self.invoke(client)
        (Path(self.temp.name) / "release.json").write_bytes(b"changed release")
        self.denied(lambda: self.invoke(client))

    def test_multipart_missing_and_expired_evidence_never_opens_network(self):
        payload, media = build_verify_payload("theorem", b"proof", "exact", boundary="test-boundary")
        self.fixture.payload = payload
        self.fixture.request.update(method="POST", path="/verify", content_type=media, body_sha256=digest(payload))
        client = self.client()
        self.instant = NOW + timedelta(minutes=2)
        self.denied(lambda: client.multipart(payload, media, action=self.fixture.action))
        self.instant = NOW
        (Path(self.temp.name) / "review.json").unlink()
        self.denied(lambda: client.multipart(payload, media, action=self.fixture.action))

    def test_missing_consultation_never_opens_network(self):
        self.fixture.consults["author"]["papers"] = []
        self.denied(lambda: self.invoke())

    def test_missing_and_circular_suppliers_never_open_network(self):
        self.fixture.package["premises"][0]["suppliers"] = ["missing"]
        self.denied(lambda: self.invoke())
        self.fixture.package["premises"][0]["suppliers"] = ["result"]
        self.denied(lambda: self.invoke())

    def test_unreviewed_method_path_content_and_action_never_open_network(self):
        client = self.client()
        for override in ({"method": "DELETE"}, {"method": "GET"}, {"path": "/missions/other"},
                         {"content_type": "text/plain"}, {"action": "not-an-action"},
                         {"payload": bytearray(self.fixture.payload)}):
            with self.subTest(override=override):
                self.denied(lambda: self.invoke(client, **override))

    def test_public_json_even_if_pinned_is_rejected(self):
        self.fixture.payload = canonical_bytes({"description": "x", "visibility": "public"})
        self.fixture.request["body_sha256"] = digest(self.fixture.payload)
        self.denied(lambda: self.invoke())

    def test_route_aliases_even_if_pinned_are_rejected(self):
        for path in ("/missions/private-id?x=1", "/missions/../private-id", "/missions/%70rivate-id"):
            with self.subTest(path=path):
                self.fixture.request["path"] = path
                self.denied(lambda: self.invoke())

    def test_valid_transport_failure_is_not_retried(self):
        self.capture.failure = TimeoutError("simulated uncertain network")
        with self.assertRaises(TimeoutError):
            self.invoke()
        self.assertEqual(len(self.capture.requests), 1)

    def test_expiry_during_journal_blocks_actual_scientific_send(self):
        client = self.client()
        client._before_mutation = lambda *_: setattr(self, "instant", NOW + timedelta(minutes=2))
        self.denied(lambda: self.invoke(client))

    def test_basis_change_during_journal_blocks_actual_scientific_send(self):
        client = self.client()
        client._before_mutation = lambda *_: Path(self.fixture.basis["path"]).write_bytes(b"changed during journal")
        self.denied(lambda: self.invoke(client))

    def test_get_readback_is_separate_and_has_no_payload(self):
        client = P2MClient(None, "publisher", opener=self.capture)
        client.call("GET", "/verify?submission_id=read-only")
        self.assertIsNone(self.capture.requests[-1].data)
        with self.assertRaises(ValueError):
            client.call("GET", "/missions", {"description": "must not send"})
        self.assertEqual(len(self.capture.requests), 1)

    def test_redirects_are_disabled_for_exact_route_and_token_safety(self):
        self.assertIsNone(NoRedirect().redirect_request(None, None, 307, "redirect", {}, "https://other.invalid"))

    def test_multipart_builder_rejects_ambiguous_boundaries(self):
        for boundary, content in (("bad\r\nheader", b"proof"), ("collision", b"--collision")):
            with self.assertRaises(ValueError):
                build_verify_payload("theorem", content, "exact", boundary=boundary)


if __name__ == "__main__":
    unittest.main(verbosity=2)
