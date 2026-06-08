"""APF Laser coherence Codomain Adapter (Tier 4 under Codomain Selection Engine).

Landed v24.3.64 from APF_IE_LASER_COHERENCE_CODOMAIN_REGIME_v1 (sibling pack), conformed to the APF bank
convention: routes through the engine's adjudicate_codomain_competition and
carries dict-shaped bank checks. The runtime evaluator (apf.laser_coherence_ie) is installed
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

ADAPTER_NAME = "laser_coherence_codomain_adapter"
ADAPTER_ENGINE = ENGINE_NAME
ADAPTER_REGIME = "LASER_COHERENCE"
ADAPTER_TIER = 4

ATLAS_INPUT_ID = "coherent_phase:laser_coherence"
ATLAS_ROUTE = "coherent_phase:laser_coherence"
ATLAS_PAYLOAD_NAME = "laser_coherence_codomain_adapter_live"
ATLAS_AXIS = "CODOMAIN"

_FIXTURES = _json.loads(r"""[
  {
    "name": "select_structural",
    "expected_verdict": "SELECT_LASER_STRUCTURAL",
    "network_state": {
      "independent_emission_cost": 4.0,
      "phase_locked_mode_cost": 1.2,
      "independent_emission_pressure": 0.2,
      "loss_pressure": 0.15,
      "spontaneous_noise_pressure": 0.08,
      "pump_noise_pressure": 0.07,
      "mode_competition_pressure": 0.05,
      "linewidth_phase_diffusion_pressure": 0.05,
      "saturation_depletion_pressure": 0.06,
      "cavity_boundary_pressure": 0.04,
      "history_pressure": 0.03,
      "gain_margin": 0.8,
      "phase_lock_residual": 0.01,
      "coherent_mode_fraction": 0.9,
      "history_barrier_cleared": true,
      "symmetry_class": "U1_phase",
      "dynamics_class": "driven_dissipative"
    }
  },
  {
    "name": "fragmented_wins",
    "expected_verdict": "FRAGMENTED_SPONTANEOUS_EMISSION_WINS",
    "network_state": {
      "independent_emission_cost": 1.0,
      "phase_locked_mode_cost": 1.5,
      "gain_margin": 0.4,
      "phase_lock_residual": 0.01,
      "coherent_mode_fraction": 0.8
    }
  },
  {
    "name": "gain_insufficient",
    "expected_verdict": "GAIN_INSUFFICIENT",
    "network_state": {
      "independent_emission_cost": 4.0,
      "phase_locked_mode_cost": 1.0,
      "gain_margin": -0.1
    }
  },
  {
    "name": "phase_lock_failed",
    "expected_verdict": "PHASE_LOCK_FAILED",
    "network_state": {
      "independent_emission_cost": 4.0,
      "phase_locked_mode_cost": 1.0,
      "gain_margin": 0.6,
      "phase_lock_residual": 0.2,
      "phase_lock_tolerance": 0.05
    }
  },
  {
    "name": "mode_competition_locked",
    "expected_verdict": "MODE_COMPETITION_LOCKED",
    "network_state": {
      "independent_emission_cost": 5.0,
      "phase_locked_mode_cost": 1.0,
      "gain_margin": 0.7,
      "phase_lock_residual": 0.01,
      "mode_competition_pressure": 1.4,
      "mode_competition_gate": 1.0
    }
  },
  {
    "name": "boundedness_audit_kpz_hold",
    "expected_verdict": "SELECT_LASER_STRUCTURAL",
    "network_state": {
      "independent_emission_cost": 4.0,
      "phase_locked_mode_cost": 1.0,
      "gain_margin": 0.8,
      "phase_lock_residual": 0.01,
      "boundedness_audit_passed": false
    }
  },
  {
    "name": "history_locked",
    "expected_verdict": "METASTABLE_HISTORY_LOCKED",
    "network_state": {
      "independent_emission_cost": 4.0,
      "phase_locked_mode_cost": 1.0,
      "gain_margin": 0.7,
      "phase_lock_residual": 0.01,
      "history_barrier_cleared": false
    }
  },
  {
    "name": "numeric_refusal",
    "expected_verdict": "REFUSE_NUMERIC_EXPORT",
    "network_state": {
      "independent_emission_cost": 4.0,
      "phase_locked_mode_cost": 1.0,
      "gain_margin": 0.7,
      "numeric_threshold_export_attempted": true
    }
  },
  {
    "name": "material_claim_refusal",
    "expected_verdict": "REFUSE_MATERIAL_SPECIFIC_CAVITY_CLAIM",
    "network_state": {
      "independent_emission_cost": 4.0,
      "phase_locked_mode_cost": 1.0,
      "gain_margin": 0.7,
      "material_or_cavity_specific_claim": true
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
            "runtime_module": "apf.laser_coherence_ie",
            "engine_module": "apf.codomain_selection_engine",
            "pack_source": "APF_IE_LASER_COHERENCE_CODOMAIN_REGIME_v1",
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


def check_T_laser_coherence_codomain_adapter_payload_contract_P() -> Dict[str, Any]:
    p = build_codomain_adapter_payload()
    required = ("adapter_name", "adapter_engine", "adapter_regime", "adapter_tier",
                "network_state", "verdict", "target_value_consumed",
                "preserved_non_claims", "external_evaluator_ledger")
    ok = (all(k in p for k in required) and p["adapter_engine"] == ENGINE_NAME
          and p["adapter_regime"] == "LASER_COHERENCE" and p["adapter_tier"] == 4
          and p["target_value_consumed"] is False and isinstance(p["verdict"], dict)
          and "status" in p["verdict"])
    return {"name": "check_T_laser_coherence_codomain_adapter_payload_contract_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_contract" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_contract",
            "summary": "Laser coherence codomain adapter payload carries the required fields and routes through the engine.",
            "dependencies": ["apf.codomain_selection_engine.adjudicate_codomain_competition", "apf.laser_coherence_ie"],
            "data": {"keys": sorted(p.keys())}}


def check_T_laser_coherence_codomain_adapter_verdict_consistent_P() -> Dict[str, Any]:
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
    return {"name": "check_T_laser_coherence_codomain_adapter_verdict_consistent_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_verdict_consistent" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_verdict_consistent",
            "summary": "Installed Laser coherence runtime reproduces every fixture verdict through the engine.",
            "dependencies": ["apf.codomain_selection_engine._adjudicate_laser_coherence"],
            "data": {"fixtures": results}}


def check_T_laser_coherence_codomain_adapter_audit_first_P() -> Dict[str, Any]:
    p = build_codomain_adapter_payload()
    exports = p["verdict"].get("exports", {})
    nc = all(exports.get(k, -1) == 0 for k in PRESERVED_NON_CLAIMS)
    led = ("runtime_module" in p["external_evaluator_ledger"]
           and "engine_module" in p["external_evaluator_ledger"])
    ok = nc and p["target_value_consumed"] is False and led
    return {"name": "check_T_laser_coherence_codomain_adapter_audit_first_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_audit_first" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_audit_first",
            "summary": "Audit-first non-claims preserved; target not consumed; evaluator ledger declared.",
            "dependencies": ["apf.codomain_selection_engine.PRESERVED_NON_CLAIMS"],
            "data": {"non_claims_preserved": nc}}


def check_T_laser_coherence_codomain_adapter_atlas_contract_P() -> Dict[str, Any]:
    attrs = (ATLAS_INPUT_ID == "coherent_phase:laser_coherence" and ATLAS_AXIS == "CODOMAIN")
    payload = build_live_atlas_payload()
    try:
        from apf.interface_atlas import (AtlasInput, AtlasInputKind, AxisKind, build_interface_atlas)
        ai = AtlasInput(input_id="atlas_contract_test:laser_coherence", kind=AtlasInputKind.CODOMAIN_PAYLOAD,
                        route=ATLAS_ROUTE, claim_text=None, payload=payload, axis=AxisKind.CODOMAIN)
        atlas = build_interface_atlas([ai], atlas_name="atlas_contract_test_laser_coherence")
        s = atlas.route_summaries[0]
        aok = (s.axis == AxisKind.CODOMAIN and s.solver_status == "COHERENT_CODOMAIN_SELECTED"
               and s.export_global_P is True
               and atlas.axis_summary.get("CODOMAIN", {}).get("global_P_count", 0) == 1)
        err = None
    except Exception as exc:
        aok = False
        err = f"{type(exc).__name__}: {exc}"
    ok = attrs and aok
    return {"name": "check_T_laser_coherence_codomain_adapter_atlas_contract_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_atlas_contract" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_atlas_contract",
            "summary": "Laser coherence adapter declares the CODOMAIN atlas contract; live payload reaches COHERENT via the engine.",
            "dependencies": ["apf.interface_atlas", "apf.codomain_selection_engine.adjudicate_codomain_competition"],
            "data": {"attrs_ok": attrs, "atlas_ok": aok, "atlas_error": err}}


def register(registry=None):
    checks = {
        "check_T_laser_coherence_codomain_adapter_payload_contract_P": check_T_laser_coherence_codomain_adapter_payload_contract_P,
        "check_T_laser_coherence_codomain_adapter_verdict_consistent_P": check_T_laser_coherence_codomain_adapter_verdict_consistent_P,
        "check_T_laser_coherence_codomain_adapter_audit_first_P": check_T_laser_coherence_codomain_adapter_audit_first_P,
        "check_T_laser_coherence_codomain_adapter_atlas_contract_P": check_T_laser_coherence_codomain_adapter_atlas_contract_P,
    }
    if registry is None:
        return checks
    registry.update(checks)
    return registry


def run_all():
    return {k: v() for k, v in register().items()}
