"""APF Bottom-pole Route 6 Obstruction Adapter — closure-by-design (v24.3.42).

Closure-by-design adapter for mass:route06_bottom_pole. Registry status [P_obstruction_named].
Produces a closure_kind=obstruction_named payload so the engine's
``_compile_payload_input`` short-circuit returns ``OBSTRUCTION_NAMED_CLOSURE``.
"""
from __future__ import annotations

from typing import Any, Dict

ATLAS_INPUT_ID = "mass:route06_bottom_pole"
ATLAS_ROUTE = "ew"
ATLAS_PAYLOAD_NAME = "bottom_pole_obstruction_real_adapter_live"


def build_live_atlas_payload() -> Dict[str, Any]:
    return {
        "name": ATLAS_PAYLOAD_NAME,
        "closure_kind": "obstruction_named",
        "obstruction_class": "POLE_CODOMAIN_REJECTED_GT_10_SIGMA",
        "knockout_summary": (
            "Bottom-pole codomain rejected by >10σ knockout: APF trace is short-distance-like and inconsistent with pole interpretation. Registry status [P_obstruction_named] (Reference - Mass Sector Closure Registry §Route 6, LATEST-11 v23–v24)."
        ),
        "target_value_consumed": False,
        "registry_status": "[P_obstruction_named]",
        "registry_pointer": "Reference - Mass Sector Closure Registry §Route 6",
    }


def _check_payload_closure_kind() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    tests = {
        "closure_kind_obstruction_named": p.get("closure_kind") == "obstruction_named",
        "obstruction_class_named": bool(p.get("obstruction_class")),
        "target_value_not_consumed": p.get("target_value_consumed") is False,
        "atlas_input_id_correct": ATLAS_INPUT_ID == "mass:route06_bottom_pole",
    }
    return {
        "name": "check_T_bottom_pole_obstruction_adapter_closure_kind_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_closure_kind" if all(tests.values()) else "FAIL",
        "summary": "Bottom-pole Route 6 obstruction adapter declares closure_kind=obstruction_named.",
        "data": {"tests": tests, "payload": p},
    }


def _check_no_smuggling() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    forbidden = {"pole_mass_measured", "fitted_pole_mass", "pdg_pole"}
    smuggled = [k for k in forbidden if k in p]
    tests = {
        "no_forbidden_keys": not smuggled,
        "target_value_consumed_false": p.get("target_value_consumed") is False,
    }
    return {
        "name": "check_T_bottom_pole_obstruction_adapter_no_smuggling_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_no_smuggling" if all(tests.values()) else "FAIL",
        "summary": "Bottom-pole Route 6 obstruction adapter does not consume target pole-mass values.",
        "data": {"tests": tests, "smuggled": smuggled},
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
    ok = (
        summary.solver_status == "OBSTRUCTION_NAMED_CLOSURE"
        and summary.export_global_P is False
    )
    return {
        "name": "check_T_bottom_pole_obstruction_adapter_atlas_routes_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_atlas_routes" if ok else "FAIL",
        "summary": "Atlas routes the Bottom-pole Route 6 payload to OBSTRUCTION_NAMED_CLOSURE.",
        "data": {"solver_status": summary.solver_status, "export_global_P": summary.export_global_P},
    }


CHECKS = {
    "check_T_bottom_pole_obstruction_adapter_closure_kind_P": _check_payload_closure_kind,
    "check_T_bottom_pole_obstruction_adapter_no_smuggling_P": _check_no_smuggling,
    "check_T_bottom_pole_obstruction_adapter_atlas_routes_P": _check_atlas_routes_to_obstruction_status,
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
