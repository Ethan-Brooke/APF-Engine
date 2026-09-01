"""The degree of an extension of the banked enforcement cost is free.

WHAT THIS ADDS, AGAINST THE PRIOR ART (read this first).

The bank names QUADRATIC_LEDGER as a physical posit (H4 in
apf/_held_holonomy_contract.py) and relocates its EXISTENCE half to a named
reading at v24.3.431 (check_L_bounded_orbit_positivity).  THAT POSIT LIVES ON A
DIFFERENT CARRIER: it is the existence of an invariant positive-definite form on
the admissible-state space, with Q2_LEDGER_ADJOINT and REVERSAL_IS_INVERSE
attached, and bounded_orbit_positivity explicitly declines to identify the form
it produces with any physical counting metric.  The configuration cost of
symmetry_cost_floor was never a candidate for it.  So the "neither supplies nor
refutes" recorded below is true for a reason PRIOR TO AND STRONGER THAN the
degree argument -- different spaces -- and the degree result is not the operative
reason.  It is recorded because a 2026-07-28 candidate module reasoned as though
it were.

That candidate claimed the banked ledger is 1-homogeneous and therefore not the
quadratic object the sandwich construction requires.  Two blinded auditors killed
it: it tested homogeneity in eps*, the unit PRICE, holding the configuration
fixed, and a cost that is literally |S|^2 passes that battery including its
explicit "not quadratic" guard.  This module banks the two statements that
survived that kill, at their honest grades, and nothing else.

  (1) THE DEGREE IS FREE.  The banked cost is a finitely additive set function on
      subsets of a finite pair-set -- additivity EXERCISED here on disjoint
      unions across the full cube, not assumed.  Its per-pair weights are read
      OFF THE BANKED CALLEE by singleton probe, never hardcoded.  For every
      d >= 1 the map F_d(v) = eps* sum_p w_p v_p^d then reproduces the banked
      cost at EVERY point of the cube at n = 4 and n = 5 (64 and 1024 subsets,
      both modes), because indicator entries are 0 or 1 and both 1^d = 1 and
      0^d = 0 for d >= 1.  The F_d are distinct off the cube and each is
      homogeneous of degree EXACTLY d.  So the banked ledger neither supplies nor
      refutes a degree: degree is a property of a chosen extension, and on the
      banked domain it is not a well-formed predicate at all.  COROLLARY,
      executed: the eps*-scaling test is provably BLIND, returning one verdict
      across every degree -- which is why the killed candidate's inference was a
      non sequitur.

  (2) THE LINEAR EXTENSION SPECIFICALLY IS NOT A QUADRATIC FORM.  L(v) =
      eps* sum_p w_p v_p satisfies L(2v) = 2L(v), a quadratic form satisfies
      Q(2v) = 4Q(v), so L quadratic forces L == 0.  What excludes L == 0 is
      NON-VANISHING, not positivity: the verdict is unchanged at eps* = -7/5,
      computed, and only eps* = 0 flips it.  The degree route is used rather than
      the parallelogram route because the parallelogram defect of an additive L
      is exactly -2L(b) and therefore vanishes on ker L: the parallelogram test
      reports "quadratic-like" for a strictly linear map, computed.

THE TWO CHECKS POINT IN OPPOSITE DIRECTIONS ON PURPOSE, and (1) is the stronger.
(2) is about one chosen extension on R^P, a space the banked cost does not
inhabit; (1) is about the banked object.  Reading (2) as "the banked ledger is
not quadratic" is the error (1) forbids, and the fence is executed in code.

NEITHER RESULT DISCHARGES ANYTHING.  P1 stays open.  QUADRATIC_LEDGER stays a
posit on its own carrier, untouched.

============================================================================
STATEMENTS

check_L_ledger_extension_degree_free
(tier 3, [P_math | the 1^d = 1 kernel is pure mathematics; the statement ABOUT
the banked ledger inherits symmetry_cost_floor's cost model, which that module
grades [P_structural] and calls a modelling choice]).

  THE CALLEE IS THE BANKED ONE: apf.symmetry_cost_floor.config_cost is imported
  and CALLED, fail-closed, with its __module__ asserted, so a vendored
  reimplementation cannot stand in even when every number agrees.

  THE WEIGHTS ARE READ, NOT ASSUMED: w_p is recovered by probing the banked
  callee on the singleton {p} at unit price, in BOTH modes.  Nothing in this
  module hardcodes a weight.  (An earlier cut hardcoded 1 and asserted a pin
  whose null space was 2-dimensional at n = 4 and 5-dimensional at n = 5; a
  blinded auditor exhibited a zero-cost enforced distinction that passed it.)

  ADDITIVITY IS EXERCISED, not asserted: c(empty) == 0, and c(S | T) ==
  c(S) + c(T) over every disjoint pair (S, T) of the n = 4 cube and every
  disjoint pair of a declared deterministic stride through the n = 5 cube.

  AGREEMENT ACROSS THE FULL CUBE: for d in 1..5, F_d agrees with the banked cost
  on ALL 64 subsets at n = 4 and ALL 1024 at n = 5, in both the positive and the
  cancelling mode, and separately on the realizable separated-pair sets of
  build_family.  The full-cube sweep is what refuses a cost that agrees only at
  the sizes a sparse probe happens to visit.

  THE FENCE ON d: 0^d = 0 is asserted for every member, and d = 0 is executed as
  the counterexample it excludes -- in the positive mode F_0 returns eps*|P|
  against a banked cost of eps*|S|, and in the cancelling mode eps* times the
  sum of ALL weights against the sum over S -- so the family's lower bound is
  load-bearing and stated for its real reason (BOTH 1^d = 1 and 0^d = 0), not
  for half of it.

  DISTINCTNESS, scoped: on the declared witness the five F_d take five pairwise
  distinct values.  This is NOT general and the scope is executed -- at
  v = (2,-2,0,0,0,0) the odd-degree members collide at 0, computed.  Without
  some such witness the agreement leg would be vacuous, which is the only work
  distinctness does here.

  EXACT DEGREE: F_d(lambda v) == lambda^d F_d(v) and != lambda^e F_d(v) for every
  e != d, at scalars whose separating property lambda^d != lambda^e is ASSERTED
  rather than left to a comment.

  THE EPS*-TEST IS BLIND: every F_d is 1-homogeneous in eps*, so that test's
  verdict set has one element while the degree set has five.  SCOPE: this is
  proved about the extension family, not about the banked callee.

  WHAT THE DEGREE RANGE DOES AND DOES NOT PIN, disclosed: the LOWER bound d >= 1
  is load-bearing and executed (admitting d = 0 fails agreement).  The UPPER
  bound is not pinned by anything here -- other tuples pass -- and in particular
  nothing in this check singles out d = 1, which is the whole subject of the
  companion check.  That is the correct posture for a freedom result, and it is
  said rather than left to be discovered.

  NO SCALAR ACTION ON THE DOMAIN: 2 * (a non-empty indicator) is the indicator of
  no subset, so "degree of the banked cost" is not well-formed.

  CONTROLS ROUTED THROUGH THE GUARD ITSELF: agreement is factored into a named
  predicate, and five families are passed through THAT predicate -- the real
  one, an affine shift, a doubled map, a shifted-weight map, the degree-shifted
  F_0, and one that is correct at d = 1 and wrong above it.  The last of these
  is what pins the degree SWEEP: without it the family could shrink to (1,) with
  every other control still reporting success.  An inline recomputation is not a
  control -- an earlier cut recomputed the F_0 row inline, which is the very
  pattern this paragraph condemns, and a blinded auditor caught the mismatch
  between this prose and that code.

  THE PRICE IS SWEPT: agreement, additivity and the empty-configuration row all
  run at three distinct values of eps*, one of them unrelated to both the unit
  probe and the working value.  An earlier cut evaluated the callee only at 1
  and 7/5, and an auditor exhibited a cost that is neither additive nor
  1-homogeneous in eps* anywhere except at exactly those two points and still
  passed.

  THE CALLEE IS HANDED THE REAL OBJECTS: the agreement rows run on the
  build_family group dicts as they come, in both modes and at every swept price,
  and the real dict is asserted to agree with the stripped {"sep_pairs": ...}
  form -- so "the banked cost is a function of the separated-pair set alone" is
  computed rather than inherited silently.  An auditor exhibited a callee that
  agreed on synthetic dicts and diverged on the objects the bank actually
  passes.

check_L_linear_extension_not_quadratic
(tier 3, [P_structural | eps* != 0 is load-bearing and its fail-control bites;
POSITIVITY is NOT load-bearing, computed; no-cancellation is NOT load-bearing,
computed]).

  THE DEGREE ROUTE: L(2v) == 2L(v) != 4L(v) wherever L(v) != 0, so L satisfies no
  quadratic form's scaling law and L quadratic would force L == 0.

  THE PREMISE IS NAMED CORRECTLY, and this is the correction of record: what
  excludes L == 0 is eps* != 0, strictly weaker than MD's positive floor.
  Computed: the verdict is TRUE at eps* = -7/5 and at eps* = 1/10^6, and FALSE
  only at eps* = 0.  Positivity buys nothing here.  This is the same shape as the
  v24.3.443 correction (the forcing premise there is psi(I) != 0, not
  positivity), and it is recorded rather than repeated.

  THE TWO NON-LOAD-BEARING PROBES ARE NOT SYMMETRIC, and the grade string
  should not be read as though they were.  Positivity CANNOT come back
  load-bearing under any weights or witnesses: L is proportional to eps*, so
  1-homogeneity forces the verdict at -7/5 and at 10^-6 to equal the verdict at
  7/5.  That row is a consistency row.  The no-cancellation row is a genuine
  probe -- replacing the witnesses with vectors inside the cancelling-mode
  kernel makes it FAIL -- and it is the one that could have gone the other way.

  THE NAMED PREMISE IS NECESSARY, NOT SUFFICIENT: what does the work is
  eps* != 0 AND some witness outside ker L.  Both are recorded in the premise
  list; citing the first alone overstates what was shown.

  NO-CANCELLATION IS NOT LOAD-BEARING, and here it is actually computed: the
  cancelling-mode weights are read off the banked callee and routed INTO L, and
  the verdict is recomputed under them.  DISCLOSED SCOPE, executed: the
  cancelling-mode L has a kernel the positive-mode L does not -- at
  v = (1,1,0,0,0,0) the cancelling L vanishes while the positive L does not -- so
  the verdict survives because SOME witness has L != 0, not because every one
  does.  Both witnesses are exhibited.

  THE FENCE, IN THE STATEMENT: Q(v) = eps* sum_p w_p v_p^2 is a genuine quadratic
  form, its Gram matrix diag(eps* w_p) is BUILT at each universe size and its
  determinant computed by exact elimination (not read off a formula, and not at a
  hardcoded |P|), and Q agrees with the banked cost at every point of the cube.
  So "the banked cost admits no quadratic extension" is FALSE.  Q is asserted to
  differ from L off the cube, or the fence would be vacuous.

  THE PARALLELOGRAM ROUTE IS UNSOUND and is not used: the defect of an additive L
  equals -2L(b) exactly, computed, and vanishes on the whole kernel.

  DOMAIN DISCLOSURE: every witness here lies outside {0,1}^P, so this check's
  content lives on the extension's domain, which the banked cost does not
  inhabit.  That is the precise reason the companion check is the stronger one.

============================================================================
MAY-NOT-CITE.

  - "The banked ledger is not quadratic."  NOT WELL-FORMED as stated -- degree is
    not a predicate of the banked object.  Under the only well-formed reading,
    "no quadratic form agrees with the banked cost", it is FALSE and computed so.
  - "The banked cost admits no quadratic extension."  FALSE, executed as a fence.
  - "The sandwich construction cannot run on the banked cost."  NOT ESTABLISHED
    either way here.  The fence kills only a DEGREE-based obstruction; P1
    realization, covariance and CP are untouched by anything in this module.
  - "QUADRATIC_LEDGER is refuted", "supplied", "derived", or "read off the
    ledger."  None of these.  It lives on a different carrier space.
  - "A second, non-additive ledger is forced."  Refuted 2026-07-28 by two blinded
    auditors: Gibbs weighting 2^-c of the SAME additive cost reproduces exact
    argmin selection in the beta -> infinity limit.  Nothing here revives it.  Do
    not re-walk any fence whose "second ledger" is a monotone transform of the
    first.
  - "Born is derived" / "P1 is reduced" / "the A2-Born tension is resolved."
    Nothing here touches P1, Born, or the selection law.
  - "MD forces the result."  It does not.  eps* != 0 does; positivity and
    no-cancellation are each computed NOT to be load-bearing.
  - "Scaling eps* tests the ledger's degree."  Computed to have exactly zero
    discriminating power.
  - "The F_d are pairwise distinct."  Only on the declared witness; the collision
    at v = (2,-2,0,0,0,0) is computed.
  - "The full domain is verified."  The cube is swept exhaustively at n = 4 and
    n = 5 and the general statement rests on 1^d = 1 with 0^d = 0; n is not
    swept and is not claimed to be.

PROVENANCE: the surviving 2 statements of the killed candidate
two_ledger_separation (two blinded cold auditors, KILL 0.85 / REDUCE 0.85,
convergent; nothing was banked).  Lane record: The Turning (parked)/
two_ledger_separation_2026-07-28/AUDIT_RESULT_and_what_survives.md.  This module
then took its own two blinded cold audits (LAND-WITH-FIXES 0.82 / REDUCE 0.85,
convergent without contact) and every fix was carried at code level before
landing: the premise re-named from positivity to non-vanishing, the
no-cancellation scoping actually computed, the weights read off the callee, the
full cube swept, additivity exercised, the controls routed through the guard, the
scalar separation asserted, the Gram matrix built, and four prose overclaims
withdrawn.

NON-EXPORTING.  physical_premises_certified = false.  No existing grade moved.
"""

from fractions import Fraction as F
from itertools import product
from typing import Callable, Dict, List, Sequence, Tuple

PHYSICAL_PREMISES_CERTIFIED = False
EXPORTS: Tuple[str, ...] = ()
BANK_MODIFIED = False

# The extension family.  d = 1 is the linear extension; d = 2 is the quadratic
# one the sandwich construction would want.  The lower bound d >= 1 is
# load-bearing: d = 0 is executed below as the excluded counterexample.
_DEGREES: Tuple[int, ...] = (1, 2, 3, 4, 5)

# A non-indicator rational witness on six coordinates.  Every F_d is non-zero on
# it and the five values are pairwise distinct; both are asserted, and the
# NON-generality of the second is asserted too, on _COLLIDING_WITNESS.
_WITNESS: Tuple[F, ...] = (F(1, 2), F(3), F(-1), F(0), F(2), F(1, 3))

# Where distinctness FAILS: odd degrees collide at 0.  Carried so the scope of
# the distinctness leg is computed rather than implied.
_COLLIDING_WITNESS: Tuple[F, ...] = (F(2), F(-2), F(0), F(0), F(0), F(0))

# Scalars for the homogeneity legs.  Their separating property lambda^d !=
# lambda^e is ASSERTED below, not left to this comment.
_LAMBDAS: Tuple[F, ...] = (F(3), F(-2), F(1, 2))

_EPS: F = F(7, 5)
# The callee is exercised at SEVERAL prices, one of them unrelated to both the
# unit probe and the working value.  An earlier cut evaluated it only at 1 and
# 7/5, and a blinded auditor exhibited a cost that is neither additive nor
# 1-homogeneous in eps* anywhere except at those two points and still passed.
_EPS_ALT: F = F(11, 3)
_EPS_SWEEP: Tuple[F, ...] = (F(7, 5), F(11, 3), F(2))
_EPS_NEGATIVE: F = F(-7, 5)          # positivity dropped, non-vanishing kept
_EPS_TINY: F = F(1, 10 ** 6)
_CARRIERS: Tuple[int, ...] = (4, 5)
_MODES: Tuple[str, ...] = ("positive", "cancelling")

# The n = 5 cube has 1024 subsets and 3^10 disjoint pairs; the additivity sweep
# takes a declared deterministic stride through it rather than all 59049.
_STRIDE_N5: int = 7


def _result(name, epistemic, key_result, evidence, fails, tier,
            dependencies, premises, negative_controls, cross_refs,
            fail_count=None):
    """Build the result dict, and CROSS-ASSERT the two failure records HERE.

    The cross-assert lives at the point the dict is BUILT, not in run_all(),
    because the bank does NOT call run_all(): bank.py invokes each registered
    check_fn() directly and reads r['passed'].  A guarantee living only in
    run_all() does not travel on the banked path -- demonstrated by a blinded
    execution audit on 2026-07-28 and corrected bank-wide at v24.3.450.

    TWO RESIDUAL LIMITS, DISCLOSED.  (a) This catches DIVERGENCE between the two
    failure records, which is the realistic tampering and is what escaped
    before; it does NOT catch a bare literal substitution of 'passed', because
    nothing downstream re-derives that field.  (b) The second record is written
    at the SAME SITE as the first (adjacent lines of one helper), so an edit
    that removes both together is not caught either.  'Independent' means
    independently stored, not independently sited."""
    counted = len(fails) if fail_count is None else fail_count
    if len(fails) != counted:
        raise AssertionError(
            f"{name}: failure records disagree -- fail_reasons has "
            f"{len(fails)} entries, the independent counter says {counted}")
    return {
        'fail_count': counted,
        'name': name,
        'epistemic': epistemic,
        'passed': (counted == 0),
        'tier': tier,
        'key_result': key_result,
        'evidence': evidence,
        'fail_reasons': fails,
        'dependencies': list(dependencies),
        'premises': list(premises),
        'negative_controls': list(negative_controls),
        'cross_refs': list(cross_refs),
        'physical_premises_certified': PHYSICAL_PREMISES_CERTIFIED,
        'exports': list(EXPORTS),
        'bank_modified': BANK_MODIFIED,
    }


# ==========================================================================
# The banked callee, and the weights READ OFF IT.
# ==========================================================================


def _banked():
    """Import the REAL banked cost.  Fail-closed: no vendored copy, because a
    vendored copy lets the checks pass while the banked object drifts."""
    from apf.symmetry_cost_floor import build_family, config_cost
    return build_family, config_cost


def _all_pairs(n: int) -> List[Tuple[int, int]]:
    return [(i, j) for i in range(n) for j in range(i + 1, n)]


def _cost(config_cost, pairs: Sequence[Tuple[int, int]], eps: F, mode: str) -> F:
    """Call the BANKED cost on an arbitrary separated-pair set."""
    return config_cost({"sep_pairs": list(pairs)}, eps, mode)


def _probe_weights(config_cost, universe: Sequence[Tuple[int, int]],
                   mode: str) -> List[F]:
    """Recover w_p by evaluating the banked cost on the singleton {p} at unit
    price.  Nothing here assumes the weight is 1."""
    return [_cost(config_cost, [p], F(1), mode) for p in universe]


def _F_d(d: int, eps: F, weights: Sequence[F], vec: Sequence[F]) -> F:
    """F_d(v) = eps * sum_p w_p v_p^d, at the weights READ off the callee."""
    return eps * sum((w * (x ** d) for w, x in zip(weights, vec)), F(0))


def _indicator(universe: Sequence[Tuple[int, int]],
               chosen: Sequence[Tuple[int, int]]) -> List[F]:
    sel = set(chosen)
    return [F(1) if p in sel else F(0) for p in universe]


def _subsets(universe: Sequence[Tuple[int, int]]):
    for mask in range(1 << len(universe)):
        yield [p for i, p in enumerate(universe) if mask >> i & 1]


def _det(m: List[List[F]]) -> F:
    """Exact determinant by fraction-free-free Gaussian elimination."""
    a = [row[:] for row in m]
    n = len(a)
    det = F(1)
    for c in range(n):
        piv = next((r for r in range(c, n) if a[r][c] != F(0)), None)
        if piv is None:
            return F(0)
        if piv != c:
            a[c], a[piv] = a[piv], a[c]
            det = -det
        det *= a[c][c]
        inv = F(1) / a[c][c]
        for r in range(c + 1, n):
            if a[r][c] != F(0):
                f = a[r][c] * inv
                for k in range(c, n):
                    a[r][k] -= f * a[c][k]
    return det


# ==========================================================================
# CHECK 1 -- the degree of an extension is not determined by the banked cost.
# ==========================================================================


def check_L_ledger_extension_degree_free() -> Dict[str, object]:
    """Tier 3, [P_math | inherits the symmetry_cost_floor cost model]."""
    fails: List[str] = []
    tally = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
            tally[0] += 1

    try:
        build_family, config_cost = _banked()
    except Exception as exc:                                  # fail-closed
        ck(False, f"the banked cost could not be imported, so nothing here was "
                  f"tested against it: {exc!r}")
        return _result(
            'L_ledger_extension_degree_free', 'P_math',
            'REFUSED: the banked cost was not importable.', {}, fails, 3,
            (), (), (), (), fail_count=tally[0])

    ck(getattr(config_cost, '__module__', None) == 'apf.symmetry_cost_floor',
       "config_cost must be the banked apf.symmetry_cost_floor function, not a "
       f"local reimplementation (got {getattr(config_cost, '__module__', None)})")

    # ---- THE AGREEMENT PREDICATE.  Controls run through THIS, not through an
    # ---- inline lookalike: a control that recomputes the comparison itself
    # ---- cannot notice that the guard has stopped firing.
    def agrees(family: Callable[[int, F, Sequence[F], Sequence[F]], F],
               universe, weights, eps, mode) -> bool:
        for S in _subsets(universe):
            banked = _cost(config_cost, S, eps, mode)
            v = _indicator(universe, S)
            for d in _DEGREES:
                if family(d, eps, weights, v) != banked:
                    return False
        return True

    cube_rows = 0
    additivity_rows = 0
    empty_rows = 0
    zero_power_rows = 0
    d0_refuted = 0
    weight_values: Dict[str, List[str]] = {}
    for n in _CARRIERS:
        universe = _all_pairs(n)
        for mode in _MODES:
            weights = _probe_weights(config_cost, universe, mode)
            weight_values[f"n{n}_{mode}"] = [str(w) for w in weights]

            # (i) ADDITIVITY, EXERCISED.  c(empty) = 0 and c(S | T) = c(S) + c(T)
            # on disjoint pairs.  This is the property the headline names, and an
            # earlier cut never tested it -- an auditor exhibited a non-additive
            # cost that passed by agreeing only at the sizes a sparse probe
            # happened to visit.
            for eps in _EPS_SWEEP:
                ck(_cost(config_cost, [], eps, mode) == F(0),
                   f"the banked cost of the empty configuration must be 0 "
                   f"(n={n}, {mode}, eps={eps})")
                empty_rows += 1
            stride = 1 if n == 4 else _STRIDE_N5
            for idx, assign in enumerate(product((0, 1, 2), repeat=len(universe))):
                if idx % stride:
                    continue
                S = [p for p, a in zip(universe, assign) if a == 1]
                T = [p for p, a in zip(universe, assign) if a == 2]
                for eps in _EPS_SWEEP:
                    ck(_cost(config_cost, S + T, eps, mode)
                       == _cost(config_cost, S, eps, mode)
                       + _cost(config_cost, T, eps, mode),
                       f"the banked cost must be additive on the disjoint pair "
                       f"({S}, {T}) (n={n}, {mode}, eps={eps})")
                    additivity_rows += 1

            # (ii) THE d-FENCE, with its REAL reason.  1^d = 1 is half of it;
            # 0^d = 0 is the other half, and d = 0 is the excluded case.
            for d in _DEGREES:
                ck(F(0) ** d == F(0),
                   f"0^{d} must vanish, or F_{d} would charge for unenforced "
                   f"pairs")
                zero_power_rows += 1
            nonfull = [p for p in universe[:-1]]
            if nonfull:
                v_nf = _indicator(universe, nonfull)
                ck(_F_d(0, _EPS, weights, v_nf)
                   != _cost(config_cost, nonfull, _EPS, mode),
                   f"d = 0 must FAIL agreement, or the family's lower bound is "
                   f"decorative (n={n}, {mode})")
                d0_refuted += 1

            # (iii) AGREEMENT ACROSS THE FULL CUBE, through the predicate.
            for eps in _EPS_SWEEP:
                ck(agrees(_F_d, universe, weights, eps, mode),
                   f"every F_d must reproduce the banked cost at EVERY point of "
                   f"the cube (n={n}, {mode}, eps={eps})")
                cube_rows += (1 << len(universe)) * len(_DEGREES)

            # (iv) CONTROLS, THROUGH THE SAME PREDICATE.  Each is a real defect.
            ck(not agrees(lambda d, e, w, v: _F_d(d, e, w, v) + F(1),
                          universe, weights, _EPS, mode),
               f"an affine shift F + 1 must FAIL the agreement predicate "
               f"(n={n}, {mode})")
            ck(not agrees(lambda d, e, w, v: F(2) * _F_d(d, e, w, v),
                          universe, weights, _EPS, mode),
               f"a doubled family 2F must FAIL the agreement predicate "
               f"(n={n}, {mode})")
            ck(not agrees(lambda d, e, w, v: _F_d(d, e, [x + F(1) for x in w], v),
                          universe, weights, _EPS, mode),
               f"a shifted-weight family must FAIL the agreement predicate "
               f"(n={n}, {mode})")
            # THE DEGREE-SHIFTED CONTROL, ROUTED THROUGH THE PREDICATE.  An
            # earlier cut recomputed this inline -- the very pattern this
            # module condemns -- and a blinded auditor caught the mismatch
            # between the prose and the code.
            ck(not agrees(lambda d, e, w, v: _F_d(0, e, w, v),
                          universe, weights, _EPS, mode),
               f"the degree-shifted family F_0 must FAIL the agreement "
               f"predicate (n={n}, {mode})")
            # A DEGREE-SENSITIVE control: correct at d = 1, wrong above it.
            # Without this the whole degree sweep could shrink to (1,) with
            # every control still reporting success.
            ck(not agrees(lambda d, e, w, v: _F_d(d, e, w, v)
                          + (F(0) if d == 1 else F(1)),
                          universe, weights, _EPS, mode),
               f"a family that is correct only at d = 1 must FAIL the agreement "
               f"predicate, or the degree sweep is not pinned (n={n}, {mode})")

        # (v) THE REALIZABLE SETS, and NO SCALAR ACTION on the domain.
        for g in build_family(n):
            v = _indicator(universe, g["sep_pairs"])
            for mode in _MODES:
                weights = _probe_weights(config_cost, universe, mode)
                for eps in _EPS_SWEEP:
                    # The REAL group dict, unstripped: an auditor exhibited a
                    # callee that agreed on synthetic {"sep_pairs": ...} dicts
                    # and diverged on the objects the bank actually passes.
                    for d in _DEGREES:
                        ck(_F_d(d, eps, weights, v) == config_cost(g, eps, mode),
                           f"F_{d} must agree with the banked cost on the REAL "
                           f"group dict of {g['name']} (n={n}, {mode}, "
                           f"eps={eps})")
                    ck(config_cost(g, eps, mode)
                       == _cost(config_cost, g["sep_pairs"], eps, mode),
                       f"the banked cost must be a function of sep_pairs ALONE: "
                       f"the real dict and the stripped one must agree "
                       f"({g['name']}, {mode}, eps={eps})")
            if g["sep_pairs"]:
                ck(any(F(2) * x not in (F(0), F(1)) for x in v),
                   f"2 * indicator must leave the banked domain ({g['name']})")

    # ---- OFF-CUBE STRUCTURE.  Weights fixed at 1 here: this half is the pure
    # ---- mathematics of the family, not a statement about the banked ledger.
    unit = [F(1)] * len(_WITNESS)
    vals = [_F_d(d, _EPS, unit, _WITNESS) for d in _DEGREES]
    ck(len(set(vals)) == len(_DEGREES),
       f"the extensions must be pairwise distinct ON THE DECLARED WITNESS, got "
       f"{len(set(vals))} distinct values for {len(_DEGREES)} degrees")
    ck(all(x != F(0) for x in vals),
       "every F_d must be non-zero on the witness, or the exact-degree leg "
       "degenerates to 0 == 0")
    ck(any(x not in (F(0), F(1)) for x in _WITNESS),
       "the witness must lie OUTSIDE the banked domain, or it cannot separate "
       "the extensions at all")
    # The scope of distinctness, COMPUTED rather than implied.
    coll = [_F_d(d, _EPS, unit, _COLLIDING_WITNESS) for d in _DEGREES]
    ck(len(set(coll)) < len(_DEGREES),
       "distinctness must be exhibited as WITNESS-SPECIFIC: a colliding vector "
       "must exist, or the scope stated in the docstring is not computed")

    # Scalars must actually separate degrees -- asserted, not commented.
    for lam in _LAMBDAS:
        for d in _DEGREES:
            for e in _DEGREES:
                if d != e:
                    ck(lam ** d != lam ** e,
                       f"lambda={lam} cannot separate degrees {d} and {e}; the "
                       f"scalar choice is load-bearing and must be asserted")

    degree_rows = 0
    for d in _DEGREES:
        base = _F_d(d, _EPS, unit, _WITNESS)
        for lam in _LAMBDAS:
            scaled = [lam * x for x in _WITNESS]
            ck(_F_d(d, _EPS, unit, scaled) == (lam ** d) * base,
               f"F_{d} must be homogeneous of degree {d} (lambda={lam})")
            for e in _DEGREES:
                if e != d:
                    ck(_F_d(d, _EPS, unit, scaled) != (lam ** e) * base,
                       f"F_{d} must NOT be homogeneous of degree {e} "
                       f"(lambda={lam}) -- the degree must be exact")
            degree_rows += 1

    # THE EPS*-TEST IS BLIND -- the defect that killed the candidate, as a result.
    eps_verdicts = set()
    for d in _DEGREES:
        base = _F_d(d, _EPS, unit, _WITNESS)
        eps_verdicts.add(all(
            _F_d(d, lam * _EPS, unit, _WITNESS) == lam * base
            for lam in _LAMBDAS))
    ck(eps_verdicts == {True},
       f"every extension must be 1-homogeneous in eps*, which is what makes the "
       f"eps*-test blind; got {sorted(str(v) for v in eps_verdicts)}")

    return _result(
        'L_ledger_extension_degree_free',
        ('[P_math | the 1^d = 1 kernel is pure; the statement ABOUT the banked '
         'ledger inherits symmetry_cost_floor\'s cost model, graded '
         '[P_structural] there]'),
        ("THE DEGREE IS FREE.  The banked cost -- config_cost from "
         "apf.symmetry_cost_floor, IMPORTED AND CALLED, its per-pair weights "
         "READ OFF THE CALLEE by singleton probe and never hardcoded -- is "
         "verified FINITELY ADDITIVE (c(empty) = 0 and c(S|T) = c(S) + c(T) on "
         "disjoint pairs, exercised) and is then reproduced EXACTLY by "
         "F_d(v) = eps* sum_p w_p v_p^d for every d in 1..5, at EVERY point of "
         "the cube at n = 4 (64 subsets) and n = 5 (1024), in BOTH the positive "
         "and cancelling modes, and on the realizable separated-pair sets.  The "
         "reason is that indicator entries are 0 or 1 with 1^d = 1 AND 0^d = 0, "
         "so the d >= 1 bound is load-bearing: d = 0 is executed as the excluded "
         "counterexample.  So the banked ledger NEITHER SUPPLIES NOR REFUTES a "
         "degree -- degree belongs to a chosen extension, and on the banked "
         "domain it is not a well-formed predicate, since 2 * (an indicator) is "
         "the indicator of no subset.  COROLLARY, executed: the eps*-scaling "
         "test is BLIND, one verdict across five degrees, which is why the "
         "2026-07-28 candidate's 'the banked ledger is 1-homogeneous, hence not "
         "quadratic' was a non sequitur.  SCOPE: distinctness of the family is "
         "WITNESS-SPECIFIC and the collision at (2,-2,0,0,0,0) is computed; n is "
         "not swept.  MAY NOT BE CITED as 'the banked ledger is not quadratic' "
         "(not well-formed) or 'the banked cost admits no quadratic extension' "
         "(FALSE, fenced in the companion check)."),
        {
            'carriers': list(_CARRIERS),
            'modes': list(_MODES),
            'degrees': list(_DEGREES),
            'cube_agreement_evaluations': cube_rows,
            'additivity_rows': additivity_rows,
            'empty_config_rows': empty_rows,
            'zero_power_rows': zero_power_rows,
            'd0_counterexample_rows': d0_refuted,
            'exact_degree_rows': degree_rows,
            'probed_weights': weight_values,
            'witness_values': [str(x) for x in vals],
            'distinct_on_witness': len(set(vals)),
            'distinct_on_colliding_witness': len(set(coll)),
            'eps_star_test_verdicts': sorted(str(v) for v in eps_verdicts),
        },
        fails,
        3,
        ('L_cost_floor_at_maximal_symmetry',),
        ("the symmetry_cost_floor cost model (that module's own "
         "[P_structural] modelling choice) is inherited, not re-derived",),
        ("an affine shift F + 1 fails the agreement predicate, through the "
         "predicate itself",
         "a doubled family 2F fails it",
         "a shifted-weight family fails it",
         "d = 0 fails agreement, so the family's lower bound is not decorative",
         "the witness is asserted to lie outside the banked domain",
         "a colliding witness is exhibited, so distinctness is scoped",),
        ('L_cost_floor_at_maximal_symmetry', 'L_orbit_count_monotone_in_symmetry',
         'QUADRATIC_LEDGER (H4, _held_holonomy_contract -- DIFFERENT CARRIER)',
         'L_bounded_orbit_positivity'),
        fail_count=tally[0],
    )


# ==========================================================================
# CHECK 2 -- the LINEAR extension, specifically, is not a quadratic form.
# ==========================================================================


def check_L_linear_extension_not_quadratic() -> Dict[str, object]:
    """Tier 3, [P_structural | eps* != 0]."""
    fails: List[str] = []
    tally = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
            tally[0] += 1

    try:
        build_family, config_cost = _banked()
    except Exception as exc:                                  # fail-closed
        ck(False, f"the banked cost could not be imported, so the fence was "
                  f"never run against it: {exc!r}")
        return _result(
            'L_linear_extension_not_quadratic',
            '[P_structural | eps* != 0]',
            'REFUSED: the banked cost was not importable.', {}, fails, 3,
            ('L_epsilon_star',), (), (), (), fail_count=tally[0])

    ck(getattr(config_cost, '__module__', None) == 'apf.symmetry_cost_floor',
       "config_cost must be the banked function, not a local reimplementation")

    universe4 = _all_pairs(4)
    w_pos = _probe_weights(config_cost, universe4, "positive")
    w_can = _probe_weights(config_cost, universe4, "cancelling")

    def L(eps: F, weights: Sequence[F], vec: Sequence[F]) -> F:
        return _F_d(1, eps, weights, vec)

    def Q(eps: F, weights: Sequence[F], vec: Sequence[F]) -> F:
        return _F_d(2, eps, weights, vec)

    def is_not_quadratic(eps: F, weights: Sequence[F], vecs) -> bool:
        """L fails every quadratic form's scaling law iff some witness has
        L(2v) != 4L(v) -- equivalently, since L(2v) = 2L(v) always, iff L is
        not identically zero on the witnesses."""
        return any(L(eps, weights, [F(2) * x for x in v])
                   != F(4) * L(eps, weights, v) for v in vecs)

    witnesses = [list(_WITNESS),
                 [F(1), F(-1), F(2), F(0), F(1, 4), F(5)],
                 [F(-3), F(1, 7), F(0), F(4), F(-1), F(2)]]

    # (i) THE DEGREE ROUTE.
    degree_rows = 0
    for v in witnesses:
        doubled = [F(2) * x for x in v]
        ck(L(_EPS, w_pos, doubled) == F(2) * L(_EPS, w_pos, v),
           "L must be 1-homogeneous: L(2v) = 2L(v)")
        if L(_EPS, w_pos, v) != F(0):
            ck(L(_EPS, w_pos, doubled) != F(4) * L(_EPS, w_pos, v),
               "L(2v) must differ from 4L(v) where L(v) != 0, which is what "
               "forbids L from being a quadratic form")
        degree_rows += 1
    ck(is_not_quadratic(_EPS, w_pos, witnesses),
       "at a non-zero eps*, L must fail the quadratic scaling law")

    # (ii) THE PREMISE, NAMED CORRECTLY.  The fail-control at eps* = 0 must bite,
    # and positivity must be shown NOT to be what does the work.  An earlier cut
    # declared eps* > 0 load-bearing on the strength of the eps* = 0 row alone;
    # two blinded auditors independently found the same defect, which is the
    # v24.3.443 correction (psi(I) != 0, not positivity) recurring.
    ck(not is_not_quadratic(F(0), w_pos, witnesses),
       "FAIL-CONTROL MUST BITE: at eps* = 0 the map L is identically zero, IS a "
       "quadratic form (the zero form), and the verdict must become False.  If "
       "it does not, the dependency is unearned")
    ck(all(L(F(0), w_pos, v) == F(0) for v in witnesses),
       "at eps* = 0 the map must actually be identically zero on the witnesses")
    ck(_EPS_NEGATIVE < F(0),
       "the positivity-idle leg must run at a genuinely NEGATIVE eps*, or it is "
       "a duplicate of the main verdict rather than a probe of the premise")
    ck(F(0) < _EPS_TINY < _EPS,
       "the floor-magnitude leg must run at a strictly smaller positive eps*, "
       "or it tests nothing the main verdict has not already tested")
    ck(is_not_quadratic(_EPS_NEGATIVE, w_pos, witnesses),
       "POSITIVITY MUST BE SHOWN IDLE: the verdict must be unchanged at a "
       "NEGATIVE eps*, or 'eps* > 0 is load-bearing' would be the correct "
       "reading and this module's grade string would be wrong")
    ck(is_not_quadratic(_EPS_TINY, w_pos, witnesses),
       "the verdict must be unchanged at an arbitrarily small positive eps*, so "
       "no floor magnitude is doing work either")

    # (iii) NO-CANCELLATION, ACTUALLY COMPUTED: the cancelling weights are routed
    # INTO L, not merely observed on the side.
    ck(w_can != w_pos,
       "the cancelling mode must actually change the weights, or the scoping "
       "claim is untested")
    ck(any(w < F(0) for w in w_can),
       "the cancelling mode must produce at least one negative weight, or MD's "
       "no-cancellation clause is not being dropped at all")
    ck(is_not_quadratic(_EPS, w_can, witnesses),
       "the verdict must be UNCHANGED under cancelling weights, which is what "
       "scopes the dependency to eps* != 0 alone")
    # DISCLOSED SCOPE: the cancelling-mode L has a kernel the positive one does
    # not, so the verdict survives on SOME witness, not on every one.
    kernel_probe = [F(1), F(1), F(0), F(0), F(0), F(0)]
    ck(L(_EPS, w_can, kernel_probe) == F(0),
       "the disclosed cancelling-mode kernel witness must actually vanish")
    ck(L(_EPS, w_pos, kernel_probe) != F(0),
       "the same witness must NOT vanish under positive weights, or there is no "
       "kernel asymmetry to disclose")

    # (iv) THE FENCE, EXECUTED against the banked cost across the FULL cube.
    fence_rows = 0
    gram_dets: Dict[str, str] = {}
    for n in _CARRIERS:
        universe = _all_pairs(n)
        for mode in _MODES:
            weights = _probe_weights(config_cost, universe, mode)
            for eps in _EPS_SWEEP:
                broke = False
                for S in _subsets(universe):
                    v = _indicator(universe, S)
                    if Q(eps, weights, v) != _cost(config_cost, S, eps, mode):
                        ck(False,
                           f"the quadratic form Q must agree with the BANKED "
                           f"cost at every point of the cube (n={n}, {mode}, "
                           f"eps={eps}, S={S})")
                        broke = True
                        break
                    fence_rows += 1
                if broke:
                    break
            for g in build_family(n):
                v = _indicator(universe, g["sep_pairs"])
                ck(Q(_EPS, weights, v) == config_cost(g, _EPS, mode),
                   f"Q must agree with the banked cost on the REAL group dict "
                   f"of {g['name']} (n={n}, {mode})")
                fence_rows += 1
            # The Gram matrix is BUILT at THIS universe's size, and its
            # determinant computed by elimination -- not read off a formula at a
            # hardcoded coordinate count.
            k = len(universe)
            gram = [[(_EPS * weights[i] if i == j else F(0))
                     for j in range(k)] for i in range(k)]
            det = _det(gram)
            gram_dets[f"n{n}_{mode}"] = str(det)
            ck(det != F(0),
               f"Q's Gram matrix must be nondegenerate (n={n}, {mode})")
            # THE ROW MUST DISCRIMINATE.  With the banked weights in {+1,-1} the
            # determinant cannot vanish, so the assertion above is a consistency
            # row, not a test.  What makes it a test is that a zero weight --
            # an enforced distinction that costs nothing -- DOES collapse it.
            zeroed = [row[:] for row in gram]
            zeroed[0][0] = F(0)
            ck(_det(zeroed) == F(0),
               f"a zero weight must collapse the Gram determinant, or the "
               f"nondegeneracy row discriminates nothing (n={n}, {mode})")
    for lam in _LAMBDAS:
        scaled = [lam * x for x in _WITNESS]
        ck(Q(_EPS, w_pos, scaled) == (lam ** 2) * Q(_EPS, w_pos, _WITNESS),
           f"Q must be a genuine quadratic form (lambda={lam})")
    ck(Q(_EPS, w_pos, _WITNESS) != L(_EPS, w_pos, _WITNESS),
       "Q must DIFFER from L off the cube, or the fence is vacuous")

    # (v) THE PARALLELOGRAM ROUTE IS UNSOUND -- why the degree route is used.
    def par_defect(eps: F, weights, a, b) -> F:
        s = [x + y for x, y in zip(a, b)]
        d = [x - y for x, y in zip(a, b)]
        return (L(eps, weights, s) + L(eps, weights, d)
                - F(2) * L(eps, weights, a) - F(2) * L(eps, weights, b))

    a_vec = [F(1), F(2), F(3), F(4), F(5), F(6)]
    b_kernel = [F(1), F(-1), F(0), F(0), F(0), F(0)]
    b_generic = [F(1), F(0), F(0), F(0), F(0), F(0)]
    ck(L(_EPS, w_pos, b_kernel) == F(0),
       "the kernel witness must actually lie in ker L")
    ck(par_defect(_EPS, w_pos, a_vec, b_kernel) == F(0),
       "on a kernel witness the parallelogram defect must VANISH for a strictly "
       "linear L -- this is the unsoundness being exhibited")
    ck(par_defect(_EPS, w_pos, a_vec, b_generic)
       == F(-2) * L(_EPS, w_pos, b_generic),
       "the parallelogram defect of an additive L must equal -2 L(b) exactly")
    ck(par_defect(_EPS, w_pos, a_vec, b_generic) != F(0),
       "off the kernel the defect must be non-zero, or the control does not "
       "discriminate")

    # (vi) DOMAIN DISCLOSURE.
    ck(all(any(x not in (F(0), F(1)) for x in v) for v in witnesses),
       "every witness must lie outside {0,1}^P: this check's content lives on a "
       "space the banked cost does not inhabit")

    return _result(
        'L_linear_extension_not_quadratic',
        ('[P_structural | eps* != 0 load-bearing (fail-control bites); '
         'POSITIVITY not load-bearing (computed at eps* = -7/5); '
         'no-cancellation not load-bearing (computed, cancelling weights '
         'routed into L)]'),
        ("THE LINEAR EXTENSION IS NOT A QUADRATIC FORM, and that is a statement "
         "about ONE CHOSEN EXTENSION.  L(v) = eps* sum_p w_p v_p satisfies "
         "L(2v) = 2L(v) != 4L(v) wherever L(v) != 0, so L quadratic would force "
         "L == 0.  WHAT EXCLUDES THAT IS NON-VANISHING, NOT POSITIVITY: the "
         "verdict is computed TRUE at eps* = -7/5 and at eps* = 10^-6 and FALSE "
         "only at eps* = 0, so MD's positive floor is idle here and the premise "
         "is eps* != 0 -- the same correction the bank made at v24.3.443, where "
         "the forcing premise is psi(I) != 0 rather than positivity.  "
         "NO-CANCELLATION IS ALSO IDLE, computed by reading the cancelling "
         "weights off the banked callee and routing them INTO L; disclosed "
         "scope, executed: the cancelling-mode L has a kernel the positive-mode "
         "L does not (at (1,1,0,0,0,0) it vanishes), so the verdict survives on "
         "SOME witness rather than on every one.  THE FENCE IS IN THE "
         "STATEMENT: Q(v) = eps* sum_p w_p v_p^2 is a genuine quadratic form "
         "whose Gram matrix is BUILT at each universe size with its determinant "
         "computed by elimination, and it agrees with the BANKED cost at EVERY "
         "point of the cube at n = 4 and n = 5 in both modes -- so 'the banked "
         "cost admits no quadratic extension' is FALSE.  This kills a "
         "DEGREE-based obstruction only; it says nothing about P1 realization, "
         "covariance or CP, and must not be cited as 'the sandwich can run'.  "
         "THE PARALLELOGRAM ROUTE IS UNSOUND and is not used: the defect of an "
         "additive L is exactly -2L(b), computed, vanishing on the whole "
         "kernel.  DOMAIN DISCLOSURE: every witness lies outside {0,1}^P, so "
         "this content lives on the extension's domain, which the banked cost "
         "does not inhabit -- the precise reason the companion check is the "
         "stronger of the two."),
        {
            'degree_route_rows': degree_rows,
            'fence_rows_vs_banked_cost': fence_rows,
            'gram_determinants': gram_dets,
            'probed_positive_weights': [str(w) for w in w_pos],
            'probed_cancelling_weights': [str(w) for w in w_can],
            'verdict_at_eps_zero': str(is_not_quadratic(F(0), w_pos, witnesses)),
            'verdict_at_eps_negative': str(
                is_not_quadratic(_EPS_NEGATIVE, w_pos, witnesses)),
            'verdict_under_cancelling': str(
                is_not_quadratic(_EPS, w_can, witnesses)),
            'L_cancelling_on_kernel_probe': str(L(_EPS, w_can, kernel_probe)),
            'L_positive_on_kernel_probe': str(L(_EPS, w_pos, kernel_probe)),
            'parallelogram_defect_on_kernel': str(
                par_defect(_EPS, w_pos, a_vec, b_kernel)),
            'parallelogram_defect_off_kernel': str(
                par_defect(_EPS, w_pos, a_vec, b_generic)),
        },
        fails,
        3,
        ('L_epsilon_star',),
        ("eps* != 0 (load-bearing)",
         "at least one witness outside ker L (load-bearing; necessary "
         "alongside eps* != 0, and citing eps* != 0 alone overstates it)",
         "MD's positive floor (computed NOT load-bearing; and it CANNOT be, "
         "since 1-homogeneity forces the negative and small-eps* rows -- that "
         "row is a consistency row, not a probe that could have gone either "
         "way)",
         "MD's no-cancellation clause (computed NOT load-bearing; this one IS "
         "a genuine probe -- witnesses inside the cancelling kernel make the "
         "leg fail)",),
        ("eps* = 0 flips the verdict to False -- the control bites",
         "eps* = -7/5 leaves it unchanged -- positivity shown idle",
         "cancelling weights routed into L leave it unchanged -- "
         "no-cancellation shown idle",
         "a nondegenerate quadratic form agrees with the banked cost at every "
         "point of the cube",
         "Q is asserted to differ from L off the cube",
         "the parallelogram defect vanishes on ker L for a strictly linear L",
         "every witness is asserted to lie outside the banked domain",),
        ('L_ledger_extension_degree_free', 'L_cost_floor_at_maximal_symmetry',
         'QUADRATIC_LEDGER (H4, _held_holonomy_contract -- DIFFERENT CARRIER)',
         'T_presentation_gauge_forces_trace'),
        fail_count=tally[0],
    )


_CHECKS = {
    'L_ledger_extension_degree_free': check_L_ledger_extension_degree_free,
    'L_linear_extension_not_quadratic': check_L_linear_extension_not_quadratic,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    """Recompute `passed`, and cross-assert the two failure records.

    A second gate only: the load-bearing cross-assert lives in _result(),
    because the bank never calls this function."""
    out = {}
    for n, fn in _CHECKS.items():
        r = fn()
        listed = len(r['fail_reasons'])
        counted = r['fail_count']
        if listed != counted:
            raise AssertionError(
                f"{n}: failure records disagree -- fail_reasons has {listed} "
                f"entries, the independent counter says {counted}")
        r['passed'] = (counted == 0)
        out[n] = r
    return out


if __name__ == '__main__':
    import sys
    bad = False
    for n, r in run_all().items():
        print(r['name'], '::', r['epistemic'][:62], '::',
              'PASS' if r['passed'] else 'FAIL')
        if not r['passed']:
            bad = True
            for f in r['fail_reasons'][:20]:
                print('  -', f)
    sys.exit(1 if bad else 0)
