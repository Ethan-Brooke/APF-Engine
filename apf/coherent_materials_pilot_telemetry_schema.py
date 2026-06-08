"""CMAL pilot telemetry schema.

Architecture-only utility for the Coherent Materials Audit Layer (CMAL).
It defines guarded pilot telemetry events that can be produced by human
pilot workflows and consumed by release governance. It does not implement
live ingestion, autonomous lab execution, public connector calls, or bank
checks.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Iterable, Literal
import json

ALLOWED_STAGES = {
    "RECEIPT_VALIDATION", "PROVENANCE_AUDIT", "LEDGER_UPDATE", "TRIAGE",
    "REVIEW_BOARD", "RELEASE_GATE", "PARTNER_FEEDBACK", "PILOT_OUTCOME",
}
ALLOWED_CODOMAINS = {
    "SC_MATERIAL_ADMISSIBILITY",
    "RARE_EARTH_QUANTUM_MEMORY",
    "CORRELATED_LAYER_PHASE_BOUNDARY",
    "HYDRIDE_PRESSURE_CONDITIONED_SC",
    "STUB_TOPOLOGICAL_MATERIAL",
    "STUB_THERMOELECTRIC",
    "STUB_ION_CONDUCTOR",
}
OVERCLAIM_STATUSES = {"PUBLIC_CLAIM_REQUESTED", "NEW_MATERIAL_PREDICTION", "NUMERIC_TC_CLAIM", "ROOM_TEMP_SC_CLAIM"}

@dataclass(frozen=True)
class PilotTelemetryEvent:
    event_id: str
    timestamp_utc: str
    material_id: str
    sample_id: str
    target_codomain: str
    stage: str
    actor_type: str
    decision_status: str
    linked_receipts: tuple[str, ...]
    linked_obligation_packets: tuple[str, ...]
    nonclaim_guard_ack: bool
    provenance_anchor: str
    notes: str = ""

@dataclass(frozen=True)
class TelemetryValidation:
    event_id: str
    status: str
    reasons: tuple[str, ...]
    route: str
    nonclaims_preserved: dict[str, int]


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


def validate_telemetry_event(event: PilotTelemetryEvent) -> TelemetryValidation:
    reasons: list[str] = []
    status = "VALID"
    route = "CMAL_PILOT_TELEMETRY"
    if not event.event_id or not event.material_id or not event.sample_id:
        status = "REPAIRABLE"
        reasons.append("missing event_id, material_id, or sample_id")
    if event.stage not in ALLOWED_STAGES:
        status = "REJECTED"
        reasons.append("stage not exported by CMAL telemetry schema")
    if event.target_codomain not in ALLOWED_CODOMAINS:
        status = "REJECTED"
        reasons.append("target_codomain not active or stub-recognized in CMAL")
    if not event.nonclaim_guard_ack:
        status = "REPAIRABLE" if status == "VALID" else status
        reasons.append("nonclaim guard not acknowledged")
    if event.decision_status in OVERCLAIM_STATUSES:
        status = "QUARANTINED"
        route = "CLAIM_FENCE"
        reasons.append("telemetry attempts to promote a forbidden claim")
    if event.target_codomain == "RARE_EARTH_QUANTUM_MEMORY" and "superconduct" in event.notes.lower():
        status = "QUARANTINED"
        route = "CLAIM_FENCE"
        reasons.append("rare-earth QM event contains superconductivity misrouting language")
    if not reasons:
        reasons.append("telemetry event is admissible for guarded pilot accounting")
    return TelemetryValidation(
        event_id=event.event_id,
        status=status,
        reasons=tuple(reasons),
        route=route,
        nonclaims_preserved={
            "APF_Mat_sixth_engine": 0,
            "materials_discovery_OS": 0,
            "materials_live_ingestion_connector": 0,
            "autonomous_lab_execution": 0,
            "SC_numeric_Tc": 0,
            "SC_new_material_prediction": 0,
            "Pearson_superconductivity_claim": 0,
            "room_temperature_superconductivity": 0,
        },
    )


def reference_telemetry_events() -> tuple[PilotTelemetryEvent, ...]:
    ts = "2026-05-19T22:45:00Z"
    return (
        PilotTelemetryEvent("TEL-QM-001", ts, "NaEu(IO3)4", "PEARSON-SAMPLE-01", "RARE_EARTH_QUANTUM_MEMORY", "PILOT_OUTCOME", "HUMAN_REVIEWER", "PROMOTE_QM_LANE_ONLY", ("QM-AFC-001", "QM-LINEWIDTH-001"), ("OP-QM-001",), True, "Pearson thesis / Chapter 7", "AFC/linewidth/spin-lifetime receipts in the QM-only lane."),
        PilotTelemetryEvent("TEL-SC-001", ts, "SC-control-material", "SC-SAMPLE-01", "SC_MATERIAL_ADMISSIBILITY", "RELEASE_GATE", "HUMAN_REVIEWER", "PROMOTE_CODOMAIN", ("SC-MEISSNER-001", "SC-FIELD-001"), ("OP-SC-001",), True, "manual dry-run fixture", "bulk SC receipt completion"),
        PilotTelemetryEvent("TEL-RTSC-001", ts, "formula-only-material", "UNKNOWN", "SC_MATERIAL_ADMISSIBILITY", "PARTNER_FEEDBACK", "PARTNER", "ROOM_TEMP_SC_CLAIM", tuple(), tuple(), True, "unreviewed partner text", "requests public room-temperature superconductivity announcement"),
        PilotTelemetryEvent("TEL-REPAIR-001", ts, "nickelate-template", "", "CORRELATED_LAYER_PHASE_BOUNDARY", "TRIAGE", "HUMAN_REVIEWER", "UPDATE_PHASE_BOUNDARY_MAP", ("NI-STRAIN-001",), ("OP-NI-001",), True, "manual phase-boundary fixture", "missing sample id should repair"),
    )


def validate_batch(events: Iterable[PilotTelemetryEvent]) -> dict:
    validations = [validate_telemetry_event(e) for e in events]
    counts: dict[str, int] = {}
    for v in validations:
        counts[v.status] = counts.get(v.status, 0) + 1
    return {
        "schema": "CMAL_PILOT_TELEMETRY_VALIDATION_REPORT_v1",
        "architecture": "CMAL subset Codomain Selection; pilot telemetry only",
        "counts_by_status": counts,
        "validations": [asdict(v) for v in validations],
        "nonclaims_preserved": all(all(value == 0 for value in v.nonclaims_preserved.values()) for v in validations),
    }
