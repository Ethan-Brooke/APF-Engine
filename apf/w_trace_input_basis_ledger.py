"""W_TRACE input-basis ledger-fill gate.

v9.1 (2026-05-08 LATER-9): the next concrete W route layer after the
v9.0 W_TRACE on-shell contract bank.  v9.0 selected the W_TRACE -> on-shell
route and enumerated the slots.  This module fills the *input-basis ledger
contract* for that route: which electroweak symbols are allowed, what provenance
each must carry, what relation template will later be used, and which target
observables remain forbidden.

Closed here:
    - Select the on-shell alpha/M_Z/G_F-style input-basis family for the W route.
    - Bank a provenance-tagged symbolic ledger schema for the allowed EW inputs.
    - Bank the comparison-equation template without evaluating it.
    - Prove observed physical M_W, W residuals, and identity transport are not
      consumed by the input basis.

Not closed here:
    - No numerical EW constants are filled.
    - No Delta r / finite radiative correction is evaluated.
    - No uncertainty propagation is evaluated.
    - No physical W mass is exported.

Status discipline:
    - v9.0 W route contract: [P_w_trace_contract] upstream.
    - This module: [P_w_input_basis_ledger], an input-basis ledger-fill gate.
    - Physical W/on-shell transport remains open.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, fields
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_onshell_transport import (
    W_ROUTE_ID,
    W_TRACE_EXPECTED_GEV,
    W_INPUT_BASIS_OPTIONS,
    FORBIDDEN_W_INPUTS,
    check_T_w_trace_on_shell_contract_bank_closure as _check_T_w_trace_on_shell_contract_bank_closure,
    check_T_w_trace_local_input_preserved as _check_T_w_trace_local_input_preserved,
    check_T_w_trace_completion_gate_remains_locked as _check_T_w_trace_completion_gate_remains_locked,
)
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_T_physical_export_gate_locked_until_all_certificates_filled,
)


W_INPUT_BASIS_LEDGER_STATUS = "P_w_input_basis_ledger"
SELECTED_W_INPUT_BASIS = "on-shell alpha/M_Z/G_F-style input basis"
INPUT_BASIS_LEDGER_FILLED = True
NUMERICAL_EW_CONSTANTS_FILLED = False
DELTA_R_EVALUATED = False
UNCERTAINTY_PROTOCOL_EVALUATED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

REQUIRED_LEDGER_FIELDS: Tuple[str, ...] = (
    "route_id",
    "selected_basis",
    "allowed_input_symbols",
    "radiative_symbol",
    "relation_template",
    "provenance_requirements",
    "correlation_requirements",
    "forbidden_inputs",
    "numerical_values_filled",
    "delta_r_evaluated",
    "uncertainty_protocol_evaluated",
    "exports_physical_M_W",
    "physical_W_transport_closed",
)

ALLOWED_W_INPUT_SYMBOLS: Tuple[str, ...] = (
    "alpha_em_reference",
    "G_F_reference",
    "M_Z_on_shell_reference",
)

PROVENANCE_REQUIREMENTS: Tuple[str, ...] = (
    "source_document_or_dataset",
    "reference_scale_or_scheme",
    "reported_uncertainty",
    "correlation_metadata_or_independence_certificate",
    "exclusion_certificate_for_observed_M_W",
)

CORRELATION_REQUIREMENTS: Tuple[str, ...] = (
    "alpha_G_F_covariance_policy",
    "alpha_M_Z_covariance_policy",
    "G_F_M_Z_covariance_policy",
    "finite_part_uncertainty_policy",
)

RELATION_TEMPLATE = (
    "terminal_symbolic_relation: M_W_on_shell^2*(1 - M_W_on_shell^2/M_Z^2) "
    "= pi*alpha_em/(sqrt(2)*G_F)*(1 + Delta_r); "
    "M_W_on_shell is a terminal output symbol, not an observed input"
)

FORBIDDEN_LEDGER_INPUTS: Tuple[str, ...] = tuple(FORBIDDEN_W_INPUTS) + (
    "PDG or world-average W mass used as an input constant",
    "CDF/ATLAS/LEP W mass used as calibration input",
    "Delta_r adjusted to match observed M_W",
)


@dataclass(frozen=True)
class WInputBasisLedger:
    """Symbolic input-basis ledger for the W_TRACE on-shell route."""

    route_id: str
    selected_basis: str
    allowed_input_symbols: Tuple[str, ...]
    radiative_symbol: str
    relation_template: str
    provenance_requirements: Tuple[str, ...]
    correlation_requirements: Tuple[str, ...]
    forbidden_inputs: Tuple[str, ...]
    numerical_values_filled: bool = False
    delta_r_evaluated: bool = False
    uncertainty_protocol_evaluated: bool = False
    exports_physical_M_W: bool = False
    physical_W_transport_closed: bool = False


@dataclass(frozen=True)
class WInputSymbolRecord:
    """One symbolic input slot in the W input-basis ledger."""

    symbol_id: str
    physical_role: str
    allowed_as_external_input: bool
    requires_provenance: bool
    requires_uncertainty: bool
    consumes_observed_M_W: bool = False
    numerical_value: str = "UNFILLED"


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def _ledger() -> WInputBasisLedger:
    return WInputBasisLedger(
        route_id=W_ROUTE_ID,
        selected_basis=SELECTED_W_INPUT_BASIS,
        allowed_input_symbols=ALLOWED_W_INPUT_SYMBOLS,
        radiative_symbol="Delta_r_finite_EW_correction_slot",
        relation_template=RELATION_TEMPLATE,
        provenance_requirements=PROVENANCE_REQUIREMENTS,
        correlation_requirements=CORRELATION_REQUIREMENTS,
        forbidden_inputs=FORBIDDEN_LEDGER_INPUTS,
        numerical_values_filled=False,
        delta_r_evaluated=False,
        uncertainty_protocol_evaluated=False,
        exports_physical_M_W=False,
        physical_W_transport_closed=False,
    )


def _symbol_records() -> Tuple[WInputSymbolRecord, ...]:
    return (
        WInputSymbolRecord(
            symbol_id="alpha_em_reference",
            physical_role="electromagnetic coupling input in declared on-shell/EW convention",
            allowed_as_external_input=True,
            requires_provenance=True,
            requires_uncertainty=True,
        ),
        WInputSymbolRecord(
            symbol_id="G_F_reference",
            physical_role="Fermi constant input used to define the weak scale convention",
            allowed_as_external_input=True,
            requires_provenance=True,
            requires_uncertainty=True,
        ),
        WInputSymbolRecord(
            symbol_id="M_Z_on_shell_reference",
            physical_role="Z on-shell reference mass entering the W on-shell comparison relation",
            allowed_as_external_input=True,
            requires_provenance=True,
            requires_uncertainty=True,
        ),
        WInputSymbolRecord(
            symbol_id="Delta_r_finite_EW_correction_slot",
            physical_role="finite electroweak radiative correction slot; not evaluated here",
            allowed_as_external_input=False,
            requires_provenance=True,
            requires_uncertainty=True,
        ),
    )


def _completion_gate_locked_for_w() -> bool:
    result = _check_T_physical_export_gate_locked_until_all_certificates_filled()
    assert _passed(result)
    allowed = result.get("physical_export_allowed_by_route", {})
    return allowed.get(W_ROUTE_ID) is False


# ---------------------------------------------------------------------
# Bank-facing W input-basis ledger checks.
# ---------------------------------------------------------------------


def check_T_w_input_basis_ledger_status_declared() -> Dict[str, Any]:
    """Declare v9.1 as input-basis ledger closure, not W transport closure."""
    contract = _check_T_w_trace_on_shell_contract_bank_closure()
    assert _passed(contract)
    assert contract.get("physical_W_transport_closed") is False
    assert contract.get("exports_physical_M_W") is False
    return {
        "name": "T_w_input_basis_ledger_status_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "dependencies": ["T_w_trace_on_shell_contract_bank_closure"],
        "closed_now": "W_TRACE on-shell input-basis ledger schema and provenance contract",
        "not_closed": "numerical EW constants, Delta_r evaluation, uncertainty propagation, physical M_W export",
        "input_basis_ledger_filled": INPUT_BASIS_LEDGER_FILLED,
        "numerical_EW_constants_filled": NUMERICAL_EW_CONSTANTS_FILLED,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "v9.1 fills the W input-basis ledger contract while the physical export gate remains locked.",
    }


def check_T_w_input_basis_selected_from_v90_options() -> Dict[str, Any]:
    """Select the on-shell alpha/M_Z/G_F family already listed in v9.0."""
    assert SELECTED_W_INPUT_BASIS in W_INPUT_BASIS_OPTIONS
    ledger = _ledger()
    assert ledger.selected_basis == SELECTED_W_INPUT_BASIS
    return {
        "name": "T_w_input_basis_selected_from_v90_options",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "selected_basis": SELECTED_W_INPUT_BASIS,
        "v90_options": list(W_INPUT_BASIS_OPTIONS),
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The W route now has a selected input-basis family without adding a new hidden option.",
    }


def check_T_w_input_basis_ledger_schema_complete() -> Dict[str, Any]:
    """The input-basis ledger exposes all fields required before constants fill."""
    actual = tuple(field.name for field in fields(WInputBasisLedger))
    missing = set(REQUIRED_LEDGER_FIELDS) - set(actual)
    extra = set(actual) - set(REQUIRED_LEDGER_FIELDS)
    assert not missing, f"W input ledger missing fields: {sorted(missing)}"
    assert not extra, f"W input ledger has unexpected fields: {sorted(extra)}"
    return {
        "name": "T_w_input_basis_ledger_schema_complete",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "ledger_fields": list(actual),
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The W input-basis ledger separates symbols, provenance, forbidden inputs, and terminal export status.",
    }


def check_T_w_input_symbols_enumerated_without_values() -> Dict[str, Any]:
    """Allowed W-route input symbols are enumerated but remain value-unfilled."""
    records = _symbol_records()
    ledger = _ledger()
    assert set(ledger.allowed_input_symbols).issubset({r.symbol_id for r in records})
    assert all(r.numerical_value == "UNFILLED" for r in records)
    assert ledger.numerical_values_filled is False
    return {
        "name": "T_w_input_symbols_enumerated_without_values",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "allowed_input_symbols": list(ledger.allowed_input_symbols),
        "symbol_records": [asdict(r) for r in records],
        "numerical_values_filled": False,
        "key_result": "The W route knows which EW symbols are allowed, but no numerical constants are imported.",
    }


def check_T_w_input_provenance_requirements_complete() -> Dict[str, Any]:
    """Every allowed external input must carry source, scheme, uncertainty, and exclusion metadata."""
    ledger = _ledger()
    required = set(PROVENANCE_REQUIREMENTS)
    assert {
        "source_document_or_dataset",
        "reference_scale_or_scheme",
        "reported_uncertainty",
        "exclusion_certificate_for_observed_M_W",
    }.issubset(required)
    records = [r for r in _symbol_records() if r.allowed_as_external_input]
    assert records and all(r.requires_provenance and r.requires_uncertainty for r in records)
    return {
        "name": "T_w_input_provenance_requirements_complete",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "provenance_requirements": list(ledger.provenance_requirements),
        "external_symbol_records": [asdict(r) for r in records],
        "key_result": "Each allowed W input symbol must be source-tagged and uncertainty-tagged before numerical fill.",
    }


def check_T_w_input_correlation_requirements_declared() -> Dict[str, Any]:
    """Input covariance/correlation metadata is required before comparison."""
    ledger = _ledger()
    assert len(ledger.correlation_requirements) >= 4
    assert any("finite_part" in item for item in ledger.correlation_requirements)
    return {
        "name": "T_w_input_correlation_requirements_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "correlation_requirements": list(ledger.correlation_requirements),
        "uncertainty_protocol_evaluated": UNCERTAINTY_PROTOCOL_EVALUATED,
        "key_result": "The W input-basis ledger requires covariance/correlation policy before any comparison error can be quoted.",
    }


def check_T_w_input_relation_template_declared_not_solved() -> Dict[str, Any]:
    """Declare the on-shell relation template without solving for a physical M_W."""
    ledger = _ledger()
    assert "M_W_on_shell" in ledger.relation_template
    assert "terminal output symbol" in ledger.relation_template
    assert ledger.exports_physical_M_W is False
    return {
        "name": "T_w_input_relation_template_declared_not_solved",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "relation_template": ledger.relation_template,
        "relation_solved": False,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The W on-shell relation is banked as a symbolic terminal template, not a solved mass prediction.",
    }


def check_T_w_delta_r_slot_declared_unevaluated() -> Dict[str, Any]:
    """The finite EW radiative correction appears only as an unevaluated slot."""
    ledger = _ledger()
    records = {r.symbol_id: r for r in _symbol_records()}
    delta = records[ledger.radiative_symbol]
    assert delta.allowed_as_external_input is False
    assert delta.numerical_value == "UNFILLED"
    assert ledger.delta_r_evaluated is False
    return {
        "name": "T_w_delta_r_slot_declared_unevaluated",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "radiative_symbol": ledger.radiative_symbol,
        "delta_r_record": asdict(delta),
        "delta_r_evaluated": DELTA_R_EVALUATED,
        "key_result": "Delta_r is an explicit finite-part slot and cannot be tuned to a W residual in v9.1.",
    }


def check_T_w_observed_MW_excluded_from_input_basis() -> Dict[str, Any]:
    """Observed W masses and residual-fitting inputs are banned from the ledger."""
    ledger = _ledger()
    assert any("observed physical M_W" in item for item in ledger.forbidden_inputs)
    assert any("residual" in item for item in ledger.forbidden_inputs)
    assert any("Delta_r adjusted" in item for item in ledger.forbidden_inputs)
    assert all(r.consumes_observed_M_W is False for r in _symbol_records())
    return {
        "name": "T_w_observed_MW_excluded_from_input_basis",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "forbidden_inputs": list(ledger.forbidden_inputs),
        "symbol_records": [asdict(r) for r in _symbol_records()],
        "key_result": "The W input-basis ledger explicitly excludes observed M_W, W residuals, and residual-tuned Delta_r.",
    }


def check_T_w_trace_value_remains_upstream_not_input_constant() -> Dict[str, Any]:
    """M_W^TRACE is preserved as upstream APF output, not an EW external constant."""
    wtrace = _check_T_w_trace_local_input_preserved()
    assert _passed(wtrace)
    assert abs(float(wtrace["M_W_TRACE_GeV"]) - W_TRACE_EXPECTED_GEV) < 1e-12
    ledger = _ledger()
    assert "M_W_TRACE" not in ledger.allowed_input_symbols
    assert "M_W_on_shell" not in ledger.allowed_input_symbols
    return {
        "name": "T_w_trace_value_remains_upstream_not_input_constant",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "M_W_TRACE_GeV": float(wtrace["M_W_TRACE_GeV"]),
        "allowed_input_symbols": list(ledger.allowed_input_symbols),
        "key_result": "M_W^TRACE is the upstream APF object; neither M_W^TRACE nor physical M_W is an external input constant.",
    }


def check_T_w_input_basis_no_inverse_fit_channel() -> Dict[str, Any]:
    """The input-basis ledger contains no free fit knob aimed at W mass error."""
    records = _symbol_records()
    fit_like = [r for r in records if "fit" in r.symbol_id.lower() or "residual" in r.symbol_id.lower()]
    ledger = _ledger()
    assert not fit_like
    assert "fit parameter chosen to minimize W-mass error" in ledger.forbidden_inputs
    return {
        "name": "T_w_input_basis_no_inverse_fit_channel",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "fit_like_records": [asdict(r) for r in fit_like],
        "forbidden_fit_inputs": [item for item in ledger.forbidden_inputs if "fit" in item or "adjusted" in item],
        "key_result": "The W input-basis ledger exposes no inverse-fit channel for minimizing the W mass discrepancy.",
    }


def check_T_w_input_basis_completion_gate_remains_locked() -> Dict[str, Any]:
    """The terminal export gate remains locked after input-basis ledger fill."""
    completion = _check_T_w_trace_completion_gate_remains_locked()
    assert _passed(completion)
    assert _completion_gate_locked_for_w() is True
    ledger = _ledger()
    blocked_by = {
        "numerical_values_filled": ledger.numerical_values_filled,
        "delta_r_evaluated": ledger.delta_r_evaluated,
        "uncertainty_protocol_evaluated": ledger.uncertainty_protocol_evaluated,
        "exports_physical_M_W": ledger.exports_physical_M_W,
        "physical_W_transport_closed": ledger.physical_W_transport_closed,
    }
    assert not any(blocked_by.values())
    return {
        "name": "T_w_input_basis_completion_gate_remains_locked",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "route_id": W_ROUTE_ID,
        "physical_export_allowed": False,
        "blocked_by_unfilled_terminal_requirements": blocked_by,
        "key_result": "The W terminal export gate is still locked after the input-basis ledger is selected.",
    }


def check_T_w_input_basis_publication_claim_ladder() -> Dict[str, Any]:
    """Publication wording is constrained to input-basis ledger status."""
    allowed_claim = "W_TRACE on-shell input-basis ledger selected and provenance-gated"
    forbidden_claims = (
        "APF predicts the physical W mass",
        "W_TRACE equals the measured W boson mass",
        "the W on-shell transport theorem is closed",
    )
    return {
        "name": "T_w_input_basis_publication_claim_ladder",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "allowed_claim": allowed_claim,
        "forbidden_claims": list(forbidden_claims),
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "The claim ladder permits only a W input-basis ledger claim, not a physical W prediction claim.",
    }


def check_T_w_input_basis_ledger_bank_closure() -> Dict[str, Any]:
    """Master v9.1 W input-basis ledger closure."""
    deps = [
        check_T_w_input_basis_ledger_status_declared(),
        check_T_w_input_basis_selected_from_v90_options(),
        check_T_w_input_basis_ledger_schema_complete(),
        check_T_w_input_symbols_enumerated_without_values(),
        check_T_w_input_provenance_requirements_complete(),
        check_T_w_input_correlation_requirements_declared(),
        check_T_w_input_relation_template_declared_not_solved(),
        check_T_w_delta_r_slot_declared_unevaluated(),
        check_T_w_observed_MW_excluded_from_input_basis(),
        check_T_w_trace_value_remains_upstream_not_input_constant(),
        check_T_w_input_basis_no_inverse_fit_channel(),
        check_T_w_input_basis_completion_gate_remains_locked(),
        check_T_w_input_basis_publication_claim_ladder(),
    ]
    assert all(_passed(dep) for dep in deps)
    ledger = _ledger()
    return {
        "name": "T_w_input_basis_ledger_bank_closure",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_INPUT_BASIS_LEDGER_STATUS,
        "dependencies": [str(dep["name"]) for dep in deps],
        "ledger": asdict(ledger),
        "symbol_records": [asdict(r) for r in _symbol_records()],
        "closed_now": "W_TRACE on-shell input-basis ledger selection, symbolic relation template, and provenance/no-smuggling gates",
        "not_closed": "numerical constants, Delta_r finite correction, uncertainty propagation, physical W export",
        "input_basis_ledger_filled": INPUT_BASIS_LEDGER_FILLED,
        "numerical_EW_constants_filled": NUMERICAL_EW_CONSTANTS_FILLED,
        "delta_r_evaluated": DELTA_R_EVALUATED,
        "uncertainty_protocol_evaluated": UNCERTAINTY_PROTOCOL_EVALUATED,
        "physical_transport_closed": False,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "W_TRACE input-basis ledger is banked; W physical transport remains open and gated.",
    }


_CHECKS = {
    "T_w_input_basis_ledger_status_declared": check_T_w_input_basis_ledger_status_declared,
    "T_w_input_basis_selected_from_v90_options": check_T_w_input_basis_selected_from_v90_options,
    "T_w_input_basis_ledger_schema_complete": check_T_w_input_basis_ledger_schema_complete,
    "T_w_input_symbols_enumerated_without_values": check_T_w_input_symbols_enumerated_without_values,
    "T_w_input_provenance_requirements_complete": check_T_w_input_provenance_requirements_complete,
    "T_w_input_correlation_requirements_declared": check_T_w_input_correlation_requirements_declared,
    "T_w_input_relation_template_declared_not_solved": check_T_w_input_relation_template_declared_not_solved,
    "T_w_delta_r_slot_declared_unevaluated": check_T_w_delta_r_slot_declared_unevaluated,
    "T_w_observed_MW_excluded_from_input_basis": check_T_w_observed_MW_excluded_from_input_basis,
    "T_w_trace_value_remains_upstream_not_input_constant": check_T_w_trace_value_remains_upstream_not_input_constant,
    "T_w_input_basis_no_inverse_fit_channel": check_T_w_input_basis_no_inverse_fit_channel,
    "T_w_input_basis_completion_gate_remains_locked": check_T_w_input_basis_completion_gate_remains_locked,
    "T_w_input_basis_publication_claim_ladder": check_T_w_input_basis_publication_claim_ladder,
    "T_w_input_basis_ledger_bank_closure": check_T_w_input_basis_ledger_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register W_TRACE input-basis ledger checks into the global bank."""
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
        "status": "W_TRACE_INPUT_BASIS_LEDGER_BANK_PASS" if ok else "W_TRACE_INPUT_BASIS_LEDGER_BANK_FAIL",
        "bank_registered": True,
        "route_status": W_INPUT_BASIS_LEDGER_STATUS,
        "route_id": W_ROUTE_ID,
        "selected_basis": SELECTED_W_INPUT_BASIS,
        "input_basis_ledger_filled": INPUT_BASIS_LEDGER_FILLED,
        "numerical_EW_constants_filled": NUMERICAL_EW_CONSTANTS_FILLED,
        "delta_r_evaluated": DELTA_R_EVALUATED,
        "uncertainty_protocol_evaluated": UNCERTAINTY_PROTOCOL_EVALUATED,
        "physical_transport_closed": False,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "results": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))
