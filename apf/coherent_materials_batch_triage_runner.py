"""CMAL batch triage runner (architecture-only).

Composes the CMAL golden benchmark, receipt contract validator, receipt-update
loop, triage kernel, and obligation packet compiler into one deterministic batch
navigation harness. It is not a live ingestion connector, not autonomous lab
execution, and not a new APF engine.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence
import csv, json

from apf.coherent_materials_golden_receipt_benchmark import iter_cases, get_case, benchmark_summary, NONCLAIM_EXPORTS
from apf.coherent_materials_receipt_contract_validator import validate_receipt
from apf.coherent_materials_candidate_triage_kernel import triage_candidate
from apf.coherent_materials_receipt_update_loop import receipt_update_roundtrip
from apf.coherent_materials_obligation_packet_adapter import compile_materials_obligation_packet_from_ledger, packet_to_dict
from apf.coherent_materials_discriminator import classify_material_ledger

BLOCKING_VALIDATION_STATUSES = {"REJECTED", "QUARANTINED"}

@dataclass(frozen=True)
class BatchCaseResult:
    case_id: str
    batch_route: str
    validation_statuses: tuple[str, ...]
    validation_routes: tuple[str, ...]
    update_status: str
    updated_classification: str
    triage_bucket: str
    next_action: str
    obligation_packet: Mapping[str, Any]
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "batch_route": self.batch_route,
            "validation_statuses": list(self.validation_statuses),
            "validation_routes": list(self.validation_routes),
            "update_status": self.update_status,
            "updated_classification": self.updated_classification,
            "triage_bucket": self.triage_bucket,
            "next_action": self.next_action,
            "obligation_packet": dict(self.obligation_packet),
            "reasons": list(self.reasons),
        }


def _route_from_validation(validations: Sequence[Any]) -> str:
    statuses = [v.status for v in validations]
    routes = [v.route for v in validations]
    if any(s == "QUARANTINED" for s in statuses):
        return "QUARANTINED_BY_VALIDATOR"
    if any(s == "REJECTED" for s in statuses):
        return "REJECTED_BY_VALIDATOR"
    if any(s == "REPAIRABLE" for s in statuses):
        return "REPAIR_REQUIRED_BY_VALIDATOR"
    if routes and all(r == "STUB_RECOGNIZED_NOT_EXPORTED" for r in routes):
        return "STUB_RECOGNIZED_NOT_EXPORTED"
    return "LEDGER_UPDATED"


def _first_triage(receipts: Sequence[Mapping[str, Any]]) -> tuple[str, str]:
    if not receipts:
        return "NO_RECEIPTS", "REQUEST_REVIEW"
    # Use the maximum admissibility gain / priority result among receipts as the case's queue bucket.
    results = [triage_candidate(r) for r in receipts]
    order = {
        "QUARANTINE_QUEUE": 0,
        "EVIDENCE_COMPLETION_QUEUE": 1,
        "BURDEN_SEPARATION_QUEUE": 2,
        "PHASE_BOUNDARY_QUEUE": 3,
        "ADMISSIBLE_CODOMAIN_QUEUE": 4,
        "CONTRACT_REPAIR_QUEUE": 5,
        "REROUTE_QUEUE": 6,
        "LOW_PRIORITY_OR_STUB_QUEUE": 7,
    }
    best = sorted(results, key=lambda x: (order.get(x.queue_bucket, 99), -x.expected_admissibility_gain, -x.triage_score))[0]
    return best.queue_bucket, best.next_action


def run_case(case_id: str, case: Mapping[str, Any] | None = None) -> BatchCaseResult:
    case = dict(case or get_case(case_id))
    ledger = dict(case["ledger"])
    receipts = list(case.get("receipts", ()))
    validations = [validate_receipt(r) for r in receipts]
    batch_route = _route_from_validation(validations)
    triage_bucket, action = _first_triage(receipts)
    validation_routes = tuple(v.route for v in validations)
    validation_statuses = tuple(v.status for v in validations)
    reasons = [reason for v in validations for reason in v.reasons]

    if batch_route == "LEDGER_UPDATED":
        update = receipt_update_roundtrip(ledger, receipts)
        update_status = str(update["update_status"])
        updated_classification = str(update["updated_classification"])
        packet = dict(update["next_obligation_packet"])
        reasons.extend(update.get("reasons", ()))
    elif batch_route == "QUARANTINED_BY_VALIDATOR":
        update_status = "QUARANTINE_CLAIM"
        updated_classification = "CLAIM_QUARANTINED"
        qledger = dict(ledger)
        qledger["classification"] = "CLAIM_QUARANTINED"
        qledger["top_action"] = "QUARANTINE_AND_REPRODUCE"
        packet = packet_to_dict(compile_materials_obligation_packet_from_ledger(qledger))
    elif batch_route == "REJECTED_BY_VALIDATOR":
        update_status = "ROUTE_TO_DIFFERENT_CODOMAIN"
        updated_classification = classify_material_ledger(ledger).classification
        packet = packet_to_dict(compile_materials_obligation_packet_from_ledger(ledger))
    elif batch_route == "REPAIR_REQUIRED_BY_VALIDATOR":
        update_status = "REQUEST_NEXT_RECEIPT"
        updated_classification = "MATERIAL_LEDGER_INSUFFICIENT"
        rledger = dict(ledger)
        rledger["classification"] = "MATERIAL_LEDGER_INSUFFICIENT"
        rledger["top_action"] = "COMPLETE_MATERIAL_LEDGER"
        packet = packet_to_dict(compile_materials_obligation_packet_from_ledger(rledger))
    else:
        update_status = "HOLD_PARTIAL"
        updated_classification = classify_material_ledger(ledger).classification
        packet = packet_to_dict(compile_materials_obligation_packet_from_ledger(ledger))

    # Promote the case-level queue from the composed update state, not from any
    # one receipt in a multi-receipt bundle.
    if update_status in {"PROMOTE_CODOMAIN"}:
        triage_bucket, action = "ADMISSIBLE_CODOMAIN_QUEUE", "EMIT_ADMISSIBILITY_PACKET"
    elif update_status == "PROMOTE_PRESSURE_CONDITIONED_SC":
        triage_bucket, action = "BURDEN_SEPARATION_QUEUE", "PRESERVE_PRESSURE_CONDITIONED_NONCLAIM"
    elif update_status == "QUARANTINE_CLAIM":
        triage_bucket, action = "QUARANTINE_QUEUE", "QUARANTINE_AND_REPRODUCE"
    elif update_status == "UPDATE_PHASE_BOUNDARY_MAP":
        triage_bucket, action = "PHASE_BOUNDARY_QUEUE", "UPDATE_PHASE_BOUNDARY_MAP"
    elif update_status == "ROUTE_TO_DIFFERENT_CODOMAIN":
        triage_bucket, action = "REROUTE_QUEUE", "REROUTE_TO_DECLARED_CODOMAIN"
    elif batch_route == "REPAIR_REQUIRED_BY_VALIDATOR":
        triage_bucket, action = "CONTRACT_REPAIR_QUEUE", "REPAIR_RECEIPT_CONTRACT"
    elif updated_classification == "RESISTIVE_ONLY_NO_MEISSNER":
        triage_bucket, action = "EVIDENCE_COMPLETION_QUEUE", "MEASURE_MEISSNER_RESPONSE"

    return BatchCaseResult(
        case_id=case_id,
        batch_route=batch_route,
        validation_statuses=validation_statuses,
        validation_routes=validation_routes,
        update_status=update_status,
        updated_classification=updated_classification,
        triage_bucket=triage_bucket,
        next_action=action,
        obligation_packet=packet,
        reasons=tuple(dict.fromkeys(str(x) for x in reasons)),
    )


def run_golden_batch() -> list[BatchCaseResult]:
    return [run_case(cid, case) for cid, case in iter_cases()]


def make_validation_report(results: Sequence[BatchCaseResult]) -> dict[str, Any]:
    return {
        "schema": "CMAL_VALIDATION_REPORT_v1",
        "case_count": len(results),
        "cases": [r.to_dict() for r in results],
        "nonclaims": dict(NONCLAIM_EXPORTS),
    }


def make_ledger_update_report(results: Sequence[BatchCaseResult]) -> dict[str, Any]:
    return {
        "schema": "CMAL_LEDGER_UPDATE_REPORT_v1",
        "promotions": [r.case_id for r in results if r.update_status in {"PROMOTE_CODOMAIN", "PROMOTE_PRESSURE_CONDITIONED_SC"}],
        "quarantines": [r.case_id for r in results if r.update_status == "QUARANTINE_CLAIM"],
        "repairs": [r.case_id for r in results if r.batch_route == "REPAIR_REQUIRED_BY_VALIDATOR"],
        "reroutes": [r.case_id for r in results if r.update_status == "ROUTE_TO_DIFFERENT_CODOMAIN"],
        "phase_boundary_updates": [r.case_id for r in results if r.update_status == "UPDATE_PHASE_BOUNDARY_MAP"],
        "case_results": [r.to_dict() for r in results],
        "nonclaims": dict(NONCLAIM_EXPORTS),
    }


def make_next_obligation_packets(results: Sequence[BatchCaseResult]) -> dict[str, Any]:
    return {
        "schema": "CMAL_NEXT_OBLIGATION_PACKETS_v1",
        "packets": {r.case_id: dict(r.obligation_packet) for r in results},
    }


def write_batch_outputs(output_dir: str | Path, results: Sequence[BatchCaseResult] | None = None) -> dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results = list(results or run_golden_batch())
    validation = make_validation_report(results)
    ledger_update = make_ledger_update_report(results)
    obligations = make_next_obligation_packets(results)
    (out / "VALIDATION_REPORT.json").write_text(json.dumps(validation, indent=2), encoding="utf-8")
    (out / "LEDGER_UPDATE_REPORT.json").write_text(json.dumps(ledger_update, indent=2), encoding="utf-8")
    (out / "NEXT_OBLIGATION_PACKETS.json").write_text(json.dumps(obligations, indent=2), encoding="utf-8")
    with (out / "TRIAGE_QUEUE.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["rank","case_id","triage_bucket","next_action","batch_route","update_status","updated_classification"])
        w.writeheader()
        for i, r in enumerate(results, 1):
            w.writerow({"rank": i, "case_id": r.case_id, "triage_bucket": r.triage_bucket, "next_action": r.next_action, "batch_route": r.batch_route, "update_status": r.update_status, "updated_classification": r.updated_classification})
    summary_lines = [
        "# CMAL Batch Audit Summary",
        "",
        "The batch runner validates incoming receipts, updates ledgers where admissible, triages candidates, and emits next obligation packets.",
        "",
        f"Case count: {len(results)}",
        "",
        "| Case | Route | Update | Classification | Queue |",
        "|---|---|---|---|---|",
    ]
    for r in results:
        summary_lines.append(f"| {r.case_id} | {r.batch_route} | {r.update_status} | {r.updated_classification} | {r.triage_bucket} |")
    summary_lines.extend([
        "",
        "## Preserved non-claims",
        "",
        "CMAL remains a Codomain Selection specialization. No APF-Mat sixth engine, Materials Discovery OS, live ingestion connector, autonomous lab execution, numeric Tc prediction, new-material prediction, Pearson superconductivity claim, or room-temperature superconductivity claim is exported.",
    ])
    (out / "CMAL_BATCH_AUDIT_SUMMARY.md").write_text("\n".join(summary_lines) + "\n", encoding="utf-8")
    return {p.name: str(p) for p in out.iterdir() if p.is_file()}


def demo_output_dict() -> dict[str, Any]:
    results = run_golden_batch()
    return {
        "benchmark": benchmark_summary(),
        "validation_report": make_validation_report(results),
        "ledger_update_report": make_ledger_update_report(results),
        "next_obligation_packets": make_next_obligation_packets(results),
    }
