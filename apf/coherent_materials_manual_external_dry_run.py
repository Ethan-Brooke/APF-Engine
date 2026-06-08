"""CMAL manual external-data dry run (architecture-only).

Defines a small hand-curated external-like receipt batch and runs it through the
CMAL validator -> receipt-update loop -> triage -> obligation packet -> trace
certificate chain. This is explicitly not a live connector, not scraping, not a
public ingestion core, and not autonomous lab execution.
"""
from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping
import csv
import json

from apf.coherent_materials_golden_receipt_benchmark import get_case
from apf.coherent_materials_batch_triage_runner import run_case
from apf.coherent_materials_receipt_trace_certificates import build_trace_certificate, certificates_to_report

PEARSON_SOURCE_ANCHORS = {
    "abstract": "PEARSONJR-DISSERTATION-2025.pdf abstract: rare-earth solids for quantum memory; inhomogeneous broadening as central obstacle; NaEu(IO3)4 linewidth/coherence/AFC receipts",
    "chapter7": "PEARSONJR-DISSERTATION-2025.pdf Chapter 7: NaEu(IO3)4 narrow optical linewidths, photon echoes, spectral holes, AFC retrieval",
    "chapter6_caution": "PEARSONJR-DISSERTATION-2025.pdf Chapter 6: EF/EF·FA MOF stability/dephasing caution receipts",
}

NONCLAIMS: dict[str, int] = {
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


def _tag_case(case: Mapping[str, Any], source_anchor: str, source_type: str = "manual_external_fixture") -> dict[str, Any]:
    c = deepcopy(case)
    c.setdefault("ledger", {}).setdefault("provenance", {})["source"] = source_anchor
    c.setdefault("ledger", {}).setdefault("provenance", {})["source_type"] = source_type
    for r in c.get("receipts", ()): 
        r.setdefault("provenance", {})["source_anchor"] = source_anchor
        r.setdefault("provenance", {})["source_type"] = source_type
        r.setdefault("provenance", {})["declared"] = True
    return c


def _pearson_caution_case() -> dict[str, Any]:
    return {
        "description": "Pearson EF/EF·FA rare-earth material caution route: stability, dephasing, and incomplete coherence receipts block promotion.",
        "expected": {
            "batch_route": "LEDGER_UPDATED",
            "updated_classification": "DEFECT_OR_INHOMOGENEITY_OVERLOADED",
        },
        "ledger": {
            "ledger_id": "ledger_pearson_ef_ef_fa_caution_manual_external",
            "classification": "DEFECT_OR_INHOMOGENEITY_OVERLOADED",
            "material": {"composition": "EF / EF_FA europium formate rare-earth MOF", "structure_known": True, "structure": "declared"},
            "material_family": "rare_earth_quantum_memory_caution",
            "coherence_type": "quantum_memory",
            "controls": {"temperature_K": 1.4},
            "evidence": {"coherence_signature": False, "stability_issue": True, "inhomogeneous_linewidth_GHz_range": [7.1, 9.7]},
            "burdens": {"inhomogeneity": 0.85, "stability": 0.9, "synthesis": 0.65},
            "scores": {"fragmented_or_normal_cost": 3.0, "coherent_cost": 5.0},
            "provenance": {"declared": True, "source": PEARSON_SOURCE_ANCHORS["chapter6_caution"], "source_type": "manual_external_fixture"},
            "top_action": "REDUCE_INHOMOGENEITY",
        },
        "receipts": [
            {
                "schema_version": "APFMaterialReceipt.v1",
                "receipt_id": "R-PEARSON-EF-FA-STABILITY-CAUTION",
                "material_id": "Pearson_EF_EF_FA",
                "sample_id": "EF_FA_MOF_reported_samples",
                "target_codomain": "RARE_EARTH_QUANTUM_MEMORY",
                "receipt_kind": "rare_earth_qm_caution_bundle",
                "measurement_method": "photoluminescence_and_material_stability_report",
                "control_vector": {"temperature_K": 1.4},
                "measured_value": {"inhomogeneous_linewidth_GHz_range": [7.1, 9.7], "air_decomposition_reported": True, "spectral_hole_burning_or_echo_completed": False},
                "uncertainty": {"declared": True},
                "instrument_or_protocol": "Pearson thesis Chapter 6 / Chapter 8 follow-up",
                "provenance": {"declared": True, "source_anchor": PEARSON_SOURCE_ANCHORS["chapter6_caution"], "source_type": "manual_external_fixture"},
                "replication_status": "THESIS_REPORTED",
                "updates_required_slots": ["stability", "synthesis_provenance"],
                "nonclaim_guard": ["not_superconductivity", "not_promotable_quantum_memory", "burden_overloaded"],
                "pass_fail": "fail",
                "contradicts_prior": False,
            }
        ],
    }


def _build_manual_cases() -> dict[str, dict[str, Any]]:
    cases: dict[str, dict[str, Any]] = {}
    cases["pearson_naeuiO3_4_thesis_qm_receipts"] = _tag_case(
        get_case("pearson_NaEu_quantum_memory_promote_nonSC"), PEARSON_SOURCE_ANCHORS["chapter7"]
    )
    cases["pearson_naeuiO3_4_misrouted_as_sc"] = _tag_case(
        get_case("pearson_NaEu_misrouted_as_SC_reject"), PEARSON_SOURCE_ANCHORS["chapter7"]
    )
    cases["pearson_ef_ef_fa_caution_burden"] = _pearson_caution_case()
    cases["manual_bulk_sc_control_receipts"] = _tag_case(
        get_case("full_bulk_sc_receipts_promote"), "manual external fixture: bulk SC control receipts"
    )
    cases["manual_resistive_only_sc_claim"] = _tag_case(
        get_case("resistive_only_missing_meissner_hold"), "manual external fixture: resistive-only SC claim"
    )
    cases["manual_hydride_pressure_conditioned"] = _tag_case(
        get_case("hydride_pressure_conditioned_SC_only"), "manual external fixture: high-pressure hydride template"
    )
    cases["manual_ambient_claim_from_pressure_only"] = _tag_case(
        get_case("ambient_claim_from_high_pressure_quarantine"), "manual external fixture: ambient claim from high-pressure receipt"
    )
    cases["manual_nickelate_phase_boundary_sweep"] = _tag_case(
        get_case("nickelate_phase_boundary_update_no_prediction"), "manual external fixture: nickelate-style strain/oxygenation/pressure sweep"
    )
    return cases

MANUAL_EXTERNAL_CASES: dict[str, dict[str, Any]] = _build_manual_cases()


def iter_manual_cases():
    return MANUAL_EXTERNAL_CASES.items()


def run_manual_external_dry_run() -> list[Any]:
    return [run_case(case_id, case) for case_id, case in iter_manual_cases()]


def build_manual_trace_certificates(results: list[Any] | None = None):
    results = results or run_manual_external_dry_run()
    certs = []
    for (case_id, case), result in zip(iter_manual_cases(), results):
        certs.append(build_trace_certificate(case_id, case, result))
    return certs


def make_reports(results: list[Any] | None = None) -> dict[str, Any]:
    results = results or run_manual_external_dry_run()
    certs = build_manual_trace_certificates(results)
    rows = [r.to_dict() for r in results]
    return {
        "validation_report": {
            "schema": "CMAL_MANUAL_EXTERNAL_VALIDATION_REPORT_v1",
            "case_count": len(rows),
            "cases": rows,
            "preserved_nonclaims": dict(NONCLAIMS),
        },
        "ledger_update_report": {
            "schema": "CMAL_MANUAL_EXTERNAL_LEDGER_UPDATE_REPORT_v1",
            "case_results": rows,
            "promotions": [r["case_id"] for r in rows if r["update_status"] in {"PROMOTE_CODOMAIN", "PROMOTE_PRESSURE_CONDITIONED_SC"}],
            "quarantines": [r["case_id"] for r in rows if r["update_status"] == "QUARANTINE_CLAIM"],
            "reroutes": [r["case_id"] for r in rows if r["update_status"] == "ROUTE_TO_DIFFERENT_CODOMAIN"],
            "preserved_nonclaims": dict(NONCLAIMS),
        },
        "obligation_packets": {
            "schema": "CMAL_MANUAL_EXTERNAL_NEXT_OBLIGATION_PACKETS_v1",
            "packets": {r["case_id"]: r["obligation_packet"] for r in rows},
        },
        "trace_certificates": certificates_to_report(certs),
    }


def write_manual_dry_run_outputs(output_dir: str | Path) -> dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results = run_manual_external_dry_run()
    reports = make_reports(results)
    paths: dict[str, str] = {}
    for name, payload in [
        ("VALIDATION_REPORT.json", reports["validation_report"]),
        ("LEDGER_UPDATE_REPORT.json", reports["ledger_update_report"]),
        ("NEXT_OBLIGATION_PACKETS.json", reports["obligation_packets"]),
        ("TRACE_CERTIFICATES.json", reports["trace_certificates"]),
    ]:
        path = out / name
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        paths[name] = str(path)
    triage_path = out / "TRIAGE_QUEUE.csv"
    with triage_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["rank", "case_id", "triage_bucket", "next_action", "batch_route", "update_status", "updated_classification"])
        writer.writeheader()
        for i, r in enumerate(results, 1):
            d = r.to_dict()
            writer.writerow({"rank": i, "case_id": d["case_id"], "triage_bucket": d["triage_bucket"], "next_action": d["next_action"], "batch_route": d["batch_route"], "update_status": d["update_status"], "updated_classification": d["updated_classification"]})
    paths["TRIAGE_QUEUE.csv"] = str(triage_path)
    summary = out / "CMAL_MANUAL_EXTERNAL_DRY_RUN_SUMMARY.md"
    lines = [
        "# CMAL Manual External Dry Run Summary",
        "",
        "This dry run uses hand-curated APFMaterialReceipt fixtures. It does not implement live Materials Project, OPTIMADE, GNoME, SuperCon, web scraping, or autonomous-lab ingestion.",
        "",
        f"Case count: {len(results)}",
        "",
        "| Case | Route | Update | Classification | Queue | Next action |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        d = r.to_dict()
        lines.append(f"| {d['case_id']} | {d['batch_route']} | {d['update_status']} | {d['updated_classification']} | {d['triage_bucket']} | {d['next_action']} |")
    lines.extend([
        "",
        "## Pearson source lane",
        "",
        "NaEu(IO3)4 routes to rare-earth quantum memory / coherent material receipts, not superconductivity. EF/EF·FA routes to caution/burden handling. Pearson-superconductivity export remains 0.",
        "",
        "## Preserved non-claims",
        "",
        "CMAL remains a Codomain Selection specialization. No APF-Mat sixth engine, Materials Discovery OS, live connector, public ingestion core, autonomous-lab execution, numeric Tc prediction, new-material prediction, or Pearson superconductivity claim is exported.",
    ])
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    paths[summary.name] = str(summary)
    return paths
