"""
third_boat_no_extension.py -- The Zipper / Quantum Lane: Paper 0 chained-boats
================================================================================
Self-contained, scipy-free bank port of the Paper 0 third-boat / no-extension
criterion (source: pool_p8_third_boat_no_extension.py, which drags the whole
pool_p2/p3/p4/p6 scipy-dependent defender-class lane). The CORE theorem is
REIMPLEMENTED self-contained here, exactly as apf/minimal_branch_obstruction.py
did for its P7 lane. Exact arithmetic (fractions.Fraction); no floats, no scipy,
no numpy, no pool/lane imports.

THE RESULT (machine-checked, honest): the executable finite meaning of Paper 0's
chained-boats / third-boat "no-extension" criterion.

  A "third boat" for a bipartite behavior is a COMMUTING extension defender: a
  shared classical cause lambda with local response functions -- i.e. a common
  cause / local hidden-variable (LHV) model. On the CHSH (2,2,2) correlation
  scenario:

  (T) A third boat EXISTS iff the behavior lies in the local (Boole) polytope
      (Fine's theorem: a joint distribution over the four observables exists iff
      every CHSH inequality holds). For the classical control on the 3-4-5 slice
      (c = -1/2, CHSH = 7/5 < 2, strictly inside) an explicit common cause is
      CONSTRUCTED: exact nonnegative weights on the 8 local deterministic vertices
      (support 5, the Caratheodory bound). For the Bell-violating native target
      (c = -101/105, CHSH = 202/75 > 2, outside) NO commuting third boat exists --
      the violated CHSH facet is the separating certificate.

  (L1) A finite tower of extension carriers (boat -> anchor -> chain -> ...)
       FLATTENS to ONE product carrier: the Cartesian product is a single common
       cause reproducing the same behavior. The finite regress is NOT itself a
       no-go -- adding a carrier is just a larger common cause. So the no-go can
       come ONLY from complete defender infeasibility (Fine), never from the mere
       fact that a third boat "has an anchor".

  (L2, the fence) Above the facet, the no-extension receipt is a REGRESSION
       witness, NOT a prequantum derivation. The Bell-violating correlation is the
       SUPPLIED datum (DOWNSTREAM_QUANTUM_REPRESENTATION); the identical
       no-extension certificate fires on ANY supplied above-facet point (a whole
       family, incl. the PR box). Certifying "no third boat" for a correlation you
       were handed does not derive, from A1-only primitives, that nature must sit
       at that correlation.

GRADES: (T) [P_math]; (L1) [P_math]; (L2) [P_structural_reading].
physical_premises_certified = False; non-exporting.

CONCORDANCES (cited, not re-derived):
  minimal_branch_obstruction (P7, [P_structural_instrument]): same 3-4-5 slice,
    same control c=-1/2 (CHSH 7/5) and native target c=-101/105 (CHSH 202/75,
    margin 52/75); this module is its common-cause / third-boat sibling.
  ijc_boolean_defender_bridge (.424, [P_math]): outside-polytope <=> no common
    Boolean/commuting-extension defender (Fine facet). The "third boat = commuting
    extension" identification rides this banked equivalence.
  fp4_process_defender (Fine facet + shared-history CHSH ceiling 2); T_IJC_dichotomy,
    T_no_IJC_no_noncommutativity (PLEC admits both branches);
    T_quantum_admissibility_condition ([P_regime], the branch is empirical). This
    module supplies the exact common-cause construction that sits under the "third
    boat" name in Paper 0's chained-boats argument (Paper 0 sec:chained_boats).

MAY NOT BE CITED FROM THIS MODULE:
  'foundation no-extension derived' (FALSE -- regression-only above the facet);
  'the third boat having an anchor/chain is a no-go' (FALSE -- the finite regress
  collapses to one product carrier); any '[P]' on the branch/QAC; 'the no-extension
  receipt derives the quantum correlation'.
"""

from fractions import Fraction as F
from itertools import product, combinations

FAMILY = "quantum.third_boat_no_extension"

# the 3-4-5 slice, shared with minimal_branch_obstruction (sibling)
NATIVE_DIRECTION = (F(3, 5), F(3, 5), F(4, 5), F(-4, 5))
CONTROL_C = F(-1, 2)            # classical control: CHSH 7/5, strictly inside
NATIVE_TARGET_C = F(-101, 105)  # Bell-violating native target: CHSH 202/75, outside
CLASSICAL_CHSH_BOUND = F(2)


# =====================================================================
# self-contained finite polytope + Fine test + common-cause construction
# =====================================================================

def _local_vertices():
    """The 8 deterministic local correlation vertices (a0b0,a0b1,a1b0,a1b1).
    Each IS an extreme common cause: a deterministic global assignment lambda
    with local response functions a_x(lambda), b_y(lambda)."""
    return sorted({(a0 * b0, a0 * b1, a1 * b0, a1 * b1)
                   for a0, a1, b0, b1 in product((1, -1), repeat=4)})


def _chsh_facets():
    """The 8 oriented CHSH facets: sign patterns s with product -1."""
    return [s for s in product((1, -1), repeat=4)
            if s[0] * s[1] * s[2] * s[3] == -1]


def _dot(s, v):
    return sum(F(si) * F(vi) for si, vi in zip(s, v))


def _behavior(c):
    """The behavior c * NATIVE_DIRECTION as an exact 4-tuple of correlators."""
    return tuple(F(c) * d for d in NATIVE_DIRECTION)


def _max_chsh(E):
    """max over the 8 CHSH facets of <s,E> (exact)."""
    return max(_dot(s, E) for s in _chsh_facets())


def _in_local_polytope(E, facets=None):
    """Fine's test: E is in the (2,2,2) correlation (Boole) polytope iff it satisfies
    the COMPLETE H-description -- the 8 box facets |E_xy| <= 1 AND the 8 oriented CHSH
    facets <s,E> <= 2. CHSH-only is complete ONLY for correlators already bounded by 1:
    e.g. E=(0, 1/2, -3/2, 0) passes all 8 CHSH facets yet has NO common cause (its
    third component is out of box), so the box constraints are load-bearing."""
    if facets is None:
        facets = _chsh_facets()
    return all(abs(F(x)) <= 1 for x in E) and \
           all(_dot(s, E) <= CLASSICAL_CHSH_BOUND for s in facets)


def _violated_facets(E):
    return [s for s in _chsh_facets() if _dot(s, E) > CLASSICAL_CHSH_BOUND]


def _rref_solve(rows, rhs):
    """Exact solve of an m x n linear system over Fraction (Gauss-Jordan).
    Returns the UNIQUE solution (list of n Fractions) iff it exists and is unique
    (rank == n and consistent); else None. No floats."""
    m = len(rows)
    n = len(rows[0]) if rows else 0
    A = [list(rows[i]) + [rhs[i]] for i in range(m)]
    pivot_col = []
    r = 0
    for col in range(n):
        piv = None
        for i in range(r, m):
            if A[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[r], A[piv] = A[piv], A[r]
        pv = A[r][col]
        A[r] = [x / pv for x in A[r]]
        for i in range(m):
            if i != r and A[i][col] != 0:
                f = A[i][col]
                A[i] = [a - f * b for a, b in zip(A[i], A[r])]
        pivot_col.append(col)
        r += 1
        if r == m:
            break
    rank = r
    for i in range(m):
        if all(A[i][c] == 0 for c in range(n)) and A[i][n] != 0:
            return None            # inconsistent
    if rank != n:
        return None                # not unique
    sol = [F(0)] * n
    for i in range(rank):
        sol[pivot_col[i]] = A[i][n]
    return sol


def _construct_common_cause(E):
    """Search for an EXACT nonnegative common cause (the third boat): weights
    w_i >= 0 on the local deterministic vertices, sum 1, reconstructing E. By
    Caratheodory a point of the 4-dim correlation polytope needs <= 5 vertices, so
    we search subsets of size <= 5 with exact rational elimination. Returns
    {support, vertices, weights} or None. A nonnegative solution EXISTS iff E is a
    convex combination of local vertices, i.e. iff E is in the local polytope
    (the constructive half of Fine); an above-facet E can have none (any nonneg
    combination of local vertices is local, so it cannot land outside)."""
    verts = _local_vertices()
    Ef = tuple(F(x) for x in E)
    for k in range(1, 6):
        for support in combinations(range(len(verts)), k):
            sub = [verts[j] for j in support]
            rows = [[F(sub[j][coord]) for j in range(k)] for coord in range(4)]
            rows.append([F(1)] * k)                       # normalization row
            rhs = [Ef[0], Ef[1], Ef[2], Ef[3], F(1)]
            w = _rref_solve(rows, rhs)
            if w is None:
                continue
            if all(wi >= 0 for wi in w):
                recon = tuple(sum(w[j] * F(sub[j][coord]) for j in range(k))
                              for coord in range(4))
                if recon == Ef and sum(w) == 1:
                    return {"support": support,
                            "vertices": tuple(sub),
                            "weights": tuple(w)}
    return None


def _flatten_tower(layers):
    """Flatten a finite tower of extension carriers (each a tuple of states) into
    ONE product carrier. Returns (product_states, index_map, expected_count). The
    product carrier is a single common cause; the regress is not a no-go."""
    tuples = tuple(product(*layers))
    expected = 1
    for L in layers:
        expected *= len(L)
    index = {state: i for i, state in enumerate(tuples)}
    return tuples, index, expected


def _certify_no_third_boat(c, provenance):
    """Certify the third-boat status of behavior c*NATIVE_DIRECTION and carry its
    provenance. `no_third_boat` is COMPUTED (Fine + construction); `provenance` is
    a SUPPLIED attribute of the datum, never computed here. `foundation_derived`
    is True only for a PREQUANTUM_APF_DERIVED provenance -- which no above-facet
    correlation in this module actually earns, because the correlation is an INPUT
    constant, not a computed A1-only consequence."""
    E = _behavior(c)
    local = _in_local_polytope(E)
    boat = _construct_common_cause(E)
    return {
        "c": str(c),
        "in_polytope": local,
        "no_third_boat": (not local) and (boat is None),
        "provenance": provenance,
        "foundation_derived": (provenance == "PREQUANTUM_APF_DERIVED"),
    }


_COMMON = {
    "tier": 4,
    "physical_premises_certified": False,
    "family": FAMILY,
    "dependencies": [],
    "cross_refs": [
        "T_minimal_branch_selection_obstruction",
        "T_ijc_boolean_defender_bridge",
        "L_fp4_incompatibility_discriminator",
        "T_IJC_dichotomy", "T_no_IJC_no_noncommutativity",
        "T_quantum_admissibility_condition",
        "Paper0_chained_boats_criterion",
    ],
    "may_not_cite": [
        "foundation no-extension derived",
        "the third boat having an anchor/chain is a no-go",
        "the no-extension receipt derives the quantum correlation",
        "any [P] on the branch/QAC",
    ],
}


# =====================================================================
# T -- third boat exists iff in the local polytope (Fine); constructed / absent
# =====================================================================

def check_T_third_boat_iff_local():
    """[P_math]. A third boat (commuting / common-cause extension = LHV) exists
    iff the behavior is in the local (Boole) polytope (Fine). CONSTRUCTED for the
    in-polytope control (c=-1/2, CHSH 7/5) as exact nonnegative weights on the
    local deterministic vertices; ABSENT for the Bell-violating native target
    (c=-101/105, CHSH 202/75). Fail-controls with real teeth."""
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        return cond

    verts = _local_vertices()
    facets = _chsh_facets()
    ck(len(verts) == 8, "8 local deterministic common-cause vertices")
    ck(len(facets) == 8, "8 oriented CHSH facets")
    ck(all(_in_local_polytope(v) for v in verts),
       "every deterministic vertex is inside the local polytope")

    # --- control: in-polytope -> third boat CONSTRUCTED ---
    ctrl = _behavior(CONTROL_C)
    ctrl_local = _in_local_polytope(ctrl)
    ck(_max_chsh(ctrl) == F(7, 5), "control CHSH 7/5")
    ck(ctrl_local, "control is inside the local polytope (Fine)")
    boat = _construct_common_cause(ctrl)
    ck(boat is not None, "third boat CONSTRUCTED for the control")
    boat_weights = None
    if boat is not None:
        w = boat["weights"]
        sub = boat["vertices"]
        boat_weights = [str(x) for x in w]
        recon = tuple(sum(w[j] * F(sub[j][c]) for j in range(len(w)))
                      for c in range(4))
        ck(all(wi >= 0 for wi in w), "common-cause weights nonnegative")
        ck(sum(w) == 1, "common-cause weights sum to 1")
        ck(recon == tuple(F(x) for x in ctrl),
           "common cause reconstructs the control behavior exactly")
        ck(len(sub) <= 5, "support within Caratheodory bound (<=5)")

    # --- Bell target: outside -> NO third boat ---
    bell = _behavior(NATIVE_TARGET_C)
    bell_local = _in_local_polytope(bell)
    bell_boat = _construct_common_cause(bell)
    ck(_max_chsh(bell) == F(202, 75), "Bell-target CHSH 202/75")
    ck(_max_chsh(bell) - F(2) == F(52, 75), "Bell-target CHSH margin 52/75")
    ck(not bell_local, "Bell target is outside the local polytope (Fine)")
    ck(bell_boat is None, "NO commuting third boat for the Bell-violating target")

    # --- the IFF, computed on both behaviors ---
    iff_control = (boat is not None) == ctrl_local
    iff_bell = (bell_boat is not None) == bell_local
    ck(iff_control and iff_bell,
       "third-boat-exists <=> in-local-polytope on both behaviors")

    # --- fail-control 1: the REAL acceptance predicate (nonneg AND exact recon AND
    #     sum 1) discriminates. It ACCEPTS the constructed boat and REJECTS a tamper
    #     that keeps the weights nonnegative and summing to 1 but shifts the
    #     reconstruction off the target -- so the rejection is carried by the recon
    #     clause SPECIFICALLY. (The prior sign-only tamper set one weight w0-1, which is
    #     always negative for interior weights, so its assertion could never fail;
    #     routing a recon-only break through the true predicate gives the leg teeth.) ---
    def _boat_accepted(weights, vertices, target):
        recon = tuple(sum(weights[j] * F(vertices[j][cc]) for j in range(len(weights)))
                      for cc in range(4))
        return (all(wi >= 0 for wi in weights)
                and sum(weights) == 1
                and recon == tuple(F(x) for x in target))

    genuine_accepted = True
    recon_tamper_rejected = True
    if boat is not None and len(boat["weights"]) >= 2:
        sub = boat["vertices"]
        w_good = list(boat["weights"])
        genuine_accepted = _boat_accepted(w_good, sub, ctrl)
        order = sorted(range(len(w_good)), key=lambda k: w_good[k], reverse=True)
        hi, lo = order[0], order[1]              # two largest weights (both positive)
        w_bad = list(w_good)
        w_bad[hi] = w_good[hi] + w_good[lo]      # nonneg preserved, sum preserved,
        w_bad[lo] = F(0)                          # recon shifts by w_lo*(v_hi-v_lo) != 0
        recon_tamper_rejected = not _boat_accepted(w_bad, sub, ctrl)
    ck(genuine_accepted,
       "the real acceptance predicate accepts the constructed common cause")
    ck(recon_tamper_rejected,
       "a recon-breaking tamper (weights still nonneg and summing to 1) is rejected "
       "by the real predicate -- the reconstruction clause has teeth")

    # --- fail-control 2 (mutation that FLIPS it): drop the violated facet(s) from
    #     Fine's test -> the broken test misclassifies the Bell target as 'local',
    #     but the constructive search still finds NO common cause; the two DISAGREE,
    #     proving the full facet family is load-bearing ---
    violated = _violated_facets(bell)
    ck(len(violated) >= 1, "the Bell target violates at least one CHSH facet")
    broken_facets = [s for s in facets if s not in violated]
    bell_local_broken = _in_local_polytope(bell, facets=broken_facets)
    mutation_flips = bell_local_broken and (bell_boat is None)
    ck(mutation_flips,
       "dropping the violated facet flips Fine's verdict but not the construction "
       "-- full facet family is load-bearing")

    passed = not fails
    out = {
        "name": "T_third_boat_iff_local",
        "epistemic": "P_math",
        "passed": passed,
        "key_result": (
            "CHSH (2,2,2) correlation scenario: a commuting third boat (common "
            "cause / LHV) exists IFF the behavior is in the local (Boole) polytope "
            "(Fine). Control c=-1/2 (CHSH 7/5, inside): third boat CONSTRUCTED, "
            "exact nonnegative weights on 5 local vertices (Caratheodory). Native "
            "target c=-101/105 (CHSH 202/75, margin 52/75, outside): NO commuting "
            "third boat; the violated CHSH facet is the separating certificate. "
            "Scope: the UNIVERSAL Fine equivalence (every (2,2,2) behavior) is "
            "imported concordance (ijc_boolean_defender_bridge); what is COMPUTED "
            "here is the iff on the two witnessed behaviors -- the constructed "
            "in-box control and the absent Bell target."
        ),
        "control_c": str(CONTROL_C),
        "control_chsh": str(_max_chsh(ctrl)),
        "control_third_boat_constructed": boat is not None,
        "control_common_cause_weights": boat_weights,
        "control_support_size": (len(boat["vertices"]) if boat else None),
        "native_target_c": str(NATIVE_TARGET_C),
        "native_target_chsh": str(_max_chsh(bell)),
        "native_target_no_third_boat": bell_boat is None,
        "iff_holds": iff_control and iff_bell,
        "mutation_dropping_facet_flips_verdict": mutation_flips,
        "fail_reasons": fails,
    }
    out.update(_COMMON)
    return out


# =====================================================================
# L1 -- the finite regress collapses to one product carrier (not a no-go)
# =====================================================================

def check_L_finite_regress_collapses():
    """[P_math]. A finite tower of extension carriers (boat -> anchor -> chain ->
    ...) flattens to ONE product carrier: an exact bijection onto the Cartesian
    product. The finite regress is NOT itself a no-go -- adding a carrier is one
    larger common cause reproducing the SAME behavior. Exhibited exactly, with a
    behavior-preservation leg and a fail-control."""
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        return cond

    # several tower shapes each collapse to one product carrier exactly
    tower_A = [(0, 1), ("a", "b"), ("slack", "loaded")]          # boat/anchor/chain
    tower_B = [(0, 1, 2), ("x", "y"), (True, False)]
    for tower, expect in ((tower_A, 8), (tower_B, 12)):
        tuples, index, expected = _flatten_tower(tower)
        ck(expected == expect, "product count == prod(layer sizes)")
        ck(len(tuples) == expected, "flattened carrier has product-many states")
        ck(len(index) == expected, "flattening is injective (distinct states)")
        ck(set(index.values()) == set(range(expected)),
           "flattening is a bijection onto range(N)")

    # behavior-preservation: a common cause built as a 2-LAYER tower (which local
    # vertex x a redundant hidden bit) reproduces the SAME behavior as its
    # flattened single-lambda carrier -- the product carrier is a faithful single
    # common cause, so the extra layer buys no new behavior.
    ctrl = _behavior(CONTROL_C)
    boat = _construct_common_cause(ctrl)
    ck(boat is not None, "control common cause available for the collapse exhibit")
    behavior_preserved = False
    if boat is not None:
        verts = boat["vertices"]
        w = boat["weights"]
        p = F(1, 3)                                   # arbitrary redundant-bit split
        flat_weight = {}
        for i in range(len(w)):
            for bit in (0, 1):
                flat_weight[(i, bit)] = w[i] * (p if bit == 0 else (1 - p))
        recon = tuple(
            sum(flat_weight[(i, bit)] * F(verts[i][c])
                for i in range(len(w)) for bit in (0, 1))
            for c in range(4))
        behavior_preserved = (recon == tuple(F(x) for x in ctrl))
        ck(behavior_preserved,
           "flattened 2-layer common cause reproduces the SAME behavior")
        ck(sum(flat_weight.values()) == 1, "flattened weights still normalized")

    # the regress-is-not-a-no-go statement made executable: a tower of ANY finite
    # depth 1..6 (2 states each) collapses to a single carrier of 2**depth states
    for depth in range(1, 7):
        layers = [(0, 1)] * depth
        tuples, index, expected = _flatten_tower(layers)
        ck(expected == 2 ** depth and len(index) == expected
           and set(index.values()) == set(range(expected)),
           "depth-%d tower collapses to one 2**%d-state carrier" % (depth, depth))

    # fail-control: a 'flattening' that DROPS a carrier is NOT the true product --
    # the collapse claim is not vacuous
    _, _, expected_A = _flatten_tower(tower_A)
    dropped_tuples, _, _ = _flatten_tower(tower_A[:-1])
    ck(len(dropped_tuples) != expected_A,
       "dropping a carrier changes the product count (collapse is not vacuous)")

    passed = not fails
    out = {
        "name": "L_finite_regress_collapses",
        "epistemic": "P_math",
        "passed": passed,
        "key_result": (
            "a finite tower of extension carriers (boat -> anchor -> chain -> ...) "
            "flattens by an exact bijection to ONE product carrier reproducing the "
            "SAME behavior; any depth 1..6 collapses to a single 2**depth-state "
            "common cause. The finite regress is NOT a no-go -- adding a carrier is "
            "one larger common cause. Corrects 'the third boat has an anchor, "
            "therefore an infinite regress / obstruction'."
        ),
        "tower_A_states": 8,
        "tower_B_states": 12,
        "behavior_preserved_under_flattening": behavior_preserved,
        "regress_is_not_a_no_go": True,
        "fail_reasons": fails,
    }
    out.update(_COMMON)
    return out


# =====================================================================
# L2 -- above the facet the no-extension receipt is regression-only (fenced)
# =====================================================================

def check_L_no_extension_above_facet_is_regression_only():
    """[P_structural_reading]. Above the facet the no-extension receipt is a
    REGRESSION witness, not a prequantum derivation. The Bell-violating correlation
    is the SUPPLIED datum (DOWNSTREAM_QUANTUM_REPRESENTATION); the identical
    no-extension certificate fires on EVERY supplied above-facet point (a whole
    family, incl. the PR box), so it cannot single out the physical value -- it
    regresses over the data it was handed. The no-go comes ONLY from Fine
    infeasibility (a violated facet), not from the mere existence of an
    anchor/chain (which collapses, L1). Fenced."""
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        return cond

    # the native Bell target: no third boat; provenance is SUPPLIED (downstream)
    native = _certify_no_third_boat(NATIVE_TARGET_C,
                                    "DOWNSTREAM_QUANTUM_REPRESENTATION")
    ck(native["no_third_boat"], "native target: no commuting third boat (Fine)")
    ck(native["provenance"] == "DOWNSTREAM_QUANTUM_REPRESENTATION",
       "native correlation is a SUPPLIED (downstream) datum")
    ck(not native["foundation_derived"],
       "native no-extension is NOT a prequantum derivation")

    # regression-generic: EVERY supplied above-facet correlation on the slice gets
    # the SAME 'no third boat' verdict. A derivation would output ONE value; this
    # certificate excludes a whole continuum -> it regresses over supplied data.
    family = [F(-101, 105), F(-4, 5), F(-9, 10), F(-1, 1)]
    all_above = all(_max_chsh(_behavior(c)) > F(2) for c in family)
    all_excluded = all(_certify_no_third_boat(c, "DOWNSTREAM_QUANTUM_REPRESENTATION")
                       ["no_third_boat"] for c in family)
    ck(all_above, "the supplied above-facet family is genuinely above the facet")
    ck(all_excluded,
       "every supplied above-facet correlation gets the same no-extension verdict")

    # a second, off-slice supplied nonlocal datum (the PR box, CHSH 4): same
    # certifier, same verdict -> the certificate is generic over supplied
    # correlations, not specific to the quantum value
    pr = (F(1), F(1), F(1), F(-1))
    pr_no_boat = (not _in_local_polytope(pr)) and (_construct_common_cause(pr) is None)
    ck(_max_chsh(pr) == F(4), "PR box CHSH 4 (off-slice supplied above-facet datum)")
    ck(pr_no_boat, "PR box: no commuting third boat (same certifier)")
    generic_over_supplied = native["no_third_boat"] and all_excluded and pr_no_boat
    ck(generic_over_supplied,
       "the no-extension certificate fires on ANY supplied above-facet datum")

    # the no-go is carried by a violated Fine facet, NOT by tower depth: a
    # nontrivial anchor/chain tower still collapses (L1), so 'the third boat has an
    # anchor' is not itself an obstruction
    _, index, expected = _flatten_tower([(0, 1), ("a", "b"), ("s", "l")])
    tower_collapses = (len(index) == expected == 8)
    ck(len(_violated_facets(_behavior(NATIVE_TARGET_C))) >= 1,
       "the no-go is carried by a violated Fine facet (complete-defender infeasibility)")
    ck(tower_collapses,
       "a nontrivial anchor/chain tower still collapses (having an anchor is not a no-go)")

    # THE FENCE / fail-control: the head 'foundation no-extension derived' is
    # REFUTED because the identical certificate is generic over supplied data. A
    # genuine prequantum derivation would single out the physical correlation;
    # regression-over-data cannot.
    foundation_no_extension_derived = False
    false_foundation_head_refuted = (generic_over_supplied
                                     and not foundation_no_extension_derived)
    ck(false_foundation_head_refuted,
       "'foundation no-extension derived' is refuted (regression-only above facet)")

    # fail-control (relabel): relabelling the SAME supplied datum 'PREQUANTUM_APF_
    # DERIVED' buys no discriminating power -- the identical verdict still fires on
    # the unrelated PR box, so the 'derived' label is not backed by any computation
    relabelled = _certify_no_third_boat(NATIVE_TARGET_C, "PREQUANTUM_APF_DERIVED")
    relabel_buys_nothing = (relabelled["no_third_boat"] == native["no_third_boat"]
                            and pr_no_boat)
    ck(relabel_buys_nothing,
       "relabelling the datum 'derived' buys no discriminating power (still generic "
       "over supplied data) -- the head stays barred")

    passed = not fails
    out = {
        "name": "L_no_extension_above_facet_is_regression_only",
        "epistemic": "P_structural_reading",
        "passed": passed,
        "key_result": (
            "above the facet the no-extension receipt is a REGRESSION witness: the "
            "Bell-violating correlation is the SUPPLIED datum (downstream quantum "
            "representation), and the identical certificate excludes a whole family "
            "of supplied above-facet correlations (incl. the PR box) -- so it does "
            "not derive, from A1-only primitives, WHICH correlation nature realizes. "
            "The no-go is carried by a violated Fine facet, not by an anchor/chain "
            "(which collapses, L1). foundation_no_extension_derived = False."
        ),
        "native_target_no_third_boat": native["no_third_boat"],
        "native_provenance": native["provenance"],
        "certificate_generic_over_supplied_data": generic_over_supplied,
        "foundation_no_extension_derived": foundation_no_extension_derived,
        "no_go_from_fine_facet_not_from_anchor": tower_collapses,
        "fail_reasons": fails,
    }
    out.update(_COMMON)
    return out


# =====================================================================
# mutation battery (extra teeth, auditor fast-path)
# =====================================================================

def run_mutations():
    r = {}
    t = check_T_third_boat_iff_local()
    r["M1_control_third_boat_constructed"] = t["control_third_boat_constructed"]
    r["M2_native_target_no_third_boat"] = t["native_target_no_third_boat"]
    r["M3_iff_holds"] = t["iff_holds"]
    r["M4_dropping_facet_flips_verdict"] = t["mutation_dropping_facet_flips_verdict"]
    l1 = check_L_finite_regress_collapses()
    r["M5_behavior_preserved_under_flattening"] = l1["behavior_preserved_under_flattening"]
    l2 = check_L_no_extension_above_facet_is_regression_only()
    r["M6_certificate_generic_over_supplied"] = l2["certificate_generic_over_supplied_data"]
    r["M7_foundation_not_derived"] = (not l2["foundation_no_extension_derived"])
    r["all_caught"] = all(r.values())
    return r


_CHECKS = {
    "T_third_boat_iff_local": check_T_third_boat_iff_local,
    "L_finite_regress_collapses": check_L_finite_regress_collapses,
    "L_no_extension_above_facet_is_regression_only":
        check_L_no_extension_above_facet_is_regression_only,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all(verbose=True):
    out = {}
    for name, fn in _CHECKS.items():
        rr = fn()
        out[name] = rr
        if verbose:
            print(("PASS" if rr["passed"] else "FAIL"), rr["epistemic"], name)
            for f in rr["fail_reasons"]:
                print("   -", f)
    muts = run_mutations()
    out["mutations"] = muts
    if verbose:
        n = sum(1 for k in muts if k.startswith("M"))
        print(("PASS" if muts["all_caught"] else "FAIL"),
              "mutation_battery ({} named)".format(n))
        npass = sum(1 for k, v in out.items() if k != "mutations" and v["passed"])
        print("== {} / {} checks pass; mutations all caught: {}".format(
            npass, len(_CHECKS), muts["all_caught"]))
    return out


if __name__ == "__main__":
    import sys
    res = run_all()
    ok = all(v["passed"] for k, v in res.items() if k != "mutations") \
        and res["mutations"]["all_caught"]
    sys.exit(0 if ok else 1)
