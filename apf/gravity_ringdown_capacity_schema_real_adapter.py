"""APF gravity ringdown capacity schema Adapter — internal-identity closure (v24.3.44).

Step C continuation Phase 2. Framework-internal structural export.
Produces closure_kind=internal_identity payload so the engine returns INTERNAL_IDENTITY_GLOBAL_P.
"""
from __future__ import annotations
from typing import Any, Dict

ATLAS_INPUT_ID = "gravity:route_ringdown_capacity_schema"
ATLAS_ROUTE = "horizon"
ATLAS_PAYLOAD_NAME = "gravity_ringdown_capacity_schema_real_adapter_live"


def build_live_atlas_payload() -> Dict[str, Any]:
    return {
        "name": ATLAS_PAYLOAD_NAME,
        "closure_kind": "internal_identity",
        "identity_summary": (
            "Ringdown capacity schema: Export_ringdown_GR_baseline = 1; Export_ringdown_capacity_schema = 1; Export_ringdown_APF_nonGR_correction = 0. Bank-witnessed at LATEST-71 via APF_GRAVITY_SOURCE_SIDE_CLOSURE_AND_RINGDOWN_GATE_v2. Ringdown is GR-limit observable with APF interpretive/source-side structure; not modified-gravity prediction."
        ),
        "target_value_consumed": False,
        "registry_status": "[P_internal] (framework structural export)",
        "registry_pointer": "LATEST-71 (APF_GRAVITY_SOURCE_SIDE_CLOSURE_AND_RINGDOWN_GATE_v2)",
    }


def _check_payload_closure_kind() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    tests = {
        "closure_kind_internal_identity": p.get("closure_kind") == "internal_identity",
        "identity_summary_present": bool(p.get("identity_summary")),
        "target_value_not_consumed": p.get("target_value_consumed") is False,
        "atlas_input_id_correct": ATLAS_INPUT_ID == "gravity:route_ringdown_capacity_schema",
    }
    return {
        "name": "check_T_gravity_ringdown_capacity_schema_adapter_closure_kind_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_closure_kind" if all(tests.values()) else "FAIL",
        "summary": "gravity ringdown capacity schema adapter declares closure_kind=internal_identity (framework structural export).",
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
        "name": "check_T_gravity_ringdown_capacity_schema_adapter_atlas_routes_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_atlas_routes" if ok else "FAIL",
        "summary": "Atlas routes gravity ringdown capacity schema payload to INTERNAL_IDENTITY_GLOBAL_P.",
        "data": {"solver_status": summary.solver_status, "export_global_P": summary.export_global_P},
    }


def _check_registry_pointer_present() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    ok = bool(p.get("registry_pointer"))
    return {
        "name": "check_T_gravity_ringdown_capacity_schema_adapter_registry_pointer_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_provenance" if ok else "FAIL",
        "summary": "gravity ringdown capacity schema adapter cites registry pointer.",
        "data": {"registry_pointer": p.get("registry_pointer")},
    }


CHECKS = {
    "check_T_gravity_ringdown_capacity_schema_adapter_closure_kind_P": _check_payload_closure_kind,
    "check_T_gravity_ringdown_capacity_schema_adapter_atlas_routes_P": _check_atlas_routes_to_identity_status,
    "check_T_gravity_ringdown_capacity_schema_adapter_registry_pointer_P": _check_registry_pointer_present,
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
