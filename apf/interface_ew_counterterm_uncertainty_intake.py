"""
APF EW Counterterm + Uncertainty Evidence Intake.

Sandbox sprint layer following APF_INTERFACE_LIVE_BLOCKER_WORK_QUEUE_v1.

Purpose
-------
The live Interface Engine currently keeps the EW route held on two structures:

    COUNTERTERM
    UNCERTAINTY_PROTOCOL

The v24.3.18 tree already contains several W-trace modules that declare and verify
counterterm conventions, finite-part slots, uncertainty propagation, comparison rules,
and no-smuggling/export-lock guards.  This intake layer gathers those modules into a
single evidence-readiness packet.

Boundary
--------
This module does *not* patch the EW adapter's route booleans and does *not* promote the
EW route.  It marks the two structures as candidate evidence present in the work queue,
while preserving the live adapter's held-for-rerun state.  Route promotion still requires
an explicit rerun/admission step.

Top check:
    check_T_EW_counterterm_uncertainty_intake_P
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence, Tuple, List
import csv
import json

try:
    from apf.ew_trace_to_scheme_real_adapter import APFModuleProbe, probe_module, build_live_adapter_report
except Exception as exc:  # pragma: no cover
    raise ImportError(f"interface_ew_counterterm_uncertainty_intake requires EW real adapter: {exc}") from exc


class IntakeStatus(str, Enum):
    CANDIDATE_EVIDENCE_PRESENT = "CANDIDATE_EVIDENCE_PRESENT"
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"
    BLOCKED_BY_PROVENANCE = "BLOCKED_BY_PROVENANCE"


@dataclass(frozen=True)
class IntakeRequirement:
    key: str
    description: str
    satisfied_by: Tuple[str, ...]
    acceptance_criteria: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceIntakeItem:
    task_id: str
    route: str
    structure_kind: str
    status: IntakeStatus
    supporting_modules: Tuple[str, ...]
    required_fragments: Tuple[str, ...]
    satisfied_fragments: Tuple[str, ...]
    checks_total: int
    checks_passing: int
    required_modules_all_import: bool
    required_modules_all_pass: bool
    export_lock_preserved: bool
    no_target_smuggling_guard: bool
    live_adapter_field: str
    rerun_command: str
    acceptance_boundary: str
    requirements: Tuple[IntakeRequirement, ...]
    notes: str = ""

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        data["requirements"] = [r.to_dict() for r in self.requirements]
        return data


@dataclass(frozen=True)
class EWCountertermUncertaintyIntake:
    version: str
    status: str
    items: Tuple[EvidenceIntakeItem, ...]
    probes: Tuple[APFModuleProbe, ...]
    live_ew_missing: Tuple[str, ...]
    live_ew_packet_status: str
    summary: Mapping[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "status": self.status,
            "items": [x.to_dict() for x in self.items],
            "probes": [p.to_dict() for p in self.probes],
            "live_ew_missing": list(self.live_ew_missing),
            "live_ew_packet_status": self.live_ew_packet_status,
            "summary": dict(self.summary),
        }


COUNTERTERM_MODULES = (
    "apf.w_trace_counterterm_convention",
    "apf.w_trace_denner_sirlin_counterterm_functional",
    "apf.w_trace_denner_ward_identity_counterterm_import",
)

UNCERTAINTY_MODULES = (
    "apf.w_trace_uncertainty_propagation",
    "apf.w_trace_correlated_uncertainty_model",
    "apf.w_trace_multisource_delta_r_comparison",
    "apf.w_trace_delta_r_comparison_harness",
    "apf.w_trace_input_convention_stress_test",
)

COUNTERTERM_REQUIRED_FRAGMENTS = (
    "finite_part_normalization_declared",
    "maps_to_delta_r_ct_os_slot",
    "forbids_observed_w_input",
    "forbids_tuned_finite_counterterm",
    "numeric_values_still_unadmitted",
    "export_request_blocked",
    "open_gates_block",
    "no_full_native_claim",
)

UNCERTAINTY_REQUIRED_FRAGMENTS = (
    "schema_declared",
    "policy_blocks_export",
    "computes_sigma_delta_r",
    "rejects_observed_w_uncertainty_input",
    "no_physical_mass_exports",
    "comparison_blocks_export",
    "no_export",
    "bank_closure",
)


def _req(key: str, description: str, satisfied_by: Sequence[str], criteria: str) -> IntakeRequirement:
    return IntakeRequirement(key, description, tuple(satisfied_by), criteria)


def _probe_many(module_names: Iterable[str]) -> Tuple[APFModuleProbe, ...]:
    return tuple(probe_module(name) for name in module_names)


def _status_text(probes: Iterable[APFModuleProbe]) -> str:
    return "\n".join("\n".join(p.statuses) for p in probes).lower()


def _module_names(probes: Iterable[APFModuleProbe]) -> Tuple[str, ...]:
    return tuple(p.module_name for p in probes)


def _checks_total(probes: Iterable[APFModuleProbe]) -> int:
    return sum(int(p.check_count) for p in probes)


def _checks_passing(probes: Iterable[APFModuleProbe]) -> int:
    return sum(int(p.passing_count) for p in probes)


def _all_import(probes: Iterable[APFModuleProbe]) -> bool:
    return all(p.import_ok for p in probes)


def _all_pass(probes: Iterable[APFModuleProbe]) -> bool:
    return all(p.import_ok and p.check_count > 0 and p.passing_count == p.check_count and not p.errors for p in probes)


def _satisfied_fragments(probes: Iterable[APFModuleProbe], fragments: Iterable[str]) -> Tuple[str, ...]:
    text = _status_text(probes)
    return tuple(fragment for fragment in fragments if fragment.lower() in text)


def _has_fragment(probes: Iterable[APFModuleProbe], fragment: str) -> bool:
    return fragment.lower() in _status_text(probes)


def _live_missing() -> Tuple[Tuple[str, ...], str]:
    report = build_live_adapter_report(name="EW_counterterm_uncertainty_intake_live_probe").to_dict()
    missing = tuple(edge.get("kind", "") for edge in report.get("movement_graph", {}).get("missing_or_blocked_edges", ()))
    packet = str(report.get("obligation_packet", {}).get("packet_status", ""))
    return missing, packet


def _counterterm_item(probes: Tuple[APFModuleProbe, ...]) -> EvidenceIntakeItem:
    satisfied = _satisfied_fragments(probes, COUNTERTERM_REQUIRED_FRAGMENTS)
    all_import = _all_import(probes)
    all_pass = _all_pass(probes)
    no_target = all(
        any(fragment in _status_text(probes) for fragment in group)
        for group in (
            ("forbids_observed_w_input", "comparison_blocks_observed_w"),
            ("forbids_world_average_input", "world_average"),
            ("forbids_apf_anchor_backsolve", "comparison_blocks_apf_input"),
            ("forbids_residual_fit", "posthoc_residual_fit"),
            ("forbids_tuned_finite_counterterm", "no_fit_admitted", "forbids_target_derivation"),
        )
    )
    # Export locks are expected here: this is evidence-intake readiness, not physical export.
    export_lock = all(
        any(fragment in _status_text(probes) for fragment in group)
        for group in (
            ("export_request_blocked", "export_candidate_preserved"),
            ("numeric_values_still_unadmitted", "counterterm_evaluator_gate_open"),
            ("no_full_native_claim", "open_gates_block", "forbids_full_closure"),
        )
    )
    ok = all_import and all_pass and len(satisfied) >= 6 and no_target and export_lock
    return EvidenceIntakeItem(
        task_id="EW_COUNTERTERM",
        route="EW",
        structure_kind="COUNTERTERM",
        status=IntakeStatus.CANDIDATE_EVIDENCE_PRESENT if ok else IntakeStatus.OPEN_EVIDENCE_REQUIRED,
        supporting_modules=_module_names(probes),
        required_fragments=COUNTERTERM_REQUIRED_FRAGMENTS,
        satisfied_fragments=satisfied,
        checks_total=_checks_total(probes),
        checks_passing=_checks_passing(probes),
        required_modules_all_import=all_import,
        required_modules_all_pass=all_pass,
        export_lock_preserved=export_lock,
        no_target_smuggling_guard=no_target,
        live_adapter_field="counterterm_finite_parts_declared",
        rerun_command="python scripts/run_first_real_ew_obligation.py",
        acceptance_boundary=(
            "Candidate evidence names finite-part/counterterm conventions and guards, but it does not by itself "
            "promote the EW route.  A route rerun/admission step must decide whether to set "
            "counterterm_finite_parts_declared=true."
        ),
        requirements=(
            _req("counterterm_scheme", "Finite-part/counterterm scheme declaration", ("apf.w_trace_counterterm_convention",), "Finite-part normalization, OS counterterm slot, and scheme family are declared."),
            _req("counterterm_functional", "Denner/Sirlin counterterm functional decomposition", ("apf.w_trace_denner_sirlin_counterterm_functional",), "Functional terms, master identity, open gate, and no-full-native-claim guards are present."),
            _req("counterterm_relation_import", "Ward-identity relation/family import", ("apf.w_trace_denner_ward_identity_counterterm_import",), "Counterterm families and open numeric gates are enumerated without target derivation or fit."),
        ),
        notes="Evidence-intake candidate for the EW counterterm live blocker; preserves export lock and no-smuggling guards.",
    )


def _uncertainty_item(probes: Tuple[APFModuleProbe, ...]) -> EvidenceIntakeItem:
    satisfied = _satisfied_fragments(probes, UNCERTAINTY_REQUIRED_FRAGMENTS)
    all_import = _all_import(probes)
    all_pass = _all_pass(probes)
    no_target = all(
        any(fragment in _status_text(probes) for fragment in group)
        for group in (
            ("rejects_observed_w_uncertainty_input", "comparison_blocks_observed_w"),
            ("rejects_apf_anchor_covariance_input", "comparison_blocks_apf_input"),
            ("forbidden_token_detected", "detects_bad_token"),
        )
    )
    export_lock = all(
        any(fragment in _status_text(probes) for fragment in group)
        for group in (
            ("policy_blocks_export", "manifest_remains_open"),
            ("no_physical_mass_exports", "no_export"),
            ("comparison_blocks_export", "verdict_is_not_export"),
        )
    )
    ok = all_import and all_pass and len(satisfied) >= 6 and no_target and export_lock
    return EvidenceIntakeItem(
        task_id="EW_UNCERTAINTY_PROTOCOL",
        route="EW",
        structure_kind="UNCERTAINTY_PROTOCOL",
        status=IntakeStatus.CANDIDATE_EVIDENCE_PRESENT if ok else IntakeStatus.OPEN_EVIDENCE_REQUIRED,
        supporting_modules=_module_names(probes),
        required_fragments=UNCERTAINTY_REQUIRED_FRAGMENTS,
        satisfied_fragments=satisfied,
        checks_total=_checks_total(probes),
        checks_passing=_checks_passing(probes),
        required_modules_all_import=all_import,
        required_modules_all_pass=all_pass,
        export_lock_preserved=export_lock,
        no_target_smuggling_guard=no_target,
        live_adapter_field="uncertainty_protocol_declared",
        rerun_command="python scripts/run_first_real_ew_obligation.py",
        acceptance_boundary=(
            "Candidate evidence names covariance/uncertainty mechanics and comparison guards, but it does not by itself "
            "promote the EW route.  A route rerun/admission step must decide whether to set "
            "uncertainty_protocol_declared=true."
        ),
        requirements=(
            _req("uncertainty_propagation", "Uncertainty propagation mechanics", ("apf.w_trace_uncertainty_propagation",), "Covariance shape, sigma propagation, and forbidden uncertainty inputs are checked."),
            _req("correlated_comparison", "Correlated multi-source comparison context", ("apf.w_trace_correlated_uncertainty_model", "apf.w_trace_multisource_delta_r_comparison"), "Comparison outputs are labeled non-export/context only."),
            _req("comparison_harness", "Comparison and input-convention stress harness", ("apf.w_trace_delta_r_comparison_harness", "apf.w_trace_input_convention_stress_test"), "Comparison blocks observed/APF target input and export requests."),
        ),
        notes="Evidence-intake candidate for the EW uncertainty-protocol live blocker; preserves export lock and no-smuggling guards.",
    )


@lru_cache(maxsize=1)
def build_ew_counterterm_uncertainty_intake() -> EWCountertermUncertaintyIntake:
    counterterm_probes = _probe_many(COUNTERTERM_MODULES)
    uncertainty_probes = _probe_many(UNCERTAINTY_MODULES)
    probes = counterterm_probes + uncertainty_probes
    items = (_counterterm_item(counterterm_probes), _uncertainty_item(uncertainty_probes))
    missing, packet = _live_missing()

    by_status: Dict[str, int] = {}
    for item in items:
        by_status[item.status.value] = by_status.get(item.status.value, 0) + 1
    summary = {
        "total_items": len(items),
        "candidate_evidence_present_items": by_status.get(IntakeStatus.CANDIDATE_EVIDENCE_PRESENT.value, 0),
        "open_items": by_status.get(IntakeStatus.OPEN_EVIDENCE_REQUIRED.value, 0),
        "checks_total": _checks_total(probes),
        "checks_passing": _checks_passing(probes),
        "by_status": by_status,
        "live_adapter_still_held": packet == "OPEN_EVIDENCE_REQUIRED" and set(missing).issubset({"COUNTERTERM", "UNCERTAINTY_PROTOCOL"}),
        "live_adapter_already_admitted": packet == "NOT_REQUIRED_ALREADY_P" and len(missing) == 0,
        "boundary": "Candidate evidence is surfaced; EW adapter may be held or already admitted by the imported-route evidence path.  No APF-internal full-loop/new-W claim is created here.",
    }
    if summary["candidate_evidence_present_items"] == 2 and summary["live_adapter_already_admitted"]:
        status = "CANDIDATE_EVIDENCE_PRESENT_ADMITTED_IMPORTED_ROUTE"
    elif summary["candidate_evidence_present_items"] == 2:
        status = "CANDIDATE_EVIDENCE_PRESENT_HELD_FOR_RERUN"
    else:
        status = "OPEN_EVIDENCE_REQUIRED"
    return EWCountertermUncertaintyIntake(
        version="APF_INTERFACE_EW_COUNTERTERM_UNCERTAINTY_INTAKE_v1",
        status=status,
        items=items,
        probes=probes,
        live_ew_missing=missing,
        live_ew_packet_status=packet,
        summary=summary,
    )


def status_by_task_id(intake: Optional[EWCountertermUncertaintyIntake] = None) -> Dict[str, str]:
    intake = intake or build_ew_counterterm_uncertainty_intake()
    return {item.task_id: item.status.value for item in intake.items}


def render_markdown(intake: Optional[EWCountertermUncertaintyIntake] = None) -> str:
    intake = intake or build_ew_counterterm_uncertainty_intake()
    lines = [
        "# APF EW Counterterm + Uncertainty Evidence Intake v1",
        "",
        f"- Status: `{intake.status}`",
        f"- Candidate evidence present: `{intake.summary.get('candidate_evidence_present_items')}` / `{intake.summary.get('total_items')}`",
        f"- Checks passing: `{intake.summary.get('checks_passing')}` / `{intake.summary.get('checks_total')}`",
        f"- Live EW adapter packet status: `{intake.live_ew_packet_status}`",
        f"- Live EW missing structures still reported: `{', '.join(intake.live_ew_missing)}`",
        "- Boundary: this intake surfaces candidate evidence; it does not patch route booleans or promote EW.",
        "",
        "## Intake items",
        "",
        "| Task | Status | Checks | Export lock | No-smuggling guard | Supporting modules |",
        "|---|---|---:|---|---|---|",
    ]
    for item in intake.items:
        lines.append(
            f"| `{item.task_id}` | `{item.status.value}` | {item.checks_passing}/{item.checks_total} | "
            f"{item.export_lock_preserved} | {item.no_target_smuggling_guard} | `{'; '.join(item.supporting_modules)}` |"
        )
    lines += ["", "## Admission boundary", ""]
    for item in intake.items:
        lines.append(f"### `{item.task_id}`")
        lines.append("")
        lines.append(item.acceptance_boundary)
        lines.append("")
        for req in item.requirements:
            lines.append(f"- `{req.key}`: {req.description}; satisfied by `{', '.join(req.satisfied_by)}`. Criteria: {req.acceptance_criteria}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def export_intake(out_dir: str | Path) -> Dict[str, str]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    intake = build_ew_counterterm_uncertainty_intake()

    json_path = out / "EW_COUNTERTERM_UNCERTAINTY_INTAKE.json"
    md_path = out / "README.md"
    csv_path = out / "ew_counterterm_uncertainty_intake.csv"
    template_path = out / "RERUN_ADMISSION_TEMPLATE.json"

    json_path.write_text(json.dumps(intake.to_dict(), indent=2, default=str), encoding="utf-8")
    md_path.write_text(render_markdown(intake), encoding="utf-8")
    template = {
        item.task_id: {
            "status": item.status.value,
            "live_adapter_field": item.live_adapter_field,
            "candidate_acceptance": False,
            "admission_note": "Set candidate_acceptance true only after route-owner admission; this intake does not auto-promote.",
            "rerun_command": item.rerun_command,
            "acceptance_boundary": item.acceptance_boundary,
            "supporting_modules": list(item.supporting_modules),
        }
        for item in intake.items
    }
    template_path.write_text(json.dumps(template, indent=2), encoding="utf-8")

    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["task_id", "status", "checks_total", "checks_passing", "export_lock_preserved", "no_target_smuggling_guard", "live_adapter_field", "supporting_modules"],
        )
        writer.writeheader()
        for item in intake.items:
            writer.writerow({
                "task_id": item.task_id,
                "status": item.status.value,
                "checks_total": item.checks_total,
                "checks_passing": item.checks_passing,
                "export_lock_preserved": item.export_lock_preserved,
                "no_target_smuggling_guard": item.no_target_smuggling_guard,
                "live_adapter_field": item.live_adapter_field,
                "supporting_modules": ";".join(item.supporting_modules),
            })

    return {
        "json": str(json_path),
        "markdown": str(md_path),
        "csv": str(csv_path),
        "rerun_admission_template": str(template_path),
    }


def check_T_EW_counterterm_evidence_candidate_P() -> Dict[str, Any]:
    intake = build_ew_counterterm_uncertainty_intake()
    item = next(x for x in intake.items if x.task_id == "EW_COUNTERTERM")
    tests = {
        "candidate_present": item.status == IntakeStatus.CANDIDATE_EVIDENCE_PRESENT,
        "all_required_modules_import": item.required_modules_all_import,
        "all_required_modules_pass": item.required_modules_all_pass,
        "fragment_coverage": len(item.satisfied_fragments) >= 6,
        "export_lock_preserved": item.export_lock_preserved,
        "no_target_smuggling_guard": item.no_target_smuggling_guard,
    }
    return {
        "name": "check_T_EW_counterterm_evidence_candidate_P",
        "consistent": all(tests.values()),
        "status": "P_evidence_candidate" if all(tests.values()) else "FAIL",
        "summary": "EW counterterm evidence candidate is present, guarded, and held for rerun admission.",
        "data": {"tests": tests, "item": item.to_dict()},
    }


def check_T_EW_uncertainty_evidence_candidate_P() -> Dict[str, Any]:
    intake = build_ew_counterterm_uncertainty_intake()
    item = next(x for x in intake.items if x.task_id == "EW_UNCERTAINTY_PROTOCOL")
    tests = {
        "candidate_present": item.status == IntakeStatus.CANDIDATE_EVIDENCE_PRESENT,
        "all_required_modules_import": item.required_modules_all_import,
        "all_required_modules_pass": item.required_modules_all_pass,
        "fragment_coverage": len(item.satisfied_fragments) >= 6,
        "export_lock_preserved": item.export_lock_preserved,
        "no_target_smuggling_guard": item.no_target_smuggling_guard,
    }
    return {
        "name": "check_T_EW_uncertainty_evidence_candidate_P",
        "consistent": all(tests.values()),
        "status": "P_evidence_candidate" if all(tests.values()) else "FAIL",
        "summary": "EW uncertainty-protocol evidence candidate is present, guarded, and held for rerun admission.",
        "data": {"tests": tests, "item": item.to_dict()},
        "dependencies": ["check_T_EW_counterterm_evidence_candidate_P"],
    }


def check_T_EW_intake_does_not_promote_route_P() -> Dict[str, Any]:
    intake = build_ew_counterterm_uncertainty_intake()
    tests = {
        "live_packet_safe": intake.live_ew_packet_status in {"OPEN_EVIDENCE_REQUIRED", "NOT_REQUIRED_ALREADY_P"},
        "live_missing_subset_or_none": set(intake.live_ew_missing).issubset({"COUNTERTERM", "UNCERTAINTY_PROTOCOL"}),
        "held_or_imported_admitted": bool(intake.summary.get("live_adapter_still_held")) or bool(intake.summary.get("live_adapter_already_admitted")),
        "status_candidate": intake.status in {"CANDIDATE_EVIDENCE_PRESENT_HELD_FOR_RERUN", "CANDIDATE_EVIDENCE_PRESENT_ADMITTED_IMPORTED_ROUTE"},
        "no_target_smuggling_guards": all(item.no_target_smuggling_guard for item in intake.items),
    }
    return {
        "name": "check_T_EW_intake_does_not_promote_route_P",
        "consistent": all(tests.values()),
        "status": "P_evidence_candidate" if all(tests.values()) else "FAIL",
        "summary": "EW intake surfaces candidate evidence while preserving no-target guards and no-new-physical-W boundary.",
        "data": {"tests": tests, "live_missing": intake.live_ew_missing, "packet": intake.live_ew_packet_status},
        "dependencies": ["check_T_EW_uncertainty_evidence_candidate_P"],
    }


def check_T_EW_counterterm_uncertainty_intake_P() -> Dict[str, Any]:
    subchecks = [
        check_T_EW_counterterm_evidence_candidate_P(),
        check_T_EW_uncertainty_evidence_candidate_P(),
        check_T_EW_intake_does_not_promote_route_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    return {
        "name": "check_T_EW_counterterm_uncertainty_intake_P",
        "consistent": ok,
        "status": "P_evidence_intake" if ok else "FAIL",
        "summary": "EW counterterm and uncertainty live blockers have candidate evidence packets, with no route promotion.",
        "data": {"subchecks": [x["name"] for x in subchecks]},
        "dependencies": [x["name"] for x in subchecks],
    }


CHECKS = {
    "check_T_EW_counterterm_evidence_candidate_P": check_T_EW_counterterm_evidence_candidate_P,
    "check_T_EW_uncertainty_evidence_candidate_P": check_T_EW_uncertainty_evidence_candidate_P,
    "check_T_EW_intake_does_not_promote_route_P": check_T_EW_intake_does_not_promote_route_P,
    "check_T_EW_counterterm_uncertainty_intake_P": check_T_EW_counterterm_uncertainty_intake_P,
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
            raise TypeError("Unsupported registry type for interface_ew_counterterm_uncertainty_intake.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Build/verify EW counterterm + uncertainty evidence intake.")
    parser.add_argument("--out-dir", default=None, help="Optional output directory for intake artifacts.")
    parser.add_argument("--json", action="store_true", help="Print intake JSON instead of check summary.")
    args = parser.parse_args()

    if args.out_dir:
        paths = export_intake(args.out_dir)
        print(json.dumps({"exported": paths}, indent=2))
    elif args.json:
        print(json.dumps(build_ew_counterterm_uncertainty_intake().to_dict(), indent=2, default=str))
    else:
        results = run_all()
        print(json.dumps(results, indent=2, sort_keys=True, default=str))
        raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
