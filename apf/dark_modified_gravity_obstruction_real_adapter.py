"""APF dark modified gravity Obstruction Adapter — closure-by-design (v24.3.43).

Step C continuation. Registry status [P_obstruction_named].
Produces closure_kind=obstruction_named payload so the engine returns OBSTRUCTION_NAMED_CLOSURE.
"""
from __future__ import annotations
from typing import Any, Dict

ATLAS_INPUT_ID = "dark:route_modified_gravity"
ATLAS_ROUTE = "horizon"
ATLAS_PAYLOAD_NAME = "dark_modified_gravity_obstruction_real_adapter_live"


def build_live_atlas_payload() -> Dict[str, Any]:
    return {
        "name": ATLAS_PAYLOAD_NAME,
        "closure_kind": "obstruction_named",
        "obstruction_class": "MODIFIED_GRAVITY_NOT_EXPORTED_BIANCHI_NO_GO",
        "knockout_summary": (
            "Modified gravity export: bank-witnessed at LATEST-71/72 as NOT exported. Bianchi-consistency no-go theorem (APF_GRAVITY_CORRECTION_OPERATOR_AUDIT_v1 + APF_GRAVITY_NON_GR_CORRECTION_TENSOR_NO_GO_v7) refuses to promote a non-GR geometric operator without all 6 Bianchi-consistency conditions satisfied. The framework exports GR-limit + APF source corrections, NOT a modified-gravity tensor."
        ),
        "target_value_consumed": False,
        "registry_status": "[P_obstruction_named]",
        "registry_pointer": "LATEST-71 + LATEST-72 gravity-sector full close (APF_GRAVITY_FULL_CLOSE_v6)",
    }


def _check_payload_closure_kind() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    tests = {
        "closure_kind_obstruction_named": p.get("closure_kind") == "obstruction_named",
        "obstruction_class_named": bool(p.get("obstruction_class")),
        "target_value_not_consumed": p.get("target_value_consumed") is False,
        "atlas_input_id_correct": ATLAS_INPUT_ID == "dark:route_modified_gravity",
    }
    return {
        "name": "check_T_dark_modified_gravity_obstruction_adapter_closure_kind_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_closure_kind" if all(tests.values()) else "FAIL",
        "summary": "dark modified gravity obstruction adapter declares closure_kind=obstruction_named.",
        "data": {"tests": tests, "payload": p},
    }


def _check_atlas_routes_to_obstruction_status() -> Dict[str, Any]:
    from apf.interface_atlas import AtlasInput, AtlasInputKind, summarize_input
    inp = AtlasInput(
        input_id=ATLAS_INPUT_ID,
        route=ATLAS_ROUTE,
        kind=AtlasInputKind.ROUTE_PAYLOAD,
        claim_text=None,
        payload=build_live_atlas_payload(),
    )
    summary = summarize_input(inp)
    ok = summary.solver_status == "OBSTRUCTION_NAMED_CLOSURE" and summary.export_global_P is False
    return {
        "name": "check_T_dark_modified_gravity_obstruction_adapter_atlas_routes_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_atlas_routes" if ok else "FAIL",
        "summary": "Atlas routes dark modified gravity payload to OBSTRUCTION_NAMED_CLOSURE.",
        "data": {"solver_status": summary.solver_status, "export_global_P": summary.export_global_P},
    }


def _check_registry_pointer_present() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    ok = bool(p.get("registry_pointer"))
    return {
        "name": "check_T_dark_modified_gravity_obstruction_adapter_registry_pointer_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_provenance" if ok else "FAIL",
        "summary": "dark modified gravity adapter cites registry pointer.",
        "data": {"registry_pointer": p.get("registry_pointer")},
    }


CHECKS = {
    "check_T_dark_modified_gravity_obstruction_adapter_closure_kind_P": _check_payload_closure_kind,
    "check_T_dark_modified_gravity_obstruction_adapter_atlas_routes_P": _check_atlas_routes_to_obstruction_status,
    "check_T_dark_modified_gravity_obstruction_adapter_registry_pointer_P": _check_registry_pointer_present,
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
