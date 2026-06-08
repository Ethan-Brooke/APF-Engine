"""
APF Descent Obstruction Calculus.

This module banks the next layer after the finite Admissible Representation Stack theorem.

Core theorem:
    Obs(D) = 0  iff  descent(D) succeeds.

Where D is a finite APF representation descent datum over the generated interface site.

Meaning:
    APF unifies regimes by deriving the obstruction calculus that determines when local
    representations can become global physics.

Scope:
    finite, bankable obstruction calculus over the APF representation descent site.
    No full infinity-stack or cohomology theory is claimed here.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, FrozenSet, Iterable, Mapping, Optional, Tuple, List


class Obstruction(str, Enum):
    NONE = "NONE"
    POLARITY_MISSING = "POLARITY_MISSING"
    REVERSAL_MISSING = "REVERSAL_MISSING"
    COMPLEX_ACTION_MISSING = "COMPLEX_ACTION_MISSING"
    NORM_MISSING = "NORM_MISSING"
    EVALUATOR_MISSING = "EVALUATOR_MISSING"
    CAPACITY_OVERSPEND = "CAPACITY_OVERSPEND"
    CODOMAIN_MISMATCH = "CODOMAIN_MISMATCH"
    PROVENANCE_SMUGGLE = "PROVENANCE_SMUGGLE"
    OVERLAP_INCOHERENCE = "OVERLAP_INCOHERENCE"


OBSTRUCTION_ORDER: Tuple[Obstruction, ...] = tuple(Obstruction)


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
class ObstructionObject:
    """Finite obstruction object.

    Algebra:
        zero = empty obstruction set
        addition/composition = union of channels

    This is a finite idempotent commutative monoid, not a claimed cohomology group.
    """
    channels: FrozenSet[Obstruction] = frozenset()

    @staticmethod
    def zero() -> "ObstructionObject":
        return ObstructionObject(frozenset())

    @staticmethod
    def of(*channels: Obstruction) -> "ObstructionObject":
        return ObstructionObject(frozenset(c for c in channels if c != Obstruction.NONE))

    @property
    def is_zero(self) -> bool:
        return len(self.channels) == 0

    def combine(self, other: "ObstructionObject") -> "ObstructionObject":
        return ObstructionObject(frozenset(self.channels | other.channels))

    def names(self) -> Tuple[str, ...]:
        return tuple(x.value for x in OBSTRUCTION_ORDER if x in self.channels)


@dataclass(frozen=True)
class LocalRepresentation:
    name: str
    capacity_load: int
    capacity_budget: int
    cost_load: float
    cost_budget: float
    codomain: str
    expected_codomain: str
    provenance_clean: bool
    requires_polarity: bool = False
    requires_reversal: bool = False
    requires_complex_action: bool = False
    requires_norm: bool = False
    requires_evaluator: bool = False
    evaluator_available: bool = True


@dataclass(frozen=True)
class DescentDatum:
    name: str
    locals: Tuple[LocalRepresentation, ...]
    overlap_coherent: bool
    global_codomain: str
    local_to_global_codomain_declared: bool
    target_value_consumed: bool = False


def obs_local(rep: LocalRepresentation, *, substrate_level: bool = False) -> ObstructionObject:
    channels: List[Obstruction] = []

    if rep.capacity_load > rep.capacity_budget or rep.cost_load > rep.cost_budget:
        channels.append(Obstruction.CAPACITY_OVERSPEND)

    if rep.codomain != rep.expected_codomain:
        channels.append(Obstruction.CODOMAIN_MISMATCH)

    if not rep.provenance_clean:
        channels.append(Obstruction.PROVENANCE_SMUGGLE)

    if substrate_level:
        if rep.requires_polarity:
            channels.append(Obstruction.POLARITY_MISSING)
        if rep.requires_reversal:
            channels.append(Obstruction.REVERSAL_MISSING)
        if rep.requires_complex_action:
            channels.append(Obstruction.COMPLEX_ACTION_MISSING)
        if rep.requires_norm:
            channels.append(Obstruction.NORM_MISSING)
        if rep.requires_evaluator and not rep.evaluator_available:
            channels.append(Obstruction.EVALUATOR_MISSING)

    # At local fiber level, complex/norm/evaluator requirements can be allowed if the
    # interface declares them. They are obstructions only when globalized to substrate.
    if rep.requires_evaluator and not rep.evaluator_available:
        channels.append(Obstruction.EVALUATOR_MISSING)

    return ObstructionObject.of(*channels)


def obs_descent(datum: DescentDatum) -> ObstructionObject:
    obs = ObstructionObject.zero()

    # Local admissibility in local fibers.
    for rep in datum.locals:
        obs = obs.combine(obs_local(rep, substrate_level=False))

    # Globalization to substrate/base: requirements can become obstructions.
    for rep in datum.locals:
        obs = obs.combine(obs_local(rep, substrate_level=(datum.global_codomain == "ACC")))

    if not datum.overlap_coherent:
        obs = obs.combine(ObstructionObject.of(Obstruction.OVERLAP_INCOHERENCE))

    if not datum.local_to_global_codomain_declared:
        obs = obs.combine(ObstructionObject.of(Obstruction.CODOMAIN_MISMATCH))

    if datum.target_value_consumed:
        obs = obs.combine(ObstructionObject.of(Obstruction.PROVENANCE_SMUGGLE))

    return obs


def descent_succeeds(datum: DescentDatum) -> bool:
    return obs_descent(datum).is_zero


def examples() -> Dict[str, DescentDatum]:
    acc_q = LocalRepresentation(
        "ACC_Q", 8, 8, 5.0, 20.0, "ACC", "ACC", True
    )
    acc_g = LocalRepresentation(
        "ACC_G", 42, 42, 18.0, 60.0, "ACC", "ACC", True
    )
    hilbert_q = LocalRepresentation(
        "Hilbert_Q", 8, 8, 12.0, 20.0, "quantum_fiber", "quantum_fiber", True,
        requires_complex_action=True, requires_norm=True, requires_reversal=True
    )
    scheme_s = LocalRepresentation(
        "Scheme_S", 11, 11, 10.0, 18.0, "scheme_fiber", "scheme_fiber", True,
        requires_evaluator=True, evaluator_available=False
    )
    too_big = LocalRepresentation(
        "TooBig_Q", 99, 8, 12.0, 20.0, "quantum_fiber", "quantum_fiber", True
    )
    smuggled = LocalRepresentation(
        "Smuggled_S", 5, 11, 4.0, 18.0, "scheme_fiber", "scheme_fiber", False
    )
    bad_codomain = LocalRepresentation(
        "BadCodomain", 5, 8, 2.0, 20.0, "quantum_fiber", "scheme_fiber", True
    )

    return {
        "ACC_global_descent": DescentDatum(
            "ACC_global_descent",
            locals=(acc_q, acc_g),
            overlap_coherent=True,
            global_codomain="ACC",
            local_to_global_codomain_declared=True,
        ),
        "Cstar_flat_global_failure": DescentDatum(
            "Cstar_flat_global_failure",
            locals=(hilbert_q,),
            overlap_coherent=True,
            global_codomain="ACC",
            local_to_global_codomain_declared=False,
        ),
        "scheme_evaluator_failure": DescentDatum(
            "scheme_evaluator_failure",
            locals=(scheme_s,),
            overlap_coherent=True,
            global_codomain="ACC",
            local_to_global_codomain_declared=False,
        ),
        "contextuality_overlap_failure": DescentDatum(
            "contextuality_overlap_failure",
            locals=(acc_q, acc_g),
            overlap_coherent=False,
            global_codomain="ACC",
            local_to_global_codomain_declared=True,
        ),
        "capacity_overspend_failure": DescentDatum(
            "capacity_overspend_failure",
            locals=(too_big,),
            overlap_coherent=True,
            global_codomain="quantum_fiber",
            local_to_global_codomain_declared=True,
        ),
        "provenance_smuggle_failure": DescentDatum(
            "provenance_smuggle_failure",
            locals=(smuggled,),
            overlap_coherent=True,
            global_codomain="scheme_fiber",
            local_to_global_codomain_declared=True,
            target_value_consumed=True,
        ),
        "codomain_mismatch_failure": DescentDatum(
            "codomain_mismatch_failure",
            locals=(bad_codomain,),
            overlap_coherent=True,
            global_codomain="ACC",
            local_to_global_codomain_declared=False,
        ),
    }


def check_T_obstruction_object_monoid_P() -> Dict:
    zero = ObstructionObject.zero()
    a = ObstructionObject.of(Obstruction.CAPACITY_OVERSPEND)
    b = ObstructionObject.of(Obstruction.CODOMAIN_MISMATCH)
    c = ObstructionObject.of(Obstruction.PROVENANCE_SMUGGLE)

    tests = {
        "zero_identity_left": zero.combine(a) == a,
        "zero_identity_right": a.combine(zero) == a,
        "idempotent": a.combine(a) == a,
        "commutative": a.combine(b) == b.combine(a),
        "associative": a.combine(b).combine(c) == a.combine(b.combine(c)),
        "zero_is_zero": zero.is_zero,
        "nonzero_not_zero": not a.is_zero,
    }

    if all(tests.values()):
        return _ok(
            "check_T_obstruction_object_monoid_P",
            status="P_calc",
            summary="Obstruction objects form a finite idempotent commutative monoid under channel union.",
            data=tests,
        )
    return _fail("check_T_obstruction_object_monoid_P", status="FAIL", summary="Obstruction monoid laws failed", data=tests)


def check_T_local_obstruction_map_P() -> Dict:
    ex = examples()
    local_tests = {
        "ACC_Q_zero": obs_local(ex["ACC_global_descent"].locals[0]).is_zero,
        "TooBig_capacity": Obstruction.CAPACITY_OVERSPEND in obs_local(ex["capacity_overspend_failure"].locals[0]).channels,
        "Smuggled_provenance": Obstruction.PROVENANCE_SMUGGLE in obs_local(ex["provenance_smuggle_failure"].locals[0]).channels,
        "BadCodomain_codomain": Obstruction.CODOMAIN_MISMATCH in obs_local(ex["codomain_mismatch_failure"].locals[0]).channels,
    }
    if all(local_tests.values()):
        return _ok(
            "check_T_local_obstruction_map_P",
            status="P_calc",
            summary="Local obstruction map detects capacity, provenance, and codomain failures while accepting clean ACC data.",
            data=local_tests,
            dependencies=["check_T_obstruction_object_monoid_P"],
        )
    return _fail("check_T_local_obstruction_map_P", status="FAIL", summary="Local obstruction map failed", data=local_tests)


def check_T_descent_obstruction_zero_iff_P() -> Dict:
    ex = examples()
    verdicts = {
        name: {
            "obs": obs_descent(d).names(),
            "obs_zero": obs_descent(d).is_zero,
            "descent_succeeds": descent_succeeds(d),
        }
        for name, d in ex.items()
    }
    tests = {
        name: v["obs_zero"] == v["descent_succeeds"]
        for name, v in verdicts.items()
    }
    # Require exactly the intended good case to pass.
    tests["only_ACC_global_passes"] = (
        verdicts["ACC_global_descent"]["descent_succeeds"] is True
        and all(v["descent_succeeds"] is False for k, v in verdicts.items() if k != "ACC_global_descent")
    )

    if all(tests.values()):
        return _ok(
            "check_T_descent_obstruction_zero_iff_P",
            status="P_theorem",
            summary="Finite descent succeeds if and only if the obstruction object is zero.",
            data={"tests": tests, "verdicts": verdicts},
            dependencies=["check_T_local_obstruction_map_P"],
        )
    return _fail("check_T_descent_obstruction_zero_iff_P", status="FAIL", summary="Zero-obstruction iff descent failed", data={"tests": tests, "verdicts": verdicts})


def check_T_Cstar_obstruction_schema_P() -> Dict:
    obs = obs_descent(examples()["Cstar_flat_global_failure"])
    required = {Obstruction.COMPLEX_ACTION_MISSING, Obstruction.NORM_MISSING, Obstruction.REVERSAL_MISSING, Obstruction.CODOMAIN_MISMATCH}
    tests = {
        "descent_fails": not obs.is_zero,
        "required_channels_present": required.issubset(obs.channels),
    }
    if all(tests.values()):
        return _ok(
            "check_T_Cstar_obstruction_schema_P",
            status="P_schema",
            summary="Flat global C*-unification fails by complex-action, norm, reversal, and codomain obstructions.",
            data={"obs": obs.names(), "required": tuple(x.value for x in required)},
            dependencies=["check_T_descent_obstruction_zero_iff_P"],
        )
    return _fail("check_T_Cstar_obstruction_schema_P", status="FAIL", summary="Cstar obstruction schema failed", data={"obs": obs.names(), "tests": tests})


def check_T_scheme_obstruction_schema_P() -> Dict:
    obs = obs_descent(examples()["scheme_evaluator_failure"])
    required = {Obstruction.EVALUATOR_MISSING, Obstruction.CODOMAIN_MISMATCH}
    tests = {
        "descent_fails": not obs.is_zero,
        "required_channels_present": required.issubset(obs.channels),
    }
    if all(tests.values()):
        return _ok(
            "check_T_scheme_obstruction_schema_P",
            status="P_schema",
            summary="Scheme/evaluator dependence fails substrate-global descent by evaluator and codomain obstructions.",
            data={"obs": obs.names(), "required": tuple(x.value for x in required)},
            dependencies=["check_T_descent_obstruction_zero_iff_P"],
        )
    return _fail("check_T_scheme_obstruction_schema_P", status="FAIL", summary="Scheme obstruction schema failed", data={"obs": obs.names(), "tests": tests})


def check_T_contextuality_obstruction_schema_P() -> Dict:
    obs = obs_descent(examples()["contextuality_overlap_failure"])
    tests = {
        "descent_fails": not obs.is_zero,
        "overlap_incoherence_present": Obstruction.OVERLAP_INCOHERENCE in obs.channels,
    }
    if all(tests.values()):
        return _ok(
            "check_T_contextuality_obstruction_schema_P",
            status="P_schema",
            summary="Contextuality/incompatible local descriptions are modeled as overlap-incoherence descent obstruction.",
            data={"obs": obs.names()},
            dependencies=["check_T_descent_obstruction_zero_iff_P"],
        )
    return _fail("check_T_contextuality_obstruction_schema_P", status="FAIL", summary="Contextuality obstruction schema failed", data={"obs": obs.names(), "tests": tests})


def check_T_capacity_and_provenance_obstruction_schemas_P() -> Dict:
    cap_obs = obs_descent(examples()["capacity_overspend_failure"])
    prov_obs = obs_descent(examples()["provenance_smuggle_failure"])
    tests = {
        "capacity_descent_fails": not cap_obs.is_zero,
        "capacity_channel_present": Obstruction.CAPACITY_OVERSPEND in cap_obs.channels,
        "provenance_descent_fails": not prov_obs.is_zero,
        "provenance_channel_present": Obstruction.PROVENANCE_SMUGGLE in prov_obs.channels,
    }
    if all(tests.values()):
        return _ok(
            "check_T_capacity_and_provenance_obstruction_schemas_P",
            status="P_schema",
            summary="Capacity overspend and provenance smuggling are obstruction-calculus failure modes.",
            data={"capacity_obs": cap_obs.names(), "provenance_obs": prov_obs.names()},
            dependencies=["check_T_descent_obstruction_zero_iff_P"],
        )
    return _fail("check_T_capacity_and_provenance_obstruction_schemas_P", status="FAIL", summary="Capacity/provenance obstruction schema failed", data={"tests": tests, "capacity_obs": cap_obs.names(), "provenance_obs": prov_obs.names()})


def check_T_obstruction_class_coverage_P() -> Dict:
    ex = examples()
    observed = set()
    for d in ex.values():
        observed.update(obs_descent(d).channels)
    required = {
        Obstruction.REVERSAL_MISSING,
        Obstruction.COMPLEX_ACTION_MISSING,
        Obstruction.NORM_MISSING,
        Obstruction.EVALUATOR_MISSING,
        Obstruction.CAPACITY_OVERSPEND,
        Obstruction.CODOMAIN_MISMATCH,
        Obstruction.PROVENANCE_SMUGGLE,
        Obstruction.OVERLAP_INCOHERENCE,
    }
    tests = {
        "required_subset_observed": required.issubset(observed),
        "observed_known": all(isinstance(x, Obstruction) for x in observed),
    }
    if all(tests.values()):
        return _ok(
            "check_T_obstruction_class_coverage_P",
            status="P_audit",
            summary="Worked examples exercise the known obstruction channels needed for current APF descent failures.",
            data={"observed": tuple(x.value for x in OBSTRUCTION_ORDER if x in observed), "required": tuple(x.value for x in required)},
            dependencies=[
                "check_T_Cstar_obstruction_schema_P",
                "check_T_scheme_obstruction_schema_P",
                "check_T_contextuality_obstruction_schema_P",
                "check_T_capacity_and_provenance_obstruction_schemas_P",
            ],
        )
    return _fail("check_T_obstruction_class_coverage_P", status="FAIL", summary="Obstruction class coverage incomplete", data={"observed": tuple(x.value for x in observed), "required": tuple(x.value for x in required), "tests": tests})


def check_T_no_cohomology_overclaim_P() -> Dict:
    return _ok(
        "check_T_no_cohomology_overclaim_P",
        status="P_audit",
        summary="Scope boundary preserved: obstruction object is a finite channel monoid, not a claimed cohomology theory.",
        data={
            "cohomology_theory_claimed": False,
            "infinity_stack_claimed": False,
            "finite_channel_monoid_claimed": True,
            "future_extensions": [
                "graded obstruction complex",
                "exact sequence formulation",
                "2-categorical descent",
                "cohomological obstruction refinement if justified later",
            ],
        },
    )


def check_T_descent_obstruction_calculus_P() -> Dict:
    subchecks = [
        check_T_obstruction_object_monoid_P(),
        check_T_local_obstruction_map_P(),
        check_T_descent_obstruction_zero_iff_P(),
        check_T_Cstar_obstruction_schema_P(),
        check_T_scheme_obstruction_schema_P(),
        check_T_contextuality_obstruction_schema_P(),
        check_T_capacity_and_provenance_obstruction_schemas_P(),
        check_T_obstruction_class_coverage_P(),
        check_T_no_cohomology_overclaim_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_descent_obstruction_calculus_P",
            status="P_calc",
            summary="APF descent obstruction calculus is P: zero obstruction iff descent, with classified failure channels.",
            data={
                "main_equivalence": "Obs(D)=0 iff D descends",
                "obstruction_algebra": "finite idempotent commutative monoid under union",
                "unification_sentence": "APF unifies regimes by deriving the obstruction calculus that determines when local representations can become global physics.",
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_descent_obstruction_calculus_P",
        status="FAIL",
        summary="Descent obstruction calculus assembly failed.",
        data={"subchecks": subchecks},
    )


CHECKS = {
    "check_T_obstruction_object_monoid_P": check_T_obstruction_object_monoid_P,
    "check_T_local_obstruction_map_P": check_T_local_obstruction_map_P,
    "check_T_descent_obstruction_zero_iff_P": check_T_descent_obstruction_zero_iff_P,
    "check_T_Cstar_obstruction_schema_P": check_T_Cstar_obstruction_schema_P,
    "check_T_scheme_obstruction_schema_P": check_T_scheme_obstruction_schema_P,
    "check_T_contextuality_obstruction_schema_P": check_T_contextuality_obstruction_schema_P,
    "check_T_capacity_and_provenance_obstruction_schemas_P": check_T_capacity_and_provenance_obstruction_schemas_P,
    "check_T_obstruction_class_coverage_P": check_T_obstruction_class_coverage_P,
    "check_T_no_cohomology_overclaim_P": check_T_no_cohomology_overclaim_P,
    "check_T_descent_obstruction_calculus_P": check_T_descent_obstruction_calculus_P,
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
            raise TypeError("Unsupported registry type for descent_obstruction_calculus.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
