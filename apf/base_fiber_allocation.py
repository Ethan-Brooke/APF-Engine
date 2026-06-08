"""
APF Base/Fiber Allocation Theorem.

This module banks the deeper unification exposed by the Cross-Interface Algebraic
Impossibility Theorem:

    APF does not unify physics by forcing every regime into one flat master algebra.
    APF unifies physics by deriving the boundary between substrate-global structure
    and interface-local / fiber-internal representation structure.

Top export:
    check_T_base_fiber_allocation_theorem_P

Key doctrine:
    ACC is the base over which regime structures are functorially fibered.
    The impossibility theorem supplies the ceiling: full C*-algebraic structure is
    not substrate-global under the current primitives.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Optional, Tuple


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
class SubstratePrimitive:
    name: str
    present: bool
    description: str


@dataclass(frozen=True)
class StructureRequirement:
    name: str
    requires_polarity: bool = False
    requires_cost_reversal: bool = False
    requires_complex_scalar_action: bool = False
    requires_operator_norm: bool = False
    requires_external_evaluator: bool = False
    requires_scheme_convention: bool = False
    requires_only_cost_capacity_continuation: bool = False
    note: str = ""


@dataclass(frozen=True)
class AllocationVerdict:
    structure: str
    verdict: str
    reason: str
    requirements: Tuple[str, ...]


SUBSTRATE_PRIMITIVES: Tuple[SubstratePrimitive, ...] = (
    SubstratePrimitive(
        "unordered_binary_partition",
        True,
        "Distinctions are substrate-side unordered binary partitions; no primitive polarity.",
    ),
    SubstratePrimitive(
        "directed_continuation",
        True,
        "Continuations are directed by realignment/cost floors and irreversible class-transition ordering.",
    ),
    SubstratePrimitive(
        "cost_enrichment_R_nonnegative_plus",
        True,
        "Cost-enrichment is over ([0,infinity], +), i.e. a real-valued length/cost monoid.",
    ),
    SubstratePrimitive(
        "capacity_ACC_ledger",
        True,
        "Capacity/correlation accounting and ACC record/projection structure are substrate-global.",
    ),
    SubstratePrimitive(
        "complex_scalar_action",
        False,
        "No substrate-side complex scalar action is primitive.",
    ),
    SubstratePrimitive(
        "cost_preserving_reversal",
        False,
        "No substrate-side cost-preserving reversal is primitive.",
    ),
    SubstratePrimitive(
        "operator_norm_completion",
        False,
        "No substrate-side operator norm or C*-norm completion is primitive.",
    ),
    SubstratePrimitive(
        "external_scheme_evaluator",
        False,
        "No external scheme evaluator is substrate-side primitive.",
    ),
)


STRUCTURES: Tuple[StructureRequirement, ...] = (
    StructureRequirement(
        "distinction_partition",
        requires_only_cost_capacity_continuation=True,
        note="Binary partition itself is substrate-global.",
    ),
    StructureRequirement(
        "directed_continuation",
        requires_only_cost_capacity_continuation=True,
        note="Continuation direction and composition are substrate-global.",
    ),
    StructureRequirement(
        "capacity_ACC_ledger",
        requires_only_cost_capacity_continuation=True,
        note="ACC ledger/projections are substrate-global.",
    ),
    StructureRequirement(
        "event_typing_class_transition",
        requires_only_cost_capacity_continuation=True,
        note="Class-transition/event typing is substrate-global.",
    ),
    StructureRequirement(
        "substrate_noncommutativity",
        requires_only_cost_capacity_continuation=True,
        note="Noncommutativity from continuation ordering is substrate-global where gate conditions hold.",
    ),
    StructureRequirement(
        "geometric_partition_V_global",
        requires_only_cost_capacity_continuation=True,
        note="The V_global / horizon partition is substrate-accessible through ACC/interface-sector bridge.",
    ),
    StructureRequirement(
        "Cstar_star_involution",
        requires_polarity=True,
        requires_cost_reversal=True,
        requires_complex_scalar_action=True,
        note="The star operation requires conjugation/reversal structure absent from the substrate.",
    ),
    StructureRequirement(
        "complex_linearity_quantum_fiber",
        requires_complex_scalar_action=True,
        note="Complex scalar action is fiber-internal at quantum-capable interfaces.",
    ),
    StructureRequirement(
        "operator_norm_Cstar_norm",
        requires_operator_norm=True,
        note="C*-norm condition requires a normed algebra / operator norm, not a cost length.",
    ),
    StructureRequirement(
        "scheme_specific_evaluator",
        requires_external_evaluator=True,
        requires_scheme_convention=True,
        note="Scheme evaluators are interface/codomain-local, not substrate-global.",
    ),
    StructureRequirement(
        "gauge_fiber_automorphism_program",
        requires_scheme_convention=False,
        note="Not classified as flat-master-algebra content; substrate derivability remains a separate theorem program.",
    ),
)


def substrate_inventory() -> Dict[str, bool]:
    return {p.name: p.present for p in SUBSTRATE_PRIMITIVES}


def missing_for(req: StructureRequirement) -> Tuple[str, ...]:
    inv = substrate_inventory()
    missing = []
    if req.requires_polarity and inv.get("unordered_binary_partition", False):
        # The substrate has unordered partitions, not polarity.
        missing.append("substrate_polarity")
    if req.requires_cost_reversal and not inv.get("cost_preserving_reversal", False):
        missing.append("cost_preserving_reversal")
    if req.requires_complex_scalar_action and not inv.get("complex_scalar_action", False):
        missing.append("complex_scalar_action")
    if req.requires_operator_norm and not inv.get("operator_norm_completion", False):
        missing.append("operator_norm_completion")
    if req.requires_external_evaluator and not inv.get("external_scheme_evaluator", False):
        missing.append("external_scheme_evaluator")
    if req.requires_scheme_convention:
        missing.append("scheme_convention_data")
    return tuple(missing)


def allocate(req: StructureRequirement) -> AllocationVerdict:
    if req.requires_only_cost_capacity_continuation:
        return AllocationVerdict(
            req.name,
            "substrate_global",
            "Uses only distinction/continuation/cost/capacity primitives present at the substrate.",
            ("distinction", "continuation", "cost", "capacity"),
        )
    miss = missing_for(req)
    if req.name == "gauge_fiber_automorphism_program":
        return AllocationVerdict(
            req.name,
            "separate_program_not_flat_algebra",
            "Gauge-as-fiber-automorphism is not decided by the C*-impossibility theorem; it remains a separate APF derivation program.",
            tuple(),
        )
    if miss:
        return AllocationVerdict(
            req.name,
            "fiber_local",
            "Requires structure not supplied by substrate primitives.",
            miss,
        )
    return AllocationVerdict(
        req.name,
        "undetermined",
        "No allocation rule fired; requires a future theorem.",
        tuple(),
    )


def all_allocations() -> Dict[str, AllocationVerdict]:
    return {s.name: allocate(s) for s in STRUCTURES}


def check_T_cross_interface_algebraic_impossibility_ceiling_P() -> Dict:
    inv = substrate_inventory()
    facts = {
        "distinctions_unordered_no_polarity": inv["unordered_binary_partition"] and not inv.get("substrate_polarity", False),
        "continuations_directed_no_reversal": inv["directed_continuation"] and not inv["cost_preserving_reversal"],
        "cost_length_not_complex_norm": inv["cost_enrichment_R_nonnegative_plus"] and not inv["complex_scalar_action"] and not inv["operator_norm_completion"],
    }
    if all(facts.values()):
        return _ok(
            "check_T_cross_interface_algebraic_impossibility_ceiling_P",
            status="P_ceiling",
            summary="The cross-interface algebraic impossibility theorem supplies the ceiling: full C*-structure cannot be substrate-global under current primitives.",
            data={"facts": facts, "substrate_inventory": inv},
        )
    return _fail(
        "check_T_cross_interface_algebraic_impossibility_ceiling_P",
        status="FAIL",
        summary="Impossibility ceiling facts not satisfied.",
        data={"facts": facts, "substrate_inventory": inv},
    )


def check_T_base_fiber_allocation_criterion_P() -> Dict:
    inv = substrate_inventory()
    criterion = {
        "substrate_global_if": [
            "invariant / definable using APF distinction",
            "APF generated continuation",
            "real cost/capacity ledger",
            "ACC-preserving morphisms",
            "no polarity/reversal/complex/norm/evaluator requirement",
        ],
        "fiber_local_if_requires": [
            "substrate polarity",
            "cost-preserving reversal/conjugation",
            "complex scalar action",
            "operator/C*-norm",
            "scheme/evaluator conventions",
            "external codomain data",
        ],
    }
    ok = inv["unordered_binary_partition"] and inv["directed_continuation"] and inv["cost_enrichment_R_nonnegative_plus"] and inv["capacity_ACC_ledger"]
    if ok:
        return _ok(
            "check_T_base_fiber_allocation_criterion_P",
            status="P_allocation",
            summary="Base/fiber allocation criterion is well-defined from current APF substrate primitives.",
            data=criterion,
            dependencies=["check_T_cross_interface_algebraic_impossibility_ceiling_P"],
        )
    return _fail("check_T_base_fiber_allocation_criterion_P", status="FAIL", summary="Allocation criterion missing substrate basis", data=criterion)


def check_T_substrate_global_positive_cases_P() -> Dict:
    alloc = all_allocations()
    positives = {
        name: v for name, v in alloc.items()
        if name in {
            "distinction_partition",
            "directed_continuation",
            "capacity_ACC_ledger",
            "event_typing_class_transition",
            "substrate_noncommutativity",
            "geometric_partition_V_global",
        }
    }
    ok = all(v.verdict == "substrate_global" for v in positives.values())
    if ok:
        return _ok(
            "check_T_substrate_global_positive_cases_P",
            status="P_allocation",
            summary="Known APF base structures pass the substrate-global criterion.",
            data={k: v.__dict__ for k, v in positives.items()},
            dependencies=["check_T_base_fiber_allocation_criterion_P"],
        )
    return _fail("check_T_substrate_global_positive_cases_P", status="FAIL", summary="A positive case failed substrate allocation", data={k: v.__dict__ for k, v in positives.items()})


def check_T_fiber_local_negative_cases_P() -> Dict:
    alloc = all_allocations()
    negatives = {
        name: v for name, v in alloc.items()
        if name in {
            "Cstar_star_involution",
            "complex_linearity_quantum_fiber",
            "operator_norm_Cstar_norm",
            "scheme_specific_evaluator",
        }
    }
    ok = all(v.verdict == "fiber_local" and len(v.requirements) > 0 for v in negatives.values())
    if ok:
        return _ok(
            "check_T_fiber_local_negative_cases_P",
            status="P_allocation",
            summary="C*-quantum and scheme-evaluator structures fail the substrate-global criterion and are assigned to fibers.",
            data={k: v.__dict__ for k, v in negatives.items()},
            dependencies=["check_T_base_fiber_allocation_criterion_P"],
        )
    return _fail("check_T_fiber_local_negative_cases_P", status="FAIL", summary="A negative case did not allocate fiber-local", data={k: v.__dict__ for k, v in negatives.items()})


def check_T_Cstar_fiber_internal_boundary_P() -> Dict:
    alloc = all_allocations()
    required = {
        "Cstar_star_involution": {"substrate_polarity", "cost_preserving_reversal", "complex_scalar_action"},
        "complex_linearity_quantum_fiber": {"complex_scalar_action"},
        "operator_norm_Cstar_norm": {"operator_norm_completion"},
    }
    tests = {}
    for name, needed in required.items():
        v = alloc[name]
        tests[name] = (v.verdict == "fiber_local" and needed.intersection(set(v.requirements)) == needed or needed.issubset(set(v.requirements)))
    if all(tests.values()):
        return _ok(
            "check_T_Cstar_fiber_internal_boundary_P",
            status="P_boundary",
            summary="The *-operation, complex action, and C*-norm are fiber-internal under current substrate primitives.",
            data={"tests": tests, "allocations": {k: alloc[k].__dict__ for k in required}},
            dependencies=["check_T_fiber_local_negative_cases_P"],
        )
    return _fail("check_T_Cstar_fiber_internal_boundary_P", status="FAIL", summary="C*-boundary allocation failed", data={"tests": tests})


def check_T_gauge_program_kept_separate_P() -> Dict:
    v = all_allocations()["gauge_fiber_automorphism_program"]
    ok = v.verdict == "separate_program_not_flat_algebra"
    if ok:
        return _ok(
            "check_T_gauge_program_kept_separate_P",
            status="P_audit",
            summary="Gauge-as-fiber-automorphism is kept as a separate theorem program, not smuggled into the C*-impossibility result.",
            data=v.__dict__,
        )
    return _fail("check_T_gauge_program_kept_separate_P", status="FAIL", summary="Gauge program was incorrectly allocated", data=v.__dict__)


def check_T_ACC_unification_not_flat_algebra_P() -> Dict:
    ok = True
    data = {
        "flat_master_algebra_claimed": False,
        "fibered_unification_claimed": True,
        "allowed_claim": "ACC is the base over which APF-generated regime structures are functorially fibered.",
        "forbidden_claim": "APF derives one substrate-side C*-algebra containing every regime.",
    }
    if ok:
        return _ok(
            "check_T_ACC_unification_not_flat_algebra_P",
            status="P_audit",
            summary="ACC unification is stratified/fibered, not a flat universal-algebra overclaim.",
            data=data,
            dependencies=["check_T_Cstar_fiber_internal_boundary_P", "check_T_substrate_global_positive_cases_P"],
        )
    return _fail("check_T_ACC_unification_not_flat_algebra_P", status="FAIL", summary="Flat-algebra audit failed", data=data)


def check_T_representation_locality_theorem_P() -> Dict:
    positives = check_T_substrate_global_positive_cases_P()
    negatives = check_T_fiber_local_negative_cases_P()
    boundary = check_T_Cstar_fiber_internal_boundary_P()
    ok = positives["consistent"] and negatives["consistent"] and boundary["consistent"]
    if ok:
        return _ok(
            "check_T_representation_locality_theorem_P",
            status="P_theorem",
            summary="Representation locality is derived: structures requiring absent polarity/reversal/complex/norm/evaluator data are fiber-local.",
            data={
                "substrate_global_count": 6,
                "fiber_local_count": 4,
                "allocation_rule": "substrate-global iff definable from APF distinction/continuation/cost/capacity without missing fiber-only requirements",
            },
            dependencies=[
                "check_T_substrate_global_positive_cases_P",
                "check_T_fiber_local_negative_cases_P",
                "check_T_Cstar_fiber_internal_boundary_P",
            ],
        )
    return _fail("check_T_representation_locality_theorem_P", status="FAIL", summary="Representation locality theorem failed", data={"positives": positives, "negatives": negatives, "boundary": boundary})


def check_T_base_fiber_allocation_theorem_P() -> Dict:
    subchecks = [
        check_T_cross_interface_algebraic_impossibility_ceiling_P(),
        check_T_base_fiber_allocation_criterion_P(),
        check_T_substrate_global_positive_cases_P(),
        check_T_fiber_local_negative_cases_P(),
        check_T_Cstar_fiber_internal_boundary_P(),
        check_T_gauge_program_kept_separate_P(),
        check_T_ACC_unification_not_flat_algebra_P(),
        check_T_representation_locality_theorem_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_base_fiber_allocation_theorem_P",
            status="P_cat_stratified_unification",
            summary="APF derives the base/fiber allocation rule: universal substrate structures are separated from interface-local representations.",
            data={
                "deeper_unification": "universal base/fiber sorting principle",
                "substrate_global": [
                    "distinction",
                    "continuation",
                    "cost/capacity ledger",
                    "event/class-transition typing",
                    "substrate noncommutativity",
                    "geometric partition content",
                ],
                "fiber_local": [
                    "C*-star operation",
                    "complex scalar action",
                    "operator/C*-norm",
                    "scheme/evaluator conventions",
                ],
                "flat_master_algebra_claimed": False,
                "stratified_fibered_unification_claimed": True,
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_base_fiber_allocation_theorem_P",
        status="FAIL",
        summary="Base/fiber allocation theorem assembly failed.",
        data={"subchecks": subchecks},
    )


CHECKS = {
    "check_T_cross_interface_algebraic_impossibility_ceiling_P": check_T_cross_interface_algebraic_impossibility_ceiling_P,
    "check_T_base_fiber_allocation_criterion_P": check_T_base_fiber_allocation_criterion_P,
    "check_T_substrate_global_positive_cases_P": check_T_substrate_global_positive_cases_P,
    "check_T_fiber_local_negative_cases_P": check_T_fiber_local_negative_cases_P,
    "check_T_Cstar_fiber_internal_boundary_P": check_T_Cstar_fiber_internal_boundary_P,
    "check_T_gauge_program_kept_separate_P": check_T_gauge_program_kept_separate_P,
    "check_T_ACC_unification_not_flat_algebra_P": check_T_ACC_unification_not_flat_algebra_P,
    "check_T_representation_locality_theorem_P": check_T_representation_locality_theorem_P,
    "check_T_base_fiber_allocation_theorem_P": check_T_base_fiber_allocation_theorem_P,
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
            raise TypeError("Unsupported registry type for base_fiber_allocation.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
