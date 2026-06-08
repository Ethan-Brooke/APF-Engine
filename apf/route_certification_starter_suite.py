"""
APF Route Certification Starter Suite.

Master route-specific certification harness for:
    - EW trace-to-scheme transport
    - dark-sector posterior/run closure
    - gauge-as-fiber-automorphism route
    - horizon-area-as-fiber-cost route
    - capacity/coarse-graining experiments
    - anti-fitting/provenance audits
"""

from __future__ import annotations

from typing import Dict, Any, Iterable, Mapping, Optional

from apf.ew_trace_scheme_transport_certifier import check_T_EW_trace_scheme_transport_certifier_P
from apf.dark_posterior_certifier import check_T_dark_posterior_certifier_P
from apf.gauge_fiber_route_classifier import check_T_gauge_fiber_route_classifier_P
from apf.horizon_fiber_cost_classifier import check_T_horizon_fiber_cost_classifier_P
from apf.capacity_coarse_grain_experiments import check_T_capacity_coarse_grain_experiments_P
from apf.anti_fitting_provenance_audit import check_T_anti_fitting_provenance_audit_P


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


def route_certifier_results() -> Dict[str, Dict[str, Any]]:
    return {
        "EW_trace_scheme": check_T_EW_trace_scheme_transport_certifier_P(),
        "dark_posterior": check_T_dark_posterior_certifier_P(),
        "gauge_fiber": check_T_gauge_fiber_route_classifier_P(),
        "horizon_fiber_cost": check_T_horizon_fiber_cost_classifier_P(),
        "capacity_coarse_grain": check_T_capacity_coarse_grain_experiments_P(),
        "anti_fitting_provenance": check_T_anti_fitting_provenance_audit_P(),
    }


def check_T_route_certification_starter_suite_P() -> Dict[str, Any]:
    results = route_certifier_results()
    tests = {
        name: result.get("consistent") and result.get("status") == "P_route_cert"
        for name, result in results.items()
    }
    if all(tests.values()):
        return _ok(
            "check_T_route_certification_starter_suite_P",
            status="P_route_suite",
            summary="All route-specific APF certification starters pass.",
            data={
                "tests": tests,
                "route_count": len(results),
                "routes": list(results.keys()),
            },
            dependencies=[result["name"] for result in results.values()],
        )
    return _fail(
        "check_T_route_certification_starter_suite_P",
        status="FAIL",
        summary="One or more route-specific certification starters failed.",
        data={"tests": tests, "results": results},
    )


CHECKS = {"check_T_route_certification_starter_suite_P": check_T_route_certification_starter_suite_P}


def register(registry=None):
    if registry is None:
        return CHECKS
    registry.update(CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, Any]]:
    results = route_certifier_results()
    results["check_T_route_certification_starter_suite_P"] = check_T_route_certification_starter_suite_P()
    return results
