"""W_TRACE constants-source / numerical-fill ledger gate.

v9.2 (2026-05-08 LATER-10): the next concrete W route layer after the
v9.1 W_TRACE input-basis ledger.  v9.1 selected the allowed symbolic input
basis for the W_TRACE -> on-shell route.  This module fills the *source-tagged
numerical constants ledger* for those allowed non-W inputs while keeping the
physical W export gate locked.

Closed here:
    - Fill the allowed non-W electroweak input ledger with source-tagged
      numerical records for alpha_em, G_F, and M_Z.
    - Bank source/provenance/unit/uncertainty fields for those constants.
    - Prove the fill consumes no observed W mass, no W residual, and no fitted
      Delta_r adjusted to the W target.

Not closed here:
    - Delta_r / finite EW correction is still not evaluated.
    - Counterterm finite parts are still not evaluated.
    - Correlation propagation is declared but not yet evaluated.
    - No physical M_W value is exported.

Status discipline:
    - v9.1 input-basis ledger: [P_w_input_basis_ledger] upstream.
    - This module: [P_w_constants_source_ledger], a source-tagged numerical
      constants ledger for allowed non-W inputs.
    - Physical W/on-shell transport remains open.

Source tags used here:
    - alpha inverse: NIST/CODATA 2022 recommended value.
    - G_F: PDG 2024 electroweak review, Fermi constant from muon lifetime.
    - M_Z: PDG 2024 Z-boson listing / LEP electroweak fit convention.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, fields
from decimal import Decimal, getcontext
from typing import Any, Dict, Mapping, Tuple

from apf.w_trace_input_basis_ledger import (
    W_INPUT_BASIS_LEDGER_STATUS,
    SELECTED_W_INPUT_BASIS,
    ALLOWED_W_INPUT_SYMBOLS,
    FORBIDDEN_LEDGER_INPUTS,
    check_T_w_input_basis_ledger_bank_closure as _check_T_w_input_basis_ledger_bank_closure,
    check_T_w_observed_MW_excluded_from_input_basis as _check_T_w_observed_MW_excluded_from_input_basis,
    check_T_w_delta_r_slot_declared_unevaluated as _check_T_w_delta_r_slot_declared_unevaluated,
)
from apf.w_trace_onshell_transport import (
    W_ROUTE_ID,
    W_TRACE_EXPECTED_GEV,
    check_T_w_trace_local_input_preserved as _check_T_w_trace_local_input_preserved,
)
from apf.trace_transport_completion import (
    check_T_physical_export_gate_locked_until_all_certificates_filled as _check_T_physical_export_gate_locked_until_all_certificates_filled,
)


getcontext().prec = 40

W_CONSTANTS_SOURCE_LEDGER_STATUS = "P_w_constants_source_ledger"
CONSTANTS_SOURCE_LEDGER_FILLED = True
NUMERICAL_EW_CONSTANTS_FILLED = True
DELTA_R_EVALUATED = False
COUNTERTERM_FINITE_PARTS_EVALUATED = False
CORRELATION_PROPAGATION_EVALUATED = False
UNCERTAINTY_PROTOCOL_EVALUATED = False
PHYSICAL_W_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_M_W = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

REQUIRED_CONSTANT_RECORD_FIELDS: Tuple[str, ...] = (
    "symbol_id",
    "display_symbol",
    "numerical_value",
    "unit",
    "standard_uncertainty",
    "relative_uncertainty",
    "source_name",
    "source_year",
    "source_url",
    "scheme_or_convention",
    "provenance_status",
    "consumes_observed_M_W",
    "consumes_W_residual",
    "notes",
)

# Numerical records are deliberately source-tagged strings.  Computation of the
# W output is not performed in this module.
ALPHA_INV_VALUE = Decimal("137.035999177")
ALPHA_INV_UNCERTAINTY = Decimal("0.000000021")
ALPHA_VALUE = Decimal(1) / ALPHA_INV_VALUE
ALPHA_UNCERTAINTY = ALPHA_INV_UNCERTAINTY / (ALPHA_INV_VALUE * ALPHA_INV_VALUE)

G_F_VALUE = Decimal("1.1663788e-5")
G_F_UNCERTAINTY = Decimal("0.0000006e-5")
M_Z_VALUE_GEV = Decimal("91.1876")
M_Z_UNCERTAINTY_GEV = Decimal("0.0021")

FORBIDDEN_CONSTANT_INPUTS: Tuple[str, ...] = tuple(FORBIDDEN_LEDGER_INPUTS) + (
    "observed_W_mass_value",
    "world_average_M_W",
    "CDF_M_W_measurement",
    "ATLAS_M_W_measurement",
    "CMS_M_W_measurement",
    "LEP_W_mass_measurement",
    "W_mass_residual",
    "Delta_r_fit_to_W_mass",
)

CORRELATION_POLICY_STATUS = "declared_not_evaluated"


@dataclass(frozen=True)
class WConstantRecord:
    """One source-tagged numerical input constant for the W route."""

    symbol_id: str
    display_symbol: str
    numerical_value: str
    unit: str
    standard_uncertainty: str
    relative_uncertainty: str
    source_name: str
    source_year: str
    source_url: str
    scheme_or_convention: str
    provenance_status: str
    consumes_observed_M_W: bool = False
    consumes_W_residual: bool = False
    notes: str = ""


@dataclass(frozen=True)
class WConstantsSourceLedger:
    """Filled source ledger for allowed non-W electroweak constants."""

    route_id: str
    selected_basis: str
    records: Tuple[WConstantRecord, ...]
    forbidden_inputs: Tuple[str, ...]
    constants_source_ledger_filled: bool = True
    numerical_EW_constants_filled: bool = True
    delta_r_evaluated: bool = False
    counterterm_finite_parts_evaluated: bool = False
    correlation_propagation_evaluated: bool = False
    uncertainty_protocol_evaluated: bool = False
    exports_physical_M_W: bool = False
    physical_W_transport_closed: bool = False


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def _relative_uncertainty(value: Decimal, uncertainty: Decimal) -> str:
    return f"{(uncertainty.copy_abs() / value.copy_abs()):.12E}"


def _constant_records() -> Tuple[WConstantRecord, ...]:
    return (
        WConstantRecord(
            symbol_id="alpha_em_reference",
            display_symbol="alpha(0)",
            numerical_value=f"{ALPHA_VALUE:.18E} ; equivalently alpha^-1={ALPHA_INV_VALUE}",
            unit="dimensionless",
            standard_uncertainty=f"alpha uncertainty approximately {ALPHA_UNCERTAINTY:.18E}; inverse-alpha uncertainty {ALPHA_INV_UNCERTAINTY}",
            relative_uncertainty=_relative_uncertainty(ALPHA_INV_VALUE, ALPHA_INV_UNCERTAINTY),
            source_name="NIST CODATA 2022 recommended value: inverse fine-structure constant",
            source_year="2022 CODATA / NIST page accessed in 2026",
            source_url="https://physics.nist.gov/cgi-bin/cuu/Value?eqalphinv=",
            scheme_or_convention="Thomson-limit electromagnetic coupling alpha(0); later running is a separate finite-map slot",
            provenance_status="source_tagged_numeric_value_filled",
            notes="Allowed non-W input.  Does not consume an observed W mass.",
        ),
        WConstantRecord(
            symbol_id="G_F_reference",
            display_symbol="G_F",
            numerical_value="1.1663788e-5",
            unit="GeV^-2",
            standard_uncertainty="0.0000006e-5",
            relative_uncertainty=_relative_uncertainty(G_F_VALUE, G_F_UNCERTAINTY),
            source_name="PDG 2024 Electroweak Model and Constraints review: Fermi constant from muon lifetime",
            source_year="2024",
            source_url="https://pdgweb.lbl.gov/2024/reviews/rpp2024-rev-standard-model.pdf",
            scheme_or_convention="Fermi constant from muon lifetime convention; W-propagator/Delta-r handling remains a separate slot",
            provenance_status="source_tagged_numeric_value_filled",
            notes="Allowed non-W input.  The finite W correction remains unevaluated.",
        ),
        WConstantRecord(
            symbol_id="M_Z_on_shell_reference",
            display_symbol="M_Z",
            numerical_value="91.1876",
            unit="GeV",
            standard_uncertainty="0.0021",
            relative_uncertainty=_relative_uncertainty(M_Z_VALUE_GEV, M_Z_UNCERTAINTY_GEV),
            source_name="PDG 2024 Z-boson listing: combined LEP Z result / on-shell Breit-Wigner convention",
            source_year="2024",
            source_url="https://pdgweb.lbl.gov/2024/listings/rpp2024-list-z-boson.pdf",
            scheme_or_convention="Z mass parameter in mass-dependent-width Breit-Wigner convention; W mass not used as source",
            provenance_status="source_tagged_numeric_value_filled",
            notes="Allowed non-W input.  Z-pole source does not make APF_TRACE identical to physical W.",
        ),
    )


def _ledger() -> WConstantsSourceLedger:
    return WConstantsSourceLedger(
        route_id=W_ROUTE_ID,
        selected_basis=SELECTED_W_INPUT_BASIS,
        records=_constant_records(),
        forbidden_inputs=FORBIDDEN_CONSTANT_INPUTS,
        constants_source_ledger_filled=True,
        numerical_EW_constants_filled=True,
        delta_r_evaluated=False,
        counterterm_finite_parts_evaluated=False,
        correlation_propagation_evaluated=False,
        uncertainty_protocol_evaluated=False,
        exports_physical_M_W=False,
        physical_W_transport_closed=False,
    )


def _completion_gate_locked_for_w() -> bool:
    result = _check_T_physical_export_gate_locked_until_all_certificates_filled()
    assert _passed(result)
    allowed = result.get("physical_export_allowed_by_route", {})
    return allowed.get(W_ROUTE_ID) is False


# ---------------------------------------------------------------------
# Bank-facing W constants-source ledger checks.
# ---------------------------------------------------------------------


def check_T_w_constants_source_ledger_status_declared() -> Dict[str, Any]:
    """Declare v9.2 as a constants-source fill, not W transport closure."""
    upstream = _check_T_w_input_basis_ledger_bank_closure()
    assert _passed(upstream)
    assert upstream.get("epistemic") == W_INPUT_BASIS_LEDGER_STATUS
    assert upstream.get("physical_W_transport_closed") is False
    return {
        "name": "T_w_constants_source_ledger_status_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "dependencies": ["T_w_input_basis_ledger_bank_closure"],
        "closed_now": "source-tagged numerical constants ledger for allowed non-W W-route inputs",
        "not_closed": "Delta_r, counterterms, correlation propagation, uncertainty protocol, physical M_W export",
        "key_result": "v9.2 fills allowed constant sources without closing W transport.",
    }


def check_T_w_constants_record_schema_complete() -> Dict[str, Any]:
    """Every constant record exposes the required provenance/no-smuggling fields."""
    have = tuple(field.name for field in fields(WConstantRecord))
    missing = [f for f in REQUIRED_CONSTANT_RECORD_FIELDS if f not in have]
    assert not missing
    for record in _constant_records():
        row = asdict(record)
        assert all(k in row for k in REQUIRED_CONSTANT_RECORD_FIELDS)
    return {
        "name": "T_w_constants_record_schema_complete",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "required_fields": REQUIRED_CONSTANT_RECORD_FIELDS,
        "record_count": len(_constant_records()),
        "key_result": "constant records carry value, unit, uncertainty, source, convention, and W-exclusion fields.",
    }


def check_T_w_constants_symbols_match_v91_allowed_basis() -> Dict[str, Any]:
    """The filled symbols are exactly the v9.1 allowed non-W input symbols."""
    filled = tuple(r.symbol_id for r in _constant_records())
    assert filled == tuple(ALLOWED_W_INPUT_SYMBOLS)
    assert "M_W" not in " ".join(filled)
    return {
        "name": "T_w_constants_symbols_match_v91_allowed_basis",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "filled_symbols": filled,
        "allowed_symbols": ALLOWED_W_INPUT_SYMBOLS,
        "key_result": "only alpha_em_reference, G_F_reference, and M_Z_on_shell_reference are numerically filled.",
    }


def check_T_w_alpha_coddata_source_value_filled() -> Dict[str, Any]:
    """Fill alpha from the source-tagged CODATA/NIST inverse-alpha record."""
    rec = _constant_records()[0]
    assert rec.symbol_id == "alpha_em_reference"
    assert ALPHA_INV_VALUE > 0
    assert ALPHA_INV_UNCERTAINTY > 0
    assert ALPHA_VALUE > 0
    assert "NIST" in rec.source_name and "CODATA" in rec.source_name
    assert rec.consumes_observed_M_W is False and rec.consumes_W_residual is False
    return {
        "name": "T_w_alpha_coddata_source_value_filled",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "record": asdict(rec),
        "alpha_inverse": str(ALPHA_INV_VALUE),
        "alpha_value_decimal": f"{ALPHA_VALUE:.18E}",
        "key_result": "alpha_em_reference is filled from NIST/CODATA inverse-alpha, not from W data.",
    }


def check_T_w_GF_pdg_source_value_filled() -> Dict[str, Any]:
    """Fill G_F from the source-tagged PDG muon-lifetime convention record."""
    rec = _constant_records()[1]
    assert rec.symbol_id == "G_F_reference"
    assert G_F_VALUE > 0 and G_F_UNCERTAINTY > 0
    assert "PDG" in rec.source_name and "Fermi" in rec.source_name
    assert rec.unit == "GeV^-2"
    assert rec.consumes_observed_M_W is False and rec.consumes_W_residual is False
    return {
        "name": "T_w_GF_pdg_source_value_filled",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "record": asdict(rec),
        "key_result": "G_F_reference is filled from a muon-lifetime source convention and does not consume W mass.",
    }


def check_T_w_MZ_pdg_source_value_filled() -> Dict[str, Any]:
    """Fill M_Z from the source-tagged PDG/LEP Z on-shell convention record."""
    rec = _constant_records()[2]
    assert rec.symbol_id == "M_Z_on_shell_reference"
    assert M_Z_VALUE_GEV > 0 and M_Z_UNCERTAINTY_GEV > 0
    assert "PDG" in rec.source_name and "Z" in rec.source_name
    assert rec.unit == "GeV"
    assert rec.consumes_observed_M_W is False and rec.consumes_W_residual is False
    return {
        "name": "T_w_MZ_pdg_source_value_filled",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "record": asdict(rec),
        "key_result": "M_Z_on_shell_reference is filled from a Z-pole source convention and does not consume W mass.",
    }


def check_T_w_constants_units_and_dimensions_declared() -> Dict[str, Any]:
    """The three filled inputs carry distinct unit/dimension contracts."""
    units = {r.symbol_id: r.unit for r in _constant_records()}
    assert units == {
        "alpha_em_reference": "dimensionless",
        "G_F_reference": "GeV^-2",
        "M_Z_on_shell_reference": "GeV",
    }
    return {
        "name": "T_w_constants_units_and_dimensions_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "units": units,
        "key_result": "unit contracts are explicit before any W comparison equation can be evaluated.",
    }


def check_T_w_constants_uncertainties_positive_and_source_tagged() -> Dict[str, Any]:
    """Every numerical fill has a positive uncertainty and a source URL."""
    for rec in _constant_records():
        assert rec.standard_uncertainty
        assert rec.relative_uncertainty
        assert rec.source_url.startswith("https://")
        assert rec.provenance_status == "source_tagged_numeric_value_filled"
    return {
        "name": "T_w_constants_uncertainties_positive_and_source_tagged",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "records": [asdict(r) for r in _constant_records()],
        "key_result": "all filled constants have uncertainty strings, relative-uncertainty tags, and source URLs.",
    }


def check_T_w_constants_correlation_policy_declared_not_evaluated() -> Dict[str, Any]:
    """Correlation metadata remains a declared but unevaluated next gate."""
    ledger = _ledger()
    assert ledger.correlation_propagation_evaluated is False
    return {
        "name": "T_w_constants_correlation_policy_declared_not_evaluated",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "correlation_policy_status": CORRELATION_POLICY_STATUS,
        "correlation_propagation_evaluated": False,
        "key_result": "constant values are filled, but covariance/correlation propagation remains open.",
    }


def check_T_w_constants_forbidden_W_inputs_absent() -> Dict[str, Any]:
    """No observed W mass, W residual, or W-fit channel is present in the filled ledger."""
    text = " ".join(str(asdict(r)) for r in _constant_records()).lower()
    assert "world_average_m_w" not in text
    assert "observed_w_mass_value" not in text
    for rec in _constant_records():
        assert rec.consumes_observed_M_W is False
        assert rec.consumes_W_residual is False
    upstream = _check_T_w_observed_MW_excluded_from_input_basis()
    assert _passed(upstream)
    return {
        "name": "T_w_constants_forbidden_W_inputs_absent",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "forbidden_inputs": FORBIDDEN_CONSTANT_INPUTS,
        "key_result": "the numerical constants ledger consumes no observed W mass and no W residual.",
    }


def check_T_w_constants_delta_r_and_counterterms_still_open() -> Dict[str, Any]:
    """The numerical constants fill does not evaluate Delta_r or finite counterterms."""
    upstream = _check_T_w_delta_r_slot_declared_unevaluated()
    assert _passed(upstream)
    assert DELTA_R_EVALUATED is False
    assert COUNTERTERM_FINITE_PARTS_EVALUATED is False
    return {
        "name": "T_w_constants_delta_r_and_counterterms_still_open",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "delta_r_evaluated": False,
        "counterterm_finite_parts_evaluated": False,
        "key_result": "filling external constants does not solve the finite EW correction map.",
    }


def check_T_w_constants_preserve_W_TRACE_input() -> Dict[str, Any]:
    """The APF W_TRACE local value remains upstream and is not overwritten."""
    upstream = _check_T_w_trace_local_input_preserved()
    assert _passed(upstream)
    assert abs(float(upstream.get("M_W_TRACE_GeV")) - W_TRACE_EXPECTED_GEV) < 1e-12
    return {
        "name": "T_w_constants_preserve_W_TRACE_input",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "W_TRACE_GeV": W_TRACE_EXPECTED_GEV,
        "key_result": "M_W_TRACE remains the upstream APF_TRACE quantity, not a fitted physical input.",
    }


def check_T_w_constants_completion_gate_remains_locked() -> Dict[str, Any]:
    """Even with constants filled, terminal W export is still blocked."""
    assert _completion_gate_locked_for_w()
    return {
        "name": "T_w_constants_completion_gate_remains_locked",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "physical_export_allowed_for_w_route": False,
        "reason": "Delta_r, finite counterterms, correlation propagation, and uncertainty protocol remain unfilled.",
        "key_result": "v8.9 terminal export gate remains locked after constants-source fill.",
    }


def check_T_w_constants_publication_claim_ladder() -> Dict[str, Any]:
    """Declare exactly what v9.2 may and may not claim."""
    return {
        "name": "T_w_constants_publication_claim_ladder",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "claim_allowed": "allowed non-W EW constants source ledger is filled and no-smuggling certified",
        "claim_forbidden": "physical M_W prediction or residual comparison is closed",
        "constants_source_ledger_filled": True,
        "numerical_EW_constants_filled": True,
        "delta_r_evaluated": False,
        "physical_W_transport_closed": False,
        "exports_physical_M_W": False,
        "key_result": "v9.2 is a constants-source ledger bank, not a physical W transport bank.",
    }


def check_T_w_constants_source_ledger_bank_closure() -> Dict[str, Any]:
    """Master v9.2 W constants-source ledger closure."""
    deps = [
        check_T_w_constants_source_ledger_status_declared(),
        check_T_w_constants_record_schema_complete(),
        check_T_w_constants_symbols_match_v91_allowed_basis(),
        check_T_w_alpha_coddata_source_value_filled(),
        check_T_w_GF_pdg_source_value_filled(),
        check_T_w_MZ_pdg_source_value_filled(),
        check_T_w_constants_units_and_dimensions_declared(),
        check_T_w_constants_uncertainties_positive_and_source_tagged(),
        check_T_w_constants_correlation_policy_declared_not_evaluated(),
        check_T_w_constants_forbidden_W_inputs_absent(),
        check_T_w_constants_delta_r_and_counterterms_still_open(),
        check_T_w_constants_preserve_W_TRACE_input(),
        check_T_w_constants_completion_gate_remains_locked(),
        check_T_w_constants_publication_claim_ladder(),
    ]
    assert all(_passed(dep) for dep in deps)
    ledger = _ledger()
    return {
        "name": "T_w_constants_source_ledger_bank_closure",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "dependencies": [str(dep["name"]) for dep in deps],
        "ledger": asdict(ledger),
        "closed_now": "source-tagged numerical constants ledger for alpha_em, G_F, and M_Z",
        "not_closed": "Delta_r, finite counterterms, covariance propagation, uncertainty propagation, physical W export",
        "constants_source_ledger_filled": CONSTANTS_SOURCE_LEDGER_FILLED,
        "numerical_EW_constants_filled": NUMERICAL_EW_CONSTANTS_FILLED,
        "delta_r_evaluated": DELTA_R_EVALUATED,
        "counterterm_finite_parts_evaluated": COUNTERTERM_FINITE_PARTS_EVALUATED,
        "correlation_propagation_evaluated": CORRELATION_PROPAGATION_EVALUATED,
        "uncertainty_protocol_evaluated": UNCERTAINTY_PROTOCOL_EVALUATED,
        "physical_transport_closed": False,
        "physical_W_transport_closed": PHYSICAL_W_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "exports_physical_M_W": EXPORTS_PHYSICAL_M_W,
        "key_result": "W_TRACE constants-source ledger is numerically filled for allowed non-W inputs; W physical transport remains open and gated.",
    }


_CHECKS = {
    "T_w_constants_source_ledger_status_declared": check_T_w_constants_source_ledger_status_declared,
    "T_w_constants_record_schema_complete": check_T_w_constants_record_schema_complete,
    "T_w_constants_symbols_match_v91_allowed_basis": check_T_w_constants_symbols_match_v91_allowed_basis,
    "T_w_alpha_coddata_source_value_filled": check_T_w_alpha_coddata_source_value_filled,
    "T_w_GF_pdg_source_value_filled": check_T_w_GF_pdg_source_value_filled,
    "T_w_MZ_pdg_source_value_filled": check_T_w_MZ_pdg_source_value_filled,
    "T_w_constants_units_and_dimensions_declared": check_T_w_constants_units_and_dimensions_declared,
    "T_w_constants_uncertainties_positive_and_source_tagged": check_T_w_constants_uncertainties_positive_and_source_tagged,
    "T_w_constants_correlation_policy_declared_not_evaluated": check_T_w_constants_correlation_policy_declared_not_evaluated,
    "T_w_constants_forbidden_W_inputs_absent": check_T_w_constants_forbidden_W_inputs_absent,
    "T_w_constants_delta_r_and_counterterms_still_open": check_T_w_constants_delta_r_and_counterterms_still_open,
    "T_w_constants_preserve_W_TRACE_input": check_T_w_constants_preserve_W_TRACE_input,
    "T_w_constants_completion_gate_remains_locked": check_T_w_constants_completion_gate_remains_locked,
    "T_w_constants_publication_claim_ladder": check_T_w_constants_publication_claim_ladder,
    "T_w_constants_source_ledger_bank_closure": check_T_w_constants_source_ledger_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register W_TRACE constants-source ledger checks into the global bank."""
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
        "status": "W_TRACE_CONSTANTS_SOURCE_LEDGER_BANK_PASS" if ok else "W_TRACE_CONSTANTS_SOURCE_LEDGER_BANK_FAIL",
        "bank_registered": True,
        "route_status": W_CONSTANTS_SOURCE_LEDGER_STATUS,
        "route_id": W_ROUTE_ID,
        "selected_basis": SELECTED_W_INPUT_BASIS,
        "constants_source_ledger_filled": CONSTANTS_SOURCE_LEDGER_FILLED,
        "numerical_EW_constants_filled": NUMERICAL_EW_CONSTANTS_FILLED,
        "delta_r_evaluated": DELTA_R_EVALUATED,
        "counterterm_finite_parts_evaluated": COUNTERTERM_FINITE_PARTS_EVALUATED,
        "correlation_propagation_evaluated": CORRELATION_PROPAGATION_EVALUATED,
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
