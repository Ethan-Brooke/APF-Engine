"""
APF Obstruction Repair Normal Form.

This module banks the next layer after Obstruction Dynamics.

Dynamics says how obstruction channels transform.
Repair Normal Form says which minimal operation sets move an obstruction object into
the exact kernel, or certify that no mathematical repair is allowed.

Top theorem:
    check_T_obstruction_repair_normal_form_P

Core claim:
    Every finite obstruction object has a canonical APF repair normal form:
      - exact if already zero;
      - minimally repairable by ordinary declared/coarse operations;
      - repairable only by substrate-revision operations;
      - non-repairable by mathematics if provenance smuggling is present.

Scope:
    finite normal-form / minimal-hitting-set calculus over the current obstruction channels.
    Not an optimization theory over physical time, and not a proof that substrate revisions
    are available; D1/D2/D3 are counterfactual dissolution routes.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from itertools import combinations
from typing import Dict, FrozenSet, Iterable, Mapping, Optional, Tuple, List

try:
    from apf.descent_obstruction_calculus import Obstruction, ObstructionObject
    from apf.obstruction_dynamics import Operation, transform, compose_transform
except Exception as exc:  # pragma: no cover
    raise ImportError(f"obstruction_repair_normal_form dependencies missing: {exc}") from exc


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


class RepairClass(str, Enum):
    EXACT = "EXACT"
    ORDINARY_REPAIRABLE = "ORDINARY_REPAIRABLE"
    SUBSTRATE_REVISION_REPAIRABLE = "SUBSTRATE_REVISION_REPAIRABLE"
    NONREPAIRABLE_PROVENANCE = "NONREPAIRABLE_PROVENANCE"
    UNKNOWN_UNSUPPORTED = "UNKNOWN_UNSUPPORTED"
    # v24.3.41 — Mass-sector Step D audit Finding 2:
    # NON_REPAIRABLE_BY_DESIGN: route closed because codomain itself is rejected
    # (heavy-quark pole-mass routes; renormalon-uncontrolled codomain). Distinct from
    # NONREPAIRABLE_PROVENANCE (target-smuggling fail-closed, not a codomain rejection).
    NON_REPAIRABLE_BY_DESIGN = "NON_REPAIRABLE_BY_DESIGN"


ORDINARY_OPERATIONS: Tuple[Operation, ...] = (
    Operation.COARSE_GRAINING,
    Operation.EVALUATOR_TRANSPORT,
    Operation.CODOMAIN_DECLARATION,
)

SUBSTRATE_REVISION_OPERATIONS: Tuple[Operation, ...] = (
    Operation.SUBSTRATE_REVISION_D1_POLARITY,
    Operation.SUBSTRATE_REVISION_D2_REVERSAL,
    Operation.SUBSTRATE_REVISION_D3_COMPLEX_NORM,
)

REPAIR_OPERATIONS: Tuple[Operation, ...] = ORDINARY_OPERATIONS + SUBSTRATE_REVISION_OPERATIONS

OPERATION_PRIORITY = {
    Operation.EVALUATOR_TRANSPORT: 0,
    Operation.CODOMAIN_DECLARATION: 1,
    Operation.COARSE_GRAINING: 2,
    Operation.SUBSTRATE_REVISION_D1_POLARITY: 3,
    Operation.SUBSTRATE_REVISION_D2_REVERSAL: 4,
    Operation.SUBSTRATE_REVISION_D3_COMPLEX_NORM: 5,
}


def op_sort_key(ops: Tuple[Operation, ...]) -> Tuple:
    return (len(ops), tuple(OPERATION_PRIORITY[op] for op in ops), tuple(op.value for op in ops))



@dataclass(frozen=True)
class RepairPlan:
    obstruction: ObstructionObject
    repair_class: RepairClass
    operations: Tuple[Operation, ...]
    final_obstruction: ObstructionObject
    note: str

    @property
    def succeeds(self) -> bool:
        return self.final_obstruction.is_zero


def apply_ops(obs: ObstructionObject, ops: Tuple[Operation, ...]) -> ObstructionObject:
    out = obs
    for op in ops:
        out = transform(out, op)
    return out


def _is_minimal_success(obs: ObstructionObject, ops: Tuple[Operation, ...]) -> bool:
    if not apply_ops(obs, ops).is_zero:
        return False
    for k in range(len(ops)):
        for sub in combinations(ops, k):
            if apply_ops(obs, tuple(sub)).is_zero:
                return False
    return True


def minimal_success_sets(obs: ObstructionObject, operations: Tuple[Operation, ...]) -> Tuple[Tuple[Operation, ...], ...]:
    """Return all inclusion/cardinality-minimal operation sets that send obs to zero."""
    if obs.is_zero:
        return ((),)
    successes: List[Tuple[Operation, ...]] = []
    for r in range(1, len(operations) + 1):
        for ops in combinations(operations, r):
            if apply_ops(obs, tuple(ops)).is_zero and _is_minimal_success(obs, tuple(ops)):
                successes.append(tuple(ops))
        if successes:
            return tuple(successes)
    return tuple()


def canonical_plan(obs: ObstructionObject) -> RepairPlan:
    """Canonical repair normal form.

    Priority:
      1. exact zero
      2. provenance-smuggled -> nonrepairable
      3. ordinary minimal repair
      4. substrate-revision minimal repair
      5. unsupported
    """
    if obs.is_zero:
        return RepairPlan(obs, RepairClass.EXACT, tuple(), obs, "Already in the exact kernel.")

    if Obstruction.PROVENANCE_SMUGGLE in obs.channels:
        # By the dynamics theorem, provenance is absorbing under mathematical repair.
        # We intentionally do not offer any operation as a repair.
        return RepairPlan(
            obs,
            RepairClass.NONREPAIRABLE_PROVENANCE,
            tuple(),
            obs,
            "Provenance smuggling is absorbing; no mathematical repair normal form is allowed.",
        )

    ordinary = minimal_success_sets(obs, ORDINARY_OPERATIONS)
    if ordinary:
        ops = sorted(ordinary, key=op_sort_key)[0]
        return RepairPlan(
            obs,
            RepairClass.ORDINARY_REPAIRABLE,
            ops,
            apply_ops(obs, ops),
            "Obstruction is repairable by ordinary APF coarse/evaluator/codomain operations.",
        )

    extended = minimal_success_sets(obs, REPAIR_OPERATIONS)
    if extended:
        ops = sorted(extended, key=op_sort_key)[0]
        return RepairPlan(
            obs,
            RepairClass.SUBSTRATE_REVISION_REPAIRABLE,
            ops,
            apply_ops(obs, ops),
            "Obstruction is repairable only with substrate-revision dissolution routes.",
        )

    return RepairPlan(
        obs,
        RepairClass.UNKNOWN_UNSUPPORTED,
        tuple(),
        obs,
        "No current APF repair operation set sends this obstruction to zero.",
    )


def example_obstructions() -> Dict[str, ObstructionObject]:
    return {
        "exact": ObstructionObject.zero(),
        "capacity": ObstructionObject.of(Obstruction.CAPACITY_OVERSPEND),
        "contextual": ObstructionObject.of(Obstruction.OVERLAP_INCOHERENCE),
        "codomain": ObstructionObject.of(Obstruction.CODOMAIN_MISMATCH),
        "scheme": ObstructionObject.of(Obstruction.EVALUATOR_MISSING, Obstruction.CODOMAIN_MISMATCH),
        "cstar": ObstructionObject.of(
            Obstruction.REVERSAL_MISSING,
            Obstruction.COMPLEX_ACTION_MISSING,
            Obstruction.NORM_MISSING,
            Obstruction.CODOMAIN_MISMATCH,
        ),
        "polarity": ObstructionObject.of(Obstruction.POLARITY_MISSING),
        "smuggled": ObstructionObject.of(Obstruction.PROVENANCE_SMUGGLE, Obstruction.CODOMAIN_MISMATCH),
        "mixed_structural_logistical": ObstructionObject.of(
            Obstruction.COMPLEX_ACTION_MISSING,
            Obstruction.NORM_MISSING,
            Obstruction.CAPACITY_OVERSPEND,
            Obstruction.CODOMAIN_MISMATCH,
        ),
    }


def plan_data(plan: RepairPlan) -> Dict:
    return {
        "before": plan.obstruction.names(),
        "class": plan.repair_class.value,
        "operations": tuple(op.value for op in plan.operations),
        "after": plan.final_obstruction.names(),
        "succeeds": plan.succeeds,
        "note": plan.note,
    }


def check_T_repair_operations_cover_channels_P() -> Dict:
    # Verify every non-provenance obstruction channel in the current calculus has a
    # channel-removing path in ordinary or substrate-revision operations.
    channel_examples = {
        Obstruction.CAPACITY_OVERSPEND: ObstructionObject.of(Obstruction.CAPACITY_OVERSPEND),
        Obstruction.CODOMAIN_MISMATCH: ObstructionObject.of(Obstruction.CODOMAIN_MISMATCH),
        Obstruction.OVERLAP_INCOHERENCE: ObstructionObject.of(Obstruction.OVERLAP_INCOHERENCE),
        Obstruction.EVALUATOR_MISSING: ObstructionObject.of(Obstruction.EVALUATOR_MISSING),
        Obstruction.POLARITY_MISSING: ObstructionObject.of(Obstruction.POLARITY_MISSING),
        Obstruction.REVERSAL_MISSING: ObstructionObject.of(Obstruction.REVERSAL_MISSING),
        Obstruction.COMPLEX_ACTION_MISSING: ObstructionObject.of(Obstruction.COMPLEX_ACTION_MISSING),
        Obstruction.NORM_MISSING: ObstructionObject.of(Obstruction.NORM_MISSING),
    }
    results = {ch.value: canonical_plan(obs).succeeds for ch, obs in channel_examples.items()}
    provenance = canonical_plan(ObstructionObject.of(Obstruction.PROVENANCE_SMUGGLE))
    tests = {
        "all_non_provenance_channels_have_repair_path": all(results.values()),
        "provenance_is_not_repaired": not provenance.succeeds and provenance.repair_class == RepairClass.NONREPAIRABLE_PROVENANCE,
    }
    if all(tests.values()):
        return _ok(
            "check_T_repair_operations_cover_channels_P",
            status="P_repair",
            summary="All non-provenance obstruction channels have a finite repair path; provenance smuggling is correctly nonrepairable.",
            data={"channel_results": results, "provenance": plan_data(provenance), "tests": tests},
        )
    return _fail("check_T_repair_operations_cover_channels_P", status="FAIL", summary="Repair operation coverage failed", data={"channel_results": results, "provenance": plan_data(provenance), "tests": tests})


def check_T_minimal_repair_plan_soundness_P() -> Dict:
    plans = {name: canonical_plan(obs) for name, obs in example_obstructions().items()}
    tests = {}
    for name, plan in plans.items():
        if plan.repair_class in {RepairClass.EXACT, RepairClass.ORDINARY_REPAIRABLE, RepairClass.SUBSTRATE_REVISION_REPAIRABLE}:
            tests[name] = plan.final_obstruction.is_zero
        elif plan.repair_class == RepairClass.NONREPAIRABLE_PROVENANCE:
            tests[name] = Obstruction.PROVENANCE_SMUGGLE in plan.obstruction.channels and not plan.succeeds
        else:
            tests[name] = False

    if all(tests.values()):
        return _ok(
            "check_T_minimal_repair_plan_soundness_P",
            status="P_repair",
            summary="Canonical repair plans are sound: success plans reach zero; provenance failures remain nonzero.",
            data={name: plan_data(plan) for name, plan in plans.items()},
            dependencies=["check_T_repair_operations_cover_channels_P"],
        )
    return _fail("check_T_minimal_repair_plan_soundness_P", status="FAIL", summary="Repair plan soundness failed", data={"tests": tests, "plans": {n: plan_data(p) for n, p in plans.items()}})


def check_T_minimality_certificate_P() -> Dict:
    # For all repairable examples, canonical plan must be inclusion/cardinality minimal.
    plans = {name: canonical_plan(obs) for name, obs in example_obstructions().items()}
    tests = {}
    for name, plan in plans.items():
        if plan.repair_class == RepairClass.EXACT:
            tests[name] = plan.operations == tuple()
        elif plan.repair_class == RepairClass.ORDINARY_REPAIRABLE:
            tests[name] = _is_minimal_success(plan.obstruction, plan.operations)
        elif plan.repair_class == RepairClass.SUBSTRATE_REVISION_REPAIRABLE:
            tests[name] = _is_minimal_success(plan.obstruction, plan.operations)
        elif plan.repair_class == RepairClass.NONREPAIRABLE_PROVENANCE:
            tests[name] = plan.operations == tuple() and not plan.succeeds
        else:
            tests[name] = False

    if all(tests.values()):
        return _ok(
            "check_T_minimality_certificate_P",
            status="P_repair",
            summary="Canonical repair normal forms are minimal for the finite operation set.",
            data={"tests": tests, "plans": {n: plan_data(p) for n, p in plans.items()}},
            dependencies=["check_T_minimal_repair_plan_soundness_P"],
        )
    return _fail("check_T_minimality_certificate_P", status="FAIL", summary="Minimality certificate failed", data={"tests": tests, "plans": {n: plan_data(p) for n, p in plans.items()}})


def check_T_ordinary_vs_substrate_revision_boundary_P() -> Dict:
    plans = {name: canonical_plan(obs) for name, obs in example_obstructions().items()}
    tests = {
        "capacity_is_ordinary": plans["capacity"].repair_class == RepairClass.ORDINARY_REPAIRABLE,
        "contextual_is_ordinary": plans["contextual"].repair_class == RepairClass.ORDINARY_REPAIRABLE,
        "scheme_is_ordinary": plans["scheme"].repair_class == RepairClass.ORDINARY_REPAIRABLE,
        "cstar_requires_substrate_revision": plans["cstar"].repair_class == RepairClass.SUBSTRATE_REVISION_REPAIRABLE,
        "polarity_requires_substrate_revision": plans["polarity"].repair_class == RepairClass.SUBSTRATE_REVISION_REPAIRABLE,
        "smuggled_nonrepairable": plans["smuggled"].repair_class == RepairClass.NONREPAIRABLE_PROVENANCE,
    }
    if all(tests.values()):
        return _ok(
            "check_T_ordinary_vs_substrate_revision_boundary_P",
            status="P_boundary",
            summary="Repair normal form separates ordinary logistical repair from substrate-revision repair and nonrepairable provenance failures.",
            data={"tests": tests, "plans": {n: plan_data(p) for n, p in plans.items()}},
            dependencies=["check_T_minimality_certificate_P"],
        )
    return _fail("check_T_ordinary_vs_substrate_revision_boundary_P", status="FAIL", summary="Ordinary/substrate boundary failed", data={"tests": tests, "plans": {n: plan_data(p) for n, p in plans.items()}})


def check_T_Cstar_repair_requires_D2D3_P() -> Dict:
    cstar = example_obstructions()["cstar"]
    plan = canonical_plan(cstar)
    ops = set(plan.operations)
    tests = {
        "requires_substrate_revision_class": plan.repair_class == RepairClass.SUBSTRATE_REVISION_REPAIRABLE,
        "contains_D2_reversal": Operation.SUBSTRATE_REVISION_D2_REVERSAL in ops,
        "contains_D3_complex_norm": Operation.SUBSTRATE_REVISION_D3_COMPLEX_NORM in ops,
        "contains_codomain_repair": Operation.CODOMAIN_DECLARATION in ops,
        "does_not_require_D1": Operation.SUBSTRATE_REVISION_D1_POLARITY not in ops,
        "reaches_zero": plan.succeeds,
    }
    if all(tests.values()):
        return _ok(
            "check_T_Cstar_repair_requires_D2D3_P",
            status="P_repair",
            summary="Flat C*-globalization can reach the exact kernel only under D2/D3 substrate revision plus codomain declaration.",
            data={"plan": plan_data(plan), "tests": tests},
            dependencies=["check_T_ordinary_vs_substrate_revision_boundary_P"],
        )
    return _fail("check_T_Cstar_repair_requires_D2D3_P", status="FAIL", summary="Cstar repair route failed", data={"plan": plan_data(plan), "tests": tests})


def check_T_provenance_no_repair_certificate_P() -> Dict:
    smuggled = example_obstructions()["smuggled"]
    plan = canonical_plan(smuggled)
    # Exhaustively confirm all non-contaminating repair operations do not remove provenance.
    all_ops = REPAIR_OPERATIONS
    exhaustive = []
    for r in range(len(all_ops) + 1):
        for ops in combinations(all_ops, r):
            after = apply_ops(smuggled, tuple(ops))
            exhaustive.append(Obstruction.PROVENANCE_SMUGGLE in after.channels and not after.is_zero)
    tests = {
        "classified_nonrepairable": plan.repair_class == RepairClass.NONREPAIRABLE_PROVENANCE,
        "no_plan_operations": plan.operations == tuple(),
        "exhaustive_repairs_do_not_remove_provenance": all(exhaustive),
    }
    if all(tests.values()):
        return _ok(
            "check_T_provenance_no_repair_certificate_P",
            status="P_audit",
            summary="No finite mathematical repair operation set removes provenance smuggling.",
            data={"plan": plan_data(plan), "tested_operation_subsets": len(exhaustive), "tests": tests},
            dependencies=["check_T_minimality_certificate_P"],
        )
    return _fail("check_T_provenance_no_repair_certificate_P", status="FAIL", summary="Provenance no-repair certificate failed", data={"plan": plan_data(plan), "tests": tests})


def check_T_kernel_repair_normalization_P() -> Dict:
    plans = {name: canonical_plan(obs) for name, obs in example_obstructions().items()}
    normalized = {
        name: plan.final_obstruction.is_zero if plan.repair_class != RepairClass.NONREPAIRABLE_PROVENANCE else False
        for name, plan in plans.items()
    }
    tests = {
        "all_repairable_normalize_to_kernel": all(
            p.final_obstruction.is_zero
            for p in plans.values()
            if p.repair_class in {RepairClass.EXACT, RepairClass.ORDINARY_REPAIRABLE, RepairClass.SUBSTRATE_REVISION_REPAIRABLE}
        ),
        "nonrepairable_does_not_normalize": not normalized["smuggled"],
        "no_unknowns": all(p.repair_class != RepairClass.UNKNOWN_UNSUPPORTED for p in plans.values()),
    }
    if all(tests.values()):
        return _ok(
            "check_T_kernel_repair_normalization_P",
            status="P_repair",
            summary="Every repairable obstruction has a canonical normalization path into the exact kernel; provenance failures do not.",
            data={"normalized": normalized, "plans": {n: plan_data(p) for n, p in plans.items()}, "tests": tests},
            dependencies=[
                "check_T_Cstar_repair_requires_D2D3_P",
                "check_T_provenance_no_repair_certificate_P",
            ],
        )
    return _fail("check_T_kernel_repair_normalization_P", status="FAIL", summary="Kernel repair normalization failed", data={"normalized": normalized, "plans": {n: plan_data(p) for n, p in plans.items()}, "tests": tests})


def check_T_no_optimization_overclaim_P() -> Dict:
    return _ok(
        "check_T_no_optimization_overclaim_P",
        status="P_audit",
        summary="Scope boundary preserved: repair normal form is finite minimality over declared operations, not a physical optimization principle.",
        data={
            "physical_time_optimization_claimed": False,
            "global_optimality_over_all_possible_math_claimed": False,
            "finite_declared_operation_minimality_claimed": True,
            "substrate_revisions_available_claimed": False,
            "D1D2D3_status": "counterfactual dissolution routes, not current primitives",
        },
    )


def check_T_obstruction_repair_normal_form_P() -> Dict:
    subchecks = [
        check_T_repair_operations_cover_channels_P(),
        check_T_minimal_repair_plan_soundness_P(),
        check_T_minimality_certificate_P(),
        check_T_ordinary_vs_substrate_revision_boundary_P(),
        check_T_Cstar_repair_requires_D2D3_P(),
        check_T_provenance_no_repair_certificate_P(),
        check_T_kernel_repair_normalization_P(),
        check_T_no_optimization_overclaim_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_obstruction_repair_normal_form_P",
            status="P_repair",
            summary="Every finite obstruction object has a canonical repair normal form or a nonrepairability certificate.",
            data={
                "main_claim": "minimal repair plan normalizes repairable obstructions into ker(Obs)",
                "classes": [c.value for c in RepairClass],
                "nonrepairable_channel": Obstruction.PROVENANCE_SMUGGLE.value,
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_obstruction_repair_normal_form_P",
        status="FAIL",
        summary="Obstruction repair normal form theorem assembly failed.",
        data={"subchecks": subchecks},
    )


CHECKS = {
    "check_T_repair_operations_cover_channels_P": check_T_repair_operations_cover_channels_P,
    "check_T_minimal_repair_plan_soundness_P": check_T_minimal_repair_plan_soundness_P,
    "check_T_minimality_certificate_P": check_T_minimality_certificate_P,
    "check_T_ordinary_vs_substrate_revision_boundary_P": check_T_ordinary_vs_substrate_revision_boundary_P,
    "check_T_Cstar_repair_requires_D2D3_P": check_T_Cstar_repair_requires_D2D3_P,
    "check_T_provenance_no_repair_certificate_P": check_T_provenance_no_repair_certificate_P,
    "check_T_kernel_repair_normalization_P": check_T_kernel_repair_normalization_P,
    "check_T_no_optimization_overclaim_P": check_T_no_optimization_overclaim_P,
    "check_T_obstruction_repair_normal_form_P": check_T_obstruction_repair_normal_form_P,
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
            raise TypeError("Unsupported registry type for obstruction_repair_normal_form.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
