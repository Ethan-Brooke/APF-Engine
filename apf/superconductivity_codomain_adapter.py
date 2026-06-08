"""APF Superconductivity Codomain Adapter.

Tier 4 sector adapter under the Codomain Selection Engine (Tier 2), per
``APF Reference Docs/Reference - APF Interface Engine Family Architecture (2026-05-19).md``
(Session 2 of the sequencing plan).

This is the first adapter built under the Codomain Selection Engine. It wraps
the ``apf.superconductivity_ie.SCEvaluation`` runtime evaluator into an
engine-readable payload via the
``apf.codomain_selection_engine.adjudicate_codomain_competition`` entry point.

What this adapter does
----------------------

* Holds a representative SC interface network state (positive coherent fixture
  from ``APF_SUPERCONDUCTIVITY_IE_AUDIT_LADDER_v5/examples/sc_positive_network.json``).
* Exposes ``build_codomain_adapter_payload()`` which adjudicates the network
  via the engine and returns an engine-axis payload dict.
* Carries the same audit-first non-claims as the underlying runtime
  evaluator + the engine.

What this adapter does at v24.3.32 (Session 3 of the architecture-review sequencing plan)
------------------------------------------------------------------------------------------

* Atlas live-runner contract declared. The adapter exports ``ATLAS_INPUT_ID``,
  ``ATLAS_ROUTE``, ``ATLAS_PAYLOAD_NAME``, ``ATLAS_AXIS = "CODOMAIN"``, and
  ``build_live_atlas_payload()``. The live runner discovers this adapter via
  ``pkgutil.iter_modules`` (which at v24.3.32 picks up both ``*_real_adapter`` and
  ``*_codomain_adapter`` names). The atlas's ``_compile_codomain_input`` dispatches
  the codomain-axis payload through ``adjudicate_codomain_competition`` rather than
  the route-axis movement-graph machinery.

* No empirical SC claim. The adapter operates on toy fixture networks for
  structural classification. Per the v5 audit ladder: positive / phase-
  fragmented / defect-overloaded fixtures test the audit-gate logic; they
  are NOT real material data.

Audit-first non-claims (preserved verbatim from the runtime evaluator)
----------------------------------------------------------------------

* ``numeric_critical_temperature = 0`` -- no Tc export
* ``material_specific_prediction = 0`` -- no per-material phase diagram
* ``highTc_solved = 0`` -- no high-Tc claim
* ``ab_initio_chemistry = 0`` -- no chemistry derived
* ``target_value_consumed = False`` -- no measured SC parameter consumed as input

References
----------

* ``apf.codomain_selection_engine`` -- Tier 2 engine this adapter targets.
* ``apf.superconductivity_ie`` -- runtime evaluator wrapped by this adapter.
* ``DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/APF_SUPERCONDUCTIVITY_IE_AUDIT_LADDER_v5/``
  -- source of the positive / fragmented / overloaded fixture networks.
* ``Reference - APF Interface Engine Family Architecture (2026-05-19).md``
  Session 2 -- specifies this adapter's role.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, Mapping, Tuple

from apf.codomain_selection_engine import (
    adjudicate_codomain_competition,
    CodomainSelectionStatus,
    CodomainSelectionVerdict,
    ENGINE_NAME,
    PRESERVED_NON_CLAIMS,
)


# ---------------------------------------------------------------------------
# Adapter identity (Tier 4 under Codomain Selection Engine)
# ---------------------------------------------------------------------------

ADAPTER_NAME = "superconductivity_codomain_adapter"
ADAPTER_ENGINE = ENGINE_NAME  # codomain_selection
ADAPTER_REGIME = "SUPERCONDUCTIVITY"
ADAPTER_TIER = 4


# ---------------------------------------------------------------------------
# Source network fixtures (verbatim from APF_SUPERCONDUCTIVITY_IE_AUDIT_LADDER_v5)
# ---------------------------------------------------------------------------

_POSITIVE_NETWORK: Dict[str, Any] = {
    "description": "Positive coherent SC toy network (verbatim from v5 audit ladder).",
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

_PHASE_FRAGMENTED_NETWORK: Dict[str, Any] = {
    "description": "Phase-fragmented SC network (fail-closed; from v5 audit ladder).",
    "epsilon_phi": 0.2,
    "min_rho_coh": 0.5,
    "winding_sector_n": 1,
    "flux_sector_phi": 1.0,
    "nodes": [
        {"node_id": "a", "capacity_C": 10.0, "phase_phi": 0.0,
         "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
        {"node_id": "b", "capacity_C": 10.0, "phase_phi": 0.7,
         "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
        {"node_id": "c", "capacity_C": 10.0, "phase_phi": 1.4,
         "coherence_sigma": 0.95, "defect_pressure_Pi": 0.05, "charge_q": 2.0},
    ],
    "edges": [["a", "b"], ["b", "c"]],
    "defects": {"thermal": 0.15, "gauge": 0.1, "disorder": 0.1,
                "competition": 0.05, "boundary": 0.05, "vortex": 0.05},
    "costs": {"C_normal": 12.0, "C_superconducting": 5.0},
}

_DEFECT_OVERLOADED_NETWORK: Dict[str, Any] = {
    "description": "Defect-overloaded SC network (fail-closed; from v5 audit ladder).",
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


# ---------------------------------------------------------------------------
# Adapter snapshot dataclass + payload builder
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class SuperconductivityCodomainAdapterSnapshot:
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
) -> SuperconductivityCodomainAdapterSnapshot:
    """Build the adapter payload by running SCEvaluation on a fixture network.

    Parameters
    ----------
    fixture : str
        One of "positive" / "phase_fragmented" / "defect_overloaded". Defaults to
        the positive fixture (representative coherent SC instance).
    """
    fixtures = {
        "positive": _POSITIVE_NETWORK,
        "phase_fragmented": _PHASE_FRAGMENTED_NETWORK,
        "defect_overloaded": _DEFECT_OVERLOADED_NETWORK,
    }
    if fixture not in fixtures:
        raise ValueError(
            f"unknown fixture {fixture!r}; choose from {sorted(fixtures)}"
        )
    network = fixtures[fixture]
    verdict = adjudicate_codomain_competition(ADAPTER_REGIME, network)
    return SuperconductivityCodomainAdapterSnapshot(
        adapter_name=ADAPTER_NAME,
        adapter_engine=ADAPTER_ENGINE,
        adapter_regime=ADAPTER_REGIME,
        adapter_tier=ADAPTER_TIER,
        source_network=network,
        verdict=verdict.to_dict(),
        target_value_consumed=False,
        preserved_non_claims=PRESERVED_NON_CLAIMS,
        external_evaluator_ledger={
            "runtime_module": "apf.superconductivity_ie",
            "runtime_function": "evaluate_sc_codomain",
            "audit_ladder_source": (
                "DOCTRINE_CONSEQUENCES_BUNDLE_LATEST_44/"
                "APF_SUPERCONDUCTIVITY_IE_AUDIT_LADDER_v5"
            ),
            "engine_module": "apf.codomain_selection_engine",
            "reference_doc": (
                "APF Reference Docs/Reference - APF Interface Engine "
                "Family Architecture (2026-05-19).md"
            ),
        },
    )


# ---------------------------------------------------------------------------
# Bank checks
# ---------------------------------------------------------------------------

def check_T_superconductivity_codomain_adapter_payload_contract_P() -> Dict[str, Any]:
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
        and payload["adapter_regime"] == "SUPERCONDUCTIVITY"
        and payload["adapter_tier"] == 4
        and payload["target_value_consumed"] is False
        and isinstance(payload["verdict"], dict)
        and "status" in payload["verdict"]
    )
    return {
        "name": "check_T_superconductivity_codomain_adapter_payload_contract_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_codomain_adapter_contract" if consistent else "FAIL",
        "epistemic": "P_codomain_adapter_contract",
        "summary": (
            "SC codomain adapter payload carries the required 9 fields with correct "
            "values: adapter identity (name/engine/regime/tier) + source_network + "
            "verdict + target_value_consumed=False + preserved_non_claims + external "
            "evaluator ledger."
        ),
        "dependencies": [
            "apf.codomain_selection_engine.adjudicate_codomain_competition",
            "apf.superconductivity_ie.evaluate_sc_codomain",
        ],
        "data": {
            "payload_keys": sorted(payload.keys()),
            "adapter_engine": payload["adapter_engine"],
            "adapter_tier": payload["adapter_tier"],
        },
    }


def check_T_superconductivity_codomain_adapter_verdict_consistent_P() -> Dict[str, Any]:
    """Adapter verdicts on the three v5 audit-ladder fixtures match expected classification."""
    positive = build_codomain_adapter_payload("positive")
    fragmented = build_codomain_adapter_payload("phase_fragmented")
    overloaded = build_codomain_adapter_payload("defect_overloaded")

    consistent = (
        positive.verdict["status"] == CodomainSelectionStatus.COHERENT_CODOMAIN_SELECTED.value
        and positive.verdict["winner_codomain"] == "charged_phase_winding_flux"
        and positive.verdict["admissibility_margin"] > 0
        and fragmented.verdict["status"] == CodomainSelectionStatus.PHASE_LOCK_FAILED.value
        and fragmented.verdict["winner_codomain"] is None
        and overloaded.verdict["status"] == CodomainSelectionStatus.MARGIN_NONPOSITIVE.value
        and overloaded.verdict["winner_codomain"] is None
        and overloaded.verdict["admissibility_margin"] <= 0
    )
    return {
        "name": "check_T_superconductivity_codomain_adapter_verdict_consistent_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_codomain_adapter_verdict_consistent" if consistent else "FAIL",
        "epistemic": "P_codomain_adapter_verdict_consistent",
        "summary": (
            "Adapter verdicts match v5 audit-ladder fixture expectations: "
            "positive -> COHERENT_CODOMAIN_SELECTED with positive margin; "
            "phase_fragmented -> PHASE_LOCK_FAILED; "
            "defect_overloaded -> MARGIN_NONPOSITIVE with nonpositive margin."
        ),
        "dependencies": [
            "APF_SUPERCONDUCTIVITY_IE_AUDIT_LADDER_v5/examples/*.json (fixture provenance)",
        ],
        "data": {
            "positive_status": positive.verdict["status"],
            "positive_margin": positive.verdict["admissibility_margin"],
            "fragmented_status": fragmented.verdict["status"],
            "overloaded_status": overloaded.verdict["status"],
            "overloaded_margin": overloaded.verdict["admissibility_margin"],
        },
    }


def check_T_superconductivity_codomain_adapter_audit_first_P() -> Dict[str, Any]:
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
        "name": "check_T_superconductivity_codomain_adapter_audit_first_P",
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


# ---------------------------------------------------------------------------
# Bank registration
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Atlas live-runner contract (v24.3.32 -- Session 3 of architecture-review plan)
# ---------------------------------------------------------------------------

ATLAS_INPUT_ID = "coherent_phase:superconductivity"
ATLAS_ROUTE = "coherent_phase:superconductivity"
ATLAS_PAYLOAD_NAME = "superconductivity_codomain_adapter_live"
ATLAS_AXIS = "CODOMAIN"


def build_live_atlas_payload() -> Dict[str, Any]:
    """Build the live codomain-axis atlas payload using the positive SC fixture.

    Returns a payload dict in the shape ``apf.interface_atlas._compile_codomain_input``
    expects: ``regime`` + ``network_state`` (where ``network_state`` is the dict
    ``apf.superconductivity_ie.load_network_dict`` consumes).

    The atlas's _compile_codomain_input dispatches this payload through
    ``adjudicate_codomain_competition`` to produce a codomain-axis verdict that the
    atlas's per-axis aggregation reads uniformly alongside route-axis adjudications.
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
# v24.3.32 atlas-contract bank check
# ---------------------------------------------------------------------------

def check_T_superconductivity_codomain_adapter_atlas_contract_P() -> Dict[str, Any]:
    """v24.3.32: adapter declares full atlas live-runner contract for the CODOMAIN axis.

    Verifies: ATLAS_INPUT_ID + ATLAS_ROUTE + ATLAS_PAYLOAD_NAME + ATLAS_AXIS
    attributes present with correct values; build_live_atlas_payload returns a
    well-shaped dict that the atlas's _compile_codomain_input can consume;
    the live payload routes through adjudicate_codomain_competition to a
    COHERENT_CODOMAIN_SELECTED verdict.
    """
    # Verify required attributes
    attrs_ok = (
        ATLAS_INPUT_ID == "coherent_phase:superconductivity"
        and ATLAS_ROUTE == "coherent_phase:superconductivity"
        and ATLAS_PAYLOAD_NAME == "superconductivity_codomain_adapter_live"
        and ATLAS_AXIS == "CODOMAIN"
    )

    # Verify payload shape
    payload = build_live_atlas_payload()
    payload_required = ("regime", "network_state", "adapter_name", "adapter_engine",
                        "axis", "target_value_consumed")
    payload_ok = all(k in payload for k in payload_required)
    payload_ok = payload_ok and payload["regime"] == "SUPERCONDUCTIVITY"
    payload_ok = payload_ok and payload["axis"] == "CODOMAIN"
    payload_ok = payload_ok and payload["target_value_consumed"] is False

    # Verify end-to-end atlas reading: payload -> _compile_codomain_input -> COHERENT verdict
    try:
        from apf.interface_atlas import (
            AtlasInput, AtlasInputKind, AxisKind, build_interface_atlas,
        )
        sc_input = AtlasInput(
            input_id="atlas_contract_test:superconductivity",
            kind=AtlasInputKind.CODOMAIN_PAYLOAD,
            route=ATLAS_ROUTE,
            claim_text=None,
            payload=payload,
            axis=AxisKind.CODOMAIN,
        )
        atlas = build_interface_atlas([sc_input], atlas_name="atlas_contract_test")
        sc_summary = atlas.route_summaries[0]
        atlas_ok = (
            sc_summary.axis == AxisKind.CODOMAIN
            and sc_summary.solver_status == "COHERENT_CODOMAIN_SELECTED"
            and sc_summary.export_global_P is True
            and atlas.axis_summary.get("CODOMAIN", {}).get("global_P_count", 0) == 1
        )
    except Exception as exc:
        atlas_ok = False
        atlas_error = f"{type(exc).__name__}: {exc}"
    else:
        atlas_error = None

    consistent = attrs_ok and payload_ok and atlas_ok
    return {
        "name": "check_T_superconductivity_codomain_adapter_atlas_contract_P",
        "consistent": consistent,
        "passed": consistent,
        "tier": 4,
        "status": "P_codomain_adapter_atlas_contract" if consistent else "FAIL",
        "epistemic": "P_codomain_adapter_atlas_contract",
        "summary": (
            "SC codomain adapter declares full atlas live-runner contract for the CODOMAIN "
            "axis: ATLAS_INPUT_ID + ATLAS_ROUTE + ATLAS_PAYLOAD_NAME + ATLAS_AXIS attributes "
            "correct; build_live_atlas_payload returns regime + network_state payload that "
            "the atlas's _compile_codomain_input dispatches through adjudicate_codomain_competition "
            "to a COHERENT_CODOMAIN_SELECTED verdict with export_global_P=True; atlas axis_summary "
            "shows CODOMAIN axis with global_P_count=1."
        ),
        "dependencies": [
            "apf.interface_atlas (v24.3.32 axis-typing refactor)",
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


def register(registry=None):
    """Register SC codomain adapter checks into the bank registry."""
    checks = {
        "check_T_superconductivity_codomain_adapter_payload_contract_P":
            check_T_superconductivity_codomain_adapter_payload_contract_P,
        "check_T_superconductivity_codomain_adapter_verdict_consistent_P":
            check_T_superconductivity_codomain_adapter_verdict_consistent_P,
        "check_T_superconductivity_codomain_adapter_audit_first_P":
            check_T_superconductivity_codomain_adapter_audit_first_P,
        "check_T_superconductivity_codomain_adapter_atlas_contract_P":
            check_T_superconductivity_codomain_adapter_atlas_contract_P,
    }
    if registry is None:
        return checks
    registry.update(checks)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {
        "check_T_superconductivity_codomain_adapter_payload_contract_P":
            check_T_superconductivity_codomain_adapter_payload_contract_P(),
        "check_T_superconductivity_codomain_adapter_verdict_consistent_P":
            check_T_superconductivity_codomain_adapter_verdict_consistent_P(),
        "check_T_superconductivity_codomain_adapter_audit_first_P":
            check_T_superconductivity_codomain_adapter_audit_first_P(),
        "check_T_superconductivity_codomain_adapter_atlas_contract_P":
            check_T_superconductivity_codomain_adapter_atlas_contract_P(),
    }
