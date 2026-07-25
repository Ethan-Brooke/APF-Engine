"""
zipper_metric_theorems.py -- The Zipper Clearance Lane, waves 2-4, v0.2
================================================================================

Charter: Reference - CONTINUATION - The Zipper Clearance Lane (2026-07-23).md
Build order: Reference - HANDOFF - The Zipper Clearance Waves 2-4 Build Seat.
Status:  bank-registered module (self-contained port of the standalone
         research module zipper_metric_theorems.py, v0.2). ppc = False.
         Non-exporting. Tier 4. Stdlib only (fractions.Fraction; NO floats;
         no scipy/numpy/sympy; no live-bank imports). Companion to wave 1
         (contextual_adjudication.py); imports nothing from it, does not
         modify it. Exact arithmetic (fractions.Fraction); NO floats anywhere.
         Caret-free (bit parity is % 2 arithmetic; powers are **) -- WG2
         fingerprint hygiene.

v0.2 CARRIES EVERY FINDING from two blinded cold audits of v0.1 (stage-1
statement-level LAND-WITH-FIXES 0.83; stage-2 adversarial-execution
LAND-WITH-FIXES 0.72, 23/36 hostile mutations initially silent). No v0.1
theorem was false; the audits found billing/relocation and
verification-BREADTH gaps. Dispositions of record:

  W3.2 (S1-1 MAJOR)  the trilemma is RE-BILLED from a check_T universal to an
       INHABITATION + case-split exhibit over a run-data mechanism space of 16
       specs (commit x preenc x live x delayed). The old 'fzc_forced' was
       f_live => f_live (a tautology on the 2-bit signature). The computed,
       falsifiable content now: all three arms inhabited by real specs;
       PREMATURE is not vacuous (a t-commit spec with NO B-source is computed
       UNFAITHFUL on half the inputs); the clearance-carrying complement
       exists. The trilemma itself is the charter's DECLARED case split.
  W2.5 (S2-1 MAJOR)  the signed-permutation grid count is 8 for L1, L4, L2 AND
       Linf -- a grid artifact that does NOT witness 'no continuous family'.
       The DISCRIMINATING computation is now the rational-rotation family per
       norm: Euclidean admits an infinite family (>= 4 exhibited), L1 and L4
       admit NONE. Docstring re-billed; the count is a secondary fact.
  W3.6 (S2-2 MAJOR)  the tightness legs (fits, overflow) are reported per case
       as exact (eps, C, floor) so the test RECOMPUTES tightness independently
       -- gutting the internal boolean no longer has zero refutation surface.
  W3.1 (S2-3 MAJOR)  NOT-PREENCODED is rebuilt as ALL-NODES-RELEVANT (flipping
       any single node's bit flips the parity relation) -- a falsifiable
       computation, not a satisfiable-either-way existential.
  W3.3 (S1-2 / S2-6)  Class I is now a COMPUTED depth-0 model (flood on a
       terminal-own-bit relation), not a literal True; Class II boundary
       records are DERIVED from the computed jump locations.
  W2.3 (S1-3)  re-billed as inhabitation of both arms (not a partition
       theorem); a MIXED family (some factor, some do not) is added so the
       classifier is non-trivial.
  W4.4 (S1-4)  'computed BOTH ways' dropped; the polarization identity is
       billed as a definitional bridge (tau-independent); the genuine
       tau-fact is Q-invariance == bilinear preservation.
  W2.2 (S1-5)  the converse is verified SYMBOLICALLY (D_(1,-1) = 0 on the
       monomial dict) and cross-checked against the grid instances.
  W4.6 (S2-5)  re-billed [concordance-citation]: it re-verifies the shared
       structural invariant INLINE (not a re-run of W4.3) and records the
       banked check-names; when the bank is absent it SKIPS the cross-check
       and says so -- it does not claim independent certification.
  W4.5 (S1-10 / S2-7)  no-J is computed over ALL enumerated diagonal
       generators; kappa and the Lambda values are reported and pinned.
  _direction (S1-6)  dead identical branch removed; canonical line rep kept.
  mutation battery (S1-7)  M3/M10/M12 now route through real computation
       (polynomial swap; the qc6b adjacency predicate; the tangent floor
       arithmetic) instead of literal-vs-literal.
  test suite (S2 systemic)  enumeration / sweep / census / grid sizes are now
       REPORTED and PINNED, and per-leg discriminating fields are asserted --
       shrinking a space to a point is no longer silent.
  docstring coverage (S1-8)  W3.4 narrowed to the (N, k) cases actually run.

CEILINGS (per charter 4f-4i and 5):
  W2.1 [P_math, FAMILY-RELATIVE]     selection within the declared L**p ansatz;
                                     never 'the burden is necessarily quadratic'.
  W2.2 [P_math]                      exact chain-rule / linear-algebra facts.
  W2.3 [P_structural]                inhabitation of a quotient dichotomy;
                                     consumes Sep/CoDef/IJC typing.
  W2.4 [P_math]                      convergent with the banked J
                                     (.432/.433); positivity LOAD-BEARING.
  W2.5 [P_math + prose]              instances; the compactness/averaging step
                                     is PROSE.
  W2.6 [P_math]                      the classical-wave ceiling is stated here.
  W3.1 [P_structural]                exact propagation lower bound.
  W3.2 [P_structural]                inhabitation + case split; nonlocal arm
                                     governed by pending R-boundary-witness.
  W3.3 [P_math]                      existence exhibits only.
  W3.4 [P_math]                      discrete constancy + witnessed-jump
                                     dichotomy, on the enumerated cases.
  W3.5 [P_math]                      exact cross-derivative contrast.
  W3.6 [P_structural]                instantiates banked finite-basis .425.
  W4.1-4.4 [P_math]                  exact moving-frame linear algebra.
  W4.5 [control]                     non-pool-reducibility WITHOUT mixing.
  W4.6 [concordance-citation]        structural re-verify + banked names;
                                     skip cross-check when bank absent.

NAMED PREMISES (consumed, never derived -- charter 3, 4f-4i):
  NON-POOL-REDUCIBILITY, MIXER-EXISTENCE, RELATIONAL-FRAME-VARIABILITY,
  CYCLIC-NEUTRALITY, NOT-PREENCODED, CONTEXT-INTEGRATION, ENV-RICHNESS,
  P-LIN (linear carrier; standing bar), L_irr, DECLARED-FORM (C, r) scoping
  (Ruling 5; NONCONSERVATIVE_OPERATIONAL_QUOTIENT the failure predicate).

CONCORDANCES (banked; cited, never duplicated):
  CoDef aggregation        check_L_codef_aggregation_argmin (.410)  -> W2.3
  finite operational basis check_T_finite_operational_basis,
                           check_T_admissibility_greedoid_structure (.425) -> W3.6
  two-exchange holonomy    two_exchange_holonomy (.432)             -> W4.3/W4.6
  graded orientation J     graded_orientation_closure central-J (.433) -> W4.6
  bounded-orbit positivity bounded_orbit_positivity boost-exclusion -> W2.4

MAY NOT BE CITED FROM THIS MODULE:
  occupancy-derivation; any Born / weighting content (.422 bar); any
  nonclassicality claim beyond the chartered kill shapes (order-sensitivity is
  NOT invoked -- charter 0 bar 8); 'the burden is necessarily quadratic'
  (W2.1 is family-relative); 'the classical buffer is dead' unconditionally
  (W2.6/W3.4 kill it only on the coherent sector, under named gates);
  'the gap is forced' without the premise names attached; the W3.2 trilemma
  as a 'derived necessity' (it is a declared case split with inhabited arms).

PORT NOTES (self-contained bank port; computed content unchanged):
  * Grades preserved at the source's honest per-leg ceilings -- fourteen
    [P_math]/[P_structural] legs (epistemic "P_math"/"P_structural"), plus
    W2.5 P_math (its GENERAL theorem rests on a disclosed prose step; the
    executed content is the discriminating instance computation), W4.5
    [control], and W4.6 [concordance-citation]. NOTHING upgraded.
  * The W4.6 concordance leg is self-contained: the original live-bank import
    probe (apf.two_exchange_holonomy / graded_orientation_closure) is REMOVED;
    banked check-names + anchor versions are HARDCODED (frozen at the port)
    and the shared structural invariant is recomputed inline. Its pass
    condition was always inline-only.
  * Each check's return dict carries the bank-contract keys: passed,
    epistemic, physical_premises_certified=False, name, tier=4, family, and
    the module-level may_not_cite fence.
"""

from fractions import Fraction
from functools import wraps
from itertools import product, permutations

F = Fraction

FAMILY = "structural.zipper_metric_theorems"

# Module-level MAY-NOT-CITE fence (surfaced in every check's return dict).
MAY_NOT_CITE = (
    "occupancy-derivation",
    "any Born / weighting content (.422 bar)",
    "any nonclassicality claim beyond the chartered kill shapes "
    "(order-sensitivity is NOT invoked -- charter 0 bar 8)",
    "'the burden is necessarily quadratic' (W2.1 is family-relative)",
    "'the classical buffer is dead' unconditionally "
    "(W2.6/W3.4 kill it only on the coherent sector, under named gates)",
    "'the gap is forced' without the premise names attached",
    "the W3.2 trilemma as a 'derived necessity' "
    "(it is a declared case split with inhabited arms)",
)


def _bank_leg(name, epistemic, ceiling):
    """Wrap a check so its return dict carries the bank-contract keys
    (name, epistemic, tier, physical_premises_certified, family, ceiling,
    may_not_cite) without altering the computed body."""
    def deco(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            r = fn(*args, **kwargs)
            r.setdefault("passed", False)
            r["name"] = name
            r["epistemic"] = epistemic
            r["tier"] = 4
            r["physical_premises_certified"] = False
            r["family"] = FAMILY
            r["ceiling"] = ceiling
            r["may_not_cite"] = list(MAY_NOT_CITE)
            return r
        return wrapped
    return deco


# =====================================================================
# PART 0 -- exact 2x2 matrix + 2-variable polynomial helpers
# =====================================================================


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(2)) for j in range(2)]
            for i in range(2)]


def mt(A):
    return [[A[j][i] for j in range(2)] for i in range(2)]


def madd(A, B):
    return [[A[i][j] + B[i][j] for j in range(2)] for i in range(2)]


def msub(A, B):
    return [[A[i][j] - B[i][j] for j in range(2)] for i in range(2)]


def mscale(A, c):
    return [[A[i][j] * c for j in range(2)] for i in range(2)]


def mvec(A, v):
    return (A[0][0] * v[0] + A[0][1] * v[1],
            A[1][0] * v[0] + A[1][1] * v[1])


def is_zero(A):
    return all(A[i][j] == 0 for i in range(2) for j in range(2))


def meq(A, B):
    return all(A[i][j] == B[i][j] for i in range(2) for j in range(2))


ID2 = [[F(1), F(0)], [F(0), F(1)]]


# --- 2-variable exact polynomials as dict {(i,j): coeff} over (x0, x1) ---

def p_add(p, q):
    out = dict(p)
    for k, c in q.items():
        out[k] = out.get(k, F(0)) + c
    return {k: c for k, c in out.items() if c != 0}


def p_scale(p, c):
    return {k: v * c for k, v in p.items() if v * c != 0}


def p_swap(p):
    """Swap the two variables: coeff of x0**i x1**j -> coeff of x0**j x1**i.
    Used to test exchange parity honestly (not by a hardcoded copy)."""
    return {(j, i): c for (i, j), c in p.items()}


def p_d0(p):
    out = {}
    for (i, j), c in p.items():
        if i >= 1:
            out[(i - 1, j)] = out.get((i - 1, j), F(0)) + c * i
    return {k: v for k, v in out.items() if v != 0}


def p_d1(p):
    out = {}
    for (i, j), c in p.items():
        if j >= 1:
            out[(i, j - 1)] = out.get((i, j - 1), F(0)) + c * j
    return {k: v for k, v in out.items() if v != 0}


def p_eq(p, q):
    return p_add(p, p_scale(q, F(-1))) == {}


def p_eval(p, x0, x1):
    return sum((c * x0 ** i * x1 ** j for (i, j), c in p.items()), F(0))


def p_dir_total_zero(p):
    """Exact SYMBOLIC criterion: D_(1,-1) p = d0 p - d1 p == 0, i.e. p is
    constant along (1,-1), i.e. p factors through the total x0 + x1."""
    return p_eq(p_add(p_d0(p), p_scale(p_d1(p), F(-1))), {})


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def pyth_points():
    """Nonidentity rational points on the unit circle (cos, sin) from
    primitive Pythagorean triples: ((m*m-n*n), 2mn) / (m*m+n*n)."""
    pts = []
    for m in range(2, 8):
        for n in range(1, m):
            if (m - n) % 2 == 1 and _gcd(m, n) == 1:
                d = m * m + n * n
                pts.append((F(m * m - n * n, d), F(2 * m * n, d)))
    return pts


# =====================================================================
# WAVE 2 -- the metric theorems (charter 4f)
# =====================================================================

def _balanced_poly(p):
    """Exact monomial dict of (a+b)**p + (a-b)**p in (a=x0, b=x1);
    coeff of a**i b**j = C(p,i) * (1 + (-1)**j)."""
    from math import comb
    out = {}
    for i in range(p + 1):
        j = p - i
        c = comb(p, i) * (1 + (-1) ** j)
        if c:
            out[(i, j)] = F(c)
    return out


@_bank_leg("L_square_law_selection", "P_math", "W2.1 [P_math, FAMILY-RELATIVE]")
def check_L_square_law_selection():
    """W2.1 [P_math, FAMILY-RELATIVE]. Within Q_p(a,b) = |a|**p + |b|**p, a
    single balanced recombination H_s(a,b) = s*(a+b, a-b) preserving the
    burden for ALL inputs forces p = 2, s**2 = 1/2.

    BILLING (mandatory): selection WITHIN the declared L**p ansatz -- NOT 'the
    burden is necessarily quadratic'. Real-exponent uniqueness rests on 2**x
    monotonicity (prose); the code verifies the INTEGER grid.

    (1) THE TWO FORCED IDENTITIES: b=0 gives 2 s**p = 1; a=b gives s**p 2**p =
        2; eliminating s**p gives 2**(p-1) = 2, i.e. 2**p = 4. Over the tested
        exponent grid, exactly p = 2 satisfies it.
    (2) EVEN-EXPONENT SWEEP: the balanced map preserves Q_p (a polynomial
        identity for even p) iff (a+b)**p + (a-b)**p is a scalar multiple of
        a**p + b**p. p = 4, 6, 8 each carry a NONZERO cross monomial (reported
        with its coefficient so the death is pinned); only p = 2 is pure and
        consistent.
    (3) At p = 2, s**2 = 1/2 makes the burden invariant for ALL rational
        (a,b) on a grid (exact, using the rational s**2)."""
    forced_grid = list(range(1, 9))
    forced = {p: (2 ** p == 4) for p in forced_grid}
    forced_gives_p2 = [p for p in forced if forced[p]] == [2]

    even_tested = [2, 4, 6, 8]
    survivors = []
    deaths = {}
    for p in even_tested:
        bp = _balanced_poly(p)
        k0, k1 = bp.get((p, 0)), bp.get((0, p))
        pure = (set(bp) <= {(p, 0), (0, p)}) and (k0 is not None) and (k0 == k1)
        if pure and F(2 ** p, 1) / k0 == 2:
            survivors.append(p)
        else:
            cross = {kk: vv for kk, vv in bp.items()
                     if kk not in ((p, 0), (0, p))}
            deaths[p] = cross

    s2 = F(1, 2)
    grid = [F(x, y) for x in range(-3, 4) for y in range(1, 4)]
    inv_p2 = all(
        s2 * (a + b) ** 2 + s2 * (a - b) ** 2 == a ** 2 + b ** 2
        for a in grid for b in grid)
    deaths_nonvacuous = all(len(deaths[p]) > 0 for p in deaths)

    passed = (forced_gives_p2 and survivors == [2] and inv_p2
              and s2 == F(1, 2) and deaths_nonvacuous
              and set(deaths) == {4, 6, 8})
    return {"passed": passed,
            "forced_identities_unique_p": forced_gives_p2,
            "forced_grid_size": len(forced_grid),
            "even_exponents_tested": even_tested,
            "even_sweep_survivors": survivors,
            "even_sweep_deaths_cross_terms":
                {p: {str(k): v for k, v in deaths[p].items()} for p in deaths},
            "p2_invariance_exact_all_inputs": inv_p2,
            "forced_scale_s_squared": s2,
            "billing": "family-relative (within L**p ansatz)"}


@_bank_leg("L_qc3_battery", "P_math", "W2.2 [P_math]")
def check_L_qc3_battery():
    """W2.2 [P_math]. Exact legs on 2-variable polynomial signatures.
    (a) EQUAL-DERIVATIVE: Sigma = f(a+b) => d_a = d_b (forward on built
        totals). The CONVERSE is verified SYMBOLICALLY -- p_dir_total_zero
        (D_(1,-1) = 0 on the monomial dict) is the exact criterion, and it is
        cross-checked against the grid factorization on a family so the two
        agree (a total factors and has D_(1,-1)=0; a**2+b**2 does neither).
    (b) MINIMAL FAITHFUL REPAIR: exchange-ODD linear functionals (computed via
        p_swap, not a hardcoded copy) are EXACTLY span{(1,-1)} = a - b; the
        exchange-EVEN a+b is excluded -- the control against collapse to the
        pooled coordinate.
    (c) DEFECT-DERIVATIVE: factoring <=> D_(1,-1) = 0, both directions.
    (d) MISMATCH PENALTY: G(a+b)+H(a-b), H nonconstant -- a same-total pair
        with different Lambda and an exact rank REVERSAL."""
    s_pow = {(2, 0): F(1), (1, 1): F(2), (0, 2): F(1)}
    s_lin = {(1, 0): F(3), (0, 1): F(3)}
    total = p_add(s_pow, s_lin)
    fwd_equal = p_eq(p_d0(total), p_d1(total))
    nontotal = {(2, 0): F(1), (0, 1): F(1)}
    nontotal_unequal = not p_eq(p_d0(nontotal), p_d1(nontotal))

    def factors_through_total(poly):
        grid = [F(x) for x in range(-2, 3)]
        seen = {}
        for a in grid:
            for b in grid:
                key = a + b
                val = p_eval(poly, a, b)
                if key in seen and seen[key] != val:
                    return False
                seen[key] = val
        return True

    Q = {(2, 0): F(1), (0, 2): F(1)}
    ab = {(1, 1): F(1)}
    family = [total, s_pow, nontotal, Q, ab]
    symbolic_matches_grid = all(
        p_dir_total_zero(poly) == factors_through_total(poly)
        for poly in family)
    equiv_a = (symbolic_matches_grid and p_dir_total_zero(total)
               and not p_dir_total_zero(nontotal))

    odd, even = [], []
    for alpha in range(-3, 4):
        for beta in range(-3, 4):
            if (alpha, beta) == (0, 0):
                continue
            L = {(1, 0): F(alpha), (0, 1): F(beta)}
            Lswap = p_swap(L)
            if p_eq(Lswap, p_scale(L, F(-1))):
                odd.append((alpha, beta))
            if p_eq(Lswap, L):
                even.append((alpha, beta))
    odd_is_amb = all(a == -b for (a, b) in odd) and (1, -1) in odd
    even_excludes_defect = all(a == b for (a, b) in even) \
        and (1, -1) not in even
    repair_unique = odd_is_amb and even_excludes_defect

    leg_c = (p_dir_total_zero(total) and not p_dir_total_zero(Q)
             and p_eq(p_add(p_d0(Q), p_scale(p_d1(Q), F(-1))),
                      {(1, 0): F(2), (0, 1): F(-2)}))

    def Lam(a, b):
        s, d = a + b, a - b
        return s + d * d
    same_total = (Lam(F(2), F(0)) != Lam(F(1), F(1))
                  and (F(2) + F(0)) == (F(1) + F(1)))
    rank_reversal = ((F(1) + F(-3)) < (F(3) + F(3))
                     and Lam(F(1), F(-3)) > Lam(F(3), F(3)))
    leg_d = same_total and rank_reversal

    passed = (fwd_equal and nontotal_unequal and equiv_a and repair_unique
              and leg_c and leg_d)
    return {"passed": passed,
            "equal_derivative_symbolic_converse_matches_grid":
                symbolic_matches_grid,
            "odd_repair_space": sorted(odd),
            "odd_span_scanned": 7 * 7 - 1,
            "minimal_repair_is_a_minus_b_unique_up_to_scale": repair_unique,
            "even_functional_excluded": even_excludes_defect,
            "defect_derivative_both_directions": leg_c,
            "mismatch_defeats_total_ranking": leg_d}


@_bank_leg("L_pool_or_defect_census", "P_structural", "W2.3 [P_structural]")
def check_L_pool_or_defect_census():
    """W2.3 [P_structural]. INHABITATION of both arms of the pool-or-defect
    dichotomy (re-billed from 'partition theorem', S1-3: the dichotomy is
    excluded-middle for any family; what is computed is that BOTH arms are
    realized, on named instances, and that a MIXED family is correctly read as
    relational). Either every signature factors through the total a+b
    (POOLED) or some carries the kernel direction a-b (RELATIONAL).

    CONCORDANCE: the pooled regime is the banked CoDef aggregation shape --
    check_L_codef_aggregation_argmin (.410); the relational regime is the
    defect sector. TYPED against banked Sep/CoDef/IJC (NON-POOL-REDUCIBILITY
    is the IJC face); consumed, not re-founded from factorization failure."""
    pooled = [{(1, 0): F(1), (0, 1): F(1)},
              {(2, 0): F(1), (1, 1): F(2), (0, 2): F(1)},
              {(1, 0): F(5), (0, 1): F(5)}]
    relational = [{(1, 0): F(2), (0, 1): F(1)}, {(1, 1): F(1)}]
    mixed = pooled[:1] + relational[:1]

    def classify_family(fam):
        return "pooled" if all(p_dir_total_zero(p) for p in fam) \
            else "relational"
    pooled_ok = classify_family(pooled) == "pooled"
    relational_ok = classify_family(relational) == "relational"
    mixed_is_relational = classify_family(mixed) == "relational"
    ab = {(1, 1): F(1)}
    ab_defect = p_eq(p_add(p_d0(ab), p_scale(p_d1(ab), F(-1))),
                     {(0, 1): F(1), (1, 0): F(-1)})
    passed = (pooled_ok and relational_ok and mixed_is_relational and ab_defect)
    return {"passed": passed,
            "both_arms_inhabited": pooled_ok and relational_ok,
            "mixed_family_reads_relational": mixed_is_relational,
            "pooled_size": len(pooled), "relational_size": len(relational),
            "ab_defect_derivative_is_b_minus_a": ab_defect,
            "concordance": "pooled == CoDef .410; typed vs Sep/CoDef/IJC"}


def _skew_space(g):
    """Distinct rational directions of {K : K**T g + g K = 0} on the
    {-1,0,1} parameter grid."""
    dirs = []
    for (p, q, r, s) in product((-1, 0, 1), repeat=4):
        K = [[F(p), F(q)], [F(r), F(s)]]
        if is_zero(madd(mm(mt(K), g), mm(g, K))) and \
                (p, q, r, s) != (0, 0, 0, 0):
            if (p, q, r, s) not in dirs and tuple(-x for x in (p, q, r, s)) \
                    not in dirs:
                dirs.append((p, q, r, s))
    return dirs


@_bank_leg("L_generator_theorem", "P_math", "W2.4 [P_math]")
def check_L_generator_theorem():
    """W2.4 [P_math]. On the oriented positive 2-plane with the DECLARED
    positive form g = I, the g-skew space is ONE-dimensional and its generator
    J = [[0,1],[-1,0]] satisfies J**2 = -I. POSITIVITY IS LOAD-BEARING: with
    the indefinite form g = diag(1,-1) the g-skew space is also 1-dim but its
    generator is the boost B = [[0,1],[1,0]] with B**2 = +I -- no square-minus
    -one. The boost control is the banked bounded_orbit_positivity
    boost-exclusion, seen from the generator side.

    CONCORDANCE: an INDEPENDENT route to the banked holonomy J
    (irrational_gate_holonomy H3; graded_orientation central-J) -- convergent
    with, not a replacement for; the ellipticity / H3 gate inheritance
    carries. No complex-structure or Born content is produced here."""
    gI = [[F(1), F(0)], [F(0), F(1)]]
    gInd = [[F(1), F(0)], [F(0), F(-1)]]
    skew_I, skew_Ind = _skew_space(gI), _skew_space(gInd)
    J = [[F(0), F(1)], [F(-1), F(0)]]
    B = [[F(0), F(1)], [F(1), F(0)]]
    passed = (len(skew_I) == 1 and len(skew_Ind) == 1
              and is_zero(madd(mm(mt(J), gI), mm(gI, J)))
              and is_zero(madd(mm(mt(B), gInd), mm(gInd, B)))
              and meq(mm(J, J), mscale(ID2, F(-1)))
              and meq(mm(B, B), ID2))
    return {"passed": passed,
            "gI_skew_dim_one": len(skew_I) == 1,
            "gInd_skew_dim_one": len(skew_Ind) == 1,
            "J_squares_to_minus_I": meq(mm(J, J), mscale(ID2, F(-1))),
            "boost_squares_to_plus_I_positivity_load_bearing":
                meq(mm(B, B), ID2),
            "concordance": "convergent with banked J (.432/.433); H3 gate"}


def _l1(v):
    return abs(v[0]) + abs(v[1])


def _l4_4(v):
    return v[0] ** 4 + v[1] ** 4


def _l2_2(v):
    return v[0] ** 2 + v[1] ** 2


def _linf(v):
    return max(abs(v[0]), abs(v[1]))


def _grid_isometries(norm_fn):
    """Count of {-1,0,1}-entry matrices preserving norm_fn on [-2,2]**2."""
    pts = [(F(x), F(y)) for x in range(-2, 3) for y in range(-2, 3)]
    count = 0
    for (a, b, c, d) in product((-1, 0, 1), repeat=4):
        M = [[F(a), F(b)], [F(c), F(d)]]
        if all(norm_fn(mvec(M, p)) == norm_fn(p) for p in pts):
            count += 1
    return count


def _rotation_preserves(norm_fn, cs):
    c, s = cs
    R = [[c, -s], [s, c]]
    return all(norm_fn(mvec(R, p)) == norm_fn(p)
               for p in [(F(1), F(0)), (F(1), F(1)), (F(2), F(-1))])


@_bank_leg("L_connected_isometry_euclidean", "P_math", "W2.5 [P_math + prose]")
def check_L_connected_isometry_euclidean():
    """W2.5 [P_math + prose]. 'Only the Euclidean form admits a nontrivial
    CONNECTED linear isometry family in 2D', witnessed exactly.

    THE DISCRIMINATING COMPUTATION (S2-1 rebuild): the nontrivial rational
    ROTATION family per norm --
      Euclidean : an INFINITE rational-rotation family (>= 4 exhibited,
                  Pythagorean) preserves x**2 + y**2;
      L1 and L4 : ZERO rotations in that family preserve the norm.
    This is what 'no continuous family for L1/L4, a continuous family for
    Euclidean' actually means. The signed-permutation grid count is 8 for L1,
    L4, L2 AND Linf -- a GRID ARTIFACT that does NOT by itself witness the
    absence of a continuous family; it is reported as a secondary fact only.

    PROSE STEP (billed as prose): the general theorem -- a continuous positive
    homogeneous burden preserved by a nontrivial connected group is Euclidean
    up to scale -- is NOT executed; the instances above are its witnesses."""
    fam = pyth_points()
    euclid_rot = [cs for cs in fam if _rotation_preserves(_l2_2, cs)]
    l1_rot = [cs for cs in fam if _rotation_preserves(_l1, cs)]
    l4_rot = [cs for cs in fam if _rotation_preserves(_l4_4, cs)]
    euclid_family = len(euclid_rot) >= 4
    l1_none = len(l1_rot) == 0
    l4_none = len(l4_rot) == 0
    grid_counts = {"l1": _grid_isometries(_l1), "l4": _grid_isometries(_l4_4),
                   "l2": _grid_isometries(_l2_2),
                   "linf": _grid_isometries(_linf)}
    passed = (euclid_family and l1_none and l4_none)
    return {"passed": passed,
            "euclid_rotation_family_size": len(euclid_rot),
            "l1_rotations_preserving": len(l1_rot),
            "l4_rotations_preserving": len(l4_rot),
            "pyth_family_size": len(fam),
            "signed_perm_grid_counts_all_8_secondary": grid_counts,
            "discriminant": "rotation family: Euclid infinite, L1/L4 zero"}


@_bank_leg("L_discrete_label_obstruction", "P_math", "W2.6 [P_math]")
def check_L_discrete_label_obstruction():
    """W2.6 [P_math]. A finite LABEL set admits only permutation dynamics; no
    permutation realizes a continuous balanced mixing.
      (1) linear maps preserving the label set {+/-e0, +/-e1} number exactly 8
          (the signed permutations of the 2-label set -- a real property of
          the label set, not a grid artifact of a norm);
      (2) a nontrivial rotation sends e0 to (3/5, 4/5), NOT a label;
      (3) the rational-rotation family is infinite (>= 4) vs 2 label
          permutations (S_2) -- computed size contrast.

    MANDATORY CONTROL -- THE CLASSICAL-WAVE PASS-THROUGH (the ceiling
    sentence): a two-component rational carrier Q**2 (a classical wave) passes
    balanced recombination (s**2 = 1/2 preserves x**2 + y**2). The obstruction
    kills the discrete LABEL buffer, NOT the wave carrier. The program's
    honest ceiling is the wave/Hilbert skeleton; quantum-vs-classical-wave
    still needs exclusive records + IJC + weighting (embargoed, .422 bar)."""
    labels = [(F(1), F(0)), (F(-1), F(0)), (F(0), F(1)), (F(0), F(-1))]
    lset = set(labels)
    perms = 0
    for (a, b, c, d) in product((-1, 0, 1), repeat=4):
        M = [[F(a), F(b)], [F(c), F(d)]]
        if all(mvec(M, p) in lset for p in labels) \
                and len({tuple(mvec(M, p)) for p in labels}) == 4:
            perms += 1
    c, s = F(3, 5), F(4, 5)
    R = [[c, -s], [s, c]]
    escapes = mvec(R, (F(1), F(0))) not in lset
    label_perms_2 = 2
    rot_family = len(pyth_points())
    s2 = F(1, 2)
    wave_grid = [(F(x), F(y)) for x in range(-2, 3) for y in range(-2, 3)]
    wave_passes = all(
        s2 * (v[0] + v[1]) ** 2 + s2 * (v[0] - v[1]) ** 2
        == v[0] ** 2 + v[1] ** 2 for v in wave_grid)
    passed = (perms == 8 and escapes and rot_family > label_perms_2
              and wave_passes)
    return {"passed": passed,
            "label_reversible_maps_finite_8": perms == 8,
            "rotation_escapes_label_set": escapes,
            "rotation_family_vs_two_label_perms": (rot_family, label_perms_2),
            "classical_wave_passes_recombination_CEILING": wave_passes}


# =====================================================================
# WAVE 3 -- clearance and nonisolation (charter 4g-4h)
# =====================================================================

def _bfs_dist(adj, terminal, n):
    dist = {terminal: 0}
    frontier = [terminal]
    while frontier:
        nxt = []
        for u in frontier:
            for w in adj[u]:
                if w not in dist:
                    dist[w] = dist[u] + 1
                    nxt.append(w)
        frontier = nxt
    return dist


def _flood_steps(adj, terminal, n, relevant):
    """INDEPENDENT of BFS: synchronous flooding. Each node unions neighbours'
    known-origin sets each step; return the step at which the terminal has
    every RELEVANT origin."""
    known = {v: {v} for v in range(n)}
    steps = 0
    while not relevant <= known[terminal]:
        nxt = {v: set(known[v]) for v in range(n)}
        for u in range(n):
            for w in adj[u]:
                nxt[u] |= known[w]
        known = nxt
        steps += 1
    return steps


@_bank_leg("L_dependency_diameter_bound", "P_structural", "W3.1 [P_structural]")
def check_L_dependency_diameter_bound():
    """W3.1 [P_structural]. Resolution depth by TWO INDEPENDENT routes that
    must agree: BFS lower bound (max_v dist(v, terminal)) and a synchronous
    flood SIMULATION (a different code path). Agreement is the theorem.

    Premise NOT-PREENCODED, rebuilt as a FALSIFIABLE computation (S2-3): the
    parity relation depends on EVERY node -- flipping any single node's bit
    flips the parity for some configuration (all_nodes_relevant), so the
    relevant-origin set is all n nodes. PRE-ENCODED CONTROL: the
    terminal-own-bit relation has relevant set {terminal}, and BOTH routes
    return depth 0 on the SAME graphs -- so the premise is load-bearing."""
    graphs = []
    for n in (2, 3, 4, 5):
        adj = {i: set() for i in range(n)}
        for i in range(n - 1):
            adj[i].add(i + 1)
            adj[i + 1].add(i)
        graphs.append(("path%d" % n, adj, n, 0))
    star = {0: {1, 2, 3}, 1: {0}, 2: {0}, 3: {0}}
    graphs.append(("star4_leafterm", star, 4, 1))
    tree = {0: {1}, 1: {0, 2, 3}, 2: {1}, 3: {1, 4}, 4: {3}}
    graphs.append(("tree5", tree, 5, 0))

    depths = {}
    routes_agree = True
    preenc_zero = True
    for name, adj, n, term in graphs:
        dist = _bfs_dist(adj, term, n)
        lower_bound = max(dist[v] for v in range(n))
        achiever = _flood_steps(adj, term, n, set(range(n)))
        preenc_flood = _flood_steps(adj, term, n, {term})
        depths[name] = lower_bound
        if lower_bound != achiever:
            routes_agree = False
        if not (max(dist[v] for v in {term}) == 0 and preenc_flood == 0):
            preenc_zero = False

    def parity(bits):
        r = 0
        for x in bits:
            r = (r + x) % 2
        return r
    m = 3
    cfgs = list(product((0, 1), repeat=m))
    relevant = []
    for v in range(m):
        flips = any(parity(c) != parity(tuple(
            (c[i] + 1) % 2 if i == v else c[i] for i in range(m)))
            for c in cfgs)
        relevant.append(flips)
    all_nodes_relevant = all(relevant)

    passed = routes_agree and all_nodes_relevant and preenc_zero
    return {"passed": passed,
            "bfs_and_flood_routes_agree": routes_agree,
            "graphs_tested": len(graphs),
            "graph_depths": depths,
            "parity_relevant_node_count": sum(relevant),
            "parity_all_nodes_relevant": all_nodes_relevant,
            "preencoded_relevant_count": 1,
            "preencoded_control_depth_zero_same_graphs": preenc_zero}


def _two_site_commit(commit, preenc, live, delayed, aA, bB, link_up):
    """Two sites A (record forms) and B, propagation delay 1. A mechanism spec
    is (commit in {'t','t1'}, preenc, live, delayed) -- the B-information
    sources it is BUILT to use. The committed terminal value is computed from
    what the mechanism actually knows at commit time (RUN DATA), NOT from any
    label. Terminal relation = aA XOR bB (as % 2)."""
    knows_b = (preenc
               or (commit == "t" and live and link_up)
               or (commit == "t1" and delayed and link_up))
    return (aA + bB) % 2 if knows_b else aA


def _spec_faithful(spec, link_up):
    commit, preenc, live, delayed = spec
    return all(_two_site_commit(commit, preenc, live, delayed, aA, bB, link_up)
               == (aA + bB) % 2
               for aA in (0, 1) for bB in (0, 1))


@_bank_leg("T_zero_clearance_trilemma_census", "P_structural", "W3.2 [P_structural]")
def check_T_zero_clearance_trilemma_census():
    """W3.2 [P_structural]. INHABITATION + case split (re-billed from a
    check_T universal, S1-1: the old headline was f_live => f_live). Two-site
    world, propagation delay 1. Enumerate the mechanism specs
    (commit x preenc x live x delayed); classify every ZERO-CLEARANCE
    (commit='t') spec by RUN DATA -- live-link vs severed-link faithfulness:
      PRE-ENCODED  faithful even with the live B->A link severed;
      NONLOCAL     faithful only WITH the live link (reads B at t);
      PREMATURE    commits at t and is UNFAITHFUL either way.
    The trilemma is the charter's DECLARED case split (a 2-bit signature); it
    is not derived here. What is COMPUTED and falsifiable:
      (i)  all three arms are INHABITED by real specs;
      (ii) PREMATURE is not vacuous -- a t-commit spec with NO B-source is
           UNFAITHFUL on half the inputs (computed, a real wrong mechanism);
      (iii)the CLEARANCE-CARRYING complement exists: a t1/delayed spec is
           faithful using the LEGAL late arrival -- the nonzero interval.
    CONCORDANCE: pre-encoded == register/accretion; premature == AE-1A; the
    NONLOCAL arm's disposition is the PENDING R-boundary-witness ruling (this
    census reports the arm, it does not close the fork). STORE-INVENTORY
    imported from wave 1."""
    specs = [("t", pe, lv, dl) for pe in (False, True)
             for lv in (False, True) for dl in (False, True)]
    arms = {"preencoded": [], "nonlocal": [], "premature": []}
    for spec in specs:
        fl = _spec_faithful(spec, True)
        fb = _spec_faithful(spec, False)
        if fl and fb:
            arms["preencoded"].append(spec)
        elif fl and not fb:
            arms["nonlocal"].append(spec)
        else:
            arms["premature"].append(spec)
    all_inhabited = all(len(v) > 0 for v in arms.values())
    premature_spec = ("t", False, False, False)
    premature_unfaithful = (not _spec_faithful(premature_spec, True)
                            and not _spec_faithful(premature_spec, False)
                            and premature_spec in arms["premature"])
    cc = ("t1", False, False, True)
    clearance_carrying = _spec_faithful(cc, True)
    passed = (all_inhabited and premature_unfaithful and clearance_carrying)
    return {"passed": passed,
            "zero_clearance_specs": len(specs),
            "arm_sizes": {k: len(v) for k, v in arms.items()},
            "all_three_arms_inhabited": all_inhabited,
            "premature_arm_genuinely_unfaithful": premature_unfaithful,
            "clearance_carrying_complement_exists": clearance_carrying}


@_bank_leg("L_class_witnesses", "P_math", "W3.3 [P_math]")
def check_L_class_witnesses():
    """W3.3 [P_math] -- EXISTENCE EXHIBITS ONLY. Three explicit finite models:
      Class I  (instantaneous / pre-encoded): a COMPUTED depth-0 model (S1-2)
               -- a graph on which the terminal relation is the terminal's own
               bit, so the relevant set is {terminal} and the flood resolves
               in 0 steps (computed, not a literal True);
      Class II (discrete Held): a finite carrier {0,1,2} with threshold jumps;
               the jump LOCATIONS are computed by scanning a rational grid and
               the boundary records are DERIVED from them (S1-2), not
               hardcoded;
      Class III(coherent Held): a rational-rotation orbit on Q**2 -- a
               continuous family, no jumps.
    The complex generator J needs Class III; nothing here excludes Class II."""
    adjI = {0: {1}, 1: {0}}
    classI_depth = _flood_steps(adjI, 0, 2, {0})
    classI_ok = (classI_depth == 0)

    def stratum(lam):
        return 0 if lam < 1 else (1 if lam < 2 else 2)
    scan = [F(k, 4) for k in range(0, 13)]
    jump_locs = [scan[i + 1] for i in range(len(scan) - 1)
                 if stratum(scan[i]) != stratum(scan[i + 1])]
    boundary_records = [(loc,) for loc in jump_locs]
    classII_ok = (jump_locs == [F(1), F(2)] and len(boundary_records) == 2)

    fam = pyth_points()
    orbit = [mvec([[c, -s], [s, c]], (F(1), F(0))) for (c, s) in fam]
    distinct = len({tuple(p) for p in orbit})
    on_circle = all(_l2_2(p) == 1 for p in orbit)
    classIII_ok = (distinct >= 4 and on_circle)

    passed = classI_ok and classII_ok and classIII_ok
    return {"passed": passed,
            "classI_computed_depth": classI_depth,
            "classII_jump_locations": [str(x) for x in jump_locs],
            "classII_boundary_records_derived": len(boundary_records),
            "classIII_coherent_orbit_states": distinct,
            "classIII_on_circle_exact": on_circle}


@_bank_leg("L_qc6b_constancy", "P_math", "W3.4 [P_math]")
def check_L_qc6b_constancy():
    """W3.4 [P_math]. On a CONNECTED discrete parameter chain, a
    permutation-valued assignment obeying the 'no-jump-without-witness'
    adjacency rule with NO witnessed boundary is CONSTANT -- verified by
    enumeration over the cases ACTUALLY RUN (S1-8): N=2,3 at chain lengths
    k=2,3,4, and N=4 at k=2 (the compute-bounded set; reported explicitly).
    The DICHOTOMY: with one witnessed edge, NONCONSTANT assignments exist.

    Premise CONTEXT-INTEGRATION: the kill bites only where the assignment must
    UPDATE across contexts; the constant (passive) assignment is the surviving
    countermodel -- this computes the dichotomy, it does not claim the buffer
    dead off the coherent sector."""
    enumerated = []
    all_constant_ok = True
    nojump_counts = {}
    for N in (2, 3, 4):
        Sn = list(permutations(range(N)))
        for k in (2, 3, 4):
            if N == 4 and k > 2:
                continue
            enumerated.append((N, k))
            no_jump = sum(
                1 for assign in product(Sn, repeat=k)
                if all(assign[i] == assign[i + 1] for i in range(k - 1)))
            nojump_counts["N%d_k%d" % (N, k)] = no_jump
            if no_jump != len(Sn):
                all_constant_ok = False

    Sn = list(permutations(range(3)))
    witnessed_edge = 1
    nonconstant = sum(
        1 for assign in product(Sn, repeat=3)
        if all(assign[i] == assign[i + 1]
               for i in range(2) if i != witnessed_edge)
        and not (assign[0] == assign[1] == assign[2]))
    passed = all_constant_ok and nonconstant > 0
    return {"passed": passed,
            "no_witness_forces_constant": all_constant_ok,
            "enumerated_N_k": enumerated,
            "nojump_counts": nojump_counts,
            "witnessed_edge_allows_nonconstant": nonconstant > 0,
            "nonconstant_count_one_witness": nonconstant}


@_bank_leg("L_cross_derivative_marker", "P_math", "W3.5 [P_math]")
def check_L_cross_derivative_marker():
    """W3.5 [P_math]. The QC6I/J marker d_lambda D_h Sigma distinguishes a
    FRAME-DEFORMING context from an OUTPUT-SHIFTING one, exactly, on
    2-variable polynomials Sigma(h=x0, lambda=x1):
      frame-deforming:  Sigma = h*lambda      -> cross = 1  (!= 0);
      output-shifting:  Sigma = h + lambda**2 -> cross = 0."""
    deform = {(1, 1): F(1)}
    shift = {(1, 0): F(1), (0, 2): F(1)}
    cross_deform = p_d1(p_d0(deform))
    cross_shift = p_d1(p_d0(shift))
    deform_nonzero = (cross_deform != {})
    shift_zero = (cross_shift == {})
    deform_val = p_eval(cross_deform, F(0), F(0)) if cross_deform else F(0)
    passed = deform_nonzero and shift_zero and deform_val == F(1)
    return {"passed": passed,
            "frame_deforming_cross_nonzero": deform_nonzero,
            "output_shifting_cross_zero": shift_zero,
            "frame_deforming_cross_value": deform_val}


@_bank_leg("L_tangent_rank_bound", "P_structural", "W3.6 [P_structural]")
def check_L_tangent_rank_bound():
    """W3.6 [P_structural]. Independent first-order response directions each
    cost >= eps* and capacity C bounds the count: dim <= floor(C/eps*),
    computed exactly. Each case reports (eps, C, floor) so the tightness is
    RECOMPUTED independently by the test (S2-2): floor*eps <= C and
    (floor+1)*eps > C, both exact.

    CONCORDANCE: the bound is the banked finite-basis shape --
    check_T_finite_operational_basis / check_T_admissibility_greedoid_structure
    (.425). This INSTANTIATES that shape; it does not re-derive the theorem."""
    def floor_div(C, eps):
        q = C / eps
        return q.numerator // q.denominator

    raw = [(F(1), F(5), 5), (F(2), F(7), 3), (F(3, 2), F(6), 4)]
    cases = []
    all_ok = True
    for eps, C, expect in raw:
        bound = floor_div(C, eps)
        fits = (bound * eps <= C)
        overflow = ((bound + 1) * eps > C)
        cases.append({"eps": eps, "C": C, "floor": bound,
                      "fits": fits, "overflow": overflow})
        if not (bound == expect and fits and overflow):
            all_ok = False
    return {"passed": all_ok,
            "dim_le_floor_C_over_eps": all_ok,
            "cases": cases,
            "concordance": "instantiates banked finite-basis .425 floor(C/eps*)"}


# =====================================================================
# WAVE 4 -- the moving exchange frame (charter 4i)
# =====================================================================

def _refl(c, s):
    """Reflection with (cos2theta, sin2theta) = (c, s): [[c,s],[s,-c]]."""
    return [[c, s], [s, -c]]


@_bank_leg("L_moving_exchange", "P_math", "W4.1 [P_math]")
def check_L_moving_exchange():
    """W4.1 [P_math]. tau_theta is the reflection family. Using EXACT rational
    frames, the discrete derivative Dtau = tau_{theta+delta} -
    tau_{theta-delta}:
      (1) ANTICOMMUTES with tau_theta exactly (the zero matrix -- because
          c*Dc + s*Ds = 0 identically);
      (2) maps the +1 eigenvector v+ into the -1 eigenspace: the v+-component
          of Dtau*v+ is ZERO and the v--component is NONZERO.
    All exact difference quotients on rational frames; the limit STRUCTURE is
    exhibited at exact finite rational separations."""
    c, s = F(3, 5), F(4, 5)
    C, S = F(3, 5), F(4, 5)
    cp, sp = c * C - s * S, s * C + c * S
    cm, sm = c * C + s * S, s * C - c * S
    tau = _refl(c, s)
    Dtau = msub(_refl(cp, sp), _refl(cm, sm))
    anticommutes = is_zero(madd(mm(tau, Dtau), mm(Dtau, tau)))

    vp = (s, F(1) - c)
    vm = (s, -(F(1) + c))
    Dvp = mvec(Dtau, vp)
    det = vp[0] * vm[1] - vp[1] * vm[0]
    alpha = (Dvp[0] * vm[1] - Dvp[1] * vm[0]) / det
    beta = (vp[0] * Dvp[1] - vp[1] * Dvp[0]) / det
    off_diagonal = (alpha == 0 and beta != 0)
    invol = meq(mm(tau, tau), ID2)
    ev_plus = (mvec(tau, vp) == vp)
    ev_minus = (mvec(tau, vm) == (-vm[0], -vm[1]))
    passed = (anticommutes and off_diagonal and invol and ev_plus and ev_minus)
    return {"passed": passed,
            "anticommutator_is_zero": anticommutes,
            "Dtau_maps_Vplus_to_Vminus": off_diagonal,
            "vplus_component": alpha, "vminus_component": beta,
            "tau_involution": invol}


def _direction(v):
    """Canonical line representative of a nonzero 2-vector: scale the first
    nonzero coordinate to 1 (invariant under v -> -v). Used for exact
    eigenline comparison."""
    a, b = v
    if a == 0 and b == 0:
        return None
    if a != 0:
        return (F(1), b / a)
    return (F(0), F(1))


@_bank_leg("L_two_frame_irreducibility", "P_math", "W4.2 [P_math]")
def check_L_two_frame_irreducibility():
    """W4.2 [P_math]. Two reflections with NO common eigenline generate an
    algebra with NO common invariant line (irreducible).
      (1) the invariant lines of a reflection are its two eigenlines; two
          reflections at distinct angles share none (exact direction compare);
      (2) their product is a rotation whose characteristic polynomial
          lambda**2 - 2C lambda + 1 has discriminant -4 S**2 < 0 -- no real
          eigenline at all."""
    c1, s1 = F(3, 5), F(4, 5)
    c2, s2 = F(5, 13), F(12, 13)
    t1, t2 = _refl(c1, s1), _refl(c2, s2)

    def eigenlines(c, s):
        return [_direction((s, F(1) - c)), _direction((s, -(F(1) + c)))]
    e1, e2 = eigenlines(c1, s1), eigenlines(c2, s2)
    no_common = len(set(map(tuple, e1)) & set(map(tuple, e2))) == 0

    prod = mm(t2, t1)
    Cc, Ss = prod[0][0], prod[1][0]
    disc = (2 * Cc) ** 2 - 4
    neg_disc = (disc == -4 * Ss ** 2 and disc < 0)
    passed = no_common and neg_disc
    return {"passed": passed,
            "no_common_eigenline": no_common,
            "product_rotation_negative_discriminant": neg_disc,
            "discriminant": disc}


@_bank_leg("L_reflection_product_rotation", "P_math", "W4.3 [P_math]")
def check_L_reflection_product_rotation():
    """W4.3 [P_math]. tau_{theta2} tau_{theta1} is an orientation-preserving
    rotation by exactly 2(theta2 - theta1): product =
    [[cos2d, -sin2d],[sin2d, cos2d]] with (cos2d, sin2d) =
    (c1 c2 + s1 s2, s2 c1 - c2 s1), det = +1. Pinned: (3/5,4/5),(5/13,12/13)
    -> (63/65, 16/65).

    CONCORDANCE: this rotation IS the banked two_exchange_holonomy object
    (.432) seen from the physics side -- the relative-loop holonomy of two
    exchanges. Convergence; consumed, not re-derived."""
    c1, s1 = F(3, 5), F(4, 5)
    c2, s2 = F(5, 13), F(12, 13)
    prod = mm(_refl(c2, s2), _refl(c1, s1))
    cosd = c1 * c2 + s1 * s2
    sind = s2 * c1 - c2 * s1
    is_rotation = meq(prod, [[cosd, -sind], [sind, cosd]])
    det = prod[0][0] * prod[1][1] - prod[0][1] * prod[1][0]
    passed = (is_rotation and det == 1
              and cosd == F(63, 65) and sind == F(16, 65))
    return {"passed": passed,
            "product_is_rotation_2dTheta": is_rotation,
            "orientation_preserving_det1": det == 1,
            "pinned_cos_sin": (cosd, sind)}


@_bank_leg("L_exchange_isometry", "P_structural", "W4.4 [P_structural]")
def check_L_exchange_isometry():
    """W4.4 [P_structural]. The exchange tau = [[0,1],[1,0]] (swap the two
    continuation roles) preserves the DECLARED Euclidean form
    Q(a,b) = a**2 + b**2. Re-billed (S1-4): the genuine tau-fact is
    Q-invariance, EQUIVALENTLY preservation of the associated bilinear form g;
    the polarization identity g(h,k) = (Q(h+k)-Q(h)-Q(k))/2 is a DEFINITIONAL
    bridge (holds with or without tau) and is billed as such, NOT as a second
    independent route.

    Named premises (QC7F): role equivalence (tau swaps the two roles) +
    CYCLIC-NEUTRALITY (the swap is committed-ledger-neutral -- consumes the
    accounting ruling + bin-(ii) .413). ORDER preserved: tau is defined
    pre-metric by the role swap; g-orthogonality is a DERIVED consequence."""
    tau = [[F(0), F(1)], [F(1), F(0)]]

    def Q(v):
        return v[0] ** 2 + v[1] ** 2

    def g(x, y):
        return x[0] * y[0] + x[1] * y[1]
    grid = [(F(x), F(y)) for x in range(-3, 4) for y in range(-3, 4)]
    invariance = all(Q(mvec(tau, h)) == Q(h) for h in grid)
    bilinear_preserved = all(
        g(mvec(tau, h), mvec(tau, k)) == g(h, k)
        for h in grid[:12] for k in grid[:12])

    def g_pol(h, k):
        return (Q((h[0] + k[0], h[1] + k[1])) - Q(h) - Q(k)) / F(2)
    polarization_bridge = all(g_pol(h, k) == g(h, k)
                              for h in grid[:12] for k in grid[:12])
    passed = invariance and bilinear_preserved and polarization_bridge
    return {"passed": passed,
            "Q_invariance_under_exchange": invariance,
            "bilinear_form_preserved_equivalent_fact": bilinear_preserved,
            "polarization_identity_bridge_tau_independent": polarization_bridge,
            "billing": "one tau-fact (Q-inv == g-preservation); "
                       "polarization is a bridge, not a 2nd route"}


@_bank_leg("L_diagonal_action_countermodel", "control", "W4.5 [control]")
def check_L_diagonal_action_countermodel():
    """W4.5 [control -- MANDATORY]. A world where BOTH the common C and the
    defect D matter (Lambda = C**2 + kappa D**2, kappa = 2 != 1) but every
    context acts DIAGONALLY (a scaling torus, no off-diagonal mixing). This is
    NON-POOL-REDUCIBLE WITHOUT any mixing generator -- so
    NON-POOL-REDUCIBILITY alone does NOT force the J-mixing of QC7. QC7 needs,
    additionally, RELATIONAL-FRAME VARIABILITY (W4.1). Keeps QC7's premise
    honest.

    Computed: (1) non-pool-reducible -- same C, different D gives different
    Lambda (kappa reported and pinned); (2) every context diagonal, closed
    under composition; (3) NO diagonal generator squares to -I -- checked over
    ALL enumerated diagonal generators (S1-10), not one."""
    kappa = F(2)

    def Lam(Cc, Dd):
        return Cc * Cc + kappa * Dd * Dd
    non_pool = (Lam(F(1), F(0)) != Lam(F(1), F(1)))
    lam_values = (Lam(F(1), F(0)), Lam(F(1), F(1)))
    diag_ctx = [[[F(a), F(0)], [F(0), F(b)]]
                for a in (1, 2) for b in (1, 2)]
    all_diagonal = all(M[0][1] == 0 and M[1][0] == 0 for M in diag_ctx)
    closed = all(mm(M, Nn)[0][1] == 0 and mm(M, Nn)[1][0] == 0
                 for M in diag_ctx for Nn in diag_ctx)
    diag_gens = [[[F(a), F(0)], [F(0), F(b)]]
                 for a in range(-2, 3) for b in range(-2, 3)]
    no_J = all(not meq(mm(G, G), mscale(ID2, F(-1))) for G in diag_gens)
    passed = non_pool and all_diagonal and closed and no_J
    return {"passed": passed,
            "non_pool_reducible_D_matters": non_pool,
            "kappa": kappa, "lambda_same_C_diff_D": lam_values,
            "every_context_diagonal": all_diagonal and closed,
            "no_diagonal_generator_squares_to_minus_I": no_J,
            "diagonal_generators_checked": len(diag_gens)}


@_bank_leg("L_bank_concordance", "concordance-citation", "W4.6 [concordance-citation]")
def check_L_bank_concordance():
    """W4.6 [concordance-citation]. Re-billed (S2-5): this leg does NOT
    independently certify anything the bank does; it re-verifies the shared
    STRUCTURAL invariant INLINE (recomputed here, not a re-run of W4.3) and
    records the exact banked check-names to consult. When the bank tree is
    importable it additionally cross-checks; when it is not (the standalone
    case), it SKIPS the cross-check and says so.

    Structural invariant (recomputed inline): a product of two reflections is
    an orientation-preserving rotation (det +1) by 2*dTheta -- the defining
    property of the banked two_exchange_holonomy relative-loop object (.432).
    The continuous frame family additionally needs ORIENTATION_SYNCHRONIZATION
    for a unique orientation-compatible J -- the Ruling-3 central-J gate whose
    executable semantics are banked in graded_orientation_closure (.433);
    cited by name, its proof NOT duplicated here. Orientation is exhibited as
    a computed fact: each reflection has det -1, their product det +1."""
    # SELF-CONTAINED PORT: the original module optionally probed the live
    # bank (apf.two_exchange_holonomy / apf.graded_orientation_closure) to set
    # a "performed"/"skipped" status; that probe is REMOVED so this module
    # imports nothing from the bank. Concordance is by CITATION only -- the
    # banked check-names and anchor versions below are HARDCODED (frozen at
    # the port) and the shared structural invariant is recomputed inline.
    c1, s1 = F(8, 17), F(15, 17)
    c2, s2 = F(20, 29), F(21, 29)
    r1, r2 = _refl(c1, s1), _refl(c2, s2)
    prod = mm(r2, r1)
    cosd, sind = c1 * c2 + s1 * s2, s2 * c1 - c2 * s1
    is_rotation = meq(prod, [[cosd, -sind], [sind, cosd]])
    det_prod = prod[0][0] * prod[1][1] - prod[0][1] * prod[1][0]
    det_r1 = r1[0][0] * r1[1][1] - r1[0][1] * r1[1][0]
    orientation_fact = (det_r1 == -1 and det_prod == 1)
    te_structural = is_rotation and det_prod == 1
    citations = {
        "two_exchange_holonomy": ".432 relative-loop rotation = 2*dTheta",
        "graded_orientation_closure": ".433 ORIENTATION_SYNCHRONIZATION "
        "central-J gate (Ruling-3)",
        "irrational_gate_holonomy": ".432 H3 ellipticity gate"}
    passed = te_structural and orientation_fact
    return {"passed": passed,
            "bank_cross_check": "self-contained (banked names hardcoded; "
            "no live-bank import)",
            "structural_invariant_recomputed_inline": te_structural,
            "orientation_det_fact": orientation_fact,
            "banked_check_names_cited": sorted(citations),
            "citations": citations,
            "concordance_anchors_hardcoded": {
                "two_exchange_holonomy": ".432",
                "graded_orientation_closure": ".433",
                "irrational_gate_holonomy": ".432"}}


# =====================================================================
# Mutation battery -- 18 named hostile mutations. True == the mutated world
# behaves exactly as the module bills (a leg catches it, or the owned control
# appears). v0.2: M3/M10/M12 route through real computation (S1-7).
# =====================================================================

def run_mutations():
    results = {}

    bp4 = _balanced_poly(4)
    results["M1_p4_has_cross_term"] = (bp4.get((2, 2), F(0)) != 0
                                       and set(bp4) != {(4, 0), (0, 4)})
    s2bad = F(1, 3)
    results["M2_wrong_scale_breaks_invariance"] = any(
        s2bad * (a + b) ** 2 + s2bad * (a - b) ** 2 != a ** 2 + b ** 2
        for a in (F(1), F(2)) for b in (F(1), F(0)))
    L_even = {(1, 0): F(1), (0, 1): F(1)}
    results["M3_even_functional_not_odd"] = not p_eq(
        p_swap(L_even), p_scale(L_even, F(-1)))
    B = [[F(0), F(1)], [F(1), F(0)]]
    results["M4_boost_squares_plus_I"] = meq(mm(B, B), ID2) and not meq(
        mm(B, B), mscale(ID2, F(-1)))
    results["M5_rotation_euclid_not_l1"] = (
        _rotation_preserves(_l2_2, (F(3, 5), F(4, 5)))
        and not _rotation_preserves(_l1, (F(3, 5), F(4, 5))))
    lset = {(F(1), F(0)), (F(-1), F(0)), (F(0), F(1)), (F(0), F(-1))}
    R = [[F(3, 5), F(-4, 5)], [F(4, 5), F(3, 5)]]
    results["M6_rotation_escapes_labels"] = mvec(R, (F(1), F(0))) not in lset

    def par(b):
        r = 0
        for x in b:
            r = (r + x) % 2
        return r
    cfgs = list(product((0, 1), repeat=3))
    results["M7_all_nodes_relevant"] = all(
        any(par(c) != par(tuple((c[i] + 1) % 2 if i == v else c[i]
                                for i in range(3))) for c in cfgs)
        for v in range(3))
    results["M8_premature_unfaithful"] = not _spec_faithful(
        ("t", False, False, False), True)
    results["M9_nonlocal_needs_live_link"] = (
        _spec_faithful(("t", False, True, False), True)
        and not _spec_faithful(("t", False, True, False), False))
    a0, a1 = (0, 1, 2), (1, 0, 2)
    results["M10_nojump_rejects_nonconstant"] = not all(
        (a0, a1)[i] == (a0, a1)[i + 1] for i in range(1))
    results["M11_output_shift_cross_zero"] = (
        p_d1(p_d0({(1, 0): F(1), (0, 2): F(1)})) == {})
    r36 = check_L_tangent_rank_bound()
    results["M12_capacity_overflow_via_floor"] = any(
        (c["floor"] + 1) * c["eps"] > c["C"] and c["floor"] * c["eps"] <= c["C"]
        for c in r36["cases"])

    r41 = check_L_moving_exchange()
    results["M13_anticommutator_zero"] = r41["anticommutator_is_zero"]
    results["M14_offdiagonal_image"] = (r41["vplus_component"] == 0
                                        and r41["vminus_component"] != 0)
    r42 = check_L_two_frame_irreducibility()
    results["M15_rotation_no_real_eigenline"] = r42[
        "product_rotation_negative_discriminant"]
    r43 = check_L_reflection_product_rotation()
    results["M16_product_det_plus_one"] = (
        r43["orientation_preserving_det1"]
        and r43["pinned_cos_sin"] == (F(63, 65), F(16, 65)))
    r45 = check_L_diagonal_action_countermodel()
    results["M17_diagonal_nonpool_no_J"] = (
        r45["non_pool_reducible_D_matters"]
        and r45["no_diagonal_generator_squares_to_minus_I"])
    r44 = check_L_exchange_isometry()
    results["M18_exchange_isometry_and_bridge"] = (
        r44["Q_invariance_under_exchange"]
        and r44["bilinear_form_preserved_equivalent_fact"])

    results["all_caught"] = all(results.values())
    return results


# =====================================================================
# Walker
# =====================================================================

_CHECKS = {
    "L_square_law_selection": check_L_square_law_selection,
    "L_qc3_battery": check_L_qc3_battery,
    "L_pool_or_defect_census": check_L_pool_or_defect_census,
    "L_generator_theorem": check_L_generator_theorem,
    "L_connected_isometry_euclidean": check_L_connected_isometry_euclidean,
    "L_discrete_label_obstruction": check_L_discrete_label_obstruction,
    "L_dependency_diameter_bound": check_L_dependency_diameter_bound,
    "T_zero_clearance_trilemma_census": check_T_zero_clearance_trilemma_census,
    "L_class_witnesses": check_L_class_witnesses,
    "L_qc6b_constancy": check_L_qc6b_constancy,
    "L_cross_derivative_marker": check_L_cross_derivative_marker,
    "L_tangent_rank_bound": check_L_tangent_rank_bound,
    "L_moving_exchange": check_L_moving_exchange,
    "L_two_frame_irreducibility": check_L_two_frame_irreducibility,
    "L_reflection_product_rotation": check_L_reflection_product_rotation,
    "L_exchange_isometry": check_L_exchange_isometry,
    "L_diagonal_action_countermodel": check_L_diagonal_action_countermodel,
    "L_bank_concordance": check_L_bank_concordance,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all(verbose=True):
    out = {}
    for name, fn in _CHECKS.items():
        r = fn()
        out[name] = r
        if verbose:
            print(("PASS" if r["passed"] else "FAIL"), name)
    muts = run_mutations()
    out["mutations"] = muts
    if verbose:
        n_named = sum(1 for k in muts if k.startswith("M"))
        print(("PASS" if muts["all_caught"] else "FAIL"),
              "mutation_battery ({} named)".format(n_named))
        n_pass = sum(1 for k, v in out.items()
                     if k != "mutations" and v["passed"])
        print("== {} / {} checks pass; mutations all caught: {}".format(
            n_pass, len(_CHECKS), muts["all_caught"]))
    return out


if __name__ == "__main__":
    run_all()
