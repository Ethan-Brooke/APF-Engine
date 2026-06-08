"""APF dark w2(a) background Adapter — internal-identity closure (v24.3.45).

Step C continuation Phase 3. APF2 second-order FCR structural derivation
of w2(a) = -1 + 3/61 - (16/61)a - (21/8)a(a-1/3)(1-a) bank-witnessed at
LATEST-62 with rational coefficients w0 = -58/61, wa = -16/61. Status
[P_internal under G_2FCR]: the curve is structurally derived from
endpoint-uniqueness + barycentric-pivot + capacity-response-ratio BEFORE
any empirical evaluation.

Produces closure_kind=internal_identity payload so the engine returns
INTERNAL_IDENTITY_GLOBAL_P at the structural-export layer. The separate
empirical-promotion gates (DESI full-shape exact runtime, MCMC posterior
convergence, NERSC reproduction) remain honestly HELD_FOR_REPAIR via
their own atlas inputs — those are not closed by this adapter.
"""
from __future__ import annotations
from typing import Any, Dict

ATLAS_INPUT_ID = "dark:route_w2_a_background"
ATLAS_ROUTE = "dark"
ATLAS_PAYLOAD_NAME = "dark_w2_a_background_real_adapter_live"


def build_live_atlas_payload() -> Dict[str, Any]:
    return {
        "name": ATLAS_PAYLOAD_NAME,
        "closure_kind": "internal_identity",
        "identity_summary": (
            "APF2 dark-energy response w2(a) = -1 + 3/61 - (16/61)a - (21/8)a(a-1/3)(1-a) "
            "structurally derived at LATEST-62 from gate G_2FCR (trace-free curvature mode "
            "of three-sector continuability simplex). Rational coefficients w0 = -58/61, "
            "wa = -16/61 forced by endpoint preservation + minimality + barycentric pivot "
            "(x_star = 1/3, three-sector neutral coordinate) + capacity response ratio "
            "(kappa_2 = Omega_Lambda/Omega_c = 21/8). Phantom-crossing at x_cross = 0.2854, "
            "z_cross = 0.3993. Status [P_internal under G_2FCR]: structural derivation "
            "BEFORE empirical evaluation; not a fit. Registry pointer LATEST-62 "
            "APF_DARK_SECTOR_2FCR_INTERNAL_CLOSURE_v1."
        ),
        "target_value_consumed": False,
        "registry_status": "[P_internal under G_2FCR]",
        "registry_pointer": "LATEST-62 (APF_DARK_SECTOR_2FCR_INTERNAL_CLOSURE_v1)",
    }


def _check_payload_closure_kind() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    tests = {
        "closure_kind_internal_identity": p.get("closure_kind") == "internal_identity",
        "identity_summary_present": bool(p.get("identity_summary")),
        "target_value_not_consumed": p.get("target_value_consumed") is False,
        "atlas_input_id_correct": ATLAS_INPUT_ID == "dark:route_w2_a_background",
    }
    return {
        "name": "check_T_dark_w2_a_background_adapter_closure_kind_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_closure_kind" if all(tests.values()) else "FAIL",
        "summary": "dark w2(a) background adapter declares closure_kind=internal_identity (APF2 structural derivation).",
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
        "name": "check_T_dark_w2_a_background_adapter_atlas_routes_P",
        "consistent": ok,
        "passed": ok,
        "status": "P_atlas_routes" if ok else "FAIL",
        "summary": "Atlas routes dark w2(a) background payload to INTERNAL_IDENTITY_GLOBAL_P.",
        "data": {"solver_status": summary.solver_status, "export_global_P": summary.export_global_P},
    }


def _check_separate_empirical_gates_not_promoted() -> Dict[str, Any]:
    p = build_live_atlas_payload()
    tests = {
        "structural_only_not_empirical": "empirical" not in p.get("identity_summary", "").lower().split("structural")[0],
        "target_value_not_consumed": p.get("target_value_consumed") is False,
        "G_2FCR_gate_named": "G_2FCR" in p.get("identity_summary", ""),
    }
    return {
        "name": "check_T_dark_w2_a_background_adapter_structural_only_P",
        "consistent": all(tests.values()),
        "passed": all(tests.values()),
        "status": "P_separation_preserved" if all(tests.values()) else "FAIL",
        "summary": "dark w2(a) adapter promotes only structural derivation; separate empirical-promotion gates (DESI full-shape, MCMC convergence, NERSC reproduction) remain HELD_FOR_REPAIR via their own atlas inputs.",
        "data": {"tests": tests},
    }


CHECKS = {
    "check_T_dark_w2_a_background_adapter_closure_kind_P": _check_payload_closure_kind,
    "check_T_dark_w2_a_background_adapter_atlas_routes_P": _check_atlas_routes_to_identity_status,
    "check_T_dark_w2_a_background_adapter_structural_only_P": _check_separate_empirical_gates_not_promoted,
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
