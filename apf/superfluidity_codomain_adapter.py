"""APF Superfluidity Codomain Adapter.

Tier 4 sector adapter under the Codomain Selection Engine (Tier 2), per
``APF Reference Docs/Reference - APF Interface Engine Family Architecture (2026-05-19).md``.

Second adapter built under the Codomain Selection Engine, and the first
*neutral* coherent-phase regime: superfluidity is superconductivity with the
charged-gauge / winding / flux machinery removed. It wraps the
``apf.superfluidity_ie.evaluate_sf_codomain`` runtime evaluator into an
engine-readable payload via the
``apf.codomain_selection_engine.adjudicate_codomain_competition`` entry point.

Provenance: installed/conformed at v24.3.62 from sibling pack
``APF_SUPERFLUIDITY_CODOMAIN_ADAPTER_INTEGRATION_v3`` (audited 2026-05-24). The
sibling pack shipped a self-contained adapter that called its own evaluator
directly and emitted a pre-evaluated payload; on landing it was conformed to
the SC precedent so it (a) routes through the engine's
``adjudicate_codomain_competition`` and (b) emits the ``{regime, network_state}``
payload that ``apf.interface_atlas._compile_codomain_input`` re-dispatches.

What this adapter does
----------------------

* Holds representative SF interface-network fixtures (positive coherent /
  fragmented-viscous / vortex-overloaded / charged-gauge-contaminated) from the
  pack's ``examples/`` set.
* Exposes ``build_codomain_adapter_payload()`` which adjudicates a fixture
  network via the engine and returns an engine-axis payload.
* Exposes the atlas live-runner contract (ATLAS_INPUT_ID + ATLAS_ROUTE +
  ATLAS_PAYLOAD_NAME + ATLAS_AXIS = "CODOMAIN" + build_live_atlas_payload), so
  the live runner discovers it via ``pkgutil.iter_modules`` and the atlas
  dispatches the CODOMAIN-axis payload through ``adjudicate_codomain_competition``.

Audit-first non-claims (preserved verbatim from the runtime evaluator + engine)
------------------------------------------------------------------------------

* ``numeric_critical_temperature = 0`` -- no T_lambda export
* ``material_specific_prediction = 0`` -- no per-material phase diagram
* ``highTc_solved = 0`` -- not applicable; no high-Tc claim
* ``ab_initio_chemistry = 0`` -- no chemistry derived
* No critical velocity, helium phase diagram, or ultracold-gas phase diagram
* No reuse of superconductivity charged-gauge/flux machinery; charged
  phase-coherence is routed back to the SC adapter by design.
* ``target_value_consumed = False`` -- no measured SF parameter consumed as input

References
----------

* ``apf.codomain_selection_engine`` -- Tier 2 engine this adapter targets.
* ``apf.superfluidity_ie`` -- runtime evaluator wrapped by this adapter.
* ``apf.superconductivity_codomain_adapter`` -- charged sibling adapter (precedent).
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict, Mapping, Tuple

from apf.codomain_selection_engine import (
    adjudicate_codomain_competition,
    CodomainSelectionStatus,
    ENGINE_NAME,
    PRESERVED_NON_CLAIMS,
)


# ---------------------------------------------------------------------------
# Adapter identity (Tier 4 under Codomain Selection Engine)
# ---------------------------------------------------------------------------

ADAPTER_NAME = "superfluidity_codomain_adapter"
ADAPTER_ENGINE = ENGINE_NAME  # codomain_selection
ADAPTER_REGIME = "SUPERFLUIDITY"
ADAPTER_TIER = 4


# ---------------------------------------------------------------------------
# Source network fixtures (verbatim from APF_SUPERFLUIDITY_..._v3/examples/)
# ---------------------------------------------------------------------------

_POSITIVE_NETWORK: Dict[str, Any] = {
    "description": "Positive neutral superfluid toy network (from pack examples).",
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

_FRAGMENTED_NETWORK: Dict[str, Any] = {
    "description": "Fragmented viscous-wins network (margin nonpositive; from pack examples).",
    "nodes": [
        {"node_id": "a", "capacity_C": 1.0, "phase_phi": 0.00,
         "phase_stiffness_sigma": 0.60, "normal_fraction_eta": 0.25,
         "local_defect_pressure_Pi": 0.05},
        {"node_id": "b", "capacity_C": 1.0, "phase_phi": 0.04,
         "phase_stiffness_sigma": 0.58, "normal_fraction_eta": 0.26,
         "local_defect_pressure_Pi": 0.05},
    ],
    "edges": [["a", "b"]],
    "defects": {"thermal": 0.3, "vortex": 0.2, "boundary": 0.2,
                "normal_fraction": 0.2, "disorder": 0.05, "drive": 0.0},
    "epsilon_phi": 0.2,
    "circulation_ratio": 1.0,
    "circulation_tolerance": 0.05,
    "vortex_overload_threshold": 1.0,
    "normal_fraction_threshold": 0.55,
    "charged_gauge_flux_required": False,
    "costs": {"C_viscous": 5.0, "C_superfluid": 4.5},
}

_VORTEX_OVERLOADED_NETWORK: Dict[str, Any] = {
    "description": "Vortex-overloaded network despite positive margin (from pack examples).",
    "nodes": [
        {"node_id": "a", "capacity_C": 1.0, "phase_phi": 0.00,
         "phase_stiffness_sigma": 0.92, "normal_fraction_eta": 0.10,
         "local_defect_pressure_Pi": 0.02},
        {"node_id": "b", "capacity_C": 1.0, "phase_phi": 0.03,
         "phase_stiffness_sigma": 0.91, "normal_fraction_eta": 0.11,
         "local_defect_pressure_Pi": 0.02},
    ],
    "edges": [["a", "b"]],
    "defects": {"thermal": 0.2, "vortex": 1.2, "boundary": 0.2,
                "normal_fraction": 0.1, "disorder": 0.0, "drive": 0.0},
    "epsilon_phi": 0.2,
    "circulation_ratio": 1.0,
    "circulation_tolerance": 0.05,
    "vortex_overload_threshold": 1.0,
    "normal_fraction_threshold": 0.55,
    "charged_gauge_flux_required": False,
    "costs": {"C_viscous": 8.5, "C_superfluid": 4.0},
}

_GAUGE_CONTAMINATED_NETWORK: Dict[str, Any] = {
    "description": "Charged-gauge-contaminated network; routed back to SC adapter (from pack examples).",
    "nodes": [
        {"node_id": "a", "capacity_C": 1.0, "phase_phi": 0.00,
         "phase_stiffness_sigma": 0.95, "normal_fraction_eta": 0.05,
         "local_defect_pressure_Pi": 0.02},
        {"node_id": "b", "capacity_C": 1.0, "phase_phi": 0.02,
         "phase_stiffness_sigma": 0.95, "normal_fraction_eta": 0.05,
         "local_defect_pressure_Pi": 0.02},
    ],
    "edges": [["a", "b"]],
    "defects": {"thermal": 0.2, "vortex": 0.1, "boundary": 0.1,
                "normal_fraction": 0.1, "disorder": 0.0, "drive": 0.0},
    "epsilon_phi": 0.2,
    "circulation_ratio": 1.0,
    "circulation_tolerance": 0.05,
    "vortex_overload_threshold": 1.0,
    "normal_fraction_threshold": 0.55,
    "charged_gauge_flux_required": True,
    "costs": {"C_viscous": 9.0, "C_superfluid": 4.0},
}

_FIXTURES = {
    "positive": _POSITIVE_NETWORK,
    "fragmented": _FRAGMENTED_NETWORK,
    "vortex_overloaded": _VORTEX_OVERLOADED_NETWORK,
    "gauge_contaminated": _GAUGE_CONTAMINATED_NETWORK,
}


# ---------------------------------------------------------------------------
# Adapter snapshot dataclass + payload builder
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SuperfluidityCodomainAdapterSnapshot:
    """Snapshot of the adapter's payload destined for the Codomain Selection Engine."""
    adapter_name: str
    adapter_engine: str
    adapter_regime: str
    adapter_tier: int
    source_network: Mapping[str, Any]
    verdict: Mapping[str, Any]
    target_value_consumed: bool
    preserved_non_claims: Tuple[str, ...]
    external_evaluator_ledger: Mapping[str, str]

    def to_payload(self) -> Dict[str, Any]:
        return asdict(self)


def build_codomain_adapter_payload(
    fixture: str = "positive",
) -> SuperfluidityCodomainAdapterSnapshot:
    """Build the adapter payload by adjudicating a fixture network through the engine.

    Parameters
    ----------
    fixture : str
        One of "positive" / "fragmented" / "vortex_overloaded" /
        "gauge_contaminated". Defaults to the positive coherent fixture.
    """
    if fixture not in _FIXTURES:
        raise ValueError(
            f"unknown fixture {fixture!r}; choose from {sorted(_FIXTURES)}"
        )
    network = _FIXTURES[fixture]
    verdict = adjudicate_codomain_competition(ADAPTER_REGIME, network)
    return SuperfluidityCodomainAdapterSnapshot(
        adapter_name=ADAPTER_NAME,
        adapter_engine=ADAPTER_ENGINE,
        adapter_regime=ADAPTER_REGIME,
        adapter_tier=ADAPTER_TIER,
        source_network=network,
        verdict=verdict.to_dict(),
        target_value_consumed=False,
        preserved_non_claims=PRESERVED_NON_CLAIMS,
        external_evaluator_ledger={
            "runtime_module": "apf.superfluidity_ie",
            "runtime_function": "evaluate_sf_codomain",
            "pack_source": "APF_SUPERFLUIDITY_CODOMAIN_ADAPTER_INTEGRATION_v3",
            "engine_module": "apf.codomain_selection_engine",
            "reference_doc": (
                "APF Reference Docs/Reference - APF Interface Engine "
                "Family Architecture (2026-05-19).md"
            ),
        },
    )


# ---------------------------------------------------------------------------
# Atlas live-runner contract (CODOMAIN axis)
# ---------------------------------------------------------------------------

ATLAS_INPUT_ID = "coherent_phase:superfluidity"
ATLAS_ROUTE = "coherent_phase:superfluidity"
ATLAS_PAYLOAD_NAME = "superfluidity_codomain_adapter_live"
ATLAS_AXIS = "CODOMAIN"


def build_live_atlas_payload() -> Dict[str, Any]:
    """Build the live codomain-axis atlas payload using the positive SF fixture.

    Returns a payload dict in the shape ``apf.interface_atlas._compile_codomain_input``
    expects: ``regime`` + ``network_state`` (the dict
    ``apf.superfluidity_ie.load_runtime_dict`` consumes). The atlas dispatches
    this through ``adjudicate_codomain_competition`` to a codomain-axis verdict
    read uniformly alongside route-axis adjudications.
    """
    return {
        "regime": ADAPTER_REGIME,
        "network_state": _POSITIVE_NETWORK,
        "adapter_name": ADAPTER_NAME,
        "adapter_engine": ADAPTER_ENGINE,
        "adapter_tier": ADAPTER_TIER,
        "axis": ATLAS_AXIS,
        "target_value_consumed": False,
        "preserved_non_claims": list(PRESERVED_NON_CLAIMS),
    }


# ---------------------------------------------------------------------------
# Bank checks
# ---------------------------------------------------------------------------

def check_T_superfluidity_codomain_adapter_payload_contract_P() -> Dict[str, Any]:
    """Adapter payload contract: required fields + correct types."""
    snap = build_codomain_adapter_payload("positive")
    payload = snap.to_payload()
    required = (
        "adapter_name", "adapter_engine", "adapter_regime", "adapter_tier",
        "source_network", "verdict", "target_value_consumed",
        "preserved_non_claims", "external_evaluator_ledger",
    )
    consistent = (
        all(k in payload for k in required)
        and payload["adapter_name"] == ADAPTER_NAME
        and payload["adapter_engine"] == ENGINE_NAME
        and payload["adapter_regime"] == "SUPERFLUIDITY"
        and payload["adapter_tier"] == 4
        and payload["target_value_consumed"] is False
        and isinstance(payload["verdict"], dict)
        and "status" in payload["verdict"]
    )
    return {
        "name": "check_T_superfluidity_codomain_adapter_payload_contract_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_codomain_adapter_contract" if consistent else "FAIL",
        "epistemic": "P_codomain_adapter_contract",
        "summary": (
            "SF codomain adapter payload carries the required 9 fields with correct "
            "values: adapter identity (name/engine/regime/tier) + source_network + "
            "verdict + target_value_consumed=False + preserved_non_claims + external "
            "evaluator ledger. Routes through the engine (not its own evaluator)."
        ),
        "dependencies": [
            "apf.codomain_selection_engine.adjudicate_codomain_competition",
            "apf.superfluidity_ie.evaluate_sf_codomain",
        ],
        "data": {
            "payload_keys": sorted(payload.keys()),
            "adapter_engine": payload["adapter_engine"],
            "adapter_tier": payload["adapter_tier"],
        },
    }


def check_T_superfluidity_codomain_adapter_verdict_consistent_P() -> Dict[str, Any]:
    """Adapter verdicts on the four fixtures match the expected engine classification."""
    positive = build_codomain_adapter_payload("positive")
    fragmented = build_codomain_adapter_payload("fragmented")
    overloaded = build_codomain_adapter_payload("vortex_overloaded")
    contaminated = build_codomain_adapter_payload("gauge_contaminated")

    consistent = (
        positive.verdict["status"] == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED.value
        and positive.verdict["winner_codomain"] == "neutral_phase_coherent_superflow"
        and positive.verdict["admissibility_margin"] is not None
        and positive.verdict["admissibility_margin"] > 0
        and fragmented.verdict["status"] == CodomainSelectionStatus.MARGIN_NONPOSITIVE.value
        and fragmented.verdict["winner_codomain"] is None
        and fragmented.verdict["admissibility_margin"] <= 0
        and overloaded.verdict["status"] == CodomainSelectionStatus.COHERENCE_INSUFFICIENT.value
        and overloaded.verdict["winner_codomain"] is None
        and "vortex_defect_overload" in overloaded.verdict["critical_fields"]
        and contaminated.verdict["status"] == CodomainSelectionStatus.OPEN_EVIDENCE_REQUIRED.value
        and contaminated.verdict["winner_codomain"] is None
        and any("charged_gauge" in cf for cf in contaminated.verdict["critical_fields"])
    )
    return {
        "name": "check_T_superfluidity_codomain_adapter_verdict_consistent_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_codomain_adapter_verdict_consistent" if consistent else "FAIL",
        "epistemic": "P_codomain_adapter_verdict_consistent",
        "summary": (
            "Adapter verdicts match fixture expectations through the engine: "
            "positive -> COHERENT_CODOMAIN_SELECTED with positive margin; "
            "fragmented -> MARGIN_NONPOSITIVE; vortex_overloaded -> "
            "COHERENCE_INSUFFICIENT (vortex_defect_overload); gauge_contaminated -> "
            "OPEN_EVIDENCE_REQUIRED routed back to the SC adapter."
        ),
        "dependencies": [
            "apf.codomain_selection_engine._adjudicate_superfluidity",
            "APF_SUPERFLUIDITY_CODOMAIN_ADAPTER_INTEGRATION_v3/examples/*.json (fixture provenance)",
        ],
        "data": {
            "positive_status": positive.verdict["status"],
            "positive_margin": positive.verdict["admissibility_margin"],
            "fragmented_status": fragmented.verdict["status"],
            "overloaded_status": overloaded.verdict["status"],
            "contaminated_status": contaminated.verdict["status"],
        },
    }


def check_T_superfluidity_codomain_adapter_audit_first_P() -> Dict[str, Any]:
    """Audit-first discipline: per-regime non-claims preserved + target not consumed."""
    snap = build_codomain_adapter_payload("positive")
    payload = snap.to_payload()
    verdict = payload["verdict"]
    exports = verdict.get("exports", {})

    non_claims_preserved = all(exports.get(nc, -1) == 0 for nc in PRESERVED_NON_CLAIMS)
    target_not_consumed = payload["target_value_consumed"] is False
    ledger_declared = (
        "runtime_module" in payload["external_evaluator_ledger"]
        and "reference_doc" in payload["external_evaluator_ledger"]
        and "engine_module" in payload["external_evaluator_ledger"]
    )
    consistent = non_claims_preserved and target_not_consumed and ledger_declared
    return {
        "name": "check_T_superfluidity_codomain_adapter_audit_first_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_codomain_adapter_audit_first" if consistent else "FAIL",
        "epistemic": "P_codomain_adapter_audit_first",
        "summary": (
            "Audit-first discipline preserved: numeric_critical_temperature + "
            "material_specific_prediction + highTc_solved + ab_initio_chemistry "
            "all = 0 in adapter export; target_value_consumed=False; external "
            "evaluator ledger declared with runtime_module + engine_module + "
            "reference_doc fields."
        ),
        "dependencies": [
            "apf.codomain_selection_engine.PRESERVED_NON_CLAIMS",
        ],
        "data": {
            "non_claims_preserved": non_claims_preserved,
            "target_not_consumed": target_not_consumed,
            "ledger_fields_declared": list(payload["external_evaluator_ledger"].keys()),
        },
    }


def check_T_superfluidity_codomain_adapter_atlas_contract_P() -> Dict[str, Any]:
    """Adapter declares full atlas live-runner contract for the CODOMAIN axis.

    Verifies ATLAS_INPUT_ID + ATLAS_ROUTE + ATLAS_PAYLOAD_NAME + ATLAS_AXIS
    attributes; build_live_atlas_payload returns a well-shaped {regime,
    network_state} dict that the atlas's _compile_codomain_input consumes; the
    live payload routes through adjudicate_codomain_competition to a
    COHERENT_CODOMAIN_SELECTED verdict on the CODOMAIN axis.
    """
    attrs_ok = (
        ATLAS_INPUT_ID == "coherent_phase:superfluidity"
        and ATLAS_ROUTE == "coherent_phase:superfluidity"
        and ATLAS_PAYLOAD_NAME == "superfluidity_codomain_adapter_live"
        and ATLAS_AXIS == "CODOMAIN"
    )

    payload = build_live_atlas_payload()
    payload_required = ("regime", "network_state", "adapter_name", "adapter_engine",
                        "axis", "target_value_consumed")
    payload_ok = all(k in payload for k in payload_required)
    payload_ok = payload_ok and payload["regime"] == "SUPERFLUIDITY"
    payload_ok = payload_ok and payload["axis"] == "CODOMAIN"
    payload_ok = payload_ok and payload["target_value_consumed"] is False

    try:
        from apf.interface_atlas import (
            AtlasInput, AtlasInputKind, AxisKind, build_interface_atlas,
        )
        sf_input = AtlasInput(
            input_id="atlas_contract_test:superfluidity",
            kind=AtlasInputKind.CODOMAIN_PAYLOAD,
            route=ATLAS_ROUTE,
            claim_text=None,
            payload=payload,
            axis=AxisKind.CODOMAIN,
        )
        atlas = build_interface_atlas([sf_input], atlas_name="atlas_contract_test_sf")
        sf_summary = atlas.route_summaries[0]
        atlas_ok = (
            sf_summary.axis == AxisKind.CODOMAIN
            and sf_summary.solver_status == "COHERENT_CODOMAIN_SELECTED"
            and sf_summary.export_global_P is True
            and atlas.axis_summary.get("CODOMAIN", {}).get("global_P_count", 0) == 1
        )
    except Exception as exc:
        atlas_ok = False
        atlas_error = f"{type(exc).__name__}: {exc}"
    else:
        atlas_error = None

    consistent = attrs_ok and payload_ok and atlas_ok
    return {
        "name": "check_T_superfluidity_codomain_adapter_atlas_contract_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_codomain_adapter_atlas_contract" if consistent else "FAIL",
        "epistemic": "P_codomain_adapter_atlas_contract",
        "summary": (
            "SF codomain adapter declares full atlas live-runner contract for the CODOMAIN "
            "axis: ATLAS_INPUT_ID + ATLAS_ROUTE + ATLAS_PAYLOAD_NAME + ATLAS_AXIS correct; "
            "build_live_atlas_payload returns regime + network_state that the atlas's "
            "_compile_codomain_input dispatches through adjudicate_codomain_competition to a "
            "COHERENT_CODOMAIN_SELECTED verdict with export_global_P=True; axis_summary shows "
            "CODOMAIN global_P_count=1."
        ),
        "dependencies": [
            "apf.interface_atlas (axis-typing refactor)",
            "apf.codomain_selection_engine.adjudicate_codomain_competition",
            "apf.interface_atlas_live_runner.discover_adapters",
        ],
        "data": {
            "attrs_ok": attrs_ok,
            "payload_ok": payload_ok,
            "atlas_ok": atlas_ok,
            "atlas_error": atlas_error,
            "ATLAS_INPUT_ID": ATLAS_INPUT_ID,
            "ATLAS_ROUTE": ATLAS_ROUTE,
            "ATLAS_PAYLOAD_NAME": ATLAS_PAYLOAD_NAME,
            "ATLAS_AXIS": ATLAS_AXIS,
        },
    }


import json as _json

# Seven APF_SUPERFLUIDITY_IE_AUDIT_LADDER_v4 fixtures, embedded verbatim. The
# v4 check below routes each through the engine and confirms the installed
# runtime reproduces the v4 verdict lattice (the post-integration audit fence).
_V4_AUDIT_FIXTURES = _json.loads(r"""[
  {
    "fixture_id": "sf_boundary_metastable",
    "expected_verdict": "METASTABLE_HISTORY_LOCKED",
    "state": {
      "atlas_axis": "CODOMAIN",
      "boundary_pressure": 0.81,
      "charge_sector": "neutral",
      "charged_gauge_contamination": false,
      "codomain_family": "neutral_phase",
      "coherence_score": 0.89,
      "forbidden_sc_markers": [],
      "fragmented_total_score": 9.7,
      "margin_to_fragmented": 3.6,
      "metastable_history_locked": true,
      "normal_fraction": 0.1,
      "numeric_export_attempt": false,
      "phase_lock": true,
      "regime_id": "superfluidity",
      "requested_exports": {},
      "superfluid_total_score": 6.1,
      "target_engine": "CODOMAIN_SELECTION",
      "thermal_pressure": 0.15,
      "vortex_defect_density": 0.08,
      "vortex_pressure": 0.1
    }
  },
  {
    "fixture_id": "sf_fragmented_viscous",
    "expected_verdict": "FRAGMENTED_WINS",
    "state": {
      "atlas_axis": "CODOMAIN",
      "boundary_pressure": 0.04,
      "charge_sector": "neutral",
      "charged_gauge_contamination": false,
      "codomain_family": "neutral_phase",
      "coherence_score": 0.82,
      "forbidden_sc_markers": [],
      "fragmented_total_score": 8.1,
      "margin_to_fragmented": -1.5,
      "metastable_history_locked": false,
      "normal_fraction": 0.12,
      "numeric_export_attempt": false,
      "phase_lock": true,
      "regime_id": "superfluidity",
      "requested_exports": {},
      "superfluid_total_score": 9.6,
      "target_engine": "CODOMAIN_SELECTION",
      "thermal_pressure": 0.2,
      "vortex_defect_density": 0.03,
      "vortex_pressure": 0.05
    }
  },
  {
    "fixture_id": "sf_gauge_contaminated",
    "expected_verdict": "REFUSE_CHARGED_GAUGE_CONTAMINATION",
    "state": {
      "atlas_axis": "CODOMAIN",
      "boundary_pressure": 0.02,
      "charge_sector": "neutral",
      "charged_gauge_contamination": true,
      "codomain_family": "neutral_phase",
      "coherence_score": 0.95,
      "forbidden_sc_markers": [
        "charged_condensate",
        "electromagnetic_flux_quantization",
        "Cooper_pair",
        "Meissner_sector",
        "SC_winding_sector"
      ],
      "fragmented_total_score": 10.0,
      "margin_to_fragmented": 5.0,
      "metastable_history_locked": false,
      "normal_fraction": 0.05,
      "numeric_export_attempt": false,
      "phase_lock": true,
      "regime_id": "superfluidity",
      "requested_exports": {},
      "superfluid_total_score": 5.0,
      "target_engine": "CODOMAIN_SELECTION",
      "thermal_pressure": 0.1,
      "vortex_defect_density": 0.02,
      "vortex_pressure": 0.06
    }
  },
  {
    "fixture_id": "sf_numeric_claim_attempt",
    "expected_verdict": "REFUSE_NUMERIC_EXPORT",
    "state": {
      "atlas_axis": "CODOMAIN",
      "boundary_pressure": 0.02,
      "charge_sector": "neutral",
      "charged_gauge_contamination": false,
      "codomain_family": "neutral_phase",
      "coherence_score": 0.93,
      "forbidden_sc_markers": [],
      "fragmented_total_score": 9.9,
      "margin_to_fragmented": 4.0,
      "metastable_history_locked": false,
      "normal_fraction": 0.04,
      "numeric_export_attempt": true,
      "phase_lock": true,
      "regime_id": "superfluidity",
      "requested_exports": {
        "SF_helium_phase_diagram": 1,
        "SF_numeric_T_lambda": 1,
        "SF_numeric_critical_velocity": 1
      },
      "superfluid_total_score": 5.9,
      "target_engine": "CODOMAIN_SELECTION",
      "thermal_pressure": 0.1,
      "vortex_defect_density": 0.03,
      "vortex_pressure": 0.06
    }
  },
  {
    "fixture_id": "sf_positive_phase_locked",
    "expected_verdict": "SELECT_SUPERFLUID_STRUCTURAL",
    "state": {
      "atlas_axis": "CODOMAIN",
      "boundary_pressure": 0.03,
      "charge_sector": "neutral",
      "charged_gauge_contamination": false,
      "codomain_family": "neutral_phase",
      "coherence_score": 0.94,
      "forbidden_sc_markers": [],
      "fragmented_total_score": 10.4,
      "margin_to_fragmented": 4.2,
      "metastable_history_locked": false,
      "normal_fraction": 0.08,
      "numeric_export_attempt": false,
      "phase_lock": true,
      "regime_id": "superfluidity",
      "requested_exports": {},
      "superfluid_total_score": 6.2,
      "target_engine": "CODOMAIN_SELECTION",
      "thermal_pressure": 0.12,
      "vortex_defect_density": 0.02,
      "vortex_pressure": 0.05
    }
  },
  {
    "fixture_id": "sf_thermal_overloaded",
    "expected_verdict": "THERMAL_PRESSURE_OVERLOAD",
    "state": {
      "atlas_axis": "CODOMAIN",
      "boundary_pressure": 0.03,
      "charge_sector": "neutral",
      "charged_gauge_contamination": false,
      "codomain_family": "neutral_phase",
      "coherence_score": 0.91,
      "forbidden_sc_markers": [],
      "fragmented_total_score": 9.2,
      "margin_to_fragmented": 3.2,
      "metastable_history_locked": false,
      "normal_fraction": 0.58,
      "numeric_export_attempt": false,
      "phase_lock": true,
      "regime_id": "superfluidity",
      "requested_exports": {},
      "superfluid_total_score": 6.0,
      "target_engine": "CODOMAIN_SELECTION",
      "thermal_pressure": 0.82,
      "vortex_defect_density": 0.05,
      "vortex_pressure": 0.08
    }
  },
  {
    "fixture_id": "sf_vortex_overloaded",
    "expected_verdict": "VORTEX_DEFECT_OVERLOAD",
    "state": {
      "atlas_axis": "CODOMAIN",
      "boundary_pressure": 0.08,
      "charge_sector": "neutral",
      "charged_gauge_contamination": false,
      "codomain_family": "neutral_phase",
      "coherence_score": 0.9,
      "forbidden_sc_markers": [],
      "fragmented_total_score": 9.3,
      "margin_to_fragmented": 3.5,
      "metastable_history_locked": false,
      "normal_fraction": 0.12,
      "numeric_export_attempt": false,
      "phase_lock": true,
      "regime_id": "superfluidity",
      "requested_exports": {},
      "superfluid_total_score": 5.8,
      "target_engine": "CODOMAIN_SELECTION",
      "thermal_pressure": 0.18,
      "vortex_defect_density": 0.61,
      "vortex_pressure": 0.84
    }
  }
]""")


def check_T_superfluidity_codomain_adapter_v4_audit_ladder_P() -> Dict[str, Any]:
    """v24.3.63: installed runtime reproduces the v4 audit-ladder verdict lattice.

    Routes all seven APF_SUPERFLUIDITY_IE_AUDIT_LADDER_v4 fixtures through the
    engine's adjudicate_codomain_competition and confirms each fixture's SF-native
    v4 verdict (carried in the obligation packet's evaluation_data) matches the
    pack's expected_verdict. This is the installed-diff audit: proof the landed
    runtime honors the full v4 fence, not just the coarse v2 runtime lattice.
    """
    results = {}
    all_match = True
    for fx in _V4_AUDIT_FIXTURES:
        verdict = adjudicate_codomain_competition(ADAPTER_REGIME, fx["state"])
        native = verdict.obligation_packet.get("evaluation_data", {}).get("sf_native_verdict")
        ok = native == fx["expected_verdict"]
        all_match = all_match and ok
        results[fx["fixture_id"]] = {"expected": fx["expected_verdict"], "got": native, "ok": ok}
    return {
        "name": "check_T_superfluidity_codomain_adapter_v4_audit_ladder_P",
        "consistent": all_match,
        "passed": all_match,
        "tier": 4,
        "status": "P_codomain_adapter_v4_audit_ladder" if all_match else "FAIL",
        "epistemic": "P_codomain_adapter_v4_audit_ladder",
        "summary": (
            "Installed SF runtime reproduces the v4 audit-ladder verdict lattice on all "
            "seven APF_SUPERFLUIDITY_IE_AUDIT_LADDER_v4 fixtures through the engine: "
            "positive -> SELECT_SUPERFLUID_STRUCTURAL; fragmented -> FRAGMENTED_WINS; "
            "thermal -> THERMAL_PRESSURE_OVERLOAD; vortex -> VORTEX_DEFECT_OVERLOAD; "
            "boundary -> METASTABLE_HISTORY_LOCKED; gauge -> REFUSE_CHARGED_GAUGE_CONTAMINATION; "
            "numeric -> REFUSE_NUMERIC_EXPORT."
        ),
        "dependencies": [
            "apf.superfluidity_ie.evaluate_sf_audit_state",
            "apf.codomain_selection_engine._adjudicate_superfluidity_v4_state",
            "APF_SUPERFLUIDITY_IE_AUDIT_LADDER_v4/fixtures/*.json (fixture provenance)",
        ],
        "data": {"fixtures": results, "fixture_count": len(_V4_AUDIT_FIXTURES)},
    }


# ---------------------------------------------------------------------------
# Bank registration
# ---------------------------------------------------------------------------

def register(registry=None):

    """Register SF codomain adapter checks into the bank registry."""
    checks = {
        "check_T_superfluidity_codomain_adapter_payload_contract_P":
            check_T_superfluidity_codomain_adapter_payload_contract_P,
        "check_T_superfluidity_codomain_adapter_verdict_consistent_P":
            check_T_superfluidity_codomain_adapter_verdict_consistent_P,
        "check_T_superfluidity_codomain_adapter_audit_first_P":
            check_T_superfluidity_codomain_adapter_audit_first_P,
        "check_T_superfluidity_codomain_adapter_atlas_contract_P":
            check_T_superfluidity_codomain_adapter_atlas_contract_P,
        "check_T_superfluidity_codomain_adapter_v4_audit_ladder_P":
            check_T_superfluidity_codomain_adapter_v4_audit_ladder_P,
    }
    if registry is None:
        return checks
    registry.update(checks)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {
        "check_T_superfluidity_codomain_adapter_payload_contract_P":
            check_T_superfluidity_codomain_adapter_payload_contract_P(),
        "check_T_superfluidity_codomain_adapter_verdict_consistent_P":
            check_T_superfluidity_codomain_adapter_verdict_consistent_P(),
        "check_T_superfluidity_codomain_adapter_audit_first_P":
            check_T_superfluidity_codomain_adapter_audit_first_P(),
        "check_T_superfluidity_codomain_adapter_atlas_contract_P":
            check_T_superfluidity_codomain_adapter_atlas_contract_P(),
        "check_T_superfluidity_codomain_adapter_v4_audit_ladder_P":
            check_T_superfluidity_codomain_adapter_v4_audit_ladder_P(),
    }
