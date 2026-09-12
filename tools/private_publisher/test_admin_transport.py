"""Administrative client tests against captured GET/PATCH urllib requests."""
import copy
import io
import json
import tempfile
import unittest
from datetime import timedelta
from pathlib import Path

from apf.evidence_gate import GateRejected
from test_administrative_publisher import AdministrativeFixture, NOW, MISSION
from p2m_guarded_client import AdministrativeP2MClient, BASE


class AdministrativeTransportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.f = AdministrativeFixture(self.temp.name)
        self.pin = self.f.freeze()
        self.instant = NOW
        self.live = {"id": MISSION, "description": self.f.baseline["description"], "visibility": "private"}
        self.requests = []
        self.on_get = None
        self.get_failure = None
        self.patch_failure = None
        self.client = AdministrativeP2MClient(self.pin, "publisher", opener=self,
                                               clock=lambda: self.instant)

    def open(self, request, timeout):
        self.assertFalse(request.has_header("Authorization"), "No credentials in these tests")
        self.requests.append(request)
        if request.get_method() == "GET":
            if self.get_failure:
                raise self.get_failure
            if self.on_get:
                self.on_get()
            return io.BytesIO(json.dumps({"missions": [self.live]}).encode())
        if self.patch_failure:
            raise self.patch_failure
        self.live["description"] = json.loads(request.data)["description"]
        return io.BytesIO(b'{"captured":true}')

    def send(self, **changes):
        return self.client.send_administrative(**(self.f.kwargs() | changes))

    def mutations(self):
        return [r for r in self.requests if r.get_method() != "GET"]

    def rejected_without_patch(self, **changes):
        count = len(self.mutations())
        with self.assertRaises(GateRejected):
            self.send(**changes)
        self.assertEqual(len(self.mutations()), count)

    def test_exact_baseline_get_then_exact_payload_patch(self):
        self.assertTrue(self.send()["captured"])
        self.assertEqual([r.get_method() for r in self.requests], ["GET", "PATCH"])
        get, patch = self.requests
        self.assertEqual(get.full_url, BASE + "/missions?limit=100&offset=0")
        self.assertEqual(patch.full_url, BASE + "/missions/" + MISSION)
        self.assertIs(patch.data, self.f.payload)
        self.assertEqual(patch.get_header("Content-type"), "application/json")

    def test_changed_live_description_blocks_patch(self):
        self.live["description"] += "concurrent change"
        self.rejected_without_patch()
        self.assertEqual(len(self.requests), 1)

    def test_missing_or_public_visibility_blocks_patch(self):
        for visibility in (None, "public", True):
            with self.subTest(visibility=visibility):
                self.live["visibility"] = visibility
                self.rejected_without_patch()
        self.live.pop("visibility")
        self.rejected_without_patch()

    def test_wrong_or_missing_identity_blocks_patch(self):
        self.live["id"] = "other"
        self.rejected_without_patch()
        self.live.pop("id")
        self.rejected_without_patch()

    def test_missing_or_nontext_description_blocks_patch(self):
        self.live.pop("description")
        self.rejected_without_patch()
        self.live["description"] = None
        self.rejected_without_patch()

    def test_get_failure_never_reaches_patch(self):
        self.get_failure = TimeoutError("simulated failed GET")
        with self.assertRaises(TimeoutError):
            self.send()
        self.assertEqual(self.mutations(), [])
        self.assertEqual(len(self.requests), 1)

    def test_expiry_during_get_blocks_patch(self):
        self.on_get = lambda: setattr(self, "instant", NOW + timedelta(seconds=61))
        self.rejected_without_patch()
        self.assertEqual(len(self.requests), 1)

    def test_changed_contract_during_get_blocks_patch(self):
        self.on_get = lambda: (Path(self.temp.name) / "mission.md").write_bytes(b"changed after initial check")
        self.rejected_without_patch()
        self.assertEqual(len(self.requests), 1)

    def test_changed_release_during_get_blocks_patch(self):
        self.on_get = lambda: (Path(self.temp.name) / "release.json").write_bytes(b"changed after initial check")
        self.rejected_without_patch()

    def test_expired_release_blocks_all_network(self):
        self.instant = NOW + timedelta(seconds=61)
        self.rejected_without_patch()
        self.assertEqual(self.requests, [])

    def test_missing_authorization_blocks_all_network(self):
        Path(self.pin["path"]).unlink()
        self.rejected_without_patch()
        self.assertEqual(self.requests, [])

    def test_unreviewed_payload_or_extra_fields_block_all_network(self):
        self.rejected_without_patch(payload=b'{"description":"substitute","visibility":"public"}')
        self.assertEqual(self.requests, [])

    def test_scientific_actions_cannot_enter_administrative_lane(self):
        for action in ("private_stage", "foundation_promote", "native_graph_complete", "full_mission_complete"):
            with self.subTest(action=action):
                self.rejected_without_patch(action=action)
        self.assertEqual(self.requests, [])

    def test_verify_and_other_routes_cannot_enter_administrative_lane(self):
        for change in ({"path": "/verify"}, {"method": "POST"}, {"path": "/missions/other"},
                       {"content_type": "multipart/form-data; boundary=x"}):
            with self.subTest(change=change):
                self.rejected_without_patch(**change)
        self.assertEqual(self.requests, [])

    def test_post_success_baseline_change_blocks_second_write(self):
        self.send()
        self.rejected_without_patch()
        self.assertEqual(len(self.mutations()), 1)

    def test_expiry_during_journal_blocks_actual_admin_send(self):
        self.client._before_mutation = lambda *_: setattr(self, "instant", NOW + timedelta(seconds=61))
        self.rejected_without_patch()
        self.assertEqual(len(self.requests), 1)

    def test_basis_change_during_journal_blocks_actual_admin_send(self):
        self.client._before_mutation = lambda *_: (Path(self.temp.name) / "basis.json").write_bytes(b"changed during journal")
        self.rejected_without_patch()
        self.assertEqual(len(self.requests), 1)

    def test_uncertain_patch_is_never_retried(self):
        self.patch_failure = TimeoutError("simulated uncertain PATCH")
        with self.assertRaises(TimeoutError):
            self.send()
        self.assertEqual([r.get_method() for r in self.requests], ["GET", "PATCH"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
