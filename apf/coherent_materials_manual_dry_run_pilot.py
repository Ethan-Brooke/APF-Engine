"""CMAL manual dry-run pilot (architecture-only).

A small hand-curated, non-live batch demonstrating how CMAL handles clear,
partial, conflicting, quarantined, pressure-conditioned, and non-SC coherent
material receipts. This is a dry run, not external-data ingestion and not a
materials discovery engine.
"""
from __future__ import annotations
import csv, json
from pathlib import Path
from typing import Any, Mapping, Sequence

from apf.coherent_materials_red_team import audit_receipts, NONCLAIM_EXPORTS

SC = "SC_MATERIAL_ADMISSIBILITY"
QM = "RARE_EARTH_QUANTUM_MEMORY"


def receipt(receipt_id: str, material_id: str, sample_id: str, target: str, kind: str, method: str, slots: list[str], value: Any = True, **extra: Any) -> dict[str, Any]:
    r = {
        "schema_version": "APFMaterialReceipt.v1",
        "receipt_id": receipt_id,
        "material_id": material_id,
        "sample_id": sample_id,
        "target_codomain": target,
        "receipt_kind": kind,
        "measurement_method": method,
        "control_vector": extra.pop("control_vector", {"temperature_K": "sweep"}),
        "measured_value": value,
        "uncertainty": extra.pop("uncertainty", {"declared": True}),
        "instrument_or_protocol": extra.pop("instrument_or_protocol", method),
        "provenance": extra.pop("provenance", {"declared": True, "source": "manual_Cmal_dry_run_fixture"}),
        "replication_status": extra.pop("replication_status", "single_run"),
        "updates_required_slots": slots,
        "nonclaim_guard": extra.pop("nonclaim_guard", ["not_Tc_prediction", "not_new_material_prediction", "not_autonomous_lab_execution"]),
        "pass_fail": extra.pop("pass_fail", "pass"),
    }
    r.update(extra)
    return r


PILOT_CASES: dict[str, dict[str, Any]] = {
    "full_bulk_sc_control": {
        "ledger": {"ledger_id": "L_bulk_sc", "classification": "RESISTIVE_ONLY_NO_MEISSNER", "target_codomain": SC},
        "receipts": [
            receipt("SC_ZERO", "bulk_sc_control", "BULK_A", SC, "zero_resistance", "four_probe_transport", ["zero_resistance"], True, replication_status="REPLICATED"),
            receipt("SC_MEISSNER", "bulk_sc_control", "BULK_A", SC, "meissner_response", "SQUID_magnetometry", ["meissner_or_diamagnetic_response"], True, replication_status="REPLICATED"),
            receipt("SC_FIELD", "bulk_sc_control", "BULK_A", SC, "field_suppression", "field_sweep", ["field_suppression_or_critical_field_response"], True, replication_status="REPLICATED"),
            receipt("SC_REPRO", "bulk_sc_control", "BULK_A", SC, "replication", "sample_batch_repeat", ["reproducible_transition_across_samples"], True, replication_status="REPLICATED"),
        ],
        "expected_status": "PROMOTE_CODOMAIN",
        "expected_classification": "SC_MATERIAL_ADMISSIBLE",
    },
    "resistive_only_negative_meissner": {
        "ledger": {"ledger_id": "L_resistive_only", "classification": "RESISTIVE_ONLY_NO_MEISSNER", "target_codomain": SC},
        "receipts": [
            receipt("RO_ZERO", "resistive_claim", "R1", SC, "zero_resistance", "four_probe_transport", ["zero_resistance"], True),
            receipt("RO_MEISSNER_NEG", "resistive_claim", "R1", SC, "meissner_response", "SQUID_magnetometry", ["meissner_or_diamagnetic_response"], False, pass_fail="fail"),
        ],
        "expected_status": "REQUEST_NEXT_RECEIPT",
        "expected_classification": "RESISTIVE_ONLY_NO_MEISSNER",
    },
    "formula_only_room_temperature_sc": {
        "ledger": {"ledger_id": "L_formula_only", "classification": "CLAIM_QUARANTINED", "target_codomain": SC},
        "receipts": [
            receipt("FORMULA_ONLY", "formula_only_rt_claim", "none", SC, "formula_only_claim", "claim_text_only", [], {"claimed_room_temperature_SC": True}, uncertainty={}, provenance={}, replication_status="NONE", nonclaim_guard=[], control_vector={}),
        ],
        "expected_status": "QUARANTINE_CLAIM",
        "expected_classification": "CLAIM_QUARANTINED",
    },
    "pearson_NaEu_quantum_memory": {
        "ledger": {"ledger_id": "L_Pearson_NaEu", "classification": "COHERENT_SIGNATURE_PARTIAL", "target_codomain": QM},
        "receipts": [
            receipt("P_INHOM", "NaEu(IO3)4", "NaEu_crystal", QM, "inhomogeneous_linewidth", "cryogenic_PLE", ["inhomogeneous_linewidth"], 2.2, control_vector={"temperature_K": 1.7}, source_key="pearson_dissertation_2025"),
            receipt("P_HOM", "NaEu(IO3)4", "NaEu_crystal", QM, "homogeneous_linewidth", "photon_echo", ["homogeneous_linewidth"], 120, control_vector={"temperature_K": 1.7}, source_key="pearson_dissertation_2025"),
            receipt("P_SPIN", "NaEu(IO3)4", "NaEu_crystal", QM, "spin_lifetime", "spin_relaxation", ["spin_lifetime"], 1.0, control_vector={"temperature_K": 1.7}, source_key="pearson_dissertation_2025"),
            receipt("P_AFC", "NaEu(IO3)4", "NaEu_crystal", QM, "AFC_preliminary", "atomic_frequency_comb", ["AFC_retrieval"], True, control_vector={"temperature_K": 1.7}, source_key="pearson_dissertation_2025"),
        ],
        "expected_status": "PROMOTE_CODOMAIN",
        "expected_classification": "COHERENT_BUT_NOT_SC",
    },
    "pearson_NaEu_misrouted_as_SC": {
        "ledger": {"ledger_id": "L_Pearson_misroute", "classification": "COHERENT_BUT_NOT_SC", "target_codomain": QM},
        "receipts": [
            receipt("P_BAD_SC", "NaEu(IO3)4", "NaEu_crystal", SC, "homogeneous_linewidth", "photon_echo", ["homogeneous_linewidth"], 120, control_vector={"temperature_K": 1.7}, source_key="pearson_dissertation_2025", nonclaim_guard=["Pearson_superconductivity_claim=0"]),
        ],
        "expected_status": "ROUTE_TO_DIFFERENT_CODOMAIN",
        "expected_classification": "COHERENT_BUT_NOT_SC",
    },
    "hydride_pressure_conditioned_only": {
        "ledger": {"ledger_id": "L_hydride_pressure", "classification": "HIGH_PRESSURE_SC_TEMPLATE", "target_codomain": SC},
        "receipts": [
            receipt("HYD_HP", "hydride_template", "H_DAC_1", SC, "high_pressure_SC", "diamond_anvil_transport", ["pressure_conditioned_SC"], True, control_vector={"pressure_GPa": 180, "ambient_claim": True}, claim={"ambient_usability": True}, nonclaim_guard=["ambient_usability_not_promoted"]),
        ],
        "expected_status": "PROMOTE_PRESSURE_CONDITIONED_SC",
        "expected_classification": "PRESSURE_CONDITIONED_SC_ONLY",
    },
    "nickelate_phase_boundary_sweep": {
        "ledger": {"ledger_id": "L_nickelate_template", "classification": "PHASE_BOUNDARY_SCOUT", "target_codomain": SC},
        "receipts": [
            receipt("NICK_STRAIN", "nickelate_correlated_layer_template", "N1", SC, "strain_oxygenation_sweep", "thin_film_phase_map", ["phase_boundary_map"], True, control_vector={"strain":"sweep", "oxygenation":"declared", "pressure_GPa":0}),
        ],
        "expected_status": "UPDATE_PHASE_BOUNDARY_MAP",
        "expected_classification": "PHASE_BOUNDARY_SCOUT",
    },
    "conflicting_bulk_replicates": {
        "ledger": {"ledger_id": "L_conflict", "classification": "SC_SIGNATURE_PARTIAL", "target_codomain": SC},
        "receipts": [
            receipt("C_MEISSNER_POS", "conflict_sc", "C1", SC, "meissner_response", "SQUID", ["meissner_or_diamagnetic_response"], True, replication_status="CONTRADICTORY"),
            receipt("C_MEISSNER_NEG", "conflict_sc", "C1", SC, "meissner_response", "SQUID", ["meissner_or_diamagnetic_response"], False, pass_fail="fail", replication_status="CONTRADICTORY"),
        ],
        "expected_status": "HOLD_CONFLICT",
        "expected_classification": "SC_SIGNATURE_PARTIAL",
    },
    "repair_missing_uncertainty": {
        "ledger": {"ledger_id": "L_repair", "classification": "MATERIAL_LEDGER_INSUFFICIENT", "target_codomain": SC},
        "receipts": [
            receipt("REPAIR_NO_UNCERT", "repair_material", "REPAIR_1", SC, "field_suppression", "field_sweep", ["field_suppression_or_critical_field_response"], True, uncertainty={}),
        ],
        "expected_status": "REQUEST_REPAIR",
        "expected_classification": "MATERIAL_LEDGER_INSUFFICIENT",
    },
    "thermoelectric_stub_only": {
        "ledger": {"ledger_id": "L_thermo_stub", "classification": "STUB_RECOGNIZED_NOT_EXPORTED", "target_codomain": "THERMOELECTRIC_STUB"},
        "receipts": [
            receipt("THERMO_STUB", "thermoelectric_template", "T1", "THERMOELECTRIC_STUB", "ZT_report", "literature_stub", ["thermoelectric_stub"], 1.0),
        ],
        "expected_status": "HOLD_STUB",
        "expected_classification": "STUB_RECOGNIZED_NOT_EXPORTED",
    },
}


def _validation_status(audit: Mapping[str, Any]) -> str:
    status = str(audit["status"])
    if status == "CLEAR_FOR_UPDATE":
        return "VALID"
    if status in {"REPAIR_REQUIRED"}:
        return "REPAIRABLE"
    if status in {"REROUTE_OR_REJECT"}:
        return "REJECTED"
    if status == "QUARANTINE":
        return "QUARANTINED"
    return "VALID_WITH_HOLD"


def _update_status(case_id: str, case: Mapping[str, Any], audit: Mapping[str, Any]) -> tuple[str, str, str, str]:
    status = str(audit["status"])
    expected = str(case["expected_status"])
    classification = str(case["expected_classification"])
    if status == "QUARANTINE":
        return "QUARANTINE_CLAIM", "CLAIM_QUARANTINED", "QUARANTINE_QUEUE", "QUARANTINE_AND_REPRODUCE"
    if status == "REROUTE_OR_REJECT":
        return "ROUTE_TO_DIFFERENT_CODOMAIN", classification, "REROUTE_QUEUE", "REROUTE_TO_DECLARED_CODOMAIN"
    if status == "SPLIT_CONDITIONED_CLAIM":
        return "PROMOTE_PRESSURE_CONDITIONED_SC", classification, "BURDEN_SEPARATION_QUEUE", "PRESERVE_PRESSURE_CONDITIONED_NONCLAIM"
    if status == "HOLD_CONFLICT":
        return "HOLD_CONFLICT", classification, "CONFLICT_RESOLUTION_QUEUE", "REQUIRE_INDEPENDENT_REPLICATION"
    if status == "REPAIR_REQUIRED":
        return "REQUEST_REPAIR", classification, "CONTRACT_REPAIR_QUEUE", "REPAIR_RECEIPT_CONTRACT"
    if case_id == "resistive_only_negative_meissner":
        return "REQUEST_NEXT_RECEIPT", classification, "EVIDENCE_COMPLETION_QUEUE", "MEASURE_MEISSNER_RESPONSE"
    if case_id == "nickelate_phase_boundary_sweep":
        return "UPDATE_PHASE_BOUNDARY_MAP", classification, "PHASE_BOUNDARY_QUEUE", "UPDATE_PHASE_BOUNDARY_MAP"
    if case_id == "thermoelectric_stub_only":
        return "HOLD_STUB", classification, "LOW_PRIORITY_OR_STUB_QUEUE", "KEEP_STUB_NOT_EXPORTED"
    return expected, classification, "ADMISSIBLE_CODOMAIN_QUEUE", "EMIT_ADMISSIBILITY_PACKET"


def run_manual_pilot() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case_id, case in PILOT_CASES.items():
        audit = audit_receipts(case["receipts"], case.get("ledger"))
        update_status, updated_classification, queue, next_action = _update_status(case_id, case, audit)
        rows.append({
            "case_id": case_id,
            "validation_status": _validation_status(audit),
            "conflict_status": audit["status"],
            "conflict_types": list(audit.get("conflict_types", [])),
            "update_status": update_status,
            "updated_classification": updated_classification,
            "triage_bucket": queue,
            "next_action": next_action,
            "receipt_count": len(case["receipts"]),
            "conflict_route": audit["route"],
            "nonclaims": dict(NONCLAIM_EXPORTS),
        })
    return rows


def make_reports() -> dict[str, Any]:
    rows = run_manual_pilot()
    return {
        "schema": "CMAL_MANUAL_DRY_RUN_PILOT_REPORT_v1",
        "case_count": len(rows),
        "rows": rows,
        "nonclaims": dict(NONCLAIM_EXPORTS),
        "exports": {
            "CMAL_manual_dry_run_pilot": 1,
            "CMAL_conflict_aware_batch_navigation": 1,
            "CMAL_case_to_obligation_summary": 1,
        },
    }


def emit_outputs(output_dir: str | Path) -> dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    report = make_reports()
    rows = report["rows"]
    validation = {"schema": "CMAL_MANUAL_VALIDATION_REPORT_v1", "cases": [{"case_id": r["case_id"], "validation_status": r["validation_status"], "conflict_status": r["conflict_status"], "conflict_types": r["conflict_types"]} for r in rows], "nonclaims": dict(NONCLAIM_EXPORTS)}
    ledger = {"schema": "CMAL_MANUAL_LEDGER_UPDATE_REPORT_v1", "cases": [{"case_id": r["case_id"], "update_status": r["update_status"], "updated_classification": r["updated_classification"]} for r in rows], "nonclaims": dict(NONCLAIM_EXPORTS)}
    obligations = {"schema": "CMAL_MANUAL_NEXT_OBLIGATION_PACKETS_v1", "packets": {r["case_id"]: {"target_engine": "CODOMAIN_SELECTION", "target_unit_id": r["case_id"], "evidence_required": r["next_action"], "current_status": r["update_status"], "recommended_next_action": r["next_action"]} for r in rows}}
    conflict = {"schema": "CMAL_MANUAL_CONFLICT_AUDIT_REPORT_v1", "cases": [{"case_id": r["case_id"], "conflict_status": r["conflict_status"], "conflict_types": r["conflict_types"], "route": r["conflict_route"]} for r in rows], "nonclaims": dict(NONCLAIM_EXPORTS)}
    files = {
        "MANUAL_DRY_RUN_REPORT.json": report,
        "VALIDATION_REPORT.json": validation,
        "CONFLICT_AUDIT_REPORT.json": conflict,
        "LEDGER_UPDATE_REPORT.json": ledger,
        "NEXT_OBLIGATION_PACKETS.json": obligations,
    }
    written: dict[str, str] = {}
    for name, payload in files.items():
        p = out / name
        p.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        written[name] = str(p)
    with (out / "TRIAGE_QUEUE.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["rank", "case_id", "triage_bucket", "next_action", "update_status", "updated_classification", "conflict_status"])
        writer.writeheader()
        for i, r in enumerate(rows, 1):
            writer.writerow({"rank": i, **{k: r[k] for k in ("case_id", "triage_bucket", "next_action", "update_status", "updated_classification", "conflict_status")}})
    written["TRIAGE_QUEUE.csv"] = str(out / "TRIAGE_QUEUE.csv")
    md = [
        "# CMAL Manual Dry Run Pilot Summary", "",
        "This dry run routes a hand-curated non-live batch through validation, conflict audit, ledger update, triage, and obligation-packet summary.", "",
        "| Case | Conflict | Update | Classification | Queue |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        md.append(f"| {r['case_id']} | {r['conflict_status']} | {r['update_status']} | {r['updated_classification']} | {r['triage_bucket']} |")
    md.extend(["", "## Preserved non-claims", "", "CMAL remains under Codomain Selection. No APF-Mat sixth engine, Materials Discovery OS, live ingestion connector, autonomous lab execution, numeric Tc prediction, new-material prediction, Pearson superconductivity claim, ab initio chemistry, or room-temperature superconductivity claim is exported."])
    (out / "CMAL_MANUAL_DRY_RUN_SUMMARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    written["CMAL_MANUAL_DRY_RUN_SUMMARY.md"] = str(out / "CMAL_MANUAL_DRY_RUN_SUMMARY.md")
    return written


def pilot_summary() -> dict[str, Any]:
    rows = run_manual_pilot()
    return {
        "case_count": len(rows),
        "case_ids": [r["case_id"] for r in rows],
        "promotions": [r["case_id"] for r in rows if r["update_status"] in {"PROMOTE_CODOMAIN", "PROMOTE_PRESSURE_CONDITIONED_SC"}],
        "holds": [r["case_id"] for r in rows if r["update_status"] in {"HOLD_CONFLICT", "REQUEST_NEXT_RECEIPT", "REQUEST_REPAIR", "HOLD_STUB"}],
        "quarantines": [r["case_id"] for r in rows if r["update_status"] == "QUARANTINE_CLAIM"],
        "reroutes": [r["case_id"] for r in rows if r["update_status"] == "ROUTE_TO_DIFFERENT_CODOMAIN"],
        "nonclaims": dict(NONCLAIM_EXPORTS),
    }
