"""Trace transport composition bank.

v8.8 (2026-05-08 LATER-6): executable composition layer for the trace-to-
scheme transport program.  The v8.7 route bank named the admissible route
families and their prerequisites; this module banks the next structural layer:
each open route is represented by an ordered, acyclic composition plan whose
stages expose inputs, outputs, external slots, counterterm slots, and export
flags.

This is intentionally *not* a numerical transport theorem.  No QCD/QED/EW
running, threshold, pole/on-shell, lattice, finite-part, or uncertainty map is
evaluated here.  The point is to make the route maps composable and auditable
before any physical comparison is attempted.

Status discipline:
    - APF_TRACE / W_TRACE closure: [P_local] upstream.
    - Trace-to-scheme boundary discipline: [P_boundary] upstream.
    - Transport ledger architecture: [P_ledger] upstream.
    - Route classification: [P_route] upstream.
    - This module: [P_composition], ordered symbolic stage composition only.
    - Physical scheme masses: still open; no physical mass vector is exported.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Iterable, Mapping, Tuple

from apf.trace_transport_routes import (
    EXPORTS_PHYSICAL_SCHEME_MASSES as ROUTES_EXPORT_PHYSICAL_SCHEME_MASSES,
    FORBIDDEN_ROUTE_IDS,
    OPEN_ROUTE_IDS,
    PHYSICAL_TRANSPORT_CLOSED as ROUTES_PHYSICAL_TRANSPORT_CLOSED,
    check_T_transport_routes_bank_closure as _check_T_transport_routes_bank_closure,
    _route_by_id,
)


COMPOSITION_STATUS = "P_composition"
PHYSICAL_TRANSPORT_CLOSED = False
EXPORTS_PHYSICAL_SCHEME_MASSES = False

TRACE_INPUT_CODOMAINS: Tuple[str, ...] = (
    "APF_TRACE immutable charged-fermion codomain",
    "W_TRACE immutable weak-branch codomain",
)

FORBIDDEN_OUTPUT_CODOMAINS: Tuple[str, ...] = (
    "physical mass vector",
    "observed mass table",
    "target residual fit",
    "identity physical reporting codomain",
)

STAGE_FIELDS: Tuple[str, ...] = (
    "route_id",
    "stage_id",
    "stage_order",
    "input_codomain",
    "output_codomain",
    "required_map",
    "required_external_slots",
    "required_counterterm_slots",
    "consumes_target_observables",
    "computes_numerical_transport",
    "exports_physical_mass_claim",
)


@dataclass(frozen=True)
class CompositionStage:
    """One symbolic stage in a trace-to-scheme transport route."""

    route_id: str
    stage_id: str
    stage_order: int
    input_codomain: str
    output_codomain: str
    required_map: str
    required_external_slots: Tuple[str, ...]
    required_counterterm_slots: Tuple[str, ...]
    consumes_target_observables: bool = False
    computes_numerical_transport: bool = False
    exports_physical_mass_claim: bool = False


def _passed(result: Mapping[str, Any]) -> bool:
    return bool(result.get("passed") is True or str(result.get("status", "")).upper() in {"PASS", "P"})


def _stage_table() -> Tuple[CompositionStage, ...]:
    return (
        # Colored short-distance / MSbar-like symbolic route.
        CompositionStage(
            route_id="colored_msbar_running_route",
            stage_id="colored_msbar_contract",
            stage_order=10,
            input_codomain="APF_TRACE immutable colored-fermion codomain",
            output_codomain="colored scheme-contract codomain S_q(mu)",
            required_map="scheme contract declaration",
            required_external_slots=(
                "renormalization scales and scale-variation envelope",
                "uncertainties, correlations, and provenance tags",
            ),
            required_counterterm_slots=("scheme-specific finite-part convention slot",),
        ),
        CompositionStage(
            route_id="colored_msbar_running_route",
            stage_id="colored_msbar_qcd_running",
            stage_order=20,
            input_codomain="colored scheme-contract codomain S_q(mu)",
            output_codomain="symbolic colored short-distance running codomain",
            required_map="QCD anomalous-dimension running map",
            required_external_slots=(
                "alpha_s(mu) and/or Lambda_QCD convention for colored transport",
                "renormalization scales and scale-variation envelope",
            ),
            required_counterterm_slots=("QCD running anomalous-dimension/counterterm slot",),
        ),
        CompositionStage(
            route_id="colored_msbar_running_route",
            stage_id="colored_msbar_threshold_matching",
            stage_order=30,
            input_codomain="symbolic colored short-distance running codomain",
            output_codomain="symbolic colored threshold-matched codomain",
            required_map="quark-threshold matching map",
            required_external_slots=(
                "quark-threshold matching conventions and threshold order",
                "uncertainties, correlations, and provenance tags",
            ),
            required_counterterm_slots=("QCD threshold matching slot",),
        ),
        CompositionStage(
            route_id="colored_msbar_running_route",
            stage_id="colored_msbar_uncertainty_envelope",
            stage_order=40,
            input_codomain="symbolic colored threshold-matched codomain",
            output_codomain="comparison-ready symbolic colored S_q(mu) codomain",
            required_map="scale-variation and uncertainty propagation map",
            required_external_slots=("uncertainties, correlations, and provenance tags",),
            required_counterterm_slots=(),
        ),
        # Charged-lepton route.
        CompositionStage(
            route_id="charged_lepton_pole_or_running_route",
            stage_id="lepton_contract",
            stage_order=10,
            input_codomain="APF_TRACE immutable charged-lepton codomain",
            output_codomain="charged-lepton scheme-contract codomain",
            required_map="scheme-specific finite-part convention",
            required_external_slots=(
                "renormalization scales and scale-variation envelope",
                "uncertainties, correlations, and provenance tags",
            ),
            required_counterterm_slots=("scheme-specific finite-part convention slot",),
        ),
        CompositionStage(
            route_id="charged_lepton_pole_or_running_route",
            stage_id="lepton_qed_running_conversion",
            stage_order=20,
            input_codomain="charged-lepton scheme-contract codomain",
            output_codomain="symbolic charged-lepton QED-running codomain",
            required_map="QED running/conversion map",
            required_external_slots=(
                "alpha_em(mu) or electroweak input basis for charged-lepton/EW transport",
                "renormalization scales and scale-variation envelope",
            ),
            required_counterterm_slots=("QED charged-lepton running slot",),
        ),
        CompositionStage(
            route_id="charged_lepton_pole_or_running_route",
            stage_id="lepton_ew_finite_policy",
            stage_order=30,
            input_codomain="symbolic charged-lepton QED-running codomain",
            output_codomain="comparison-ready symbolic charged-lepton codomain",
            required_map="EW/Yukawa finite correction policy when target precision requires it",
            required_external_slots=("uncertainties, correlations, and provenance tags",),
            required_counterterm_slots=("EW/Yukawa running slot",),
        ),
        # W_TRACE route.
        CompositionStage(
            route_id="w_trace_on_shell_route",
            stage_id="w_input_basis_contract",
            stage_order=10,
            input_codomain="W_TRACE immutable weak-branch codomain",
            output_codomain="symbolic EW input-basis codomain",
            required_map="EW input-basis declaration",
            required_external_slots=(
                "weak input convention for W/on-shell comparisons",
                "alpha_em(mu) or electroweak input basis for charged-lepton/EW transport",
            ),
            required_counterterm_slots=("scheme-specific finite-part convention slot",),
        ),
        CompositionStage(
            route_id="w_trace_on_shell_route",
            stage_id="w_radiative_finite_conversion",
            stage_order=20,
            input_codomain="symbolic EW input-basis codomain",
            output_codomain="symbolic W on-shell-convention codomain",
            required_map="radiative correction / finite-part conversion map",
            required_external_slots=("uncertainties, correlations, and provenance tags",),
            required_counterterm_slots=(
                "EW/Yukawa running slot",
                "on-shell or pole-convention conversion slot",
            ),
        ),
        CompositionStage(
            route_id="w_trace_on_shell_route",
            stage_id="w_uncertainty_protocol",
            stage_order=30,
            input_codomain="symbolic W on-shell-convention codomain",
            output_codomain="comparison-ready symbolic W convention codomain",
            required_map="uncertainty propagation and comparison protocol",
            required_external_slots=("uncertainties, correlations, and provenance tags",),
            required_counterterm_slots=(),
        ),
        # Colored pole/on-shell route extends the colored short-distance leg.
        CompositionStage(
            route_id="colored_pole_or_on_shell_route",
            stage_id="colored_short_distance_leg_required",
            stage_order=10,
            input_codomain="comparison-ready symbolic colored S_q(mu) codomain",
            output_codomain="symbolic colored short-distance codomain accepted",
            required_map="short-distance colored transport route",
            required_external_slots=(
                "alpha_s(mu) and/or Lambda_QCD convention for colored transport",
                "renormalization scales and scale-variation envelope",
            ),
            required_counterterm_slots=("QCD running anomalous-dimension/counterterm slot",),
        ),
        CompositionStage(
            route_id="colored_pole_or_on_shell_route",
            stage_id="colored_pole_conversion",
            stage_order=20,
            input_codomain="symbolic colored short-distance codomain accepted",
            output_codomain="comparison-ready symbolic colored pole/on-shell codomain",
            required_map="pole/on-shell conversion finite-part map",
            required_external_slots=("uncertainties, correlations, and provenance tags",),
            required_counterterm_slots=("on-shell or pole-convention conversion slot",),
        ),
        CompositionStage(
            route_id="colored_pole_or_on_shell_route",
            stage_id="colored_pole_ambiguity_ledger",
            stage_order=30,
            input_codomain="comparison-ready symbolic colored pole/on-shell codomain",
            output_codomain="symbolic colored pole/on-shell codomain with ambiguity ledger",
            required_map="renormalon/scheme-ambiguity warning ledger for quarks",
            required_external_slots=("uncertainties, correlations, and provenance tags",),
            required_counterterm_slots=(),
        ),
        # Light-quark low-energy route requires a nonperturbative convention leg.
        CompositionStage(
            route_id="light_quark_low_energy_route",
            stage_id="light_quark_nonperturbative_contract",
            stage_order=10,
            input_codomain="APF_TRACE immutable light-quark codomain",
            output_codomain="symbolic low-energy nonperturbative contract codomain",
            required_map="nonperturbative convention declaration",
            required_external_slots=(
                "alpha_s(mu) and/or Lambda_QCD convention for colored transport",
                "quark-threshold matching conventions and threshold order",
                "uncertainties, correlations, and provenance tags",
            ),
            required_counterterm_slots=(
                "QCD threshold matching slot",
                "scheme-specific finite-part convention slot",
            ),
        ),
        CompositionStage(
            route_id="light_quark_low_energy_route",
            stage_id="light_quark_matching",
            stage_order=20,
            input_codomain="symbolic low-energy nonperturbative contract codomain",
            output_codomain="comparison-ready symbolic light-quark low-energy codomain",
            required_map="matching from trace codomain into selected low-energy convention",
            required_external_slots=("uncertainties, correlations, and provenance tags",),
            required_counterterm_slots=("scheme-specific finite-part convention slot",),
        ),
    )


def _stages_for(route_id: str) -> Tuple[CompositionStage, ...]:
    return tuple(stage for stage in _stage_table() if stage.route_id == route_id)


def _required_maps_for(route_id: str) -> Tuple[str, ...]:
    return _route_by_id(route_id).required_maps


def _is_strictly_increasing(values: Iterable[int]) -> bool:
    values = tuple(values)
    return all(a < b for a, b in zip(values, values[1:]))


# ---------------------------------------------------------------------
# Bank-facing composition checks.
# ---------------------------------------------------------------------


def check_T_transport_composition_status_declared() -> Dict[str, Any]:
    """Declare that v8.8 is symbolic route composition, not transport closure."""
    routes = _check_T_transport_routes_bank_closure()
    assert _passed(routes)
    assert routes.get("physical_transport_closed") is False
    assert ROUTES_PHYSICAL_TRANSPORT_CLOSED is False
    assert ROUTES_EXPORT_PHYSICAL_SCHEME_MASSES is False
    return {
        "name": "T_transport_composition_status_declared",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPOSITION_STATUS,
        "dependencies": ["T_transport_routes_bank_closure"],
        "closed_now": "ordered symbolic route-stage composition",
        "open_next": "derive/evaluate actual QCD/QED/EW/threshold/finite-part maps",
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "v8.8 banks how admissible route stages compose while leaving numerical physical transport open.",
    }


def check_T_composition_stage_schema_complete() -> Dict[str, Any]:
    """Every composition stage exposes the audit fields required for no-smuggling."""
    missing_by_stage = {}
    for stage in _stage_table():
        payload = asdict(stage)
        missing = [field for field in STAGE_FIELDS if field not in payload]
        if missing:
            missing_by_stage[stage.stage_id] = missing
    assert not missing_by_stage
    return {
        "name": "T_composition_stage_schema_complete",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_composition | no-smuggling",
        "stage_count": len(_stage_table()),
        "required_fields": list(STAGE_FIELDS),
        "stages": [asdict(stage) for stage in _stage_table()],
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "Each symbolic stage has explicit codomain, prerequisite-map, ledger-slot, and export flags.",
    }


def check_T_composition_graph_acyclic() -> Dict[str, Any]:
    """Stage orders are strictly increasing in every route, giving an acyclic DAG."""
    route_orders = {route_id: [stage.stage_order for stage in _stages_for(route_id)] for route_id in OPEN_ROUTE_IDS}
    assert all(_is_strictly_increasing(orders) for orders in route_orders.values())
    assert len({(stage.route_id, stage.stage_id) for stage in _stage_table()}) == len(_stage_table())
    return {
        "name": "T_composition_graph_acyclic",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_composition | DAG",
        "route_orders": route_orders,
        "cycles_detected": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "Every open route has a strictly ordered symbolic composition chain.",
    }


def check_T_open_routes_have_nonempty_stage_plans() -> Dict[str, Any]:
    """Each open route has at least one symbolic composition plan."""
    stage_counts = {route_id: len(_stages_for(route_id)) for route_id in OPEN_ROUTE_IDS}
    assert all(count > 0 for count in stage_counts.values())
    assert not _stages_for(FORBIDDEN_ROUTE_IDS[0])
    return {
        "name": "T_open_routes_have_nonempty_stage_plans",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPOSITION_STATUS,
        "stage_counts": stage_counts,
        "forbidden_route_stage_count": len(_stages_for(FORBIDDEN_ROUTE_IDS[0])),
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "All open routes are composition-ready; the forbidden identity route remains planless.",
    }


def check_T_colored_msbar_composition_ordered() -> Dict[str, Any]:
    """Colored short-distance route is contract -> QCD running -> thresholds -> uncertainty."""
    route_id = "colored_msbar_running_route"
    stages = _stages_for(route_id)
    stage_ids = tuple(stage.stage_id for stage in stages)
    assert stage_ids == (
        "colored_msbar_contract",
        "colored_msbar_qcd_running",
        "colored_msbar_threshold_matching",
        "colored_msbar_uncertainty_envelope",
    )
    required = set(_required_maps_for(route_id))
    covered = {stage.required_map for stage in stages}
    assert "QCD anomalous-dimension running map" in covered
    assert "quark-threshold matching map" in covered
    assert covered.issubset(required | {"scheme contract declaration"})
    return {
        "name": "T_colored_msbar_composition_ordered",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_composition | colored-branch",
        "stage_ids": list(stage_ids),
        "terminal_codomain": stages[-1].output_codomain,
        "computed_here": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The colored short-distance route now has an ordered symbolic composition plan without evaluating QCD transport.",
    }


def check_T_charged_lepton_composition_ordered() -> Dict[str, Any]:
    """Charged-lepton route is contract -> QED conversion -> EW finite policy."""
    route_id = "charged_lepton_pole_or_running_route"
    stages = _stages_for(route_id)
    stage_ids = tuple(stage.stage_id for stage in stages)
    assert stage_ids == (
        "lepton_contract",
        "lepton_qed_running_conversion",
        "lepton_ew_finite_policy",
    )
    assert stages[-1].output_codomain == "comparison-ready symbolic charged-lepton codomain"
    return {
        "name": "T_charged_lepton_composition_ordered",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_composition | lepton-branch",
        "stage_ids": list(stage_ids),
        "terminal_codomain": stages[-1].output_codomain,
        "computed_here": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The charged-lepton route now has an ordered QED/EW symbolic composition plan.",
    }


def check_T_w_trace_composition_ordered() -> Dict[str, Any]:
    """W_TRACE route is input-basis contract -> radiative conversion -> uncertainty."""
    route_id = "w_trace_on_shell_route"
    stages = _stages_for(route_id)
    stage_ids = tuple(stage.stage_id for stage in stages)
    assert stage_ids == (
        "w_input_basis_contract",
        "w_radiative_finite_conversion",
        "w_uncertainty_protocol",
    )
    assert stages[0].input_codomain == "W_TRACE immutable weak-branch codomain"
    return {
        "name": "T_w_trace_composition_ordered",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_composition | W_TRACE-boundary",
        "stage_ids": list(stage_ids),
        "terminal_codomain": stages[-1].output_codomain,
        "computed_here": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The W_TRACE route now has an ordered symbolic EW/on-shell composition plan.",
    }


def check_T_colored_pole_composition_extends_msbar() -> Dict[str, Any]:
    """Colored pole/on-shell route is staged after short-distance transport."""
    stages = _stages_for("colored_pole_or_on_shell_route")
    assert stages[0].input_codomain == "comparison-ready symbolic colored S_q(mu) codomain"
    assert stages[0].required_map == "short-distance colored transport route"
    assert any(stage.required_map == "pole/on-shell conversion finite-part map" for stage in stages)
    return {
        "name": "T_colored_pole_composition_extends_msbar",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_composition | colored-branch",
        "stage_ids": [stage.stage_id for stage in stages],
        "depends_on_route": "colored_msbar_running_route",
        "direct_trace_to_pole_allowed": False,
        "computed_here": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "Colored pole/on-shell comparison remains a second-leg route after short-distance transport.",
    }


def check_T_light_quark_composition_requires_nonperturbative_leg() -> Dict[str, Any]:
    """Light-quark route begins with a nonperturbative contract, not identity."""
    stages = _stages_for("light_quark_low_energy_route")
    assert stages[0].stage_id == "light_quark_nonperturbative_contract"
    assert "nonperturbative contract" in stages[0].output_codomain
    assert all("physical" not in stage.output_codomain.lower() for stage in stages)
    return {
        "name": "T_light_quark_composition_requires_nonperturbative_leg",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_composition | nonperturbative-boundary",
        "stage_ids": [stage.stage_id for stage in stages],
        "direct_trace_to_low_energy_quote_allowed": False,
        "computed_here": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "Light-quark comparison is blocked until a nonperturbative convention leg is declared and evaluated.",
    }


def check_T_stage_inputs_exclude_target_observables() -> Dict[str, Any]:
    """No symbolic stage is allowed to consume target mass observables."""
    offending = [stage.stage_id for stage in _stage_table() if stage.consumes_target_observables]
    assert not offending
    assert all(not stage.consumes_target_observables for stage in _stage_table())
    return {
        "name": "T_stage_inputs_exclude_target_observables",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_composition | no-inverse-fit",
        "offending_stages": offending,
        "target_observables_consumed": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "Composition stages cannot read physical target masses as inputs.",
    }


def check_T_stage_outputs_are_intermediate_not_physical_claims() -> Dict[str, Any]:
    """Terminal codomains remain symbolic/comparison-ready, not physical claims."""
    bad_flags = [stage.stage_id for stage in _stage_table() if stage.exports_physical_mass_claim]
    bad_words = [
        stage.stage_id
        for stage in _stage_table()
        if any(forbidden in stage.output_codomain.lower() for forbidden in ("observed", "target residual", "identity physical"))
    ]
    assert not bad_flags
    assert not bad_words
    assert all(stage.computes_numerical_transport is False for stage in _stage_table())
    return {
        "name": "T_stage_outputs_are_intermediate_not_physical_claims",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_composition | codomain-discipline",
        "bad_export_flags": bad_flags,
        "bad_output_codomain_words": bad_words,
        "computes_numerical_transport": False,
        "forbidden_output_codomain_examples": list(FORBIDDEN_OUTPUT_CODOMAINS),
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "All stage outputs are symbolic/intermediate codomains rather than physical mass predictions.",
    }


def check_T_forbidden_identity_route_has_no_composition_plan() -> Dict[str, Any]:
    """The identity trace-to-physical route remains quarantined."""
    forbidden_counts = {route_id: len(_stages_for(route_id)) for route_id in FORBIDDEN_ROUTE_IDS}
    assert all(count == 0 for count in forbidden_counts.values())
    return {
        "name": "T_forbidden_identity_route_has_no_composition_plan",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_composition | no-smuggling",
        "forbidden_stage_counts": forbidden_counts,
        "identity_route_composable": False,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The forbidden identity route is not merely uncomputed; it has no admissible composition plan.",
    }


def check_T_composition_external_slots_accounted_to_route() -> Dict[str, Any]:
    """Every stage-level external/counterterm slot is already declared by its route."""
    missing_external = {}
    missing_counterterm = {}
    for route_id in OPEN_ROUTE_IDS:
        route = _route_by_id(route_id)
        route_external = set(route.required_external_slots)
        route_counterterms = set(route.required_counterterm_slots)
        used_external = {slot for stage in _stages_for(route_id) for slot in stage.required_external_slots}
        used_counterterms = {slot for stage in _stages_for(route_id) for slot in stage.required_counterterm_slots}
        ext_delta = sorted(used_external - route_external)
        ct_delta = sorted(used_counterterms - route_counterterms)
        if ext_delta:
            missing_external[route_id] = ext_delta
        if ct_delta:
            missing_counterterm[route_id] = ct_delta
    assert not missing_external
    assert not missing_counterterm
    return {
        "name": "T_composition_external_slots_accounted_to_route",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": "P_composition | ledger-compatibility",
        "missing_external_slots": missing_external,
        "missing_counterterm_slots": missing_counterterm,
        "new_hidden_slots": [],
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "Stage composition introduces no hidden external constants or counterterm slots beyond the v8.7 routes.",
    }


def check_T_trace_transport_composition_bank_closure() -> Dict[str, Any]:
    """Master v8.8 closure: symbolic composition only, no physical transport."""
    deps = [
        check_T_transport_composition_status_declared(),
        check_T_composition_stage_schema_complete(),
        check_T_composition_graph_acyclic(),
        check_T_open_routes_have_nonempty_stage_plans(),
        check_T_colored_msbar_composition_ordered(),
        check_T_charged_lepton_composition_ordered(),
        check_T_w_trace_composition_ordered(),
        check_T_colored_pole_composition_extends_msbar(),
        check_T_light_quark_composition_requires_nonperturbative_leg(),
        check_T_stage_inputs_exclude_target_observables(),
        check_T_stage_outputs_are_intermediate_not_physical_claims(),
        check_T_forbidden_identity_route_has_no_composition_plan(),
        check_T_composition_external_slots_accounted_to_route(),
    ]
    assert all(_passed(dep) for dep in deps)
    return {
        "name": "T_trace_transport_composition_bank_closure",
        "passed": True,
        "status": "PASS",
        "tier": 4,
        "epistemic": COMPOSITION_STATUS,
        "dependencies": [dep["name"] for dep in deps],
        "composition_stage_table": [asdict(stage) for stage in _stage_table()],
        "closed_now": "ordered symbolic composition plans for all open transport routes",
        "open_next": "fill one route with evaluated transport maps and uncertainty propagation",
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "key_result": "The trace-to-scheme transport program now has an executable symbolic composition DAG; physical masses remain open.",
    }


_CHECKS = {
    "T_transport_composition_status_declared": check_T_transport_composition_status_declared,
    "T_composition_stage_schema_complete": check_T_composition_stage_schema_complete,
    "T_composition_graph_acyclic": check_T_composition_graph_acyclic,
    "T_open_routes_have_nonempty_stage_plans": check_T_open_routes_have_nonempty_stage_plans,
    "T_colored_msbar_composition_ordered": check_T_colored_msbar_composition_ordered,
    "T_charged_lepton_composition_ordered": check_T_charged_lepton_composition_ordered,
    "T_w_trace_composition_ordered": check_T_w_trace_composition_ordered,
    "T_colored_pole_composition_extends_msbar": check_T_colored_pole_composition_extends_msbar,
    "T_light_quark_composition_requires_nonperturbative_leg": check_T_light_quark_composition_requires_nonperturbative_leg,
    "T_stage_inputs_exclude_target_observables": check_T_stage_inputs_exclude_target_observables,
    "T_stage_outputs_are_intermediate_not_physical_claims": check_T_stage_outputs_are_intermediate_not_physical_claims,
    "T_forbidden_identity_route_has_no_composition_plan": check_T_forbidden_identity_route_has_no_composition_plan,
    "T_composition_external_slots_accounted_to_route": check_T_composition_external_slots_accounted_to_route,
    "T_trace_transport_composition_bank_closure": check_T_trace_transport_composition_bank_closure,
}


def register(registry: Dict[str, Any]) -> None:
    """Register trace transport composition checks into the global bank."""
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
        "status": "TRACE_TRANSPORT_COMPOSITION_BANK_PASS" if ok else "TRACE_TRANSPORT_COMPOSITION_BANK_FAIL",
        "bank_registered": True,
        "composition_status": COMPOSITION_STATUS,
        "physical_transport_closed": PHYSICAL_TRANSPORT_CLOSED,
        "exports_physical_scheme_masses": EXPORTS_PHYSICAL_SCHEME_MASSES,
        "results": rows,
    }


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2))
