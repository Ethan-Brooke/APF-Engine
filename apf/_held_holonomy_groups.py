"""Private H1-H5 finite witnesses for :mod:`apf.held_holonomy`."""
from __future__ import annotations
from ._held_holonomy_common import *
def held_relative_loop_group_impl() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    s3 = _perm_group(3)
    identity: Permutation = (0, 1, 2)
    cycle: Permutation = (1, 2, 0)
    cycle2 = _perm_compose(cycle, cycle)
    a3: FrozenSet[Permutation] = frozenset((identity, cycle, cycle2))

    # A normal-subgroup quotient is a two-sided congruence.
    for g in s3:
        gi = _perm_inverse(g)
        for n in a3:
            ck(_perm_compose(_perm_compose(g, n), gi) in a3,
               "A3 must be normal in S3")

    quotient_signatures = sorted({tuple(sorted(_right_coset(g, a3))) for g in s3})
    ck(len(quotient_signatures) == 2, "S3/A3 has two classes")

    for a, a2, b, b2 in product(s3, repeat=4):
        if _same_right_coset(a, a2, a3) and _same_right_coset(b, b2, a3):
            ck(_same_right_coset(_perm_compose(a, b),
                                _perm_compose(a2, b2), a3),
               "multiplication must descend through two-sided congruence")
    for a, a2 in product(s3, repeat=2):
        if _same_right_coset(a, a2, a3):
            ck(_same_right_coset(_perm_inverse(a), _perm_inverse(a2), a3),
               "inverse must descend through two-sided congruence")

    # Base/reference transport identifies isotropy groups by conjugation.
    transport: Permutation = (1, 0, 2)
    transport_inv = _perm_inverse(transport)

    def conj(g: Permutation) -> Permutation:
        return _perm_compose(_perm_compose(transport, g), transport_inv)

    for g, h in product(s3, repeat=2):
        ck(conj(_perm_compose(g, h)) == _perm_compose(conj(g), conj(h)),
           "reference change must preserve loop multiplication by conjugation")
    ck(any(conj(g) != g for g in s3),
       "nonabelian reference-change control must be nontrivial")

    # One-sided cosets from a non-normal subgroup do not define a quotient group.
    transposition: Permutation = (1, 0, 2)
    h_bad: FrozenSet[Permutation] = frozenset((identity, transposition))
    one_sided_failure = _find_one_sided_failure(s3, h_bad)
    ck(one_sided_failure is not None,
       "non-normal one-sided equivalence must fail well-defined multiplication")

    # Reversal ADMISSION without reversal-is-inverse yields only a monoid.
    # In the two-element monoid {e,a} with a*a=a, the reversal of a is a
    # (admitted, same class), yet a has no inverse.  The group claim therefore
    # consumes reversed-loop-is-inverse as a named premise; closure under
    # reversal alone does not supply it.
    monoid = ("e", "a")
    mtab = {("e", "e"): "e", ("e", "a"): "a", ("a", "e"): "a", ("a", "a"): "a"}
    ck(all(mtab[(mtab[(x, y)], z)] == mtab[(x, mtab[(y, z)])]
           for x in monoid for y in monoid for z in monoid),
       "monoid countermodel must be associative")
    reversal_map = {"e": "e", "a": "a"}
    ck(all(reversal_map[x] in monoid for x in monoid),
       "reversal must be admitted in the monoid countermodel")
    a_has_inverse = any(mtab[("a", z)] == "e" and mtab[(z, "a")] == "e"
                        for z in monoid)
    ck(not a_has_inverse,
       "reversal admission must not manufacture an inverse: the group claim "
       "consumes reversed_loop_is_inverse as a premise")

    # Torsor leg: the descended quotient group acts freely and transitively
    # on the coset space (the finite shadow of the trajectory torsor).
    coset_space = sorted({tuple(sorted(_right_coset(g, a3))) for g in s3})
    quotient_reps = (identity, transposition)
    for c in coset_space:
        images = [tuple(sorted(_right_coset(_perm_compose(q, c[0]), a3)))
                  for q in quotient_reps]
        ck(sorted(images) == coset_space,
           "quotient action on the coset space must be transitive")
        ck(len(set(images)) == len(quotient_reps),
           "quotient action on the coset space must be free")

    path = FinitePath("gamma", "x", "r", "gamma^-1")
    path_class = PathClass(path.name, tuple(sorted(_right_coset(cycle, a3))))

    return _result(
        "T_held_relative_loop_group",
        "P_math",
        ("A reversible path quotient becomes a group only after complete "
         "operational identity is a two-sided congruence AND reversal is the "
         "inverse: the two-element idempotent monoid admits reversal yet has "
         "no inverse, so reversed_loop_is_inverse is a named premise of the "
         "group claim, not a consequence of reversal admission.  The S3/A3 "
         "witness certifies descended multiplication and inverse, the free "
         "transitive quotient action on the coset space (the torsor shadow), "
         "and reference change by conjugation.  A non-normal one-sided "
         "quotient fails."),
        [],
        {
            "positive_group": "S3",
            "normal_subgroup": "A3",
            "quotient_class_count": len(quotient_signatures),
            "reference_change": "inner conjugation in S3",
            "sample_path": asdict(path),
            "sample_path_class": asdict(path_class),
            "one_sided_failure": [list(p) for p in one_sided_failure]
            if one_sided_failure else None,
            "torsor_group_distinction_kept": True,
            "torsor_action_free_and_transitive": True,
            "monoid_countermodel": {
                "elements": list(monoid),
                "law": "a*a=a",
                "reversal_admitted": True,
                "inverse_exists": False,
            },
        },
        fails,
        premises=(
            "reversible_record_free_closure",
            "typed_associative_concatenation",
            "two_sided_complete_operational_congruence",
            "reversed_loop_is_inverse",
        ),
        negative_controls=(
            "right-coset equivalence by non-normal <(12)> in S3",
            "idempotent two-element monoid: reversal admitted, no inverse",
        ),
        cross_refs=(
            "Paper 1 Technical Supplement v9.18: complete continuation identity",
            "Paper 5 Mathematical Note v1.7: relative-loop group and torsor",
        ),
    )


# ---------------------------------------------------------------------------
# H2: a later recombination witness makes the effective loop nontrivial
# ---------------------------------------------------------------------------


def held_recombination_nontriviality_impl() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    completions = ("q_left", "q_right", "q_balanced")
    readouts = {
        "gamma_plus": {"q_left": F(1), "q_right": F(0), "q_balanced": F(1, 2)},
        "gamma_minus": {"q_left": F(0), "q_right": F(1), "q_balanced": F(-1, 2)},
        "eta_1": {"q_left": F(1), "q_right": F(1), "q_balanced": F(0)},
        "eta_2": {"q_left": F(1), "q_right": F(1), "q_balanced": F(0)},
    }

    def signature(name: str) -> Tuple[F, ...]:
        return tuple(readouts[name][q] for q in completions)

    plus = PathClass("gamma_plus", tuple(signature("gamma_plus")))
    minus = PathClass("gamma_minus", tuple(signature("gamma_minus")))
    ck(plus.signature != minus.signature,
       "recombination completion must distinguish the two path classes")

    # The distinguishing completion establishes nonidentity in the OPERATIONAL
    # quotient F_H.  C2 is the smallest witness: 0 identity, 1 non-null.
    operational_relative_loop = 0 if plus.signature == minus.signature else 1
    ck(operational_relative_loop == 1,
       "distinguished paths give a nonidentity operational relative loop")

    eta1 = PathClass("eta_1", tuple(signature("eta_1")))
    eta2 = PathClass("eta_2", tuple(signature("eta_2")))
    ck(eta1.signature == eta2.signature,
       "multiplicity-only negative control must remain quotient-null")
    null_relative_loop = 0 if eta1.signature == eta2.signature else 1
    ck(null_relative_loop == 0,
       "trajectory multiplicity alone must not certify operational holonomy")

    # Representation well-definedness: labels in one operational class carry
    # one declared carrier action.
    class_actions = {"eta_1": _eye(2), "eta_2": _eye(2)}
    ck(_eq(class_actions["eta_1"], class_actions["eta_2"]),
       "the represented action must be constant on operational classes")

    # KERNEL-DEATH CONTROL: operational nontriviality does NOT reach the
    # effective represented quotient F_H^eff = F_H/ker(rho) without faithful
    # first-order action.  The delta pair is separated only by a readout the
    # first-jet carrier does not represent; the declared first-jet action of
    # its relative loop is the identity, so the operationally nonidentity
    # loop dies in ker(rho).
    delta_completions = ("q_second_order",)
    delta_readouts = {
        "delta_1": {"q_second_order": F(1)},
        "delta_2": {"q_second_order": F(-1)},
    }
    delta_sigs = {
        name: tuple(delta_readouts[name][q] for q in delta_completions)
        for name in delta_readouts
    }
    ck(delta_sigs["delta_1"] != delta_sigs["delta_2"],
       "kernel-death pair must be operationally distinguished")
    delta_first_jet_action = _eye(2)
    ck(_eq(delta_first_jet_action, _eye(2)),
       "kernel-death relative loop acts as the identity on the first-jet "
       "carrier: operational nontriviality can die in ker(rho)")

    # Conditional effective horn: under faithful first-order action (the gate
    # consumed at H6), a nonidentity operational class acts nonidentically.
    gamma_first_jet_action = _scal(F(-1), _eye(2))
    ck(not _eq(gamma_first_jet_action, _eye(2)),
       "under the faithfulness gate the gamma relative loop acts "
       "nonidentically on the carrier")

    return _result(
        "T_held_recombination_nontriviality",
        "P_math",
        ("Two record-free trajectories define distinct OPERATIONAL path "
         "classes when one admissible completion/readout separates their "
         "complete signatures; their relative C2 loop is nonidentity in the "
         "operational quotient F_H.  Nonidentity in the EFFECTIVE represented "
         "quotient F_H^eff additionally requires faithful first-order action, "
         "the gate consumed at H6: the kernel-death control exhibits an "
         "operationally nonidentity loop whose first-jet action is the "
         "identity.  Two merely label-distinct trajectories with the same "
         "complete signature remain null, and the represented action is "
         "constant on operational classes."),
        ["T_held_relative_loop_group"],
        {
            "completions": list(completions),
            "gamma_plus_signature": [str(x) for x in plus.signature],
            "gamma_minus_signature": [str(x) for x in minus.signature],
            "operational_relative_loop": operational_relative_loop,
            "multiplicity_only_relative_loop": null_relative_loop,
            "representation_constant_on_classes": True,
            "kernel_death_control": {
                "operationally_distinguished": True,
                "first_jet_action_is_identity": True,
                "moral": "F_H-nontrivial does not imply F_H^eff-nontrivial "
                         "without faithful first-order action",
            },
            "faithful_horn_action": "half-turn -I (nonidentity)",
        },
        fails,
        premises=(
            "complete_operational_path_equivalence",
            "later_admissible_recombination_readout",
            "faithful_first_order_action_for_the_effective_corollary",
        ),
        negative_controls=(
            "two trajectory labels with identical complete continuation signatures",
            "operationally nonidentity loop with identity first-jet action "
            "(kernel death without the faithfulness gate)",
        ),
        cross_refs=(
            "Paper 5 Mathematical Note v1.7: occupied interference witness",
        ),
    )


# ---------------------------------------------------------------------------
# H3/H6 classification: nontrivial connected subgroup of SO(2)
# ---------------------------------------------------------------------------


def _circle_add(x: F, y: F) -> F:
    z = x + y
    return z - (z.numerator // z.denominator)


def _cyclic_subgroup(n: int) -> FrozenSet[F]:
    return frozenset(F(k, n) for k in range(n))


def held_connected_subgroup_so2_impl() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    finite_controls: Dict[str, Dict[str, object]] = {}
    for n in (2, 3, 4, 6):
        c_n = _cyclic_subgroup(n)
        closed = all(_circle_add(a, b) in c_n for a, b in product(c_n, repeat=2))
        inverses = all(_circle_add(a, -a) == 0 for a in c_n)
        disconnected = len(c_n) > 1  # finite Hausdorff connected iff singleton.
        ck(closed and inverses, "C_n must be an exact subgroup of R/Z")
        ck(disconnected, "nontrivial finite C_n is not connected")
        finite_controls[f"C_{n}"] = {
            "order": n,
            "closed_under_angle_addition": closed,
            "connected": False,
        }

    # Exact infinite-order rational rotation: the finite cyclic controls do
    # not exhaust the subgroups of SO(2).  R has cos=3/5, sin=4/5; the
    # Gaussian-integer certificate (3+4i=(2+i)^2, 5=(2+i)(2-i), the primes
    # 2+i and 2-i non-associate) forbids (3+4i)^n = 5^n for n>=1, so R has
    # infinite order; the first 24 powers are computed pairwise distinct.
    r35 = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
    ck(_eq(_mm(_transpose(r35), r35), _eye(2)) and _det2(r35) == 1,
       "the 3/5 rotation must lie in SO(2) exactly")

    def _gmul(z, w):
        return (z[0] * w[0] - z[1] * w[1], z[0] * w[1] + z[1] * w[0])

    two_plus_i = (2, 1)
    ck(_gmul(two_plus_i, two_plus_i) == (3, 4), "(2+i)^2 = 3+4i")
    ck(two_plus_i[0] ** 2 + two_plus_i[1] ** 2 == 5,
       "N(2+i)=5 is prime, so 2+i is a Gaussian prime")
    associates_of_two_plus_i = {(2, 1), (-2, -1), (-1, 2), (1, -2)}
    ck((2, -1) not in associates_of_two_plus_i,
       "2-i is not an associate of 2+i")
    orbit_points = []
    power = _eye(2)
    for n in range(1, 25):
        power = _mm(power, r35)
        orbit_points.append((power[0][0], power[1][0]))
        ck(not _eq(power, _eye(2)),
           "the 3/5 rotation must not return to the identity")
    ck(len(set(orbit_points)) == 24,
       "the first 24 orbit points must be pairwise distinct")

    # Rational parametrization battery: R(t) covers the rational circle and
    # composes by the tangent half-angle addition law.  This is the exact
    # executable shadow of the one-dimensional branch filling SO(2).
    def _rt(t):
        d = 1 + t * t
        return [[(1 - t * t) / d, (-2 * t) / d],
                [(2 * t) / d, (1 - t * t) / d]]

    grid = [F(n, d) for n in range(-3, 4) for d in (1, 2, 3)]
    for t in grid:
        m = _rt(t)
        ck(_eq(_mm(_transpose(m), m), _eye(2)) and _det2(m) == 1,
           "R(t) must lie in SO(2) exactly for rational t")
    composition_checked = 0
    for t1 in grid:
        for t2 in grid:
            if t1 * t2 == 1:
                continue
            ck(_eq(_mm(_rt(t1), _rt(t2)), _rt((t1 + t2) / (1 - t1 * t2))),
               "R(t) must compose by the tangent addition law")
            composition_checked += 1
    pythagorean_directions = (
        (F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)), (F(8, 17), F(15, 17)),
        (F(-3, 5), F(4, 5)), (F(0), F(1)), (F(1), F(0)),
    )
    for a, b in pythagorean_directions:
        ck(a * a + b * b == 1, "direction must be an exact unit vector")
        if a != -1:
            ck(_mv(_rt(b / (1 + a)), [F(1), F(0)]) == [a, b],
               "R(b/(1+a)) must reach the direction (a,b)")
    ck(_eq(_mm(_rt(F(1)), _rt(F(1))), _scal(F(-1), _eye(2))),
       "the half-turn is reached as R(1)^2")

    # The connected-Lie-subgroup dimension dichotomy is a NAMED standard-
    # mathematics import, recorded (not derived) here: a connected Lie
    # subgroup of the one-dimensional group SO(2) has dimension zero (trivial)
    # or one (open, hence all of connected SO(2)).  What this check COMPUTES
    # is the exact instance surface around that import: the disconnected C_n
    # controls, the infinite-order witness, and the parametrization battery.
    dimensions = (0, 1)
    branch = {
        0: "trivial",
        1: "SO(2)",
    }
    ck(set(branch) == set(dimensions), "Lie dimension branches must be exhaustive")
    ck(branch[0] == "trivial", "connected zero-dimensional branch is trivial")
    ck(branch[1] == "SO(2)", "one-dimensional branch is open and full")
    nontrivial_connected_result = branch[1]
    ck(nontrivial_connected_result == "SO(2)",
       "nontrivial connected subgroup must be the full circle")

    c2 = _cyclic_subgroup(2)
    ck(c2 == frozenset((F(0), F(1, 2))), "{I,-I} is the C2 control")

    return _result(
        "T_held_connected_subgroup_so2",
        "P_math",
        ("The connected-Lie-subgroup dimension dichotomy for SO(2) (dim 0 "
         "trivial; dim 1 open, hence the full circle) is consumed as a NAMED "
         "standard-mathematics import, not derived here.  What is computed "
         "exactly: the C_n disconnected controls including {I,-I}; an "
         "infinite-order rational rotation (cos=3/5) with a Gaussian-integer "
         "non-associate-primes certificate, showing the finite controls do "
         "not exhaust the subgroup lattice; and the rational tangent "
         "half-angle parametrization battery (SO(2) membership, the exact "
         "composition law, and Pythagorean-direction coverage with the "
         "half-turn as R(1)^2) as the executable shadow of the "
         "one-dimensional branch filling the circle."),
        ["T_held_relative_loop_group", "T_held_recombination_nontriviality"],
        {
            "classification": {"dim_0": "trivial", "dim_1": "SO(2)"},
            "classification_execution_status":
                "dimension dichotomy imported by name; controls, "
                "infinite-order witness, and parametrization battery computed",
            "finite_disconnected_controls": finite_controls,
            "infinite_order_witness": {
                "rotation": "cos=3/5, sin=4/5",
                "certificate": "3+4i=(2+i)^2; 5=(2+i)(2-i); 2+i, 2-i "
                               "non-associate Gaussian primes",
                "distinct_powers_computed": 24,
            },
            "parametrization_battery": {
                "grid_size": len(grid),
                "compositions_checked": composition_checked,
                "pythagorean_directions": len(pythagorean_directions),
                "half_turn": "R(1)^2",
            },
            "nontrivial_connected_result": nontrivial_connected_result,
            "standard_math_imports": [
                "connected 0-dimensional Lie group is trivial",
                "same-dimensional Lie subgroup is open",
                "connected topological group has no proper open subgroup",
            ],
        },
        fails,
        premises=(
            "effective_image_is_a_Lie_subgroup_of_SO2",
            "connectedness_of_the_effective_image",
            "nontriviality_of_the_effective_image",
        ),
        negative_controls=(
            "C2={I,-I}",
            "finite cyclic C3, C4, C6",
        ),
        cross_refs=(
            "Paper 5 Mathematical Note v1.7: every nontrivial path-connected subgroup of SO(2) is SO(2)",
        ),
    )


# ---------------------------------------------------------------------------
# H4: exact isometry from the represented ledger adjoint
# ---------------------------------------------------------------------------


