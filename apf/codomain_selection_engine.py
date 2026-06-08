"""APF Codomain Selection Engine.

Tier 2 member of the APF Interface Engine family per
``APF Reference Docs/Reference - APF Interface Engine Family Architecture (2026-05-19).md``
(Session 2 of the sequencing plan).

The Codomain Selection Engine adjudicates a *regime's competition over
admissible coherent codomains*. This is structurally orthogonal to the existing
Route Adjudication Engine (which adjudicates single transport paths through a
sector). Both engines share the IE family's audit-first discipline + abstract
output shape (verdict + critical fields + obligation packet), but they differ
in unit of adjudication, failure-mode taxonomy, and underlying machinery.

Unit of adjudication
--------------------

A regime's codomain competition. Input: a regime name from the
``APF_IE_EXTENDED_COHERENT_PHASE_REGIMES_v1`` registry (currently 7 regimes:
SUPERCONDUCTIVITY / SUPERFLUIDITY / MAGNETISM / BOSE_EINSTEIN_CONDENSATION /
LASER_COHERENCE / SYNCHRONIZATION / TOPOLOGICAL_ORDER), plus a network state
dict describing the interface network's nodes / edges / defects / costs.

Output: a ``CodomainSelectionVerdict`` typed by the engine's failure-mode
taxonomy.

Failure-mode taxonomy
---------------------

Engine-specific (not shared with Route Adjudication Engine):

* ``COHERENT_CODOMAIN_SELECTED`` -- coherent codomain wins competition;
  all audit gates pass.
* ``MARGIN_NONPOSITIVE`` -- candidate coherent codomain's admissibility margin
  S = C(R_N) - C(R_SC) - Pi_defects <= 0.
* ``PHASE_LOCK_FAILED`` -- margin positive but phase-locking audit gate fails.
* ``COHERENCE_INSUFFICIENT`` -- margin positive, phase locked, but coherent
  density below threshold.
* ``METASTABLE_HISTORY_LOCKED`` -- coherent codomain wins on instantaneous
  margin but history state + transition barrier hold current codomain in
  fragmented regime (hysteresis layer).
* ``OPEN_EVIDENCE_REQUIRED`` -- regime lacks a runtime evaluator or input
  network state is incomplete.

Per-regime runtime availability
-------------------------------

As of v24.3.65, all seven coherent-phase regimes (SUPERCONDUCTIVITY, SUPERFLUIDITY,
MAGNETISM, BOSE_EINSTEIN_CONDENSATION, LASER_COHERENCE, SYNCHRONIZATION,
TOPOLOGICAL_ORDER) have runtime evaluators; the coherent-phase family is complete.
A regime registered without a runtime evaluator would return ``OPEN_EVIDENCE_REQUIRED``
with an obligation packet naming the missing evaluator + audit-ladder fixtures.

Dispatch is registry-driven (v24.3.62): each runtime-available regime names its
adjudicator in ``REGIME_RUNTIME_REGISTRY[...]["runtime_dispatcher"]``, resolved via
the ``_REGIME_DISPATCHERS`` table. Landing a regime = flip ``runtime_available`` +
name a dispatcher + add one ``_REGIME_DISPATCHERS`` entry; no other engine code changes.

Audit-first discipline
----------------------

Preserved verbatim from the 9-pack coherent-phase arc + extended-regimes pack:

* ``numeric_critical_temperature = 0`` per regime
* ``material_specific_prediction = 0`` per regime
* ``highTc_solved = 0`` for SC
* ``ab_initio_chemistry = 0`` for all regimes

No empirical claim is exported by this engine. The engine produces *structural
classification verdicts* over interface network states, not material predictions.

References
----------

* ``apf.superconductivity_ie`` -- SCEvaluation runtime evaluator (this engine
  delegates SC adjudication to that module).
* ``apf.codomain_competition`` -- generic competition selector (utility layer).
* ``apf.codomain_transition_dynamics`` -- phase-boundary + transition barriers.
* ``apf.codomain_hysteresis`` -- history-state + barrier-gated transitions.
* ``DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_IE_COHERENT_PHASE_REGIME_MASTER_v1``
  -- master pack with the HistBarrierSelect equation.
* ``DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_IE_EXTENDED_COHERENT_PHASE_REGIMES_v1``
  -- 7-regime registry + general inequality.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Dict, List, Mapping, Optional, Tuple


# ---------------------------------------------------------------------------
# Engine identity (Tier 2 of IE family)
# ---------------------------------------------------------------------------

ENGINE_NAME = "codomain_selection"
ENGINE_FAMILY = "APF_Interface_Engine"
ENGINE_TIER = 2
ENGINE_ROLE = "codomain_competition_adjudication"


# ---------------------------------------------------------------------------
# Verdict status enum (engine-specific failure-mode taxonomy)
# ---------------------------------------------------------------------------

class CodomainSelectionStatus(str, Enum):
    COHERENT_CODOMAIN_SELECTED = "COHERENT_CODOMAIN_SELECTED"
    MARGIN_NONPOSITIVE = "MARGIN_NONPOSITIVE"
    PHASE_LOCK_FAILED = "PHASE_LOCK_FAILED"
    COHERENCE_INSUFFICIENT = "COHERENCE_INSUFFICIENT"
    METASTABLE_HISTORY_LOCKED = "METASTABLE_HISTORY_LOCKED"
    OPEN_EVIDENCE_REQUIRED = "OPEN_EVIDENCE_REQUIRED"


# ---------------------------------------------------------------------------
# Verdict dataclass
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class CodomainSelectionVerdict:
    regime: str
    status: CodomainSelectionStatus
    winner_codomain: Optional[str]
    admissibility_margin: Optional[float]
    audit_gates: Mapping[str, bool]
    critical_fields: Tuple[str, ...]
    obligation_packet: Mapping[str, Any]
    exports: Mapping[str, int]
    reason: str

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["status"] = self.status.value
        return d


# ---------------------------------------------------------------------------
# Per-regime runtime registry (which regimes have runtime evaluators)
# ---------------------------------------------------------------------------

REGIME_RUNTIME_REGISTRY: Dict[str, Dict[str, Any]] = {
    "SUPERCONDUCTIVITY": {
        "runtime_module": "apf.superconductivity_ie",
        "runtime_dispatcher": "_adjudicate_superconductivity",
        "audit_ladder_fixtures": (
            "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/"
            "APF_SUPERCONDUCTIVITY_IE_AUDIT_LADDER_v5/examples/"
        ),
        "runtime_available": True,
    },
    "SUPERFLUIDITY": {
        "runtime_module": "apf.superfluidity_ie",
        "runtime_dispatcher": "_adjudicate_superfluidity",
        "audit_ladder_fixtures": (
            "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/"
            "APF_SUPERFLUIDITY_IE_RUNTIME_SCAFFOLD_v2/examples/"
        ),
        "runtime_available": True,
    },
    "MAGNETISM": {
        "runtime_module": "apf.magnetism_ie",
        "runtime_dispatcher": "_adjudicate_magnetism",
        "audit_ladder_fixtures": "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_IE_MAGNETISM_CODOMAIN_REGIME_v1/",
        "runtime_available": True,
    },
    "BOSE_EINSTEIN_CONDENSATION": {
        "runtime_module": "apf.bec_ie",
        "runtime_dispatcher": "_adjudicate_bec",
        "audit_ladder_fixtures": "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_IE_BEC_CODOMAIN_REGIME_v1/",
        "runtime_available": True,
    },
    "LASER_COHERENCE": {
        "runtime_module": "apf.laser_coherence_ie",
        "runtime_dispatcher": "_adjudicate_laser_coherence",
        "audit_ladder_fixtures": "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_IE_LASER_COHERENCE_CODOMAIN_REGIME_v1/",
        "runtime_available": True,
    },
    "SYNCHRONIZATION": {
        "runtime_module": "apf.synchronization_ie",
        "runtime_dispatcher": "_adjudicate_synchronization",
        "audit_ladder_fixtures": "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_IE_SYNCHRONIZATION_CODOMAIN_REGIME_v1/",
        "runtime_available": True,
    },
    "TOPOLOGICAL_ORDER": {
        "runtime_module": "apf.topological_order_ie",
        "runtime_dispatcher": "_adjudicate_topological_order",
        "audit_ladder_fixtures": "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_IE_TOPOLOGICAL_ORDER_CODOMAIN_REGIME_v1/",
        "runtime_available": True,
    },
}


# ---------------------------------------------------------------------------
# Per-regime audit-first non-claims (preserved verbatim across all 7 regimes)
# ---------------------------------------------------------------------------

PRESERVED_NON_CLAIMS = (
    "numeric_critical_temperature",
    "material_specific_prediction",
    "highTc_solved",
    "ab_initio_chemistry",
)


# ---------------------------------------------------------------------------
# Engine entry point
# ---------------------------------------------------------------------------

def adjudicate_codomain_competition(
    regime: str,
    network_state: Optional[Mapping[str, Any]] = None,
) -> CodomainSelectionVerdict:
    """Adjudicate a regime's codomain competition.

    Parameters
    ----------
    regime : str
        Regime name from the extended-regimes registry. Case-insensitive.
    network_state : Mapping[str, Any] or None
        Interface network state dict (nodes / edges / defects / costs).
        If None, returns OPEN_EVIDENCE_REQUIRED with a network-state-missing
        obligation.

    Returns
    -------
    CodomainSelectionVerdict
    """
    regime_key = regime.upper()
    regime_info = REGIME_RUNTIME_REGISTRY.get(regime_key)

    if regime_info is None:
        return _unknown_regime_verdict(regime)

    if not regime_info["runtime_available"]:
        return _no_runtime_verdict(regime_key, regime_info)

    if network_state is None:
        return _network_missing_verdict(regime_key)

    # Registry-driven dispatch (generalized v24.3.62): each runtime-available
    # regime names its adjudicator via the registry's "runtime_dispatcher"
    # field; _REGIME_DISPATCHERS maps that name to the function. Adding a regime
    # is now: flip runtime_available + name a dispatcher + register it below.
    dispatcher_name = regime_info.get("runtime_dispatcher")
    dispatcher = (
        _REGIME_DISPATCHERS.get(dispatcher_name) if dispatcher_name else None
    )
    if dispatcher is None:
        return _no_runtime_verdict(regime_key, regime_info)
    return dispatcher(network_state)


def _adjudicate_superconductivity(
    network_state: Mapping[str, Any],
) -> CodomainSelectionVerdict:
    """Dispatch SC adjudication to apf.superconductivity_ie.

    Maps SCEvaluation result onto engine-specific verdict status.
    """
    from apf.superconductivity_ie import (
        load_network_dict,
        evaluate_sc_codomain,
    )

    try:
        network, costs = load_network_dict(dict(network_state))
    except (KeyError, TypeError, ValueError) as exc:
        return CodomainSelectionVerdict(
            regime="SUPERCONDUCTIVITY",
            status=CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED,
            winner_codomain=None,
            admissibility_margin=None,
            audit_gates={},
            critical_fields=("network_state_malformed",),
            obligation_packet={
                "obligation_kind": "network_state_malformed",
                "target_engine": ENGINE_NAME,
                "target_unit_id": "regime:SUPERCONDUCTIVITY",
                "evidence_required": [
                    "well-formed network_state dict with nodes / edges / defects / costs",
                ],
                "current_status": "INVALID_INPUT",
                "recommended_next_action": (
                    "supply network state matching apf.superconductivity_ie.load_network_dict schema"
                ),
                "error_detail": f"{type(exc).__name__}: {exc}",
            },
            exports={k: 0 for k in PRESERVED_NON_CLAIMS},
            reason=f"network state load failed: {exc}",
        )

    evaluation = evaluate_sc_codomain(network, costs)

    selected = evaluation.selected_codomain
    if selected == "SC_PHASE_CODOMAIN":
        status = CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED
        winner = "charged_phase_winding_flux"
        critical: Tuple[str, ...] = ()
    elif selected == "DEFECT_OVERLOADED":
        status = CodomainSelectionStatus.MARGIN_NONPOSITIVE
        winner = None
        critical = ("admissibility_margin_nonpositive",)
    elif selected == "PHASE_FRAGMENTED":
        status = CodomainSelectionStatus.PHASE_LOCK_FAILED
        winner = None
        critical = ("phase_lock_audit_gate_failed",)
    elif selected == "NORMAL_OR_COMPETING_CODOMAIN":
        status = CodomainSelectionStatus.COHERENCE_INSUFFICIENT
        winner = None
        critical = ("coherent_density_below_threshold",)
    else:
        status = CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED
        winner = None
        critical = (f"unknown_classification:{selected}",)

    audit_gates = {
        "admissibility_margin_positive": evaluation.admissibility_margin > 0,
        "phase_locked": evaluation.phase_locked,
        "coherent_density_above_threshold": (
            evaluation.coherent_density >= network.min_rho_coh
        ),
    }

    obligation_packet = _build_obligation_packet(
        regime="SUPERCONDUCTIVITY",
        status=status,
        critical=critical,
        evaluation_data={
            "admissibility_margin": evaluation.admissibility_margin,
            "phase_locked": evaluation.phase_locked,
            "coherent_density": evaluation.coherent_density,
            "max_phase_gap": evaluation.max_phase_gap,
            "total_defect_pressure": evaluation.total_defect_pressure,
        },
    )

    exports = {
        "SC_coherent_codomain_selected": int(
            status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED
        ),
        "SC_admissibility_margin_evaluated": 1,
    }
    for non_claim in PRESERVED_NON_CLAIMS:
        exports[non_claim] = 0

    return CodomainSelectionVerdict(
        regime="SUPERCONDUCTIVITY",
        status=status,
        winner_codomain=winner,
        admissibility_margin=evaluation.admissibility_margin,
        audit_gates=audit_gates,
        critical_fields=critical,
        obligation_packet=obligation_packet,
        exports=exports,
        reason=evaluation.reason,
    )


def _adjudicate_superfluidity_v4_state(
    state: Mapping[str, Any],
) -> CodomainSelectionVerdict:
    """Adjudicate a flat v4 SF audit-state and map it onto the common
    CodomainSelectionStatus taxonomy. Reproduces APF_SUPERFLUIDITY_IE_AUDIT_LADDER_v4;
    the SF-native v4 verdict id is preserved in critical_fields + the obligation
    packet's evaluation_data (sf_native_verdict)."""
    from apf.superfluidity_ie import evaluate_sf_audit_state, SFAuditVerdict

    av = evaluate_sf_audit_state(dict(state))
    margin = state.get("margin_to_fragmented")

    mapping = {
        SFAuditVerdict.SELECT_SUPERFLUID_STRUCTURAL: (
            CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED,
            "neutral_phase_coherent_superflow", ()),
        SFAuditVerdict.FRAGMENTED_WINS: (
            CodomainSelectionStatus.MARGIN_NONPOSITIVE, None, ("fragmented_wins",)),
        SFAuditVerdict.COHERENCE_INSUFFICIENT: (
            CodomainSelectionStatus.COHERENCE_INSUFFICIENT, None, ("coherence_insufficient",)),
        SFAuditVerdict.THERMAL_PRESSURE_OVERLOAD: (
            CodomainSelectionStatus.COHERENCE_INSUFFICIENT, None, ("thermal_pressure_overload",)),
        SFAuditVerdict.VORTEX_DEFECT_OVERLOAD: (
            CodomainSelectionStatus.COHERENCE_INSUFFICIENT, None, ("vortex_defect_overload",)),
        SFAuditVerdict.METASTABLE_HISTORY_LOCKED: (
            CodomainSelectionStatus.METASTABLE_HISTORY_LOCKED, None, ("metastable_history_locked",)),
        SFAuditVerdict.HOLD_EVIDENCE_REQUIRED: (
            CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED, None, ("hold_evidence_required",)),
        SFAuditVerdict.REFUSE_CHARGED_GAUGE_CONTAMINATION: (
            CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED, None,
            ("charged_gauge_contamination_route_to_superconductivity",)),
        SFAuditVerdict.REFUSE_NUMERIC_EXPORT: (
            CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED, None, ("numeric_export_refused",)),
    }
    status, winner, critical = mapping[av]

    audit_gates = {
        "phase_lock": bool(state.get("phase_lock")),
        "coherence_ok": state.get("coherence_score", 0.0) >= 0.70,
        "thermal_ok": (state.get("thermal_pressure", 0.0) < 0.70
                       and state.get("normal_fraction", 0.0) < 0.50),
        "vortex_ok": (state.get("vortex_pressure", 0.0) < 0.70
                      and state.get("vortex_defect_density", 0.0) < 0.50),
        "boundary_ok": (not state.get("metastable_history_locked")
                        and state.get("boundary_pressure", 0.0) < 0.70),
        "neutral_no_gauge": not (state.get("charged_gauge_contamination")
                                 or state.get("forbidden_sc_markers")),
        "no_numeric_export": not state.get("numeric_export_attempt"),
    }

    obligation_packet = _build_obligation_packet(
        regime="SUPERFLUIDITY",
        status=status,
        critical=critical,
        evaluation_data={
            "sf_native_verdict": av.value,
            "margin_to_fragmented": margin,
            "coherence_score": state.get("coherence_score"),
            "thermal_pressure": state.get("thermal_pressure"),
            "vortex_pressure": state.get("vortex_pressure"),
            "boundary_pressure": state.get("boundary_pressure"),
            "audit_ladder": "APF_SUPERFLUIDITY_IE_AUDIT_LADDER_v4",
        },
    )

    exports = {
        "SF_coherent_codomain_selected": int(
            status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED
        ),
        "SF_admissibility_margin_evaluated": 1,
        "SF_v4_audit_ladder_evaluated": 1,
    }
    for non_claim in PRESERVED_NON_CLAIMS:
        exports[non_claim] = 0

    return CodomainSelectionVerdict(
        regime="SUPERFLUIDITY",
        status=status,
        winner_codomain=winner,
        admissibility_margin=float(margin) if isinstance(margin, (int, float)) else None,
        audit_gates=audit_gates,
        critical_fields=critical,
        obligation_packet=obligation_packet,
        exports=exports,
        reason=f"superfluidity v4 audit verdict: {av.value}",
    )


def _adjudicate_superfluidity(
    network_state: Mapping[str, Any],
) -> CodomainSelectionVerdict:
    """Dispatch SF adjudication to apf.superfluidity_ie (neutral coherent-phase regime).

    Maps SFVerdict onto the common CodomainSelectionStatus taxonomy. SF-specific
    failure modes (circulation / vortex / normal-fraction) fold into the coarse
    common buckets; the SF-native detail is preserved in critical_fields + reason.
    Charged-gauge contamination is not an SF failure -- it is routed back to the
    SC adapter, reported as OPEN_EVIDENCE_REQUIRED with a redirect.

    A flat v4 audit-state input routes to the richer v4 audit-ladder path.
    """
    from apf.superfluidity_ie import (
        load_runtime_dict,
        evaluate_sf_codomain,
        SFVerdict,
        is_sf_audit_state,
    )

    if is_sf_audit_state(dict(network_state)):
        return _adjudicate_superfluidity_v4_state(dict(network_state))

    try:
        network, costs = load_runtime_dict(dict(network_state))
    except (KeyError, TypeError, ValueError) as exc:
        return CodomainSelectionVerdict(
            regime="SUPERFLUIDITY",
            status=CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED,
            winner_codomain=None,
            admissibility_margin=None,
            audit_gates={},
            critical_fields=("network_state_malformed",),
            obligation_packet={
                "obligation_kind": "network_state_malformed",
                "target_engine": ENGINE_NAME,
                "target_unit_id": "regime:SUPERFLUIDITY",
                "evidence_required": [
                    "well-formed network_state dict with nodes / edges / defects / costs",
                ],
                "current_status": "INVALID_INPUT",
                "recommended_next_action": (
                    "supply network state matching apf.superfluidity_ie.load_runtime_dict schema"
                ),
                "error_detail": f"{type(exc).__name__}: {exc}",
            },
            exports={k: 0 for k in PRESERVED_NON_CLAIMS},
            reason=f"network state load failed: {exc}",
        )

    evaluation = evaluate_sf_codomain(network, costs)
    sf_verdict = evaluation.verdict
    margin = evaluation.admissibility_margin

    if sf_verdict == SFVerdict.SF_PHASE_CODOMAIN:
        status = CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED
        winner = "neutral_phase_coherent_superflow"
        critical: Tuple[str, ...] = ()
    elif sf_verdict == SFVerdict.PHASE_LOCK_FAILED:
        status = CodomainSelectionStatus.PHASE_LOCK_FAILED
        winner = None
        critical = ("phase_lock_audit_gate_failed",)
    elif sf_verdict == SFVerdict.VISCOUS_FRAGMENTED_CODOMAIN:
        if margin <= 0:
            status = CodomainSelectionStatus.MARGIN_NONPOSITIVE
            critical = ("admissibility_margin_nonpositive",)
        else:
            status = CodomainSelectionStatus.COHERENCE_INSUFFICIENT
            critical = ("coherent_density_below_threshold",)
        winner = None
    elif sf_verdict == SFVerdict.CIRCULATION_QUANTIZATION_FAILED:
        status = CodomainSelectionStatus.COHERENCE_INSUFFICIENT
        winner = None
        critical = ("circulation_quantization_audit_gate_failed",)
    elif sf_verdict == SFVerdict.VORTEX_OVERLOADED:
        status = CodomainSelectionStatus.COHERENCE_INSUFFICIENT
        winner = None
        critical = ("vortex_defect_overload",)
    elif sf_verdict == SFVerdict.NORMAL_FRACTION_OVERLOADED:
        status = CodomainSelectionStatus.COHERENCE_INSUFFICIENT
        winner = None
        critical = ("normal_fraction_overload",)
    elif sf_verdict == SFVerdict.CHARGED_GAUGE_CONTAMINATION:
        status = CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED
        winner = None
        critical = ("charged_gauge_contamination_route_to_superconductivity",)
    else:
        status = CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED
        winner = None
        critical = (f"unknown_sf_verdict:{sf_verdict.value}",)

    audit_gates = {
        "admissibility_margin_positive": evaluation.admissibility_margin > 0,
        "phase_locked": evaluation.phase_locked,
        "circulation_quantized": evaluation.circulation_quantized,
        "normal_fraction_below_threshold": (
            evaluation.average_normal_fraction < network.normal_fraction_threshold
        ),
    }

    obligation_packet = _build_obligation_packet(
        regime="SUPERFLUIDITY",
        status=status,
        critical=critical,
        evaluation_data={
            "admissibility_margin": evaluation.admissibility_margin,
            "phase_locked": evaluation.phase_locked,
            "circulation_quantized": evaluation.circulation_quantized,
            "coherent_density": evaluation.coherent_density,
            "average_normal_fraction": evaluation.average_normal_fraction,
            "defect_pressure_total": evaluation.defect_pressure_total,
            "sf_native_verdict": sf_verdict.value,
        },
    )

    exports = {
        "SF_coherent_codomain_selected": int(
            status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED
        ),
        "SF_admissibility_margin_evaluated": 1,
    }
    for non_claim in PRESERVED_NON_CLAIMS:
        exports[non_claim] = 0

    return CodomainSelectionVerdict(
        regime="SUPERFLUIDITY",
        status=status,
        winner_codomain=winner,
        admissibility_margin=evaluation.admissibility_margin,
        audit_gates=audit_gates,
        critical_fields=critical,
        obligation_packet=obligation_packet,
        exports=exports,
        reason=f"superfluidity verdict: {sf_verdict.value}",
    )


# Registry-driven dispatch table (v24.3.62). Maps the registry's
# "runtime_dispatcher" name to the adjudicator function. Future regimes append
# one entry here alongside flipping runtime_available in REGIME_RUNTIME_REGISTRY.
_LASER_VERDICT_STATUS_MAP = {
    "SELECT_LASER_STRUCTURAL": "COHERENT_CODOMAIN_SELECTED",
    "FRAGMENTED_SPONTANEOUS_EMISSION_WINS": "MARGIN_NONPOSITIVE",
    "GAIN_INSUFFICIENT": "COHERENCE_INSUFFICIENT",
    "PHASE_LOCK_FAILED": "PHASE_LOCK_FAILED",
    "COHERENCE_INSUFFICIENT": "COHERENCE_INSUFFICIENT",
    "LOSS_PRESSURE_OVERLOAD": "COHERENCE_INSUFFICIENT",
    "NOISE_PRESSURE_OVERLOAD": "COHERENCE_INSUFFICIENT",
    "MODE_COMPETITION_LOCKED": "COHERENCE_INSUFFICIENT",
    "SATURATION_DEPLETION_OVERLOAD": "COHERENCE_INSUFFICIENT",
    "METASTABLE_HISTORY_LOCKED": "METASTABLE_HISTORY_LOCKED",
    "OPEN_EVIDENCE_REQUIRED": "OPEN_EVIDENCE_REQUIRED",
    "REFUSE_NUMERIC_EXPORT": "OPEN_EVIDENCE_REQUIRED",
    "REFUSE_MATERIAL_SPECIFIC_CAVITY_CLAIM": "OPEN_EVIDENCE_REQUIRED",
    "REFUSE_BEC_OR_SUPERCONDUCTIVITY_RELABEL": "OPEN_EVIDENCE_REQUIRED"
}


def _adjudicate_magnetism(network_state: Mapping[str, Any]) -> CodomainSelectionVerdict:
    """Adjudicate Magnetism via apf.magnetism_ie, mapping the native verdict onto the
    common CodomainSelectionStatus taxonomy. Native verdict preserved in the
    obligation packet's evaluation_data."""
    from apf.magnetism_ie import evaluate_magnetism_state
    result = evaluate_magnetism_state(dict(network_state))
    native = result.get("verdict")
    margin = result.get("margin")
    status_str = result.get("common_status") or "OPEN_EVIDENCE_REQUIRED"
    try:
        status = CodomainSelectionStatus(status_str)
    except ValueError:
        status = CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED
    winner = "magnetism_coherent_codomain" if status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED else None
    critical = () if status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED else (str(native).lower(),)
    obligation_packet = _build_obligation_packet(
        regime="MAGNETISM", status=status, critical=critical,
        evaluation_data={"native_verdict": native, "margin": margin,
                         "reason": result.get("reason"),
                         "regime_pack": "APF_IE_MAGNETISM_CODOMAIN_REGIME_v1"})
    exports = {"magnetism_coherent_codomain_selected": int(status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED),
               "magnetism_admissibility_margin_evaluated": 1}
    for non_claim in PRESERVED_NON_CLAIMS:
        exports[non_claim] = 0
    return CodomainSelectionVerdict(
        regime="MAGNETISM", status=status, winner_codomain=winner,
        admissibility_margin=float(margin) if isinstance(margin, (int, float)) else None,
        audit_gates={}, critical_fields=critical, obligation_packet=obligation_packet,
        exports=exports, reason=str(result.get("reason", "")))

def _adjudicate_bec(network_state: Mapping[str, Any]) -> CodomainSelectionVerdict:
    """Adjudicate Bose-Einstein condensation via apf.bec_ie, mapping the native verdict onto the
    common CodomainSelectionStatus taxonomy. Native verdict preserved in the
    obligation packet's evaluation_data."""
    from apf.bec_ie import evaluate_bec_state
    result = evaluate_bec_state(dict(network_state))
    native = result.get("verdict")
    margin = result.get("margin")
    status_str = result.get("common_status") or "OPEN_EVIDENCE_REQUIRED"
    try:
        status = CodomainSelectionStatus(status_str)
    except ValueError:
        status = CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED
    winner = "bec_coherent_codomain" if status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED else None
    critical = () if status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED else (str(native).lower(),)
    obligation_packet = _build_obligation_packet(
        regime="BOSE_EINSTEIN_CONDENSATION", status=status, critical=critical,
        evaluation_data={"native_verdict": native, "margin": margin,
                         "reason": result.get("reason"),
                         "regime_pack": "APF_IE_BEC_CODOMAIN_REGIME_v1"})
    exports = {"bec_coherent_codomain_selected": int(status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED),
               "bec_admissibility_margin_evaluated": 1}
    for non_claim in PRESERVED_NON_CLAIMS:
        exports[non_claim] = 0
    return CodomainSelectionVerdict(
        regime="BOSE_EINSTEIN_CONDENSATION", status=status, winner_codomain=winner,
        admissibility_margin=float(margin) if isinstance(margin, (int, float)) else None,
        audit_gates={}, critical_fields=critical, obligation_packet=obligation_packet,
        exports=exports, reason=str(result.get("reason", "")))

def _adjudicate_laser_coherence(network_state: Mapping[str, Any]) -> CodomainSelectionVerdict:
    """Adjudicate Laser coherence via apf.laser_coherence_ie, mapping the native verdict onto the
    common CodomainSelectionStatus taxonomy. Native verdict preserved in the
    obligation packet's evaluation_data."""
    from apf.laser_coherence_ie import evaluate_from_dict
    result = evaluate_from_dict(dict(network_state))
    native = result.get("verdict")
    margin = result.get("admissibility_margin")
    status_str = _LASER_VERDICT_STATUS_MAP.get(native, "OPEN_EVIDENCE_REQUIRED")
    try:
        status = CodomainSelectionStatus(status_str)
    except ValueError:
        status = CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED
    winner = "laser_coherence_coherent_codomain" if status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED else None
    critical = () if status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED else (str(native).lower(),)
    obligation_packet = _build_obligation_packet(
        regime="LASER_COHERENCE", status=status, critical=critical,
        evaluation_data={"native_verdict": native, "margin": margin,
                         "reason": result.get("reason"),
                         "regime_pack": "APF_IE_LASER_COHERENCE_CODOMAIN_REGIME_v1"})
    exports = {"laser_coherence_coherent_codomain_selected": int(status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED),
               "laser_coherence_admissibility_margin_evaluated": 1}
    for non_claim in PRESERVED_NON_CLAIMS:
        exports[non_claim] = 0
    return CodomainSelectionVerdict(
        regime="LASER_COHERENCE", status=status, winner_codomain=winner,
        admissibility_margin=float(margin) if isinstance(margin, (int, float)) else None,
        audit_gates={}, critical_fields=critical, obligation_packet=obligation_packet,
        exports=exports, reason=str(result.get("reason", "")))

def _adjudicate_synchronization(network_state: Mapping[str, Any]) -> CodomainSelectionVerdict:
    """Adjudicate Synchronization via apf.synchronization_ie, mapping the native verdict onto the
    common CodomainSelectionStatus taxonomy. Native verdict preserved in the
    obligation packet's evaluation_data."""
    from apf.synchronization_ie import evaluate_synchronization_payload
    result = evaluate_synchronization_payload(dict(network_state))
    native = result.get("verdict")
    margin = result.get("margin")
    status_str = result.get("common_status") or "OPEN_EVIDENCE_REQUIRED"
    try:
        status = CodomainSelectionStatus(status_str)
    except ValueError:
        status = CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED
    winner = "synchronization_coherent_codomain" if status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED else None
    critical = () if status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED else (str(native).lower(),)
    obligation_packet = _build_obligation_packet(
        regime="SYNCHRONIZATION", status=status, critical=critical,
        evaluation_data={"native_verdict": native, "margin": margin,
                         "reason": result.get("reason"),
                         "regime_pack": "APF_IE_SYNCHRONIZATION_CODOMAIN_REGIME_v1"})
    exports = {"synchronization_coherent_codomain_selected": int(status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED),
               "synchronization_admissibility_margin_evaluated": 1}
    for non_claim in PRESERVED_NON_CLAIMS:
        exports[non_claim] = 0
    return CodomainSelectionVerdict(
        regime="SYNCHRONIZATION", status=status, winner_codomain=winner,
        admissibility_margin=float(margin) if isinstance(margin, (int, float)) else None,
        audit_gates={}, critical_fields=critical, obligation_packet=obligation_packet,
        exports=exports, reason=str(result.get("reason", "")))

def _adjudicate_topological_order(network_state: Mapping[str, Any]) -> CodomainSelectionVerdict:
    """Adjudicate Topological order via apf.topological_order_ie, mapping the
    native verdict onto the common CodomainSelectionStatus taxonomy. Native
    verdict preserved in the obligation packet's evaluation_data."""
    from apf.topological_order_ie import evaluate_topological_order_payload
    result = evaluate_topological_order_payload(dict(network_state))
    native = result.get("verdict")
    margin = result.get("margin")
    status_str = result.get("common_status") or "OPEN_EVIDENCE_REQUIRED"
    try:
        status = CodomainSelectionStatus(status_str)
    except ValueError:
        status = CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED
    winner = "topological_order_coherent_codomain" if status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED else None
    critical = () if status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED else (str(native).lower(),)
    obligation_packet = _build_obligation_packet(
        regime="TOPOLOGICAL_ORDER", status=status, critical=critical,
        evaluation_data={"native_verdict": native, "margin": margin,
                         "reason": result.get("reason"),
                         "regime_pack": "APF_IE_TOPOLOGICAL_ORDER_CODOMAIN_REGIME_v1"})
    exports = {"topological_order_coherent_codomain_selected": int(status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED),
               "topological_order_admissibility_margin_evaluated": 1}
    for non_claim in PRESERVED_NON_CLAIMS:
        exports[non_claim] = 0
    return CodomainSelectionVerdict(
        regime="TOPOLOGICAL_ORDER", status=status, winner_codomain=winner,
        admissibility_margin=float(margin) if isinstance(margin, (int, float)) else None,
        audit_gates={}, critical_fields=critical, obligation_packet=obligation_packet,
        exports=exports, reason=str(result.get("reason", "")))

_REGIME_DISPATCHERS = {
    "_adjudicate_superconductivity": _adjudicate_superconductivity,
    "_adjudicate_superfluidity": _adjudicate_superfluidity,
    "_adjudicate_magnetism": _adjudicate_magnetism,
    "_adjudicate_bec": _adjudicate_bec,
    "_adjudicate_laser_coherence": _adjudicate_laser_coherence,
    "_adjudicate_synchronization": _adjudicate_synchronization,
    "_adjudicate_topological_order": _adjudicate_topological_order,
}


def _build_obligation_packet(
    regime: str,
    status: CodomainSelectionStatus,
    critical: Tuple[str, ...],
    evaluation_data: Mapping[str, Any],
) -> Dict[str, Any]:
    """Build an obligation packet in the meta-schema shape (per Reference doc Q3).

    Common fields: obligation_kind, target_engine, target_unit_id, evidence_required,
    current_status, recommended_next_action. Engine-specific evidence_required content.
    """
    if status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED:
        return {
            "obligation_kind": "no_obligation",
            "target_engine": ENGINE_NAME,
            "target_unit_id": f"regime:{regime}",
            "evidence_required": [],
            "current_status": status.value,
            "recommended_next_action": "none -- coherent codomain selected with all audit gates passing",
            "evaluation_data": dict(evaluation_data),
        }

    if status == CodomainSelectionStatus.MARGIN_NONPOSITIVE:
        return {
            "obligation_kind": "reduce_defect_pressure_or_lower_coherent_cost",
            "target_engine": ENGINE_NAME,
            "target_unit_id": f"regime:{regime}",
            "evidence_required": [
                "interface_network with reduced thermal/gauge/disorder/competition/boundary/vortex defects",
                "OR cost ledger with C(R_coherent) < current value",
            ],
            "current_status": status.value,
            "recommended_next_action": (
                "supply interface network with admissibility margin S = C(R_N) - C(R_C) - Pi > 0"
            ),
            "evaluation_data": dict(evaluation_data),
        }

    if status == CodomainSelectionStatus.PHASE_LOCK_FAILED:
        return {
            "obligation_kind": "tighten_phase_coupling_across_edges",
            "target_engine": ENGINE_NAME,
            "target_unit_id": f"regime:{regime}",
            "evidence_required": [
                "interface_network with max phase gap below epsilon_phi on all coherent edges",
            ],
            "current_status": status.value,
            "recommended_next_action": (
                "reduce phase fragmentation; ensure |phi_a - phi_b| <= epsilon_phi for all edges"
            ),
            "evaluation_data": dict(evaluation_data),
        }

    if status == CodomainSelectionStatus.COHERENCE_INSUFFICIENT:
        return {
            "obligation_kind": "increase_coherent_density",
            "target_engine": ENGINE_NAME,
            "target_unit_id": f"regime:{regime}",
            "evidence_required": [
                "interface_network with coherent density rho >= min_rho_coh threshold",
            ],
            "current_status": status.value,
            "recommended_next_action": (
                "increase node coherence_sigma values OR reduce min_rho_coh threshold per audit policy"
            ),
            "evaluation_data": dict(evaluation_data),
        }

    if status == CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED:
        return {
            "obligation_kind": "supply_runtime_evaluator_or_network_state",
            "target_engine": ENGINE_NAME,
            "target_unit_id": f"regime:{regime}",
            "evidence_required": [
                "runtime evaluator module for the regime",
                "audit-ladder fixture networks",
                "interface_network state dict",
            ],
            "current_status": status.value,
            "recommended_next_action": "see REGIME_RUNTIME_REGISTRY for which evidence is missing",
            "evaluation_data": dict(evaluation_data),
        }

    return {
        "obligation_kind": "unknown",
        "target_engine": ENGINE_NAME,
        "target_unit_id": f"regime:{regime}",
        "evidence_required": [],
        "current_status": status.value,
        "recommended_next_action": "see critical_fields",
        "evaluation_data": dict(evaluation_data),
    }


def _unknown_regime_verdict(regime: str) -> CodomainSelectionVerdict:
    return CodomainSelectionVerdict(
        regime=regime,
        status=CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED,
        winner_codomain=None,
        admissibility_margin=None,
        audit_gates={},
        critical_fields=("regime_not_in_registry",),
        obligation_packet={
            "obligation_kind": "regime_not_registered",
            "target_engine": ENGINE_NAME,
            "target_unit_id": f"regime:{regime}",
            "evidence_required": ["regime added to extended-regimes registry"],
            "current_status": "UNKNOWN_REGIME",
            "recommended_next_action": (
                "see APF_IE_EXTENDED_COHERENT_PHASE_REGIMES_v1 registry; "
                "register new regime via Reference doc Session 6+ workflow"
            ),
        },
        exports={k: 0 for k in PRESERVED_NON_CLAIMS},
        reason=f"regime {regime!r} not in REGIME_RUNTIME_REGISTRY",
    )


def _no_runtime_verdict(
    regime: str,
    regime_info: Mapping[str, Any],
) -> CodomainSelectionVerdict:
    return CodomainSelectionVerdict(
        regime=regime,
        status=CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED,
        winner_codomain=None,
        admissibility_margin=None,
        audit_gates={},
        critical_fields=("runtime_evaluator_missing", "audit_ladder_fixtures_missing"),
        obligation_packet={
            "obligation_kind": "runtime_evaluator_missing",
            "target_engine": ENGINE_NAME,
            "target_unit_id": f"regime:{regime}",
            "evidence_required": [
                "runtime evaluator module (per-regime analog of apf.superconductivity_ie)",
                "audit-ladder fixture networks (positive / fragmented / overloaded analogs)",
                "per-regime admissibility-margin specialization",
            ],
            "current_status": "STRUCTURAL_TYPED_ONLY",
            "recommended_next_action": (
                f"build apf/{regime.lower()}_ie.py paralleling apf/superconductivity_ie.py; "
                "ship audit-ladder fixtures; specialize admissibility margin"
            ),
        },
        exports={k: 0 for k in PRESERVED_NON_CLAIMS},
        reason=(
            f"regime {regime} is registered at structural grade but has no runtime evaluator; "
            "see Reference - APF Interface Engine Family Architecture Session 6+"
        ),
    )


def _network_missing_verdict(regime: str) -> CodomainSelectionVerdict:
    return CodomainSelectionVerdict(
        regime=regime,
        status=CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED,
        winner_codomain=None,
        admissibility_margin=None,
        audit_gates={},
        critical_fields=("network_state_missing",),
        obligation_packet={
            "obligation_kind": "network_state_missing",
            "target_engine": ENGINE_NAME,
            "target_unit_id": f"regime:{regime}",
            "evidence_required": ["interface_network state dict (nodes / edges / defects / costs)"],
            "current_status": "MISSING_INPUT",
            "recommended_next_action": (
                "call adjudicate_codomain_competition with network_state argument"
            ),
        },
        exports={k: 0 for k in PRESERVED_NON_CLAIMS},
        reason="network_state argument required for adjudication",
    )


# ---------------------------------------------------------------------------
# Bank checks (audit-first discipline; at least one per Tier 2 engine)
# ---------------------------------------------------------------------------

# Embedded test fixtures (parallel to SC v5 audit-ladder pattern; minimal)
_SC_POSITIVE_NETWORK: Dict[str, Any] = {
    "epsilon_phi": 0.2,
    "min_rho_coh": 0.5,
    "winding_sector_n": 1,
    "flux_sector_phi": 1.0,
    "nodes": [
        {"node_id": "a", "capacity_C": 10.0, "phase_phi": 0.00,
         "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
        {"node_id": "b", "capacity_C": 10.0, "phase_phi": 0.04,
         "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
        {"node_id": "c", "capacity_C": 10.0, "phase_phi": 0.08,
         "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
        {"node_id": "d", "capacity_C": 10.0, "phase_phi": 0.03,
         "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
    ],
    "edges": [["a", "b"], ["b", "c"], ["c", "d"], ["d", "a"]],
    "defects": {"thermal": 0.15, "gauge": 0.1, "disorder": 0.1,
                "competition": 0.05, "boundary": 0.05, "vortex": 0.05},
    "costs": {"C_normal": 12.0, "C_superconducting": 5.0},
}

_SC_OVERLOADED_NETWORK: Dict[str, Any] = {
    "epsilon_phi": 0.2,
    "min_rho_coh": 0.5,
    "winding_sector_n": 1,
    "flux_sector_phi": 1.0,
    "nodes": [
        {"node_id": "a", "capacity_C": 10.0, "phase_phi": 0.00,
         "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
        {"node_id": "b", "capacity_C": 10.0, "phase_phi": 0.04,
         "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
    ],
    "edges": [["a", "b"]],
    "defects": {"thermal": 5.0, "gauge": 2.0, "disorder": 2.0,
                "competition": 1.0, "boundary": 1.0, "vortex": 1.0},
    "costs": {"C_normal": 12.0, "C_superconducting": 5.0},
}

# Superfluidity positive fixture (neutral coherent-phase; from
# APF_SUPERFLUIDITY_CODOMAIN_ADAPTER_INTEGRATION_v3/examples/sf_positive_network.json).
_SF_POSITIVE_NETWORK: Dict[str, Any] = {
    "nodes": [
        {"node_id": "a", "capacity_C": 1.0, "phase_phi": 0.00,
         "phase_stiffness_sigma": 0.96, "normal_fraction_eta": 0.03,
         "local_defect_pressure_Pi": 0.04},
        {"node_id": "b", "capacity_C": 1.0, "phase_phi": 0.05,
         "phase_stiffness_sigma": 0.94, "normal_fraction_eta": 0.04,
         "local_defect_pressure_Pi": 0.03},
        {"node_id": "c", "capacity_C": 1.0, "phase_phi": -0.03,
         "phase_stiffness_sigma": 0.95, "normal_fraction_eta": 0.05,
         "local_defect_pressure_Pi": 0.03},
    ],
    "edges": [["a", "b"], ["b", "c"], ["c", "a"]],
    "defects": {"thermal": 0.45, "vortex": 0.25, "boundary": 0.25,
                "normal_fraction": 0.15, "disorder": 0.05, "drive": 0.0},
    "epsilon_phi": 0.2,
    "circulation_ratio": 1.01,
    "circulation_tolerance": 0.05,
    "vortex_overload_threshold": 1.0,
    "normal_fraction_threshold": 0.55,
    "charged_gauge_flux_required": False,
    "costs": {"C_viscous": 9.0, "C_superfluid": 4.0},
}


def check_T_codomain_selection_engine_identity_P() -> Dict[str, Any]:
    """Engine identity contract: declares Tier 2 + family membership + role."""
    consistent = (
        ENGINE_NAME == "codomain_selection"
        and ENGINE_FAMILY == "APF_Interface_Engine"
        and ENGINE_TIER == 2
        and ENGINE_ROLE == "codomain_competition_adjudication"
        and len(REGIME_RUNTIME_REGISTRY) == 7
        and len(PRESERVED_NON_CLAIMS) == 4
        and "SUPERCONDUCTIVITY" in REGIME_RUNTIME_REGISTRY
        and REGIME_RUNTIME_REGISTRY["SUPERCONDUCTIVITY"]["runtime_available"] is True
    )
    return {
        "name": "check_T_codomain_selection_engine_identity_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_engine_identity" if consistent else "FAIL",
        "epistemic": "P_engine_identity",
        "summary": (
            "Codomain Selection Engine declares correct Tier 2 role + IE family membership; "
            "7 regimes registered, all 7 runtime-available (SUPERCONDUCTIVITY + SUPERFLUIDITY + "
            "MAGNETISM + BOSE_EINSTEIN_CONDENSATION + LASER_COHERENCE + SYNCHRONIZATION + "
            "TOPOLOGICAL_ORDER); coherent-phase family complete; 4 preserved non-claims per Reference doc."
        ),
        "dependencies": [
            "Reference - APF Interface Engine Family Architecture (2026-05-19).md",
            "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_IE_EXTENDED_COHERENT_PHASE_REGIMES_v1",
        ],
        "data": {
            "engine_name": ENGINE_NAME,
            "engine_tier": ENGINE_TIER,
            "engine_role": ENGINE_ROLE,
            "regimes_registered": len(REGIME_RUNTIME_REGISTRY),
            "runtime_available_regimes": [
                k for k, v in REGIME_RUNTIME_REGISTRY.items() if v["runtime_available"]
            ],
        },
    }


def check_T_codomain_selection_engine_entry_point_P() -> Dict[str, Any]:
    """Engine entry point: runs end-to-end on SC fixture + verdict shapes."""
    positive_verdict = adjudicate_codomain_competition(
        "SUPERCONDUCTIVITY", _SC_POSITIVE_NETWORK
    )
    overloaded_verdict = adjudicate_codomain_competition(
        "SUPERCONDUCTIVITY", _SC_OVERLOADED_NETWORK
    )
    sf_positive_verdict = adjudicate_codomain_competition(
        "SUPERFLUIDITY", _SF_POSITIVE_NETWORK
    )
    network_missing_verdict = adjudicate_codomain_competition("MAGNETISM", None)
    unknown_verdict = adjudicate_codomain_competition("UNKNOWN_REGIME_XYZ", None)

    consistent = (
        positive_verdict.status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED
        and positive_verdict.winner_codomain == "charged_phase_winding_flux"
        and positive_verdict.admissibility_margin is not None
        and positive_verdict.admissibility_margin > 0
        and overloaded_verdict.status == CodomainSelectionStatus.MARGIN_NONPOSITIVE
        and overloaded_verdict.winner_codomain is None
        and overloaded_verdict.admissibility_margin is not None
        and overloaded_verdict.admissibility_margin <= 0
        and sf_positive_verdict.status == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED
        and sf_positive_verdict.admissibility_margin is not None
        and sf_positive_verdict.admissibility_margin > 0
        and network_missing_verdict.status == CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED
        and "network_state_missing" in network_missing_verdict.critical_fields
        and unknown_verdict.status == CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED
        and "regime_not_in_registry" in unknown_verdict.critical_fields
    )
    return {
        "name": "check_T_codomain_selection_engine_entry_point_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_engine_entry_point" if consistent else "FAIL",
        "epistemic": "P_engine_entry_point",
        "summary": (
            "Engine entry point produces correct verdict status across 5 cases: SC positive -> "
            "COHERENT_CODOMAIN_SELECTED with positive margin; SC overloaded -> MARGIN_NONPOSITIVE; "
            "SF positive -> COHERENT_CODOMAIN_SELECTED via registry-driven dispatch; "
            "MAGNETISM with no network -> OPEN_EVIDENCE_REQUIRED with network_state_missing; "
            "unknown regime -> OPEN_EVIDENCE_REQUIRED with regime_not_in_registry."
        ),
        "dependencies": [
            "apf.superconductivity_ie.evaluate_sc_codomain",
            "apf.superconductivity_ie.load_network_dict",
        ],
        "data": {
            "positive_status": positive_verdict.status.value,
            "positive_margin": positive_verdict.admissibility_margin,
            "overloaded_status": overloaded_verdict.status.value,
            "overloaded_margin": overloaded_verdict.admissibility_margin,
            "network_missing_status": network_missing_verdict.status.value,
            "unknown_status": unknown_verdict.status.value,
        },
    }


def check_T_codomain_selection_engine_audit_first_P() -> Dict[str, Any]:
    """Audit-first discipline: per-regime non-claims preserved across all verdicts."""
    verdicts = [
        adjudicate_codomain_competition("SUPERCONDUCTIVITY", _SC_POSITIVE_NETWORK),
        adjudicate_codomain_competition("SUPERCONDUCTIVITY", _SC_OVERLOADED_NETWORK),
        adjudicate_codomain_competition("SUPERFLUIDITY", None),
        adjudicate_codomain_competition("MAGNETISM", None),
        adjudicate_codomain_competition("BOSE_EINSTEIN_CONDENSATION", None),
        adjudicate_codomain_competition("LASER_COHERENCE", None),
        adjudicate_codomain_competition("SYNCHRONIZATION", None),
        adjudicate_codomain_competition("TOPOLOGICAL_ORDER", None),
    ]
    non_claims_preserved = all(
        all(v.exports.get(nc, -1) == 0 for nc in PRESERVED_NON_CLAIMS)
        for v in verdicts
    )
    no_target_smuggled = all(
        v.obligation_packet.get("target_engine") == ENGINE_NAME
        for v in verdicts
    )
    consistent = non_claims_preserved and no_target_smuggled
    return {
        "name": "check_T_codomain_selection_engine_audit_first_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_engine_audit_first" if consistent else "FAIL",
        "epistemic": "P_engine_audit_first",
        "summary": (
            "Audit-first discipline preserved across all 8 verdict cases: "
            "numeric_critical_temperature / material_specific_prediction / highTc_solved / "
            "ab_initio_chemistry all = 0 in every export; no obligation packet smuggles target."
        ),
        "dependencies": [
            "APF_IE_COHERENT_PHASE_REGIME_MASTER_v1 (master pack non-claims)",
            "APF_IE_EXTENDED_COHERENT_PHASE_REGIMES_v1 (per-regime non-claims)",
        ],
        "data": {
            "verdicts_checked": len(verdicts),
            "non_claims_preserved": non_claims_preserved,
            "no_target_smuggled": no_target_smuggled,
        },
    }


# ---------------------------------------------------------------------------
# Bank registration
# ---------------------------------------------------------------------------

def register(registry=None):
    """Register Codomain Selection Engine checks into the bank registry."""
    checks = {
        "check_T_codomain_selection_engine_identity_P": check_T_codomain_selection_engine_identity_P,
        "check_T_codomain_selection_engine_entry_point_P": check_T_codomain_selection_engine_entry_point_P,
        "check_T_codomain_selection_engine_audit_first_P": check_T_codomain_selection_engine_audit_first_P,
    }
    if registry is None:
        return checks
    registry.update(checks)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {
        "check_T_codomain_selection_engine_identity_P": check_T_codomain_selection_engine_identity_P(),
        "check_T_codomain_selection_engine_entry_point_P": check_T_codomain_selection_engine_entry_point_P(),
        "check_T_codomain_selection_engine_audit_first_P": check_T_codomain_selection_engine_audit_first_P(),
    }
