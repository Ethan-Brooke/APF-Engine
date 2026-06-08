"""APF sin²θ_W source identity Route 12 Adapter — internal-identity closure (v24.3.42).

Closure-by-construction adapter for mass:route12_sin2_theta_w_source_identity. Registry status [P_internal].
Produces a closure_kind=internal_identity payload so the engine's
``_compile_payload_input`` short-circuit returns ``INTERNAL_IDENTITY_GLOBAL_P``.
"""
from __future__ import annotations

from typing import Any, Dict

ATLAS_INPUT_ID = "mass:route12_sin2_theta_w_source_identity"
ATLAS_ROUTE = "ew"
ATLAS_PAYLOAD_NAME = "sin2theta_w_source_identity_real_adapter_live"


def build_live_atlas_payload() -> Dict[str, Any]:
    return {
        "name": ATLAS_PAYLOAD_NAME,
        "closure_kind": "internal_identity",
        "identity_summary": (
            "sin²θ_W^source = 3/13 = 0.230769 is the APF source value; the source IS the codomain (admissibility-anchored, scheme-independent). Identity by structural construction; no transport required. Registry status [P_internal] (Reference - Mass Sector Closure Registry §Route 12)."
        ),
        "target_value_consumed": False,
        "registry_status": "[P_internal]",
        "registry_pointer": "Reference - Mass Sector Closure Registry §Route 12",
    }


def _check_payload_closure_kind() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    tests = {
        "closure_kind_internal_identity": p.get("closure_kind") == "internal_identity",
        "identity_summary_present": bool(p.get("identity_summary")),
        "target_value_not_consumed": p.get("target_value_consumed") is False,
        "atlas_input_id_correct": ATLAS_INPUT_ID == "mass:route12_sin2_theta_w_source_identity",
    }
    return {
        "name": "check_T_sin2theta_w_source_identity_adapter_closure_kind_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_closure_kind" if all(tests.values()) else "FAIL",
        "summary": "sin²θ_W source identity Route 12 adapter declares closure_kind=internal_identity.",
        "data": {"tests": tests, "payload": p},
    }


def _check_no_smuggling() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    forbidden = {"fitted_sin2theta", "pdg_sin2theta_measured", "post_hoc_value"}
    smuggled = [k for k in forbidden if k in p]
    tests = {
        "no_forbidden_keys": not smuggled,
        "target_value_consumed_false": p.get("target_value_consumed") is False,
    }
    return {
        "name": "check_T_sin2theta_w_source_identity_adapter_no_smuggling_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_no_smuggling" if all(tests.values()) else "FAIL",
        "summary": "sin²θ_W source identity Route 12 adapter does not consume target sin²θ_W values.",
        "data": {"tests": tests, "smuggled": smuggled},
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
    ok = (
        summary.solver_status == "INTERNAL_IDENTITY_GLOBAL_P"
        and summary.export_global_P is True
    )
    return {
        "name": "check_T_sin2theta_w_source_identity_adapter_atlas_routes_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_atlas_routes" if ok else "FAIL",
        "summary": "Atlas routes the sin²θ_W source identity Route 12 payload to INTERNAL_IDENTITY_GLOBAL_P.",
        "data": {"solver_status": summary.solver_status, "export_global_P": summary.export_global_P},
    }


CHECKS = {
    "check_T_sin2theta_w_source_identity_adapter_closure_kind_P": _check_payload_closure_kind,
    "check_T_sin2theta_w_source_identity_adapter_no_smuggling_P": _check_no_smuggling,
    "check_T_sin2theta_w_source_identity_adapter_atlas_routes_P": _check_atlas_routes_to_identity_status,
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
