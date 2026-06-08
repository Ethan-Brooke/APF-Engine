"""Trace-to-scheme transport ledger bank.

v8.6 (2026-05-08 LATER-4): executable ledger architecture for the next
APF push after the v8.5 boundary bank.  This module does not evaluate QCD,
QED, EW, threshold, or counterterm maps.  It bank-registers the *pre-theorem
ledger* that a future trace-to-scheme transport theorem must satisfy before
APF_TRACE/W_TRACE quantities can be compared to physical reporting schemes.

Status discipline:
    - APF_TRACE / W_TRACE closure: closed upstream at [P_local].
    - Trace-to-scheme boundary discipline: closed upstream at [P_boundary].
    - This module: [P_ledger], an executable transport-contract architecture.
    - Physical scheme masses: still open; no physical mass vector is exported.

The point of v8.6 is to prevent the next phase from drifting into a hidden fit.
Every transport factor must declare its domain, codomain, dependencies,
external constants, counterterm slots, and whether it may consume target
observables.  In this bank, no factor may consume target masses or return
physical masses as APF predictions.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, Mapping, Tuple

from apf.trace_scheme_transport import (
    REQUIRED_TRANSPORT_FACTORS,
    FORBIDDEN_INVERSE_INPUTS,
    check_T_trace_to_scheme_boundary_bank_closure as _check_T_trace_to_scheme_boundary_bank_closure,
    check_T_trace_codomain_immutability as _check_T_trace_codomain_immutability,
    check_T_scheme_target_contract_declared as _check_T_scheme_target_contract_declared,
)
from apf.trace_sector_closure import check_T_W_trace_branch_local as _check_T_W_trace_branch_local


TRACE_INPUTS: Tuple[str, ...] = (
    "APF_TRACE charged-fermion vector",
    "W_TRACE branch",
    "trace-sector normalizers",
)

COLORED_BRANCH: Tuple[str, ...] = ("m_u", "m_c", "m_t", "m_d", "m_s", "m_b")
LEPTON_BRANCH: Tuple[str, ...] = ("m_e", "m_mu", "m_tau")
WEAK_BRANCH: Tuple[str, ...] = ("M_W_TRACE",)

REQUIRED_SCHEME_CONTRACT_FIELDS: Tuple[str, ...] = (
    "scheme_name",
    "reference_scale_or_convention",
    "renormalization_convention",
    "counterterm_family",
    "target_observable_family",
    "external_constants_ledger_id",
    "uncertainty_protocol_id",
)

EXTERNAL_CONSTANT_SLOTS: Tuple[str, ...] = (
    "alpha_s(mu) and/or Lambda_QCD convention for colored transport",
    "quark-threshold matching conventions and threshold order",
    "alpha_em(mu) or electroweak input basis for charged-lepton/EW transport",
    "weak input convention for W/on-shell comparisons",
    "renormalization scales and scale-variation envelope",
    "uncertainties, correlations, and provenance tags",
)

COUNTERTERM_SLOTS: Tuple[str, ...] = (
    "QCD running anomalous-dimension/counterterm slot",
    "QCD threshold matching slot",
    "QED charged-lepton running slot",
    "EW/Yukawa running slot",
    "on-shell or pole-convention conversion slot",
    "scheme-specific finite-part convention slot",
)

OPEN_PROOF_OBLIGATIONS: Tuple[str, ...] = (
    "derive or import the transport maps without using target masses as calibration data",
    "choose a canonical target scheme S and reference scale/convention before comparison",
    "evaluate QCD threshold and running maps for colored fermions",
    "evaluate QED/EW running maps for charged leptons and W_TRACE when relevant",
    "propagate external-constant uncertainties and correlations",
    "separate agreement assessment from parameter fitting",
)


@dataclass(frozen=True)
class SchemeContract:
    """Minimal target-scheme contract for future transport attempts."""

    scheme_name: str
    reference_scale_or_convention: str
    renormalization_convention: str
    counterterm_family: str
    target_observable_family: str
    external_constants_ledger_id: str
    uncertainty_protocol_id: str
    may_consume_target_masses: bool = False
    exports_physical_masses: bool = False


@dataclass(frozen=True)
class TransportFactor:
    """One declared factor in the trace-to-scheme transport ledger."""

    name: str
    domain: Tuple[str, ...]
    codomain: str
    depends_on: Tuple[str, ...]
    external_constant_slots: Tuple[str, ...]
    counterterm_slots: Tuple[str, ...]
    may_consume_target_observables: bool = False
    evaluated_in_this_bank: bool = False


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def _scheme_contract_template() -> SchemeContract:
    return SchemeContract(
        scheme_name="DECLARED_BY_FUTURE_TRANSPORT_THEOREM",
        reference_scale_or_convention="REQUIRED_BEFORE_COMPARISON",
        renormalization_convention="REQUIRED_BEFORE_COMPARISON",
        counterterm_family="REQUIRED_BEFORE_COMPARISON",
        target_observable_family="physical reporting scheme S(mu), not APF_TRACE",
        external_constants_ledger_id="REQUIRED_EXTERNAL_LEDGER",
        uncertainty_protocol_id="REQUIRED_UNCERTAINTY_PROTOCOL",
    )


def _factor_graph() -> Tuple[TransportFactor, ...]:
    return (
        TransportFactor(
            name="trace_input_lock",
            domain=TRACE_INPUTS,
            codomain="immutable APF_TRACE / W_TRACE inputs",
            depends_on=(),
            external_constant_slots=(),
            counterterm_slots=(),
        ),
        TransportFactor(
            name="scheme_contract",
            domain=("declared target scheme S", "declared scale/convention"),
            codomain="transport contract",
            depends_on=("trace_input_lock",),
            external_constant_slots=("external constants ledger id", "uncertainty protocol id"),
            counterterm_slots=("counterterm-family declaration", "scheme-specific finite-part convention slot"),
        ),
        TransportFactor(
            name="colored_qcd_transport_branch",
            domain=COLORED_BRANCH,
            codomain="colored-fermion scheme candidates, not physical APF predictions",
            depends_on=("scheme_contract",),
            external_constant_slots=(
                "alpha_s(mu) and/or Lambda_QCD convention for colored transport",
                "quark-threshold matching conventions and threshold order",
                "renormalization scales and scale-variation envelope",
            ),
            counterterm_slots=("QCD running anomalous-dimension/counterterm slot", "QCD threshold matching slot"),
        ),
        TransportFactor(
            name="lepton_qed_ew_transport_branch",
            domain=LEPTON_BRANCH,
            codomain="charged-lepton scheme candidates, not physical APF predictions",
            depends_on=("scheme_contract",),
            external_constant_slots=(
                "alpha_em(mu) or electroweak input basis for charged-lepton/EW transport",
                "renormalization scales and scale-variation envelope",
            ),
            counterterm_slots=("QED charged-lepton running slot", "EW/Yukawa running slot"),
        ),
        TransportFactor(
            name="weak_trace_transport_branch",
            domain=WEAK_BRANCH,
            codomain="W-scheme candidate, not physical APF prediction",
            depends_on=("scheme_contract",),
            external_constant_slots=("weak input convention for W/on-shell comparisons", "uncertainties, correlations, and provenance tags"),
            counterterm_slots=("EW/Yukawa running slot", "on-shell or pole-convention conversion slot"),
        ),
        TransportFactor(
            name="uncertainty_and_comparison_protocol",
            domain=("scheme candidates", "external constants ledger", "declared comparison metric"),
            codomain="comparison record only",
            depends_on=(
                "colored_qcd_transport_branch",
                "lepton_qed_ew_transport_branch",
                "weak_trace_transport_branch",
            ),
            external_constant_slots=("uncertainties, correlations, and provenance tags",),
            counterterm_slots=(),
        ),
    )


def _names(items: Iterable[TransportFactor]) -> Tuple[str, ...]:
    return tuple(item.name for item in items)


# ---------------------------------------------------------------------
# Bank-facing transport-ledger checks.
# ---------------------------------------------------------------------


def check_T_transport_ledger_status_declared() -> Dict[str, Any]:
    """Declare that v8.6 is a ledger architecture, not transport closure."""
    boundary = _check_T_trace_to_scheme_boundary_bank_closure()
    assert _passed(boundary)
    assert boundary.get("physical_transport_closed") is False
    return {
        "name": "T_transport_ledger_status_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger",
        "dependencies": ["T_trace_to_scheme_boundary_bank_closure"],
        "ledger_status": "transport architecture banked; transport formulas not evaluated",
        "closed_now": "ledger discipline and proof obligations",
        "open_next": "actual trace-to-scheme transport maps",
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "v8.6 banks the transport ledger architecture while preserving the open physical-transport boundary.",
    }


def check_T_transport_scheme_contract_schema_complete() -> Dict[str, Any]:
    """Certify the target-scheme contract schema required before comparison."""
    prior = _check_T_scheme_target_contract_declared()
    assert _passed(prior)
    contract = _scheme_contract_template()
    payload = asdict(contract)
    missing = [field for field in REQUIRED_SCHEME_CONTRACT_FIELDS if field not in payload]
    assert not missing
    assert contract.may_consume_target_masses is False
    assert contract.exports_physical_masses is False
    return {
        "name": "T_transport_scheme_contract_schema_complete",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger | no-smuggling",
        "required_fields": list(REQUIRED_SCHEME_CONTRACT_FIELDS),
        "template": payload,
        "may_consume_target_masses": False,
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "Any future physical comparison must first instantiate a full target-scheme contract.",
    }


def check_T_transport_factor_graph_acyclic() -> Dict[str, Any]:
    """Declare an acyclic dependency graph for the future transport map."""
    graph = _factor_graph()
    seen = set()
    edges = []
    for factor in graph:
        assert factor.name not in seen, f"duplicate factor {factor.name}"
        for dep in factor.depends_on:
            assert dep in seen, f"factor {factor.name} depends on unavailable or cyclic predecessor {dep}"
            edges.append((dep, factor.name))
        seen.add(factor.name)
    return {
        "name": "T_transport_factor_graph_acyclic",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger",
        "factors": [asdict(factor) for factor in graph],
        "edges": edges,
        "topological_order": list(_names(graph)),
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "The trace-to-scheme problem is staged as an acyclic ledger, not an implicit identity map.",
    }


def check_T_transport_branch_domains_partitioned() -> Dict[str, Any]:
    """Partition colored, charged-lepton, and W transport branches."""
    colored = set(COLORED_BRANCH)
    leptons = set(LEPTON_BRANCH)
    weak = set(WEAK_BRANCH)
    assert colored.isdisjoint(leptons)
    assert colored.isdisjoint(weak)
    assert leptons.isdisjoint(weak)
    assert len(colored | leptons | weak) == len(COLORED_BRANCH) + len(LEPTON_BRANCH) + len(WEAK_BRANCH)
    return {
        "name": "T_transport_branch_domains_partitioned",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger",
        "colored_branch": list(COLORED_BRANCH),
        "lepton_branch": list(LEPTON_BRANCH),
        "weak_branch": list(WEAK_BRANCH),
        "shared_contract_only": True,
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "QCD, QED/EW lepton, and W_TRACE transport branches are separated before formulas are attempted.",
    }


def check_T_external_constant_slots_declared_not_filled() -> Dict[str, Any]:
    """External constants are named slots with provenance, not hidden inputs."""
    graph = _factor_graph()
    slots = sorted({slot for factor in graph for slot in factor.external_constant_slots})
    assert set(EXTERNAL_CONSTANT_SLOTS).issubset(set(slots))
    return {
        "name": "T_external_constant_slots_declared_not_filled",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger | no-smuggling",
        "required_slots": list(EXTERNAL_CONSTANT_SLOTS),
        "declared_slots": slots,
        "filled_numeric_values_in_this_bank": {},
        "current_external_constants_used_for_closure": [],
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "Transport constants are ledger slots only; no hidden numerical constants are used to close physical masses.",
    }


def check_T_counterterm_slots_declared_not_evaluated() -> Dict[str, Any]:
    """Counterterm and finite-part slots are declared but unevaluated."""
    graph = _factor_graph()
    slots = sorted({slot for factor in graph for slot in factor.counterterm_slots})
    assert set(COUNTERTERM_SLOTS).issubset(set(slots))
    assert all(factor.evaluated_in_this_bank is False for factor in graph)
    return {
        "name": "T_counterterm_slots_declared_not_evaluated",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger | boundary",
        "required_counterterm_slots": list(COUNTERTERM_SLOTS),
        "declared_counterterm_slots": slots,
        "counterterm_values_evaluated": False,
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "The transport theorem has named counterterm slots, but this bank does not evaluate them.",
    }


def check_T_reference_scale_required_before_comparison() -> Dict[str, Any]:
    """A scheme comparison is illegal without a reference scale/convention."""
    contract = _scheme_contract_template()
    assert contract.reference_scale_or_convention == "REQUIRED_BEFORE_COMPARISON"
    return {
        "name": "T_reference_scale_required_before_comparison",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger | boundary",
        "required_contract_fields": ["scheme_name", "reference_scale_or_convention", "renormalization_convention"],
        "comparison_allowed_without_reference_scale": False,
        "canonical_scheme_selected_here": False,
        "canonical_scale_selected_here": False,
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "No physical comparison can be asserted until S(mu) or an equivalent scheme convention is declared.",
    }


def check_T_uncertainty_protocol_required() -> Dict[str, Any]:
    """Uncertainty propagation is a required ledger leg, not presentation polish."""
    graph = _factor_graph()
    assert "uncertainty_and_comparison_protocol" in _names(graph)
    protocol_requirements = (
        "external-constant uncertainties",
        "scale-variation envelope",
        "threshold-convention uncertainty",
        "scheme-conversion uncertainty",
        "correlation/provenance tags",
        "comparison metric declared before looking at target residuals",
    )
    return {
        "name": "T_uncertainty_protocol_required",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger",
        "protocol_requirements": list(protocol_requirements),
        "uncertainty_protocol_evaluated_here": False,
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "Trace-to-scheme transport must carry uncertainties and correlations as part of the theorem, not as after-the-fact prose.",
    }


def check_T_target_observables_not_transport_inputs() -> Dict[str, Any]:
    """Future transport may compare to targets only after maps are fixed."""
    graph = _factor_graph()
    forbidden_lower = " ".join(FORBIDDEN_INVERSE_INPUTS).lower()
    assert "identity map apf_trace == physical masses" in forbidden_lower
    assert all(factor.may_consume_target_observables is False for factor in graph)
    return {
        "name": "T_target_observables_not_transport_inputs",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger | no-smuggling",
        "forbidden_inverse_inputs": list(FORBIDDEN_INVERSE_INPUTS),
        "factors_may_consume_target_observables": {factor.name: factor.may_consume_target_observables for factor in graph},
        "used_target_observables_as_inputs": [],
        "comparison_after_transport_only": True,
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "Target observables are barred as transport inputs; they can enter only after the map is fixed for comparison.",
    }


def check_T_trace_values_remain_immutable_inputs() -> Dict[str, Any]:
    """Import the v8.5 trace vector and W_TRACE branch as immutable inputs."""
    trace = _check_T_trace_codomain_immutability()
    w = _check_T_W_trace_branch_local()
    assert _passed(trace) and _passed(w)
    assert trace.get("mutable_by_transport") is False
    assert w.get("exports_physical_M_W") is False
    return {
        "name": "T_trace_values_remain_immutable_inputs",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger | no-smuggling",
        "trace_codomain": trace.get("codomain"),
        "masses_GeV": trace.get("masses_GeV"),
        "M_W_TRACE_GeV": w.get("M_W_TRACE_GeV"),
        "mutable_by_transport": False,
        "retuning_allowed": False,
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "Transport consumes immutable APF_TRACE/W_TRACE inputs; it cannot retune the local trace sector.",
    }


def check_T_publication_claim_ladder_trace_vs_transport() -> Dict[str, Any]:
    """Bank the exact publication claim ladder for this phase."""
    return {
        "name": "T_publication_claim_ladder_trace_vs_transport",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger | publication-boundary",
        "allowed_claims": [
            "APF_TRACE/W_TRACE closure is locally banked at [P_local].",
            "Trace-to-scheme boundary discipline is banked at [P_boundary].",
            "Transport-ledger architecture is banked at [P_ledger].",
        ],
        "forbidden_claims": [
            "APF_TRACE masses are physical pole masses.",
            "APF_TRACE masses are already MSbar masses by identity.",
            "The codebase predicts physical charged-fermion masses without a transport theorem.",
            "Agreement residuals may be minimized by fitting a hidden scalar transport.",
        ],
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "The publication language is constrained before the next physical-mass paper draft is written.",
    }


def check_T_open_transport_proof_obligations_listed() -> Dict[str, Any]:
    """List the remaining theorem obligations explicitly."""
    required = set(REQUIRED_TRANSPORT_FACTORS)
    obligations_text = " ".join(OPEN_PROOF_OBLIGATIONS)
    assert "target masses" in obligations_text
    assert required
    return {
        "name": "T_open_transport_proof_obligations_listed",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger | open-problem-discipline",
        "required_transport_factors_from_v8_5": list(REQUIRED_TRANSPORT_FACTORS),
        "open_proof_obligations": list(OPEN_PROOF_OBLIGATIONS),
        "closed_by_this_bank": [],
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "The ledger names exactly what remains to be proved before physical scheme masses can be claimed.",
    }


def check_T_transport_ledger_bank_closure() -> Dict[str, Any]:
    """Master v8.6 closure: ledger architecture only, no physical transport."""
    deps = [
        check_T_transport_ledger_status_declared(),
        check_T_transport_scheme_contract_schema_complete(),
        check_T_transport_factor_graph_acyclic(),
        check_T_transport_branch_domains_partitioned(),
        check_T_external_constant_slots_declared_not_filled(),
        check_T_counterterm_slots_declared_not_evaluated(),
        check_T_reference_scale_required_before_comparison(),
        check_T_uncertainty_protocol_required(),
        check_T_target_observables_not_transport_inputs(),
        check_T_trace_values_remain_immutable_inputs(),
        check_T_publication_claim_ladder_trace_vs_transport(),
        check_T_open_transport_proof_obligations_listed(),
    ]
    assert all(_passed(dep) for dep in deps)
    return {
        "name": "T_transport_ledger_bank_closure",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_ledger",
        "dependencies": [dep["name"] for dep in deps],
        "scheme_contract_template": asdict(_scheme_contract_template()),
        "factor_graph": [asdict(factor) for factor in _factor_graph()],
        "open_next": "derive/evaluate actual trace-to-scheme transport maps under the ledger",
        "exports_physical_scheme_masses": False,
        "physical_transport_closed": False,
        "key_result": "The trace-to-scheme transport ledger is bank-closed as architecture only; physical transport remains open.",
    }


_CHECKS = {
    "T_transport_ledger_status_declared": check_T_transport_ledger_status_declared,
    "T_transport_scheme_contract_schema_complete": check_T_transport_scheme_contract_schema_complete,
    "T_transport_factor_graph_acyclic": check_T_transport_factor_graph_acyclic,
    "T_transport_branch_domains_partitioned": check_T_transport_branch_domains_partitioned,
    "T_external_constant_slots_declared_not_filled": check_T_external_constant_slots_declared_not_filled,
    "T_counterterm_slots_declared_not_evaluated": check_T_counterterm_slots_declared_not_evaluated,
    "T_reference_scale_required_before_comparison": check_T_reference_scale_required_before_comparison,
    "T_uncertainty_protocol_required": check_T_uncertainty_protocol_required,
    "T_target_observables_not_transport_inputs": check_T_target_observables_not_transport_inputs,
    "T_trace_values_remain_immutable_inputs": check_T_trace_values_remain_immutable_inputs,
    "T_publication_claim_ladder_trace_vs_transport": check_T_publication_claim_ladder_trace_vs_transport,
    "T_open_transport_proof_obligations_listed": check_T_open_transport_proof_obligations_listed,
    "T_transport_ledger_bank_closure": check_T_transport_ledger_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register trace-to-scheme transport-ledger checks into the global bank."""
    registry.update(_CHECKS)


def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _CHECKS.items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(row["passed"] for row in rows)
    return {
        "passed": sum(1 for row in rows if row["passed"]),
        "total": len(rows),
        "status": "TRACE_TRANSPORT_LEDGER_BANK_PASS" if ok else "TRACE_TRANSPORT_LEDGER_BANK_FAIL",
        "bank_registered": True,
        "physical_transport_closed": False,
        "exports_physical_scheme_masses": False,
        "results": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))
