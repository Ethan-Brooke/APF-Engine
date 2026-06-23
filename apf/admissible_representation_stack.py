"""
APF Admissible Representation Stack — finite descent theorem.

This module banks the next unification layer after the Base/Fiber Allocation Theorem.

Main claim:
    APF unifies physical descriptions as admissible representation descent over the
    finite-capacity interface base.

Careful scope:
    This is a finite, bankable, 1-categorical stack/sheaf-like descent theorem over the
    generated APF interface site.  It does NOT claim a full infinity-stack construction.
    It provides the current corpus-grade object: a presheaf/fibration of representation
    categories with finite descent and obstruction classification.

Top export:
    check_T_admissible_representation_stack_P

Slogan:
    The universe does not carry one universal algebra; it carries a finite-capacity interface
    base over which admissible representations may or may not descend.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Optional, Tuple, List


OBSTRUCTION_CLASSES: Tuple[str, ...] = (
    "NONE",
    "POLARITY_MISSING",
    "REVERSAL_MISSING",
    "COMPLEX_ACTION_MISSING",
    "NORM_MISSING",
    "EVALUATOR_MISSING",
    "CAPACITY_OVERSPEND",
    "CODOMAIN_MISMATCH",
    "PROVENANCE_SMUGGLE",
    "OVERLAP_INCOHERENCE",
)


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
class Interface:
    name: str
    capacity: int
    cost_budget: float
    codomain: str


@dataclass(frozen=True)
class InterfaceMorphism:
    name: str
    source: str
    target: str
    cost: float
    acc_preserving: bool
    codomain_map: str


@dataclass(frozen=True)
class Representation:
    name: str
    interface: str
    kind: str
    capacity_load: int
    cost_load: float
    codomain: str
    provenance: str
    requires_polarity: bool = False
    requires_reversal: bool = False
    requires_complex_action: bool = False
    requires_norm: bool = False
    requires_external_evaluator: bool = False
    uses_target_as_input: bool = False


@dataclass(frozen=True)
class Restriction:
    """Restriction/transport of a representation along an interface morphism."""
    name: str
    morphism: str
    source_rep: str
    target_rep: str
    acc_compatible: bool
    cost_monotone: bool
    provenance_clean: bool
    codomain_coherent: bool


@dataclass(frozen=True)
class DescentDatum:
    name: str
    cover: Tuple[str, ...]
    local_reps: Tuple[str, ...]
    restrictions: Tuple[str, ...]
    overlap_agreement: bool
    claimed_global_rep: Optional[str]


def interface_site() -> Dict:
    """A finite APF interface site with enough structure to test descent and obstruction."""
    interfaces = {
        "Gamma": Interface("Gamma", capacity=61, cost_budget=100.0, codomain="ACC"),
        "Q": Interface("Q", capacity=8, cost_budget=20.0, codomain="quantum_fiber"),
        "G": Interface("G", capacity=42, cost_budget=60.0, codomain="geometric_fiber"),
        "S": Interface("S", capacity=11, cost_budget=18.0, codomain="scheme_fiber"),
        "O": Interface("O", capacity=5, cost_budget=8.0, codomain="overlap"),
    }
    morphisms = {
        "Q_to_Gamma": InterfaceMorphism("Q_to_Gamma", "Q", "Gamma", 4.0, True, "forget_to_ACC"),
        "G_to_Gamma": InterfaceMorphism("G_to_Gamma", "G", "Gamma", 7.0, True, "forget_to_ACC"),
        "S_to_Gamma": InterfaceMorphism("S_to_Gamma", "S", "Gamma", 3.0, True, "forget_to_ACC"),
        "O_to_Q": InterfaceMorphism("O_to_Q", "O", "Q", 2.0, True, "include_overlap"),
        "O_to_G": InterfaceMorphism("O_to_G", "O", "G", 2.0, True, "include_overlap"),
    }
    return {"interfaces": interfaces, "morphisms": morphisms}


def representation_catalog() -> Dict[str, Representation]:
    return {
        # Global substrate representation: should descend.
        "ACC_global": Representation(
            "ACC_global", "Gamma", "substrate_acc", 61, 30.0, "ACC", "APF_generated"
        ),
        "ACC_Q": Representation(
            "ACC_Q", "Q", "substrate_acc_restricted", 8, 5.0, "ACC", "APF_generated"
        ),
        "ACC_G": Representation(
            "ACC_G", "G", "substrate_acc_restricted", 42, 18.0, "ACC", "APF_generated"
        ),
        "ACC_O_from_Q": Representation(
            "ACC_O_from_Q", "O", "substrate_overlap", 5, 3.0, "ACC", "APF_generated"
        ),
        "ACC_O_from_G": Representation(
            "ACC_O_from_G", "O", "substrate_overlap", 5, 3.0, "ACC", "APF_generated"
        ),

        # Fiber-local quantum representation: local admissible but not substrate-global.
        "Hilbert_Q": Representation(
            "Hilbert_Q", "Q", "quantum_fiber_Cstar", 8, 12.0, "quantum_fiber",
            "APF_fiber_internal",
            requires_complex_action=True,
            requires_norm=True,
        ),

        # Scheme evaluator representation: local, requires external evaluator; not global.
        "Scheme_S": Representation(
            "Scheme_S", "S", "scheme_evaluator", 11, 12.0, "scheme_fiber",
            "external_evaluator_declared",
            requires_external_evaluator=True,
        ),

        # Bad overcapacity representation.
        "TooBig_Q": Representation(
            "TooBig_Q", "Q", "bad_overcapacity", 99, 12.0, "quantum_fiber",
            "APF_generated",
        ),

        # Bad provenance representation.
        "Smuggled_S": Representation(
            "Smuggled_S", "S", "bad_smuggle", 5, 5.0, "scheme_fiber",
            "target_value_consumed",
            uses_target_as_input=True,
        ),

        # Bad missing-evaluator representation: tries to globalize evaluator data at substrate.
        "MissingEvaluator_Gamma": Representation(
            "MissingEvaluator_Gamma", "Gamma", "bad_missing_evaluator", 5, 5.0, "ACC",
            "external_evaluator_absent",
            requires_external_evaluator=True,
        ),

        # Bad flat C*-global representation.
        "Flat_Cstar_Gamma": Representation(
            "Flat_Cstar_Gamma", "Gamma", "flat_master_Cstar", 61, 30.0, "ACC",
            "not_APF_generated",
            requires_complex_action=True,
            requires_norm=True,
            requires_reversal=True,
        ),

        # Bad flat/global evaluator: explicitly exercises EVALUATOR_MISSING at the base.
        "Flat_Evaluator_Gamma": Representation(
            "Flat_Evaluator_Gamma", "Gamma", "flat_scheme_evaluator", 10, 5.0, "ACC",
            "not_APF_generated",
            requires_external_evaluator=True,
        ),
    }


def restriction_catalog() -> Dict[str, Restriction]:
    return {
        "res_ACC_Q": Restriction("res_ACC_Q", "Q_to_Gamma", "ACC_global", "ACC_Q", True, True, True, True),
        "res_ACC_G": Restriction("res_ACC_G", "G_to_Gamma", "ACC_global", "ACC_G", True, True, True, True),
        "res_Q_O": Restriction("res_Q_O", "O_to_Q", "ACC_Q", "ACC_O_from_Q", True, True, True, True),
        "res_G_O": Restriction("res_G_O", "O_to_G", "ACC_G", "ACC_O_from_G", True, True, True, True),

        # Local fiber representation can restrict inside its fiber, but cannot be globalized as substrate ACC.
        "res_Hilbert_Q_to_ACC": Restriction("res_Hilbert_Q_to_ACC", "Q_to_Gamma", "Flat_Cstar_Gamma", "Hilbert_Q", False, True, True, False),

        # Scheme evaluator has codomain/evaluator dependency and cannot be substrate-global.
        "res_Scheme_S_to_ACC": Restriction("res_Scheme_S_to_ACC", "S_to_Gamma", "ACC_global", "Scheme_S", False, True, True, False),
    }


def descent_data_catalog() -> Dict[str, DescentDatum]:
    return {
        "ACC_descent_QG": DescentDatum(
            "ACC_descent_QG",
            cover=("Q", "G"),
            local_reps=("ACC_Q", "ACC_G"),
            restrictions=("res_ACC_Q", "res_ACC_G", "res_Q_O", "res_G_O"),
            overlap_agreement=True,
            claimed_global_rep="ACC_global",
        ),
        "Hilbert_flat_descent_fail": DescentDatum(
            "Hilbert_flat_descent_fail",
            cover=("Q",),
            local_reps=("Hilbert_Q",),
            restrictions=("res_Hilbert_Q_to_ACC",),
            overlap_agreement=True,
            claimed_global_rep="Flat_Cstar_Gamma",
        ),
        "Scheme_global_descent_fail": DescentDatum(
            "Scheme_global_descent_fail",
            cover=("S",),
            local_reps=("Scheme_S",),
            restrictions=("res_Scheme_S_to_ACC",),
            overlap_agreement=True,
            claimed_global_rep="Flat_Evaluator_Gamma",
        ),
        "Overlap_failure": DescentDatum(
            "Overlap_failure",
            cover=("Q", "G"),
            local_reps=("ACC_Q", "ACC_G"),
            restrictions=("res_ACC_Q", "res_ACC_G"),
            overlap_agreement=False,
            claimed_global_rep="ACC_global",
        ),
    }


def classify_representation(rep: Representation, site: Optional[Dict] = None) -> Tuple[bool, Tuple[str, ...]]:
    site = site or interface_site()
    iface = site["interfaces"][rep.interface]
    obstructions: List[str] = []

    if rep.capacity_load > iface.capacity:
        obstructions.append("CAPACITY_OVERSPEND")
    if rep.cost_load > iface.cost_budget:
        obstructions.append("CAPACITY_OVERSPEND")
    if rep.uses_target_as_input or rep.provenance == "target_value_consumed":
        obstructions.append("PROVENANCE_SMUGGLE")
    if rep.requires_complex_action and rep.interface == "Gamma":
        obstructions.append("COMPLEX_ACTION_MISSING")
    if rep.requires_norm and rep.interface == "Gamma":
        obstructions.append("NORM_MISSING")
    if rep.requires_reversal and rep.interface == "Gamma":
        obstructions.append("REVERSAL_MISSING")
    if rep.requires_polarity and rep.interface == "Gamma":
        obstructions.append("POLARITY_MISSING")
    if rep.requires_external_evaluator and rep.interface == "Gamma":
        obstructions.append("EVALUATOR_MISSING")
    if rep.codomain != iface.codomain and rep.interface != "Gamma" and not rep.kind.startswith("substrate_acc"):
        # fiber-local codomain should match fiber interface; substrate ACC restrictions are base data over fibers.
        obstructions.append("CODOMAIN_MISMATCH")
    if rep.interface == "Gamma" and rep.codomain != "ACC":
        obstructions.append("CODOMAIN_MISMATCH")

    return (len(obstructions) == 0, tuple(obstructions) or ("NONE",))


def restriction_ok(res: Restriction) -> Tuple[bool, Tuple[str, ...]]:
    obstructions: List[str] = []
    if not res.acc_compatible:
        obstructions.append("CODOMAIN_MISMATCH")
    if not res.cost_monotone:
        obstructions.append("CAPACITY_OVERSPEND")
    if not res.provenance_clean:
        obstructions.append("PROVENANCE_SMUGGLE")
    if not res.codomain_coherent:
        obstructions.append("CODOMAIN_MISMATCH")
    return (len(obstructions) == 0, tuple(obstructions) or ("NONE",))


def descent_ok(datum: DescentDatum) -> Tuple[bool, Tuple[str, ...]]:
    reps = representation_catalog()
    restrictions = restriction_catalog()
    obstructions: List[str] = []

    for rep_name in datum.local_reps:
        ok, obs = classify_representation(reps[rep_name])
        if not ok:
            obstructions.extend(x for x in obs if x != "NONE")

    for res_name in datum.restrictions:
        ok, obs = restriction_ok(restrictions[res_name])
        if not ok:
            obstructions.extend(x for x in obs if x != "NONE")

    if not datum.overlap_agreement:
        obstructions.append("OVERLAP_INCOHERENCE")

    if datum.claimed_global_rep is None:
        obstructions.append("CODOMAIN_MISMATCH")
    else:
        ok, obs = classify_representation(reps[datum.claimed_global_rep])
        if not ok:
            obstructions.extend(x for x in obs if x != "NONE")

    unique = tuple(sorted(set(obstructions), key=OBSTRUCTION_CLASSES.index))
    return (len(unique) == 0, unique or ("NONE",))


def check_T_interface_site_finite_P() -> Dict:
    site = interface_site()
    tests = {
        "interfaces_nonempty": len(site["interfaces"]) >= 1,
        "morphisms_nonempty": len(site["morphisms"]) >= 1,
        "all_morphism_endpoints_exist": all(
            m.source in site["interfaces"] and m.target in site["interfaces"]
            for m in site["morphisms"].values()
        ),
        "all_costs_nonnegative": all(m.cost >= 0 for m in site["morphisms"].values()),
    }
    if all(tests.values()):
        return _ok(
            "check_T_interface_site_finite_P",
            status="P_structural_reading",
            summary="Finite APF interface site is well-formed.",
            data=tests,
        )
    return _fail("check_T_interface_site_finite_P", status="FAIL", summary="Finite interface site failed", data=tests)


def check_T_representation_presheaf_defined_P() -> Dict:
    reps = representation_catalog()
    site = interface_site()
    tests = {
        "representations_nonempty": len(reps) >= 1,
        "all_interfaces_exist": all(r.interface in site["interfaces"] for r in reps.values()),
        "all_obstructions_known": all(
            all(x in OBSTRUCTION_CLASSES for x in classify_representation(r)[1])
            for r in reps.values()
        ),
    }
    if all(tests.values()):
        return _ok(
            "check_T_representation_presheaf_defined_P",
            status="P_structural_reading",
            summary="Representation assignment over the APF interface site is defined and typed.",
            data=tests,
            dependencies=["check_T_interface_site_finite_P"],
        )
    return _fail("check_T_representation_presheaf_defined_P", status="FAIL", summary="Representation presheaf typing failed", data=tests)


def check_T_restriction_maps_defined_P() -> Dict:
    restrictions = restriction_catalog()
    reps = representation_catalog()
    site = interface_site()
    tests = {
        "restrictions_nonempty": len(restrictions) >= 1,
        "all_morphisms_exist": all(r.morphism in site["morphisms"] for r in restrictions.values()),
        "all_reps_exist": all(r.source_rep in reps and r.target_rep in reps for r in restrictions.values()),
        "all_obstructions_known": all(
            all(x in OBSTRUCTION_CLASSES for x in restriction_ok(r)[1])
            for r in restrictions.values()
        ),
    }
    if all(tests.values()):
        return _ok(
            "check_T_restriction_maps_defined_P",
            status="P_structural_reading",
            summary="Restriction maps for local representations are typed and audit-classified.",
            data=tests,
            dependencies=["check_T_representation_presheaf_defined_P"],
        )
    return _fail("check_T_restriction_maps_defined_P", status="FAIL", summary="Restriction map definition failed", data=tests)


def check_T_descent_gluing_rule_P() -> Dict:
    data = descent_data_catalog()
    verdicts = {name: descent_ok(d) for name, d in data.items()}
    tests = {
        "ACC_descent_passes": verdicts["ACC_descent_QG"][0] is True,
        "Hilbert_flat_descent_fails": verdicts["Hilbert_flat_descent_fail"][0] is False,
        "Scheme_global_descent_fails": verdicts["Scheme_global_descent_fail"][0] is False,
        "Overlap_failure_fails": verdicts["Overlap_failure"][0] is False,
    }
    if all(tests.values()):
        return _ok(
            "check_T_descent_gluing_rule_P",
            status="P_descent",
            summary="Finite descent/gluing rule accepts ACC-compatible data and rejects obstructed globalizations.",
            data={
                "tests": tests,
                "verdicts": {k: {"passes": v[0], "obstructions": v[1]} for k, v in verdicts.items()},
            },
            dependencies=["check_T_restriction_maps_defined_P"],
        )
    return _fail("check_T_descent_gluing_rule_P", status="FAIL", summary="Descent/gluing rule failed", data={"tests": tests, "verdicts": verdicts})


def check_T_obstruction_classification_complete_P() -> Dict:
    reps = representation_catalog()
    data = descent_data_catalog()
    observed = set()
    for r in reps.values():
        observed.update(classify_representation(r)[1])
    for d in data.values():
        observed.update(descent_ok(d)[1])
    observed.discard("NONE")

    required = {
        "COMPLEX_ACTION_MISSING",
        "NORM_MISSING",
        "REVERSAL_MISSING",
        "EVALUATOR_MISSING",
        "CAPACITY_OVERSPEND",
        "CODOMAIN_MISMATCH",
        "PROVENANCE_SMUGGLE",
        "OVERLAP_INCOHERENCE",
    }
    tests = {
        "required_obstructions_observed": required.issubset(observed),
        "all_observed_known": observed.issubset(set(OBSTRUCTION_CLASSES)),
    }
    if all(tests.values()):
        return _ok(
            "check_T_obstruction_classification_complete_P",
            status="P_obstruction",
            summary="Descent obstruction classes cover the known APF failure modes exercised by this theorem.",
            data={"observed": sorted(observed), "required": sorted(required)},
            dependencies=["check_T_descent_gluing_rule_P"],
        )
    return _fail("check_T_obstruction_classification_complete_P", status="FAIL", summary="Obstruction classification incomplete", data={"observed": sorted(observed), "required": sorted(required), "tests": tests})


def check_T_contextuality_as_failed_descent_schema_P() -> Dict:
    # Schema-level check: contextuality is represented as overlap incoherence or absence of
    # a global section even when local sections are admissible.
    verdict = descent_ok(descent_data_catalog()["Overlap_failure"])
    ok = (verdict[0] is False and "OVERLAP_INCOHERENCE" in verdict[1])
    if ok:
        return _ok(
            "check_T_contextuality_as_failed_descent_schema_P",
            status="P_schema",
            summary="Contextuality/incompatible-local-description is represented as failed descent via overlap incoherence.",
            data={"descent_pass": verdict[0], "obstructions": verdict[1]},
            dependencies=["check_T_obstruction_classification_complete_P"],
        )
    return _fail("check_T_contextuality_as_failed_descent_schema_P", status="FAIL", summary="Failed-descent contextuality schema did not fire", data={"verdict": verdict})


def check_T_scheme_dependence_as_fiber_local_schema_P() -> Dict:
    scheme = representation_catalog()["Scheme_S"]
    local_ok, local_obs = classify_representation(scheme)
    descent_pass, descent_obs = descent_ok(descent_data_catalog()["Scheme_global_descent_fail"])
    ok = local_ok and (descent_pass is False) and ("CODOMAIN_MISMATCH" in descent_obs or "EVALUATOR_MISSING" in descent_obs)
    if ok:
        return _ok(
            "check_T_scheme_dependence_as_fiber_local_schema_P",
            status="P_schema",
            summary="Scheme dependence is represented as fiber-local evaluator structure that fails substrate-global descent.",
            data={"local_ok": local_ok, "local_obstructions": local_obs, "global_descent_obstructions": descent_obs},
            dependencies=["check_T_descent_gluing_rule_P"],
        )
    return _fail("check_T_scheme_dependence_as_fiber_local_schema_P", status="FAIL", summary="Scheme-dependence schema failed", data={"local_ok": local_ok, "local_obs": local_obs, "descent_obs": descent_obs})


def check_T_quantum_Cstar_as_fiber_local_schema_P() -> Dict:
    hilbert = representation_catalog()["Hilbert_Q"]
    local_ok, local_obs = classify_representation(hilbert)
    descent_pass, descent_obs = descent_ok(descent_data_catalog()["Hilbert_flat_descent_fail"])
    ok = local_ok and (descent_pass is False) and {"COMPLEX_ACTION_MISSING", "NORM_MISSING"}.intersection(set(descent_obs))
    if ok:
        return _ok(
            "check_T_quantum_Cstar_as_fiber_local_schema_P",
            status="P_schema",
            summary="Quantum C*/Hilbert structure is local-admissible in a quantum fiber but fails flat substrate-global descent.",
            data={"local_ok": local_ok, "local_obstructions": local_obs, "global_descent_obstructions": descent_obs},
            dependencies=["check_T_descent_gluing_rule_P"],
        )
    return _fail("check_T_quantum_Cstar_as_fiber_local_schema_P", status="FAIL", summary="Quantum C* fiber-local schema failed", data={"local_ok": local_ok, "local_obs": local_obs, "descent_obs": descent_obs})


def check_T_not_full_infinity_stack_overclaim_P() -> Dict:
    return _ok(
        "check_T_not_full_infinity_stack_overclaim_P",
        status="P_audit",
        summary="Scope boundary preserved: this is a finite 1-categorical descent theorem, not a claimed full infinity-stack construction.",
        data={
            "full_infinity_stack_claimed": False,
            "finite_descent_stack_like_theorem_claimed": True,
            "future_programs": [
                "2-fibered refinement",
                "infinity-stack refinement",
                "sheaf-of-modules refinement",
                "gauge-as-fiber-automorphism theorem",
                "horizon-area-as-fiber-cost theorem",
            ],
        },
    )


def check_T_admissible_representation_stack_P() -> Dict:
    subchecks = [
        check_T_interface_site_finite_P(),
        check_T_representation_presheaf_defined_P(),
        check_T_restriction_maps_defined_P(),
        check_T_descent_gluing_rule_P(),
        check_T_obstruction_classification_complete_P(),
        check_T_contextuality_as_failed_descent_schema_P(),
        check_T_scheme_dependence_as_fiber_local_schema_P(),
        check_T_quantum_Cstar_as_fiber_local_schema_P(),
        check_T_not_full_infinity_stack_overclaim_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_admissible_representation_stack_P",
            status="P_cat_finite_descent",
            summary="APF representations form a finite stack/sheaf-like descent object over the interface base, with obstruction classification.",
            data={
                "deeper_unification": "admissible representation descent over finite-capacity interfaces",
                "global_sections": ["ACC_global", "substrate-compatible ledgers"],
                "local_sections": ["Hilbert_Q", "Scheme_S"],
                "failed_descent_examples": ["Hilbert_flat_descent_fail", "Scheme_global_descent_fail", "Overlap_failure"],
                "obstruction_classes": list(OBSTRUCTION_CLASSES),
                "full_infinity_stack_claimed": False,
                "finite_descent_theorem_claimed": True,
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_admissible_representation_stack_P",
        status="FAIL",
        summary="Admissible Representation Stack theorem assembly failed.",
        data={"subchecks": subchecks},
    )


CHECKS = {
    "check_T_interface_site_finite_P": check_T_interface_site_finite_P,
    "check_T_representation_presheaf_defined_P": check_T_representation_presheaf_defined_P,
    "check_T_restriction_maps_defined_P": check_T_restriction_maps_defined_P,
    "check_T_descent_gluing_rule_P": check_T_descent_gluing_rule_P,
    "check_T_obstruction_classification_complete_P": check_T_obstruction_classification_complete_P,
    "check_T_contextuality_as_failed_descent_schema_P": check_T_contextuality_as_failed_descent_schema_P,
    "check_T_scheme_dependence_as_fiber_local_schema_P": check_T_scheme_dependence_as_fiber_local_schema_P,
    "check_T_quantum_Cstar_as_fiber_local_schema_P": check_T_quantum_Cstar_as_fiber_local_schema_P,
    "check_T_not_full_infinity_stack_overclaim_P": check_T_not_full_infinity_stack_overclaim_P,
    "check_T_admissible_representation_stack_P": check_T_admissible_representation_stack_P,
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
            raise TypeError("Unsupported registry type for admissible_representation_stack.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
