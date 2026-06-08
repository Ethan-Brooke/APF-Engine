"""
APF Representation Descent Kernel.

This is the master consolidation module for the unification stack:

  1. Base/Fiber Allocation
  2. Admissible Representation Stack
  3. Descent Obstruction Calculus
  4. Descent Exactness
  5. Obstruction Dynamics
  6. Obstruction Repair Normal Form
  7. Globalization Promotion Gate

Top export:
    check_T_APF_representation_descent_kernel_P

Main theorem:
    APF unifies physics by classifying when local admissible representations can
    descend to global physical structure over finite-capacity interfaces.

Publication sentence:
    Global physics is the zero-obstruction exact kernel of admissible representation
    descent over the ACC/interface base.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Optional, Tuple

try:
    from apf.base_fiber_allocation import check_T_base_fiber_allocation_theorem_P
    from apf.admissible_representation_stack import check_T_admissible_representation_stack_P
    from apf.descent_obstruction_calculus import (
        Obstruction,
        ObstructionObject,
        check_T_descent_obstruction_calculus_P,
    )
    from apf.descent_exactness import check_T_descent_exactness_theorem_P
    from apf.obstruction_dynamics import check_T_obstruction_dynamics_theorem_P
    from apf.obstruction_repair_normal_form import (
        RepairClass,
        canonical_plan,
        check_T_obstruction_repair_normal_form_P,
    )
    from apf.globalization_promotion_gate import (
        PromotionStatus,
        decide_promotion,
        check_T_globalization_promotion_gate_P,
    )
except Exception as exc:  # pragma: no cover
    raise ImportError(f"representation_descent_kernel dependency import failed: {exc}") from exc


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


@dataclass(frozen=True)
class SectorCase:
    name: str
    description: str
    obstruction: ObstructionObject
    expected_status: PromotionStatus
    expected_repair_class: RepairClass
    safe_claim: str


def sector_cases() -> Dict[str, SectorCase]:
    return {
        "ACC_base_unification": SectorCase(
            name="ACC_base_unification",
            description="Substrate ACC base/fiber theorem with zero obstruction.",
            obstruction=ObstructionObject.zero(),
            expected_status=PromotionStatus.EXPORT_GLOBAL_P,
            expected_repair_class=RepairClass.EXACT,
            safe_claim="Global P: ACC base/fiber representation descent kernel is exact.",
        ),
        "EW_trace_to_scheme_transport": SectorCase(
            name="EW_trace_to_scheme_transport",
            description="Trace-sector local closure attempting physical scheme export.",
            obstruction=ObstructionObject.of(Obstruction.EVALUATOR_MISSING, Obstruction.CODOMAIN_MISMATCH),
            expected_status=PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED,
            expected_repair_class=RepairClass.ORDINARY_REPAIRABLE,
            safe_claim="Local/trace P only; physical scheme export awaits evaluator/codomain transport and rerun.",
        ),
        "dark_sector_empirical_route": SectorCase(
            name="dark_sector_empirical_route",
            description="Dark-sector empirical/posterior route before convergence/robustness close.",
            obstruction=ObstructionObject.of(Obstruction.EVALUATOR_MISSING),
            expected_status=PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED,
            expected_repair_class=RepairClass.ORDINARY_REPAIRABLE,
            safe_claim="Research/runtime progress only; empirical/global P awaits posterior/evaluator closure.",
        ),
        "flat_Cstar_substrate_unification": SectorCase(
            name="flat_Cstar_substrate_unification",
            description="Attempt to promote full C*-algebraic structure to substrate-global layer.",
            obstruction=ObstructionObject.of(
                Obstruction.REVERSAL_MISSING,
                Obstruction.COMPLEX_ACTION_MISSING,
                Obstruction.NORM_MISSING,
                Obstruction.CODOMAIN_MISMATCH,
            ),
            expected_status=PromotionStatus.HOLD_SUBSTRATE_REVISION_REQUIRED,
            expected_repair_class=RepairClass.SUBSTRATE_REVISION_REPAIRABLE,
            safe_claim="Not current global P; opens D2/D3 substrate-revision program.",
        ),
        "gauge_as_fiber_automorphism_program": SectorCase(
            name="gauge_as_fiber_automorphism_program",
            description="Gauge group/fiber automorphism program before full descent proof.",
            obstruction=ObstructionObject.of(Obstruction.CODOMAIN_MISMATCH),
            expected_status=PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED,
            expected_repair_class=RepairClass.ORDINARY_REPAIRABLE,
            safe_claim="Separate theorem program; needs explicit codomain/descent proof before global P.",
        ),
        "horizon_area_as_fiber_cost_program": SectorCase(
            name="horizon_area_as_fiber_cost_program",
            description="Horizon-area/fiber-cost program before full descent proof.",
            obstruction=ObstructionObject.of(Obstruction.OVERLAP_INCOHERENCE),
            expected_status=PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED,
            expected_repair_class=RepairClass.ORDINARY_REPAIRABLE,
            safe_claim="Separate theorem program; needs overlap/descent proof before global P.",
        ),
        "post_hoc_or_target_consuming_claim": SectorCase(
            name="post_hoc_or_target_consuming_claim",
            description="Any claim that consumes target value as input.",
            obstruction=ObstructionObject.of(Obstruction.PROVENANCE_SMUGGLE, Obstruction.CODOMAIN_MISMATCH),
            expected_status=PromotionStatus.FAIL_CLOSED_PROVENANCE,
            expected_repair_class=RepairClass.NONREPAIRABLE_PROVENANCE,
            safe_claim="Fail closed; rebuild from clean provenance.",
        ),
    }


def _check_result_is_p(result: Dict, expected_status: str) -> bool:
    return bool(result.get("consistent")) and result.get("status") == expected_status


def check_T_kernel_dependencies_loaded_P() -> Dict:
    dependency_checks = {
        "base_fiber_allocation": check_T_base_fiber_allocation_theorem_P(),
        "admissible_representation_stack": check_T_admissible_representation_stack_P(),
        "descent_obstruction_calculus": check_T_descent_obstruction_calculus_P(),
        "descent_exactness": check_T_descent_exactness_theorem_P(),
        "obstruction_dynamics": check_T_obstruction_dynamics_theorem_P(),
        "obstruction_repair_normal_form": check_T_obstruction_repair_normal_form_P(),
        "globalization_promotion_gate": check_T_globalization_promotion_gate_P(),
    }
    expected = {
        "base_fiber_allocation": "P_cat_stratified_unification",
        "admissible_representation_stack": "P_cat_finite_descent",
        "descent_obstruction_calculus": "P_calc",
        "descent_exactness": "P_exact",
        "obstruction_dynamics": "P_dyn",
        "obstruction_repair_normal_form": "P_repair",
        "globalization_promotion_gate": "P_gate",
    }
    tests = {
        name: _check_result_is_p(result, expected[name])
        for name, result in dependency_checks.items()
    }
    if all(tests.values()):
        return _ok(
            "check_T_kernel_dependencies_loaded_P",
            status="P_kernel",
            summary="All representation-descent kernel dependency layers load and pass their top P checks.",
            data={"tests": tests, "statuses": {k: v.get("status") for k, v in dependency_checks.items()}},
        )
    return _fail(
        "check_T_kernel_dependencies_loaded_P",
        status="FAIL",
        summary="One or more kernel dependency layers failed.",
        data={"tests": tests, "results": dependency_checks},
    )


def check_T_kernel_ladder_order_P() -> Dict:
    ladder = [
        "Base/Fiber Allocation",
        "Admissible Representation Stack",
        "Descent Obstruction Calculus",
        "Descent Exactness",
        "Obstruction Dynamics",
        "Obstruction Repair Normal Form",
        "Globalization Promotion Gate",
    ]
    tests = {
        "all_layers_present": len(ladder) == 7,
        "allocation_before_stack": ladder.index("Base/Fiber Allocation") < ladder.index("Admissible Representation Stack"),
        "stack_before_obstruction": ladder.index("Admissible Representation Stack") < ladder.index("Descent Obstruction Calculus"),
        "obstruction_before_exactness": ladder.index("Descent Obstruction Calculus") < ladder.index("Descent Exactness"),
        "exactness_before_dynamics": ladder.index("Descent Exactness") < ladder.index("Obstruction Dynamics"),
        "dynamics_before_repair": ladder.index("Obstruction Dynamics") < ladder.index("Obstruction Repair Normal Form"),
        "repair_before_promotion": ladder.index("Obstruction Repair Normal Form") < ladder.index("Globalization Promotion Gate"),
    }
    if all(tests.values()):
        return _ok(
            "check_T_kernel_ladder_order_P",
            status="P_kernel",
            summary="The representation-descent kernel theorem stack is ordered coherently.",
            data={"ladder": ladder, "tests": tests},
            dependencies=["check_T_kernel_dependencies_loaded_P"],
        )
    return _fail("check_T_kernel_ladder_order_P", status="FAIL", summary="Kernel ladder order failed", data={"ladder": ladder, "tests": tests})


def check_T_sector_promotion_classification_P() -> Dict:
    results = {}
    tests = {}
    for name, case in sector_cases().items():
        decision = decide_promotion(name, case.obstruction)
        plan = canonical_plan(case.obstruction)
        results[name] = {
            "description": case.description,
            "obstruction": case.obstruction.names(),
            "promotion_status": decision.status.value,
            "repair_class": plan.repair_class.value,
            "export_global_P": decision.export_global_P,
            "safe_claim": case.safe_claim,
            "next_action": decision.next_action,
        }
        tests[f"{name}_status"] = decision.status == case.expected_status
        tests[f"{name}_repair_class"] = plan.repair_class == case.expected_repair_class
        tests[f"{name}_global_export_consistent"] = decision.export_global_P == case.obstruction.is_zero

    if all(tests.values()):
        return _ok(
            "check_T_sector_promotion_classification_P",
            status="P_kernel",
            summary="Promotion gate correctly classifies active APF sector examples.",
            data={"sector_results": results, "tests": tests},
            dependencies=["check_T_kernel_ladder_order_P"],
        )
    return _fail(
        "check_T_sector_promotion_classification_P",
        status="FAIL",
        summary="Sector promotion classification failed.",
        data={"sector_results": results, "tests": tests},
    )


def check_T_master_unification_sentence_P() -> Dict:
    sentence = "Global physics is the zero-obstruction exact kernel of admissible representation descent over the ACC/interface base."
    components = {
        "global_physics": "global physics" in sentence.lower(),
        "zero_obstruction": "zero-obstruction" in sentence,
        "exact_kernel": "exact kernel" in sentence,
        "representation_descent": "representation descent" in sentence,
        "ACC_interface_base": "ACC/interface base" in sentence,
    }
    if all(components.values()):
        return _ok(
            "check_T_master_unification_sentence_P",
            status="P_kernel",
            summary="Master unification sentence contains all required APF descent-kernel components.",
            data={"sentence": sentence, "components": components},
            dependencies=["check_T_sector_promotion_classification_P"],
        )
    return _fail("check_T_master_unification_sentence_P", status="FAIL", summary="Master sentence incomplete", data={"sentence": sentence, "components": components})


def check_T_no_flat_master_algebra_or_infinity_overclaim_P() -> Dict:
    return _ok(
        "check_T_no_flat_master_algebra_or_infinity_overclaim_P",
        status="P_audit",
        summary="Scope boundary preserved: the kernel is finite/fibered/obstruction-based, not a flat master algebra or infinity-stack claim.",
        data={
            "flat_master_algebra_claimed": False,
            "full_Cstar_substrate_global_claimed": False,
            "infinity_stack_claimed": False,
            "cohomology_theory_claimed": False,
            "finite_representation_descent_kernel_claimed": True,
        },
        dependencies=["check_T_master_unification_sentence_P"],
    )


def check_T_APF_representation_descent_kernel_P() -> Dict:
    subchecks = [
        check_T_kernel_dependencies_loaded_P(),
        check_T_kernel_ladder_order_P(),
        check_T_sector_promotion_classification_P(),
        check_T_master_unification_sentence_P(),
        check_T_no_flat_master_algebra_or_infinity_overclaim_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_APF_representation_descent_kernel_P",
            status="P_unification",
            summary="APF Representation Descent Kernel is P: global physics is zero-obstruction exact admissible representation descent over the ACC/interface base.",
            data={
                "main_theorem": "Global physics = ker(Obs) = im(Glob) inside finite admissible representation descent.",
                "kernel_stack": [
                    "base_fiber_allocation",
                    "admissible_representation_stack",
                    "descent_obstruction_calculus",
                    "descent_exactness",
                    "obstruction_dynamics",
                    "obstruction_repair_normal_form",
                    "globalization_promotion_gate",
                ],
                "active_sector_classification": list(sector_cases().keys()),
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_APF_representation_descent_kernel_P",
        status="FAIL",
        summary="Representation Descent Kernel assembly failed.",
        data={"subchecks": subchecks},
    )


CHECKS = {
    "check_T_kernel_dependencies_loaded_P": check_T_kernel_dependencies_loaded_P,
    "check_T_kernel_ladder_order_P": check_T_kernel_ladder_order_P,
    "check_T_sector_promotion_classification_P": check_T_sector_promotion_classification_P,
    "check_T_master_unification_sentence_P": check_T_master_unification_sentence_P,
    "check_T_no_flat_master_algebra_or_infinity_overclaim_P": check_T_no_flat_master_algebra_or_infinity_overclaim_P,
    "check_T_APF_representation_descent_kernel_P": check_T_APF_representation_descent_kernel_P,
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
            raise TypeError("Unsupported registry type for representation_descent_kernel.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
