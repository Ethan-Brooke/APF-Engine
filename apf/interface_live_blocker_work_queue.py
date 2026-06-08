"""
APF Interface Live Blocker Work Queue.

Sandbox sprint layer for the v24.3.18 Interface Engine live blockers.

Purpose
-------
The operational Interface Engine already reports the live missing structures:

    EW route   : EVALUATOR_MAP, EXTERNAL_CONSTANT, COUNTERTERM, UNCERTAINTY_PROTOCOL
    Dark route : EVALUATOR_MAP, EMPIRICAL_POSTERIOR

This module turns those typed missing structures into first-class repair work items:

    missing movement edge
      -> route work item
      -> evidence slots
      -> acceptance criteria
      -> rerun command
      -> no-promotion guard

Boundary
--------
This module does not supply the missing evidence and does not promote either route.
It is an operational queue and verifier for the next evidence-acquisition sprint.

Top check:
    check_T_interface_live_blocker_work_queue_P
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, replace
from enum import Enum
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple, List
from functools import lru_cache
import csv
import json
from pathlib import Path

try:
    from apf.ew_trace_to_scheme_real_adapter import build_live_adapter_report as build_live_ew_report
    from apf.dark_posterior_real_adapter import build_live_adapter_report as build_live_dark_report
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_live_blocker_work_queue requires live adapters: {exc}") from exc

try:
    from apf.interface_ew_counterterm_uncertainty_intake import status_by_task_id as ew_intake_status_by_task_id
except Exception:  # pragma: no cover
    ew_intake_status_by_task_id = None

try:
    from apf.interface_dark_posterior_evidence_intake import status_by_task_id as dark_intake_status_by_task_id
except Exception:  # pragma: no cover
    dark_intake_status_by_task_id = None


class WorkItemStatus(str, Enum):
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"
    CANDIDATE_EVIDENCE_PRESENT = "CANDIDATE_EVIDENCE_PRESENT"
    READY_TO_RERUN = "READY_TO_RERUN"
    CLOSED_BY_RERUN = "CLOSED_BY_RERUN"
    BLOCKED_BY_PROVENANCE = "BLOCKED_BY_PROVENANCE"


@dataclass(frozen=True)
class EvidenceRequirement:
    key: str
    description: str
    acceptance_criteria: str
    example_value: Any = "TODO"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LiveBlockerWorkItem:
    task_id: str
    route: str
    structure_kind: str
    structure_name: str
    source: str
    target: str
    status: WorkItemStatus
    backing_fields: Tuple[str, ...]
    evidence_requirements: Tuple[EvidenceRequirement, ...]
    rerun_command: str
    acceptance_gate: str
    no_smuggling_guard: str
    detected_live_status: str = ""
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["evidence_requirements"] = [x.to_dict() for x in self.evidence_requirements]
        return data


@dataclass(frozen=True)
class LiveBlockerWorkQueue:
    version: str
    status: str
    items: Tuple[LiveBlockerWorkItem, ...]
    source_reports: Mapping[str, Any]
    summary: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "status": self.status,
            "items": [x.to_dict() for x in self.items],
            "source_reports": dict(self.source_reports),
            "summary": dict(self.summary),
        }


def _req(key: str, description: str, criteria: str, example: Any = "TODO") -> EvidenceRequirement:
    return EvidenceRequirement(key, description, criteria, example)


# These map structure-level blockers to the concrete route fields that must become true.
# They are deliberately conservative: evidence completeness only permits rerun; it does
# not certify that the rerun reaches global P.
EW_REQUIREMENT_MAP: Mapping[str, Tuple[Tuple[str, ...], Tuple[EvidenceRequirement, ...], str, str]] = {
    "EVALUATOR_MAP": (
        ("evaluator_map_found",),
        (
            _req("evaluator_definition", "Declare the EW APF_TRACE -> physical-scheme evaluator map.", "Must specify domain, codomain, input ledger, output object, invariants, and finite-part convention dependencies."),
            _req("evaluator_verifier", "Provide a verifier/check for the evaluator map.", "Must be a runnable script/check or banked theorem certificate that evaluates the map without target inversion."),
        ),
        "python scripts/run_first_real_ew_obligation.py",
        "EW evaluator map closes only if the rerun no longer reports EVALUATOR_MAP missing and target_value_consumed remains false.",
    ),
    "EXTERNAL_CONSTANT": (
        ("external_constants_ledger_clean",),
        (
            _req("constants_ledger_source", "Provide the external constants ledger source/provenance.", "Must name constants, source document/version, uncertainty, codomain role, and why the value is exogenous rather than a fitted target."),
            _req("constants_no_target_leakage", "Certify no physical target/posterior/fitted value is used as an input.", "Must explicitly list forbidden targets and show none appear in evaluator inputs."),
        ),
        "python scripts/run_first_real_ew_obligation.py",
        "External constants close only if the ledger is clean and does not consume the EW target as input.",
    ),
    "COUNTERTERM": (
        ("counterterm_finite_parts_declared",),
        (
            _req("counterterm_scheme", "Declare counterterm and finite-part scheme.", "Must specify finite part, subtraction prescription, scale, diagram-class content, and matching/counterterm convention."),
            _req("counterterm_verifier", "Provide a counterterm finite-part verifier.", "Must check all declared slots and fail closed on fitted/target-derived counterterms."),
        ),
        "python scripts/run_first_real_ew_obligation.py",
        "Counterterm evidence closes only if finite-part slots are declared before rerun and no fitted counterterm is consumed.",
    ),
    "UNCERTAINTY_PROTOCOL": (
        ("uncertainty_protocol_declared",),
        (
            _req("uncertainty_model", "Declare uncertainty propagation protocol.", "Must state covariance/truncation/source uncertainty propagation from route input to comparison object."),
            _req("comparison_rule", "Declare comparison rule.", "Must define the comparison statistic and acceptance threshold without inverse-fitting the observed target."),
        ),
        "python scripts/run_first_real_ew_obligation.py",
        "Uncertainty protocol closes only if the comparison protocol is declared and rerun remains provenance-clean.",
    ),
}

DARK_REQUIREMENT_MAP: Mapping[str, Tuple[Tuple[str, ...], Tuple[EvidenceRequirement, ...], str, str]] = {
    "EVALUATOR_MAP": (
        ("evaluator_map_found", "posterior_closed", "robustness_checks_passed"),
        (
            _req("posterior_evaluator_definition", "Declare the dark posterior evaluator map.", "Must specify data inputs, model outputs, posterior object, convergence diagnostics, robustness matrix, and export criterion."),
            _req("posterior_evaluator_verifier", "Provide a verifier/check for the posterior evaluator.", "Must be runnable and must fail closed if posterior/best-fit outputs are used as inputs."),
        ),
        "python scripts/run_first_real_dark_obligation.py",
        "Dark evaluator map closes only when posterior closure and robustness evidence jointly make evaluator_map_found true after rerun.",
    ),
    "EMPIRICAL_POSTERIOR": (
        ("posterior_closed", "chains_converged", "robustness_checks_passed"),
        (
            _req("posterior_summary", "Provide posterior closure summary.", "Must include posterior artifacts, chains/profile evidence, closure criterion, and the exact route/model configuration."),
            _req("posterior_repro_command", "Provide a reproducible posterior command/config hash/path.", "Must include enough command/config/provenance data to rerun the posterior without consuming the posterior as an input."),
            _req("robustness_matrix", "Provide robustness checks.", "Must list perturbations, SN/BAO/CMB/growth variants as applicable, pass/fail status, and known environmental blockers."),
        ),
        "python scripts/run_first_real_dark_obligation.py",
        "Empirical posterior closes only if posterior and robustness evidence survive rerun and no posterior output is consumed as an input.",
    ),
}

NO_SMUGGLING_GUARD = (
    "Evidence completeness is permission to rerun only. The route must still fail closed if a target, fitted output, "
    "posterior output, or comparator residual is consumed as an evaluator input."
)


def _movement_edges(report: Mapping[str, Any]) -> Tuple[Mapping[str, Any], ...]:
    movement = report.get("movement_graph", {})
    return tuple(movement.get("edges", ()))


def _missing_edges(report: Mapping[str, Any]) -> Tuple[Mapping[str, Any], ...]:
    movement = report.get("movement_graph", {})
    return tuple(movement.get("missing_or_blocked_edges", ()))


def _edge_status_to_work_status(edge_status: str) -> WorkItemStatus:
    if edge_status in {"PRESENT_STABLE", "MOVES_CLEANLY"}:
        return WorkItemStatus.CANDIDATE_EVIDENCE_PRESENT
    return WorkItemStatus.OPEN_EVIDENCE_REQUIRED


def _item_from_edge(route: str, edge: Mapping[str, Any]) -> Optional[LiveBlockerWorkItem]:
    kind = str(edge.get("kind", ""))
    mapping = EW_REQUIREMENT_MAP if route == "EW" else DARK_REQUIREMENT_MAP
    if kind not in mapping:
        return None
    backing_fields, reqs, rerun, gate = mapping[kind]
    live_status = str(edge.get("status", ""))
    work_status = _edge_status_to_work_status(live_status)
    return LiveBlockerWorkItem(
        task_id=f"{route}_{kind}",
        route=route,
        structure_kind=kind,
        structure_name=str(edge.get("structure_name", kind)),
        source=str(edge.get("source", "")),
        target=str(edge.get("target", "")),
        status=work_status,
        backing_fields=tuple(backing_fields),
        evidence_requirements=tuple(reqs),
        rerun_command=rerun,
        acceptance_gate=gate,
        no_smuggling_guard=NO_SMUGGLING_GUARD,
        detected_live_status=live_status,
        notes=(
            f"Generated from live movement edge {edge.get('edge_id', 'unknown')}. "
            + ("Candidate evidence is present in the live probe; keep as a queue item until the full route rerun closes." if work_status == WorkItemStatus.CANDIDATE_EVIDENCE_PRESENT else "Evidence still required before rerun can close this structure.")
        ),
    )


@lru_cache(maxsize=1)
def build_live_blocker_work_queue() -> LiveBlockerWorkQueue:
    ew_report = build_live_ew_report(name="EW_live_blocker_work_queue").to_dict()
    dark_report = build_live_dark_report(name="DARK_live_blocker_work_queue").to_dict()

    items: List[LiveBlockerWorkItem] = []
    # Keep all target structures in the queue, even when a live probe now supplies
    # candidate evidence.  This preserves the user-facing work list while making
    # progress visible (e.g. EW_EXTERNAL_CONSTANT can move from missing to candidate-present).
    for edge in _movement_edges(ew_report):
        item = _item_from_edge("EW", edge)
        if item is not None:
            items.append(item)
    for edge in _movement_edges(dark_report):
        item = _item_from_edge("DARK", edge)
        if item is not None:
            items.append(item)

    # Evidence-intake modules can surface candidate evidence while leaving live
    # adapters held.  This updates the work queue's user-facing status without
    # changing route booleans or promoting routes.
    candidate_status: Dict[str, str] = {}
    if ew_intake_status_by_task_id is not None:
        try:
            candidate_status.update(ew_intake_status_by_task_id())
        except Exception:
            pass
    if dark_intake_status_by_task_id is not None:
        try:
            candidate_status.update(dark_intake_status_by_task_id())
        except Exception:
            pass
    if candidate_status:
        updated_items: List[LiveBlockerWorkItem] = []
        for item in items:
            if (
                item.task_id in candidate_status
                and candidate_status[item.task_id] == WorkItemStatus.CANDIDATE_EVIDENCE_PRESENT.value
                and item.status == WorkItemStatus.OPEN_EVIDENCE_REQUIRED
            ):
                updated_items.append(replace(
                    item,
                    status=WorkItemStatus.CANDIDATE_EVIDENCE_PRESENT,
                    detected_live_status=f"{item.detected_live_status}|EVIDENCE_INTAKE_CANDIDATE",
                    notes=item.notes + " Evidence-intake candidate is present; route remains held until explicit rerun/admission.",
                ))
            else:
                updated_items.append(item)
        items = updated_items

    by_route: Dict[str, int] = {}
    by_kind: Dict[str, int] = {}
    by_status: Dict[str, int] = {}
    for item_ in items:
        by_route[item_.route] = by_route.get(item_.route, 0) + 1
        by_kind[item_.structure_kind] = by_kind.get(item_.structure_kind, 0) + 1
        by_status[item_.status.value] = by_status.get(item_.status.value, 0) + 1

    summary = {
        "total_items": len(items),
        "open_items": by_status.get("OPEN_EVIDENCE_REQUIRED", 0),
        "candidate_evidence_present_items": by_status.get("CANDIDATE_EVIDENCE_PRESENT", 0),
        "by_route": by_route,
        "by_kind": by_kind,
        "by_status": by_status,
        "ready_to_rerun_items": 0,
        "closed_items": 0,
        "boundary": "This queue captures live blockers and candidate evidence; it does not promote routes.",
    }
    return LiveBlockerWorkQueue(
        version="APF_INTERFACE_LIVE_BLOCKER_WORK_QUEUE_v3",
        status="OPEN_EVIDENCE_REQUIRED",
        items=tuple(items),
        source_reports={
            "ew_payload": ew_report.get("payload", {}),
            "dark_payload": dark_report.get("payload", {}),
            "ew_edges": list(_movement_edges(ew_report)),
            "dark_edges": list(_movement_edges(dark_report)),
            "ew_missing_edges": list(_missing_edges(ew_report)),
            "dark_missing_edges": list(_missing_edges(dark_report)),
            "ew_packet_status": ew_report.get("obligation_packet", {}).get("packet_status"),
            "dark_packet_status": dark_report.get("obligation_packet", {}).get("packet_status"),
        },
        summary=summary,
    )


def evidence_template_for_queue(queue: Optional[LiveBlockerWorkQueue] = None) -> Dict[str, Any]:
    queue = queue or build_live_blocker_work_queue()
    return {
        item.task_id: {
            "status": item.status.value,
            "backing_fields": list(item.backing_fields),
            "evidence": {req.key: req.example_value for req in item.evidence_requirements},
            "acceptance_gate": item.acceptance_gate,
            "rerun_command": item.rerun_command,
            "no_smuggling_guard": item.no_smuggling_guard,
        }
        for item in queue.items
    }


def render_markdown(queue: Optional[LiveBlockerWorkQueue] = None) -> str:
    queue = queue or build_live_blocker_work_queue()
    lines = [
        "# APF Interface Live Blocker Work Queue v3",
        "",
        f"- Status: `{queue.status}`",
        f"- Total tracked items: `{queue.summary.get('total_items')}`",
        f"- Still open: `{queue.summary.get('open_items')}`",
        f"- Candidate evidence present: `{queue.summary.get('candidate_evidence_present_items')}`",
        "- Boundary: evidence completeness permits rerun only; it does not promote EW or dark routes.",
        "",
        "## Open work items",
        "",
        "| Task | Route | Structure | Status | Source → Target | Backing fields | Rerun |",
        "|---|---|---|---|---|---|---|",
    ]
    for item in queue.items:
        lines.append(
            f"| `{item.task_id}` | `{item.route}` | `{item.structure_kind}` | `{item.status.value}` | "
            f"{item.source} → {item.target} | `{', '.join(item.backing_fields)}` | `{item.rerun_command}` |"
        )
    lines += ["", "## Evidence requirements", ""]
    for item in queue.items:
        lines += [f"### `{item.task_id}` — {item.structure_name}", ""]
        lines.append(f"Acceptance gate: {item.acceptance_gate}")
        lines.append("")
        lines.append(f"No-smuggling guard: {item.no_smuggling_guard}")
        lines.append("")
        for req in item.evidence_requirements:
            lines.append(f"- `{req.key}`: {req.description} Criteria: {req.acceptance_criteria}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def export_work_queue(out_dir: str | Path) -> Dict[str, str]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    queue = build_live_blocker_work_queue()
    data = queue.to_dict()

    json_path = out / "LIVE_BLOCKER_WORK_QUEUE.json"
    template_path = out / "EVIDENCE_TEMPLATE.json"
    md_path = out / "README.md"
    csv_path = out / "live_blocker_work_queue.csv"

    json_path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")
    template_path.write_text(json.dumps(evidence_template_for_queue(queue), indent=2, default=str), encoding="utf-8")
    md_path.write_text(render_markdown(queue), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["task_id", "route", "structure_kind", "structure_name", "status", "detected_live_status", "backing_fields", "evidence_keys", "rerun_command"],
        )
        writer.writeheader()
        for item in queue.items:
            writer.writerow({
                "task_id": item.task_id,
                "route": item.route,
                "structure_kind": item.structure_kind,
                "structure_name": item.structure_name,
                "status": item.status.value,
                "detected_live_status": item.detected_live_status,
                "backing_fields": ";".join(item.backing_fields),
                "evidence_keys": ";".join(req.key for req in item.evidence_requirements),
                "rerun_command": item.rerun_command,
            })

    return {
        "json": str(json_path),
        "template": str(template_path),
        "markdown": str(md_path),
        "csv": str(csv_path),
    }


def check_T_live_blocker_inventory_P() -> Dict[str, Any]:
    queue = build_live_blocker_work_queue()
    ids = {item.task_id for item in queue.items}
    required = {
        "EW_EVALUATOR_MAP",
        "EW_EXTERNAL_CONSTANT",
        "EW_COUNTERTERM",
        "EW_UNCERTAINTY_PROTOCOL",
        "DARK_EVALUATOR_MAP",
        "DARK_EMPIRICAL_POSTERIOR",
    }
    tests = {
        "required_items_present": required.issubset(ids),
        "no_extra_unmapped_items": len(ids) == len(queue.items),
        "six_tracked_items": len(queue.items) == 6,
        "status_open": queue.status == "OPEN_EVIDENCE_REQUIRED",
        "external_constant_candidate_present": any(item.task_id == "EW_EXTERNAL_CONSTANT" and item.status == WorkItemStatus.CANDIDATE_EVIDENCE_PRESENT for item in queue.items),
        "dark_evaluator_candidate_present": any(item.task_id == "DARK_EVALUATOR_MAP" and item.status == WorkItemStatus.CANDIDATE_EVIDENCE_PRESENT for item in queue.items),
        "dark_posterior_still_open": any(item.task_id == "DARK_EMPIRICAL_POSTERIOR" and item.status == WorkItemStatus.OPEN_EVIDENCE_REQUIRED for item in queue.items),
        "counterterm_candidate_present": any(item.task_id == "EW_COUNTERTERM" and item.status == WorkItemStatus.CANDIDATE_EVIDENCE_PRESENT for item in queue.items),
        "uncertainty_candidate_present": any(item.task_id == "EW_UNCERTAINTY_PROTOCOL" and item.status == WorkItemStatus.CANDIDATE_EVIDENCE_PRESENT for item in queue.items),
    }
    return {
        "name": "check_T_live_blocker_inventory_P",
        "consistent": all(tests.values()),
        "status": "P_work_queue" if all(tests.values()) else "FAIL",
        "summary": "Live EW and dark target structures are captured as six explicit work-queue items, including EW and dark candidate-present evidence.",
        "data": {"tests": tests, "ids": sorted(ids), "summary": queue.summary},
    }


def check_T_work_items_have_evidence_requirements_P() -> Dict[str, Any]:
    queue = build_live_blocker_work_queue()
    tests = {
        "all_have_requirements": all(len(item.evidence_requirements) >= 2 for item in queue.items),
        "all_have_acceptance_gates": all(bool(item.acceptance_gate) for item in queue.items),
        "all_have_rerun_commands": all(item.rerun_command.startswith("python scripts/run_first_real_") for item in queue.items),
        "all_have_no_smuggling_guard": all("fail closed" in item.no_smuggling_guard.lower() for item in queue.items),
    }
    return {
        "name": "check_T_work_items_have_evidence_requirements_P",
        "consistent": all(tests.values()),
        "status": "P_work_queue" if all(tests.values()) else "FAIL",
        "summary": "Every live work item has evidence requirements, acceptance gate, rerun command, and no-smuggling guard.",
        "data": {"tests": tests},
        "dependencies": ["check_T_live_blocker_inventory_P"],
    }


def check_T_queue_does_not_promote_routes_P() -> Dict[str, Any]:
    queue = build_live_blocker_work_queue()
    template = evidence_template_for_queue(queue)
    tests = {
        "no_items_closed": all(item.status != WorkItemStatus.CLOSED_BY_RERUN for item in queue.items),
        "has_open_items": any(item.status == WorkItemStatus.OPEN_EVIDENCE_REQUIRED for item in queue.items),
        "ready_to_rerun_zero": queue.summary.get("ready_to_rerun_items") == 0,
        "closed_items_zero": queue.summary.get("closed_items") == 0,
        "template_is_todo": all(any(v == "TODO" for v in entry["evidence"].values()) for entry in template.values()),
    }
    return {
        "name": "check_T_queue_does_not_promote_routes_P",
        "consistent": all(tests.values()),
        "status": "P_work_queue" if all(tests.values()) else "FAIL",
        "summary": "Work queue is operational only: it creates evidence tasks but does not close or promote EW/dark routes.",
        "data": {"tests": tests},
        "dependencies": ["check_T_work_items_have_evidence_requirements_P"],
    }


def check_T_interface_live_blocker_work_queue_P() -> Dict[str, Any]:
    subchecks = [
        check_T_live_blocker_inventory_P(),
        check_T_work_items_have_evidence_requirements_P(),
        check_T_queue_does_not_promote_routes_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_interface_live_blocker_work_queue_P",
        "consistent": ok,
        "status": "P_work_queue" if ok else "FAIL",
        "summary": "Interface Live Blocker Work Queue v3 is P: live blockers are explicit evidence tasks, dark evaluator-map admission is visible, and no route is promoted by the queue.",
        "data": {"subchecks": [x["name"] for x in subchecks]},
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_live_blocker_inventory_P": check_T_live_blocker_inventory_P,
    "check_T_work_items_have_evidence_requirements_P": check_T_work_items_have_evidence_requirements_P,
    "check_T_queue_does_not_promote_routes_P": check_T_queue_does_not_promote_routes_P,
    "check_T_interface_live_blocker_work_queue_P": check_T_interface_live_blocker_work_queue_P,
}


def register(registry=None):
    if registry is None:
        return CHECKS
    if hasattr(registry, "update"):
        registry.update(CHECKS)
        return registry
    for name, fn in CHECKS.items():
        if hasattr(registry, "register"):
            registry.register(name, fn)
        elif hasattr(registry, "add"):
            registry.add(name, fn)
        else:
            raise TypeError("Unsupported registry type for interface_live_blocker_work_queue.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build/verify the APF live blocker work queue.")
    parser.add_argument("--out-dir", default=None, help="Optional output directory for queue artifacts.")
    parser.add_argument("--json", action="store_true", help="Print queue JSON instead of check summary.")
    args = parser.parse_args()

    if args.out_dir:
        paths = export_work_queue(args.out_dir)
        print(json.dumps({"exported": paths}, indent=2))
    elif args.json:
        print(json.dumps(build_live_blocker_work_queue().to_dict(), indent=2, default=str))
    else:
        results = run_all()
        print(json.dumps(results, indent=2, sort_keys=True, default=str))
        raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
