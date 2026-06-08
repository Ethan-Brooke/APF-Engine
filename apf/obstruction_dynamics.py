"""
APF Obstruction Dynamics Theorem.

This module banks the next layer after Descent Exactness.

Exactness says:
    global physics = ker(Obs)

Obstruction dynamics says:
    how finite obstruction objects transform under APF operations:
      - refinement
      - coarse-graining
      - declared evaluator/codomain transport
      - substrate revision
      - provenance contamination

Scope:
    finite channel dynamics over the current APF obstruction calculus.
    This is not a flow equation in physical time and not a cohomological spectral sequence.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, FrozenSet, Iterable, Mapping, Optional, Tuple

try:
    from apf.descent_obstruction_calculus import Obstruction, ObstructionObject
except Exception as exc:  # pragma: no cover
    raise ImportError(f"obstruction_dynamics requires apf.descent_obstruction_calculus: {exc}") from exc


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


class Operation(str, Enum):
    REFINEMENT = "REFINEMENT"
    COARSE_GRAINING = "COARSE_GRAINING"
    EVALUATOR_TRANSPORT = "EVALUATOR_TRANSPORT"
    SUBSTRATE_REVISION_D1_POLARITY = "SUBSTRATE_REVISION_D1_POLARITY"
    SUBSTRATE_REVISION_D2_REVERSAL = "SUBSTRATE_REVISION_D2_REVERSAL"
    SUBSTRATE_REVISION_D3_COMPLEX_NORM = "SUBSTRATE_REVISION_D3_COMPLEX_NORM"
    PROVENANCE_CONTAMINATION = "PROVENANCE_CONTAMINATION"
    CODOMAIN_DECLARATION = "CODOMAIN_DECLARATION"


STRUCTURAL_CHANNELS = frozenset({
    Obstruction.POLARITY_MISSING,
    Obstruction.REVERSAL_MISSING,
    Obstruction.COMPLEX_ACTION_MISSING,
    Obstruction.NORM_MISSING,
})

LOGISTICAL_CHANNELS = frozenset({
    Obstruction.EVALUATOR_MISSING,
    Obstruction.CAPACITY_OVERSPEND,
    Obstruction.CODOMAIN_MISMATCH,
    Obstruction.OVERLAP_INCOHERENCE,
})

ABSORBING_CHANNELS = frozenset({
    Obstruction.PROVENANCE_SMUGGLE,
})


@dataclass(frozen=True)
class DynamicsStep:
    name: str
    operation: Operation
    before: ObstructionObject
    after: ObstructionObject
    note: str


def remove_channels(obs: ObstructionObject, channels: FrozenSet[Obstruction]) -> ObstructionObject:
    return ObstructionObject(frozenset(ch for ch in obs.channels if ch not in channels))


def add_channels(obs: ObstructionObject, channels: FrozenSet[Obstruction]) -> ObstructionObject:
    return ObstructionObject(frozenset(obs.channels | channels))


def transform(obs: ObstructionObject, operation: Operation) -> ObstructionObject:
    """Finite obstruction dynamics.

    Design:
      * Refinement can reveal hidden failures but cannot erase existing ones.
      * Coarse-graining can remove capacity/overlap/codomain pressure but not structural
        substrate absences or provenance smuggling.
      * Evaluator/codomain transport can remove evaluator and codomain channels only.
      * Substrate revisions D1/D2/D3 remove their corresponding structural channel(s).
      * Provenance contamination is absorbing: once target values are smuggled, the
        PROVENANCE_SMUGGLE channel remains under ordinary operations.
    """
    if operation == Operation.REFINEMENT:
        # In this finite witness, refinement reveals codomain mismatch if not already exact.
        if obs.is_zero:
            return obs
        return add_channels(obs, frozenset({Obstruction.CODOMAIN_MISMATCH}))

    if operation == Operation.COARSE_GRAINING:
        # Coarse graining can relieve capacity/overlap/codomain stress but cannot remove
        # structural absences or provenance smuggling.
        return remove_channels(
            obs,
            frozenset({
                Obstruction.CAPACITY_OVERSPEND,
                Obstruction.OVERLAP_INCOHERENCE,
                Obstruction.CODOMAIN_MISMATCH,
            })
        )

    if operation == Operation.EVALUATOR_TRANSPORT:
        return remove_channels(obs, frozenset({Obstruction.EVALUATOR_MISSING}))

    if operation == Operation.CODOMAIN_DECLARATION:
        return remove_channels(obs, frozenset({Obstruction.CODOMAIN_MISMATCH}))

    if operation == Operation.SUBSTRATE_REVISION_D1_POLARITY:
        return remove_channels(obs, frozenset({Obstruction.POLARITY_MISSING}))

    if operation == Operation.SUBSTRATE_REVISION_D2_REVERSAL:
        return remove_channels(obs, frozenset({Obstruction.REVERSAL_MISSING}))

    if operation == Operation.SUBSTRATE_REVISION_D3_COMPLEX_NORM:
        return remove_channels(obs, frozenset({Obstruction.COMPLEX_ACTION_MISSING, Obstruction.NORM_MISSING}))

    if operation == Operation.PROVENANCE_CONTAMINATION:
        return add_channels(obs, frozenset({Obstruction.PROVENANCE_SMUGGLE}))

    raise ValueError(f"Unknown operation: {operation}")


def compose_transform(obs: ObstructionObject, *ops: Operation) -> ObstructionObject:
    out = obs
    for op in ops:
        out = transform(out, op)
    return out


def examples() -> Dict[str, ObstructionObject]:
    return {
        "exact": ObstructionObject.zero(),
        "capacity": ObstructionObject.of(Obstruction.CAPACITY_OVERSPEND),
        "contextual": ObstructionObject.of(Obstruction.OVERLAP_INCOHERENCE),
        "scheme": ObstructionObject.of(Obstruction.EVALUATOR_MISSING, Obstruction.CODOMAIN_MISMATCH),
        "cstar": ObstructionObject.of(
            Obstruction.REVERSAL_MISSING,
            Obstruction.COMPLEX_ACTION_MISSING,
            Obstruction.NORM_MISSING,
            Obstruction.CODOMAIN_MISMATCH,
        ),
        "smuggled": ObstructionObject.of(Obstruction.PROVENANCE_SMUGGLE, Obstruction.CODOMAIN_MISMATCH),
        "polarity": ObstructionObject.of(Obstruction.POLARITY_MISSING),
    }


def names(obs: ObstructionObject) -> Tuple[str, ...]:
    return obs.names()


def check_T_obstruction_dynamics_operations_defined_P() -> Dict:
    ex = examples()
    tests = {}
    for op in Operation:
        for name, obs in ex.items():
            result = transform(obs, op)
            tests[f"{op.value}_{name}_typed"] = isinstance(result, ObstructionObject)
    if all(tests.values()):
        return _ok(
            "check_T_obstruction_dynamics_operations_defined_P",
            status="P_structural",
            summary="Finite obstruction dynamics operations are defined on obstruction objects.",
            data={"operation_count": len(Operation), "example_count": len(ex), "all_typed": True},
        )
    return _fail("check_T_obstruction_dynamics_operations_defined_P", status="FAIL", summary="Some obstruction operation was not typed", data=tests)


def check_T_refinement_monotonicity_P() -> Dict:
    ex = examples()
    results = {name: transform(obs, Operation.REFINEMENT) for name, obs in ex.items()}
    tests = {
        name: obs.channels.issubset(results[name].channels)
        for name, obs in ex.items()
    }
    if all(tests.values()):
        return _ok(
            "check_T_refinement_monotonicity_P",
            status="P_dyn",
            summary="Refinement is obstruction-monotone: it can reveal channels but does not erase existing obstructions.",
            data={name: {"before": names(ex[name]), "after": names(results[name])} for name in ex},
            dependencies=["check_T_obstruction_dynamics_operations_defined_P"],
        )
    return _fail("check_T_refinement_monotonicity_P", status="FAIL", summary="Refinement erased an obstruction", data=tests)


def check_T_coarse_graining_relief_P() -> Dict:
    ex = examples()
    coarse_capacity = transform(ex["capacity"], Operation.COARSE_GRAINING)
    coarse_contextual = transform(ex["contextual"], Operation.COARSE_GRAINING)
    coarse_cstar = transform(ex["cstar"], Operation.COARSE_GRAINING)
    coarse_smuggled = transform(ex["smuggled"], Operation.COARSE_GRAINING)

    tests = {
        "capacity_can_be_relieved": coarse_capacity.is_zero,
        "overlap_can_be_relieved": coarse_contextual.is_zero,
        "structural_channels_remain": all(ch in coarse_cstar.channels for ch in (Obstruction.REVERSAL_MISSING, Obstruction.COMPLEX_ACTION_MISSING, Obstruction.NORM_MISSING)),
        "provenance_remains": Obstruction.PROVENANCE_SMUGGLE in coarse_smuggled.channels,
    }
    if all(tests.values()):
        return _ok(
            "check_T_coarse_graining_relief_P",
            status="P_dyn",
            summary="Coarse-graining can relieve logistical pressure but not structural absences or provenance smuggling.",
            data={
                "capacity_after": names(coarse_capacity),
                "contextual_after": names(coarse_contextual),
                "cstar_after": names(coarse_cstar),
                "smuggled_after": names(coarse_smuggled),
                "tests": tests,
            },
            dependencies=["check_T_obstruction_dynamics_operations_defined_P"],
        )
    return _fail("check_T_coarse_graining_relief_P", status="FAIL", summary="Coarse-graining dynamics failed", data=tests)


def check_T_declared_transport_resolution_P() -> Dict:
    scheme = examples()["scheme"]
    after_eval = transform(scheme, Operation.EVALUATOR_TRANSPORT)
    after_both = compose_transform(scheme, Operation.EVALUATOR_TRANSPORT, Operation.CODOMAIN_DECLARATION)

    tests = {
        "evaluator_transport_removes_evaluator_only": (
            Obstruction.EVALUATOR_MISSING not in after_eval.channels
            and Obstruction.CODOMAIN_MISMATCH in after_eval.channels
        ),
        "evaluator_plus_codomain_transport_resolves_scheme": after_both.is_zero,
    }
    if all(tests.values()):
        return _ok(
            "check_T_declared_transport_resolution_P",
            status="P_dyn",
            summary="Declared evaluator/codomain transport can move scheme-local data into the exact kernel when no other obstruction remains.",
            data={"before": names(scheme), "after_eval": names(after_eval), "after_both": names(after_both), "tests": tests},
            dependencies=["check_T_obstruction_dynamics_operations_defined_P"],
        )
    return _fail("check_T_declared_transport_resolution_P", status="FAIL", summary="Declared transport dynamics failed", data=tests)


def check_T_structural_obstruction_invariance_P() -> Dict:
    cstar = examples()["cstar"]
    ordinary_ops = (
        Operation.COARSE_GRAINING,
        Operation.EVALUATOR_TRANSPORT,
        Operation.CODOMAIN_DECLARATION,
    )
    after = compose_transform(cstar, *ordinary_ops)
    tests = {
        "complex_remains": Obstruction.COMPLEX_ACTION_MISSING in after.channels,
        "norm_remains": Obstruction.NORM_MISSING in after.channels,
        "reversal_remains": Obstruction.REVERSAL_MISSING in after.channels,
        "codomain_can_be_removed": Obstruction.CODOMAIN_MISMATCH not in after.channels,
    }
    if all(tests.values()):
        return _ok(
            "check_T_structural_obstruction_invariance_P",
            status="P_dyn",
            summary="Structural C*-obstructions remain invariant under ordinary logistical repairs.",
            data={"before": names(cstar), "after_ordinary_repairs": names(after), "tests": tests},
            dependencies=["check_T_coarse_graining_relief_P", "check_T_declared_transport_resolution_P"],
        )
    return _fail("check_T_structural_obstruction_invariance_P", status="FAIL", summary="Structural obstruction invariance failed", data=tests)


def check_T_substrate_revision_dissolution_routes_P() -> Dict:
    cstar = examples()["cstar"]
    after_D2 = transform(cstar, Operation.SUBSTRATE_REVISION_D2_REVERSAL)
    after_D3 = transform(cstar, Operation.SUBSTRATE_REVISION_D3_COMPLEX_NORM)
    after_D2D3 = compose_transform(cstar, Operation.SUBSTRATE_REVISION_D2_REVERSAL, Operation.SUBSTRATE_REVISION_D3_COMPLEX_NORM, Operation.CODOMAIN_DECLARATION)
    polarity = examples()["polarity"]
    after_D1 = transform(polarity, Operation.SUBSTRATE_REVISION_D1_POLARITY)

    tests = {
        "D1_removes_polarity": after_D1.is_zero,
        "D2_removes_reversal_only": Obstruction.REVERSAL_MISSING not in after_D2.channels and Obstruction.COMPLEX_ACTION_MISSING in after_D2.channels,
        "D3_removes_complex_norm": Obstruction.COMPLEX_ACTION_MISSING not in after_D3.channels and Obstruction.NORM_MISSING not in after_D3.channels,
        "D2D3_plus_codomain_resolves_cstar": after_D2D3.is_zero,
    }
    if all(tests.values()):
        return _ok(
            "check_T_substrate_revision_dissolution_routes_P",
            status="P_dyn",
            summary="D1/D2/D3 substrate-revision routes dissolve exactly their corresponding structural obstructions.",
            data={
                "cstar_before": names(cstar),
                "after_D2": names(after_D2),
                "after_D3": names(after_D3),
                "after_D2D3_codomain": names(after_D2D3),
                "after_D1_polarity": names(after_D1),
                "tests": tests,
            },
            dependencies=["check_T_structural_obstruction_invariance_P"],
        )
    return _fail("check_T_substrate_revision_dissolution_routes_P", status="FAIL", summary="Substrate revision routes failed", data=tests)


def check_T_provenance_absorbing_boundary_P() -> Dict:
    zero = examples()["exact"]
    contaminated = transform(zero, Operation.PROVENANCE_CONTAMINATION)
    repaired = compose_transform(
        contaminated,
        Operation.COARSE_GRAINING,
        Operation.EVALUATOR_TRANSPORT,
        Operation.CODOMAIN_DECLARATION,
        Operation.SUBSTRATE_REVISION_D1_POLARITY,
        Operation.SUBSTRATE_REVISION_D2_REVERSAL,
        Operation.SUBSTRATE_REVISION_D3_COMPLEX_NORM,
    )
    tests = {
        "contamination_adds_provenance": Obstruction.PROVENANCE_SMUGGLE in contaminated.channels,
        "ordinary_and_structural_repairs_do_not_remove_provenance": Obstruction.PROVENANCE_SMUGGLE in repaired.channels,
        "repaired_still_nonzero": not repaired.is_zero,
    }
    if all(tests.values()):
        return _ok(
            "check_T_provenance_absorbing_boundary_P",
            status="P_audit",
            summary="Provenance smuggling is absorbing under obstruction dynamics; it cannot be repaired by mathematical transport.",
            data={"contaminated": names(contaminated), "after_repairs": names(repaired), "tests": tests},
            dependencies=["check_T_obstruction_dynamics_operations_defined_P"],
        )
    return _fail("check_T_provenance_absorbing_boundary_P", status="FAIL", summary="Provenance absorbing boundary failed", data=tests)


def check_T_obstruction_dynamics_exact_kernel_motion_P() -> Dict:
    ex = examples()
    scheme_resolved = compose_transform(ex["scheme"], Operation.EVALUATOR_TRANSPORT, Operation.CODOMAIN_DECLARATION)
    cstar_ordinarily_repaired = compose_transform(ex["cstar"], Operation.COARSE_GRAINING, Operation.CODOMAIN_DECLARATION)
    cstar_substrate_revised = compose_transform(ex["cstar"], Operation.SUBSTRATE_REVISION_D2_REVERSAL, Operation.SUBSTRATE_REVISION_D3_COMPLEX_NORM, Operation.CODOMAIN_DECLARATION)

    tests = {
        "scheme_can_enter_kernel_with_declared_transport": scheme_resolved.is_zero,
        "cstar_cannot_enter_kernel_by_ordinary_repair": not cstar_ordinarily_repaired.is_zero,
        "cstar_can_enter_kernel_only_after_substrate_revision": cstar_substrate_revised.is_zero,
        "exact_stays_exact_under_coarse_graining": transform(ex["exact"], Operation.COARSE_GRAINING).is_zero,
    }
    if all(tests.values()):
        return _ok(
            "check_T_obstruction_dynamics_exact_kernel_motion_P",
            status="P_dyn",
            summary="Obstruction dynamics determines which local data can move into the exact kernel and under what operations.",
            data={
                "scheme_resolved": names(scheme_resolved),
                "cstar_ordinarily_repaired": names(cstar_ordinarily_repaired),
                "cstar_substrate_revised": names(cstar_substrate_revised),
                "tests": tests,
            },
            dependencies=[
                "check_T_declared_transport_resolution_P",
                "check_T_structural_obstruction_invariance_P",
                "check_T_substrate_revision_dissolution_routes_P",
            ],
        )
    return _fail("check_T_obstruction_dynamics_exact_kernel_motion_P", status="FAIL", summary="Exact-kernel motion dynamics failed", data=tests)


def check_T_no_physical_time_flow_overclaim_P() -> Dict:
    return _ok(
        "check_T_no_physical_time_flow_overclaim_P",
        status="P_audit",
        summary="Scope boundary preserved: obstruction dynamics is formal transformation calculus, not a physical-time flow equation.",
        data={
            "physical_time_flow_claimed": False,
            "spectral_sequence_claimed": False,
            "finite_transformation_calculus_claimed": True,
            "future_programs": [
                "graded obstruction dynamics",
                "actual continuation-flow law",
                "cohomological refinement if derived",
                "renormalization/coarse-graining applications",
            ],
        },
    )


def check_T_obstruction_dynamics_theorem_P() -> Dict:
    subchecks = [
        check_T_obstruction_dynamics_operations_defined_P(),
        check_T_refinement_monotonicity_P(),
        check_T_coarse_graining_relief_P(),
        check_T_declared_transport_resolution_P(),
        check_T_structural_obstruction_invariance_P(),
        check_T_substrate_revision_dissolution_routes_P(),
        check_T_provenance_absorbing_boundary_P(),
        check_T_obstruction_dynamics_exact_kernel_motion_P(),
        check_T_no_physical_time_flow_overclaim_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_obstruction_dynamics_theorem_P",
            status="P_dyn",
            summary="Finite obstruction dynamics is P: transformations of obstruction channels determine motion into/out of the exact kernel.",
            data={
                "main_claim": "obstruction classes transform functorially under finite APF repair/refinement/revision operations",
                "kernel_motion": "ordinary repairs resolve logistical obstructions; structural obstructions require substrate revision; provenance is absorbing",
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_obstruction_dynamics_theorem_P",
        status="FAIL",
        summary="Obstruction dynamics theorem assembly failed.",
        data={"subchecks": subchecks},
    )


CHECKS = {
    "check_T_obstruction_dynamics_operations_defined_P": check_T_obstruction_dynamics_operations_defined_P,
    "check_T_refinement_monotonicity_P": check_T_refinement_monotonicity_P,
    "check_T_coarse_graining_relief_P": check_T_coarse_graining_relief_P,
    "check_T_declared_transport_resolution_P": check_T_declared_transport_resolution_P,
    "check_T_structural_obstruction_invariance_P": check_T_structural_obstruction_invariance_P,
    "check_T_substrate_revision_dissolution_routes_P": check_T_substrate_revision_dissolution_routes_P,
    "check_T_provenance_absorbing_boundary_P": check_T_provenance_absorbing_boundary_P,
    "check_T_obstruction_dynamics_exact_kernel_motion_P": check_T_obstruction_dynamics_exact_kernel_motion_P,
    "check_T_no_physical_time_flow_overclaim_P": check_T_no_physical_time_flow_overclaim_P,
    "check_T_obstruction_dynamics_theorem_P": check_T_obstruction_dynamics_theorem_P,
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
            raise TypeError("Unsupported registry type for obstruction_dynamics.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
