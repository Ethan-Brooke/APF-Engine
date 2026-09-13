"""Prospective APF evidence gate. Integrity/declared-closure checks, not physics certification.

The caller must obtain the authorization file's SHA256 through a trusted channel.
Never derive that anchor from the candidate release. Existing historical records
without this extension are untouched; they simply cannot authorize this entry point.
"""
from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

ACTIONS = frozenset({"private_stage", "foundation_promote", "native_graph_complete", "full_mission_complete"})
AXES = frozenset({"papers", "codebank", "machine_checked", "foundation"})
MAX_BYTES = 64 * 1024 * 1024


class GateRejected(ValueError):
    """No mutation is authorized when this exception is raised."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def require(ok: bool, code: str) -> None:
    if not ok:
        raise GateRejected(code)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate_json_key")
        result[key] = value
    return result


def _json(raw: bytes):
    return json.loads(raw.decode("utf-8-sig"), object_pairs_hook=_pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(GateRejected("nonfinite_json")))


def _time(value: str) -> datetime:
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(result.tzinfo is not None and result.utcoffset() is not None, "timezone_required")
    return result.astimezone(timezone.utc)


def _text(value: Any, code: str) -> str:
    require(isinstance(value, str) and bool(value.strip()), code)
    return value


def _pin(pin: Mapping[str, Any]) -> bytes:
    require(isinstance(pin, dict), "invalid_pin")
    require(set(pin) == {"path", "sha256"}, "invalid_pin_fields")
    require(isinstance(pin["sha256"], str) and re.fullmatch(r"[0-9a-f]{64}", pin["sha256"]) is not None, "invalid_digest")
    path = Path(pin["path"])
    require(path.is_absolute(), "absolute_pin_path_required")
    with path.open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    require(len(raw) <= MAX_BYTES, "evidence_too_large")
    require(digest(raw) == pin["sha256"], "stale_evidence_pin")
    return raw


def _record(pin):
    data = _json(_pin(pin))["evidence_gate"]
    require(type(data["schema_version"]) is int and data["schema_version"] == 1, "unsupported_schema")
    return data


def _axes(value):
    require(isinstance(value, dict) and set(value) == AXES, "four_evidence_axes_required")
    for item in value.values():
        _text(item, "empty_evidence_axis")


def _consult(pin, person, before, needed):
    data = _record(pin)
    require(data["person_id"] == person and data["status"] == "complete", "consultation_identity_or_status")
    require(_time(data["read_completed_at"]) <= _time(data["recorded_at"]) <= before, "consultation_not_saved_before_work")
    observed = set()
    for kind in ("papers", "codebank"):
        require(isinstance(data[kind], list) and bool(data[kind]), "missing_paper_or_code_consultation")
        for source in data[kind]:
            _pin(source)
            observed.add(source["sha256"])
    require(needed <= observed, "consumed_sources_not_consulted")


def _closure(package, review, authority, promotion):
    nodes = package["premises"]
    require(isinstance(nodes, list) and bool(nodes), "missing_premise_inventory")
    ids = [n["id"] for n in nodes]
    require(all(isinstance(i, str) and i for i in ids) and len(set(ids)) == len(ids), "duplicate_or_invalid_premise_id")
    by_id = dict(zip(ids, nodes))
    root = package["conclusion_id"]
    require(root in by_id and by_id[root]["kind"] == "derived", "conclusion_assumed_as_premise")
    require(set(review["accepted_premise_ids"]) == set(ids), "premise_inventory_review_mismatch")
    allowed = {"derived", "approved_input", "original_definition", "math_apparatus", "physical_assumption"}
    known_files = {p["sha256"] for p in package["files"]}
    states = {}

    def visit(key):
        require(key in by_id, "missing_supplier")
        require(states.get(key) != 1, "circular_supplier")
        if states.get(key) == 2:
            return
        states[key] = 1
        node = by_id[key]
        kind = node["kind"]
        require(kind in allowed, "unknown_premise_kind")
        suppliers = node["suppliers"]
        require(isinstance(suppliers, list) and len(set(suppliers)) == len(suppliers), "invalid_suppliers")
        evidence = node["evidence"]
        require(isinstance(evidence, list), "invalid_premise_evidence")
        for pin in evidence:
            _pin(pin)
            require(pin["sha256"] in known_files, "premise_evidence_outside_package")
        if kind == "derived":
            require(bool(evidence), "missing_derivation_evidence")
            if not suppliers:
                require(node.get("no_physical_premises_reviewed") is True and
                        key in review["ordinary_disposition_ids"], "missing_supplier")
        elif kind == "approved_input":
            require(not suppliers, "approved_input_has_supplier")
            approved = authority["approved_inputs"].get(node["input_id"])
            require(approved is not None and approved in evidence, "unapproved_or_weakened_input")
        elif kind in ("original_definition", "math_apparatus"):
            require(not suppliers and bool(evidence), "ordinary_disposition_evidence_required")
            require(key in review["ordinary_disposition_ids"] and bool(node["disposition"].strip()), "ordinary_disposition_not_reviewed")
        else:
            require(not promotion, "unresolved_physical_leaf")
            require(not suppliers and bool(node["disposition"].strip()), "conditional_leaf_disposition_required")
        for supplier in suppliers:
            visit(supplier)
        states[key] = 2

    visit(root)
    require(set(states) == set(ids), "unreachable_declared_premise")
    return by_id


def _graph(pin, review, authority, release, nodes, now):
    require(pin["sha256"] == review["graph_sha256"], "graph_not_independently_reviewed")
    envelope = _record(pin)
    require(envelope["mission_id"] == authority["mission_id"] and envelope["visibility"] == "private", "graph_mission_or_visibility")
    seen = _time(envelope["observed_at"])
    require(seen <= _time(review["decided_at"]), "graph_observed_after_review")
    age = (now - seen).total_seconds()
    limit = authority["max_graph_age_seconds"]
    require(type(limit) is int and 0 < limit <= 86400 and 0 <= age <= limit, "stale_graph_readback")
    raw_pin = envelope["native_graph"]
    raw = _json(_pin(raw_pin))
    expected = review["graph_requirements"]
    require(envelope["request"] == {"method": "GET", "path": "/theorems/" + expected["root_id"] + "/graph", "status": 200}, "not_native_graph_readback")
    require(raw.get("has_hidden_deprecated_sketches") is False and
            all(n.get("has_more_children", False) is False for n in raw["nodes"]), "native_graph_truncated")
    require(raw["root_id"] == expected["root_id"], "wrong_native_graph_root")
    ids = set()
    statuses = {}
    for node in raw["nodes"]:
        kind = node["node_type"]
        if kind in ("theorem", "definition"):
            key = node.get("theorem_id") or node.get("definition_id")
        elif kind == "sketch":
            # Native graph sketches are actual intermediates; never replace them
            # with fabricated direct theorem-to-theorem edges.
            key = node.get("node_id") or node.get("id")
            if key is None and node.get("sketch_id"):
                key = "sketch-" + node["sketch_id"]
        else:
            raise GateRejected("unknown_native_node_type")
        _text(key, "missing_native_node_id")
        require(key not in ids, "duplicate_native_node")
        ids.add(key)
        statuses[key] = node.get("status")
    edges = {(e["source"], e["target"], e["kind"]) for e in raw["edges"]}
    require(all(a in ids and b in ids and isinstance(k, str) and k for a, b, k in edges), "dangling_native_edge")
    required_nodes = set(expected["nodes"])
    required_edges = {tuple(e) for e in expected["edges"]}
    require(all(len(e) == 3 for e in required_edges), "invalid_required_native_edge")
    require(required_nodes <= ids and expected["root_id"] in required_nodes, "missing_native_graph_nodes")
    require(required_edges <= edges, "missing_native_graph_edges")
    adjacency = {key: set() for key in ids}
    for a, b, _ in edges:
        adjacency[a].add(b)
    reached = set()
    pending = [expected["root_id"]]
    while pending:
        key = pending.pop()
        if key not in reached:
            reached.add(key)
            pending.extend(adjacency[key])
    require(required_nodes <= reached, "disconnected_native_dependency")
    require(reached == required_nodes and
            {e for e in edges if e[0] in reached} == required_edges, "unreviewed_native_dependency")
    native_states = {}
    def acyclic(key):
        require(native_states.get(key) != 1, "circular_native_dependency")
        if native_states.get(key) == 2:
            return
        native_states[key] = 1
        for child in adjacency[key]:
            acyclic(child)
        native_states[key] = 2
    acyclic(expected["root_id"])
    accounted = {n.get("native_id") for n in nodes.values()} | set(review["ordinary_native_ids"])
    for raw_node in raw["nodes"]:
        if raw_node["node_type"] in ("theorem", "definition"):
            key = raw_node.get("theorem_id") or raw_node.get("definition_id")
            if key in required_nodes:
                require(key in accounted, "native_premise_not_accounted")
                require(raw_node.get("status") in ("Proved", "Definition"), "native_proof_not_accepted")
    for node in nodes.values():
        native = node.get("native_id")
        if node["kind"] in ("derived", "approved_input"):
            require(native in required_nodes, "missing_native_premise_identity")
        if native:
            require(native in required_nodes, "unreviewed_native_premise")
            if node["kind"] == "derived":
                require(statuses.get(native) == "Proved", "native_proof_not_accepted")
    require(nodes[release["conclusion_id"]]["native_id"] == expected["root_id"], "graph_root_conclusion_mismatch")
    # A deep API result does not establish what the ordinary native UI shows.
    ui = _record(envelope["default_ui_readback"])
    require(ui["mission_id"] == authority["mission_id"] and ui["native_default_view"] is True, "default_native_ui_not_evidenced")
    require(ui["reviewer_id"] == review["reviewer_id"] and ui["root_id"] == expected["root_id"], "ui_scope_or_reviewer_mismatch")
    _pin(ui["capture"])
    require(required_nodes <= set(ui["visible_nodes"]) and
            required_edges <= {tuple(e) for e in ui["visible_edges"]}, "native_default_ui_missing_dependencies")
    require(seen <= _time(ui["observed_at"]) <= _time(review["decided_at"]) <= now, "ui_observed_after_review_or_invalid_time")


@dataclass(frozen=True)
class Decision:
    action: str
    mission_id: str
    conclusion_id: str
    permitted_claim: str
    expires_at: datetime
    release_sha256: str
    foundation_credit_permitted: bool
    native_graph_completion_permitted: bool
    full_mission_completion_permitted: bool


def validate_request(authorization_pin, *, publisher_id: str, action: str,
                     method: str, path: str, payload: bytes, content_type: str,
                     now: datetime | None = None) -> Decision:
    """Validate a pinned authorization and exact request. Every error denies.

    Pin the immutable authorization independently of candidate data. This does
    not load/pin mutable live work-order status or budget fields. Re-authorizing
    administrative mission metadata is distinct from invalidating old proofs.
    """
    try:
        require(type(payload) is bytes, "immutable_payload_bytes_required")
        instant = now or datetime.now(timezone.utc)
        require(instant.tzinfo is not None, "timezone_required")
        auth = _record(authorization_pin)
        for key in ("mission", "basis"):
            _pin(auth[key])
        for pin in auth["approved_inputs"].values():
            _pin(pin)
        require(action in ACTIONS and action in auth["allowed_actions"], "action_not_authorized")
        require(publisher_id == auth["publisher_id"], "wrong_publisher")
        assignment = _record(auth["assignment"])
        selection = _record(auth["selection"])
        review = _record(auth["review"])
        release = _record(auth["release"])
        require(release["mission_id"] == auth["mission_id"], "wrong_mission")
        require(release["action"] == action and release["publisher_id"] == publisher_id, "release_action_or_publisher")
        require(release["private_only"] is True, "private_only_required")
        start, end = _time(release["not_before"]), _time(release["expires_at"])
        require(start <= instant < end, "expired_or_future_release")
        require(release["assignment_sha256"] == auth["assignment"]["sha256"] and
                release["selection_sha256"] == auth["selection"]["sha256"] and
                release["review_sha256"] == auth["review"]["sha256"], "release_evidence_mismatch")
        for key in ("mission_scope_sha256", "basis_scope_sha256"):
            require(assignment[key] == auth[key], "changed_commissioned_scope")
        conclusion = assignment["conclusion_id"]
        conclusion_hash = digest(assignment["conclusion"].encode("utf-8"))
        require(conclusion_hash == auth["conclusion_sha256"], "wrong_commissioned_conclusion")
        for item in (release, review):
            require(item["conclusion_id"] == conclusion and item["conclusion_sha256"] == conclusion_hash, "wrong_commissioned_conclusion")
        require(selection["assignment_sha256"] == auth["assignment"]["sha256"] and
                review["assignment_sha256"] == auth["assignment"]["sha256"], "wrong_reviewed_assignment")
        author = assignment["author_id"]
        require(assignment["manager_id"] == auth["manager_id"], "wrong_assignment_manager")
        assigned = _time(assignment["assigned_at"])
        require(assigned <= _time(selection["evaluation_started_at"]), "assignment_after_selection_started")
        for field in ("work_type", "intended_addition"):
            _text(assignment[field], "missing_work_type_or_intended_addition")
            require(selection[field] == assignment[field] == review[field], "work_type_or_addition_review_mismatch")
        for record, role in ((selection, "selection"), (review, "proof")):
            require(record["accepted"] is True and record["author_id"] == author, "review_not_accepted")
            require(record["reviewer_id"] != author and record["reviewer_id"] == auth["reviewers"][role], "review_not_independent")
            require(_time(record["evaluation_started_at"]) <= _time(record["decided_at"]) <= start, "invalid_review_chronology")
        require(_time(selection["decided_at"]) <= _time(assignment["constructed_after_utc"]), "selection_after_construction")
        package = _record(release["package"])
        require(release["package"]["sha256"] == review["package_sha256"], "wrong_reviewed_package")
        require(package["conclusion_id"] == conclusion, "wrong_package_conclusion")
        construction = _time(assignment["constructed_after_utc"])
        require(construction <= _time(package["frozen_at"]) <= _time(review["decided_at"]), "incoherent_construction_freeze_review")
        require(construction <= _time(review["evaluation_started_at"]), "proof_evaluation_before_construction")
        require(isinstance(package["files"], list) and bool(package["files"]), "empty_package")
        for pin in package["files"]:
            _pin(pin)
        needed = set()
        for kind in ("papers", "codebank"):
            require(isinstance(package["sources"][kind], list) and bool(package["sources"][kind]), "missing_consumed_sources")
            for pin in package["sources"][kind]:
                _pin(pin)
                needed.add(pin["sha256"])
        _consult(assignment["manager_consultation"], auth["manager_id"], assigned, needed)
        _consult(assignment["author_consultation"], author, _time(assignment["constructed_after_utc"]), needed)
        for record in (selection, review):
            _consult(record["consultation"], record["reviewer_id"], _time(record["evaluation_started_at"]), needed)
        require(review["source_fidelity_accepted"] is True and review["premise_inventory_complete"] is True, "source_or_premise_review_missing")
        require(review["proof_verdict"] in ("accepted", "not_applicable"), "proof_not_accepted")
        require(action in review["allowed_actions"] and release["permitted_claim"] == review["permitted_claim"], "unreviewed_action_or_claim")
        for item in (package, review, release):
            _axes(item["evidence_axes"])
        require(package["evidence_axes"] == review["evidence_axes"] == release["evidence_axes"], "evidence_axes_changed")
        promotion = action != "private_stage"
        if promotion:
            require(review["proof_verdict"] == "accepted" and review["machine_checked"] is True and
                    review["foundation_closure_accepted"] is True and review["objective_complete"] is True, "promotion_review_incomplete")
        if review["proof_verdict"] == "accepted":
            proof_pins = review["proof_evidence"]
            require(isinstance(proof_pins, list) and bool(proof_pins), "missing_proof_review_evidence")
            for pin in proof_pins:
                _pin(pin)
                require(pin in package["files"], "proof_evidence_outside_package")
        nodes = _closure(package, review, auth, promotion)
        if action == "full_mission_complete":
            require(assignment["scope"] == "full_mission" and
                    conclusion_hash == auth["full_mission_conclusion_sha256"], "intermediate_is_not_full_mission")
        if action in ("native_graph_complete", "full_mission_complete"):
            _graph(release["graph"], review, auth, release, nodes, instant)
        request = release["request"]
        require(request in review["accepted_requests"], "outgoing_request_not_independently_reviewed")
        milestone_delete = (method == "DELETE" and isinstance(path, str) and
                            re.fullmatch(r"/milestones/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", path) is not None)
        require(method in ("POST", "PUT", "PATCH") or milestone_delete, "invalid_mutation_route")
        if milestone_delete:
            require(action == "private_stage", "milestone_delete_requires_private_stage")
            require(payload == b"{}" and content_type == "application/json",
                    "milestone_delete_requires_empty_object")
        # Supported mutation endpoints use plain ASCII route segments. Queries,
        # escapes, dot segments, fragments and backslashes require a separately
        # reviewed adapter; never apply policy to an ambiguous literal string.
        require(isinstance(path, str) and re.fullmatch(r"/[A-Za-z0-9_-]+(?:/[A-Za-z0-9_-]+)*", path) is not None,
                "noncanonical_mutation_route")
        if path.startswith("/missions/"):
            require(path.split("/", 3)[2].split("?", 1)[0] == auth["mission_id"], "mutation_mission_mismatch")
        require(request == {"method": method, "path": path, "content_type": content_type,
                            "body_sha256": digest(payload)}, "exact_request_mismatch")
        media_type = content_type.split(";", 1)[0].strip().lower()
        require(media_type == "application/json" or
                (path == "/verify" and media_type == "multipart/form-data"),
                "unsupported_mutation_media_type")
        if media_type == "application/json":
            body = _json(payload)
            require(isinstance(body, dict), "json_mutation_object_required")
            require(body.get("mission_id", auth["mission_id"]) == auth["mission_id"], "mutation_mission_mismatch")
            require(body.get("private", True) is True and body.get("visibility", "private") == "private" and
                    body.get("public_release", False) is False, "public_mutation_forbidden")
            if path in ("/submit-problem", "/submit-definition"):
                require(body.get("private") is True, "registration_private_flag_required")
        return Decision(action, auth["mission_id"], conclusion, review["permitted_claim"], end,
                        auth["release"]["sha256"], promotion,
                        action in ("native_graph_complete", "full_mission_complete"),
                        action == "full_mission_complete")
    except GateRejected:
        raise
    except (KeyError, TypeError, ValueError, OSError, RecursionError, OverflowError, AttributeError) as exc:
        raise GateRejected("malformed_or_unavailable_evidence") from exc
