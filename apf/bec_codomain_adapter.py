"""APF Bose-Einstein condensation Codomain Adapter (Tier 4 under Codomain Selection Engine).

Landed v24.3.64 from APF_IE_BEC_CODOMAIN_REGIME_v1 (sibling pack), conformed to the APF bank
convention: routes through the engine's adjudicate_codomain_competition and
carries dict-shaped bank checks. The runtime evaluator (apf.bec_ie) is installed
verbatim from the pack; this adapter wraps it for engine + atlas + bank. Charged
sibling precedent: apf.superconductivity_codomain_adapter.

Non-claims preserved: no numeric critical parameter, no material-specific
prediction, no ab-initio chemistry, no experimental result.
"""
from __future__ import annotations
import json as _json
from typing import Any, Dict

from apf.codomain_selection_engine import (
    adjudicate_codomain_competition,
    CodomainSelectionStatus,
    ENGINE_NAME,
    PRESERVED_NON_CLAIMS,
)

ADAPTER_NAME = "bec_codomain_adapter"
ADAPTER_ENGINE = ENGINE_NAME
ADAPTER_REGIME = "BOSE_EINSTEIN_CONDENSATION"
ADAPTER_TIER = 4

ATLAS_INPUT_ID = "coherent_phase:bec"
ATLAS_ROUTE = "coherent_phase:bec"
ATLAS_PAYLOAD_NAME = "bec_codomain_adapter_live"
ATLAS_AXIS = "CODOMAIN"

_FIXTURES = _json.loads(r"""[
  {
    "name": "three_dimensional_interacting_bec_structural_pass",
    "expected_verdict": "SELECT_BEC_STRUCTURAL",
    "network_state": {
      "cost_fragmented": 10.0,
      "cost_coherent": 5.0,
      "thermal_depletion_pressure": 0.2,
      "interaction_pressure": 0.2,
      "fragmentation_pressure": 0.1,
      "trap_boundary_pressure": 0.1,
      "phase_fluctuation_pressure": 0.1,
      "finite_size_pressure": 0.0,
      "dimensional_pressure": 0.0,
      "history_pressure": 0.1,
      "macroscopic_occupation": true,
      "phase_lock": true,
      "single_mode_dominance": true,
      "condensate_fraction_evidence": true,
      "symmetry_class": "O2",
      "dimension": 3.0,
      "interaction_class": "weak_repulsive"
    }
  },
  {
    "name": "two_dimensional_bkt_bec_like_structural_pass",
    "expected_verdict": "SELECT_BEC_STRUCTURAL",
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 4.0,
      "thermal_depletion_pressure": 0.2,
      "interaction_pressure": 0.1,
      "fragmentation_pressure": 0.0,
      "trap_boundary_pressure": 0.0,
      "phase_fluctuation_pressure": 0.2,
      "finite_size_pressure": 0.0,
      "dimensional_pressure": 0.1,
      "history_pressure": 0.0,
      "macroscopic_occupation": true,
      "phase_lock": true,
      "single_mode_dominance": true,
      "symmetry_class": "U1",
      "dimension": 2.0,
      "bkt_allowed": true
    }
  },
  {
    "name": "ideal_trap_mean_field_route_selected",
    "expected_verdict": "SELECT_BEC_STRUCTURAL",
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 4.0,
      "thermal_depletion_pressure": 0.2,
      "interaction_pressure": 0.0,
      "fragmentation_pressure": 0.0,
      "trap_boundary_pressure": 0.1,
      "phase_fluctuation_pressure": 0.1,
      "finite_size_pressure": 0.0,
      "dimensional_pressure": 0.0,
      "history_pressure": 0.0,
      "macroscopic_occupation": true,
      "phase_lock": true,
      "single_mode_dominance": true,
      "symmetry_class": "O2",
      "dimension": 3.0,
      "interaction_class": "ideal",
      "trap_class": "mean_field_trap"
    }
  },
  {
    "name": "thermal_gas_wins_margin_nonpositive",
    "expected_verdict": "THERMAL_GAS_WINS",
    "network_state": {
      "cost_fragmented": 4.0,
      "cost_coherent": 6.0,
      "thermal_depletion_pressure": 0.1,
      "interaction_pressure": 0.1,
      "fragmentation_pressure": 0.0,
      "trap_boundary_pressure": 0.0,
      "phase_fluctuation_pressure": 0.0,
      "symmetry_class": "O2",
      "dimension": 3.0,
      "macroscopic_occupation": true,
      "phase_lock": true,
      "single_mode_dominance": true
    }
  },
  {
    "name": "no_macroscopic_occupation_blocks_positive_margin",
    "expected_verdict": "MACROSCOPIC_OCCUPATION_INSUFFICIENT",
    "network_state": {
      "cost_fragmented": 12.0,
      "cost_coherent": 3.0,
      "thermal_depletion_pressure": 0.1,
      "interaction_pressure": 0.1,
      "fragmentation_pressure": 0.0,
      "trap_boundary_pressure": 0.0,
      "phase_fluctuation_pressure": 0.0,
      "symmetry_class": "O2",
      "dimension": 3.0,
      "macroscopic_occupation": false,
      "phase_lock": true,
      "single_mode_dominance": true
    }
  },
  {
    "name": "fragmented_condensate_refusal",
    "expected_verdict": "FRAGMENTED_CONDENSATE_REFUSAL",
    "network_state": {
      "cost_fragmented": 12.0,
      "cost_coherent": 3.0,
      "thermal_depletion_pressure": 0.1,
      "interaction_pressure": 0.1,
      "fragmentation_pressure": 2.0,
      "fragmentation_gate": 1.0,
      "fragmented_condensate_candidate": true,
      "trap_boundary_pressure": 0.0,
      "phase_fluctuation_pressure": 0.0,
      "symmetry_class": "O2",
      "dimension": 3.0,
      "macroscopic_occupation": true,
      "phase_lock": true,
      "single_mode_dominance": true
    }
  },
  {
    "name": "finite_size_rounded_hold",
    "expected_verdict": "FINITE_SIZE_ROUNDED_HOLD",
    "network_state": {
      "cost_fragmented": 12.0,
      "cost_coherent": 3.0,
      "thermal_depletion_pressure": 0.1,
      "interaction_pressure": 0.1,
      "fragmentation_pressure": 0.0,
      "trap_boundary_pressure": 0.0,
      "phase_fluctuation_pressure": 0.0,
      "finite_size_rounding": true,
      "symmetry_class": "O2",
      "dimension": 3.0,
      "macroscopic_occupation": true,
      "phase_lock": true,
      "single_mode_dominance": true
    }
  },
  {
    "name": "history_barrier_locked_despite_positive_margin",
    "expected_verdict": "METASTABLE_HISTORY_LOCKED",
    "network_state": {
      "cost_fragmented": 12.0,
      "cost_coherent": 5.0,
      "thermal_depletion_pressure": 0.1,
      "interaction_pressure": 0.1,
      "fragmentation_pressure": 0.0,
      "trap_boundary_pressure": 0.0,
      "phase_fluctuation_pressure": 0.0,
      "symmetry_class": "O2",
      "dimension": 3.0,
      "macroscopic_occupation": true,
      "phase_lock": true,
      "single_mode_dominance": true,
      "history_barrier_cleared": false
    }
  },
  {
    "name": "numeric_export_hard_refusal_precedes_margin",
    "expected_verdict": "REFUSE_NUMERIC_TC_EXPORT",
    "network_state": {
      "cost_fragmented": 100.0,
      "cost_coherent": 1.0,
      "numeric_export_attempt": true,
      "target_value_consumed": true,
      "attempted_export_value": "Tc = 500 nK",
      "symmetry_class": "O2",
      "dimension": 3.0
    }
  }
]""")
_POSITIVE_NETWORK = next(
    f["network_state"] for f in _FIXTURES
    if str(f.get("expected_verdict", "")).startswith("SELECT")
)


def build_codomain_adapter_payload(network_state=None) -> Dict[str, Any]:
    state = network_state if network_state is not None else _POSITIVE_NETWORK
    verdict = adjudicate_codomain_competition(ADAPTER_REGIME, state)
    return {
        "adapter_name": ADAPTER_NAME,
        "adapter_engine": ADAPTER_ENGINE,
        "adapter_regime": ADAPTER_REGIME,
        "adapter_tier": ADAPTER_TIER,
        "network_state": state,
        "verdict": verdict.to_dict(),
        "target_value_consumed": False,
        "preserved_non_claims": list(PRESERVED_NON_CLAIMS),
        "external_evaluator_ledger": {
            "runtime_module": "apf.bec_ie",
            "engine_module": "apf.codomain_selection_engine",
            "pack_source": "APF_IE_BEC_CODOMAIN_REGIME_v1",
        },
    }


def build_live_atlas_payload() -> Dict[str, Any]:
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


def check_T_bec_codomain_adapter_payload_contract_P() -> Dict[str, Any]:
    p = build_codomain_adapter_payload()
    required = ("adapter_name", "adapter_engine", "adapter_regime", "adapter_tier",
                "network_state", "verdict", "target_value_consumed",
                "preserved_non_claims", "external_evaluator_ledger")
    ok = (all(k in p for k in required) and p["adapter_engine"] == ENGINE_NAME
          and p["adapter_regime"] == "BOSE_EINSTEIN_CONDENSATION" and p["adapter_tier"] == 4
          and p["target_value_consumed"] is False and isinstance(p["verdict"], dict)
          and "status" in p["verdict"])
    return {"name": "check_T_bec_codomain_adapter_payload_contract_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_contract" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_contract",
            "summary": "Bose-Einstein condensation codomain adapter payload carries the required fields and routes through the engine.",
            "dependencies": ["apf.codomain_selection_engine.adjudicate_codomain_competition", "apf.bec_ie"],
            "data": {"keys": sorted(p.keys())}}


def check_T_bec_codomain_adapter_verdict_consistent_P() -> Dict[str, Any]:
    results = {}
    ok = True
    for fx in _FIXTURES:
        exp = fx.get("expected_verdict")
        if exp is None:
            continue
        v = adjudicate_codomain_competition(ADAPTER_REGIME, fx["network_state"])
        native = v.obligation_packet.get("evaluation_data", {}).get("native_verdict")
        m = (native == exp)
        ok = ok and m
        results[fx.get("name")] = {"expected": exp, "got": native, "ok": m}
    return {"name": "check_T_bec_codomain_adapter_verdict_consistent_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_verdict_consistent" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_verdict_consistent",
            "summary": "Installed Bose-Einstein condensation runtime reproduces every fixture verdict through the engine.",
            "dependencies": ["apf.codomain_selection_engine._adjudicate_bec"],
            "data": {"fixtures": results}}


def check_T_bec_codomain_adapter_audit_first_P() -> Dict[str, Any]:
    p = build_codomain_adapter_payload()
    exports = p["verdict"].get("exports", {})
    nc = all(exports.get(k, -1) == 0 for k in PRESERVED_NON_CLAIMS)
    led = ("runtime_module" in p["external_evaluator_ledger"]
           and "engine_module" in p["external_evaluator_ledger"])
    ok = nc and p["target_value_consumed"] is False and led
    return {"name": "check_T_bec_codomain_adapter_audit_first_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_audit_first" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_audit_first",
            "summary": "Audit-first non-claims preserved; target not consumed; evaluator ledger declared.",
            "dependencies": ["apf.codomain_selection_engine.PRESERVED_NON_CLAIMS"],
            "data": {"non_claims_preserved": nc}}


def check_T_bec_codomain_adapter_atlas_contract_P() -> Dict[str, Any]:
    attrs = (ATLAS_INPUT_ID == "coherent_phase:bec" and ATLAS_AXIS == "CODOMAIN")
    payload = build_live_atlas_payload()
    try:
        from apf.interface_atlas import (AtlasInput, AtlasInputKind, AxisKind, build_interface_atlas)
        ai = AtlasInput(input_id="atlas_contract_test:bec", kind=AtlasInputKind.CODOMAIN_PAYLOAD,
                        route=ATLAS_ROUTE, claim_text=None, payload=payload, axis=AxisKind.CODOMAIN)
        atlas = build_interface_atlas([ai], atlas_name="atlas_contract_test_bec")
        s = atlas.route_summaries[0]
        aok = (s.axis == AxisKind.CODOMAIN and s.solver_status == "COHERENT_CODOMAIN_SELECTED"
               and s.export_global_P is True
               and atlas.axis_summary.get("CODOMAIN", {}).get("global_P_count", 0) == 1)
        err = None
    except Exception as exc:
        aok = False
        err = f"{type(exc).__name__}: {exc}"
    ok = attrs and aok
    return {"name": "check_T_bec_codomain_adapter_atlas_contract_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_atlas_contract" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_atlas_contract",
            "summary": "Bose-Einstein condensation adapter declares the CODOMAIN atlas contract; live payload reaches COHERENT via the engine.",
            "dependencies": ["apf.interface_atlas", "apf.codomain_selection_engine.adjudicate_codomain_competition"],
            "data": {"attrs_ok": attrs, "atlas_ok": aok, "atlas_error": err}}


def register(registry=None):
    checks = {
        "check_T_bec_codomain_adapter_payload_contract_P": check_T_bec_codomain_adapter_payload_contract_P,
        "check_T_bec_codomain_adapter_verdict_consistent_P": check_T_bec_codomain_adapter_verdict_consistent_P,
        "check_T_bec_codomain_adapter_audit_first_P": check_T_bec_codomain_adapter_audit_first_P,
        "check_T_bec_codomain_adapter_atlas_contract_P": check_T_bec_codomain_adapter_atlas_contract_P,
    }
    if registry is None:
        return checks
    registry.update(checks)
    return registry


def run_all():
    return {k: v() for k, v in register().items()}
