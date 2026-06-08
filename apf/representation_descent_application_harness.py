"""
APF Representation Descent Application Harness.

Purpose
-------
Turn the representation descent kernel into an operational sector classifier.

Input:
    sector metadata

Output:
    * canonical APF obstruction object
    * promotion/export status
    * repair normal form
    * safe claim language
    * next action
    * no-smuggling audit fields

This harness applies the kernel to active APF sectors:
    - EW trace-to-scheme transport
    - dark-sector empirical/posterior route
    - gauge-as-fiber-automorphism program
    - horizon-area-as-fiber-cost program
    - flat substrate C* attempt
    - clean ACC base/fiber unification
    - provenance-smuggled / target-consuming claim
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Iterable, Mapping, Optional, Tuple, List

try:
    from apf.descent_obstruction_calculus import Obstruction, ObstructionObject
    from apf.obstruction_repair_normal_form import RepairClass, canonical_plan, plan_data
    from apf.globalization_promotion_gate import PromotionStatus, decide_promotion
except Exception as exc:  # pragma: no cover
    raise ImportError(f"application harness dependencies missing: {exc}") from exc


def _ok(name: str, *, status: str, summary: str, data: Optional[Mapping] = None,
        dependencies: Optional[Iterable[str]] = None) -> Dict:
    return {
        "name": name,
        "consistent": True,
        "status": status,
        "summary": summary,
        "data": dict(data or {}),
        "dependencies": list(dependencies or []),
    }


def _fail(name: str, *, status: str, summary: str, data: Optional[Mapping] = None,
          dependencies: Optional[Iterable[str]] = None) -> Dict:
    return {
        "name": name,
        "consistent": False,
        "status": status,
        "summary": summary,
        "data": dict(data or {}),
        "dependencies": list(dependencies or []),
    }


@dataclass(frozen=True)
class SectorMetadata:
    """Raw sector metadata.

    Deliberately contains no expected promotion label/status field.
    """
    name: str
    sector: str
    local_claim_available: bool
    global_claim_requested: bool
    has_ACC_base: bool
    has_local_representation: bool
    has_evaluator_map: bool
    has_codomain_transport: bool
    has_overlap_gluing_proof: bool
    has_capacity_budget_proof: bool
    capacity_overspend_detected: bool
    posterior_or_empirical_closed: bool
    target_value_consumed: bool
    needs_substrate_polarity: bool
    needs_substrate_reversal: bool
    needs_complex_action: bool
    needs_operator_norm: bool
    notes: str = ""


@dataclass(frozen=True)
class SectorClassification:
    name: str
    obstruction: ObstructionObject
    promotion_status: PromotionStatus
    repair_class: RepairClass
    export_global_P: bool
    export_local_P: bool
    safe_claim: str
    next_action: str
    repair_plan: Mapping
    metadata_notes: str


def obstruction_from_metadata(meta: SectorMetadata) -> ObstructionObject:
    channels: List[Obstruction] = []

    # Basic substrate/local data.
    if not meta.has_ACC_base:
        channels.append(Obstruction.CODOMAIN_MISMATCH)
    if not meta.has_local_representation:
        channels.append(Obstruction.EVALUATOR_MISSING)

    # Ordinary descent failures.
    if not meta.has_evaluator_map:
        channels.append(Obstruction.EVALUATOR_MISSING)
    if not meta.has_codomain_transport:
        channels.append(Obstruction.CODOMAIN_MISMATCH)
    if not meta.has_overlap_gluing_proof:
        channels.append(Obstruction.OVERLAP_INCOHERENCE)
    if not meta.has_capacity_budget_proof or meta.capacity_overspend_detected:
        channels.append(Obstruction.CAPACITY_OVERSPEND)
    if not meta.posterior_or_empirical_closed:
        # Empirical/posterior nonclosure is represented as missing evaluator/route closure
        # in the current finite obstruction calculus.
        channels.append(Obstruction.EVALUATOR_MISSING)

    # Fail-closed provenance.
    if meta.target_value_consumed:
        channels.append(Obstruction.PROVENANCE_SMUGGLE)

    # Structural substrate-global failures.
    if meta.needs_substrate_polarity:
        channels.append(Obstruction.POLARITY_MISSING)
    if meta.needs_substrate_reversal:
        channels.append(Obstruction.REVERSAL_MISSING)
    if meta.needs_complex_action:
        channels.append(Obstruction.COMPLEX_ACTION_MISSING)
    if meta.needs_operator_norm:
        channels.append(Obstruction.NORM_MISSING)

    return ObstructionObject.of(*channels)


def safe_claim_language(meta: SectorMetadata, status: PromotionStatus, repair_class: RepairClass, obs: ObstructionObject) -> Tuple[str, str]:
    if status == PromotionStatus.EXPORT_GLOBAL_P:
        return (
            "Global P: obstruction object is zero; sector claim lies in the exact descent kernel.",
            "Export as global P and cite zero-obstruction descent.",
        )

    if status == PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED:
        if meta.sector == "EW":
            return (
                "Local/trace P only: physical scheme export is held until evaluator and codomain transport close and the gate is rerun.",
                "Build/evaluate the trace-to-scheme transport map, declare codomain transport, regenerate metadata, rerun harness.",
            )
        if meta.sector == "DARK":
            return (
                "Runtime/research progress only: robust empirical P is held until posterior/empirical closure and route evaluator status close.",
                "Continue posterior/convergence/robustness work, then rerun harness from updated metadata.",
            )
        if meta.sector == "GAUGE":
            return (
                "Separate theorem program: gauge-as-fiber-automorphism is not global P until codomain/descent proof closes.",
                "Prove fiber-automorphism codomain map and overlap descent, then rerun harness.",
            )
        if meta.sector == "HORIZON":
            return (
                "Separate theorem program: horizon-area-as-fiber-cost is held until overlap/gluing descent closes.",
                "Prove horizon/interface overlap coherence and capacity-cost gluing, then rerun harness.",
            )
        return (
            "Local/repairable only: not global P until ordinary repair is executed and obstruction rechecks to zero.",
            "Execute ordinary repair plan and rerun harness.",
        )

    if status == PromotionStatus.HOLD_SUBSTRATE_REVISION_REQUIRED:
        return (
            "Not current global P: promotion would require substrate-revision routes, not current APF primitives.",
            "Open a D1/D2/D3 substrate-revision theorem program; do not export as current P.",
        )

    if status == PromotionStatus.FAIL_CLOSED_PROVENANCE:
        return (
            "Fail closed: target/provenance smuggling is present; no mathematical repair normal form is allowed.",
            "Rebuild from clean provenance and rerun harness.",
        )

    return (
        "Fail closed: unsupported obstruction state in current APF calculus.",
        "Do not export; add a theorem or metadata route before rerunning.",
    )


def classify_sector(meta: SectorMetadata) -> SectorClassification:
    obs = obstruction_from_metadata(meta)
    decision = decide_promotion(meta.name, obs)
    plan = canonical_plan(obs)
    claim, action = safe_claim_language(meta, decision.status, plan.repair_class, obs)
    return SectorClassification(
        name=meta.name,
        obstruction=obs,
        promotion_status=decision.status,
        repair_class=plan.repair_class,
        export_global_P=decision.export_global_P,
        export_local_P=decision.export_local_P and meta.local_claim_available,
        safe_claim=claim,
        next_action=action,
        repair_plan=plan_data(plan),
        metadata_notes=meta.notes,
    )


def classification_data(c: SectorClassification) -> Dict:
    return {
        "name": c.name,
        "obstruction": c.obstruction.names(),
        "promotion_status": c.promotion_status.value,
        "repair_class": c.repair_class.value,
        "export_global_P": c.export_global_P,
        "export_local_P": c.export_local_P,
        "safe_claim": c.safe_claim,
        "next_action": c.next_action,
        "repair_plan": dict(c.repair_plan),
        "metadata_notes": c.metadata_notes,
    }


def canonical_sector_metadata() -> Dict[str, SectorMetadata]:
    return {
        "ACC_base_fiber_unification": SectorMetadata(
            name="ACC_base_fiber_unification",
            sector="ACC",
            local_claim_available=True,
            global_claim_requested=True,
            has_ACC_base=True,
            has_local_representation=True,
            has_evaluator_map=True,
            has_codomain_transport=True,
            has_overlap_gluing_proof=True,
            has_capacity_budget_proof=True,
            capacity_overspend_detected=False,
            posterior_or_empirical_closed=True,
            target_value_consumed=False,
            needs_substrate_polarity=False,
            needs_substrate_reversal=False,
            needs_complex_action=False,
            needs_operator_norm=False,
            notes="Clean ACC/interface descent kernel case.",
        ),
        "EW_trace_to_scheme_transport": SectorMetadata(
            name="EW_trace_to_scheme_transport",
            sector="EW",
            local_claim_available=True,
            global_claim_requested=True,
            has_ACC_base=True,
            has_local_representation=True,
            has_evaluator_map=False,
            has_codomain_transport=False,
            has_overlap_gluing_proof=True,
            has_capacity_budget_proof=True,
            capacity_overspend_detected=False,
            posterior_or_empirical_closed=True,
            target_value_consumed=False,
            needs_substrate_polarity=False,
            needs_substrate_reversal=False,
            needs_complex_action=False,
            needs_operator_norm=False,
            notes="Trace-sector closure exists; physical scheme export awaits transport/evaluator.",
        ),
        "dark_sector_empirical_route": SectorMetadata(
            name="dark_sector_empirical_route",
            sector="DARK",
            local_claim_available=True,
            global_claim_requested=True,
            has_ACC_base=True,
            has_local_representation=True,
            has_evaluator_map=False,
            has_codomain_transport=True,
            has_overlap_gluing_proof=True,
            has_capacity_budget_proof=True,
            capacity_overspend_detected=False,
            posterior_or_empirical_closed=False,
            target_value_consumed=False,
            needs_substrate_polarity=False,
            needs_substrate_reversal=False,
            needs_complex_action=False,
            needs_operator_norm=False,
            notes="Runtime progress; posterior/robust empirical closure still open.",
        ),
        "gauge_as_fiber_automorphism": SectorMetadata(
            name="gauge_as_fiber_automorphism",
            sector="GAUGE",
            local_claim_available=True,
            global_claim_requested=True,
            has_ACC_base=True,
            has_local_representation=True,
            has_evaluator_map=True,
            has_codomain_transport=False,
            has_overlap_gluing_proof=True,
            has_capacity_budget_proof=True,
            capacity_overspend_detected=False,
            posterior_or_empirical_closed=True,
            target_value_consumed=False,
            needs_substrate_polarity=False,
            needs_substrate_reversal=False,
            needs_complex_action=False,
            needs_operator_norm=False,
            notes="Separate theorem program; codomain/descent map not yet closed.",
        ),
        "horizon_area_as_fiber_cost": SectorMetadata(
            name="horizon_area_as_fiber_cost",
            sector="HORIZON",
            local_claim_available=True,
            global_claim_requested=True,
            has_ACC_base=True,
            has_local_representation=True,
            has_evaluator_map=True,
            has_codomain_transport=True,
            has_overlap_gluing_proof=False,
            has_capacity_budget_proof=True,
            capacity_overspend_detected=False,
            posterior_or_empirical_closed=True,
            target_value_consumed=False,
            needs_substrate_polarity=False,
            needs_substrate_reversal=False,
            needs_complex_action=False,
            needs_operator_norm=False,
            notes="Separate theorem program; overlap/descent proof still open.",
        ),
        "flat_Cstar_substrate_attempt": SectorMetadata(
            name="flat_Cstar_substrate_attempt",
            sector="CSTAR",
            local_claim_available=True,
            global_claim_requested=True,
            has_ACC_base=True,
            has_local_representation=True,
            has_evaluator_map=True,
            has_codomain_transport=False,
            has_overlap_gluing_proof=True,
            has_capacity_budget_proof=True,
            capacity_overspend_detected=False,
            posterior_or_empirical_closed=True,
            target_value_consumed=False,
            needs_substrate_polarity=False,
            needs_substrate_reversal=True,
            needs_complex_action=True,
            needs_operator_norm=True,
            notes="Flat substrate-global C* attempt; blocked by structural channels.",
        ),
        "target_consuming_claim": SectorMetadata(
            name="target_consuming_claim",
            sector="PROVENANCE",
            local_claim_available=False,
            global_claim_requested=True,
            has_ACC_base=True,
            has_local_representation=True,
            has_evaluator_map=True,
            has_codomain_transport=True,
            has_overlap_gluing_proof=True,
            has_capacity_budget_proof=True,
            capacity_overspend_detected=False,
            posterior_or_empirical_closed=True,
            target_value_consumed=True,
            needs_substrate_polarity=False,
            needs_substrate_reversal=False,
            needs_complex_action=False,
            needs_operator_norm=False,
            notes="Any post-hoc/target-consuming derivation attempt.",
        ),
    }


def run_canonical_harness() -> Dict[str, SectorClassification]:
    return {name: classify_sector(meta) for name, meta in canonical_sector_metadata().items()}


def check_T_sector_metadata_schema_no_expected_labels_P() -> Dict:
    fields = set(SectorMetadata.__dataclass_fields__.keys())
    forbidden = {"expected_status", "expected_label", "expected_repair_class", "label", "status"}
    tests = {
        "no_expected_label_fields": fields.isdisjoint(forbidden),
        "has_required_raw_fields": {
            "has_evaluator_map",
            "has_codomain_transport",
            "posterior_or_empirical_closed",
            "target_value_consumed",
            "needs_substrate_reversal",
            "needs_complex_action",
            "needs_operator_norm",
        }.issubset(fields),
    }
    if all(tests.values()):
        return _ok(
            "check_T_sector_metadata_schema_no_expected_labels_P",
            status="P_harness",
            summary="Sector metadata schema contains raw inputs only and no expected-label leakage.",
            data={"fields": sorted(fields), "tests": tests},
        )
    return _fail("check_T_sector_metadata_schema_no_expected_labels_P", status="FAIL", summary="Sector metadata schema failed no-label audit", data={"fields": sorted(fields), "tests": tests})


def check_T_obstruction_derivation_from_metadata_P() -> Dict:
    classifications = run_canonical_harness()
    data = {name: classification_data(c) for name, c in classifications.items()}
    tests = {
        "ACC_zero": data["ACC_base_fiber_unification"]["obstruction"] == tuple(),
        "EW_has_evaluator_codomain": set(data["EW_trace_to_scheme_transport"]["obstruction"]) == {"EVALUATOR_MISSING", "CODOMAIN_MISMATCH"},
        "dark_has_evaluator": set(data["dark_sector_empirical_route"]["obstruction"]) == {"EVALUATOR_MISSING"},
        "gauge_has_codomain": set(data["gauge_as_fiber_automorphism"]["obstruction"]) == {"CODOMAIN_MISMATCH"},
        "horizon_has_overlap": set(data["horizon_area_as_fiber_cost"]["obstruction"]) == {"OVERLAP_INCOHERENCE"},
        "Cstar_has_structural": {"REVERSAL_MISSING", "COMPLEX_ACTION_MISSING", "NORM_MISSING", "CODOMAIN_MISMATCH"}.issubset(set(data["flat_Cstar_substrate_attempt"]["obstruction"])),
        "target_has_provenance": "PROVENANCE_SMUGGLE" in set(data["target_consuming_claim"]["obstruction"]),
    }
    if all(tests.values()):
        return _ok(
            "check_T_obstruction_derivation_from_metadata_P",
            status="P_harness",
            summary="Canonical sector obstructions are derived from raw metadata.",
            data={"classifications": data, "tests": tests},
            dependencies=["check_T_sector_metadata_schema_no_expected_labels_P"],
        )
    return _fail("check_T_obstruction_derivation_from_metadata_P", status="FAIL", summary="Metadata obstruction derivation failed", data={"classifications": data, "tests": tests})


def check_T_promotion_status_outputs_P() -> Dict:
    classifications = run_canonical_harness()
    status = {name: c.promotion_status.value for name, c in classifications.items()}
    tests = {
        "ACC_exports": status["ACC_base_fiber_unification"] == "EXPORT_GLOBAL_P",
        "EW_holds_ordinary": status["EW_trace_to_scheme_transport"] == "HOLD_ORDINARY_REPAIR_REQUIRED",
        "dark_holds_ordinary": status["dark_sector_empirical_route"] == "HOLD_ORDINARY_REPAIR_REQUIRED",
        "gauge_holds_ordinary": status["gauge_as_fiber_automorphism"] == "HOLD_ORDINARY_REPAIR_REQUIRED",
        "horizon_holds_ordinary": status["horizon_area_as_fiber_cost"] == "HOLD_ORDINARY_REPAIR_REQUIRED",
        "Cstar_holds_substrate_revision": status["flat_Cstar_substrate_attempt"] == "HOLD_SUBSTRATE_REVISION_REQUIRED",
        "target_fails_closed": status["target_consuming_claim"] == "FAIL_CLOSED_PROVENANCE",
    }
    if all(tests.values()):
        return _ok(
            "check_T_promotion_status_outputs_P",
            status="P_harness",
            summary="Harness emits correct promotion statuses from derived obstructions.",
            data={"statuses": status, "tests": tests},
            dependencies=["check_T_obstruction_derivation_from_metadata_P"],
        )
    return _fail("check_T_promotion_status_outputs_P", status="FAIL", summary="Promotion status outputs failed", data={"statuses": status, "tests": tests})


def check_T_repair_normal_form_outputs_P() -> Dict:
    classifications = run_canonical_harness()
    repairs = {name: c.repair_class.value for name, c in classifications.items()}
    tests = {
        "ACC_exact": repairs["ACC_base_fiber_unification"] == "EXACT",
        "EW_ordinary": repairs["EW_trace_to_scheme_transport"] == "ORDINARY_REPAIRABLE",
        "dark_ordinary": repairs["dark_sector_empirical_route"] == "ORDINARY_REPAIRABLE",
        "gauge_ordinary": repairs["gauge_as_fiber_automorphism"] == "ORDINARY_REPAIRABLE",
        "horizon_ordinary": repairs["horizon_area_as_fiber_cost"] == "ORDINARY_REPAIRABLE",
        "Cstar_substrate_revision": repairs["flat_Cstar_substrate_attempt"] == "SUBSTRATE_REVISION_REPAIRABLE",
        "target_nonrepairable": repairs["target_consuming_claim"] == "NONREPAIRABLE_PROVENANCE",
    }
    if all(tests.values()):
        return _ok(
            "check_T_repair_normal_form_outputs_P",
            status="P_harness",
            summary="Harness emits canonical repair normal forms for sector obstructions.",
            data={"repair_classes": repairs, "tests": tests},
            dependencies=["check_T_promotion_status_outputs_P"],
        )
    return _fail("check_T_repair_normal_form_outputs_P", status="FAIL", summary="Repair normal form outputs failed", data={"repair_classes": repairs, "tests": tests})


def check_T_safe_claim_language_outputs_P() -> Dict:
    classifications = run_canonical_harness()
    claims = {name: c.safe_claim for name, c in classifications.items()}
    tests = {
        "ACC_global_language": "Global P" in claims["ACC_base_fiber_unification"],
        "EW_local_trace_language": "Local/trace P only" in claims["EW_trace_to_scheme_transport"],
        "dark_runtime_language": "Runtime/research progress only" in claims["dark_sector_empirical_route"],
        "gauge_program_language": "Separate theorem program" in claims["gauge_as_fiber_automorphism"],
        "horizon_program_language": "Separate theorem program" in claims["horizon_area_as_fiber_cost"],
        "Cstar_not_current_language": "Not current global P" in claims["flat_Cstar_substrate_attempt"],
        "target_fail_closed_language": "Fail closed" in claims["target_consuming_claim"],
    }
    if all(tests.values()):
        return _ok(
            "check_T_safe_claim_language_outputs_P",
            status="P_harness",
            summary="Harness emits safe reviewer-facing claim language for each sector.",
            data={"claims": claims, "tests": tests},
            dependencies=["check_T_repair_normal_form_outputs_P"],
        )
    return _fail("check_T_safe_claim_language_outputs_P", status="FAIL", summary="Safe claim language failed", data={"claims": claims, "tests": tests})


def check_T_harness_no_overpromotion_P() -> Dict:
    classifications = run_canonical_harness()
    tests = {
        "global_export_only_zero": all(c.export_global_P == c.obstruction.is_zero for c in classifications.values()),
        "nonzero_not_exported": all((not c.export_global_P) for c in classifications.values() if not c.obstruction.is_zero),
        "provenance_not_local_or_global": (not classifications["target_consuming_claim"].export_global_P) and (not classifications["target_consuming_claim"].export_local_P),
        "Cstar_not_exported": not classifications["flat_Cstar_substrate_attempt"].export_global_P,
    }
    if all(tests.values()):
        return _ok(
            "check_T_harness_no_overpromotion_P",
            status="P_audit",
            summary="Harness does not overpromote: only zero-obstruction claims export global P; provenance fails closed.",
            data={"tests": tests},
            dependencies=["check_T_safe_claim_language_outputs_P"],
        )
    return _fail("check_T_harness_no_overpromotion_P", status="FAIL", summary="Harness overpromotion audit failed", data=tests)


def check_T_application_harness_export_table_P() -> Dict:
    classifications = run_canonical_harness()
    rows = [classification_data(c) for c in classifications.values()]
    tests = {
        "row_count": len(rows) == 7,
        "all_rows_have_status": all(row["promotion_status"] for row in rows),
        "all_rows_have_next_action": all(row["next_action"] for row in rows),
        "all_rows_have_obstruction": all("obstruction" in row for row in rows),
    }
    if all(tests.values()):
        return _ok(
            "check_T_application_harness_export_table_P",
            status="P_harness",
            summary="Harness export table is complete for canonical active sectors.",
            data={"rows": rows, "tests": tests},
            dependencies=["check_T_harness_no_overpromotion_P"],
        )
    return _fail("check_T_application_harness_export_table_P", status="FAIL", summary="Harness export table failed", data={"rows": rows, "tests": tests})


def check_T_representation_descent_application_harness_P() -> Dict:
    subchecks = [
        check_T_sector_metadata_schema_no_expected_labels_P(),
        check_T_obstruction_derivation_from_metadata_P(),
        check_T_promotion_status_outputs_P(),
        check_T_repair_normal_form_outputs_P(),
        check_T_safe_claim_language_outputs_P(),
        check_T_harness_no_overpromotion_P(),
        check_T_application_harness_export_table_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_representation_descent_application_harness_P",
            status="P_application",
            summary="Representation Descent Application Harness is P: it derives obstruction, status, repair, and safe claim language from sector metadata.",
            data={
                "canonical_sector_count": len(canonical_sector_metadata()),
                "exports_global_P": [name for name, c in run_canonical_harness().items() if c.export_global_P],
                "held_or_failed": [name for name, c in run_canonical_harness().items() if not c.export_global_P],
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_representation_descent_application_harness_P",
        status="FAIL",
        summary="Representation Descent Application Harness failed.",
        data={"subchecks": subchecks},
    )


CHECKS = {
    "check_T_sector_metadata_schema_no_expected_labels_P": check_T_sector_metadata_schema_no_expected_labels_P,
    "check_T_obstruction_derivation_from_metadata_P": check_T_obstruction_derivation_from_metadata_P,
    "check_T_promotion_status_outputs_P": check_T_promotion_status_outputs_P,
    "check_T_repair_normal_form_outputs_P": check_T_repair_normal_form_outputs_P,
    "check_T_safe_claim_language_outputs_P": check_T_safe_claim_language_outputs_P,
    "check_T_harness_no_overpromotion_P": check_T_harness_no_overpromotion_P,
    "check_T_application_harness_export_table_P": check_T_application_harness_export_table_P,
    "check_T_representation_descent_application_harness_P": check_T_representation_descent_application_harness_P,
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
            raise TypeError("Unsupported registry type for representation_descent_application_harness.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
