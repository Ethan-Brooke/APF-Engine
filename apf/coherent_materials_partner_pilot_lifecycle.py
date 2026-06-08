"""APF Coherent Materials — Partner-pilot lifecycle (merged kit + feedback intake + review board + readiness gate + governance gate).

CMAL module-collapse (v24.3.66, Integrator Response v1.1 Q7). Architecture-only:
no register(), no check_*, no BANK_REGISTRY entry, no EXPECTED delta. Merged
verbatim from: coherent_materials_partner_pilot_kit, coherent_materials_partner_feedback_intake, coherent_materials_pilot_outcome_review_board, coherent_materials_pilot_readiness_gate, coherent_materials_release_governance_gate. Two colliding
constants were source-prefixed to preserve both consumers' values.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any
import json
from dataclasses import dataclass, asdict
from typing import Iterable, Literal
import csv, json
from typing import Iterable
from dataclasses import dataclass
from typing import Any, Mapping


# === merged from coherent_materials_partner_pilot_kit ===
PARTNER_PILOT_KIT_NONCLAIM_GUARDS: dict[str, int] = {
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

PILOT_LANES: tuple[str, ...] = (
    "RARE_EARTH_QUANTUM_MEMORY",
    "SUPERCONDUCTIVITY_EVIDENCE_COMPLETION",
    "CORRELATED_LAYER_PHASE_BOUNDARY",
    "HYDRIDE_PRESSURE_CONDITIONED",
)


def material_ledger_template() -> dict[str, Any]:
    return {
        "schema": "APFMaterialLedger.v1",
        "ledger_id": "MATERIAL_OR_SAMPLE_IDENTIFIER",
        "material": {
            "composition": "REQUIRED",
            "structure_or_phase": "unknown_or_declared",
            "sample_id": "REQUIRED",
            "synthesis_route": "REQUIRED_FOR_PROMOTION",
            "provenance": "REQUIRED",
        },
        "control_vector": {
            "temperature_K": None,
            "pressure_GPa": None,
            "field_T": None,
            "strain": None,
            "doping_or_oxygenation": None,
            "history": [],
        },
        "target_codomain": "SC_MATERIAL_ADMISSIBILITY | RARE_EARTH_QUANTUM_MEMORY | OTHER_STUB",
        "evidence_slots": [],
        "nonclaim_guard": "formula_alone_never_promotes",
    }


def material_receipt_template() -> dict[str, Any]:
    return {
        "schema": "APFMaterialReceipt.v1",
        "receipt_id": "RECEIPT_IDENTIFIER",
        "material_id": "MATERIAL_IDENTIFIER",
        "sample_id": "REQUIRED",
        "target_codomain": "REQUIRED",
        "receipt_kind": "REQUIRED",
        "measurement_method": "REQUIRED",
        "control_vector": {
            "temperature_K": None,
            "pressure_GPa": None,
            "field_T": None,
            "strain": None,
            "history": [],
        },
        "measured_value": "REQUIRED",
        "uncertainty": "REQUIRED",
        "instrument_or_protocol": "REQUIRED",
        "provenance": {
            "source_anchor": "paper/figure/lab-notebook/run-id",
            "operator_or_source": "REQUIRED",
            "timestamp_or_date": "REQUIRED",
        },
        "replication_status": "single_run | internal_replicate | independent_replicate",
        "updates_required_slots": [],
        "nonclaim_guard": "do_not_promote_beyond_declared_codomain",
    }


def protocol_cards() -> dict[str, str]:
    return {
        "RARE_EARTH_QM_PEARSON_CARD.md": """# CMAL Pilot Card — Rare-earth quantum memory\n\n**Target codomain:** `RARE_EARTH_QUANTUM_MEMORY`\n\n**Use case:** Pearson-style stoichiometric Eu material ledger, including NaEu(IO3)4.\n\n**Dominant burden:** inhomogeneous broadening / local-environment variation.\n\n**Receipts required:** homogeneous linewidth, inhomogeneous linewidth, optical lifetime, spin lifetime, photon echo or spectral-hole-burning trace, AFC efficiency/bandwidth/storage-time receipts, stability/provenance.\n\n**Promotion rule:** promote only within the quantum-memory/coherent-material lane. Never promote to superconductivity.\n""",
        "SC_EVIDENCE_COMPLETION_CARD.md": """# CMAL Pilot Card — Superconductivity evidence completion\n\n**Target codomain:** `SC_MATERIAL_ADMISSIBILITY`\n\n**Use case:** resistive-transition or zero-resistance claim that lacks bulk-superconductivity receipts.\n\n**Receipts required:** resistivity transition, Meissner/diamagnetic response, field suppression or critical-field behavior, reproducibility, sample/provenance ledger.\n\n**Promotion rule:** resistivity alone never promotes; missing Meissner/field/provenance routes to evidence completion or quarantine.\n""",
        "CORRELATED_LAYER_PHASE_BOUNDARY_CARD.md": """# CMAL Pilot Card — Correlated-layer phase boundary\n\n**Target codomain:** `SC_MATERIAL_ADMISSIBILITY` with competing codomains.\n\n**Use case:** nickelate/cuprate/iron-based/interface template with SC competing against AFM, CDW, stripe, pseudogap, vortex, or normal codomains.\n\n**Receipts required:** strain/pressure/oxygenation/history sweep, normal transport, magnetic/charge-order probes, SC evidence receipts if claimed, and phase-boundary map.\n\n**Promotion rule:** update phase-boundary map; do not export new-material prediction or numeric Tc.\n""",
        "HYDRIDE_PRESSURE_CONDITIONED_CARD.md": """# CMAL Pilot Card — High-pressure hydride\n\n**Target codomain:** pressure-conditioned superconductivity.\n\n**Use case:** high-pressure hydride receipt bundle.\n\n**Receipts required:** pressure ledger, structure/provenance, resistivity, magnetic/field response where available, reproducibility, decompression/ambient-claim separation.\n\n**Promotion rule:** high-pressure receipts may promote pressure-conditioned SC only. They never promote ambient usability by themselves.\n""",
        "INTAKE_REVIEW_PROMPTS.md": """# CMAL Intake Review Prompts\n\n1. What codomain is actually claimed?\n2. Which receipt slots are present, missing, repairable, or invalid?\n3. Does any receipt smuggle a target value or infer ambient behavior from high-pressure-only data?\n4. Does the material require rerouting to a non-SC coherent codomain?\n5. What is the next obligation packet and what would change the claim state?\n""",
    }


def pilot_kit_index() -> dict[str, Any]:
    return {
        "schema": "CMAL_PARTNER_PILOT_KIT_INDEX_v2",
        "pilot_lanes": list(PILOT_LANES),
        "template_files": ["MaterialLedger_template.json", "APFMaterialReceipt_template.json"],
        "protocol_cards": sorted(protocol_cards()),
        "nonclaim_guards": dict(PARTNER_PILOT_KIT_NONCLAIM_GUARDS),
        "interpretation": "human-facing pilot kit for CMAL receipts and protocol cards; architecture-only",
    }


def write_pilot_kit(output_dir: str | Path) -> dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    paths: dict[str, str] = {}
    templates = out / "templates"
    cards_dir = out / "protocol_cards"
    templates.mkdir(parents=True, exist_ok=True)
    cards_dir.mkdir(parents=True, exist_ok=True)
    ledger = templates / "MaterialLedger_template.json"
    ledger.write_text(json.dumps(material_ledger_template(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths[ledger.name] = str(ledger)
    receipt = templates / "APFMaterialReceipt_template.json"
    receipt.write_text(json.dumps(material_receipt_template(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths[receipt.name] = str(receipt)
    for name, text in protocol_cards().items():
        p = cards_dir / name
        p.write_text(text, encoding="utf-8")
        paths[name] = str(p)
    brief = out / "CMAL_PARTNER_BRIEF.md"
    brief.write_text(
        "# CMAL Partner Pilot Brief\n\n"
        "CMAL is a Codomain Selection specialization for materials audit, not a new engine or Materials Discovery OS. "
        "The pilot asks collaborators to provide typed ledgers and receipts so APF can classify claim state, issue an obligation packet, and preserve non-claims.\n\n"
        "Hero lanes: rare-earth quantum memory and superconductivity evidence completion / correlated-layer phase-boundary mapping.\n",
        encoding="utf-8",
    )
    paths[brief.name] = str(brief)
    index = out / "PILOT_KIT_INDEX.json"
    index.write_text(json.dumps(pilot_kit_index(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths[index.name] = str(index)
    return paths


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "cmal_partner_pilot_kit"
    print(json.dumps(write_pilot_kit(target), indent=2))

# === merged from coherent_materials_partner_feedback_intake ===
ALLOWED_CODOMAINS = {
    "SC_MATERIAL_ADMISSIBILITY",
    "RARE_EARTH_QUANTUM_MEMORY",
    "CORRELATED_LAYER_PHASE_BOUNDARY",
    "HYDRIDE_PRESSURE_CONDITIONED_SC",
    "STUB_TOPOLOGICAL_MATERIAL",
    "STUB_THERMOELECTRIC",
    "STUB_ION_CONDUCTOR",
}
QUARANTINE_TERMS = {"room_temperature_sc", "new_material_claim", "formula_only_sc_claim", "tc_prediction"}

@dataclass(frozen=True)
class PartnerFeedbackRecord:
    feedback_id: str
    partner_alias: str
    pilot_card_id: str
    material_id: str
    target_codomain: str
    feedback_kind: str
    severity: str
    text: str
    requested_change: str
    receipt_ids: tuple[str, ...]
    nonclaim_guard_ack: bool
    consent_to_route_to_cmal: bool

@dataclass(frozen=True)
class FeedbackIntakeDecision:
    feedback_id: str
    status: str
    route: str
    reasons: tuple[str, ...]
    next_action: str
    nonclaims_preserved: dict[str, int]


def classify_feedback(record: PartnerFeedbackRecord) -> FeedbackIntakeDecision:
    reasons: list[str] = []
    status = "ACCEPTED"
    route = "CMAL_REVIEW_BOARD"
    next_action = "QUEUE_FOR_REVIEW_BOARD"
    if not record.feedback_id or not record.partner_alias:
        reasons.append("missing feedback_id or partner_alias")
        status = "NEEDS_CLARIFICATION"
        next_action = "REQUEST_FEEDBACK_METADATA"
    if not record.pilot_card_id or not record.material_id:
        reasons.append("missing pilot_card_id or material_id")
        status = "NEEDS_CLARIFICATION"
        next_action = "REQUEST_CARD_AND_MATERIAL_ID"
    if not record.nonclaim_guard_ack or not record.consent_to_route_to_cmal:
        reasons.append("partner did not acknowledge nonclaim guard or routing consent")
        status = "NEEDS_CLARIFICATION"
        next_action = "REQUEST_NONCLAIM_ACK_AND_CONSENT"
    if record.target_codomain not in ALLOWED_CODOMAINS:
        reasons.append("target_codomain not exported by active CMAL registry")
        status = "OUT_OF_SCOPE"
        route = "DEFER_SCOPE"
        next_action = "RETURN_WITH_SUPPORTED_CODOMAIN_LIST"
    if record.feedback_kind in QUARANTINE_TERMS:
        reasons.append("feedback kind attempts claim promotion beyond pilot guard")
        status = "QUARANTINED"
        route = "CLAIM_FENCE"
        next_action = "QUARANTINE_AND_REQUIRE_FULL_RECEIPTS"
    if "superconduct" in record.text.lower() and record.target_codomain == "RARE_EARTH_QUANTUM_MEMORY":
        reasons.append("Pearson/QM material text appears to route as superconductivity")
        status = "QUARANTINED"
        route = "CLAIM_FENCE"
        next_action = "REROUTE_TO_QM_OR_REJECT_SC_OVERCLAIM"
    if not reasons:
        reasons.append("feedback admissible for human CMAL review")
    return FeedbackIntakeDecision(
        feedback_id=record.feedback_id,
        status=status,
        route=route,
        reasons=tuple(reasons),
        next_action=next_action,
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


def reference_feedback_batch() -> tuple[PartnerFeedbackRecord, ...]:
    return (
        PartnerFeedbackRecord("FB-QM-001", "rare-earth-lab", "PEARSON_QM_CARD", "NaEu(IO3)4", "RARE_EARTH_QUANTUM_MEMORY", "protocol_clarification", "medium", "Request AFC receipt slot for storage-time/efficiency tradeoff.", "add AFC receipt row", ("QM-AFC-001",), True, True),
        PartnerFeedbackRecord("FB-SC-001", "transport-lab", "SC_EVIDENCE_COMPLETION_CARD", "SC-control-material", "SC_MATERIAL_ADMISSIBILITY", "receipt_request", "high", "Need Meissner and field suppression receipt columns split.", "split bulk-SC receipts", ("SC-RHO-001",), True, True),
        PartnerFeedbackRecord("FB-REPAIR-001", "partner-x", "", "nickelate-template", "CORRELATED_LAYER_PHASE_BOUNDARY", "metadata_gap", "low", "The sweep card lacks sample provenance.", "request sample provenance field", tuple(), True, True),
        PartnerFeedbackRecord("FB-RTSC-001", "anonymous", "SC_CARD", "formula-only-material", "SC_MATERIAL_ADMISSIBILITY", "room_temperature_sc", "critical", "Formula-only room-temperature superconductivity should be announced.", "promote public claim", tuple(), True, True),
        PartnerFeedbackRecord("FB-SCOPE-001", "data-team", "INGESTION_CARD", "mp-candidate", "BATTERY_ION_CONDUCTOR", "new_domain_request", "medium", "Request battery-ion conductor lane.", "add new active codomain", tuple(), True, True),
    )


def summarize_feedback(records: Iterable[PartnerFeedbackRecord]) -> dict:
    decisions = [classify_feedback(r) for r in records]
    counts: dict[str, int] = {}
    for d in decisions:
        counts[d.status] = counts.get(d.status, 0) + 1
    return {
        "schema": "CMAL_PARTNER_FEEDBACK_INTAKE_REPORT_v1",
        "architecture": "CMAL subset Codomain Selection; human feedback only",
        "counts_by_status": counts,
        "decisions": [asdict(d) for d in decisions],
    }


def write_feedback_outputs(out_dir: Path, records: Iterable[PartnerFeedbackRecord] | None = None) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    records = tuple(records or reference_feedback_batch())
    decisions = [classify_feedback(r) for r in records]
    report = summarize_feedback(records)
    report_path = out_dir / "CMAL_PARTNER_FEEDBACK_INTAKE_REPORT.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    csv_path = out_dir / "CMAL_PARTNER_FEEDBACK_QUEUE.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["feedback_id", "status", "route", "next_action", "reasons"])
        for d in decisions:
            w.writerow([d.feedback_id, d.status, d.route, d.next_action, "; ".join(d.reasons)])
    md_path = out_dir / "CMAL_PARTNER_FEEDBACK_SUMMARY.md"
    md_path.write_text("\n".join([
        "# CMAL Partner Feedback Intake Summary",
        "",
        "CMAL remains a Codomain Selection specialization. This intake gate accepts partner feedback for human review and blocks overclaiming.",
        "",
        f"Status counts: `{report['counts_by_status']}`",
        "",
        "No live connector, no autonomous execution, no numeric Tc prediction, no new-material prediction.",
    ]), encoding="utf-8")
    return {p.name: str(p) for p in (report_path, csv_path, md_path)}

# === merged from coherent_materials_pilot_outcome_review_board ===
try:
    from apf.coherent_materials_partner_feedback_intake import PartnerFeedbackRecord, classify_feedback, reference_feedback_batch
except Exception:  # pragma: no cover - pack-local fallback safety
    PartnerFeedbackRecord = None
    classify_feedback = None
    reference_feedback_batch = None

@dataclass(frozen=True)
class ReviewBoardItem:
    feedback_id: str
    board_decision: str
    review_lane: str
    action_owner: str
    required_receipts_or_edits: tuple[str, ...]
    public_release_allowed: bool
    notes: str


def board_decision_for_feedback(record) -> ReviewBoardItem:
    d = classify_feedback(record)
    if d.status == "ACCEPTED" and record.target_codomain == "RARE_EARTH_QUANTUM_MEMORY":
        return ReviewBoardItem(record.feedback_id, "ADVANCE_PILOT_CARD", "RARE_EARTH_QM", "CMAL + partner scientist", ("AFC efficiency/storage-time receipt", "linewidth provenance receipt", "sample stability note"), False, "Advance only inside non-SC quantum-memory lane.")
    if d.status == "ACCEPTED" and record.target_codomain == "SC_MATERIAL_ADMISSIBILITY":
        return ReviewBoardItem(record.feedback_id, "HOLD_FOR_RECEIPTS", "SC_EVIDENCE_COMPLETION", "CMAL reviewer", ("Meissner", "field suppression", "replication", "sample provenance"), False, "Evidence-completion improvement; no Tc or material prediction.")
    if d.status == "NEEDS_CLARIFICATION":
        return ReviewBoardItem(record.feedback_id, "ISSUE_CLARIFICATION", "METADATA_REPAIR", "partner", ("pilot_card_id", "material_id", "nonclaim acknowledgement"), False, "Cannot enter outcome queue until metadata is repaired.")
    if d.status == "QUARANTINED":
        return ReviewBoardItem(record.feedback_id, "QUARANTINE_OVERCLAIM", "CLAIM_FENCE", "CMAL reviewer", ("full receipt bundle", "claim-fence certificate"), False, "Overclaim blocked at pilot boundary.")
    return ReviewBoardItem(record.feedback_id, "DEFER_SCOPE", "UNEXPORTED_CODOMAIN", "architecture review", ("codomain registry proposal", "nonclaim guard"), False, "Requested codomain is not active/exported.")


def reference_review_board() -> tuple[ReviewBoardItem, ...]:
    return tuple(board_decision_for_feedback(r) for r in reference_feedback_batch())


def summarize_review_board(items: Iterable[ReviewBoardItem] | None = None) -> dict:
    items = tuple(items or reference_review_board())
    counts: dict[str, int] = {}
    for item in items:
        counts[item.board_decision] = counts.get(item.board_decision, 0) + 1
    return {
        "schema": "CMAL_PILOT_OUTCOME_REVIEW_BOARD_v1",
        "decision_counts": counts,
        "items": [asdict(i) for i in items],
        "all_public_release_blocked_by_default": all(not i.public_release_allowed for i in items),
    }


def write_review_board_outputs(out_dir: Path) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    items = reference_review_board()
    report = summarize_review_board(items)
    json_path = out_dir / "CMAL_PILOT_OUTCOME_REVIEW_BOARD.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    csv_path = out_dir / "CMAL_REVIEW_BOARD_QUEUE.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["feedback_id", "board_decision", "review_lane", "action_owner", "public_release_allowed", "required_receipts_or_edits"])
        for i in items:
            w.writerow([i.feedback_id, i.board_decision, i.review_lane, i.action_owner, i.public_release_allowed, "; ".join(i.required_receipts_or_edits)])
    md_path = out_dir / "CMAL_REVIEW_BOARD_SUMMARY.md"
    md_path.write_text("\n".join([
        "# CMAL Pilot Outcome Review Board",
        "",
        "Human-reviewed queue. Public release is blocked by default for all pilot feedback items.",
        "",
        f"Decision counts: `{report['decision_counts']}`",
    ]), encoding="utf-8")
    return {p.name: str(p) for p in (json_path, csv_path, md_path)}

# === merged from coherent_materials_pilot_readiness_gate ===
PILOT_READINESS_NONCLAIM_GUARDS: dict[str, int] = {
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
    "experimental_result_claim": 0,
}

REQUIRED_CAPABILITIES: tuple[str, ...] = (
    "material_ledger_template",
    "material_receipt_template",
    "functional_codomain_receipt_cards",
    "receipt_contract_validator",
    "receipt_update_loop",
    "provenance_conflict_auditor",
    "claim_fence_certifier",
    "batch_triage_runner",
    "portfolio_planner",
    "partner_protocol_cards",
)

REQUIRED_FENCES: tuple[str, ...] = (
    "formula_only_claim_quarantine",
    "resistive_only_no_meissner_nonpromotion",
    "Pearson_as_SC_rejection_or_reroute",
    "high_pressure_to_ambient_claim_block",
    "stub_overexport_block",
    "duplicate_or_conflicting_receipt_block",
)

@dataclass(frozen=True)
class ReadinessReport:
    status: str
    ready_for: str
    capabilities_present: tuple[str, ...]
    fences_present: tuple[str, ...]
    blocking_gaps: tuple[str, ...]
    yellow_gaps: tuple[str, ...]
    preserved_nonclaims: Mapping[str, int]
    next_packet: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema": "CMAL_PILOT_READINESS_REPORT_v1",
            "status": self.status,
            "ready_for": self.ready_for,
            "capabilities_present": list(self.capabilities_present),
            "fences_present": list(self.fences_present),
            "blocking_gaps": list(self.blocking_gaps),
            "yellow_gaps": list(self.yellow_gaps),
            "preserved_nonclaims": dict(self.preserved_nonclaims),
            "next_packet": self.next_packet,
            "interpretation": "readiness for human-reviewed internal/partner pilot only; not public discovery OS and not autonomous lab execution",
        }


def evaluate_pilot_readiness(capabilities: tuple[str, ...] | None = None, fences: tuple[str, ...] | None = None, include_live_connector: bool = False, include_autonomous_execution: bool = False) -> ReadinessReport:
    capabilities = capabilities or REQUIRED_CAPABILITIES
    fences = fences or REQUIRED_FENCES
    missing_caps = tuple(c for c in REQUIRED_CAPABILITIES if c not in capabilities)
    missing_fences = tuple(f for f in REQUIRED_FENCES if f not in fences)
    blocking = list(missing_caps) + list(missing_fences)
    if include_live_connector:
        blocking.append("live_connector_not_allowed_in_core_readiness_gate")
    if include_autonomous_execution:
        blocking.append("autonomous_execution_not_allowed")
    yellow = (
        "no independent external lab receipts yet",
        "no live OPTIMADE/MaterialsProject/SuperCon/GNoME connector by design",
        "not a public-facing Materials Discovery OS",
        "partner safety/protocol compliance remains external to APF",
    )
    status = "PARTNER_PILOT_READY_WITH_GUARDS" if not blocking else "NOT_READY"
    return ReadinessReport(
        status=status,
        ready_for="human-reviewed non-live partner pilot" if not blocking else "blocked until missing capabilities/fences are supplied",
        capabilities_present=tuple(capabilities),
        fences_present=tuple(fences),
        blocking_gaps=tuple(blocking),
        yellow_gaps=yellow,
        preserved_nonclaims=PILOT_READINESS_NONCLAIM_GUARDS,
        next_packet="CMAL_PARTNER_PILOT_PACKET_v1" if not blocking else "CMAL_BLOCKER_REPAIR_PACKET_v1",
    )


def reference_readiness_report() -> ReadinessReport:
    return evaluate_pilot_readiness()


def write_readiness_outputs(output_dir: str | Path, report: ReadinessReport | None = None) -> dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    report = report or reference_readiness_report()
    paths: dict[str, str] = {}
    report_path = out / "CMAL_PILOT_READINESS_REPORT.json"
    report_path.write_text(json.dumps(report.to_dict(), indent=2, ensure_ascii=False), encoding="utf-8")
    paths[report_path.name] = str(report_path)
    summary = out / "CMAL_PILOT_READINESS_SUMMARY.md"
    lines = [
        "# CMAL Pilot Readiness Summary", "",
        f"**Status:** `{report.status}`", f"**Ready for:** {report.ready_for}", f"**Next packet:** `{report.next_packet}`", "",
        "## Green checks", "",
    ]
    lines += [f"- {c}" for c in report.capabilities_present]
    lines += ["", "## Claim fences", ""]
    lines += [f"- {f}" for f in report.fences_present]
    lines += ["", "## Yellow gaps", ""]
    lines += [f"- {g}" for g in report.yellow_gaps]
    lines += ["", "## Preserved non-claims", ""]
    lines += [f"- `{k} = {v}`" for k, v in report.preserved_nonclaims.items()]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    paths[summary.name] = str(summary)
    packet = out / "CMAL_PARTNER_PILOT_PACKET_v1.md"
    packet.write_text(
        "# CMAL Partner Pilot Packet v1\n\n"
        "Use this packet only for human-reviewed, non-live CMAL pilots. Required bundle: material ledger template, APFMaterialReceipt template, protocol card, claim-fence summary, portfolio plan, and non-claim ledger.\n\n"
        "Do not represent this as APF-Mat OS, autonomous lab execution, material prediction, numeric Tc prediction, or Pearson superconductivity.\n",
        encoding="utf-8",
    )
    paths[packet.name] = str(packet)
    return paths


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "cmal_pilot_readiness_outputs"
    print(json.dumps(write_readiness_outputs(target), indent=2))

# === merged from coherent_materials_release_governance_gate ===
PRESERVED_NONCLAIMS = {
    "APF_Mat_sixth_engine": 0,
    "materials_discovery_OS": 0,
    "materials_live_ingestion_connector": 0,
    "materials_public_ingestion_core": 0,
    "autonomous_lab_execution": 0,
    "SC_numeric_Tc": 0,
    "SC_new_material_prediction": 0,
    "SC_ab_initio_chemistry": 0,
    "Pearson_superconductivity_claim": 0,
    "room_temperature_superconductivity": 0,
    "unreviewed_public_release": 0,
}

@dataclass(frozen=True)
class ReleaseRequest:
    release_id: str
    channel: str
    artifact_label: str
    includes_new_material_claim: bool
    includes_live_connector: bool
    includes_autonomous_execution: bool
    includes_numeric_Tc_prediction: bool
    ip_clearance_recorded: bool
    human_review_recorded: bool
    nonclaim_guard_present: bool

@dataclass(frozen=True)
class ReleaseDecision:
    release_id: str
    status: str
    allowed_channel: str
    blockers: tuple[str, ...]
    required_next_actions: tuple[str, ...]
    preserved_nonclaims: dict[str, int]


def evaluate_release_request(req: ReleaseRequest) -> ReleaseDecision:
    blockers: list[str] = []
    actions: list[str] = []
    allowed = req.channel
    if req.includes_live_connector:
        blockers.append("live ingestion connector not exported by CMAL")
        actions.append("convert to external APFMaterialReceipt contract only")
    if req.includes_autonomous_execution:
        blockers.append("autonomous lab execution not exported")
        actions.append("route to human-reviewed partner pilot only")
    if req.includes_numeric_Tc_prediction:
        blockers.append("numeric Tc prediction not exported")
        actions.append("remove Tc prediction or recast as receipt requirement")
    if req.includes_new_material_claim:
        blockers.append("new material prediction / public claim not exported")
        actions.append("route to claim-fence certificate and receipt bundle")
    if not req.nonclaim_guard_present:
        blockers.append("nonclaim guard missing")
        actions.append("attach CMAL nonclaim ledger")
    if req.channel in {"PUBLIC_PREPRINT", "PUBLIC_DECK", "PRESS_RELEASE"} and not req.ip_clearance_recorded:
        blockers.append("public channel requires IP clearance")
        actions.append("record IP/counsel clearance before public release")
    if req.channel in {"PARTNER_PILOT", "INTERNAL_BANK"} and not req.human_review_recorded:
        blockers.append("human review missing")
        actions.append("record human review board decision")
    if blockers:
        if req.channel in {"PARTNER_PILOT", "INTERNAL_BANK"} and all("human review" in b or "nonclaim" in b for b in blockers):
            status = "REPAIRABLE_BEFORE_RELEASE"
        else:
            status = "BLOCKED"
            allowed = "NONE"
    else:
        if req.channel == "INTERNAL_BANK":
            status = "ALLOW_INTERNAL_BANK"
        elif req.channel == "PARTNER_PILOT":
            status = "ALLOW_PARTNER_PILOT_WITH_GUARDS"
        else:
            status = "ALLOW_ONLY_IF_PUBLIC_REVIEW_MINUTES_EXIST"
    return ReleaseDecision(req.release_id, status, allowed, tuple(blockers), tuple(actions), PRESERVED_NONCLAIMS.copy())


def reference_release_requests() -> tuple[ReleaseRequest, ...]:
    return (
        ReleaseRequest("REL-INT-001", "INTERNAL_BANK", "CMAL feedback-release pack", False, False, False, False, True, True, True),
        ReleaseRequest("REL-PILOT-001", "PARTNER_PILOT", "CMAL partner pilot packet", False, False, False, False, True, True, True),
        ReleaseRequest("REL-PUBLIC-001", "PUBLIC_DECK", "materials revolution deck", False, False, False, False, False, True, True),
        ReleaseRequest("REL-LIVE-001", "PARTNER_PILOT", "Materials Project live connector", False, True, False, False, True, True, True),
        ReleaseRequest("REL-AUTO-001", "PARTNER_PILOT", "self-driving lab action runner", False, False, True, False, True, True, True),
        ReleaseRequest("REL-TC-001", "PUBLIC_PREPRINT", "new high-Tc material note", True, False, False, True, False, True, True),
    )


def summarize_release_governance(reqs: tuple[ReleaseRequest, ...] | None = None) -> dict:
    reqs = reqs or reference_release_requests()
    decisions = [evaluate_release_request(r) for r in reqs]
    counts: dict[str, int] = {}
    for d in decisions:
        counts[d.status] = counts.get(d.status, 0) + 1
    return {
        "schema": "CMAL_RELEASE_GOVERNANCE_GATE_v1",
        "formal_placement": "CMAL subset Codomain Selection; not APF-Mat OS or sixth engine",
        "decision_counts": counts,
        "decisions": [asdict(d) for d in decisions],
        "preserved_nonclaims": PRESERVED_NONCLAIMS,
    }


def write_release_governance_outputs(out_dir: Path) -> dict[str, str]:
    out_dir.mkdir(parents=True, exist_ok=True)
    report = summarize_release_governance()
    json_path = out_dir / "CMAL_RELEASE_GOVERNANCE_REPORT.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path = out_dir / "CMAL_RELEASE_GOVERNANCE_SUMMARY.md"
    md_path.write_text("\n".join([
        "# CMAL Release Governance Summary",
        "",
        "Internal bank and guarded partner-pilot release are allowed when human review and nonclaim guards are recorded.",
        "Public, live-connector, autonomous-execution, numeric-Tc, and new-material-prediction channels remain blocked unless separately cleared by future architecture and IP review.",
        "",
        f"Decision counts: `{report['decision_counts']}`",
        "",
        "Preserved nonclaims: all zero-export guards remain zero.",
    ]), encoding="utf-8")
    return {p.name: str(p) for p in (json_path, md_path)}
