"""APF Charm-pole Obstruction Adapter — closure-by-design (v24.3.42).

Mass-sector Route 4 (m_c → pole) closure-by-design adapter. Registry status is
``[P_obstruction_named]`` — the pole codomain is rejected (inheritance from
top-pole quarantine pattern; renormalon-uncontrolled in charm sector).

Produces a closure_kind=obstruction_named payload so the engine's
``_compile_payload_input`` short-circuit returns ``OBSTRUCTION_NAMED_CLOSURE``
status. Closes Mass-sector engine confirmation gap for R4.
"""
from __future__ import annotations

from typing import Any, Dict, Mapping

ATLAS_INPUT_ID = "mass:route04_charm_pole"
ATLAS_ROUTE = "ew"
ATLAS_PAYLOAD_NAME = "charm_pole_obstruction_real_adapter_live"


def build_live_atlas_payload() -> Dict[str, Any]:
    return {
        "name": ATLAS_PAYLOAD_NAME,
        "closure_kind": "obstruction_named",
        "obstruction_class": "POLE_CODOMAIN_REJECTED_RENORMALON_UNCONTROLLED",
        "knockout_summary": (
            "Charm-pole codomain rejected: APF trace is short-distance-like; pole interpretation "
            "inherits the renormalon-uncontrolled quarantine from the top-pole pattern. "
            "Registry status [P_obstruction_named] (Reference - Mass Sector Closure Registry §Route 4)."
        ),
        "target_value_consumed": False,
        "registry_status": "[P_obstruction_named]",
        "registry_pointer": "Reference - Mass Sector Closure Registry §Route 4",
    }


def _check_payload_closure_kind() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    tests = {
        "closure_kind_obstruction_named": p.get("closure_kind") == "obstruction_named",
        "obstruction_class_named": bool(p.get("obstruction_class")),
        "target_value_not_consumed": p.get("target_value_consumed") is False,
        "atlas_input_id_route04": ATLAS_INPUT_ID == "mass:route04_charm_pole",
    }
    return {
        "name": "check_T_charm_pole_obstruction_adapter_closure_kind_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_closure_kind" if all(tests.values()) else "FAIL",
        "summary": "Charm-pole obstruction adapter declares closure_kind=obstruction_named with named obstruction class.",
        "data": {"tests": tests, "payload": p},
    }


def _check_no_smuggling() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    forbidden = {"pole_mass_measured", "fitted_pole_mass", "pdg_charm_pole"}
    smuggled = [k for k in forbidden if k in p]
    tests = {
        "no_forbidden_keys": not smuggled,
        "target_value_consumed_false": p.get("target_value_consumed") is False,
    }
    return {
        "name": "check_T_charm_pole_obstruction_adapter_no_smuggling_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_no_smuggling" if all(tests.values()) else "FAIL",
        "summary": "Charm-pole obstruction adapter does not consume target pole-mass values.",
        "data": {"tests": tests, "smuggled": smuggled},
    }


def _check_atlas_routes_to_obstruction_status() -> Dict[str, Any]:
    """End-to-end: payload through atlas should produce OBSTRUCTION_NAMED_CLOSURE."""
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
        "name": "check_T_charm_pole_obstruction_adapter_atlas_routes_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_atlas_routes" if ok else "FAIL",
        "summary": "Atlas routes the charm-pole payload to OBSTRUCTION_NAMED_CLOSURE.",
        "data": {"solver_status": summary.solver_status, "export_global_P": summary.export_global_P},
    }


CHECKS = {
    "check_T_charm_pole_obstruction_adapter_closure_kind_P": _check_payload_closure_kind,
    "check_T_charm_pole_obstruction_adapter_no_smuggling_P": _check_no_smuggling,
    "check_T_charm_pole_obstruction_adapter_atlas_routes_P": _check_atlas_routes_to_obstruction_status,
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
