"""CMAL portfolio planner (architecture-only).

Turns CMAL triage/update results into a bounded human-review portfolio. The
planner ranks *claim-admissibility gain per experimental/provenance burden*; it
is not a discovery-likelihood score, not autonomous lab execution, not a live
connector, and not a sixth APF engine.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence
import csv
import json

NONCLAIM_GUARDS: dict[str, int] = {
    "APF_Mat_sixth_engine": 0,
    "materials_discovery_OS_architecture": 0,
    "materials_live_ingestion_connector": 0,
    "materials_public_ingestion_core_engine": 0,
    "autonomous_lab_execution": 0,
    "SC_numeric_Tc_prediction": 0,
    "SC_new_material_prediction": 0,
    "SC_highTc_solution": 0,
    "SC_ab_initio_chemistry": 0,
    "Pearson_superconductivity_claim": 0,
    "room_temperature_superconductivity_claim": 0,
}

COST_BY_BUCKET: dict[str, float] = {
    "QUARANTINE_QUEUE": 2.0,
    "EVIDENCE_COMPLETION_QUEUE": 4.0,
    "ADMISSIBLE_CODOMAIN_QUEUE": 2.0,
    "BURDEN_SEPARATION_QUEUE": 4.0,
    "PHASE_BOUNDARY_QUEUE": 6.0,
    "REROUTE_QUEUE": 2.0,
    "CONTRACT_REPAIR_QUEUE": 1.5,
    "LOW_PRIORITY_OR_STUB_QUEUE": 1.0,
}

GAIN_BY_BUCKET: dict[str, float] = {
    "QUARANTINE_QUEUE": 0.92,
    "EVIDENCE_COMPLETION_QUEUE": 0.86,
    "PHASE_BOUNDARY_QUEUE": 0.78,
    "ADMISSIBLE_CODOMAIN_QUEUE": 0.74,
    "BURDEN_SEPARATION_QUEUE": 0.68,
    "REROUTE_QUEUE": 0.58,
    "CONTRACT_REPAIR_QUEUE": 0.46,
    "LOW_PRIORITY_OR_STUB_QUEUE": 0.12,
}

LANE_WEIGHT: dict[str, float] = {
    "RARE_EARTH_QUANTUM_MEMORY": 0.30,
    "SUPERCONDUCTIVITY": 0.30,
    "CORRELATED_LAYER_SC": 0.28,
    "HYDRIDE_PRESSURE_SC": 0.24,
    "GENERAL_COHERENT_MATERIAL": 0.16,
    "STUB": -0.20,
}

@dataclass(frozen=True)
class PilotBudget:
    max_actions: int = 5
    max_total_cost: float = 18.0
    lane_minima: Mapping[str, int] | None = None
    include_stub_actions: bool = False
    allow_quarantine_actions: bool = True

    def minima(self) -> Mapping[str, int]:
        return self.lane_minima or {"RARE_EARTH_QUANTUM_MEMORY": 1, "SUPERCONDUCTIVITY": 1}

@dataclass(frozen=True)
class PortfolioCandidate:
    case_id: str
    lane: str
    triage_bucket: str
    update_status: str
    classification: str
    next_action: str
    obligation_packet_id: str
    cost: float
    expected_admissibility_gain: float
    overclaim_risk_reduction: float
    provenance_risk: float
    score: float
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "lane": self.lane,
            "triage_bucket": self.triage_bucket,
            "update_status": self.update_status,
            "classification": self.classification,
            "next_action": self.next_action,
            "obligation_packet_id": self.obligation_packet_id,
            "cost": self.cost,
            "expected_admissibility_gain": self.expected_admissibility_gain,
            "overclaim_risk_reduction": self.overclaim_risk_reduction,
            "provenance_risk": self.provenance_risk,
            "score": self.score,
            "reasons": list(self.reasons),
        }

@dataclass(frozen=True)
class PortfolioPlan:
    selected: tuple[PortfolioCandidate, ...]
    deferred: tuple[PortfolioCandidate, ...]
    total_cost: float
    budget: PilotBudget
    nonclaim_guards: Mapping[str, int]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "CMAL_PORTFOLIO_PLAN_v2",
            "selected": [c.to_dict() for c in self.selected],
            "deferred": [c.to_dict() for c in self.deferred],
            "total_cost": self.total_cost,
            "budget": {
                "max_actions": self.budget.max_actions,
                "max_total_cost": self.budget.max_total_cost,
                "lane_minima": dict(self.budget.minima()),
                "include_stub_actions": self.budget.include_stub_actions,
                "allow_quarantine_actions": self.budget.allow_quarantine_actions,
            },
            "nonclaim_guards": dict(self.nonclaim_guards),
            "interpretation": "bounded human-review portfolio; not autonomous lab execution and not discovery likelihood",
        }


def sample_results() -> list[dict[str, Any]]:
    return [
        {"case_id":"pearson_naeu_qm", "updated_classification":"COHERENT_BUT_NOT_SC", "update_status":"PROMOTE_CODOMAIN", "triage_bucket":"ADMISSIBLE_CODOMAIN_QUEUE", "next_action":"OPTIMIZE_AFC_EFFICIENCY", "obligation_packet":{"packet_id":"QM-AFC-001"}, "validation_statuses":["VALID"], "reasons":["non-SC coherent-material lane"]},
        {"case_id":"resistive_only_sc_claim", "updated_classification":"RESISTIVE_ONLY_NO_MEISSNER", "update_status":"REQUEST_NEXT_RECEIPT", "triage_bucket":"EVIDENCE_COMPLETION_QUEUE", "next_action":"MEASURE_MEISSNER_RESPONSE", "obligation_packet":{"packet_id":"SC-MEISSNER-001"}, "validation_statuses":["VALID"], "reasons":["resistivity alone never promotes"]},
        {"case_id":"formula_only_room_temp_sc", "updated_classification":"CLAIM_QUARANTINED", "update_status":"QUARANTINE_CLAIM", "triage_bucket":"QUARANTINE_QUEUE", "next_action":"QUARANTINE_AND_REPRODUCE", "obligation_packet":{"packet_id":"Q-RTSC-001"}, "validation_statuses":["QUARANTINED"], "reasons":["formula-only extraordinary claim"]},
        {"case_id":"nickelate_phase_boundary_template", "updated_classification":"PHASE_BOUNDARY_SCOUT", "update_status":"UPDATE_PHASE_BOUNDARY_MAP", "triage_bucket":"PHASE_BOUNDARY_QUEUE", "next_action":"SWEEP_STRAIN_PRESSURE_OXYGENATION", "obligation_packet":{"packet_id":"CL-SWEEP-001"}, "validation_statuses":["VALID"], "reasons":["correlated-layer competition"]},
        {"case_id":"hydride_pressure_conditioned", "updated_classification":"SC_MATERIAL_ADMISSIBLE_PRESSURE_CONDITIONED", "update_status":"PROMOTE_PRESSURE_CONDITIONED_SC", "triage_bucket":"BURDEN_SEPARATION_QUEUE", "next_action":"SEPARATE_PRESSURE_CONDITION_FROM_AMBIENT_USABILITY", "obligation_packet":{"packet_id":"HYD-P-001"}, "validation_statuses":["VALID"], "reasons":["pressure-conditioned only"]},
        {"case_id":"missing_uncertainty_receipt", "updated_classification":"MATERIAL_LEDGER_INSUFFICIENT", "update_status":"REQUEST_REPAIR", "triage_bucket":"CONTRACT_REPAIR_QUEUE", "next_action":"SUPPLY_UNCERTAINTY_AND_CONTROL_VECTOR", "obligation_packet":{"packet_id":"REPAIR-001"}, "validation_statuses":["REPAIRABLE"], "reasons":["missing uncertainty"]},
    ]


def _as_dict(result: Any) -> Mapping[str, Any]:
    if hasattr(result, "to_dict"):
        return result.to_dict()
    if isinstance(result, Mapping):
        return result
    raise TypeError(f"unsupported result type {type(result)!r}")


def _packet_id(packet: Mapping[str, Any]) -> str:
    for key in ("packet_id", "target_unit_id", "obligation_id"):
        if packet.get(key):
            return str(packet[key])
    return "packet:none" if not packet else "packet:present"


def infer_lane(row: Mapping[str, Any]) -> str:
    case_id = str(row.get("case_id", "")).lower()
    cls = str(row.get("updated_classification", row.get("classification", ""))).upper()
    action = str(row.get("next_action", "")).upper()
    bucket = str(row.get("triage_bucket", "")).upper()
    if "pearson" in case_id or "QUANTUM" in cls or "AFC" in action:
        return "RARE_EARTH_QUANTUM_MEMORY"
    if "nickelate" in case_id or "PHASE_BOUNDARY" in bucket or "PHASE_BOUNDARY" in action:
        return "CORRELATED_LAYER_SC"
    if "hydride" in case_id or "pressure" in case_id:
        return "HYDRIDE_PRESSURE_SC"
    if "STUB" in bucket or "topological" in case_id or "thermoelectric" in case_id or "ion_conductor" in case_id:
        return "STUB"
    if "SC" in cls or "SUPERCONDUCT" in action or "MEISSNER" in action or "resistive" in case_id or "bulk_sc" in case_id or "ambient" in case_id:
        return "SUPERCONDUCTIVITY"
    return "GENERAL_COHERENT_MATERIAL"


def _overclaim_risk(row: Mapping[str, Any]) -> float:
    cls = str(row.get("updated_classification", "")).upper()
    update = str(row.get("update_status", "")).upper()
    bucket = str(row.get("triage_bucket", "")).upper()
    case_id = str(row.get("case_id", "")).lower()
    if "QUARANT" in update or "QUARANT" in cls or "QUARANTINE" in bucket:
        return 1.00
    if "RESISTIVE_ONLY" in cls:
        return 0.74
    if "MISROUTED" in case_id or "REROUTE" in update:
        return 0.70
    if "PRESSURE" in update or "hydride" in case_id:
        return 0.58
    if "PHASE_BOUNDARY" in bucket or "nickelate" in case_id:
        return 0.44
    if "STUB" in bucket:
        return 0.10
    return 0.25


def _provenance_risk(row: Mapping[str, Any]) -> float:
    statuses = [str(s).upper() for s in row.get("validation_statuses", ())]
    if any(s == "REPAIRABLE" for s in statuses):
        return 0.62
    if any(s in {"REJECTED", "QUARANTINED"} for s in statuses):
        return 0.50
    if not statuses:
        return 0.35
    return 0.15


def candidate_from_result(result: Any) -> PortfolioCandidate:
    row = dict(_as_dict(result))
    bucket = str(row.get("triage_bucket", "LOW_PRIORITY_OR_STUB_QUEUE"))
    lane = infer_lane(row)
    cost = COST_BY_BUCKET.get(bucket, 3.0)
    gain = GAIN_BY_BUCKET.get(bucket, 0.20)
    overclaim = _overclaim_risk(row)
    provenance = _provenance_risk(row)
    score = (1.35 * gain) + (0.95 * overclaim) + LANE_WEIGHT.get(lane, 0.0) - (0.12 * cost) - (0.40 * provenance)
    return PortfolioCandidate(
        case_id=str(row.get("case_id", "unknown_case")),
        lane=lane,
        triage_bucket=bucket,
        update_status=str(row.get("update_status", "UNKNOWN_UPDATE")),
        classification=str(row.get("updated_classification", "UNKNOWN_CLASSIFICATION")),
        next_action=str(row.get("next_action", "REQUEST_REVIEW")),
        obligation_packet_id=_packet_id(dict(row.get("obligation_packet", {}))),
        cost=float(cost),
        expected_admissibility_gain=round(float(gain), 3),
        overclaim_risk_reduction=round(float(overclaim), 3),
        provenance_risk=round(float(provenance), 3),
        score=round(float(score), 4),
        reasons=tuple(str(x) for x in row.get("reasons", ()))[:8],
    )


def plan_portfolio(results: Sequence[Any], budget: PilotBudget | None = None) -> PortfolioPlan:
    budget = budget or PilotBudget()
    candidates = [candidate_from_result(r) for r in results]
    if not budget.include_stub_actions:
        candidates = [c for c in candidates if c.lane != "STUB"]
    if not budget.allow_quarantine_actions:
        candidates = [c for c in candidates if c.triage_bucket != "QUARANTINE_QUEUE"]
    remaining = sorted(candidates, key=lambda c: (-c.score, c.cost, c.case_id))
    selected: list[PortfolioCandidate] = []
    total_cost = 0.0

    def can_add(c: PortfolioCandidate) -> bool:
        return len(selected) < budget.max_actions and total_cost + c.cost <= budget.max_total_cost and c not in selected

    for lane, n in budget.minima().items():
        lane_candidates = [c for c in remaining if c.lane == lane]
        lane_candidates.sort(key=lambda c: (-c.score, c.cost, c.case_id))
        count = 0
        for c in lane_candidates:
            if count >= n:
                break
            if can_add(c):
                selected.append(c)
                total_cost += c.cost
                count += 1

    for c in remaining:
        if can_add(c):
            selected.append(c)
            total_cost += c.cost

    deferred = tuple(c for c in sorted(candidates, key=lambda c: (-c.score, c.case_id)) if c not in selected)
    return PortfolioPlan(tuple(selected), deferred, round(total_cost, 3), budget, NONCLAIM_GUARDS)


def plan_from_manual_dry_run(budget: PilotBudget | None = None) -> PortfolioPlan:
    try:
        from apf.coherent_materials_manual_external_dry_run import run_manual_external_dry_run
        results = run_manual_external_dry_run()
    except Exception:
        results = sample_results()
    return plan_portfolio(results, budget=budget)


def write_portfolio_outputs(output_dir: str | Path, plan: PortfolioPlan | None = None) -> dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    plan = plan or plan_from_manual_dry_run()
    paths: dict[str, str] = {}
    plan_path = out / "PORTFOLIO_PLAN.json"
    plan_path.write_text(json.dumps(plan.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths[plan_path.name] = str(plan_path)
    queue_path = out / "PORTFOLIO_QUEUE.csv"
    with queue_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["rank", "case_id", "lane", "triage_bucket", "next_action", "cost", "score", "selected"])
        w.writeheader()
        all_candidates = list(plan.selected) + list(plan.deferred)
        selected_ids = {c.case_id for c in plan.selected}
        for i, c in enumerate(all_candidates, 1):
            w.writerow({"rank": i, "case_id": c.case_id, "lane": c.lane, "triage_bucket": c.triage_bucket, "next_action": c.next_action, "cost": c.cost, "score": c.score, "selected": c.case_id in selected_ids})
    paths[queue_path.name] = str(queue_path)
    summary = out / "CMAL_PORTFOLIO_SUMMARY.md"
    lines = [
        "# CMAL Pilot Portfolio Summary", "",
        "This portfolio is a bounded human-review plan. It ranks claim-admissibility gain and overclaim-risk containment; it is not a discovery-likelihood score and not autonomous lab execution.", "",
        f"Selected actions: {len(plan.selected)}", f"Total cost units: {plan.total_cost}", "",
        "| Rank | Case | Lane | Queue | Action | Cost | Score |", "|---:|---|---|---|---|---:|---:|",
    ]
    for i, c in enumerate(plan.selected, 1):
        lines.append(f"| {i} | {c.case_id} | {c.lane} | {c.triage_bucket} | {c.next_action} | {c.cost:.1f} | {c.score:.3f} |")
    lines.extend(["", "## Preserved non-claims", "", "- APF-Mat is not promoted to a sixth engine.", "- No Materials Discovery OS architecture is exported.", "- No live ingestion connector or autonomous lab execution is exported.", "- No numeric Tc, new superconductor prediction, room-temperature superconductivity claim, or ab initio chemistry claim is exported."])
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    paths[summary.name] = str(summary)
    return paths


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "cmal_portfolio_outputs"
    print(json.dumps(write_portfolio_outputs(target), indent=2))
