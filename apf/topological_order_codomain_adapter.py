"""APF Topological order Codomain Adapter (Tier 4 under Codomain Selection Engine).

Landed v24.3.65 from APF_IE_TOPOLOGICAL_ORDER_CODOMAIN_REGIME_v1 (sibling pack), conformed to the APF bank
convention: routes through the engine's adjudicate_codomain_competition and
carries dict-shaped bank checks. The runtime evaluator (apf.topological_order_ie) is installed
verbatim from the pack. Seventh and final coherent-phase regime.

Non-claims preserved: no numeric gap/critical-parameter export, no
material-specific topological-phase claim, no ab-initio chemistry, no experiment.
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

ADAPTER_NAME = "topological_order_codomain_adapter"
ADAPTER_ENGINE = ENGINE_NAME
ADAPTER_REGIME = "TOPOLOGICAL_ORDER"
ADAPTER_TIER = 4

ATLAS_INPUT_ID = "coherent_phase:topological_order"
ATLAS_ROUTE = "coherent_phase:topological_order"
ATLAS_PAYLOAD_NAME = "topological_order_codomain_adapter_live"
ATLAS_AXIS = "CODOMAIN"

_FIXTURES = _json.loads(r"""[
  {
    "name": "select_z2_topological_order",
    "expected_verdict": "SELECT_TOPOLOGICAL_ORDER_STRUCTURAL",
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 2.0,
      "thermal_pressure": 0.15,
      "gap_pressure": 0.1,
      "anyon_defect_pressure": 0.1,
      "boundary_pressure": 0.05,
      "disorder_pressure": 0.05,
      "local_order_pressure": 0.05,
      "degeneracy_pressure": 0.05,
      "braid_winding_pressure": 0.05,
      "history_pressure": 0.02,
      "dimension": 2,
      "topology_class": "Z2_gauge",
      "global_sector_declared": true,
      "winding_or_braid_ledger_declared": true,
      "local_indistinguishability_declared": true,
      "local_indistinguishability_passed": true,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true,
      "history_barrier_cleared": true
    }
  },
  {
    "name": "local_records_win_nonpositive_margin",
    "expected_verdict": null,
    "network_state": {
      "cost_fragmented": 2.0,
      "cost_coherent": 4.0,
      "global_sector_declared": true,
      "winding_or_braid_ledger_declared": true,
      "local_indistinguishability_passed": true,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true
    }
  },
  {
    "name": "global_sector_missing",
    "expected_verdict": "GLOBAL_SECTOR_LEDGER_MISSING",
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 1.0,
      "global_sector_declared": false,
      "winding_or_braid_ledger_declared": true,
      "local_indistinguishability_passed": true,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true
    }
  },
  {
    "name": "local_indistinguishability_failed",
    "expected_verdict": "LOCAL_INDISTINGUISHABILITY_FAILED",
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 1.0,
      "local_indistinguishability_passed": false,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true
    }
  },
  {
    "name": "gap_insufficient",
    "expected_verdict": "GAP_INSUFFICIENT",
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 1.0,
      "gap_pressure": 2.0,
      "gap_gate": 1.0,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true
    }
  },
  {
    "name": "local_order_contamination_refused",
    "expected_verdict": "LOCAL_ORDER_CONTAMINATION_REFUSED",
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 1.0,
      "local_order_contamination": true,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true
    }
  },
  {
    "name": "history_locked",
    "expected_verdict": null,
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 1.0,
      "history_barrier_cleared": false,
      "history_pressure": 0.2,
      "history_gate": 1.0,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true
    }
  },
  {
    "name": "numeric_gap_export_refused",
    "expected_verdict": "REFUSE_NUMERIC_GAP_EXPORT",
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 1.0,
      "numeric_export_attempt": true,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true
    }
  },
  {
    "name": "material_specific_claim_refused",
    "expected_verdict": "REFUSE_MATERIAL_SPECIFIC_TOPOLOGICAL_PHASE_CLAIM",
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 1.0,
      "material_specific_claim": true,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true
    }
  },
  {
    "name": "wrong_regime_relabel_refused",
    "expected_verdict": "REFUSE_WRONG_REGIME_CONTAMINATION",
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 1.0,
      "ordinary_symmetry_breaking_relabel": true,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true
    }
  },
  {
    "name": "chern_fqh_route",
    "expected_verdict": "SELECT_TOPOLOGICAL_ORDER_STRUCTURAL",
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 2.0,
      "topology_class": "FQH",
      "chern_or_fqh_flag": true,
      "thermal_pressure": 0.1,
      "gap_pressure": 0.1,
      "anyon_defect_pressure": 0.1,
      "boundary_pressure": 0.1,
      "degeneracy_pressure": 0.1,
      "braid_winding_pressure": 0.1,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true
    }
  },
  {
    "name": "spt_guarded_route",
    "expected_verdict": null,
    "network_state": {
      "cost_fragmented": 8.0,
      "cost_coherent": 2.0,
      "topology_class": "SPT",
      "spt_boundary_flag": true,
      "topological_gap_declared": true,
      "topological_degeneracy_declared": true,
      "anyon_or_defect_sector_declared": true,
      "boundary_condition_declared": true
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
            "runtime_module": "apf.topological_order_ie",
            "engine_module": "apf.codomain_selection_engine",
            "pack_source": "APF_IE_TOPOLOGICAL_ORDER_CODOMAIN_REGIME_v1",
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


def check_T_topological_order_codomain_adapter_payload_contract_P() -> Dict[str, Any]:
    p = build_codomain_adapter_payload()
    required = ("adapter_name", "adapter_engine", "adapter_regime", "adapter_tier",
                "network_state", "verdict", "target_value_consumed",
                "preserved_non_claims", "external_evaluator_ledger")
    ok = (all(k in p for k in required) and p["adapter_engine"] == ENGINE_NAME
          and p["adapter_regime"] == "TOPOLOGICAL_ORDER" and p["adapter_tier"] == 4
          and p["target_value_consumed"] is False and isinstance(p["verdict"], dict)
          and "status" in p["verdict"])
    return {"name": "check_T_topological_order_codomain_adapter_payload_contract_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_contract" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_contract",
            "summary": "Topological order codomain adapter payload carries the required fields and routes through the engine.",
            "dependencies": ["apf.codomain_selection_engine.adjudicate_codomain_competition", "apf.topological_order_ie"],
            "data": {"keys": sorted(p.keys())}}


def check_T_topological_order_codomain_adapter_verdict_consistent_P() -> Dict[str, Any]:
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
    return {"name": "check_T_topological_order_codomain_adapter_verdict_consistent_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_verdict_consistent" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_verdict_consistent",
            "summary": "Installed Topological order runtime reproduces every fixture verdict through the engine.",
            "dependencies": ["apf.codomain_selection_engine._adjudicate_topological_order"],
            "data": {"fixtures": results}}


def check_T_topological_order_codomain_adapter_audit_first_P() -> Dict[str, Any]:
    p = build_codomain_adapter_payload()
    exports = p["verdict"].get("exports", {})
    nc = all(exports.get(k, -1) == 0 for k in PRESERVED_NON_CLAIMS)
    led = ("runtime_module" in p["external_evaluator_ledger"]
           and "engine_module" in p["external_evaluator_ledger"])
    ok = nc and p["target_value_consumed"] is False and led
    return {"name": "check_T_topological_order_codomain_adapter_audit_first_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_audit_first" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_audit_first",
            "summary": "Audit-first non-claims preserved; target not consumed; evaluator ledger declared.",
            "dependencies": ["apf.codomain_selection_engine.PRESERVED_NON_CLAIMS"],
            "data": {"non_claims_preserved": nc}}


def check_T_topological_order_codomain_adapter_atlas_contract_P() -> Dict[str, Any]:
    attrs = (ATLAS_INPUT_ID == "coherent_phase:topological_order" and ATLAS_AXIS == "CODOMAIN")
    payload = build_live_atlas_payload()
    try:
        from apf.interface_atlas import (AtlasInput, AtlasInputKind, AxisKind, build_interface_atlas)
        ai = AtlasInput(input_id="atlas_contract_test:topological_order", kind=AtlasInputKind.CODOMAIN_PAYLOAD,
                        route=ATLAS_ROUTE, claim_text=None, payload=payload, axis=AxisKind.CODOMAIN)
        atlas = build_interface_atlas([ai], atlas_name="atlas_contract_test_topological_order")
        s = atlas.route_summaries[0]
        aok = (s.axis == AxisKind.CODOMAIN and s.solver_status == "COHERENT_CODOMAIN_SELECTED"
               and s.export_global_P is True
               and atlas.axis_summary.get("CODOMAIN", {}).get("global_P_count", 0) == 1)
        err = None
    except Exception as exc:
        aok = False
        err = f"{type(exc).__name__}: {exc}"
    ok = attrs and aok
    return {"name": "check_T_topological_order_codomain_adapter_atlas_contract_P", "consistent": ok, "passed": ok,
            "tier": 4, "status": "P_codomain_adapter_atlas_contract" if ok else "FAIL",
            "epistemic": "P_codomain_adapter_atlas_contract",
            "summary": "Topological order adapter declares the CODOMAIN atlas contract; live payload reaches COHERENT via the engine.",
            "dependencies": ["apf.interface_atlas", "apf.codomain_selection_engine.adjudicate_codomain_competition"],
            "data": {"attrs_ok": attrs, "atlas_ok": aok, "atlas_error": err}}


def register(registry=None):
    checks = {
        "check_T_topological_order_codomain_adapter_payload_contract_P": check_T_topological_order_codomain_adapter_payload_contract_P,
        "check_T_topological_order_codomain_adapter_verdict_consistent_P": check_T_topological_order_codomain_adapter_verdict_consistent_P,
        "check_T_topological_order_codomain_adapter_audit_first_P": check_T_topological_order_codomain_adapter_audit_first_P,
        "check_T_topological_order_codomain_adapter_atlas_contract_P": check_T_topological_order_codomain_adapter_atlas_contract_P,
    }
    if registry is None:
        return checks
    registry.update(checks)
    return registry


def run_all():
    return {k: v() for k, v in register().items()}
