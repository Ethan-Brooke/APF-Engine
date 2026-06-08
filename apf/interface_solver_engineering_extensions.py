"""
APF Interface Solver Engineering Extensions.

Top-level engineering extension verifier.
"""

from __future__ import annotations

import json
from typing import Dict, Iterable, Mapping, Optional

from apf.interface_solver_descent_bridge import InterfaceSolverProblem, solve_interface_descent
from apf.interface_solver_contracts import example_problem_dicts, load_problem_list, problem_from_dict
from apf.interface_solver_batch import certify_batch, certificates_to_jsonable, certificates_to_csv_rows
from apf.interface_solver_ci_policy import CIPolicyMode, evaluate_ci_policy, policy_result_to_dict
from apf.interface_solver_report import render_markdown_report, render_json_report
from apf.interface_solver_route_adapters import ew_trace_to_scheme_problem, dark_empirical_problem, from_generic_solver_result


def _ok(name: str, *, status: str, summary: str, data: Optional[Mapping] = None,
        dependencies: Optional[Iterable[str]] = None) -> Dict:
    return {
        "name": name,
        "consistent": True,
        "status": status,
        "summary": summary,
        "data": dict(data or {}),
        "dependencies": list(dependencies or []),
    }


def _fail(name: str, *, status: str, summary: str, data: Optional[Mapping] = None,
          dependencies: Optional[Iterable[str]] = None) -> Dict:
    return {
        "name": name,
        "consistent": False,
        "status": status,
        "summary": summary,
        "data": dict(data or {}),
        "dependencies": list(dependencies or []),
    }


def check_T_engineering_contract_validation_P() -> Dict:
    raw = example_problem_dicts()[0]
    problem = problem_from_dict(raw)
    leaked = dict(raw)
    leaked["expected_status"] = "EXPORT_GLOBAL_P"
    leakage_rejected = False
    try:
        problem_from_dict(leaked)
    except ValueError:
        leakage_rejected = True

    tests = {
        "problem_created": problem.name == raw["name"],
        "leakage_rejected": leakage_rejected,
        "payload_loader_count": len(load_problem_list({"problems": list(example_problem_dicts())})) == 2,
    }
    if all(tests.values()):
        return _ok(
            "check_T_engineering_contract_validation_P",
            status="P_engineering",
            summary="Strict contract validation works and rejects expected-label leakage.",
            data={"tests": tests},
        )
    return _fail("check_T_engineering_contract_validation_P", status="FAIL", summary="Contract validation failed", data=tests)


def check_T_batch_certification_P() -> Dict:
    problems = load_problem_list({"problems": list(example_problem_dicts())})
    certs = certify_batch(problems)
    payload = certificates_to_jsonable(certs)
    rows = certificates_to_csv_rows(certs)
    tests = {
        "cert_count": len(certs) == 2,
        "jsonable_count": payload["certificate_count"] == 2,
        "csv_header": rows[0][0] == "problem_name",
        "one_global_export": len(payload["summary"]["global_exports"]) == 1,
        "one_held_or_failed": len(payload["summary"]["held_or_failed"]) == 1,
    }
    if all(tests.values()):
        return _ok(
            "check_T_batch_certification_P",
            status="P_engineering",
            summary="Batch certification produces JSON/CSV-ready outputs and summaries.",
            data={"tests": tests, "summary": payload["summary"]},
            dependencies=["check_T_engineering_contract_validation_P"],
        )
    return _fail("check_T_batch_certification_P", status="FAIL", summary="Batch certification failed", data={"tests": tests, "payload": payload})


def check_T_ci_policy_gate_P() -> Dict:
    problems = load_problem_list({"problems": list(example_problem_dicts())})
    certs = certify_batch(problems)
    permissive = evaluate_ci_policy(certs, mode=CIPolicyMode.PERMISSIVE_RESEARCH)
    strict = evaluate_ci_policy(certs, mode=CIPolicyMode.STRICT_GLOBAL_EXPORT)
    target_problem = InterfaceSolverProblem(
        name="bad_target_consuming",
        sector="PROVENANCE",
        local_solution_found=True,
        global_export_requested=True,
        acc_base_present=True,
        evaluator_map_found=True,
        codomain_transport_found=True,
        overlap_gluing_verified=True,
        capacity_budget_verified=True,
        capacity_overspend_detected=False,
        empirical_or_posterior_closed=True,
        target_value_used_as_input=True,
    )
    fail_closed = evaluate_ci_policy([solve_interface_descent(target_problem)], mode=CIPolicyMode.BLOCK_FAIL_CLOSED)
    tests = {
        "permissive_passes_held": permissive.pass_gate is True,
        "strict_fails_held": strict.pass_gate is False,
        "fail_closed_blocks": fail_closed.pass_gate is False,
    }
    if all(tests.values()):
        return _ok(
            "check_T_ci_policy_gate_P",
            status="P_engineering",
            summary="CI policy gate distinguishes permissive research, strict global export, and fail-closed provenance.",
            data={
                "tests": tests,
                "permissive": policy_result_to_dict(permissive),
                "strict": policy_result_to_dict(strict),
                "fail_closed": policy_result_to_dict(fail_closed),
            },
            dependencies=["check_T_batch_certification_P"],
        )
    return _fail("check_T_ci_policy_gate_P", status="FAIL", summary="CI policy gate failed", data=tests)


def check_T_report_generation_P() -> Dict:
    problems = load_problem_list({"problems": list(example_problem_dicts())})
    certs = certify_batch(problems)
    policy = evaluate_ci_policy(certs, mode=CIPolicyMode.BLOCK_FAIL_CLOSED)
    md = render_markdown_report(certs, policy)
    js = render_json_report(certs, policy)
    tests = {
        "markdown_has_title": "# APF Interface Solver Certification Report" in md,
        "markdown_has_certificates": "## Certificates" in md,
        "json_has_policy": "policy" in js,
        "json_has_certificates": len(js["certificates"]) == 2,
    }
    if all(tests.values()):
        return _ok(
            "check_T_report_generation_P",
            status="P_engineering",
            summary="Markdown and JSON certification reports render successfully.",
            data={"tests": tests, "json_summary": js["summary"]},
            dependencies=["check_T_ci_policy_gate_P"],
        )
    return _fail("check_T_report_generation_P", status="FAIL", summary="Report generation failed", data=tests)


def check_T_route_adapter_templates_P() -> Dict:
    ew = ew_trace_to_scheme_problem(
        name="adapter_EW_open",
        trace_local_closed=True,
        evaluator_map_found=False,
        codomain_transport_found=False,
        notes="adapter test",
    )
    dark = dark_empirical_problem(
        name="adapter_dark_open",
        local_route_found=True,
        posterior_closed=False,
        evaluator_map_found=False,
        notes="adapter test",
    )
    generic = from_generic_solver_result({
        "name": "adapter_generic_clean",
        "sector": "ACC",
        "local_solution_found": True,
        "global_export_requested": True,
        "acc_base_present": True,
        "evaluator_map_found": True,
        "codomain_transport_found": True,
        "overlap_gluing_verified": True,
        "capacity_budget_verified": True,
        "capacity_overspend_detected": False,
        "empirical_or_posterior_closed": True,
        "target_value_used_as_input": False,
    })
    certs = certify_batch([ew, dark, generic])
    statuses = {c.problem_name: c.solver_status.value for c in certs}
    tests = {
        "ew_held": statuses["adapter_EW_open"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "dark_held": statuses["adapter_dark_open"] == "SOLVED_LOCAL_HELD_FOR_REPAIR",
        "generic_global": statuses["adapter_generic_clean"] == "SOLVED_GLOBAL_P",
    }
    if all(tests.values()):
        return _ok(
            "check_T_route_adapter_templates_P",
            status="P_engineering",
            summary="Route adapter templates produce certifiable InterfaceSolverProblem objects.",
            data={"tests": tests, "statuses": statuses},
            dependencies=["check_T_report_generation_P"],
        )
    return _fail("check_T_route_adapter_templates_P", status="FAIL", summary="Route adapter templates failed", data={"tests": tests, "statuses": statuses})


def check_T_interface_solver_engineering_extensions_P() -> Dict:
    subchecks = [
        check_T_engineering_contract_validation_P(),
        check_T_batch_certification_P(),
        check_T_ci_policy_gate_P(),
        check_T_report_generation_P(),
        check_T_route_adapter_templates_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_interface_solver_engineering_extensions_P",
            status="P_engineering",
            summary="Interface solver engineering extensions are P: strict contracts, batch certification, CI gates, reports, and adapters pass.",
            data={
                "capabilities": [
                    "strict schema validation",
                    "expected-label leakage rejection",
                    "batch certification",
                    "JSON/CSV export",
                    "CI policy gates",
                    "Markdown/JSON reports",
                    "route adapter templates",
                ],
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_interface_solver_engineering_extensions_P",
        status="FAIL",
        summary="Interface solver engineering extensions failed.",
        data={"subchecks": subchecks},
    )


CHECKS = {
    "check_T_engineering_contract_validation_P": check_T_engineering_contract_validation_P,
    "check_T_batch_certification_P": check_T_batch_certification_P,
    "check_T_ci_policy_gate_P": check_T_ci_policy_gate_P,
    "check_T_report_generation_P": check_T_report_generation_P,
    "check_T_route_adapter_templates_P": check_T_route_adapter_templates_P,
    "check_T_interface_solver_engineering_extensions_P": check_T_interface_solver_engineering_extensions_P,
}


def register(registry=None):
    if registry is None:
        return CHECKS
    if hasattr(registry, "update"):
        registry.update(CHECKS)
        return registry
    for name, fn in CHECKS.items():
        if hasattr(registry, "register"):
            registry.register(name, fn)
        elif hasattr(registry, "add"):
            registry.add(name, fn)
        else:
            raise TypeError("Unsupported registry type for interface_solver_engineering_extensions.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
