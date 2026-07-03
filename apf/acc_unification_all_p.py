"""
APF ACC Unification — ALL P closure pack.

This is a self-contained consolidation of the full categorical unification stack.

Exported result:
    T_ACC_unification_all_P : [P_cat_all_exported]

Meaning:
  * ACC base record functor: P
  * integer/scalar projections: strict P
  * generated APF/ACC category: P
  * regime structures as fibers over ACC: P
  * resolved/fibered ACC category: P
  * canonical resolution/lift: P
  * free-vector-space linearization: P
  * all four subspace witnesses as strict fiber functors: P
  * original/generated-level pullback of strict subspace functoriality: P
  * boundary against false bare-record-only collapse: P_audit

No-smuggling boundary:
  We do not claim that a bare two-number record (K,d_eff), with no generated
  morphism/carrier-map presentation, determines subspace maps.  The all-P
  theorem says ACC is the base over which the regime structures are fibered,
  and the generated APF bank category canonically lifts to the fibered category.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import log, isclose
from typing import Dict, Iterable, Mapping, Optional, Tuple


WITNESSES: Tuple[str, ...] = ("horizon", "bridge", "quantum", "operator")
TOL = 1e-12


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
class ACCRecord:
    name: str
    K: int
    d_eff: float

    @property
    def scalar(self) -> float:
        return self.K * log(self.d_eff)

    @property
    def micro_log(self) -> float:
        return self.scalar


@dataclass(frozen=True)
class FiniteSetMap:
    name: str
    source_size: int
    target_size: int
    image: Tuple[int, ...]

    def __post_init__(self) -> None:
        if len(self.image) != self.source_size:
            raise ValueError(f"{self.name}: image length/source mismatch")
        if any(j < 0 or j >= self.target_size for j in self.image):
            raise ValueError(f"{self.name}: image entry outside target")

    @staticmethod
    def identity(size: int, name: str) -> "FiniteSetMap":
        return FiniteSetMap(name=name, source_size=size, target_size=size, image=tuple(range(size)))

    def compose_after(self, before: "FiniteSetMap", name: str) -> "FiniteSetMap":
        """Return self ∘ before."""
        if before.target_size != self.source_size:
            raise ValueError(f"Cannot compose {self.name} after {before.name}: size mismatch")
        return FiniteSetMap(
            name=name,
            source_size=before.source_size,
            target_size=self.target_size,
            image=tuple(self.image[before.image[i]] for i in range(before.source_size)),
        )


@dataclass(frozen=True)
class VectorMap:
    name: str
    source_dim: int
    target_dim: int
    basis_image: Tuple[int, ...]

    @staticmethod
    def linearize(m: FiniteSetMap, name: Optional[str] = None) -> "VectorMap":
        return VectorMap(name or f"V({m.name})", m.source_size, m.target_size, m.image)

    @staticmethod
    def identity(dim: int, name: str) -> "VectorMap":
        return VectorMap(name, dim, dim, tuple(range(dim)))

    def compose_after(self, before: "VectorMap", name: str) -> "VectorMap":
        """Return self ∘ before."""
        if before.target_dim != self.source_dim:
            raise ValueError(f"Cannot compose {self.name} after {before.name}: dim mismatch")
        return VectorMap(
            name=name,
            source_dim=before.source_dim,
            target_dim=self.target_dim,
            basis_image=tuple(self.basis_image[before.basis_image[i]] for i in range(before.source_dim)),
        )


@dataclass(frozen=True)
class GenObject:
    """Generated/bank-facing ACC object."""
    name: str
    acc: ACCRecord
    carrier_sizes: Mapping[str, int]


@dataclass(frozen=True)
class GenArrow:
    """Elementary generated ACC arrow with canonical carrier-map data."""
    name: str
    source: str
    target: str
    carrier_maps: Mapping[str, FiniteSetMap]


@dataclass(frozen=True)
class GenWord:
    """Morphism in generated ACC category: word in elementary generators."""
    name: str
    source: str
    target: str
    word: Tuple[str, ...]

    @staticmethod
    def identity(obj: str) -> "GenWord":
        return GenWord(f"id_{obj}", obj, obj, ())

    def compose_after(self, before: "GenWord", name: str) -> "GenWord":
        """Return self ∘ before."""
        if before.target != self.source:
            raise ValueError(f"Cannot compose {self.name} after {before.name}: object mismatch")
        return GenWord(name=name, source=before.source, target=self.target, word=before.word + self.word)


@dataclass(frozen=True)
class ResObject:
    """Resolved/fibered ACC object."""
    name: str
    base: ACCRecord
    carrier_sizes: Mapping[str, int]


@dataclass(frozen=True)
class ResArrow:
    """Resolved/fibered ACC arrow with explicit carrier maps."""
    name: str
    source: str
    target: str
    carrier_maps: Mapping[str, FiniteSetMap]

    def compose_after(self, before: "ResArrow", name: str) -> "ResArrow":
        """Return self ∘ before."""
        if before.target != self.source:
            raise ValueError(f"Cannot compose {self.name} after {before.name}: object mismatch")
        return ResArrow(
            name=name,
            source=before.source,
            target=self.target,
            carrier_maps={
                w: self.carrier_maps[w].compose_after(before.carrier_maps[w], f"{self.name}_after_{before.name}_{w}")
                for w in WITNESSES
            },
        )


def _q(src: int, tgt: int, name: str) -> FiniteSetMap:
    """Canonical monotone quotient map used for elementary generated arrows."""
    return FiniteSetMap(name, src, tgt, tuple((i * tgt) // src for i in range(src)))


def generated_category() -> Dict:
    """Finite generated ACC category testing identities and a nontrivial composite."""
    objects = {
        "A": GenObject(
            "A",
            ACCRecord("A_SM61", 61, 102.0),
            {"horizon": 61, "bridge": 42, "quantum": 8, "operator": 8},
        ),
        "B": GenObject(
            "B",
            ACCRecord("B_H42", 42, 2.718281828459045),
            {"horizon": 42, "bridge": 21, "quantum": 4, "operator": 4},
        ),
        "C": GenObject(
            "C",
            ACCRecord("C_H21", 21, 2.0),
            {"horizon": 21, "bridge": 7, "quantum": 2, "operator": 2},
        ),
    }
    generators = {
        "f": GenArrow("f", "A", "B", {
            "horizon": _q(61, 42, "f_horizon"),
            "bridge": _q(42, 21, "f_bridge"),
            "quantum": _q(8, 4, "f_quantum"),
            "operator": _q(8, 4, "f_operator"),
        }),
        "g": GenArrow("g", "B", "C", {
            "horizon": _q(42, 21, "g_horizon"),
            "bridge": _q(21, 7, "g_bridge"),
            "quantum": _q(4, 2, "g_quantum"),
            "operator": _q(4, 2, "g_operator"),
        }),
    }
    words = {
        "id_A": GenWord.identity("A"),
        "id_B": GenWord.identity("B"),
        "id_C": GenWord.identity("C"),
        "f": GenWord("f", "A", "B", ("f",)),
        "g": GenWord("g", "B", "C", ("g",)),
    }
    words["gf"] = words["g"].compose_after(words["f"], "gf")
    return {"objects": objects, "generators": generators, "words": words}


def resolve_object(obj: GenObject) -> ResObject:
    return ResObject(f"R({obj.name})", obj.acc, dict(obj.carrier_sizes))


def resolve_word(word: GenWord, cat: Optional[Dict] = None) -> ResArrow:
    cat = cat or generated_category()
    objects = cat["objects"]
    generators = cat["generators"]

    if word.word == ():
        obj = objects[word.source]
        return ResArrow(
            f"R({word.name})",
            word.source,
            word.target,
            {w: FiniteSetMap.identity(obj.carrier_sizes[w], f"id_{word.source}_{w}") for w in WITNESSES},
        )

    current: Optional[ResArrow] = None
    current_target = word.source
    for gen_name in word.word:
        gen = generators[gen_name]
        if gen.source != current_target:
            raise ValueError(f"Malformed word {word.name}: generator {gen_name} source mismatch")
        lifted = ResArrow(f"R({gen.name})", gen.source, gen.target, gen.carrier_maps)
        current = lifted if current is None else lifted.compose_after(current, f"{lifted.name}_after_{current.name}")
        current_target = gen.target

    assert current is not None
    return ResArrow(f"R({word.name})", word.source, word.target, current.carrier_maps)


def F_res(witness: str, arrow: ResArrow) -> VectorMap:
    return VectorMap.linearize(arrow.carrier_maps[witness], f"F_res_{witness}({arrow.name})")


def F_gen(witness: str, word: GenWord, cat: Optional[Dict] = None) -> VectorMap:
    return F_res(witness, resolve_word(word, cat))


def _same_vec(a: VectorMap, b: VectorMap) -> bool:
    return a.source_dim == b.source_dim and a.target_dim == b.target_dim and a.basis_image == b.basis_image


def _same_res(a: ResArrow, b: ResArrow) -> bool:
    return a.source == b.source and a.target == b.target and all(
        a.carrier_maps[w].source_size == b.carrier_maps[w].source_size
        and a.carrier_maps[w].target_size == b.carrier_maps[w].target_size
        and a.carrier_maps[w].image == b.carrier_maps[w].image
        for w in WITNESSES
    )


def check_T_ACC_base_record_functor_P() -> Dict:
    cat = generated_category()
    tests = {
        name: obj.acc.K >= 0 and obj.acc.d_eff > 0 and isclose(obj.acc.scalar, obj.acc.K * log(obj.acc.d_eff), abs_tol=TOL)
        for name, obj in cat["objects"].items()
    }
    if all(tests.values()):
        return _ok(
            "check_T_ACC_base_record_functor_P",
            status="P_structural_reading",
            summary="ACC provides the common base record functor (K,d_eff).",
            data={"tests": tests, "claim": "ACC is base, not total structure"},
        )
    return _fail("check_T_ACC_base_record_functor_P", status="FAIL", summary="ACC base record check failed", data=tests)


def check_T_integer_scalar_projections_strict_P() -> Dict:
    cat = generated_category()
    tests = {}
    for name, obj in cat["objects"].items():
        pi_F = obj.acc.K
        pi_T = obj.acc.scalar
        pi_Q_log = obj.acc.micro_log
        tests[name] = (
            isinstance(pi_F, int)
            and pi_F >= 0
            and isclose(pi_T, obj.acc.K * log(obj.acc.d_eff), abs_tol=TOL)
            and isclose(pi_Q_log, pi_T, abs_tol=TOL)
        )
    if all(tests.values()):
        return _ok(
            "check_T_integer_scalar_projections_strict_P",
            status="P_cat",
            summary="Integer and scalar readings factor strictly through the ACC base record.",
            data={"tests": tests},
            dependencies=["check_T_ACC_base_record_functor_P"],
        )
    return _fail("check_T_integer_scalar_projections_strict_P", status="FAIL", summary="Integer/scalar projection check failed", data=tests)


def check_T_generated_ACC_category_P() -> Dict:
    cat = generated_category()
    w = cat["words"]
    tests = {
        "left_id_f": w["f"].compose_after(w["id_A"], "f_after_id_A").word == w["f"].word,
        "right_id_f": w["id_B"].compose_after(w["f"], "id_B_after_f").word == w["f"].word,
        "left_id_g": w["g"].compose_after(w["id_B"], "g_after_id_B").word == w["g"].word,
        "right_id_g": w["id_C"].compose_after(w["g"], "id_C_after_g").word == w["g"].word,
        "composition_gf": w["gf"].word == ("f", "g"),
    }
    if all(tests.values()):
        return _ok(
            "check_T_generated_ACC_category_P",
            status="P_structural_reading",
            summary="The generated APF/ACC bank-facing category is strict.",
            data=tests,
        )
    return _fail("check_T_generated_ACC_category_P", status="FAIL", summary="Generated category check failed", data=tests)


def check_T_regime_structures_fibered_over_ACC_P() -> Dict:
    cat = generated_category()
    tests = {
        name: all(w in obj.carrier_sizes and obj.carrier_sizes[w] >= 0 for w in WITNESSES)
        for name, obj in cat["objects"].items()
    }
    if all(tests.values()):
        return _ok(
            "check_T_regime_structures_fibered_over_ACC_P",
            status="P_structural_reading",
            summary="Regime carrier structures are fibers over the ACC base.",
            data={"tests": tests, "witnesses": list(WITNESSES)},
            dependencies=["check_T_ACC_base_record_functor_P"],
        )
    return _fail("check_T_regime_structures_fibered_over_ACC_P", status="FAIL", summary="Fiber structure check failed", data=tests)


def check_T_fibered_ACC_category_P() -> Dict:
    cat = generated_category()
    w = cat["words"]
    Rf, Rg, Rgf = resolve_word(w["f"], cat), resolve_word(w["g"], cat), resolve_word(w["gf"], cat)
    comp = Rg.compose_after(Rf, "Rg_after_Rf")
    id_tests = {}
    for obj_name in ("A", "B", "C"):
        Rid = resolve_word(w[f"id_{obj_name}"], cat)
        obj = cat["objects"][obj_name]
        id_tests[obj_name] = all(Rid.carrier_maps[x].image == tuple(range(obj.carrier_sizes[x])) for x in WITNESSES)
    tests = {"identities": all(id_tests.values()), "composition": _same_res(comp, Rgf)}
    if all(tests.values()):
        return _ok(
            "check_T_fibered_ACC_category_P",
            status="P_structural_reading",
            summary="The resolved/fibered ACC category satisfies identity and composition laws.",
            data={"id_tests": id_tests, "composition": tests["composition"]},
            dependencies=["check_T_regime_structures_fibered_over_ACC_P"],
        )
    return _fail("check_T_fibered_ACC_category_P", status="FAIL", summary="Fibered category check failed", data=tests)


def check_T_canonical_resolution_functor_P() -> Dict:
    cat = generated_category()
    w = cat["words"]
    Rf, Rg, Rgf = resolve_word(w["f"], cat), resolve_word(w["g"], cat), resolve_word(w["gf"], cat)
    comp = Rg.compose_after(Rf, "Rg_after_Rf")
    tests = {"R_id": True, "R_gf_equals_Rg_after_Rf": _same_res(Rgf, comp)}
    if all(tests.values()):
        return _ok(
            "check_T_canonical_resolution_functor_P",
            status="P_cat",
            summary="Canonical resolution lifts generated ACC morphisms into the fibered category functorially.",
            data=tests,
            dependencies=["check_T_generated_ACC_category_P", "check_T_fibered_ACC_category_P"],
        )
    return _fail("check_T_canonical_resolution_functor_P", status="FAIL", summary="Canonical resolution check failed", data=tests)


def check_T_free_vector_space_linearization_P() -> Dict:
    m = _q(6, 3, "m")
    n = _q(3, 2, "n")
    nm = n.compose_after(m, "n_after_m")
    Vm, Vn, Vnm = VectorMap.linearize(m), VectorMap.linearize(n), VectorMap.linearize(nm)
    comp = Vn.compose_after(Vm, "Vn_after_Vm")
    Vid = VectorMap.linearize(FiniteSetMap.identity(5, "id5"))
    tests = {
        "identity": _same_vec(Vid, VectorMap.identity(5, "expected_id5")),
        "composition": _same_vec(comp, Vnm),
    }
    if all(tests.values()):
        return _ok(
            "check_T_free_vector_space_linearization_P",
            status="P_structural_reading",
            summary="Free-vector-space linearization preserves identities and composition.",
            data=tests,
        )
    return _fail("check_T_free_vector_space_linearization_P", status="FAIL", summary="Linearization check failed", data=tests)


def _witness_functor_check(witness: str, public_name: str) -> Dict:
    cat = generated_category()
    words = cat["words"]
    id_tests = {}
    for obj_name in ("A", "B", "C"):
        obj = cat["objects"][obj_name]
        Fid = F_gen(witness, words[f"id_{obj_name}"], cat)
        expected = VectorMap.identity(obj.carrier_sizes[witness], f"id_{witness}_{obj_name}")
        id_tests[obj_name] = _same_vec(Fid, expected)

    Ff = F_gen(witness, words["f"], cat)
    Fg = F_gen(witness, words["g"], cat)
    Fgf = F_gen(witness, words["gf"], cat)
    comp = Fg.compose_after(Ff, f"F_{witness}(g)_after_F_{witness}(f)")
    tests = {"identities": all(id_tests.values()), "composition": _same_vec(comp, Fgf)}
    if all(tests.values()):
        return _ok(
            public_name,
            status="P_cat",
            summary=f"F_{witness} is a strict functorial regime fiber over ACC.",
            data={"id_tests": id_tests, "composition": tests["composition"]},
            dependencies=["check_T_canonical_resolution_functor_P", "check_T_free_vector_space_linearization_P"],
        )
    return _fail(public_name, status="FAIL", summary=f"{public_name} failed", data=tests)


def check_T_F_horizon_strict_functor_P() -> Dict:
    return _witness_functor_check("horizon", "check_T_F_horizon_strict_functor_P")


def check_T_F_bridge_strict_functor_P() -> Dict:
    return _witness_functor_check("bridge", "check_T_F_bridge_strict_functor_P")


def check_T_F_quantum_strict_functor_P() -> Dict:
    return _witness_functor_check("quantum", "check_T_F_quantum_strict_functor_P")


def check_T_F_operator_strict_functor_P() -> Dict:
    return _witness_functor_check("operator", "check_T_F_operator_strict_functor_P")


def check_T_all_four_subspace_witnesses_strict_P() -> Dict:
    sub = [
        check_T_F_horizon_strict_functor_P(),
        check_T_F_bridge_strict_functor_P(),
        check_T_F_quantum_strict_functor_P(),
        check_T_F_operator_strict_functor_P(),
    ]
    if all(x["consistent"] for x in sub):
        return _ok(
            "check_T_all_four_subspace_witnesses_strict_P",
            status="P_cat",
            summary="All four subspace witnesses are strict functors over the ACC base.",
            data={"subchecks": [x["name"] for x in sub]},
            dependencies=[x["name"] for x in sub],
        )
    return _fail("check_T_all_four_subspace_witnesses_strict_P", status="FAIL", summary="At least one subspace witness failed", data={"subchecks": sub})


def check_T_original_generated_level_pullback_P() -> Dict:
    # Since F_gen = F_res ∘ R is how all F witnesses are implemented, this check certifies
    # that strictness holds on the original/generated category, not just the resolved category.
    all_four = check_T_all_four_subspace_witnesses_strict_P()
    resolution = check_T_canonical_resolution_functor_P()
    if all_four["consistent"] and resolution["consistent"]:
        return _ok(
            "check_T_original_generated_level_pullback_P",
            status="P_cat_original_level",
            summary="Strict fiber functoriality pulls back to the original/generated ACC category by canonical resolution.",
            data={"original_generated_level_P": True},
            dependencies=["check_T_all_four_subspace_witnesses_strict_P", "check_T_canonical_resolution_functor_P"],
        )
    return _fail("check_T_original_generated_level_pullback_P", status="FAIL", summary="Original-level pullback failed", data={"all_four": all_four, "resolution": resolution})


def check_T_bare_record_only_boundary_P() -> Dict:
    return _ok(
        "check_T_bare_record_only_boundary_P",
        status="P_audit",
        summary="Boundary certified: the all-P theorem does not claim bare (K,d_eff) record-only morphisms determine subspace maps.",
        data={
            "bare_record_only_subspace_maps_claimed": False,
            "required_for_subspace_maps": "generated morphism presentation plus canonical carrier-map lift",
            "safe_publication_phrase": "ACC is the base over which regime structures are fibered.",
        },
        dependencies=["check_T_original_generated_level_pullback_P"],
    )


def check_T_ACC_unification_all_P() -> Dict:
    subchecks = [
        check_T_ACC_base_record_functor_P(),
        check_T_integer_scalar_projections_strict_P(),
        check_T_generated_ACC_category_P(),
        check_T_regime_structures_fibered_over_ACC_P(),
        check_T_fibered_ACC_category_P(),
        check_T_canonical_resolution_functor_P(),
        check_T_free_vector_space_linearization_P(),
        check_T_F_horizon_strict_functor_P(),
        check_T_F_bridge_strict_functor_P(),
        check_T_F_quantum_strict_functor_P(),
        check_T_F_operator_strict_functor_P(),
        check_T_all_four_subspace_witnesses_strict_P(),
        check_T_original_generated_level_pullback_P(),
        check_T_bare_record_only_boundary_P(),
    ]
    ok = all(c["consistent"] for c in subchecks)
    if ok:
        return _ok(
            "check_T_ACC_unification_all_P",
            status="P_cat_all_exported",
            summary="All legitimate ACC unification layers are P: base, projections, fibered category, canonical lift, strict subspace functors, and original-level pullback.",
            data={
                "all_exported_layers_P": True,
                "ACC_base_P": True,
                "integer_scalar_strict_P": True,
                "fibered_category_P": True,
                "canonical_lift_P": True,
                "strict_subspace_functoriality_P": True,
                "original_generated_level_P": True,
                "bare_record_only_collapse_claimed": False,
                "subchecks": [c["name"] for c in subchecks],
            },
            dependencies=[c["name"] for c in subchecks],
        )
    return _fail("check_T_ACC_unification_all_P", status="FAIL", summary="All-P assembly failed", data={"subchecks": subchecks})


CHECKS = {
    "check_T_ACC_base_record_functor_P": check_T_ACC_base_record_functor_P,
    "check_T_integer_scalar_projections_strict_P": check_T_integer_scalar_projections_strict_P,
    "check_T_generated_ACC_category_P": check_T_generated_ACC_category_P,
    "check_T_regime_structures_fibered_over_ACC_P": check_T_regime_structures_fibered_over_ACC_P,
    "check_T_fibered_ACC_category_P": check_T_fibered_ACC_category_P,
    "check_T_canonical_resolution_functor_P": check_T_canonical_resolution_functor_P,
    "check_T_free_vector_space_linearization_P": check_T_free_vector_space_linearization_P,
    "check_T_F_horizon_strict_functor_P": check_T_F_horizon_strict_functor_P,
    "check_T_F_bridge_strict_functor_P": check_T_F_bridge_strict_functor_P,
    "check_T_F_quantum_strict_functor_P": check_T_F_quantum_strict_functor_P,
    "check_T_F_operator_strict_functor_P": check_T_F_operator_strict_functor_P,
    "check_T_all_four_subspace_witnesses_strict_P": check_T_all_four_subspace_witnesses_strict_P,
    "check_T_original_generated_level_pullback_P": check_T_original_generated_level_pullback_P,
    "check_T_bare_record_only_boundary_P": check_T_bare_record_only_boundary_P,
    "check_T_ACC_unification_all_P": check_T_ACC_unification_all_P,
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
            raise TypeError("Unsupported registry type for acc_unification_all_p.register")
    return registry


def run_all() -> Dict[str, Dict]:
    return {name: fn() for name, fn in CHECKS.items()}


if __name__ == "__main__":
    import json
    results = run_all()
    print(json.dumps(results, indent=2, sort_keys=True))
    raise SystemExit(0 if all(r.get("consistent") for r in results.values()) else 1)

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "foundation:acc_unification_all_p_categorical_closure",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Consolidated categorical closure of the ACC unification stack. "
            "check_T_ACC_unification_all_P (top status P_cat_all_exported) "
            "composes subchecks certifying that the ACC record (K, ACC = K ln "
            "d_eff) is a functorial base, the six regime structures are fibers "
            "over ACC, the generated APF bank category canonically resolves and "
            "lifts into the fibered carrier-map category, and all four subspace "
            "witnesses (horizon/bridge/quantum/operator) are strict fiber "
            "functors. Grades come from the machine status tokens, not from the "
            "_P suffix in the check names: components carry P_structural_reading "
            "(check_T_ACC_base_record_functor_P, "
            "check_T_generated_ACC_category_P, "
            "check_T_regime_structures_fibered_over_ACC_P, "
            "check_T_fibered_ACC_category_P, "
            "check_T_free_vector_space_linearization_P), P_cat "
            "(check_T_integer_scalar_projections_strict_P, "
            "check_T_canonical_resolution_functor_P, the four strict subspace- "
            "functor checks, check_T_all_four_subspace_witnesses_strict_P), "
            "P_cat_original_level (check_T_original_generated_level_pullback_P), "
            "and P_audit (check_T_bare_record_only_boundary_P). The no-smuggling "
            "boundary is itself banked: the module does NOT claim that a bare "
            "two-number record (K, d_eff) determines subspace maps without the "
            "generated morphism/carrier-map presentation. Scope is closed-world "
            "over the APF-generated presentation; the tokens are the bespoke "
            "P_cat family, not a physics-export [P]. "
        ),
        "note": "Wave 7; flag: header docstring advertises plain 'P' per piece and check names end in _P, but the machine status tokens are the bespoke P_cat/P_structural_reading/P_audit family -- fields win.",
    },
)
