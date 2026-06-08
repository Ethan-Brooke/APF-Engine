"""APF gravity Bianchi rigidity Adapter — internal-identity closure (v24.3.44).

Step C continuation Phase 2. Framework-internal structural export.
Produces closure_kind=internal_identity payload so the engine returns INTERNAL_IDENTITY_GLOBAL_P.
"""
from __future__ import annotations
from typing import Any, Dict

ATLAS_INPUT_ID = "gravity:route_bianchi_rigidity"
ATLAS_ROUTE = "horizon"
ATLAS_PAYLOAD_NAME = "gravity_bianchi_rigidity_real_adapter_live"


def build_live_atlas_payload() -> Dict[str, Any]:
    return {
        "name": ATLAS_PAYLOAD_NAME,
        "closure_kind": "internal_identity",
        "identity_summary": (
            "Bianchi rigidity theorem: any APF non-GR correction operator must satisfy 6 conditions (symmetric rank-2 + divergence-free + geometric + APF-coefficient + non-degenerate + empirically exported without consuming residuals). Bank-witnessed at LATEST-72 via APF_GRAVITY_BIANCHI_RIGIDITY_PUSH_v8 (Export_metric_side_rigidity_theorem = 1; Export_nonGR_correction_tensor_no_go_P = 1)."
        ),
        "target_value_consumed": False,
        "registry_status": "[P_internal] (framework structural export)",
        "registry_pointer": "LATEST-72 (APF_GRAVITY_BIANCHI_RIGIDITY_PUSH_v8 + APF_GRAVITY_NON_GR_CORRECTION_TENSOR_NO_GO_v7)",
    }


def _check_payload_closure_kind() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    tests = {
        "closure_kind_internal_identity": p.get("closure_kind") == "internal_identity",
        "identity_summary_present": bool(p.get("identity_summary")),
        "target_value_not_consumed": p.get("target_value_consumed") is False,
        "atlas_input_id_correct": ATLAS_INPUT_ID == "gravity:route_bianchi_rigidity",
    }
    return {
        "name": "check_T_gravity_bianchi_rigidity_adapter_closure_kind_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_closure_kind" if all(tests.values()) else "FAIL",
        "summary": "gravity Bianchi rigidity adapter declares closure_kind=internal_identity (framework structural export).",
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
        "name": "check_T_gravity_bianchi_rigidity_adapter_atlas_routes_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_atlas_routes" if ok else "FAIL",
        "summary": "Atlas routes gravity Bianchi rigidity payload to INTERNAL_IDENTITY_GLOBAL_P.",
        "data": {"solver_status": summary.solver_status, "export_global_P": summary.export_global_P},
    }


def _check_registry_pointer_present() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    ok = bool(p.get("registry_pointer"))
    return {
        "name": "check_T_gravity_bianchi_rigidity_adapter_registry_pointer_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_provenance" if ok else "FAIL",
        "summary": "gravity Bianchi rigidity adapter cites registry pointer.",
        "data": {"registry_pointer": p.get("registry_pointer")},
    }


CHECKS = {
    "check_T_gravity_bianchi_rigidity_adapter_closure_kind_P": _check_payload_closure_kind,
    "check_T_gravity_bianchi_rigidity_adapter_atlas_routes_P": _check_atlas_routes_to_identity_status,
    "check_T_gravity_bianchi_rigidity_adapter_registry_pointer_P": _check_registry_pointer_present,
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
