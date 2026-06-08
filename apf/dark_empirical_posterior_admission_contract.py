"""
APF dark empirical-posterior admission contract.

Purpose
-------
Formalize the exact evidence contract for admitting DARK_EMPIRICAL_POSTERIOR
through the Interface Engine without promoting dark robust empirical P from
profile probes, adapter smoke, or launch infrastructure alone.

Boundary
--------
This module is an admission contract and verifier.  It does not supply MCMC or
profile posterior artifacts.  It keeps the following flags reserved at zero
unless a later evidence pack supplies converged posterior/profile artifacts and
passes the declared no-smuggling gate:

    Export_dark_RouteC_APF2_posterior_P = 0
    Export_dark_RouteC_MCMC_posterior_P = 0
    Export_dark_robust_empirical_P = 0

Top check:
    check_T_dark_empirical_posterior_admission_contract_P
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence, Tuple
import csv
import json

try:
    from apf.interface_dark_posterior_evidence_intake import (
        build_dark_posterior_evidence_intake,
        status_by_task_id as dark_intake_status_by_task_id,
    )
except Exception:  # pragma: no cover
    build_dark_posterior_evidence_intake = None
    dark_intake_status_by_task_id = None


VERSION = "APF_DARK_EMPIRICAL_POSTERIOR_ADMISSION_CONTRACT_v1"
MARKER = "DARK_EMPIRICAL_POSTERIOR_ADMISSION_CONTRACT_PASS"


class ContractSlotStatus(str, Enum):
    PRESENT_CANDIDATE = "PRESENT_CANDIDATE"
    OPEN_REQUIRED = "OPEN_REQUIRED"
    FORBIDDEN_INPUT_GUARD = "FORBIDDEN_INPUT_GUARD"


class AdmissionVerdict(str, Enum):
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"
    READY_TO_RERUN = "READY_TO_RERUN"
    BLOCKED_BY_PROVENANCE = "BLOCKED_BY_PROVENANCE"


@dataclass(frozen=True)
class PosteriorAdmissionSlot:
    key: str
    status: ContractSlotStatus
    description: str
    acceptance_criteria: str
    satisfies_adapter_fields: Tuple[str, ...]
    supporting_artifacts: Tuple[str, ...]
    forbidden_inputs: Tuple[str, ...] = tuple()
    example_value: Any = "TODO"

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["status"] = self.status.value
        return data


@dataclass(frozen=True)
class PosteriorAdmissionContract:
    version: str
    verdict: AdmissionVerdict
    slots: Tuple[PosteriorAdmissionSlot, ...]
    preserved_nonclaim_exports: Mapping[str, int]
    adapter_patch_if_admitted: Mapping[str, bool]
    candidate_support_summary: Mapping[str, Any]
    no_smuggling_guard: str
    rerun_command: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "verdict": self.verdict.value,
            "slots": [slot.to_dict() for slot in self.slots],
            "preserved_nonclaim_exports": dict(self.preserved_nonclaim_exports),
            "adapter_patch_if_admitted": dict(self.adapter_patch_if_admitted),
            "candidate_support_summary": dict(self.candidate_support_summary),
            "no_smuggling_guard": self.no_smuggling_guard,
            "rerun_command": self.rerun_command,
        }


REQUIRED_SLOT_KEYS: Tuple[str, ...] = (
    "posterior_runtime_artifacts",
    "convergence_diagnostics",
    "frozen_apf2_coefficient_guard",
    "no_posterior_output_as_input_guard",
    "declared_threshold_rule",
    "profile_mcmc_adjudication_table",
)

PRESERVED_NONCLAIM_EXPORTS: Mapping[str, int] = {
    "Export_dark_RouteC_APF2_posterior_P": 0,
    "Export_dark_RouteC_MCMC_posterior_P": 0,
    "Export_dark_robust_empirical_P": 0,
}

FORBIDDEN_POSTERIOR_INPUTS: Tuple[str, ...] = (
    "posterior_samples",
    "posterior_mean",
    "posterior_bestfit",
    "profile_minimum_chi2",
    "observed_delta_chi2_as_input",
    "fitted_APF2_coefficients",
    "target_acceptance_verdict",
)

NO_SMUGGLING_GUARD = (
    "The posterior or profile output may be compared after the evaluator runs, but it may not appear as an input "
    "to the evaluator map, APF2 coefficients, route configuration, threshold selection, or rerun patch."
)


def _slot(
    key: str,
    status: ContractSlotStatus,
    description: str,
    criteria: str,
    fields: Sequence[str],
    artifacts: Sequence[str],
    *,
    forbidden: Sequence[str] = tuple(),
    example: Any = "TODO",
) -> PosteriorAdmissionSlot:
    return PosteriorAdmissionSlot(
        key=key,
        status=status,
        description=description,
        acceptance_criteria=criteria,
        satisfies_adapter_fields=tuple(fields),
        supporting_artifacts=tuple(artifacts),
        forbidden_inputs=tuple(forbidden),
        example_value=example,
    )


def _intake_summary() -> Mapping[str, Any]:
    if build_dark_posterior_evidence_intake is None:
        return {"intake_available": False}
    try:
        intake = build_dark_posterior_evidence_intake()
        statuses = dark_intake_status_by_task_id(intake) if dark_intake_status_by_task_id is not None else {}
        return {
            "intake_available": True,
            "intake_status": intake.status,
            "task_status": dict(statuses),
            "profile_probe_accept_at_95": intake.summary.get("profile_probe_accept_at_95"),
            "candidate_evidence_present_items": intake.summary.get("candidate_evidence_present_items"),
            "open_items": intake.summary.get("open_items"),
            "pack_probes_loaded": intake.summary.get("pack_probes_loaded"),
            "pack_probes_total": intake.summary.get("pack_probes_total"),
        }
    except Exception as exc:
        return {"intake_available": False, "error": repr(exc)}


def build_admission_contract(evidence: Optional[Mapping[str, Any]] = None) -> PosteriorAdmissionContract:
    """Build the conservative dark empirical-posterior admission contract.

    A supplied evidence mapping can be used by future runs.  In the current
    sandbox sprint the mapping is absent/empty, so the contract remains open.
    """
    evidence = dict(evidence or {})
    candidate = _intake_summary()

    def present(key: str) -> bool:
        value = evidence.get(key)
        if value in (None, "", "TODO", [], {}):
            return False
        return True

    smuggled = sorted(set(str(x) for x in evidence.get("inputs_used", ())) & set(FORBIDDEN_POSTERIOR_INPUTS))

    runtime_present = present("posterior_runtime_artifacts")
    convergence_present = present("convergence_diagnostics")
    coefficient_guard_present = present("frozen_apf2_coefficient_guard")
    no_smuggle_present = present("no_posterior_output_as_input_guard") and not smuggled
    threshold_present = present("declared_threshold_rule")
    table_present = present("profile_mcmc_adjudication_table")

    slots = (
        _slot(
            "posterior_runtime_artifacts",
            ContractSlotStatus.PRESENT_CANDIDATE if runtime_present else ContractSlotStatus.OPEN_REQUIRED,
            "Actual MCMC/profile runtime artifacts for the frozen APF2 Route-C posterior.",
            "Must include chain/profile outputs, run metadata, config hash/path, and data-compilation labels; smoke/profile-probe artifacts alone do not satisfy this slot.",
            ("posterior_closed", "run_completed"),
            tuple(evidence.get("posterior_runtime_artifacts", ())) if runtime_present else ("TODO: external MCMC/profile posterior result pack",),
        ),
        _slot(
            "convergence_diagnostics",
            ContractSlotStatus.PRESENT_CANDIDATE if convergence_present else ContractSlotStatus.OPEN_REQUIRED,
            "Convergence diagnostics for the posterior/profile run.",
            "Must supply R-hat/ESS/trace diagnostics or an explicitly accepted profile-likelihood substitute.",
            ("chains_converged",),
            tuple(evidence.get("convergence_diagnostics", ())) if convergence_present else ("TODO: R-hat/ESS or declared substitute",),
        ),
        _slot(
            "frozen_apf2_coefficient_guard",
            ContractSlotStatus.PRESENT_CANDIDATE if coefficient_guard_present else ContractSlotStatus.OPEN_REQUIRED,
            "Guard that APF2 coefficients/source table are frozen before posterior evaluation.",
            "Must name the frozen APF2 source table/hash and certify no coefficient refit or posterior-conditioned coefficient adjustment.",
            ("evaluator_map_found",),
            tuple(evidence.get("frozen_apf2_coefficient_guard", ())) if coefficient_guard_present else ("APF_DARK_SECTOR_ROUTE_C_APF2_TABULATED_W2_COBAYA_BRIDGE_v1",),
            forbidden=("fitted_APF2_coefficients",),
        ),
        _slot(
            "no_posterior_output_as_input_guard",
            ContractSlotStatus.FORBIDDEN_INPUT_GUARD if no_smuggle_present else ContractSlotStatus.OPEN_REQUIRED,
            "No-smuggling guard for posterior/profile outputs.",
            "Must list all evaluator inputs and certify none is a posterior output, profile minimum, target verdict, or fitted comparator residual.",
            ("target_value_consumed",),
            tuple(evidence.get("no_posterior_output_as_input_guard", ())) if no_smuggle_present else ("TODO: input ledger + forbidden-input audit",),
            forbidden=FORBIDDEN_POSTERIOR_INPUTS,
        ),
        _slot(
            "declared_threshold_rule",
            ContractSlotStatus.PRESENT_CANDIDATE if threshold_present else ContractSlotStatus.OPEN_REQUIRED,
            "Declared profile/MCMC threshold rule.",
            "Must freeze acceptance threshold before reading the posterior result; examples include 2-dof chi-square threshold or declared posterior credibility criterion.",
            ("posterior_closed", "robustness_checks_passed"),
            tuple(evidence.get("declared_threshold_rule", ())) if threshold_present else ("TODO: frozen threshold/adjudication rule",),
        ),
        _slot(
            "profile_mcmc_adjudication_table",
            ContractSlotStatus.PRESENT_CANDIDATE if table_present else ContractSlotStatus.OPEN_REQUIRED,
            "Adjudication table over profile/MCMC datasets and variants.",
            "Must list each dataset/config variant, posterior/profile verdict, convergence status, and known environmental blockers.",
            ("posterior_closed", "robustness_checks_passed"),
            tuple(evidence.get("profile_mcmc_adjudication_table", ())) if table_present else ("TODO: profile/MCMC adjudication table",),
        ),
    )

    all_required_present = all(slot.status != ContractSlotStatus.OPEN_REQUIRED for slot in slots)
    if smuggled:
        verdict = AdmissionVerdict.BLOCKED_BY_PROVENANCE
    elif all_required_present:
        verdict = AdmissionVerdict.READY_TO_RERUN
    else:
        verdict = AdmissionVerdict.OPEN_EVIDENCE_REQUIRED

    return PosteriorAdmissionContract(
        version=VERSION,
        verdict=verdict,
        slots=slots,
        preserved_nonclaim_exports=PRESERVED_NONCLAIM_EXPORTS,
        adapter_patch_if_admitted={
            "route_built": True,
            "run_completed": True,
            "data_ledger_clean": True,
            "evaluator_map_found": True,
            "codomain_transport_found": True,
            "chains_converged": verdict == AdmissionVerdict.READY_TO_RERUN,
            "posterior_closed": verdict == AdmissionVerdict.READY_TO_RERUN,
            "robustness_checks_passed": verdict == AdmissionVerdict.READY_TO_RERUN,
            "target_value_consumed": False,
        },
        candidate_support_summary=candidate,
        no_smuggling_guard=NO_SMUGGLING_GUARD,
        rerun_command="python scripts/run_first_real_dark_obligation.py",
    )


def evidence_template(contract: Optional[PosteriorAdmissionContract] = None) -> Dict[str, Any]:
    contract = contract or build_admission_contract()
    return {
        slot.key: {
            "status": slot.status.value,
            "example_value": slot.example_value,
            "acceptance_criteria": slot.acceptance_criteria,
            "forbidden_inputs": list(slot.forbidden_inputs),
            "satisfies_adapter_fields": list(slot.satisfies_adapter_fields),
        }
        for slot in contract.slots
    }


def render_markdown(contract: Optional[PosteriorAdmissionContract] = None) -> str:
    contract = contract or build_admission_contract()
    lines = [
        "# APF Dark Empirical Posterior Admission Contract v1",
        "",
        f"- Verdict: `{contract.verdict.value}`",
        "- Boundary: profile-probe support and MCMC-launch infrastructure are not posterior closure.",
        "- Positive effect now admitted: dark evaluator-map candidate can be wired into the live adapter.",
        "- Preserved nonclaims:",
    ]
    for key, value in contract.preserved_nonclaim_exports.items():
        lines.append(f"  - `{key} = {value}`")
    lines += ["", "## Contract slots", "", "| Slot | Status | Adapter fields | Criteria |", "|---|---|---|---|"]
    for slot in contract.slots:
        lines.append(f"| `{slot.key}` | `{slot.status.value}` | `{'; '.join(slot.satisfies_adapter_fields)}` | {slot.acceptance_criteria} |")
    lines += ["", "## No-smuggling guard", "", contract.no_smuggling_guard, ""]
    lines += ["## Candidate support summary", "", "```json", json.dumps(contract.candidate_support_summary, indent=2, default=str), "```", ""]
    return "\n".join(lines).rstrip() + "\n"


def export_contract(out_dir: str | Path) -> Dict[str, str]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    contract = build_admission_contract()
    json_path = out / "DARK_EMPIRICAL_POSTERIOR_ADMISSION_CONTRACT.json"
    template_path = out / "EVIDENCE_TEMPLATE.json"
    md_path = out / "README.md"
    csv_path = out / "posterior_admission_slots.csv"
    json_path.write_text(json.dumps(contract.to_dict(), indent=2, default=str), encoding="utf-8")
    template_path.write_text(json.dumps(evidence_template(contract), indent=2, default=str), encoding="utf-8")
    md_path.write_text(render_markdown(contract), encoding="utf-8")
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["key", "status", "satisfies_adapter_fields", "supporting_artifacts", "forbidden_inputs", "acceptance_criteria"])
        writer.writeheader()
        for slot in contract.slots:
            writer.writerow({
                "key": slot.key,
                "status": slot.status.value,
                "satisfies_adapter_fields": ";".join(slot.satisfies_adapter_fields),
                "supporting_artifacts": ";".join(slot.supporting_artifacts),
                "forbidden_inputs": ";".join(slot.forbidden_inputs),
                "acceptance_criteria": slot.acceptance_criteria,
            })
    return {"json": str(json_path), "template": str(template_path), "markdown": str(md_path), "csv": str(csv_path)}


def _res(name: str, passed: bool, **data: Any) -> Dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "consistent": bool(passed),
        "status": "PASS" if passed else "FAIL",
        "epistemic": VERSION,
        "marker": MARKER if passed else "",
        "data": data,
    }


def check_T_posterior_contract_required_slots_declared() -> Dict[str, Any]:
    c = build_admission_contract()
    keys = {slot.key for slot in c.slots}
    tests = {
        "all_required_keys_present": set(REQUIRED_SLOT_KEYS) == keys,
        "six_slots": len(c.slots) == 6,
        "all_have_criteria": all(bool(slot.acceptance_criteria) for slot in c.slots),
        "all_have_adapter_fields": all(bool(slot.satisfies_adapter_fields) for slot in c.slots),
    }
    return _res("check_T_posterior_contract_required_slots_declared", all(tests.values()), tests=tests, keys=sorted(keys))


def check_T_posterior_contract_preserves_nonclaims() -> Dict[str, Any]:
    c = build_admission_contract()
    tests = {
        "apf2_posterior_zero": c.preserved_nonclaim_exports.get("Export_dark_RouteC_APF2_posterior_P") == 0,
        "mcmc_posterior_zero": c.preserved_nonclaim_exports.get("Export_dark_RouteC_MCMC_posterior_P") == 0,
        "robust_empirical_zero": c.preserved_nonclaim_exports.get("Export_dark_robust_empirical_P") == 0,
        "verdict_open_without_artifacts": c.verdict == AdmissionVerdict.OPEN_EVIDENCE_REQUIRED,
    }
    return _res("check_T_posterior_contract_preserves_nonclaims", all(tests.values()), tests=tests, preserved=dict(c.preserved_nonclaim_exports))


def check_T_posterior_contract_no_smuggling_guard() -> Dict[str, Any]:
    c = build_admission_contract()
    guard_slot = next(slot for slot in c.slots if slot.key == "no_posterior_output_as_input_guard")
    tests = {
        "forbidden_inputs_declared": set(FORBIDDEN_POSTERIOR_INPUTS).issubset(set(guard_slot.forbidden_inputs)),
        "guard_mentions_no_input": "may not appear as an input" in c.no_smuggling_guard,
        "target_consumed_patch_false": c.adapter_patch_if_admitted.get("target_value_consumed") is False,
    }
    return _res("check_T_posterior_contract_no_smuggling_guard", all(tests.values()), tests=tests)


def check_T_posterior_contract_evaluator_admission_separated() -> Dict[str, Any]:
    c = build_admission_contract()
    summary = dict(c.candidate_support_summary)
    tests = {
        "intake_available": summary.get("intake_available") is True,
        "evaluator_candidate_present": summary.get("task_status", {}).get("DARK_EVALUATOR_MAP") == "CANDIDATE_EVIDENCE_PRESENT",
        "posterior_still_open": summary.get("task_status", {}).get("DARK_EMPIRICAL_POSTERIOR") == "OPEN_EVIDENCE_REQUIRED",
        "adapter_evaluator_patch_true": c.adapter_patch_if_admitted.get("evaluator_map_found") is True,
        "adapter_posterior_patch_false": c.adapter_patch_if_admitted.get("posterior_closed") is False,
    }
    return _res("check_T_posterior_contract_evaluator_admission_separated", all(tests.values()), tests=tests, summary=summary)


def check_T_dark_empirical_posterior_admission_contract_P() -> Dict[str, Any]:
    checks = [
        check_T_posterior_contract_required_slots_declared(),
        check_T_posterior_contract_preserves_nonclaims(),
        check_T_posterior_contract_no_smuggling_guard(),
        check_T_posterior_contract_evaluator_admission_separated(),
    ]
    ok = all(c.get("passed") for c in checks)
    return _res("check_T_dark_empirical_posterior_admission_contract_P", ok, subchecks=[c["name"] for c in checks], marker=MARKER)


CHECKS = {
    "check_T_posterior_contract_required_slots_declared": check_T_posterior_contract_required_slots_declared,
    "check_T_posterior_contract_preserves_nonclaims": check_T_posterior_contract_preserves_nonclaims,
    "check_T_posterior_contract_no_smuggling_guard": check_T_posterior_contract_no_smuggling_guard,
    "check_T_posterior_contract_evaluator_admission_separated": check_T_posterior_contract_evaluator_admission_separated,
    "check_T_dark_empirical_posterior_admission_contract_P": check_T_dark_empirical_posterior_admission_contract_P,
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
            raise TypeError("Unsupported registry type for dark_empirical_posterior_admission_contract.register")
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    out = run_all()
    ok = all(x.get("passed") for x in out.values())
    print(json.dumps(out, indent=2, sort_keys=True, default=str))
    print(MARKER if ok else "DARK_EMPIRICAL_POSTERIOR_ADMISSION_CONTRACT_FAIL")
    raise SystemExit(0 if ok else 1)
