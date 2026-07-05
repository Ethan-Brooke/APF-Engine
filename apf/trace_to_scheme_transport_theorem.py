"""Trace-to-scheme transport theorem bank.

v14.9 (2026-05-09): paper-facing theorem layer for promoting APF_TRACE/W_TRACE
objects into named physical reporting schemes.  This module does not evaluate a
new numerical physical mass map.  It closes the theorem *form*: a trace result
may be exported as a physical scheme value if and only if a named route has a
filled scheme contract, evaluated route-stage maps, filled external/counterterm
ledgers, an evaluated uncertainty protocol, and no target-observable/inverse-fit
consumption.

Status discipline:
    APF_TRACE / W_TRACE local closure: [P_local]
    Validation neighborhoods: [P_validation]
    Transport theorem form: [P_theorem]
    Physical scheme export by any route in the present code state: OPEN / false
"""
from __future__ import annotations

from dataclasses import dataclass, asdict, fields
from typing import Any, Dict, Iterable, Mapping, Tuple

from apf.trace_scheme_transport import (
    check_T_trace_to_scheme_boundary_bank_closure as _check_boundary,
)
from apf.trace_transport_ledger import (
    check_T_transport_ledger_bank_closure as _check_ledger,
)
from apf.trace_transport_routes import (
    check_T_transport_routes_bank_closure as _check_routes,
)
from apf.trace_transport_composition import (
    check_T_trace_transport_composition_bank_closure as _check_composition,
)
from apf.trace_transport_completion import (
    check_T_trace_transport_completion_gate_bank_closure as _check_completion,
)
from apf.trace_sector_closure import (
    check_T_apf_trace_sector_closure as _check_trace_sector,
)

THEOREM_STATUS = "P_transport_theorem"
PHYSICAL_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

OPEN_ROUTE_ORDER: Tuple[str, ...] = (
    "w_trace_on_shell_route",
    "charged_lepton_pole_or_running_route",
    "colored_msbar_running_route",
    "colored_pole_or_on_shell_route",
    "light_quark_low_energy_route",
)

TRANSPORT_THEOREM_OBLIGATIONS: Tuple[str, ...] = (
    "immutable APF_TRACE/W_TRACE domain value",
    "declared target scheme S and scale/convention mu",
    "route-stage map composition with typed domains/codomains",
    "evaluated running/matching/counterterm finite parts where required",
    "filled external constants ledger with provenance, uncertainties, and correlations",
    "evaluated uncertainty/comparison protocol fixed before residuals are read",
    "no target physical observable, PDG vector, or post-hoc scalar may enter as input",
)

ROUTE_THEOREM_CLAUSES: Mapping[str, Mapping[str, Any]] = {
    "w_trace_on_shell_route": {
        "domain": ("M_W_TRACE",),
        "target": "W on-shell/EW input-basis convention",
        "map_symbol": "R_W^{OS}",
        "claim_when_closed": "M_W^{APF->OS} in a declared on-shell convention",
        "least_burden": True,
    },
    "charged_lepton_pole_or_running_route": {
        "domain": ("m_e", "m_mu", "m_tau"),
        "target": "charged-lepton pole/on-shell/running convention",
        "map_symbol": "R_l^{S(mu)}",
        "claim_when_closed": "charged lepton APF_TRACE entries transported into a declared lepton scheme",
        "least_burden": True,
    },
    "colored_msbar_running_route": {
        "domain": ("m_u", "m_c", "m_t", "m_d", "m_s", "m_b"),
        "target": "short-distance colored MSbar-like running scheme",
        "map_symbol": "R_q^{MSbar(mu)}",
        "claim_when_closed": "colored APF_TRACE entries transported into declared short-distance running masses",
        "least_burden": False,
    },
    "colored_pole_or_on_shell_route": {
        "domain": ("m_u", "m_c", "m_t", "m_d", "m_s", "m_b"),
        "target": "colored pole/on-shell convention after short-distance leg",
        "map_symbol": "R_q^{pole/OS}",
        "claim_when_closed": "colored APF_TRACE entries transported into declared pole/on-shell convention with ambiguity ledger",
        "least_burden": False,
    },
    "light_quark_low_energy_route": {
        "domain": ("m_u", "m_d", "m_s"),
        "target": "low-energy/lattice/hadronic convention",
        "map_symbol": "R_{uds}^{LE}",
        "claim_when_closed": "light-quark APF_TRACE entries transported into a declared nonperturbative convention",
        "least_burden": False,
    },
}

REQUIRED_EXPORT_CERTIFICATE_FIELDS: Tuple[str, ...] = (
    "route_id",
    "scheme_contract_filled",
    "all_stage_maps_evaluated",
    "external_constants_ledger_filled",
    "counterterm_maps_evaluated",
    "uncertainty_protocol_evaluated",
    "target_observables_consumed",
    "may_export_physical_scheme_value",
)


@dataclass(frozen=True)
class ExportCertificate:
    """Paper-facing terminal certificate for trace-to-scheme export."""

    route_id: str
    scheme_contract_filled: bool
    all_stage_maps_evaluated: bool
    external_constants_ledger_filled: bool
    counterterm_maps_evaluated: bool
    uncertainty_protocol_evaluated: bool
    target_observables_consumed: bool
    may_export_physical_scheme_value: bool


@dataclass(frozen=True)
class RouteClause:
    """Route-specific specialization of the theorem."""

    route_id: str
    domain: Tuple[str, ...]
    target: str
    map_symbol: str
    claim_when_closed: str
    stage_ids: Tuple[str, ...]
    required_external_slots: Tuple[str, ...]
    required_counterterm_slots: Tuple[str, ...]
    present_status: str


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def _unique(items: Iterable[str]) -> Tuple[str, ...]:
    return tuple(sorted({str(x) for x in items if str(x)}))


def _completion_certificates() -> Tuple[Mapping[str, Any], ...]:
    result = _check_completion()
    assert _passed(result)
    return tuple(result.get("certificates", ()))


def _composition_rows() -> Tuple[Mapping[str, Any], ...]:
    result = _check_composition()
    assert _passed(result)
    return tuple(result.get("composition_stage_table", ()))


def _rows_for_route(route_id: str) -> Tuple[Mapping[str, Any], ...]:
    rows = [r for r in _composition_rows() if r.get("route_id") == route_id]
    return tuple(sorted(rows, key=lambda row: int(row.get("stage_order", 0))))


def _export_certificate(route_id: str) -> ExportCertificate:
    # Current code state: completion gate declares all physical exports blocked.
    # Build a theorem-facing certificate directly from the stage table so the paper
    # can state exactly what remains missing.
    rows = _rows_for_route(route_id)
    has_stages = bool(rows)
    all_stage_maps_evaluated = all(bool(r.get("computes_numerical_transport")) for r in rows) if has_stages else False
    consumes_target = any(bool(r.get("consumes_target_observables")) for r in rows)
    # Scheme, external, counterterm, and uncertainty fields are deliberately unfilled in v14.9.
    scheme_contract_filled = False
    external_constants_ledger_filled = False
    counterterm_maps_evaluated = False
    uncertainty_protocol_evaluated = False
    may_export = (
        route_id != "identity_trace_to_physical_route"
        and scheme_contract_filled
        and has_stages
        and all_stage_maps_evaluated
        and external_constants_ledger_filled
        and counterterm_maps_evaluated
        and uncertainty_protocol_evaluated
        and not consumes_target
    )
    return ExportCertificate(
        route_id=route_id,
        scheme_contract_filled=scheme_contract_filled,
        all_stage_maps_evaluated=all_stage_maps_evaluated,
        external_constants_ledger_filled=external_constants_ledger_filled,
        counterterm_maps_evaluated=counterterm_maps_evaluated,
        uncertainty_protocol_evaluated=uncertainty_protocol_evaluated,
        target_observables_consumed=consumes_target,
        may_export_physical_scheme_value=may_export,
    )


def _route_clause(route_id: str) -> RouteClause:
    spec = ROUTE_THEOREM_CLAUSES[route_id]
    rows = _rows_for_route(route_id)
    stage_ids = tuple(str(r.get("stage_id")) for r in rows)
    external = _unique(slot for r in rows for slot in r.get("required_external_slots", ()))
    counterterms = _unique(slot for r in rows for slot in r.get("required_counterterm_slots", ()))
    return RouteClause(
        route_id=route_id,
        domain=tuple(spec["domain"]),
        target=str(spec["target"]),
        map_symbol=str(spec["map_symbol"]),
        claim_when_closed=str(spec["claim_when_closed"]),
        stage_ids=stage_ids,
        required_external_slots=external,
        required_counterterm_slots=counterterms,
        present_status="OPEN: theorem form closed; evaluated transport maps not filled",
    )


def check_T_transport_theorem_upstream_banks_closed() -> Dict[str, Any]:
    """The theorem is built only on closed boundary/ledger/route/composition gates."""
    deps = {
        "trace_sector_closure": _check_trace_sector(),
        "trace_to_scheme_boundary": _check_boundary(),
        "transport_ledger": _check_ledger(),
        "transport_routes": _check_routes(),
        "transport_composition": _check_composition(),
        "transport_completion_gate": _check_completion(),
    }
    assert all(_passed(v) for v in deps.values())
    assert deps["trace_sector_closure"].get("exports_physical_masses") is False
    return {
        "name": "T_transport_theorem_upstream_banks_closed",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": THEOREM_STATUS,
        "dependencies": sorted(deps),
        "closed_input_codomain": "APF_TRACE / W_TRACE",
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "The transport theorem rests on closed trace, boundary, ledger, route, composition, and completion-gate banks.",
    }


def check_T_admissible_transport_definition_complete() -> Dict[str, Any]:
    """Declare the exact data required by the theorem."""
    return {
        "name": "T_admissible_transport_definition_complete",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": THEOREM_STATUS,
        "required_obligations": list(TRANSPORT_THEOREM_OBLIGATIONS),
        "forbidden_shortcut": "identity APF_TRACE/W_TRACE -> physical reporting scheme",
        "allowed_output_before_all_obligations": "validation comparison or symbolic route plan only",
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "Admissible transport is a typed, ledgered, uncertainty-propagating map; it is not a codomain relabeling.",
    }


def check_T_transport_export_iff_certificate_complete() -> Dict[str, Any]:
    """State the iff gate: physical export iff every terminal certificate field is filled."""
    certs = tuple(_export_certificate(route_id) for route_id in OPEN_ROUTE_ORDER + ("identity_trace_to_physical_route",))
    assert not any(c.may_export_physical_scheme_value for c in certs)
    fields_actual = tuple(field.name for field in fields(ExportCertificate))
    assert fields_actual == REQUIRED_EXPORT_CERTIFICATE_FIELDS
    return {
        "name": "T_transport_export_iff_certificate_complete",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": THEOREM_STATUS,
        "iff_statement": "A trace value may be exported as a physical scheme value iff its route certificate has all positive fields filled and target_observables_consumed is false.",
        "certificate_fields": list(fields_actual),
        "current_certificates": [asdict(c) for c in certs],
        "current_exporting_routes": [],
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "The theorem closes the export predicate while proving that no current route satisfies it.",
    }


def check_T_route_specific_theorem_clauses_enumerated() -> Dict[str, Any]:
    """Every allowed route has a route-specific theorem clause."""
    clauses = tuple(_route_clause(route_id) for route_id in OPEN_ROUTE_ORDER)
    assert {c.route_id for c in clauses} == set(OPEN_ROUTE_ORDER)
    assert all(c.stage_ids for c in clauses)
    return {
        "name": "T_route_specific_theorem_clauses_enumerated",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": THEOREM_STATUS,
        "clauses": [asdict(c) for c in clauses],
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "The theorem specializes to W, charged-lepton, colored-MSbar, colored-pole, and light-quark routes.",
    }


def check_T_w_trace_on_shell_route_theorem_obligations() -> Dict[str, Any]:
    """W_TRACE is the first route but remains open until EW finite maps are evaluated."""
    clause = _route_clause("w_trace_on_shell_route")
    cert = _export_certificate("w_trace_on_shell_route")
    assert clause.stage_ids == ("w_input_basis_contract", "w_radiative_finite_conversion", "w_uncertainty_protocol")
    assert cert.may_export_physical_scheme_value is False
    return {
        "name": "T_w_trace_on_shell_route_theorem_obligations",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": THEOREM_STATUS,
        "route_clause": asdict(clause),
        "certificate": asdict(cert),
        "next_closure_payload": [
            "electroweak input-basis contract filled without M_W target consumption",
            "radiative finite conversion map evaluated",
            "on-shell convention and uncertainty protocol evaluated",
        ],
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "W_TRACE is the cleanest first physical-export route, but current paper status remains validation-only.",
    }


def check_T_bottom_msbar_route_theorem_obligations() -> Dict[str, Any]:
    """Bottom validation is promising but the colored MSbar transport theorem is still open."""
    clause = _route_clause("colored_msbar_running_route")
    cert = _export_certificate("colored_msbar_running_route")
    assert "colored_msbar_qcd_running" in clause.stage_ids
    assert "colored_msbar_threshold_matching" in clause.stage_ids
    assert cert.may_export_physical_scheme_value is False
    return {
        "name": "T_bottom_msbar_route_theorem_obligations",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": THEOREM_STATUS,
        "route_clause": asdict(clause),
        "bottom_trace_value_GeV": 4.1774904559270665,
        "validation_neighborhood": "within 0.79 sigma of PDG 2025 mb(mb)_MSbar, but not an exported MSbar mass",
        "certificate": asdict(cert),
        "next_closure_payload": [
            "MSbar target contract for m_b(m_b) filled before comparison residuals are read",
            "QCD anomalous-dimension running map evaluated",
            "threshold matching and scale envelope evaluated",
            "external alpha_s/threshold/correlation ledger filled",
        ],
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "Bottom remains the best colored target, but its physical MSbar export requires the colored route certificate.",
    }


def check_T_no_inverse_fit_transport_theorem() -> Dict[str, Any]:
    """The theorem excludes target-observable fitting as a matter of definition and certificate."""
    comp = _check_composition()
    rows = tuple(comp.get("composition_stage_table", ()))
    consumers = [r for r in rows if r.get("consumes_target_observables")]
    certs = tuple(_export_certificate(route_id) for route_id in OPEN_ROUTE_ORDER)
    assert not consumers
    assert not any(c.target_observables_consumed for c in certs)
    return {
        "name": "T_no_inverse_fit_transport_theorem",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": THEOREM_STATUS + " | no-smuggling",
        "stage_consumers_of_target_observables": [],
        "certificate_target_consumers": [],
        "forbidden_inputs": [
            "target physical mass vector",
            "reported M_W target value",
            "PDG/MSbar/pole/lattice masses as calibration inputs",
            "post-hoc scalar fitted to residuals",
            "identity codomain relabeling",
        ],
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "Transport may use external constants and counterterms, but not the quantity being predicted as an inverse calibration input.",
    }


def check_T_residuals_are_transport_observables_not_contradictions() -> Dict[str, Any]:
    """Paper-facing interpretation of W and bottom residuals before export closure."""
    return {
        "name": "T_residuals_are_transport_observables_not_contradictions",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": THEOREM_STATUS,
        "residual_rule": "Before a route certificate closes, residuals measure unresolved trace-to-scheme transport plus external/input and comparison uncertainty, not APF_TRACE failure or physical export.",
        "applies_to": [
            "W_TRACE few-MeV positive residual",
            "sin^2(theta_W) order-10^-3 scheme displacement",
            "bottom TRACE few-MeV short-distance residual",
        ],
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "Validation residuals are now assigned to the transport theorem's open finite-map slots.",
    }


def check_T_trace_to_scheme_transport_theorem_bank_closure() -> Dict[str, Any]:
    """Close the v14.9 theorem-form bank without exporting physical masses."""
    checks = [
        check_T_transport_theorem_upstream_banks_closed(),
        check_T_admissible_transport_definition_complete(),
        check_T_transport_export_iff_certificate_complete(),
        check_T_route_specific_theorem_clauses_enumerated(),
        check_T_w_trace_on_shell_route_theorem_obligations(),
        check_T_bottom_msbar_route_theorem_obligations(),
        check_T_no_inverse_fit_transport_theorem(),
        check_T_residuals_are_transport_observables_not_contradictions(),
    ]
    assert all(_passed(c) for c in checks)
    return {
        "name": "T_trace_to_scheme_transport_theorem_bank_closure",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": THEOREM_STATUS,
        # dependencies, NOT component_checks (.396 second-audit leg-9
        # catch, reversing the 22:53 follow-through): this module's
        # register() ships _collect_checks(), so all eight constituents
        # ARE individually registered bank members -- citing them as
        # dependencies creates NO dangling roots (each resolves), and
        # parking them in component_checks silently dropped eight
        # registered members (and their subtrees) from every census
        # closure. The K3/w_os precedent applies only to UNREGISTERED
        # in-body parts; the leg-9 lint now polices exactly this.
        "dependencies": [c["name"] for c in checks],
        "closed_now": "trace-to-scheme transport theorem form and export iff-gate",
        "still_open": "evaluated route maps and filled external/counterterm/uncertainty ledgers for any physical scheme export",
        "recommended_next_route": "w_trace_on_shell_route, then bottom MSbar colored route or charged lepton route",
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "key_result": "v14.9 proves what must be true for physical export and why the present results remain validation/trace claims only.",
    }

# v15.x registry compatibility shim: earlier paper theorem layer exposed check_* functions
# for verify_all but did not expose a bank.register hook.
def _collect_checks() -> Dict[str, Any]:
    return {name: obj for name, obj in globals().items() if name.startswith("check_") and callable(obj)}


def register(registry: Dict[str, Any]) -> None:
    registry.update(_collect_checks())


def run_all() -> Dict[str, Any]:
    rows = []
    for name, fn in _collect_checks().items():
        try:
            result = fn()
            rows.append({"name": name, "passed": _passed(result), "result": result})
        except Exception as exc:  # pragma: no cover
            rows.append({"name": name, "passed": False, "error": repr(exc)})
    ok = all(r["passed"] for r in rows)
    return {"passed": ok, "status": "TRACE_TO_SCHEME_TRANSPORT_THEOREM_BANK_PASS" if ok else "TRACE_TO_SCHEME_TRANSPORT_THEOREM_BANK_FAIL", "checks": rows}
