"""Synthetic boundary tests; no credentials or live transport are used."""
import copy
import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from apf.evidence_gate import GateRejected, canonical_bytes, digest, validate_request
from apf.private_publisher import GuardedPrivatePublisher

NOW = datetime(2026, 9, 12, 19, 0, tzinfo=timezone.utc)


def stamp(minutes):
    return (NOW + timedelta(minutes=minutes)).isoformat()


class Fixture:
    def __init__(self, root):
        self.root = Path(root)
        self.action = "foundation_promote"
        self.payload = b'{"description":"exact reviewed claim","visibility":"private"}'
        self.request = {"method": "PATCH", "path": "/missions/private-id", "content_type": "application/json", "body_sha256": digest(self.payload)}
        self.paper = self.file("paper.txt", b"Original paper source, synthetic.")
        self.code = self.file("code.py", b"# Actual code source, synthetic\n")
        self.proof = self.file("proof.lean", b"-- Exact reviewed proof, synthetic only\n")
        self.basis = self.file("basis.json", canonical_bytes({"B05": "uniform support-novel family marginal floor"}))
        self.mission = self.file("mission.md", b"Explicit commissioned mission, synthetic.")
        self.sources = {"papers": [self.paper], "codebank": [self.code]}
        self.consults = {}
        for person, ago in (("manager", -16), ("author", -11), ("selector", -13), ("reviewer", -6)):
            self.consults[person] = {"person_id": person, "status": "complete", "read_completed_at": stamp(ago-1), "recorded_at": stamp(ago), **self.sources}
        self.assignment = {"mission_scope_sha256": digest(b"mission semantic scope"), "basis_scope_sha256": digest(b"basis semantic scope"), "conclusion_id": "result", "conclusion": "Exact selected conclusion.", "scope": "segment", "author_id": "author", "work_type": "formalization", "intended_addition": "Formalize the exact scoped existing result", "manager_id": "manager", "assigned_at": stamp(-15), "constructed_after_utc": stamp(-8)}
        self.package = {"conclusion_id": "result", "frozen_at": stamp(-4), "files": [self.proof, self.basis, self.paper, self.code], "sources": self.sources, "evidence_axes": {"papers": "Source checked", "codebank": "Code checked", "machine_checked": "Scoped proof checked", "foundation": "Scoped closure accepted"}, "premises": [
            {"id": "result", "kind": "derived", "suppliers": ["input"], "evidence": [self.proof], "native_id": "native-result"},
            {"id": "input", "kind": "approved_input", "suppliers": [], "evidence": [self.basis], "input_id": "B05", "native_id": "native-input"},
        ]}
        self.selection = {"accepted": True, "author_id": "author", "reviewer_id": "selector", "evaluation_started_at": stamp(-12), "decided_at": stamp(-9), "work_type": self.assignment["work_type"], "intended_addition": self.assignment["intended_addition"]}
        self.review = {"accepted": True, "author_id": "author", "reviewer_id": "reviewer", "evaluation_started_at": stamp(-3), "decided_at": stamp(-2), "conclusion_id": "result", "conclusion_sha256": digest(self.assignment["conclusion"].encode()), "source_fidelity_accepted": True, "premise_inventory_complete": True, "proof_verdict": "accepted", "machine_checked": True, "foundation_closure_accepted": True, "objective_complete": True, "allowed_actions": ["private_stage", "foundation_promote", "native_graph_complete", "full_mission_complete"], "permitted_claim": "Exact reviewed claim", "accepted_premise_ids": ["result", "input"], "ordinary_disposition_ids": [], "evidence_axes": self.package["evidence_axes"], "accepted_requests": [self.request], "proof_evidence": [self.proof], "ordinary_native_ids": [], "work_type": self.assignment["work_type"], "intended_addition": self.assignment["intended_addition"]}
        self.release = {"mission_id": "private-id", "publisher_id": "publisher", "private_only": True, "not_before": stamp(-1), "expires_at": stamp(1), "conclusion_id": "result", "conclusion_sha256": self.review["conclusion_sha256"], "permitted_claim": self.review["permitted_claim"], "evidence_axes": self.package["evidence_axes"], "request": self.request}
        self.raw_graph = {"root_id": "native-result", "has_hidden_deprecated_sketches": False, "nodes": [{"node_type": "theorem", "theorem_id": "native-result", "status": "Proved", "has_more_children": False}, {"node_type": "sketch", "id": "sketch-s"}, {"node_type": "definition", "theorem_id": "native-input", "status": "Definition"}], "edges": [{"source": "native-result", "target": "sketch-s", "kind": "sketch"}, {"source": "sketch-s", "target": "native-input", "kind": "child"}]}
        self.requirements = {"root_id": "native-result", "nodes": ["native-result", "sketch-s", "native-input"], "edges": [["native-result", "sketch-s", "sketch"], ["sketch-s", "native-input", "child"]]}
        self.ui = {"mission_id": "private-id", "root_id": "native-result", "native_default_view": True, "reviewer_id": "reviewer", "observed_at": stamp(-3), "visible_nodes": list(self.requirements["nodes"]), "visible_edges": copy.deepcopy(self.requirements["edges"]), "capture": self.file("ui-capture.txt", b"Synthetic native UI readback evidence")}
        self.graph = {"mission_id": "private-id", "visibility": "private", "observed_at": stamp(-3), "request": {"method": "GET", "path": "/theorems/native-result/graph", "status": 200}}

    def file(self, name, raw):
        path = self.root / name
        path.write_bytes(raw)
        return {"path": str(path), "sha256": digest(raw)}

    def record(self, name, data):
        return self.file(name, canonical_bytes({"evidence_gate": {"schema_version": 1, **data}}))

    def freeze(self):
        """Re-pin synthetic reviewed data so semantic tests reach the deep checks."""
        cp = {person: self.record(person+"-consult.json", data) for person, data in self.consults.items()}
        self.assignment["author_consultation"] = cp["author"]
        self.assignment["manager_consultation"] = cp["manager"]
        assignment = self.record("assignment.json", self.assignment)
        self.selection.update(assignment_sha256=assignment["sha256"], consultation=cp["selector"])
        selection = self.record("selection.json", self.selection)
        package = self.record("package.json", self.package)
        self.graph.update(native_graph=self.file("native-graph.json", canonical_bytes(self.raw_graph)), default_ui_readback=self.record("ui.json", self.ui))
        graph = self.record("graph.json", self.graph)
        self.review.update(assignment_sha256=assignment["sha256"], package_sha256=package["sha256"], consultation=cp["reviewer"], graph_sha256=graph["sha256"], graph_requirements=self.requirements)
        review = self.record("review.json", self.review)
        self.release.update(action=self.action, assignment_sha256=assignment["sha256"], selection_sha256=selection["sha256"], review_sha256=review["sha256"], package=package, graph=graph)
        release = self.record("release.json", self.release)
        self.authority = {"mission": self.mission, "basis": self.basis, "assignment": assignment, "selection": selection, "review": review, "release": release, "mission_id": "private-id", "publisher_id": "publisher", "manager_id": "manager", "reviewers": {"selection": "selector", "proof": "reviewer"}, "approved_inputs": {"B05": self.basis}, "allowed_actions": list(self.review["allowed_actions"]), "mission_scope_sha256": digest(b"mission semantic scope"), "basis_scope_sha256": digest(b"basis semantic scope"), "conclusion_sha256": digest(b"Exact selected conclusion."), "full_mission_conclusion_sha256": digest(b"Exact selected conclusion."), "max_graph_age_seconds": 3600}
        return self.record("authorization.json", self.authority)

    def kwargs(self):
        return dict(action=self.action, method=self.request["method"], path=self.request["path"], payload=self.payload, content_type=self.request["content_type"])


class GateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.f = Fixture(self.temp.name)

    def invoke(self, pin=None, *, clock=None, kwargs=None):
        self.calls = []
        def callback(*args):
            self.calls.append(args)
            return "simulated mutation"
        publisher = GuardedPrivatePublisher(pin or self.f.freeze(), "publisher", callback, clock=clock or (lambda: NOW))
        return publisher.mutate(**(kwargs or self.f.kwargs()))

    def rejected(self, code=None, pin=None, **kwargs):
        with self.assertRaises(GateRejected) as caught:
            self.invoke(pin, **kwargs)
        self.assertEqual(self.calls, [], "Mutation callback must never be entered")
        if code:
            self.assertEqual(caught.exception.code, code)

    def test_alternate_media_types_cannot_bypass_privacy(self):
        for route, media in (("/missions/private-id", "application/merge-patch+json"),
                             ("/submit-problem", "application/vnd.api+json"),
                             ("/submit-definition", "text/plain"),
                             ("/submit-problem", "multipart/form-data; boundary=x")):
            with self.subTest(route=route, media=media), tempfile.TemporaryDirectory() as folder:
                self.f = Fixture(folder)
                self.f.payload = b'{"private":false,"visibility":"public"}'
                self.f.request.update(path=route, content_type=media, body_sha256=digest(self.f.payload))
                self.rejected("unsupported_mutation_media_type")

    def test_reviewed_verify_multipart_remains_supported(self):
        self.f.payload = b'--x\r\nContent-Disposition: form-data; name="file"\r\n\r\nexact reviewed proof\r\n--x--\r\n'
        self.f.request.update(method="POST", path="/verify", content_type="multipart/form-data; boundary=x", body_sha256=digest(self.f.payload))
        self.assertEqual(self.invoke(), "simulated mutation")

    def configure_milestone_delete(self):
        self.f.action = "private_stage"
        self.f.payload = b"{}"
        self.f.request.update(method="DELETE", path="/milestones/9a54f1bf-66eb-4f87-9c57-3cca8b584baf",
                              body_sha256=digest(self.f.payload))

    def test_reviewed_milestone_delete_sends_exactly_once(self):
        self.configure_milestone_delete()
        self.assertEqual(self.invoke(), "simulated mutation")
        self.assertEqual(self.calls, [("DELETE", self.f.request["path"], b"{}", "application/json")])

    def test_even_reviewed_delete_rejects_other_routes(self):
        for route in ("/theorems/9a54f1bf-66eb-4f87-9c57-3cca8b584baf", "/missions/private-id",
                      "/milestones/not-a-uuid", "/milestones", "/milestones/9a54f1bf-66eb-4f87-9c57-3cca8b584baf/history",
                      "/milestones/9a54f1bf-66eb-4f87-9c57-3cca8b584baf?x=1"):
            with self.subTest(route=route):
                self.configure_milestone_delete()
                self.f.request["path"] = route
                self.rejected("invalid_mutation_route")

    def test_milestone_delete_rejects_nonempty_or_unreviewed_body(self):
        self.configure_milestone_delete()
        self.f.payload = b'{"theorem_id":"other"}'
        self.f.request["body_sha256"] = digest(self.f.payload)
        self.rejected("milestone_delete_requires_empty_object")

    def test_milestone_delete_cannot_promote_a_claim(self):
        self.configure_milestone_delete()
        self.f.action = "foundation_promote"
        self.rejected("milestone_delete_requires_private_stage")

    def test_milestone_delete_rejects_changed_uuid_and_expiry(self):
        self.configure_milestone_delete()
        pin = self.f.freeze()
        args = self.f.kwargs()
        args["path"] = "/milestones/00000000-0000-0000-0000-000000000000"
        self.rejected("exact_request_mismatch", pin, kwargs=args)
        self.rejected(pin=pin, clock=lambda: NOW + timedelta(minutes=2))

    def test_positive_boundary_invokes_exact_bytes_once(self):
        self.assertEqual(self.invoke(), "simulated mutation")
        self.assertEqual(self.calls, [("PATCH", "/missions/private-id", self.f.payload, "application/json")])

    def test_changed_or_weakened_input_is_rejected(self):
        pin = self.f.freeze()
        Path(self.f.basis["path"]).write_text("pointwise positivity instead of uniform floor")
        self.rejected("stale_evidence_pin", pin)

    def test_stale_source_proof_package_and_review_are_rejected(self):
        for key in ("paper", "code", "proof"):
            with self.subTest(key=key), tempfile.TemporaryDirectory() as folder:
                self.f = Fixture(folder)
                pin = self.f.freeze()
                Path(getattr(self.f, key)["path"]).write_bytes(b"changed")
                self.rejected("stale_evidence_pin", pin)
        for name in ("package.json", "assignment.json", "review.json", "selection.json", "release.json", "mission.md"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as folder:
                self.f = Fixture(folder)
                pin = self.f.freeze()
                (Path(folder)/name).write_bytes(b"changed")
                self.rejected("stale_evidence_pin", pin)

    def test_assumed_output_is_rejected(self):
        self.f.package["premises"][0].update(kind="approved_input", input_id="B05", suppliers=[], evidence=[self.f.basis])
        self.rejected("conclusion_assumed_as_premise")

    def test_missing_supplier_is_rejected(self):
        self.f.package["premises"][0]["suppliers"] = ["absent"]
        self.rejected("missing_supplier")

    def test_cycle_is_rejected(self):
        self.f.package["premises"][1].update(kind="derived", suppliers=["result"], evidence=[self.f.proof])
        self.rejected("circular_supplier")

    def test_unresolved_physical_leaf_blocks_promotion(self):
        self.f.package["premises"][1].update(kind="physical_assumption", disposition="Conditional supplied datum")
        self.rejected("unresolved_physical_leaf")

    def test_reviewed_conditional_staging_has_no_foundation_credit(self):
        self.f.action = "private_stage"
        self.f.package["premises"][1].update(kind="physical_assumption", disposition="Explicitly supplied and unresolved")
        self.f.review["foundation_closure_accepted"] = False
        pin = self.f.freeze()
        decision = validate_request(pin, publisher_id="publisher", now=NOW, **self.f.kwargs())
        self.assertFalse(decision.foundation_credit_permitted)
        self.assertFalse(decision.full_mission_completion_permitted)
        self.assertEqual(self.invoke(pin), "simulated mutation")

    def test_ordinary_math_has_reviewed_disposition_without_fake_input_id(self):
        node = self.f.package["premises"][1]
        node.update(kind="math_apparatus", evidence=[self.f.code], disposition="Ordinary mathematical apparatus, independently reviewed")
        node.pop("input_id")
        self.f.review["ordinary_disposition_ids"] = ["input"]
        self.assertEqual(self.invoke(), "simulated mutation")
        self.f.review["ordinary_disposition_ids"] = []
        self.rejected("ordinary_disposition_not_reviewed")

    def test_missing_paper_or_code_consultation(self):
        for person in ("manager", "author", "selector", "reviewer"):
            for kind in ("papers", "codebank"):
                with self.subTest(person=person, kind=kind), tempfile.TemporaryDirectory() as folder:
                    self.f = Fixture(folder)
                    self.f.consults[person][kind] = []
                    self.rejected("missing_paper_or_code_consultation")

    def test_late_prior_work_record(self):
        self.f.consults["reviewer"]["recorded_at"] = stamp(-1)
        self.rejected("consultation_not_saved_before_work")

    def test_selection_after_construction(self):
        self.f.selection["decided_at"] = stamp(-7)
        self.rejected("selection_after_construction")

    def test_self_review(self):
        self.f.review["reviewer_id"] = "author"
        self.rejected("review_not_independent")

    def test_wrong_commissioned_conclusion(self):
        self.f.assignment["conclusion"] = "A different easier conclusion."
        self.rejected("wrong_commissioned_conclusion")

    def test_changed_mission_scope(self):
        self.f.assignment["mission_scope_sha256"] = digest(b"weaker objective")
        self.rejected("changed_commissioned_scope")

    def test_positive_native_graph_and_full_scope_control(self):
        self.f.action = "full_mission_complete"
        self.f.assignment["scope"] = "full_mission"
        self.assertEqual(self.invoke(), "simulated mutation")

    def test_intermediate_cannot_complete_full_mission(self):
        self.f.action = "full_mission_complete"
        self.rejected("intermediate_is_not_full_mission")

    def test_missing_graph_edge(self):
        self.f.action = "native_graph_complete"
        self.f.raw_graph["edges"].pop()
        self.rejected("missing_native_graph_edges")

    def test_missing_graph_node(self):
        self.f.action = "native_graph_complete"
        self.f.raw_graph["nodes"].pop()
        self.rejected("dangling_native_edge")

    def test_deep_api_is_not_default_native_ui(self):
        self.f.action = "native_graph_complete"
        self.f.ui["native_default_view"] = False
        self.rejected("default_native_ui_not_evidenced")

    def test_default_ui_missing_edge(self):
        self.f.action = "native_graph_complete"
        self.f.ui["visible_edges"] = []
        self.rejected("native_default_ui_missing_dependencies")

    def test_graph_truncation(self):
        self.f.action = "native_graph_complete"
        self.f.raw_graph["nodes"][0]["has_more_children"] = True
        self.rejected("native_graph_truncated")

    def test_expired_release(self):
        self.f.release["expires_at"] = NOW.isoformat()
        self.rejected("expired_or_future_release")

    def test_release_expires_between_validation_and_callback(self):
        times = iter([NOW, NOW + timedelta(minutes=2)])
        self.rejected("release_expired_before_mutation", clock=lambda: next(times))

    def test_different_payload_and_route(self):
        for key, value in (("payload", b"unreviewed bytes"), ("path", "/missions/other")):
            kw = self.f.kwargs()
            kw[key] = value
            self.rejected("mutation_mission_mismatch" if key == "path" else "exact_request_mismatch", kwargs=kw)

    def test_manager_cannot_replace_request_after_independent_review(self):
        self.f.release["request"] = {**self.f.request, "body_sha256": digest(b"different")}
        self.rejected("outgoing_request_not_independently_reviewed")

    def test_public_payload_denied_even_if_listed(self):
        self.f.payload = b'{"visibility":"public"}'
        self.f.request["body_sha256"] = digest(self.f.payload)
        self.rejected("public_mutation_forbidden")

    def test_four_axes_required_and_unchanged(self):
        self.f.release["evidence_axes"] = {**self.f.package["evidence_axes"], "foundation": "Unreviewed promotion"}
        self.rejected("evidence_axes_changed")

    def test_no_cached_permit_and_no_automatic_retry(self):
        pin = self.f.freeze()
        calls = []
        def callback(*args):
            calls.append(args)
            raise OSError("simulated uncertain transport")
        pub = GuardedPrivatePublisher(pin, "publisher", callback, clock=lambda: NOW)
        with self.assertRaises(OSError):
            pub.mutate(**self.f.kwargs())
        self.assertEqual(len(calls), 1)
        Path(self.f.proof["path"]).write_bytes(b"changed between calls")
        with self.assertRaises(GateRejected):
            pub.mutate(**self.f.kwargs())
        self.assertEqual(len(calls), 1)

    def test_unpinned_live_operational_status_can_change(self):
        pin = self.f.freeze()
        (self.f.root/"ACTIVE_WORK_ORDER.json").write_text('{"status":"progress changed","remaining":4}')
        self.assertEqual(self.invoke(pin), "simulated mutation")

    def test_future_author_work_and_reading_rejected(self):
        self.f.assignment["constructed_after_utc"] = stamp(10)
        self.f.consults["author"]["recorded_at"] = stamp(9)
        self.rejected("incoherent_construction_freeze_review")

    def test_package_freeze_before_construction_rejected(self):
        self.f.package["frozen_at"] = stamp(-20)
        self.rejected("incoherent_construction_freeze_review")

    def test_proof_decision_before_construction_rejected(self):
        self.f.review["evaluation_started_at"] = stamp(-11)
        self.f.review["decided_at"] = stamp(-10)
        self.rejected("incoherent_construction_freeze_review")

    def test_proof_evaluation_before_construction_rejected(self):
        self.f.review["evaluation_started_at"] = stamp(-10)
        self.rejected("proof_evaluation_before_construction")

    def test_graph_observed_after_its_review_rejected(self):
        self.f.action = "native_graph_complete"
        self.f.graph["observed_at"] = stamp(-1)
        self.f.ui["observed_at"] = stamp(-1)
        self.rejected("graph_observed_after_review")

    def test_ui_observed_after_its_review_rejected(self):
        self.f.action = "native_graph_complete"
        self.f.ui["observed_at"] = stamp(-1)
        self.rejected("ui_observed_after_review_or_invalid_time")

    def test_ambiguous_routes_rejected_before_callback(self):
        routes = ["/submit-problem?trace=1", "/missions/private-id/../../missions/other",
                  "/missions/private-id/%2e%2e/other", "/missions/private-id#fragment",
                  "/missions//private-id", "/missions/private-id\\other", "/missions/private-id\n"]
        for path in routes:
            with self.subTest(path=path), tempfile.TemporaryDirectory() as folder:
                self.f = Fixture(folder)
                self.f.request["path"] = path
                self.rejected("noncanonical_mutation_route")

    def test_manager_record_after_assignment(self):
        self.f.consults["manager"]["recorded_at"] = stamp(-14)
        self.rejected("consultation_not_saved_before_work")

    def test_assignment_after_selection_started(self):
        self.f.assignment["assigned_at"] = stamp(-10)
        self.rejected("assignment_after_selection_started")

    def test_wrong_manager(self):
        self.f.assignment["manager_id"] = "untrusted-manager"
        self.rejected("wrong_assignment_manager")

    def test_missing_work_type_or_intended_addition(self):
        for field in ("work_type", "intended_addition"):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as folder:
                self.f = Fixture(folder)
                self.f.assignment[field] = ""
                self.rejected("missing_work_type_or_intended_addition")

    def test_work_type_and_addition_must_match_both_reviews(self):
        for role in ("selection", "review"):
            for field in ("work_type", "intended_addition"):
                with self.subTest(role=role, field=field), tempfile.TemporaryDirectory() as folder:
                    self.f = Fixture(folder)
                    getattr(self.f, role)[field] = "Different work"
                    self.rejected("work_type_or_addition_review_mismatch")

    def test_missing_proof_evidence(self):
        self.f.review["proof_evidence"] = []
        self.rejected("missing_proof_review_evidence")

    def test_native_extra_dependency_requires_review(self):
        self.f.action = "native_graph_complete"
        self.f.raw_graph["nodes"].append({"node_type": "theorem", "theorem_id": "unexpected", "status": "Proved"})
        self.f.raw_graph["edges"].append({"source": "native-result", "target": "unexpected", "kind": "structural"})
        self.rejected("unreviewed_native_dependency")

    def test_native_cycle_rejected_even_when_expected(self):
        self.f.action = "native_graph_complete"
        edge = {"source": "native-input", "target": "native-result", "kind": "structural"}
        self.f.raw_graph["edges"].append(edge)
        self.f.requirements["edges"].append([edge["source"], edge["target"], edge["kind"]])
        self.rejected("circular_native_dependency")

    def test_stale_graph_readback(self):
        self.f.action = "native_graph_complete"
        self.f.graph["observed_at"] = stamp(-120)
        self.rejected("stale_graph_readback")

    def test_native_unproved_supplier(self):
        self.f.action = "native_graph_complete"
        self.f.raw_graph["nodes"][0]["status"] = "Open"
        self.rejected("native_proof_not_accepted")

    def test_graph_readback_is_actual_native_route(self):
        self.f.action = "native_graph_complete"
        self.f.graph["request"]["path"] = "/inventories"
        self.rejected("not_native_graph_readback")

    def test_private_registration_requires_explicit_flag(self):
        self.f.request["path"] = "/submit-problem"
        self.rejected("registration_private_flag_required")

    def test_approved_input_label_cannot_be_replaced(self):
        self.f.package["premises"][1]["input_id"] = "FAKE"
        self.rejected("unapproved_or_weakened_input")

    def test_missing_schema_fields_fail_closed(self):
        self.f.review.pop("source_fidelity_accepted")
        self.rejected("malformed_or_unavailable_evidence")

    def test_conclusion_inventory_must_be_independently_accepted(self):
        self.f.review["accepted_premise_ids"] = ["result"]
        self.rejected("premise_inventory_review_mismatch")

    def test_refresh_admin_authority_preserves_frozen_math(self):
        first = self.f.freeze()
        original_assignment = self.f.authority["assignment"]
        original_review = self.f.authority["review"]
        self.f.mission = self.f.file("mission.md", b"Authorized administrative clarification; same commissioned content")
        self.rejected("stale_evidence_pin", first)
        refreshed = self.f.freeze()
        self.assertEqual(original_assignment, self.f.authority["assignment"])
        self.assertEqual(original_review, self.f.authority["review"])
        self.assertEqual(self.invoke(refreshed), "simulated mutation")

    def test_untrusted_authority_change_missing_evidence_and_malformed_json(self):
        pin = self.f.freeze()
        Path(pin["path"]).write_bytes(b"changed trusted authorization")
        self.rejected("stale_evidence_pin", pin)
        pin = self.f.freeze()
        Path(self.f.proof["path"]).unlink()
        self.rejected("malformed_or_unavailable_evidence", pin)

    def test_duplicate_json_keys_fail_closed(self):
        pin = self.f.freeze()
        raw = b'{"evidence_gate":{},"evidence_gate":{}}'
        pin = self.f.file("authorization.json", raw)
        self.rejected("duplicate_json_key", pin)


if __name__ == "__main__":
    unittest.main()
