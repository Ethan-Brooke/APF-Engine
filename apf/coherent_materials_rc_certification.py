"""APF Coherent Materials — Release-candidate certification (merged acceptance-test harness + RC certifier).

CMAL module-collapse (v24.3.66, Integrator Response v1.1 Q7). Architecture-only:
no register(), no check_*, no BANK_REGISTRY entry, no EXPECTED delta. Merged
verbatim from: coherent_materials_acceptance_test_harness, coherent_materials_release_candidate_certifier. Two colliding
constants were source-prefixed to preserve both consumers' values.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Iterable
import csv, json
from typing import Mapping


# === merged from coherent_materials_acceptance_test_harness ===
NONCLAIMS = {
    "APF_Mat_sixth_engine": 0,
    "materials_discovery_OS": 0,
    "materials_live_ingestion_connector": 0,
    "autonomous_lab_execution": 0,
    "SC_numeric_Tc": 0,
    "SC_new_material_prediction": 0,
    "SC_highTc_solution": 0,
    "SC_ab_initio_chemistry": 0,
    "Pearson_superconductivity_claim": 0,
    "room_temperature_superconductivity": 0,
    "unreviewed_public_release": 0,
}

@dataclass(frozen=True)
class AcceptanceCase:
    case_id: str
    description: str
    receipt_route: str
    target_codomain: str
    flags: tuple[str, ...]
    expected_status: str
    expected_next_action: str

@dataclass(frozen=True)
class AcceptanceOutcome:
    case_id: str
    observed_status: str
    observed_next_action: str
    passed: bool
    reasons: tuple[str, ...]


def acceptance_fixtures() -> tuple[AcceptanceCase, ...]:
    return (
        AcceptanceCase("ACC-SC-FULL", "full bulk superconductivity receipts", "bulk_sc_receipts", "SC_MATERIAL_ADMISSIBILITY", ("rho_zero", "meissner", "field_suppression", "replicated"), "SC_MATERIAL_ADMISSIBLE", "ALLOW_GUARDED_PROMOTION"),
        AcceptanceCase("ACC-SC-RESISTIVE", "resistive-only superconductivity claim", "resistive_only", "SC_MATERIAL_ADMISSIBILITY", ("rho_zero",), "RESISTIVE_ONLY_NO_MEISSNER", "REQUEST_MEISSNER_AND_FIELD_RECEIPTS"),
        AcceptanceCase("ACC-RTSC-FORMULA", "formula-only room-temperature SC claim", "formula_only", "SC_MATERIAL_ADMISSIBILITY", ("formula_only", "room_temp_sc"), "CLAIM_QUARANTINED", "QUARANTINE_AND_REQUIRE_REPLICATION"),
        AcceptanceCase("ACC-QM-PEARSON", "Pearson NaEu(IO3)4 quantum-memory receipts", "pearson_qm", "RARE_EARTH_QUANTUM_MEMORY", ("linewidth", "spin_lifetime", "afc"), "COHERENT_BUT_NOT_SC", "PROMOTE_QM_LANE_ONLY"),
        AcceptanceCase("ACC-QM-AS-SC", "Pearson material misrouted as superconductivity", "pearson_qm", "SC_MATERIAL_ADMISSIBILITY", ("linewidth", "afc", "misroute_sc"), "REJECTED_MISROUTED_CODOMAIN", "REROUTE_TO_QM_OR_REJECT_SC"),
        AcceptanceCase("ACC-HYDRIDE-HP", "hydride high-pressure receipts", "high_pressure_sc", "HYDRIDE_PRESSURE_CONDITIONED_SC", ("high_pressure", "meissner", "field_suppression"), "PRESSURE_CONDITIONED_SC", "PROMOTE_PRESSURE_CONDITIONED_ONLY"),
        AcceptanceCase("ACC-HYDRIDE-AMBIENT", "ambient usability inferred from high-pressure receipts", "high_pressure_sc", "SC_MATERIAL_ADMISSIBILITY", ("ambient_claim_from_high_pressure",), "CLAIM_QUARANTINED", "SEPARATE_HIGH_PRESSURE_FROM_AMBIENT"),
        AcceptanceCase("ACC-NICKELATE-SWEEP", "nickelate-style strain/oxygenation sweep", "phase_boundary_sweep", "CORRELATED_LAYER_PHASE_BOUNDARY", ("strain_sweep", "oxygenation_sweep"), "PHASE_BOUNDARY_UPDATED", "UPDATE_PHASE_BOUNDARY_MAP"),
        AcceptanceCase("ACC-STUB-TOPO", "topological material stub", "stub", "STUB_TOPOLOGICAL_MATERIAL", ("stub_only",), "STUB_RECOGNIZED_NOT_EXPORTED", "HOLD_STUB"),
        AcceptanceCase("ACC-REPAIR-UNC", "missing uncertainty receipt", "malformed_receipt", "SC_MATERIAL_ADMISSIBILITY", ("missing_uncertainty",), "REPAIRABLE_RECEIPT", "REQUEST_REPAIR"),
        AcceptanceCase("ACC-FEEDBACK-OK", "partner feedback accepted for review board", "partner_feedback", "RARE_EARTH_QUANTUM_MEMORY", ("nonclaim_ack", "clarification"), "FEEDBACK_ACCEPTED", "QUEUE_REVIEW_BOARD"),
        AcceptanceCase("ACC-FEEDBACK-OVERCLAIM", "partner feedback asks for public overclaim", "partner_feedback", "SC_MATERIAL_ADMISSIBILITY", ("public_claim", "new_material_prediction"), "CLAIM_QUARANTINED", "CLAIM_FENCE"),
    )


def route_case(case: AcceptanceCase) -> tuple[str, str, tuple[str, ...]]:
    flags = set(case.flags)
    if "room_temp_sc" in flags or "public_claim" in flags or "new_material_prediction" in flags:
        return "CLAIM_QUARANTINED", "QUARANTINE_AND_REQUIRE_REPLICATION" if "room_temp_sc" in flags else "CLAIM_FENCE", ("forbidden claim fence triggered",)
    if "ambient_claim_from_high_pressure" in flags:
        return "CLAIM_QUARANTINED", "SEPARATE_HIGH_PRESSURE_FROM_AMBIENT", ("high-pressure receipt cannot promote ambient claim",)
    if "misroute_sc" in flags:
        return "REJECTED_MISROUTED_CODOMAIN", "REROUTE_TO_QM_OR_REJECT_SC", ("Pearson/rare-earth QM receipt misrouted as SC",)
    if "missing_uncertainty" in flags:
        return "REPAIRABLE_RECEIPT", "REQUEST_REPAIR", ("missing uncertainty blocks consumption",)
    if case.target_codomain == "RARE_EARTH_QUANTUM_MEMORY" and {"linewidth", "spin_lifetime", "afc"}.issubset(flags):
        return "COHERENT_BUT_NOT_SC", "PROMOTE_QM_LANE_ONLY", ("QM coherent material receipts complete enough for guarded lane",)
    if case.target_codomain == "SC_MATERIAL_ADMISSIBILITY" and {"rho_zero", "meissner", "field_suppression", "replicated"}.issubset(flags):
        return "SC_MATERIAL_ADMISSIBLE", "ALLOW_GUARDED_PROMOTION", ("bulk SC receipt bundle complete",)
    if case.target_codomain == "SC_MATERIAL_ADMISSIBILITY" and "rho_zero" in flags:
        return "RESISTIVE_ONLY_NO_MEISSNER", "REQUEST_MEISSNER_AND_FIELD_RECEIPTS", ("resistive-only evidence is partial",)
    if case.target_codomain == "HYDRIDE_PRESSURE_CONDITIONED_SC" and "high_pressure" in flags:
        return "PRESSURE_CONDITIONED_SC", "PROMOTE_PRESSURE_CONDITIONED_ONLY", ("pressure condition remains part of claim",)
    if case.target_codomain == "CORRELATED_LAYER_PHASE_BOUNDARY":
        return "PHASE_BOUNDARY_UPDATED", "UPDATE_PHASE_BOUNDARY_MAP", ("phase-boundary evidence updates map, not material prediction",)
    if case.target_codomain.startswith("STUB_"):
        return "STUB_RECOGNIZED_NOT_EXPORTED", "HOLD_STUB", ("future codomain stub recognized but not exported",)
    if case.receipt_route == "partner_feedback":
        return "FEEDBACK_ACCEPTED", "QUEUE_REVIEW_BOARD", ("feedback accepted for human review",)
    return "HOLD_PARTIAL", "REQUEST_NEXT_RECEIPT", ("default partial hold",)


def run_acceptance_suite(cases: Iterable[AcceptanceCase] | None = None) -> dict:
    cases = tuple(acceptance_fixtures() if cases is None else cases)
    outcomes: list[AcceptanceOutcome] = []
    for case in cases:
        status, action, reasons = route_case(case)
        outcomes.append(AcceptanceOutcome(
            case_id=case.case_id,
            observed_status=status,
            observed_next_action=action,
            passed=(status == case.expected_status and action == case.expected_next_action),
            reasons=reasons,
        ))
    counts: dict[str, int] = {}
    for o in outcomes:
        counts[o.observed_status] = counts.get(o.observed_status, 0) + 1
    return {
        "schema": "CMAL_ACCEPTANCE_TEST_HARNESS_REPORT_v1",
        "architecture": "CMAL subset Codomain Selection; deterministic acceptance fixtures",
        "total_cases": len(outcomes),
        "passed_cases": sum(1 for o in outcomes if o.passed),
        "failed_cases": sum(1 for o in outcomes if not o.passed),
        "counts_by_status": counts,
        "outcomes": [asdict(o) for o in outcomes],
        "suite_status": "CMAL_ACCEPTANCE_TEST_HARNESS_PASS" if all(o.passed for o in outcomes) else "CMAL_ACCEPTANCE_TEST_HARNESS_FAIL",
        "nonclaims": NONCLAIMS,
    }

# === merged from coherent_materials_release_candidate_certifier ===
REQUIRED_ACCEPTANCE_STATUS = "CMAL_ACCEPTANCE_TEST_HARNESS_PASS"
ALLOWED_GOVERNANCE_STATUSES = {"ALLOW_INTERNAL_BANK", "ALLOW_PARTNER_PILOT_WITH_GUARDS"}
BLOCKED_CHANNELS = (
    "PUBLIC_UNREVIEWED_RELEASE",
    "LIVE_EXTERNAL_CONNECTORS",
    "AUTONOMOUS_LAB_EXECUTION",
    "MATERIAL_PREDICTION_CLAIMS",
    "ROOM_TEMPERATURE_SC_CLAIMS",
)

@dataclass(frozen=True)
class ReleaseCandidateCertificate:
    rc_id: str
    status: str
    allowed_channels: tuple[str, ...]
    blocked_channels: tuple[str, ...]
    reasons: tuple[str, ...]
    required_next_reviews: tuple[str, ...]
    exports: dict[str, int]
    nonclaims: dict[str, int]


def certify_release_candidate(acceptance_report: Mapping, governance_status: str = "ALLOW_PARTNER_PILOT_WITH_GUARDS") -> ReleaseCandidateCertificate:
    reasons: list[str] = []
    status = "BLOCKED"
    allowed: tuple[str, ...] = tuple()
    suite_ok = acceptance_report.get("suite_status") == REQUIRED_ACCEPTANCE_STATUS
    nonclaims = dict(acceptance_report.get("nonclaims", {}))
    nonclaims_ok = bool(nonclaims) and all(v == 0 for v in nonclaims.values())
    if not suite_ok:
        reasons.append("acceptance harness did not pass")
    if governance_status not in ALLOWED_GOVERNANCE_STATUSES:
        reasons.append("release governance status is not allowed")
    if not nonclaims_ok:
        reasons.append("one or more preserved nonclaims are not false")
    if suite_ok and governance_status in ALLOWED_GOVERNANCE_STATUSES and nonclaims_ok:
        status = "INTERNAL_RELEASE_CANDIDATE_WITH_GUARDS"
        allowed = ("INTERNAL_BANK_REVIEW", "GUARDED_PARTNER_PILOT_PACKET")
        reasons.append("acceptance harness passed and governance allows guarded pilot channel")
    return ReleaseCandidateCertificate(
        rc_id="CMAL-RC-2026-05-19-v1",
        status=status,
        allowed_channels=allowed,
        blocked_channels=BLOCKED_CHANNELS,
        reasons=tuple(reasons),
        required_next_reviews=("human integrator review", "IP/counsel review before public-facing materials", "partner-pilot feedback review board"),
        exports={
            "CMAL_acceptance_harness": 1 if suite_ok else 0,
            "CMAL_pilot_telemetry_schema": 1,
            "CMAL_release_candidate_certificate": 1 if status == "INTERNAL_RELEASE_CANDIDATE_WITH_GUARDS" else 0,
            "CMAL_guarded_partner_pilot_ready": 1 if status == "INTERNAL_RELEASE_CANDIDATE_WITH_GUARDS" else 0,
        },
        nonclaims=nonclaims or {
            "APF_Mat_sixth_engine": 0,
            "materials_discovery_OS": 0,
            "materials_live_ingestion_connector": 0,
            "autonomous_lab_execution": 0,
            "SC_numeric_Tc": 0,
            "SC_new_material_prediction": 0,
            "Pearson_superconductivity_claim": 0,
            "room_temperature_superconductivity": 0,
            "unreviewed_public_release": 0,
        },
    )


def reference_certificate() -> dict:
    from apf.coherent_materials_acceptance_test_harness import run_acceptance_suite
    cert = certify_release_candidate(run_acceptance_suite(), "ALLOW_PARTNER_PILOT_WITH_GUARDS")
    return asdict(cert)
