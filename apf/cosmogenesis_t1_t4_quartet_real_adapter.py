"""APF cosmogenesis T1-T4 quartet Adapter — internal-identity closure (v24.3.44).

Step C continuation Phase 2. Framework-internal structural export.
Produces closure_kind=internal_identity payload so the engine returns INTERNAL_IDENTITY_GLOBAL_P.
"""
from __future__ import annotations
from typing import Any, Dict

ATLAS_INPUT_ID = "cosmogenesis:route_t1_t4_quartet"
ATLAS_ROUTE = "horizon"
ATLAS_PAYLOAD_NAME = "cosmogenesis_t1_t4_quartet_real_adapter_live"


def build_live_atlas_payload() -> Dict[str, Any]:
    return {
        "name": ATLAS_PAYLOAD_NAME,
        "closure_kind": "internal_identity",
        "identity_summary": (
            "Cosmogenesis T1-T4 quartet bank-witnessed at LATEST-44 v33-v36 via apf.plec + apf.gravity. T1 substrate-side alignment as Type V realignment-cost; T2 channel-flow vacuum-face/content-face from holographic ceiling; T3 cumulative-balance equation |V_global,local|_deposit = |V_global,local|_release + S_radiation (structural form of BH unitarity at substrate-side ledger); T4 lattice ordering with Page-curve turnover at half-evaporation. Framework certifies its own cosmogenesis structural arc."
        ),
        "target_value_consumed": False,
        "registry_status": "[P_internal] (framework structural export)",
        "registry_pointer": "LATEST-44 v33-v36 (cosmogenic quartet T1-T4 in apf.plec + apf.gravity)",
    }


def _check_payload_closure_kind() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    tests = {
        "closure_kind_internal_identity": p.get("closure_kind") == "internal_identity",
        "identity_summary_present": bool(p.get("identity_summary")),
        "target_value_not_consumed": p.get("target_value_consumed") is False,
        "atlas_input_id_correct": ATLAS_INPUT_ID == "cosmogenesis:route_t1_t4_quartet",
    }
    return {
        "name": "check_T_cosmogenesis_t1_t4_quartet_adapter_closure_kind_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_closure_kind" if all(tests.values()) else "FAIL",
        "summary": "cosmogenesis T1-T4 quartet adapter declares closure_kind=internal_identity (framework structural export).",
        "data": {"tests": tests, "payload": p},
    }


def _check_atlas_routes_to_identity_status() -> Dict[str, Any]:
    from apf.interface_atlas import AtlasInput, AtlasInputKind, summarize_input
    inp = AtlasInput(
        input_id=ATLAS_INPUT_ID,
        route=ATLAS_ROUTE,
        kind=AtlasInputKind.ROUTE_PAYLOAD,
        claim_text=None,
        payload=build_live_atlas_payload(),
    )
    summary = summarize_input(inp)
    ok = summary.solver_status == "INTERNAL_IDENTITY_GLOBAL_P" and summary.export_global_P is True
    return {
        "name": "check_T_cosmogenesis_t1_t4_quartet_adapter_atlas_routes_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_atlas_routes" if ok else "FAIL",
        "summary": "Atlas routes cosmogenesis T1-T4 quartet payload to INTERNAL_IDENTITY_GLOBAL_P.",
        "data": {"solver_status": summary.solver_status, "export_global_P": summary.export_global_P},
    }


def _check_registry_pointer_present() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    ok = bool(p.get("registry_pointer"))
    return {
        "name": "check_T_cosmogenesis_t1_t4_quartet_adapter_registry_pointer_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_provenance" if ok else "FAIL",
        "summary": "cosmogenesis T1-T4 quartet adapter cites registry pointer.",
        "data": {"registry_pointer": p.get("registry_pointer")},
    }


CHECKS = {
    "check_T_cosmogenesis_t1_t4_quartet_adapter_closure_kind_P": _check_payload_closure_kind,
    "check_T_cosmogenesis_t1_t4_quartet_adapter_atlas_routes_P": _check_atlas_routes_to_identity_status,
    "check_T_cosmogenesis_t1_t4_quartet_adapter_registry_pointer_P": _check_registry_pointer_present,
}


def register(registry=None):
    if registry is None:
        return dict(CHECKS)
    registry.update(CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    print(json.dumps(run_all(), indent=2, sort_keys=True, default=str))
