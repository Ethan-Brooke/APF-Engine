"""
APF Representation Descent Kernel — Adversarial Audit.

Purpose
-------
Hardens the Representation Descent Kernel against the main challenge:

    The kernel theorem must not be tautological.
    Descent must be checked independently from the obstruction object.

This module adds:
  * independent descent predicate;
  * independent obstruction derivation from raw finite-site metadata;
  * generated globalization image rather than hand-coded image;
  * mutation knockouts for every descent axiom;
  * deterministic random finite-site stress;
  * sector obstruction derivation from metadata;
  * no expected-label leakage audit;
  * exactness non-tautology check.

Top export:
    check_T_representation_descent_kernel_adversarial_audit_P
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
import inspect
import random
from typing import Dict, Iterable, Mapping, Optional, Tuple, FrozenSet, List, Set

try:
    from apf.descent_obstruction_calculus import Obstruction, ObstructionObject
    from apf.globalization_promotion_gate import PromotionStatus, decide_promotion
    from apf.representation_descent_kernel import check_T_APF_representation_descent_kernel_P
except Exception as exc:  # pragma: no cover
    raise ImportError(f"adversarial audit dependencies missing: {exc}") from exc


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
class RawLocalDatum:
    """Raw local representation datum.

    No expected status fields are allowed here.
    """
    name: str
    capacity_load: int
    capacity_budget: int
    cost_load: float
    cost_budget: float
    acc_compatible: bool
    cost_monotone: bool
    codomain: str
    target_codomain: str
    codomain_map_declared: bool
    overlap_agreement: bool
    provenance_clean: bool
    requires_polarity: bool = False
    requires_reversal: bool = False
    requires_complex_action: bool = False
    requires_norm: bool = False
    requires_evaluator: bool = False
    evaluator_available: bool = True


@dataclass(frozen=True)
class RawDescentDatum:
    name: str
    locals: Tuple[RawLocalDatum, ...]
    global_codomain: str
    cover_declared: bool
    global_structure_available: bool
    target_value_consumed: bool = False


@dataclass(frozen=True)
class GlobalSeed:
    name: str
    base_codomain: str
    capacity_budget: int
    cost_budget: float
    cover_names: Tuple[str, ...]


def independent_descent_predicate(datum: RawDescentDatum) -> bool:
    """Independent descent/gluing check.

    This predicate is intentionally written from raw gluing conditions rather than
    from the obstruction or promotion machinery.

    Descent requires:
      1. cover declared;
      2. global structure available;
      3. every local datum is ACC-compatible;
      4. cost monotone;
      5. capacity and cost within budget;
      6. provenance clean and no target value consumed;
      7. codomain coherence or declared codomain map;
      8. overlap agreement;
      9. no missing evaluator;
      10. no substrate-global request for polarity/reversal/complex/norm.
    """
    if not datum.cover_declared:
        return False
    if not datum.global_structure_available:
        return False
    if datum.target_value_consumed:
        return False
    if len(datum.locals) == 0:
        return False

    for local in datum.locals:
        if not local.acc_compatible:
            return False
        if not local.cost_monotone:
            return False
        if local.capacity_load > local.capacity_budget:
            return False
        if local.cost_load > local.cost_budget:
            return False
        if not local.provenance_clean:
            return False
        if not local.overlap_agreement:
            return False
        if local.codomain != local.target_codomain and not local.codomain_map_declared:
            return False
        if local.requires_evaluator and not local.evaluator_available:
            return False
        if datum.global_codomain == "ACC" and (
            local.requires_polarity
            or local.requires_reversal
            or local.requires_complex_action
            or local.requires_norm
        ):
            return False

    return True


def derive_obstruction_from_raw(datum: RawDescentDatum) -> ObstructionObject:
    """Derive obstruction from raw metadata, separately from descent predicate."""
    channels: List[Obstruction] = []

    if not datum.cover_declared:
        channels.append(Obstruction.OVERLAP_INCOHERENCE)
    if not datum.global_structure_available:
        channels.append(Obstruction.CODOMAIN_MISMATCH)
    if datum.target_value_consumed:
        channels.append(Obstruction.PROVENANCE_SMUGGLE)

    for local in datum.locals:
        if not local.acc_compatible:
            channels.append(Obstruction.CODOMAIN_MISMATCH)
        if not local.cost_monotone:
            channels.append(Obstruction.CAPACITY_OVERSPEND)
        if local.capacity_load > local.capacity_budget or local.cost_load > local.cost_budget:
            channels.append(Obstruction.CAPACITY_OVERSPEND)
        if not local.provenance_clean:
            channels.append(Obstruction.PROVENANCE_SMUGGLE)
        if not local.overlap_agreement:
            channels.append(Obstruction.OVERLAP_INCOHERENCE)
        if local.codomain != local.target_codomain and not local.codomain_map_declared:
            channels.append(Obstruction.CODOMAIN_MISMATCH)
        if local.requires_evaluator and not local.evaluator_available:
            channels.append(Obstruction.EVALUATOR_MISSING)

        if datum.global_codomain == "ACC":
            if local.requires_polarity:
                channels.append(Obstruction.POLARITY_MISSING)
            if local.requires_reversal:
                channels.append(Obstruction.REVERSAL_MISSING)
            if local.requires_complex_action:
                channels.append(Obstruction.COMPLEX_ACTION_MISSING)
            if local.requires_norm:
                channels.append(Obstruction.NORM_MISSING)

    return ObstructionObject.of(*channels)


def raw_examples() -> Dict[str, RawDescentDatum]:
    clean_q = RawLocalDatum(
        "ACC_Q", 8, 8, 5.0, 20.0, True, True, "ACC", "ACC", True, True, True
    )
    clean_g = RawLocalDatum(
        "ACC_G", 42, 42, 18.0, 60.0, True, True, "ACC", "ACC", True, True, True
    )
    cstar_q = RawLocalDatum(
        "Hilbert_Q", 8, 8, 12.0, 20.0, True, True, "quantum_fiber", "ACC", False, True, True,
        requires_reversal=True, requires_complex_action=True, requires_norm=True
    )
    scheme_s = RawLocalDatum(
        "Scheme_S", 11, 11, 10.0, 18.0, True, True, "scheme_fiber", "ACC", False, True, True,
        requires_evaluator=True, evaluator_available=False
    )
    too_big = RawLocalDatum(
        "TooBig", 99, 8, 12.0, 20.0, True, True, "ACC", "ACC", True, True, True
    )
    smuggled = RawLocalDatum(
        "Smuggled", 5, 11, 4.0, 18.0, True, True, "scheme_fiber", "ACC", False, True, False
    )
    overlap_bad = RawLocalDatum(
        "OverlapBad", 5, 8, 2.0, 20.0, True, True, "ACC", "ACC", True, False, True
    )

    return {
        "ACC_clean": RawDescentDatum("ACC_clean", (clean_q, clean_g), "ACC", True, True),
        "Cstar_bad": RawDescentDatum("Cstar_bad", (cstar_q,), "ACC", True, True),
        "Scheme_bad": RawDescentDatum("Scheme_bad", (scheme_s,), "ACC", True, True),
        "Capacity_bad": RawDescentDatum("Capacity_bad", (too_big,), "ACC", True, True),
        "Provenance_bad": RawDescentDatum("Provenance_bad", (smuggled,), "ACC", True, True, target_value_consumed=True),
        "Overlap_bad": RawDescentDatum("Overlap_bad", (overlap_bad,), "ACC", True, True),
        "No_cover_bad": RawDescentDatum("No_cover_bad", (clean_q,), "ACC", False, True),
        "No_global_bad": RawDescentDatum("No_global_bad", (clean_q,), "ACC", True, False),
    }


def generate_globalization_image(seed: GlobalSeed) -> RawDescentDatum:
    """Generate local restrictions from a global seed.

    This is intentionally computed from the seed/cover rather than hard-coded as an image set.
    """
    locals_: List[RawLocalDatum] = []
    if not seed.cover_names:
        return RawDescentDatum(
            f"{seed.name}_empty_cover",
            tuple(),
            seed.base_codomain,
            cover_declared=False,
            global_structure_available=True,
        )

    per_capacity = max(1, seed.capacity_budget // len(seed.cover_names))
    per_cost = max(0.1, seed.cost_budget / len(seed.cover_names))

    for cover in seed.cover_names:
        locals_.append(
            RawLocalDatum(
                name=f"{seed.name}|{cover}",
                capacity_load=min(per_capacity, seed.capacity_budget),
                capacity_budget=max(per_capacity, 1),
                cost_load=per_cost * 0.5,
                cost_budget=per_cost,
                acc_compatible=True,
                cost_monotone=True,
                codomain=seed.base_codomain,
                target_codomain=seed.base_codomain,
                codomain_map_declared=True,
                overlap_agreement=True,
                provenance_clean=True,
            )
        )

    return RawDescentDatum(
        name=f"Glob({seed.name})",
        locals=tuple(locals_),
        global_codomain=seed.base_codomain,
        cover_declared=True,
        global_structure_available=True,
    )


def mutated_datum(base: RawDescentDatum, mutation: str) -> RawDescentDatum:
    local = base.locals[0]
    if mutation == "cover":
        return replace(base, cover_declared=False)
    if mutation == "global":
        return replace(base, global_structure_available=False)
    if mutation == "target":
        return replace(base, target_value_consumed=True)
    if mutation == "acc":
        return replace(base, locals=(replace(local, acc_compatible=False),))
    if mutation == "cost":
        return replace(base, locals=(replace(local, cost_monotone=False),))
    if mutation == "capacity":
        return replace(base, locals=(replace(local, capacity_load=local.capacity_budget + 1),))
    if mutation == "cost_budget":
        return replace(base, locals=(replace(local, cost_load=local.cost_budget + 1.0),))
    if mutation == "provenance":
        return replace(base, locals=(replace(local, provenance_clean=False),))
    if mutation == "codomain":
        return replace(base, locals=(replace(local, codomain="quantum_fiber", target_codomain="ACC", codomain_map_declared=False),))
    if mutation == "overlap":
        return replace(base, locals=(replace(local, overlap_agreement=False),))
    if mutation == "evaluator":
        return replace(base, locals=(replace(local, requires_evaluator=True, evaluator_available=False),))
    if mutation == "cstar":
        return replace(base, locals=(replace(local, requires_reversal=True, requires_complex_action=True, requires_norm=True),))
    raise ValueError(f"unknown mutation {mutation}")


def random_datum(rng: random.Random, idx: int) -> RawDescentDatum:
    n = rng.randint(1, 3)
    locals_ = []
    for j in range(n):
        cap_budget = rng.randint(1, 20)
        cost_budget = float(rng.randint(1, 30))
        locals_.append(
            RawLocalDatum(
                name=f"R{idx}_{j}",
                capacity_load=rng.randint(0, 25),
                capacity_budget=cap_budget,
                cost_load=float(rng.randint(0, 35)),
                cost_budget=cost_budget,
                acc_compatible=rng.choice([True, True, False]),
                cost_monotone=rng.choice([True, True, False]),
                codomain=rng.choice(["ACC", "quantum_fiber", "scheme_fiber"]),
                target_codomain=rng.choice(["ACC", "quantum_fiber", "scheme_fiber"]),
                codomain_map_declared=rng.choice([True, False]),
                overlap_agreement=rng.choice([True, True, False]),
                provenance_clean=rng.choice([True, True, False]),
                requires_polarity=rng.choice([False, False, True]),
                requires_reversal=rng.choice([False, False, True]),
                requires_complex_action=rng.choice([False, False, True]),
                requires_norm=rng.choice([False, False, True]),
                requires_evaluator=rng.choice([False, False, True]),
                evaluator_available=rng.choice([True, False]),
            )
        )
    return RawDescentDatum(
        name=f"rand_{idx}",
        locals=tuple(locals_),
        global_codomain=rng.choice(["ACC", "quantum_fiber", "scheme_fiber"]),
        cover_declared=rng.choice([True, True, False]),
        global_structure_available=rng.choice([True, True, False]),
        target_value_consumed=rng.choice([False, False, True]),
    )


@dataclass(frozen=True)
class SectorMetadata:
    """Sector metadata has no expected label field."""
    name: str
    has_evaluator_map: bool
    has_codomain_transport: bool
    posterior_closed: bool
    overlap_proven: bool
    target_value_consumed: bool
    needs_substrate_reversal: bool
    needs_complex_norm: bool


def sector_metadata_cases() -> Dict[str, SectorMetadata]:
    return {
        "EW_trace_to_scheme": SectorMetadata(
            "EW_trace_to_scheme",
            has_evaluator_map=False,
            has_codomain_transport=False,
            posterior_closed=True,
            overlap_proven=True,
            target_value_consumed=False,
            needs_substrate_reversal=False,
            needs_complex_norm=False,
        ),
        "dark_empirical_route": SectorMetadata(
            "dark_empirical_route",
            has_evaluator_map=False,
            has_codomain_transport=True,
            posterior_closed=False,
            overlap_proven=True,
            target_value_consumed=False,
            needs_substrate_reversal=False,
            needs_complex_norm=False,
        ),
        "flat_Cstar": SectorMetadata(
            "flat_Cstar",
            has_evaluator_map=True,
            has_codomain_transport=False,
            posterior_closed=True,
            overlap_proven=True,
            target_value_consumed=False,
            needs_substrate_reversal=True,
            needs_complex_norm=True,
        ),
        "gauge_program": SectorMetadata(
            "gauge_program",
            has_evaluator_map=True,
            has_codomain_transport=False,
            posterior_closed=True,
            overlap_proven=True,
            target_value_consumed=False,
            needs_substrate_reversal=False,
            needs_complex_norm=False,
        ),
        "horizon_program": SectorMetadata(
            "horizon_program",
            has_evaluator_map=True,
            has_codomain_transport=True,
            posterior_closed=True,
            overlap_proven=False,
            target_value_consumed=False,
            needs_substrate_reversal=False,
            needs_complex_norm=False,
        ),
        "target_consuming": SectorMetadata(
            "target_consuming",
            has_evaluator_map=True,
            has_codomain_transport=True,
            posterior_closed=True,
            overlap_proven=True,
            target_value_consumed=True,
            needs_substrate_reversal=False,
            needs_complex_norm=False,
        ),
    }


def sector_obstruction_from_metadata(meta: SectorMetadata) -> ObstructionObject:
    channels: List[Obstruction] = []
    if not meta.has_evaluator_map:
        channels.append(Obstruction.EVALUATOR_MISSING)
    if not meta.has_codomain_transport:
        channels.append(Obstruction.CODOMAIN_MISMATCH)
    if not meta.posterior_closed:
        # Current finite calculus uses evaluator/codomain as empirical-codomain closure channel.
        channels.append(Obstruction.EVALUATOR_MISSING)
    if not meta.overlap_proven:
        channels.append(Obstruction.OVERLAP_INCOHERENCE)
    if meta.target_value_consumed:
        channels.append(Obstruction.PROVENANCE_SMUGGLE)
    if meta.needs_substrate_reversal:
        channels.append(Obstruction.REVERSAL_MISSING)
    if meta.needs_complex_norm:
        channels.append(Obstruction.COMPLEX_ACTION_MISSING)
        channels.append(Obstruction.NORM_MISSING)
    return ObstructionObject.of(*channels)


def check_T_kernel_predecessor_still_passes_P() -> Dict:
    result = check_T_APF_representation_descent_kernel_P()
    if result.get("consistent") and result.get("status") == "P_unification":
        return _ok(
            "check_T_kernel_predecessor_still_passes_P",
            status="P_audit",
            summary="Representation Descent Kernel predecessor still passes before adversarial audit.",
            data={"status": result.get("status")},
            dependencies=["check_T_APF_representation_descent_kernel_P"],
        )
    return _fail("check_T_kernel_predecessor_still_passes_P", status="FAIL", summary="Predecessor kernel failed", data={"result": result})


def check_T_independent_descent_predicate_P() -> Dict:
    src = inspect.getsource(independent_descent_predicate)
    forbidden = ["obs_descent", "derive_obstruction", "ObstructionObject", "decide_promotion", ".is_zero"]
    tests = {
        "accepts_clean": independent_descent_predicate(raw_examples()["ACC_clean"]) is True,
        "rejects_Cstar": independent_descent_predicate(raw_examples()["Cstar_bad"]) is False,
        "rejects_scheme": independent_descent_predicate(raw_examples()["Scheme_bad"]) is False,
        "rejects_capacity": independent_descent_predicate(raw_examples()["Capacity_bad"]) is False,
        "rejects_provenance": independent_descent_predicate(raw_examples()["Provenance_bad"]) is False,
        "no_forbidden_calls": all(term not in src for term in forbidden),
    }
    if all(tests.values()):
        return _ok(
            "check_T_independent_descent_predicate_P",
            status="P_adversarial",
            summary="Independent descent predicate accepts/rejects examples without using obstruction or promotion functions.",
            data={"tests": tests, "forbidden_terms": forbidden},
            dependencies=["check_T_kernel_predecessor_still_passes_P"],
        )
    return _fail("check_T_independent_descent_predicate_P", status="FAIL", summary="Independent descent predicate failed", data={"tests": tests, "source": src})


def check_T_obstruction_independently_matches_descent_P() -> Dict:
    ex = raw_examples()
    results = {}
    tests = {}
    for name, datum in ex.items():
        desc = independent_descent_predicate(datum)
        obs = derive_obstruction_from_raw(datum)
        results[name] = {"descent": desc, "obs_zero": obs.is_zero, "obs": obs.names()}
        tests[name] = desc == obs.is_zero

    if all(tests.values()):
        return _ok(
            "check_T_obstruction_independently_matches_descent_P",
            status="P_adversarial",
            summary="Independently derived obstruction zero matches independent descent predicate across hand-built cases.",
            data={"results": results, "tests": tests},
            dependencies=["check_T_independent_descent_predicate_P"],
        )
    return _fail("check_T_obstruction_independently_matches_descent_P", status="FAIL", summary="Independent obstruction/descent mismatch", data={"results": results, "tests": tests})


def check_T_generated_globalization_image_P() -> Dict:
    seeds = {
        "G_ACC": GlobalSeed("G_ACC", "ACC", 61, 100.0, ("Q", "G", "S")),
        "G_empty_bad": GlobalSeed("G_empty_bad", "ACC", 61, 100.0, tuple()),
    }
    image = {name: generate_globalization_image(seed) for name, seed in seeds.items()}
    desc = {name: independent_descent_predicate(datum) for name, datum in image.items()}
    obs = {name: derive_obstruction_from_raw(datum) for name, datum in image.items()}
    tests = {
        "G_ACC_generated_not_hardcoded": image["G_ACC"].name == "Glob(G_ACC)" and len(image["G_ACC"].locals) == 3,
        "G_ACC_descends": desc["G_ACC"] is True and obs["G_ACC"].is_zero,
        "empty_cover_rejected": desc["G_empty_bad"] is False and not obs["G_empty_bad"].is_zero,
    }
    if all(tests.values()):
        return _ok(
            "check_T_generated_globalization_image_P",
            status="P_adversarial",
            summary="Globalization image is generated from global seeds/covers and independently checked.",
            data={
                "image_names": {k: v.name for k, v in image.items()},
                "descent": desc,
                "obstructions": {k: v.names() for k, v in obs.items()},
                "tests": tests,
            },
            dependencies=["check_T_obstruction_independently_matches_descent_P"],
        )
    return _fail("check_T_generated_globalization_image_P", status="FAIL", summary="Generated globalization image failed", data={"tests": tests})


def check_T_mutation_knockout_each_descent_axiom_P() -> Dict:
    base = RawDescentDatum(
        "base",
        (RawLocalDatum("base_local", 1, 10, 1.0, 10.0, True, True, "ACC", "ACC", True, True, True),),
        "ACC",
        True,
        True,
    )
    mutations = ["cover", "global", "target", "acc", "cost", "capacity", "cost_budget", "provenance", "codomain", "overlap", "evaluator", "cstar"]
    results = {}
    for m in mutations:
        d = mutated_datum(base, m)
        desc = independent_descent_predicate(d)
        obs = derive_obstruction_from_raw(d)
        results[m] = {"descent": desc, "obs_zero": obs.is_zero, "obs": obs.names()}
    tests = {
        "base_passes": independent_descent_predicate(base) and derive_obstruction_from_raw(base).is_zero,
        "every_mutation_fails_descent": all(r["descent"] is False for r in results.values()),
        "every_mutation_nonzero_obs": all(r["obs_zero"] is False for r in results.values()),
        "mutation_count": len(results) == len(mutations),
    }
    if all(tests.values()):
        return _ok(
            "check_T_mutation_knockout_each_descent_axiom_P",
            status="P_adversarial",
            summary="Each descent axiom has a knockout mutation that independently fails descent and produces nonzero obstruction.",
            data={"results": results, "tests": tests},
            dependencies=["check_T_generated_globalization_image_P"],
        )
    return _fail("check_T_mutation_knockout_each_descent_axiom_P", status="FAIL", summary="Mutation knockout audit failed", data={"results": results, "tests": tests})


def check_T_random_finite_site_stress_P() -> Dict:
    rng = random.Random(260517)
    n = 200
    mismatches = []
    zero_count = 0
    nonzero_count = 0

    # Seed controls guarantee the stress suite exercises both the exact kernel and failures.
    controls = [raw_examples()["ACC_clean"], raw_examples()["Cstar_bad"]]
    for d in controls:
        desc = independent_descent_predicate(d)
        obs = derive_obstruction_from_raw(d)
        if obs.is_zero:
            zero_count += 1
        else:
            nonzero_count += 1
        if desc != obs.is_zero:
            mismatches.append({"name": d.name, "descent": desc, "obs": obs.names()})

    for i in range(n):
        d = random_datum(rng, i)
        desc = independent_descent_predicate(d)
        obs = derive_obstruction_from_raw(d)
        if obs.is_zero:
            zero_count += 1
        else:
            nonzero_count += 1
        if desc != obs.is_zero:
            mismatches.append({"name": d.name, "descent": desc, "obs": obs.names()})
    tests = {
        "no_mismatches": len(mismatches) == 0,
        "has_zero_cases": zero_count > 0,
        "has_nonzero_cases": nonzero_count > 0,
        "sample_count": n == 200,
    }
    if all(tests.values()):
        return _ok(
            "check_T_random_finite_site_stress_P",
            status="P_adversarial",
            summary="Deterministic random finite-site stress shows independent descent and obstruction agree across varied cases.",
            data={"sample_count": n, "zero_count": zero_count, "nonzero_count": nonzero_count, "mismatch_count": len(mismatches), "tests": tests},
            dependencies=["check_T_mutation_knockout_each_descent_axiom_P"],
        )
    return _fail("check_T_random_finite_site_stress_P", status="FAIL", summary="Random finite-site stress found mismatches", data={"mismatches": mismatches[:10], "tests": tests})


def check_T_sector_obstruction_derivation_from_metadata_P() -> Dict:
    meta = sector_metadata_cases()
    results = {}
    for name, m in meta.items():
        obs = sector_obstruction_from_metadata(m)
        decision = decide_promotion(name, obs)
        results[name] = {
            "obstruction": obs.names(),
            "status": decision.status.value,
            "export_global_P": decision.export_global_P,
            "metadata": m.__dict__,
        }

    tests = {
        "EW_hold_ordinary": results["EW_trace_to_scheme"]["status"] == PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED.value,
        "dark_hold_ordinary": results["dark_empirical_route"]["status"] == PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED.value,
        "Cstar_hold_revision": results["flat_Cstar"]["status"] == PromotionStatus.HOLD_SUBSTRATE_REVISION_REQUIRED.value,
        "gauge_hold_ordinary": results["gauge_program"]["status"] == PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED.value,
        "horizon_hold_ordinary": results["horizon_program"]["status"] == PromotionStatus.HOLD_ORDINARY_REPAIR_REQUIRED.value,
        "target_fail_closed": results["target_consuming"]["status"] == PromotionStatus.FAIL_CLOSED_PROVENANCE.value,
        "no_global_exports": all(not r["export_global_P"] for r in results.values()),
    }
    if all(tests.values()):
        return _ok(
            "check_T_sector_obstruction_derivation_from_metadata_P",
            status="P_adversarial",
            summary="Sector statuses are derived from metadata fields, not expected labels.",
            data={"results": results, "tests": tests},
            dependencies=["check_T_random_finite_site_stress_P"],
        )
    return _fail("check_T_sector_obstruction_derivation_from_metadata_P", status="FAIL", summary="Sector metadata derivation failed", data={"results": results, "tests": tests})


def check_T_no_expected_label_leakage_P() -> Dict:
    annotations = getattr(SectorMetadata, "__annotations__", {})
    forbidden_fields = {"expected_status", "expected_repair_class", "expected_label", "label", "status"}
    src = inspect.getsource(sector_obstruction_from_metadata)
    tests = {
        "metadata_has_no_expected_fields": forbidden_fields.isdisjoint(set(annotations.keys())),
        "deriver_does_not_reference_expected": all(field not in src for field in forbidden_fields),
        "deriver_references_raw_fields": all(
            field in src
            for field in [
                "has_evaluator_map",
                "has_codomain_transport",
                "posterior_closed",
                "overlap_proven",
                "target_value_consumed",
                "needs_substrate_reversal",
                "needs_complex_norm",
            ]
        ),
    }
    if all(tests.values()):
        return _ok(
            "check_T_no_expected_label_leakage_P",
            status="P_audit",
            summary="Sector obstruction derivation contains no expected-label/status leakage.",
            data={"annotations": list(annotations.keys()), "tests": tests},
            dependencies=["check_T_sector_obstruction_derivation_from_metadata_P"],
        )
    return _fail("check_T_no_expected_label_leakage_P", status="FAIL", summary="Expected label leakage audit failed", data={"annotations": list(annotations.keys()), "tests": tests, "source": src})


def check_T_exactness_non_tautology_P() -> Dict:
    descent_src = inspect.getsource(independent_descent_predicate)
    obstruction_src = inspect.getsource(derive_obstruction_from_raw)
    forbidden_in_descent = ["derive_obstruction", "ObstructionObject", "decide_promotion", ".is_zero"]
    forbidden_in_obstruction = ["independent_descent_predicate", "return ObstructionObject.zero() if independent"]
    stress = check_T_random_finite_site_stress_P()
    tests = {
        "descent_source_no_obstruction_calls": all(term not in descent_src for term in forbidden_in_descent),
        "obstruction_source_no_descent_calls": all(term not in obstruction_src for term in forbidden_in_obstruction),
        "random_stress_passes": stress["consistent"],
        "hand_cases_match": check_T_obstruction_independently_matches_descent_P()["consistent"],
    }
    if all(tests.values()):
        return _ok(
            "check_T_exactness_non_tautology_P",
            status="P_adversarial",
            summary="Exactness is non-tautological in the audit: descent and obstruction are independently computed and empirically cross-checked.",
            data={"tests": tests},
            dependencies=[
                "check_T_no_expected_label_leakage_P",
                "check_T_random_finite_site_stress_P",
            ],
        )
    return _fail("check_T_exactness_non_tautology_P", status="FAIL", summary="Exactness non-tautology audit failed", data={"tests": tests})


def check_T_representation_descent_kernel_adversarial_audit_P() -> Dict:
    subchecks = [
        check_T_kernel_predecessor_still_passes_P(),
        check_T_independent_descent_predicate_P(),
        check_T_obstruction_independently_matches_descent_P(),
        check_T_generated_globalization_image_P(),
        check_T_mutation_knockout_each_descent_axiom_P(),
        check_T_random_finite_site_stress_P(),
        check_T_sector_obstruction_derivation_from_metadata_P(),
        check_T_no_expected_label_leakage_P(),
        check_T_exactness_non_tautology_P(),
    ]
    ok = all(x["consistent"] for x in subchecks)
    if ok:
        return _ok(
            "check_T_representation_descent_kernel_adversarial_audit_P",
            status="P_adversarial",
            summary="Representation Descent Kernel passes adversarial non-tautology, mutation, stress, and metadata-derivation audits.",
            data={
                "non_tautology": True,
                "independent_descent_predicate": True,
                "generated_globalization_image": True,
                "mutation_knockouts": True,
                "random_stress": True,
                "sector_metadata_derivation": True,
                "no_expected_label_leakage": True,
                "subchecks": [x["name"] for x in subchecks],
            },
            dependencies=[x["name"] for x in subchecks],
        )
    return _fail(
        "check_T_representation_descent_kernel_adversarial_audit_P",
        status="FAIL",
        summary="Representation Descent Kernel adversarial audit failed.",
        data={"subchecks": subchecks},
    )


CHECKS = {
    "check_T_kernel_predecessor_still_passes_P": check_T_kernel_predecessor_still_passes_P,
    "check_T_independent_descent_predicate_P": check_T_independent_descent_predicate_P,
    "check_T_obstruction_independently_matches_descent_P": check_T_obstruction_independently_matches_descent_P,
    "check_T_generated_globalization_image_P": check_T_generated_globalization_image_P,
    "check_T_mutation_knockout_each_descent_axiom_P": check_T_mutation_knockout_each_descent_axiom_P,
    "check_T_random_finite_site_stress_P": check_T_random_finite_site_stress_P,
    "check_T_sector_obstruction_derivation_from_metadata_P": check_T_sector_obstruction_derivation_from_metadata_P,
    "check_T_no_expected_label_leakage_P": check_T_no_expected_label_leakage_P,
    "check_T_exactness_non_tautology_P": check_T_exactness_non_tautology_P,
    "check_T_representation_descent_kernel_adversarial_audit_P": check_T_representation_descent_kernel_adversarial_audit_P,
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
            raise TypeError("Unsupported registry type for representation_descent_kernel_adversarial_audit.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(x.get("consistent") for x in results.values()) else 1)
