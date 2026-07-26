"""
rent_exclusion_gate.py -- The Rent-Exclusion Gate on the Hidden Order
================================================================================
RESEARCH-LANE BANK CANDIDATE. NOT wired into the bank (no verify_all edit, no
_module_manifest bump, non-exporting, physical_premises_certified = False).
Self-contained: fractions.Fraction + itertools + stdlib ONLY. No scipy, no numpy,
no multiprocessing/pool, no apf imports. The CHSH (2,2,2) local polytope is
re-implemented inline (clean-room; it mirrors the banked sibling
third_boat_no_extension.py on the same 3-4-5 slice, but imports nothing).

--------------------------------------------------------------------------------
THE QUESTION IT SETTLES
--------------------------------------------------------------------------------
In the APF cost ledger a cost is one of exactly two BOOKABLE kinds:

  (a) a formation / realignment COMMITMENT, booked ONCE at a transition and
      standing thereafter as committed capacity -- a DEPOSIT, read freely each
      time afterwards (cross-ref T_realignment_cost_is_transition_energy);
  (b) a PER-ACTIVATION charge, booked when and only when an interface activates
      on held content.

EXCLUDED from the ledger: standing-rent -- a cost of merely persisting
(cross-ref T_ledger_rent_excluded). The rent-exclusion gate asks of any proposed
cost: is it a one-time deposit (a) or a per-activation charge (b) -- or is it
mere persistence (excluded)?

Apply the gate to the HIDDEN ORDER: the extra structure a classical / reductive
account must carry to reproduce a Bell-violating quantum correlation. If that
order is a kind-(a) amortizable DEPOSIT, it is ~free over many pairs
(rent-adjacent) and the "the reductive account pays an occupant cost" prize dies.
If it is a kind-(b) PER-ACTIVATION charge, the prize survives the gate.

VERDICT (machine-checked): the hidden order is a kind-(b) PER-ACTIVATION charge.
A deposit is exactly shared randomness = a local hidden variable; by Fine it can
reach only the local (Boole) polytope, and its reachable set does NOT grow with
the pair-count N -- so it can never be amortized into the above-facet correlation.
Reproducing the above-facet correlation requires per-pair DIRECTED structure,
which is booked each activation. The order therefore PASSES the rent-exclusion
gate as a chargeable per-activation cost.

--------------------------------------------------------------------------------
THE THREE CHECKS
--------------------------------------------------------------------------------
  L_deposit_is_local_hidden_variable        [P_structural] (with a [P_math] core)
      A kind-(a) deposit (one-time shared lambda, read identically each pair, no
      per-pair directed input) IS shared randomness = a common cause / LHV. By
      Fine (cross-ref check_T_third_boat_iff_local) the deposit-reachable set is
      EXACTLY the local polytope. [P_math] core: every deposit behavior (convex
      combination of the 8 deterministic vertices) satisfies all 8 CHSH facets
      (<=2) by linearity; the native above-facet target (CHSH 202/75 > 2, margin
      52/75) violates a facet, so a deposit-only account provably cannot reach it.

  T_order_is_per_activation_not_standing_rent           [P_structural]
      Therefore reproducing the above-facet correlation needs per-pair directed
      structure (communication) -- shared randomness is provably insufficient
      (Bell/Fine restated). Per-pair directed structure is booked EACH activation
      -> kind-(b) per-activation charge; it is NOT excluded standing-rent (mere
      persistence) and NOT a kind-(a) deposit (the deposit is the LHV that fails
      by L1). NON-AMORTIZATION made executable: a bounded one-time deposit of k
      classical states, applied identically per pair, reaches ONLY the polytope
      for ALL N (its reachable set is N-independent). Only per-pair directed
      input escapes -- THAT is the per-activation part.

  T_relative_charge_no_absolute_baseline                [P_structural_reading]
      The charge is a RELATIVE per-pair difference: the reductive account carries
      a directed per-pair term the irreducible (orthodox) account does not. A2
      (least-cost selection) is comparative, so only the SIGN of the difference
      matters -- no absolute cost baseline is needed. This SIDESTEPS the reduced
      cost-shape / directionality posit (which required an absolute "unenforced
      baseline"). Represented as (common commit term) + (directed term: >0 for
      reductive, 0 for irreducible); the difference is the directed term, strictly
      positive above the facet and baseline-independent.

--------------------------------------------------------------------------------
CRITICAL FENCES  (may_not_cite on all three checks)
--------------------------------------------------------------------------------
  * This does NOT derive the QAC. Banked wall (Paper 20 Supplement D2 /
    v24.3.397): "cost surplus as a quantum criterion is REFUTED -- superadditivity
    is NECESSARY-not-sufficient for the QAC." This module is ONTOLOGY-SELECTION
    GIVEN a quantum-capable interface (which ontic account of the SAME supplied
    correlation is cheaper), NOT a criterion that makes an interface quantum. Do
    NOT cite "cost surplus => quantum".
  * It does NOT prove APF assigns the per-activation charge a POSITIVE cost --
    that is enforcement-realism, a SEPARATE open step (does APF charge the
    realization of the directed influence regardless of the mechanism's
    self-description?). This module shows the order is per-activation
    (chargeABLE), NOT that it is charged.
  * It does NOT lift the QAC (still needs enforcement-realism; G-hold-exact is now constitutively free under A2-exact, Ethan's ruling 2026-07-26).
    "capacity shortage => quantum" and "the branch/QAC is derived" stay BARRED.
  * "deposit = shared-randomness = LHV" is a MODELING READING of rent-exclusion
    kind-(a); only the polytope-membership is the [P_math] part.

GRADES: L1 [P_structural] ([P_math] core); T2 [P_structural]; T3
[P_structural_reading]. physical_premises_certified = False. Non-exporting.

CONCORDANCES (cited, not re-derived):
  third_boat_no_extension.check_T_third_boat_iff_local ([P_math]): third boat
    (commuting extension = LHV = common cause) exists iff in the local polytope
    (Fine). The "deposit = common cause" identification rides this equivalence.
  ijc_boolean_defender_bridge (.424, [P_math]): outside-polytope <=> no commuting
    Boolean defender (a violated Fine facet).
  minimal_branch_obstruction (P7): same 3-4-5 slice, |c| = 5/7 the local boundary
    (CHSH 2); native |c| = 101/105 (CHSH 202/75) outside, margin 52/75.
  T_ledger_rent_excluded ([P]): standing-rent is excluded from the ledger.
  T_realignment_cost_is_transition_energy ([P]): a kind-(a) commitment books once
    at the transition.
  T_IJC_dichotomy, T_quantum_admissibility_condition ([P_regime]): the branch /
    QAC stays empirical; this module does not touch it.
"""

from fractions import Fraction as F
from itertools import product, combinations, combinations_with_replacement

FAMILY = "quantum.rent_exclusion_gate"

# the 3-4-5 slice, shared with the banked sibling third_boat_no_extension.py
NATIVE_DIRECTION = (F(3, 5), F(3, 5), F(4, 5), F(-4, 5))
CONTROL_C = F(-1, 2)             # classical control: CHSH 7/5, strictly inside
NATIVE_TARGET_C = F(-101, 105)   # Bell-violating native target: CHSH 202/75, outside
CLASSICAL_CHSH_BOUND = F(2)
LOCAL_BOUNDARY_ABS_C = F(5, 7)   # |c| = 5/7 is the local boundary (CHSH = 2)


# =====================================================================
#  self-contained finite CHSH (2,2,2) local polytope (inline; imports nothing)
# =====================================================================

def _local_vertices():
    """The 8 deterministic local correlation vertices (a0b0, a0b1, a1b0, a1b1).
    Each IS a kind-(a) DEPOSIT read extremally: a one-time shared lambda fixing
    local response functions a_x(lambda), b_y(lambda), read identically every pair
    with NO per-pair directed input. Every such vertex has correlator-product +1
    (E00 E01 E10 E11 = (a0 a1 b0 b1)^2 = 1) -- the structural signature of 'no
    directed input'."""
    return sorted({(a0 * b0, a0 * b1, a1 * b0, a1 * b1)
                   for a0, a1, b0, b1 in product((1, -1), repeat=4)})


def _chsh_facets():
    """The 8 oriented CHSH facets: sign patterns s in {+-1}^4 with product -1.
    The facet inequality is <s, E> <= 2."""
    return [s for s in product((1, -1), repeat=4)
            if s[0] * s[1] * s[2] * s[3] == -1]


def _dot(s, v):
    return sum(F(si) * F(vi) for si, vi in zip(s, v))


def _behavior(c):
    """The behavior c * NATIVE_DIRECTION as an exact 4-tuple of correlators
    (matches the banked sibling's convention E = c * DIRECTION)."""
    return tuple(F(c) * d for d in NATIVE_DIRECTION)


def _max_chsh(E):
    """max over the 8 CHSH facets of <s, E> (exact)."""
    return max(_dot(s, E) for s in _chsh_facets())


def _in_local_polytope(E, facets=None):
    """Fine's test: E is in the (2,2,2) correlation (Boole) polytope iff it
    satisfies the COMPLETE H-description -- the 8 box facets |E_xy| <= 1 AND the 8
    oriented CHSH facets <s,E> <= 2. CHSH-only is complete ONLY for correlators
    already bounded by 1; the box constraints are independently load-bearing."""
    if facets is None:
        facets = _chsh_facets()
    return all(abs(F(x)) <= 1 for x in E) and \
           all(_dot(s, E) <= CLASSICAL_CHSH_BOUND for s in facets)


def _violated_facets(E):
    return [s for s in _chsh_facets() if _dot(s, E) > CLASSICAL_CHSH_BOUND]


def _rref_solve(rows, rhs):
    """Exact Gauss-Jordan over Fraction. Returns the UNIQUE solution (list of n
    Fractions) iff it exists and is unique; else None. No floats."""
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
            return None
    if rank != n:
        return None
    sol = [F(0)] * n
    for i in range(rank):
        sol[pivot_col[i]] = A[i][n]
    return sol


def _construct_common_cause(E):
    """Search for an EXACT nonnegative DEPOSIT (common cause): weights w_i >= 0 on
    the local deterministic vertices, sum 1, reconstructing E. By Caratheodory a
    point of the 4-dim correlation polytope needs <= 5 vertices. Returns
    {support, vertices, weights} or None. A nonnegative solution EXISTS iff E is a
    convex combination of local vertices, i.e. iff E is in the local polytope
    (the constructive half of Fine). Any nonneg combination of local vertices is
    local, so an above-facet E can have NONE."""
    verts = _local_vertices()
    Ef = tuple(F(x) for x in E)
    for k in range(1, 6):
        for support in combinations(range(len(verts)), k):
            sub = [verts[j] for j in support]
            rows = [[F(sub[j][coord]) for j in range(k)] for coord in range(4)]
            rows.append([F(1)] * k)
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


def _deposit_behavior(weights, vertices):
    """Per-pair correlator of a shared-lambda deposit: E = sum_lambda p(lambda) v(lambda).
    N-INDEPENDENT by construction: no pair-count enters this expression -- the
    deposit is read identically each pair."""
    return tuple(sum(weights[i] * F(vertices[i][c]) for i in range(len(weights)))
                 for c in range(4))


def _deposit_empirical_max_chsh(N):
    """Exact, EXHAUSTIVE enumeration of every deposit's per-pair empirical behavior
    over N pairs. A deposit realizes some shared lambda per pair; over N pairs the
    empirical per-(x,y) correlator is the average, i.e. a rational convex
    combination (1/N) * sum of local vertices. Enumerate all multisets of N
    vertices, take the exact max CHSH. It is 2 for EVERY N (achieved by all-N-pairs
    on one optimal vertex; every mixture is <= 2 by convexity). Real teeth for
    N-independence: the reachable optimum never grows with N."""
    verts = _local_vertices()
    best = F(0)
    for ms in combinations_with_replacement(range(len(verts)), N):
        E = tuple(sum(F(verts[i][c]) for i in ms) / N for c in range(4))
        m = _max_chsh(E)
        if m > best:
            best = m
    return best


def _rollout_best_deposit_chsh(N):
    """Explicit N-pair rollout of the best single-state deposit: draw lambda ONCE
    (the shared deposit), fix the best vertex, and 'play' N pairs. With lambda
    fixed the outcomes are deterministic, so the empirical per-(x,y) correlator
    over the N pairs equals that vertex's component EXACTLY, and the empirical CHSH
    = 2 for every N (no fluctuation, no growth). Returns (chsh, N)."""
    verts = _local_vertices()
    best = max(verts, key=lambda v: _max_chsh(v))
    emp = tuple(F(x) for x in best)            # identical for all N pairs
    return _max_chsh(emp), N


def _signaling_behavior():
    """A per-pair DIRECTED (communicating) strategy: Alice reads Bob's setting y
    each pair (per-pair directed input = a per-activation event) and outputs
    a(x, y); Bob outputs b(y) = +1. Choosing a(x, y) = -1 iff (x, y) = (1, 1),
    else +1, yields E = (+1, +1, +1, -1) with CHSH = 4 -- OUTSIDE the polytope. Its
    correlator-product is -1, structurally IMPOSSIBLE for any deposit (which is
    always product +1). The directed read is booked EACH pair: kind-(b)
    per-activation, not a one-time deposit."""
    def a(x, y):
        return -1 if (x == 1 and y == 1) else 1

    def b(y):
        return 1

    return (F(a(0, 0) * b(0)), F(a(0, 1) * b(1)),
            F(a(1, 0) * b(0)), F(a(1, 1) * b(1)))


def _aggregate_two(E1, E2, w):
    """The 'N=2 aggregate' of two per-pair behaviors is a convex mixture; if both
    are in the polytope the mixture is too (convexity). Exhibits that collecting
    more pairs cannot leave the polytope."""
    return tuple(w * F(a) + (1 - w) * F(b) for a, b in zip(E1, E2))


# =====================================================================
#  shared bank-contract metadata
# =====================================================================

_COMMON = {
    "tier": 4,
    "physical_premises_certified": False,
    "family": FAMILY,
    "dependencies": [],
    "cross_refs": [
        "check_T_third_boat_iff_local",
        "T_ledger_rent_excluded",
        "T_realignment_cost_is_transition_energy",
        "T_ijc_boolean_defender_bridge",
        "T_minimal_branch_selection_obstruction",
        "T_IJC_dichotomy",
        "T_quantum_admissibility_condition",
        "Paper20_Supplement_D2_superadditivity_necessary_not_sufficient",
        "symmetry_cost_floor",
        "order_refining_break",
        "occupant_cost_selection",
    ],
    "may_not_cite": [
        "cost surplus => quantum",
        "the branch/QAC is derived",
        "capacity shortage => quantum",
        "APF charges the per-activation directed structure a positive cost "
        "(enforcement-realism is OPEN)",
        "the rent-exclusion gate lifts the QAC",
        "superadditivity is sufficient for the QAC (Paper 20 Supp D2: "
        "necessary-not-sufficient)",
    ],
}


# =====================================================================
#  L1 -- a kind-(a) deposit is a local hidden variable (polytope-bound)
# =====================================================================

def check_L_deposit_is_local_hidden_variable():
    """[P_structural] with a [P_math] core.

    A kind-(a) DEPOSIT -- a one-time shared structure lambda, read the same way
    each pair with NO per-pair directed input -- is exactly SHARED RANDOMNESS = a
    common cause / local hidden variable. By Fine (cross-ref
    check_T_third_boat_iff_local) the set of correlations a deposit-only account
    can reach is EXACTLY the local (Boole) polytope.

    [P_math] core: enumerate the 8 local deterministic vertices; every deposit
    behavior is a convex combination of them, and by LINEARITY of the CHSH facet
    functionals every such combination satisfies all 8 CHSH facets (<= 2). The
    native above-facet target (CHSH 202/75 > 2, margin 52/75) violates a facet, so
    a deposit-only account PROVABLY cannot reproduce it (also confirmed
    constructively: no nonnegative common cause exists).

    FENCE: 'deposit = shared randomness = LHV' is a MODELING reading of
    rent-exclusion kind-(a) ([P_structural]); the polytope-membership is the
    [P_math] part. This does NOT derive the QAC and does NOT use cost surplus as a
    quantum criterion (barred; Paper 20 Supp D2)."""
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        return cond

    verts = _local_vertices()
    facets = _chsh_facets()
    ck(len(verts) == 8, "8 local deterministic deposit vertices")
    ck(len(facets) == 8, "8 oriented CHSH facets (sign product -1)")
    ck(all(v[0] * v[1] * v[2] * v[3] == 1 for v in verts),
       "every deposit vertex has correlator-product +1 (no directed input)")

    # --- [P_math] core: the easy (no-go) inclusion, exactly ---
    ck(all(_in_local_polytope(v) for v in verts),
       "every deposit vertex is inside the local polytope (box AND CHSH)")
    ck(all(_dot(s, v) <= F(2) for s in facets for v in verts),
       "all 64 (vertex, facet) evaluations satisfy CHSH <= 2")
    tight_counts = [sum(1 for v in verts if _dot(s, v) == F(2)) for s in facets]
    ck(all(t == 4 for t in tight_counts),
       "each CHSH facet is tight (= 2) on exactly 4 vertices (facet-defining)")

    # linearity teeth: f_s(sum w_i v_i) == sum w_i f_s(v_i) EXACTLY -> convex hull <= 2
    dep_w = [F(1, 2), F(1, 3), F(1, 6)]
    dep_v = [verts[0], verts[2], verts[7]]
    dep_E = _deposit_behavior(dep_w, dep_v)
    s0 = facets[0]
    lhs = _dot(s0, dep_E)
    rhs = sum(dep_w[i] * _dot(s0, dep_v[i]) for i in range(3))
    ck(lhs == rhs,
       "CHSH facet functional is linear: f_s(deposit) == combo of f_s(vertices)")
    ck(_max_chsh(dep_E) <= F(2), "the sampled deposit satisfies CHSH <= 2")

    # a deposit CAN reproduce the in-polytope control (constructive Fine half)
    ctrl = _behavior(CONTROL_C)
    ctrl_boat = _construct_common_cause(ctrl)
    ck(_max_chsh(ctrl) == F(7, 5), "control CHSH 7/5 (inside)")
    ck(ctrl_boat is not None,
       "a deposit (nonnegative common cause) reproduces the in-polytope control")

    # --- native target: outside -> provably NOT deposit-reachable ---
    tgt = _behavior(NATIVE_TARGET_C)
    tgt_chsh = _max_chsh(tgt)
    ck(tgt_chsh == F(202, 75), "native target CHSH == 202/75")
    ck(tgt_chsh - F(2) == F(52, 75), "native facet-violation margin == 52/75")
    viol = _violated_facets(tgt)
    ck(len(viol) == 1, "native target violates exactly one CHSH facet")
    ck(all(abs(x) <= 1 for x in tgt),
       "native target satisfies the box facets (violation is CHSH-only)")
    tgt_local = _in_local_polytope(tgt)
    ck(not tgt_local, "native target is OUTSIDE the local polytope")
    tgt_boat = _construct_common_cause(tgt)
    ck(tgt_boat is None,
       "NO deposit reproduces the native target (constructive Fine no-go)")

    # --- fail-control 1 (mutation flips): drop the violated facet -> the broken
    #     membership test misclassifies the target as 'inside', but the constructive
    #     search still finds NO deposit; the two DISAGREE -> the full facet family is
    #     load-bearing (a deposit still cannot reach an above-facet point) ---
    broken = [s for s in facets if s not in viol]
    tgt_local_broken = _in_local_polytope(tgt, facets=broken)
    mutation_dropping_facet_flips = tgt_local_broken and (tgt_boat is None)
    ck(mutation_dropping_facet_flips,
       "dropping the violated facet flips the membership verdict but not the "
       "construction -- the facet is load-bearing")

    # --- fail-control 2: an INSIDE target (control, CHSH 7/5) IS deposit-reachable
    #     -> the gate genuinely discriminates inside vs outside ---
    mutation_inside_reachable = (tgt_boat is None) and (ctrl_boat is not None)
    ck(mutation_inside_reachable,
       "an inside target is deposit-reachable while the outside target is not "
       "(the gate discriminates)")

    passed = not fails
    out = {
        "name": "L_deposit_is_local_hidden_variable",
        "epistemic": "P_structural",
        "math_core": "P_math",
        "passed": passed,
        "key_result": (
            "A kind-(a) DEPOSIT (one-time shared lambda, read identically each "
            "pair, no per-pair directed input) is shared randomness = a common "
            "cause / LHV, so the deposit-reachable set is EXACTLY the local (Boole) "
            "polytope (Fine; cross-ref check_T_third_boat_iff_local). [P_math] "
            "core: every deposit behavior is a convex combination of the 8 "
            "deterministic vertices and, by linearity of the CHSH facets, satisfies "
            "CHSH <= 2 (all 64 vertex-facet evaluations <= 2; each facet tight on 4 "
            "vertices). The native target (c = -101/105, CHSH 202/75, margin 52/75) "
            "violates exactly one CHSH facet, so a deposit-only account provably "
            "cannot reproduce it (no nonnegative common cause exists). FENCE: the "
            "deposit=LHV identification is a modeling reading of rent-exclusion "
            "kind-(a); the polytope-membership is the [P_math] part."
        ),
        "n_vertices": len(verts),
        "n_facets": len(facets),
        "control_c": str(CONTROL_C),
        "control_chsh": str(_max_chsh(ctrl)),
        "control_deposit_reproducible": ctrl_boat is not None,
        "native_target_c": str(NATIVE_TARGET_C),
        "native_target_chsh": str(tgt_chsh),
        "native_target_margin": str(tgt_chsh - F(2)),
        "native_target_violated_facets": len(viol),
        "native_target_in_polytope": tgt_local,
        "native_target_no_common_cause": tgt_boat is None,
        "mutation_dropping_facet_flips": mutation_dropping_facet_flips,
        "mutation_inside_reachable": mutation_inside_reachable,
        "fail_reasons": fails,
    }
    out.update(_COMMON)
    return out


# =====================================================================
#  T2 -- the hidden order is per-activation, not standing-rent
# =====================================================================

def check_T_order_is_per_activation_not_standing_rent():
    """[P_structural].

    Because a deposit-only account reaches only the local polytope (L1),
    reproducing the above-facet correlation requires PER-PAIR directed structure
    (communication) -- shared randomness is provably insufficient (Bell/Fine
    restated). Per-pair directed structure is booked EACH time the interface
    activates -> a kind-(b) PER-ACTIVATION charge. It is NOT excluded standing-rent
    (mere persistence) and NOT a kind-(a) amortizable deposit (the deposit is the
    LHV that FAILS by L1).

    NON-AMORTIZATION made executable: a bounded one-time deposit of k classical
    states, applied identically per pair, reaches only the polytope for ALL
    pair-counts N -- its reachable set does NOT grow with N (enumerated exactly for
    N in 1..6; the linear-program optimum = 2 for all N). Only per-pair DIRECTED
    input escapes the polytope; THAT escape is the per-activation part.

    CONCLUSION: the hidden order PASSES the rent-exclusion gate as a chargeable
    per-activation cost.

    FENCE: this shows the order is per-activation (chargeABLE); it does NOT prove
    APF charges it a positive cost (enforcement-realism is OPEN) and does NOT
    derive the QAC or use cost surplus as a quantum criterion (barred; Supp D2)."""
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        return cond

    verts = _local_vertices()

    # (A) a deposit's per-pair behavior is in the polytope (<= 2)
    dep_w = [F(1, 4)] * 4
    dep_v = [verts[0], verts[3], verts[5], verts[6]]
    dep_E = _deposit_behavior(dep_w, dep_v)
    ck(_in_local_polytope(dep_E),
       "a shared-lambda deposit behavior is in the local polytope")
    ck(_max_chsh(dep_E) <= F(2), "deposit behavior satisfies CHSH <= 2")

    # (B) N-INDEPENDENCE, enumerated EXACTLY for small N
    small_Ns = [1, 2, 3, 4, 5, 6]
    enum_opt = [_deposit_empirical_max_chsh(N) for N in small_Ns]
    ck(all(x == F(2) for x in enum_opt),
       "enumerated max deposit CHSH == 2 for every N in 1..6 (all empirical deposits)")
    ck(len(set(enum_opt)) == 1,
       "the enumerated deposit optimum does NOT grow with N (N-independent)")

    # explicit N-pair rollout of the best single-state deposit
    roll = [_rollout_best_deposit_chsh(N)[0] for N in small_Ns]
    ck(all(x == F(2) for x in roll),
       "explicit N-pair rollout: empirical CHSH == 2 for every N")

    # closed form -- a CHSH facet functional is LINEAR, so its maximum over the convex
    # hull of deposits is attained at a vertex: max over hull == max over vertices ==
    # lp_opt, with NO dependence on the pair-count N. The deposit's reachable CHSH
    # optimum is therefore N-FREE at 2. No large-N loop is needed or possible
    # (N = 10^9 is not enumerable); the finite N=1..6 enumeration matches this closed
    # form exactly, which is where the real teeth are.
    lp_opt = max(_max_chsh(v) for v in verts)
    tgt_chsh = _max_chsh(_behavior(NATIVE_TARGET_C))
    ck(lp_opt == F(2), "closed-form deposit optimum (max over vertices) == 2")
    ck(lp_opt < tgt_chsh,
       "deposit optimum (2) < native target (202/75): unreachable at any N")
    ck(all(x == lp_opt for x in enum_opt) and lp_opt == F(2),
       "closed form (max over hull == max over vertices == 2, N-free): the N=1..6 "
       "enumeration matches the closed-form optimum, so no N dependence remains to "
       "enumerate at large N (the deleted big-N loop only repeated the constant)")

    # reachable SET is N-independent = the polytope (convexity spot-check)
    agg = _aggregate_two(_behavior(CONTROL_C), dep_E, F(1, 3))
    ck(_in_local_polytope(agg),
       "the N=2 aggregate of two in-polytope behaviors stays in the polytope")

    # (C) the ESCAPE is per-pair DIRECTED input (per-activation), not deposit size or N
    sig = _signaling_behavior()
    sig_chsh = _max_chsh(sig)
    ck(sig_chsh == F(4), "per-pair directed (signaling) strategy reaches CHSH 4")
    ck(not _in_local_polytope(sig),
       "the directed (signaling) behavior is OUTSIDE the polytope")
    ck(sig[0] * sig[1] * sig[2] * sig[3] == F(-1),
       "the directed behavior has correlator-product -1 (impossible for any deposit)")
    ck(sig_chsh > F(2),
       "the directed escape clears the facet (CHSH 4 > 2)")

    deposit_escapes = (lp_opt > F(2)) or any(x > F(2) for x in enum_opt)
    directed_escapes = sig_chsh > F(2)
    ck(not deposit_escapes,
       "a deposit (any k, any N) does NOT escape the polytope")
    ck(directed_escapes,
       "per-pair directed input DOES escape the polytope")

    # responsiveness of the enumeration (real teeth, replacing the big-N theater):
    # the enumeration / closed form returns 2 because it maximizes over the ADMITTED
    # (local) vertex set, not because it is hardwired. Admit the directed (signaling)
    # vertex into the vertex pool and re-run the SAME max: it jumps to 4. So the "2"
    # is a genuine response to the local-only restriction (exactly L1's content).
    verts_with_directed = verts + [tuple(int(x) for x in sig)]
    responsive_max = max(_max_chsh(v) for v in verts_with_directed)
    ck(responsive_max == F(4),
       "responsiveness: admitting a directed vertex jumps the enumerated max from 2 "
       "to 4 -- the deposit optimum genuinely tracks the vertex set (real teeth)")

    # the two axes separated (from the closed form + the real N=1..6 enumeration; no
    # repeated-constant theater): the deposit optimum is N-free at 2 and the directed
    # optimum is a single N-free value 4. Only the directed one clears the facet ->
    # escape tracks DIRECTEDNESS (per-activation), NOT the pair-count (amortization).
    deposit_optimum_N_independent = (len(set(enum_opt)) == 1
                                     and all(x == lp_opt for x in enum_opt)
                                     and lp_opt == F(2))
    directed_optimum_N_independent = (sig_chsh == F(4))
    both_N_independent = (deposit_optimum_N_independent
                          and directed_optimum_N_independent)
    only_directed_input_escapes = (lp_opt == F(2) and sig_chsh > F(2))
    ck(both_N_independent,
       "both deposit and directed optima are N-independent (neither amortizes): "
       "deposit == 2 across N=1..6 and closed-form, directed == 4 (single behavior)")
    ck(only_directed_input_escapes,
       "only the directed optimum (4) exceeds 2 -> the escape is PER-ACTIVATION, "
       "not amortization of a deposit")

    passed = not fails
    out = {
        "name": "T_order_is_per_activation_not_standing_rent",
        "epistemic": "P_structural",
        "passed": passed,
        "key_result": (
            "Reproducing the above-facet correlation (CHSH 202/75 > 2) requires "
            "per-pair DIRECTED structure -- shared randomness is provably "
            "insufficient (L1 / Fine). A bounded one-time deposit of k classical "
            "states, applied identically per pair, reaches ONLY the polytope for "
            "ALL N: the enumerated max empirical CHSH is 2 for N in 1..6 and the "
            "linear-program optimum (max over vertices) is 2 for arbitrarily large "
            "N -- its reachable set is N-INDEPENDENT, so it cannot be amortized "
            "into above-facet reproduction. Only per-pair directed input escapes "
            "(explicit signaling strategy, CHSH 4, correlator-product -1 -- "
            "structurally impossible for any deposit). The hidden order is a "
            "kind-(b) PER-ACTIVATION charge, not excluded standing-rent and not a "
            "kind-(a) deposit; it PASSES the rent-exclusion gate as chargeable. "
            "FENCE: chargeABLE, not proven charged (enforcement-realism OPEN)."
        ),
        "deposit_behavior_in_polytope": _in_local_polytope(dep_E),
        "enumerated_deposit_opt_small_N": [str(x) for x in enum_opt],
        "closed_form_deposit_opt": str(lp_opt),
        "responsiveness_directed_vertex_max": str(responsive_max),
        "native_target_chsh": str(tgt_chsh),
        "deposit_optimum_N_independent": deposit_optimum_N_independent,
        "signaling_escape_chsh": str(sig_chsh),
        "signaling_correlator_product": str(sig[0] * sig[1] * sig[2] * sig[3]),
        "deposit_escapes": deposit_escapes,
        "directed_input_escapes": directed_escapes,
        "only_directed_input_escapes": only_directed_input_escapes,
        "fail_reasons": fails,
    }
    out.update(_COMMON)
    return out


# =====================================================================
#  T3 -- the charge is a relative per-pair difference; no absolute baseline
# =====================================================================

def check_T_relative_charge_no_absolute_baseline():
    """[P_structural_reading].

    The per-activation charge is a RELATIVE per-pair DIFFERENCE: the reductive
    (hidden-order) account carries a directed per-pair term (needed to exit the
    polytope) that the irreducible (orthodox) account does not. A2 (least-cost
    selection) is COMPARATIVE, so only the SIGN of the difference matters -- no
    absolute cost baseline is needed. This SIDESTEPS the reduced cost-shape /
    directionality posit, which required an absolute 'unenforced baseline' (that
    lift was REDUCED; not resurrected here).

    Model: each account's per-pair cost = (common commit term B) + (directed term).
    Directed term is > 0 for the reductive account (above the facet), 0 for the
    irreducible account. The difference is the directed term, INDEPENDENT of B and
    strictly positive above the facet.

    MODELING ASSUMPTION (fenced): the irreducible / orthodox account carries NO
    directed per-pair term (d_irr = 0). This is the LOAD-BEARING asymmetry -- the
    entire relative charge is the reductive account's directed term measured against
    an orthodox account that books none. It is an explicit modeling choice about the
    orthodox ontology (declining a directed per-pair influence is exactly what makes
    an account "irreducible / orthodox" here), NOT a derived fact; the fail-control
    fail_control_asymmetry_flips shows the result flips if the orthodox account is
    given the same directed term.

    FENCE: this does NOT prove the directed term has a POSITIVE APF cost --
    whether APF charges it (enforcement-realism) is OPEN. The checks pass for ANY
    positive placeholder directed term; only baseline-cancellation and the SIGN of
    the difference are load-bearing. Does NOT derive the QAC; barred heads stand."""
    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        return cond

    tgt = _behavior(NATIVE_TARGET_C)
    ctrl = _behavior(CONTROL_C)
    above = _max_chsh(tgt) > F(2)     # directed structure required
    below = _max_chsh(ctrl) <= F(2)   # no directed structure required
    ck(above, "native target is above the facet (directed structure required)")
    ck(below, "control is below the facet (no directed structure required)")

    # POSITIVE placeholders for the directed term -- magnitude is NOT derived
    # (enforcement-realism OPEN); the argument uses only 'directed term > 0'.
    baselines = [F(0), F(1), F(100), F(-7), F(3, 2)]
    deltas = [F(52, 75), F(1), F(1, 1000), F(7)]
    d_irr = F(0)

    # baseline-independence AND sign, across a grid of (B, directed term)
    baseline_independent = True
    sign_positive = True
    a2_picks_irreducible = True
    for B in baselines:
        for d_red in deltas:
            reductive = B + d_red
            irreducible = B + d_irr
            delta = reductive - irreducible
            if delta != d_red:
                baseline_independent = False
            if not (delta > 0):
                sign_positive = False
            if not (irreducible < reductive):
                a2_picks_irreducible = False
    ck(baseline_independent,
       "ALGEBRAIC IDENTITY (not a discriminating catch): the common baseline B "
       "cancels by construction of the shared-commit model, so the difference == the "
       "directed term regardless of B. Load-bearingness of the shared B is shown by "
       "fail_control_baseline_flips (unequal baselines), NOT by this identity.")
    ck(sign_positive,
       "the difference is strictly positive above the facet (any positive directed term)")
    ck(a2_picks_irreducible,
       "A2 (least cost) selects the irreducible (orthodox) account above the facet")

    # below the facet the correlation is classically reachable, so the REDUCTIVE
    # account needs no directed term either (d_red_below = 0 by construction): both
    # accounts book only B and the difference vanishes -> A2 indifferent. Real teeth
    # come from the CONTRAST -- the same model gives a strictly positive difference
    # above the facet (sign_positive) -- so this is a below/above contrast, not a
    # bare x - x always-true guard.
    d_red_below = F(0)
    indifferent_below = all((B + d_red_below) - (B + d_irr) == F(0) for B in baselines)
    ck(indifferent_below and sign_positive,
       "below the facet the difference is 0 (reductive directed term also 0) WHILE "
       "above the facet the same model gives a strictly positive difference -- a real "
       "below/above contrast, not a bare x - x")

    # --- fail-control 1 (asymmetry load-bearing): a REAL contrast, not x - x. For
    #     each (B, d_red) compute BOTH the SYMMETRIZED difference (give the irreducible
    #     account the same directed term d_red -> sym == 0) AND the real ASYMMETRIC
    #     difference (reductive d_red vs irreducible d_irr = 0 -> asym == d_red != 0).
    #     The leg asserts sym == 0 AND asym != 0, so the reductive-vs-irreducible
    #     asymmetry is load-bearing: symmetrizing the directed term (d_irr -> d_red)
    #     collapses asym to 0 and flips this leg to False. ---
    fail_control_asymmetry_flips = True
    for B in baselines:
        for d_red in deltas:
            sym = (B + d_red) - (B + d_red)    # symmetrized: both accounts carry d_red
            asym = (B + d_red) - (B + d_irr)   # real: reductive d_red vs irreducible d_irr=0
            if not (sym == F(0) and asym != F(0)):
                fail_control_asymmetry_flips = False
    ck(fail_control_asymmetry_flips,
       "fail-control: the symmetrized directed term cancels (sym == 0) while the real "
       "reductive-vs-irreducible difference does not (asym != 0) -- the asymmetry is "
       "load-bearing (symmetrizing d_irr -> d_red flips this leg to False)")

    # --- fail-control 2 (shared-baseline load-bearing): unequal baselines make the
    #     difference baseline-DEPENDENT -> the absolute-baseline-free reading breaks.
    #     The shared common-commit term is EXACTLY what sidesteps the absolute
    #     unenforced baseline. Flip. ---
    d_red = F(1)
    delta_a = (F(10) + d_red) - (F(3) + d_irr)
    delta_b = (F(20) + d_red) - (F(3) + d_irr)
    fail_control_baseline_flips = (delta_a != d_red) and (delta_b != delta_a)
    ck(fail_control_baseline_flips,
       "fail-control: unequal baselines make the difference baseline-DEPENDENT "
       "(the shared common-commit term is load-bearing)")

    passed = not fails
    out = {
        "name": "T_relative_charge_no_absolute_baseline",
        "epistemic": "P_structural_reading",
        "passed": passed,
        "key_result": (
            "The per-activation charge is a RELATIVE per-pair DIFFERENCE: the "
            "reductive account carries a directed per-pair term (needed to exit the "
            "polytope) the irreducible account does not. Writing each account's "
            "cost as (common commit term B) + (directed term), the difference "
            "equals the directed term -- INDEPENDENT of B across an arbitrary grid "
            "of baselines -- and is strictly positive above the facet. A2 is "
            "comparative, so only the SIGN matters: no absolute cost baseline is "
            "needed, which SIDESTEPS the reduced cost-shape / directionality posit "
            "(the absolute 'unenforced baseline'). Fail-controls: symmetrizing the "
            "directed term zeroes the difference (asymmetry load-bearing); unequal "
            "baselines make it baseline-dependent (shared commit term load-bearing). "
            "FENCE: the directed term's POSITIVITY as an APF cost "
            "(enforcement-realism) is OPEN; only cancellation and sign are proven."
        ),
        "above_facet_directed_required": above,
        "baseline_independent": baseline_independent,
        "sign_positive_above_facet": sign_positive,
        "a2_selects_irreducible": a2_picks_irreducible,
        "indifferent_below_facet": indifferent_below,
        "fail_control_asymmetry_flips": fail_control_asymmetry_flips,
        "fail_control_baseline_flips": fail_control_baseline_flips,
        "d_irr": str(d_irr),
        "d_irr_zero_is_fenced_modeling_assumption": (
            "the irreducible/orthodox account carries NO directed per-pair term "
            "(d_irr = 0) -- an explicit FENCED modeling assumption and the "
            "load-bearing asymmetry, not a derived fact"),
        "directed_term_positivity_is_open": True,
        "fail_reasons": fails,
    }
    out.update(_COMMON)
    return out


# =====================================================================
#  mutation battery (auditor fast-path)
# =====================================================================

def run_mutations():
    # Every entry is a REAL discriminating catch (a code mutation flips it to False).
    # The always-true baseline_independent algebraic identity is deliberately NOT in
    # this battery -- it is documented as an identity inside the check; the load-
    # bearing baseline test is M7_shared_baseline_load_bearing (unequal baselines).
    r = {}
    a = check_L_deposit_is_local_hidden_variable()
    r["M1_native_target_outside_polytope"] = (not a["native_target_in_polytope"])
    r["M2_no_deposit_reproduces_target"] = a["native_target_no_common_cause"]
    r["M3_dropping_facet_flips"] = a["mutation_dropping_facet_flips"]
    b = check_T_order_is_per_activation_not_standing_rent()
    r["M4_deposit_optimum_N_independent"] = b["deposit_optimum_N_independent"]
    r["M5_only_directed_input_escapes"] = b["only_directed_input_escapes"]
    c = check_T_relative_charge_no_absolute_baseline()
    r["M6_asymmetry_load_bearing"] = c["fail_control_asymmetry_flips"]
    r["M7_shared_baseline_load_bearing"] = c["fail_control_baseline_flips"]
    r["all_caught"] = all(r.values())
    return r


_CHECKS = {
    "L_deposit_is_local_hidden_variable": check_L_deposit_is_local_hidden_variable,
    "T_order_is_per_activation_not_standing_rent":
        check_T_order_is_per_activation_not_standing_rent,
    "T_relative_charge_no_absolute_baseline":
        check_T_relative_charge_no_absolute_baseline,
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
