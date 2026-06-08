"""APF Coherent Materials — Red team (merged adversarial stress suite + claim-fence certifier + provenance conflict auditor).

CMAL module-collapse (v24.3.66, Integrator Response v1.1 Q7). Architecture-only:
no register(), no check_*, no BANK_REGISTRY entry, no EXPECTED delta. Merged
verbatim from: coherent_materials_adversarial_receipt_stress_suite, coherent_materials_claim_fence_certifier, coherent_materials_provenance_conflict_auditor. Two colliding
constants were source-prefixed to preserve both consumers' values.
"""
from __future__ import annotations
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence
import csv
import json
from apf.coherent_materials_batch_triage_runner import run_case
from apf.coherent_materials_golden_receipt_benchmark import get_case
from apf.coherent_materials_receipt_contract_validator import DEMO_RECEIPTS, validate_receipt
from collections import defaultdict


# === merged from coherent_materials_adversarial_receipt_stress_suite ===
ADVERSARIAL_NONCLAIM_EXPORTS: dict[str, int] = {
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
    "ambient_superconductivity_from_pressure_only": 0,
}


def _ledger(case_id: str, target_codomain: str = "SC_MATERIAL_ADMISSIBILITY", classification: str = "MATERIAL_LEDGER_INSUFFICIENT") -> dict[str, Any]:
    return {
        "ledger_id": "ledger_" + case_id,
        "classification": classification,
        "material": {"composition": case_id, "structure_known": False},
        "material_family": "adversarial_fixture",
        "target_codomain": target_codomain,
        "coherence_type": target_codomain,
        "controls": {},
        "evidence": {},
        "burdens": {"provenance": 0.8},
        "scores": {"fragmented_or_normal_cost": 3.0, "coherent_cost": 4.5},
        "provenance": {"declared": False, "source": "CMAL adversarial fixture"},
    }


def _case_from_receipt(case_id: str, receipt: Mapping[str, Any], *, classification: str = "MATERIAL_LEDGER_INSUFFICIENT", attack_class: str = "front_gate") -> dict[str, Any]:
    target = str(receipt.get("target_codomain", "SC_MATERIAL_ADMISSIBILITY"))
    return {
        "attack_class": attack_class,
        "description": "CMAL adversarial receipt fixture: " + case_id,
        "ledger": _ledger(case_id, target, classification),
        "receipts": [deepcopy(dict(receipt))],
    }


def _copy_demo(name: str) -> dict[str, Any]:
    return deepcopy(dict(DEMO_RECEIPTS[name]))


def _target_value_smuggling_receipt() -> dict[str, Any]:
    r = _copy_demo("resistive_only")
    r.update({
        "receipt_id": "R-ADVERSARIAL-TARGET-VALUE-SMUGGLE",
        "material_id": "target_value_smuggling_fixture",
        "sample_id": "smuggle_sample_1",
        "receipt_kind": "target_value_smuggling",
        "target_value_smuggling": True,
        "measured_value": {"zero_resistance": True, "claimed_Tc_K": 300, "target_value_used": True},
        "nonclaim_guard": [],
    })
    return r


def _missing_uncertainty_receipt() -> dict[str, Any]:
    r = _copy_demo("resistive_only")
    r["receipt_id"] = "R-ADVERSARIAL-MISSING-UNCERTAINTY"
    r["material_id"] = "missing_uncertainty_fixture"
    r.pop("uncertainty", None)
    return r


def _missing_sample_id_receipt() -> dict[str, Any]:
    r = _copy_demo("bulk_sc_full")
    r["receipt_id"] = "R-ADVERSARIAL-MISSING-SAMPLE-ID"
    r["material_id"] = "missing_sample_id_fixture"
    r.pop("sample_id", None)
    return r


def _unknown_codomain_receipt() -> dict[str, Any]:
    r = _copy_demo("bulk_sc_full")
    r.update({
        "receipt_id": "R-ADVERSARIAL-UNKNOWN-CODOMAIN",
        "material_id": "unknown_codomain_fixture",
        "sample_id": "unknown_codomain_sample",
        "target_codomain": "MAGICAL_MATERIAL_CODOMAIN",
        "nonclaim_guard": [],
    })
    return r


def _negative_meissner_receipts() -> list[dict[str, Any]]:
    r1 = _copy_demo("resistive_only")
    r1.update({
        "receipt_id": "R-ADVERSARIAL-RESISTIVE-TRACE",
        "material_id": "negative_meissner_fixture",
        "sample_id": "neg_meissner_sample",
        "receipt_kind": "R_SC_RESISTIVITY_ZERO_OR_DROP",
        "updates_required_slots": ["R_SC_RESISTIVITY_ZERO_OR_DROP"],
    })
    r2 = _copy_demo("bulk_sc_full")
    r2.update({
        "receipt_id": "R-ADVERSARIAL-MEISSNER-NEGATIVE",
        "material_id": "negative_meissner_fixture",
        "sample_id": "neg_meissner_sample",
        "receipt_kind": "R_SC_MEISSNER_DIAMAGNETIC_RESPONSE",
        "measured_value": {"meissner_or_diamagnetic_response": False},
        "updates_required_slots": ["R_SC_MEISSNER_DIAMAGNETIC_RESPONSE"],
        "pass_fail": "fail",
        "contradicts_prior": True,
        "nonclaim_guard": ["negative_meissner_blocks_SC"],
    })
    return [r1, r2]


def _duplicate_receipt_id_bundle() -> list[dict[str, Any]]:
    r1 = _copy_demo("bulk_sc_full")
    r1.update({
        "receipt_id": "R-DUPLICATE-ID",
        "material_id": "duplicate_id_fixture",
        "sample_id": "dup_sample",
    })
    r2 = _copy_demo("hydride_ambient_smuggle")
    r2.update({
        "receipt_id": "R-DUPLICATE-ID",
        "material_id": "duplicate_id_fixture",
        "sample_id": "dup_sample",
    })
    return [r1, r2]


def _mixed_sc_qm_bundle() -> list[dict[str, Any]]:
    r1 = _copy_demo("bulk_sc_full")
    r1.update({"receipt_id": "R-MIXED-BULK-SC", "material_id": "mixed_bundle_fixture", "sample_id": "mixed_sample"})
    r2 = _copy_demo("pearson_misrouted_sc")
    r2.update({"receipt_id": "R-MIXED-PEARSON-AS-SC"})
    return [r1, r2]


ADVERSARIAL_CASES: dict[str, dict[str, Any]] = {
    "positive_control_full_sc_promotes": {
        "attack_class": "positive_control",
        "description": "Known-good bulk SC receipt bundle should still promote; verifies that red-team hardening does not close valid paths.",
        "ledger": get_case("full_bulk_sc_receipts_promote")["ledger"],
        "receipts": get_case("full_bulk_sc_receipts_promote")["receipts"],
        "expected": {"batch_route": "LEDGER_UPDATED", "update_status": "PROMOTE_CODOMAIN", "updated_classification": "SC_MATERIAL_ADMISSIBLE"},
    },
    "formula_only_room_temperature_sc_claim": {
        **_case_from_receipt("formula_only_room_temperature_sc_claim", _copy_demo("formula_only_rtsc"), attack_class="formula_only_overclaim"),
        "expected": {"validation_status": "QUARANTINED", "batch_route": "QUARANTINED_BY_VALIDATOR", "update_status": "QUARANTINE_CLAIM"},
    },
    "target_value_smuggling_sc_claim": {
        **_case_from_receipt("target_value_smuggling_sc_claim", _target_value_smuggling_receipt(), attack_class="target_value_smuggling"),
        "expected": {"validation_status": "QUARANTINED", "validation_route": "TARGET_VALUE_SMUGGLING", "update_status": "QUARANTINE_CLAIM"},
    },
    "resistive_only_overclaimed_as_bulk_sc": {
        **_case_from_receipt("resistive_only_overclaimed_as_bulk_sc", _copy_demo("resistive_only"), classification="RESISTIVE_ONLY_NO_MEISSNER", attack_class="evidence_overclaim"),
        "expected": {"validation_route": "RESISTIVE_ONLY_NO_MEISSNER", "update_status": "REQUEST_NEXT_RECEIPT"},
    },
    "pearson_naeuiO3_4_misrouted_as_sc": {
        **_case_from_receipt("pearson_naeuiO3_4_misrouted_as_sc", _copy_demo("pearson_misrouted_sc"), attack_class="codomain_misroute"),
        "expected": {"validation_status": "REJECTED", "batch_route": "REJECTED_BY_VALIDATOR", "update_status": "ROUTE_TO_DIFFERENT_CODOMAIN"},
    },
    "ambient_claim_from_pressure_conditioned_hydride": {
        **_case_from_receipt("ambient_claim_from_pressure_conditioned_hydride", _copy_demo("hydride_ambient_smuggle"), attack_class="condition_smuggling"),
        "expected": {"validation_status": "QUARANTINED", "batch_route": "QUARANTINED_BY_VALIDATOR", "update_status": "QUARANTINE_CLAIM"},
    },
    "missing_uncertainty_repairable_receipt": {
        **_case_from_receipt("missing_uncertainty_repairable_receipt", _missing_uncertainty_receipt(), attack_class="contract_repair"),
        "expected": {"validation_status": "REPAIRABLE", "batch_route": "REPAIR_REQUIRED_BY_VALIDATOR"},
    },
    "missing_sample_id_rejected_receipt": {
        **_case_from_receipt("missing_sample_id_rejected_receipt", _missing_sample_id_receipt(), attack_class="critical_contract_missing"),
        "expected": {"validation_status": "REJECTED", "batch_route": "REJECTED_BY_VALIDATOR"},
    },
    "unknown_codomain_rejected_receipt": {
        **_case_from_receipt("unknown_codomain_rejected_receipt", _unknown_codomain_receipt(), attack_class="unknown_codomain"),
        "expected": {"validation_status": "REJECTED", "validation_route": "UNKNOWN_OR_UNEXPORTED_CODOMAIN"},
    },
    "topological_stub_overexport_attempt": {
        **_case_from_receipt("topological_stub_overexport_attempt", _copy_demo("topological_stub"), attack_class="stub_overexport"),
        "expected": {"validation_route": "STUB_RECOGNIZED_NOT_EXPORTED"},
    },
    "negative_meissner_contradiction": {
        "attack_class": "contradictory_receipts",
        "description": "A zero-resistance receipt paired with a negative/contradictory Meissner receipt must not promote bulk SC.",
        "ledger": _ledger("negative_meissner_contradiction", "SC_MATERIAL_ADMISSIBILITY", "RESISTIVE_ONLY_NO_MEISSNER"),
        "receipts": _negative_meissner_receipts(),
        "expected": {"update_status": "QUARANTINE_CLAIM"},
    },
    "duplicate_receipt_id_conflict": {
        "attack_class": "provenance_conflict",
        "description": "Duplicate receipt IDs in a mixed bundle should be caught by the claim-fence certifier even when local validators inspect receipts one-by-one.",
        "ledger": _ledger("duplicate_receipt_id_conflict", "SC_MATERIAL_ADMISSIBILITY", "MATERIAL_LEDGER_INSUFFICIENT"),
        "receipts": _duplicate_receipt_id_bundle(),
        "expected": {"claim_fence_flag": "DUPLICATE_RECEIPT_IDS"},
    },
    "mixed_sc_and_pearson_misroute_bundle": {
        "attack_class": "mixed_codomain_bundle",
        "description": "A mixed SC + Pearson-as-SC bundle should not allow the valid SC receipt to hide a rejected codomain-misrouted receipt.",
        "ledger": _ledger("mixed_sc_and_pearson_misroute_bundle", "SC_MATERIAL_ADMISSIBILITY", "MATERIAL_LEDGER_INSUFFICIENT"),
        "receipts": _mixed_sc_qm_bundle(),
        "expected": {"batch_route": "REJECTED_BY_VALIDATOR", "update_status": "ROUTE_TO_DIFFERENT_CODOMAIN"},
    },
}


@dataclass(frozen=True)
class AdversarialCaseResult:
    case_id: str
    attack_class: str
    validation_statuses: tuple[str, ...]
    validation_routes: tuple[str, ...]
    batch_route: str
    update_status: str
    updated_classification: str
    triage_bucket: str
    next_action: str
    expected: Mapping[str, Any]
    local_expectation_passed: bool
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "attack_class": self.attack_class,
            "validation_statuses": list(self.validation_statuses),
            "validation_routes": list(self.validation_routes),
            "batch_route": self.batch_route,
            "update_status": self.update_status,
            "updated_classification": self.updated_classification,
            "triage_bucket": self.triage_bucket,
            "next_action": self.next_action,
            "expected": dict(self.expected),
            "local_expectation_passed": self.local_expectation_passed,
            "reasons": list(self.reasons),
        }


def _matches_expectation(result_dict: Mapping[str, Any], validation_statuses: Sequence[str], validation_routes: Sequence[str], expected: Mapping[str, Any]) -> bool:
    for key, value in expected.items():
        if key == "validation_status" and value not in validation_statuses:
            return False
        if key == "validation_route" and value not in validation_routes:
            return False
        if key in result_dict and result_dict[key] != value:
            return False
        # claim_fence_flag is evaluated by the separate claim-fence certifier.
    return True


def run_adversarial_case(case_id: str, case: Mapping[str, Any] | None = None) -> AdversarialCaseResult:
    c = dict(case or ADVERSARIAL_CASES[case_id])
    receipts = list(c.get("receipts", ()))
    validations = [validate_receipt(r) for r in receipts]
    result = run_case(case_id, c)
    rd = result.to_dict()
    validation_statuses = tuple(v.status for v in validations)
    validation_routes = tuple(v.route for v in validations)
    expected = dict(c.get("expected", {}))
    passed = _matches_expectation(rd, validation_statuses, validation_routes, expected)
    reasons = tuple(dict.fromkeys([reason for v in validations for reason in v.reasons] + list(rd.get("reasons", ()))))
    return AdversarialCaseResult(
        case_id=case_id,
        attack_class=str(c.get("attack_class", "unknown")),
        validation_statuses=validation_statuses,
        validation_routes=validation_routes,
        batch_route=str(rd["batch_route"]),
        update_status=str(rd["update_status"]),
        updated_classification=str(rd["updated_classification"]),
        triage_bucket=str(rd["triage_bucket"]),
        next_action=str(rd["next_action"]),
        expected=expected,
        local_expectation_passed=passed,
        reasons=reasons,
    )


def run_adversarial_stress_suite() -> list[AdversarialCaseResult]:
    return [run_adversarial_case(case_id, case) for case_id, case in ADVERSARIAL_CASES.items()]


def make_validation_report(results: Sequence[AdversarialCaseResult]) -> dict[str, Any]:
    return {
        "schema": "CMAL_ADVERSARIAL_RECEIPT_STRESS_VALIDATION_REPORT_v1",
        "case_count": len(results),
        "cases": [r.to_dict() for r in results],
        "status_counts": {s: sum(s in r.validation_statuses for r in results) for s in sorted({s for r in results for s in r.validation_statuses})},
        "update_counts": {s: sum(r.update_status == s for r in results) for s in sorted({r.update_status for r in results})},
        "local_expectations_passed": all(r.local_expectation_passed for r in results),
        "preserved_nonclaims": dict(ADVERSARIAL_NONCLAIM_EXPORTS),
    }


def write_adversarial_stress_outputs(output_dir: str | Path, results: Sequence[AdversarialCaseResult] | None = None) -> dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    results = list(results or run_adversarial_stress_suite())
    paths: dict[str, str] = {}
    report = make_validation_report(results)
    p = out / "ADVERSARIAL_VALIDATION_REPORT.json"
    p.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    paths[p.name] = str(p)
    matrix = out / "FAILURE_MODE_MATRIX.csv"
    with matrix.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["case_id", "attack_class", "validation_statuses", "validation_routes", "batch_route", "update_status", "updated_classification", "expectation_passed"])
        w.writeheader()
        for r in results:
            w.writerow({
                "case_id": r.case_id,
                "attack_class": r.attack_class,
                "validation_statuses": "+".join(r.validation_statuses),
                "validation_routes": "+".join(r.validation_routes),
                "batch_route": r.batch_route,
                "update_status": r.update_status,
                "updated_classification": r.updated_classification,
                "expectation_passed": r.local_expectation_passed,
            })
    paths[matrix.name] = str(matrix)
    summary = out / "CMAL_ADVERSARIAL_STRESS_SUMMARY.md"
    lines = [
        "# CMAL Adversarial Receipt Stress Summary",
        "",
        "This stress suite attacks the CMAL receipt front gate with formula-only, target-smuggled, pressure/ambient-smuggled, codomain-misrouted, missing-contract, unknown-codomain, stub-overexport, contradictory, duplicate-ID, and mixed-codomain receipts.",
        "",
        f"Case count: {len(results)}",
        f"Local expectations passed: {all(r.local_expectation_passed for r in results)}",
        "",
        "| Case | Attack class | Validation | Batch route | Update | Classification |",
        "|---|---|---|---|---|---|",
    ]
    for r in results:
        lines.append(f"| {r.case_id} | {r.attack_class} | {'+'.join(r.validation_statuses)} / {'+'.join(r.validation_routes)} | {r.batch_route} | {r.update_status} | {r.updated_classification} |")
    lines += [
        "",
        "## Non-claim fence",
        "",
        "No adversarial case is allowed to promote numeric Tc, new-material prediction, room-temperature superconductivity, Pearson-as-superconductivity, autonomous-lab execution, live ingestion, Materials Discovery OS architecture, or APF-Mat sixth-engine status.",
    ]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    paths[summary.name] = str(summary)
    return paths

# === merged from coherent_materials_claim_fence_certifier ===
FORBIDDEN_PROMOTION_STATUSES = {"PROMOTE_CODOMAIN", "PROMOTE_PRESSURE_CONDITIONED_SC"}
ALLOWED_PROMOTION_CASES = {"positive_control_full_sc_promotes"}

@dataclass(frozen=True)
class ClaimFenceFinding:
    case_id: str
    finding: str
    severity: str
    passed: bool
    details: str
    def to_dict(self) -> dict[str, Any]:
        return {"case_id": self.case_id, "finding": self.finding, "severity": self.severity, "passed": self.passed, "details": self.details}


def _receipt_ids(case: Mapping[str, Any]) -> list[str]:
    return [str(r.get("receipt_id", "UNKNOWN_RECEIPT")) for r in case.get("receipts", ())]


def _has_duplicate_receipt_ids(case: Mapping[str, Any]) -> bool:
    ids = _receipt_ids(case)
    return len(ids) != len(set(ids))


def _contains_pearson_as_sc(case: Mapping[str, Any]) -> bool:
    for r in case.get("receipts", ()):
        text = " ".join(str(r.get(k, "")).lower() for k in ("receipt_id", "material_id", "sample_id", "instrument_or_protocol"))
        if "pearson" in text and str(r.get("target_codomain")) == "SC_MATERIAL_ADMISSIBILITY":
            return True
    return False


def _contains_pressure_ambient_smuggle(case: Mapping[str, Any]) -> bool:
    for r in case.get("receipts", ()):
        cv = r.get("control_vector", {}) if isinstance(r.get("control_vector"), Mapping) else {}
        mv = r.get("measured_value", {}) if isinstance(r.get("measured_value"), Mapping) else {}
        try:
            pressure = float(cv.get("pressure_GPa", 0) or 0)
        except Exception:
            pressure = 0.0
        if pressure > 1.0 and mv.get("ambient_usability_claimed") is True:
            return True
    return False


def _contains_target_smuggle(case: Mapping[str, Any]) -> bool:
    for r in case.get("receipts", ()):
        if r.get("target_value_smuggling") or r.get("receipt_kind") == "target_value_smuggling":
            return True
        mv = r.get("measured_value", {}) if isinstance(r.get("measured_value"), Mapping) else {}
        if mv.get("target_value_used") is True:
            return True
    return False


def _contains_stub(case: Mapping[str, Any]) -> bool:
    return any(str(r.get("target_codomain", "")).endswith("_STUB") for r in case.get("receipts", ()))


def certify_claim_fence(results: Sequence[Any] | None = None, cases: Mapping[str, Mapping[str, Any]] | None = None) -> dict[str, Any]:
    results = list(results or run_adversarial_stress_suite())
    cases = dict(cases or ADVERSARIAL_CASES)
    findings: list[ClaimFenceFinding] = []
    for r in results:
        case = cases[r.case_id]
        adversarial = r.case_id not in ALLOWED_PROMOTION_CASES
        if adversarial and r.update_status in FORBIDDEN_PROMOTION_STATUSES:
            findings.append(ClaimFenceFinding(r.case_id, "FORBIDDEN_ADVERSARIAL_PROMOTION", "critical", False, f"adversarial case promoted via {r.update_status}"))
        else:
            findings.append(ClaimFenceFinding(r.case_id, "NO_FORBIDDEN_ADVERSARIAL_PROMOTION", "info", True, r.update_status))
        if _has_duplicate_receipt_ids(case):
            findings.append(ClaimFenceFinding(r.case_id, "DUPLICATE_RECEIPT_IDS", "warning", True, "duplicate receipt IDs detected and fenced for review"))
        if _contains_pearson_as_sc(case):
            passed = r.batch_route == "REJECTED_BY_VALIDATOR" or r.update_status == "ROUTE_TO_DIFFERENT_CODOMAIN"
            findings.append(ClaimFenceFinding(r.case_id, "PEARSON_AS_SC_BLOCKED", "critical", passed, f"batch_route={r.batch_route}; update={r.update_status}"))
        if _contains_pressure_ambient_smuggle(case):
            passed = r.update_status == "QUARANTINE_CLAIM" or r.batch_route == "QUARANTINED_BY_VALIDATOR"
            findings.append(ClaimFenceFinding(r.case_id, "AMBIENT_FROM_PRESSURE_ONLY_BLOCKED", "critical", passed, f"batch_route={r.batch_route}; update={r.update_status}"))
        if _contains_target_smuggle(case):
            passed = r.update_status == "QUARANTINE_CLAIM" or "TARGET_VALUE_SMUGGLING" in r.validation_routes
            findings.append(ClaimFenceFinding(r.case_id, "TARGET_VALUE_SMUGGLING_BLOCKED", "critical", passed, f"validation_routes={r.validation_routes}"))
        if _contains_stub(case):
            passed = r.update_status not in FORBIDDEN_PROMOTION_STATUSES
            findings.append(ClaimFenceFinding(r.case_id, "STUB_OVEREXPORT_BLOCKED", "critical", passed, r.update_status))
    nonclaims_ok = all(value == 0 for value in ADVERSARIAL_NONCLAIM_EXPORTS.values())
    fence_pass = nonclaims_ok and all(f.passed for f in findings if f.severity == "critical")
    return {
        "schema": "CMAL_CLAIM_FENCE_CERTIFIER_REPORT_v1",
        "case_count": len(results),
        "finding_count": len(findings),
        "fence_pass": fence_pass,
        "critical_failures": [f.to_dict() for f in findings if f.severity == "critical" and not f.passed],
        "caught_failure_modes": [f.to_dict() for f in findings if f.finding in {"DUPLICATE_RECEIPT_IDS", "PEARSON_AS_SC_BLOCKED", "AMBIENT_FROM_PRESSURE_ONLY_BLOCKED", "TARGET_VALUE_SMUGGLING_BLOCKED", "STUB_OVEREXPORT_BLOCKED"}],
        "findings": [f.to_dict() for f in findings],
        "preserved_nonclaims": dict(ADVERSARIAL_NONCLAIM_EXPORTS),
    }


def write_claim_fence_report(output_dir: str | Path, results: Sequence[Any] | None = None) -> dict[str, str]:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    report = certify_claim_fence(results)
    p = out / "RED_TEAM_CLAIM_FENCE_REPORT.json"
    p.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    summary = out / "CMAL_CLAIM_FENCE_SUMMARY.md"
    lines = [
        "# CMAL Claim-Fence Summary",
        "",
        f"Fence pass: {report['fence_pass']}",
        f"Critical failures: {len(report['critical_failures'])}",
        "",
        "Caught failure modes include Pearson-as-SC misrouting, ambient-from-pressure-only smuggling, target-value smuggling, stub over-export attempts, and duplicate receipt IDs.",
        "",
        "The fence certifies non-promotion of APF-Mat sixth-engine status, Materials Discovery OS status, live ingestion, autonomous lab execution, numeric Tc prediction, new-material prediction, Pearson superconductivity, and room-temperature superconductivity.",
    ]
    summary.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {p.name: str(p), summary.name: str(summary)}

# === merged from coherent_materials_provenance_conflict_auditor ===
NONCLAIM_EXPORTS = {
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
}

CONFLICT_PRECEDENCE = {
    "EXTRAORDINARY_UNVERIFIED": 0,
    "CONDITION_CONFLATION": 1,
    "CODOMAIN_MISROUTE": 2,
    "REPLICATION_CONFLICT": 3,
    "MEASUREMENT_CONFLICT": 4,
    "PROVENANCE_INCOMPLETE": 5,
    "SAMPLE_ID_MISSING": 6,
}

REQUIRED_RECEIPT_FIELDS = (
    "schema_version", "receipt_id", "material_id", "sample_id", "target_codomain",
    "receipt_kind", "measurement_method", "control_vector", "measured_value",
    "uncertainty", "instrument_or_protocol", "provenance", "replication_status",
    "updates_required_slots", "nonclaim_guard",
)

SC_TARGETS = {"SC", "SC_MATERIAL_ADMISSIBILITY", "SUPERCONDUCTIVITY"}
QM_TARGETS = {"RARE_EARTH_QUANTUM_MEMORY", "QUANTUM_MEMORY", "COHERENT_MATERIAL_QM"}


def _text(value: Any) -> str:
    return str(value or "").strip().lower()


def _target(receipt: Mapping[str, Any]) -> str:
    return str(receipt.get("target_codomain", ""))


def _material(receipt: Mapping[str, Any]) -> str:
    return str(receipt.get("material_id") or receipt.get("composition") or "")


def _truthy_measurement(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return True
    if isinstance(value, Mapping):
        if "present" in value:
            return bool(value["present"])
        if "zero_resistance" in value:
            return bool(value["zero_resistance"])
        if "claimed_room_temperature_SC" in value:
            return bool(value["claimed_room_temperature_SC"])
    return bool(value)


def _control(receipt: Mapping[str, Any]) -> Mapping[str, Any]:
    c = receipt.get("control_vector")
    return c if isinstance(c, Mapping) else {}


def _pressure_gpa(receipt: Mapping[str, Any]) -> float | None:
    c = _control(receipt)
    for key in ("pressure_GPa", "pressure_gpa", "p_GPa"):
        if key in c:
            try:
                return float(c[key])
            except Exception:
                return None
    return None


def _declares_ambient_claim(receipt: Mapping[str, Any]) -> bool:
    claim = receipt.get("claim", {})
    extra = receipt.get("extra", {})
    c = _control(receipt)
    return bool(
        (isinstance(claim, Mapping) and claim.get("ambient_usability"))
        or (isinstance(extra, Mapping) and extra.get("ambient_claim"))
        or c.get("ambient_claim")
    )


def _is_pearson_material(receipt: Mapping[str, Any]) -> bool:
    material = _material(receipt).lower()
    source = _text(receipt.get("source_key") or receipt.get("source"))
    return "pearson" in source or "naeu" in material or "io3" in material


def _field_missing(receipt: Mapping[str, Any], field: str) -> bool:
    if field not in receipt:
        return True
    value = receipt.get(field)
    if value is None:
        return True
    if isinstance(value, (str, list, tuple, dict, set)) and len(value) == 0:
        return True
    return False


def _missing_required(receipt: Mapping[str, Any]) -> list[str]:
    return [f for f in REQUIRED_RECEIPT_FIELDS if _field_missing(receipt, f)]


def audit_receipts(receipts: Sequence[Mapping[str, Any]], ledger: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Return a fail-closed conflict/provenance audit for a receipt set."""
    receipt_list = [dict(r) for r in receipts]
    conflicts: list[dict[str, Any]] = []
    ledger = dict(ledger or {})

    for r in receipt_list:
        missing = _missing_required(r)
        if missing:
            conflicts.append({
                "type": "PROVENANCE_INCOMPLETE",
                "receipt_id": r.get("receipt_id", "<missing>"),
                "reason": "required receipt fields are missing or empty",
                "fields": missing,
                "recommended_action": "REQUEST_REPAIR",
            })
        if _field_missing(r, "sample_id") or str(r.get("sample_id", "")).lower() in {"none", "formula_only", "formula"}:
            conflicts.append({
                "type": "SAMPLE_ID_MISSING",
                "receipt_id": r.get("receipt_id", "<missing>"),
                "reason": "material evidence lacks a concrete sample identifier",
                "recommended_action": "REQUEST_SAMPLE_PROVENANCE",
            })
        if _target(r) in SC_TARGETS and _is_pearson_material(r):
            conflicts.append({
                "type": "CODOMAIN_MISROUTE",
                "receipt_id": r.get("receipt_id", "<missing>"),
                "reason": "Pearson NaEu(IO3)4 receipts belong to rare-earth quantum-memory coherence, not superconductivity",
                "recommended_action": "REROUTE_TO_RARE_EARTH_QUANTUM_MEMORY",
            })
        if _target(r) in SC_TARGETS and (_text(r.get("receipt_kind")) == "formula_only_claim" or _declares_ambient_claim(r) and _text(r.get("measurement_method")) == "claim_text_only"):
            conflicts.append({
                "type": "EXTRAORDINARY_UNVERIFIED",
                "receipt_id": r.get("receipt_id", "<missing>"),
                "reason": "extraordinary superconductivity claim is formula/text only",
                "recommended_action": "QUARANTINE_AND_REPRODUCE",
            })
        p = _pressure_gpa(r)
        if p is not None and p > 1.0 and _declares_ambient_claim(r):
            conflicts.append({
                "type": "CONDITION_CONFLATION",
                "receipt_id": r.get("receipt_id", "<missing>"),
                "reason": "high-pressure evidence is being used to imply ambient usability",
                "pressure_GPa": p,
                "recommended_action": "SPLIT_PRESSURE_CONDITIONED_AND_AMBIENT_CLAIMS",
            })

    by_slot: dict[tuple[str, str, str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for r in receipt_list:
        slots = r.get("updates_required_slots") or [r.get("receipt_kind", "unknown")]
        if not isinstance(slots, (list, tuple)):
            slots = [str(slots)]
        for slot in slots:
            by_slot[(_material(r), str(r.get("sample_id", "")), _target(r), str(slot))].append(r)

    for key, group in by_slot.items():
        if len(group) < 2:
            continue
        outcomes = {(_truthy_measurement(g.get("measured_value")), str(g.get("pass_fail", "pass")).lower()) for g in group}
        if len(outcomes) > 1:
            conflicts.append({
                "type": "MEASUREMENT_CONFLICT",
                "receipt_ids": [g.get("receipt_id", "<missing>") for g in group],
                "reason": f"same material/sample/codomain/slot carries conflicting outcomes: {key}",
                "recommended_action": "HOLD_AND_REQUIRE_REPLICATION",
            })

    by_material_target: dict[tuple[str, str], list[Mapping[str, Any]]] = defaultdict(list)
    for r in receipt_list:
        by_material_target[(_material(r), _target(r))].append(r)
    for key, group in by_material_target.items():
        sample_ids = {str(g.get("sample_id", "")) for g in group}
        if len(sample_ids) > 1 and any(g.get("replication_status") == "CONTRADICTORY" for g in group):
            conflicts.append({
                "type": "REPLICATION_CONFLICT",
                "receipt_ids": [g.get("receipt_id", "<missing>") for g in group],
                "reason": "replicated samples disagree and at least one receipt declares contradictory replication",
                "recommended_action": "HOLD_AND_REQUIRE_INDEPENDENT_REPLICATION",
            })

    conflict_types = sorted({c["type"] for c in conflicts}, key=lambda x: CONFLICT_PRECEDENCE.get(x, 99))
    if not conflicts:
        status = "CLEAR_FOR_UPDATE"
        route = "ACCEPT_TO_RECEIPT_UPDATE_LOOP"
        action = "CONSUME_RECEIPTS"
    elif "EXTRAORDINARY_UNVERIFIED" in conflict_types:
        status = "QUARANTINE"
        route = "QUARANTINED_BEFORE_UPDATE"
        action = "QUARANTINE_AND_REPRODUCE"
    elif "CONDITION_CONFLATION" in conflict_types:
        status = "SPLIT_CONDITIONED_CLAIM"
        route = "SPLIT_PRESSURE_CONDITIONED_CLAIM"
        action = "PRESERVE_AMBIENT_NONCLAIM"
    elif "CODOMAIN_MISROUTE" in conflict_types:
        status = "REROUTE_OR_REJECT"
        route = "REROUTE_TO_DECLARED_CODOMAIN"
        action = "REROUTE_RECEIPT"
    elif "MEASUREMENT_CONFLICT" in conflict_types or "REPLICATION_CONFLICT" in conflict_types:
        status = "HOLD_CONFLICT"
        route = "HOLD_PENDING_CONFLICT_RESOLUTION"
        action = "REQUIRE_INDEPENDENT_REPLICATION"
    else:
        status = "REPAIR_REQUIRED"
        route = "REPAIR_RECEIPT_CONTRACT"
        action = "REQUEST_REPAIR"

    return {
        "schema": "CMAL_PROVENANCE_CONFLICT_AUDIT_v1",
        "status": status,
        "route": route,
        "recommended_action": action,
        "conflict_types": conflict_types,
        "conflicts": conflicts,
        "receipt_count": len(receipt_list),
        "ledger_id": ledger.get("ledger_id", ""),
        "nonclaims": dict(NONCLAIM_EXPORTS),
    }


def summarize_audit(audit: Mapping[str, Any]) -> str:
    types = ", ".join(audit.get("conflict_types", ())) or "none"
    return f"{audit.get('status')} via {audit.get('route')} conflicts={types} action={audit.get('recommended_action')}"


def demo_cases() -> dict[str, list[dict[str, Any]]]:
    return {
        "clear_sc_bundle": [
            {"schema_version":"APFMaterialReceipt.v1","receipt_id":"D1","material_id":"bulk_sc","sample_id":"S1","target_codomain":"SC_MATERIAL_ADMISSIBILITY","receipt_kind":"meissner_response","measurement_method":"SQUID","control_vector":{"temperature_K":"sweep"},"measured_value":True,"uncertainty":{"declared":True},"instrument_or_protocol":"SQUID","provenance":{"declared":True},"replication_status":"REPLICATED","updates_required_slots":["meissner_or_diamagnetic_response"],"nonclaim_guard":["not_Tc_prediction"]}
        ],
        "pearson_misroute": [
            {"schema_version":"APFMaterialReceipt.v1","receipt_id":"D2","material_id":"NaEu(IO3)4","sample_id":"P1","target_codomain":"SC_MATERIAL_ADMISSIBILITY","receipt_kind":"linewidth","measurement_method":"photon_echo","control_vector":{"temperature_K":1.7},"measured_value":120,"uncertainty":{"declared":True},"instrument_or_protocol":"photon_echo","provenance":{"declared":True},"replication_status":"single_run","updates_required_slots":["homogeneous_linewidth"],"nonclaim_guard":["Pearson_superconductivity_claim=0"],"source_key":"pearson_dissertation_2025"}
        ],
        "pressure_conflation": [
            {"schema_version":"APFMaterialReceipt.v1","receipt_id":"D3","material_id":"hydride_template","sample_id":"H1","target_codomain":"SC_MATERIAL_ADMISSIBILITY","receipt_kind":"high_pressure_SC","measurement_method":"diamond_anvil_transport","control_vector":{"pressure_GPa":180,"ambient_claim":True},"measured_value":True,"uncertainty":{"declared":True},"instrument_or_protocol":"DAC","provenance":{"declared":True},"replication_status":"single_run","updates_required_slots":["pressure_conditioned_SC"],"nonclaim_guard":["ambient_usability_not_promoted"],"claim":{"ambient_usability":True}}
        ],
    }


def demo_matrix() -> dict[str, str]:
    return {name: audit_receipts(receipts)["status"] for name, receipts in demo_cases().items()}
