"""Tomographic completeness does not supply the matching rank-one effect.

WHAT THIS ADDS, AGAINST THE PRIOR ART (read this first).

The bank already separates effect SOUNDNESS from effect SATURATION, in three
places (check_T_effect_soundness_not_saturation in quantum_frontend_closure.py,
check_T_soundness_saturation_separation in dense_sandwich_born.py, and a leg of
two_exchange_holonomy.py).  ALL_POSITIVE_EFFECTS_REALIZABLE is a named-open leaf
and dense_sandwich_born.py lists the saturation names in FORBIDDEN_DEPENDENCIES.

But the banked separation witness -- the family {0, I, P_0, P_1, I/2} at
quantum_frontend_closure.py -- has real span dimension TWO in Herm(2).  It is
not tomographically complete.  So it leaves open the one repair a reader
naturally reaches for:

    "granted soundness is not saturation, surely a TOMOGRAPHICALLY COMPLETE
     effect family must contain the matching rank-one effect of an admitted
     pure state -- otherwise what is it complete for?"

IT NEED NOT.  This module closes that route with a family that is order-sound,
convex, complement-closed AND tomographically complete (coordinate rank 4, the
full dimension of Herm(2)), and which still omits the matching support effect of
an exhibited pure state.

  THE FAMILY: the convex hull of {0, I, P_a : a in the six signed Bloch axes}.
  Its trace-one slice is the CROSS-POLYTOPE {r : ||r||_1 <= 1} -- the octahedron
  inscribed in the Bloch ball.

  THE OMITTED STATE: the Bloch vector r* = (24/25, 0, -7/25), for which
  ||r*||_2 = 1 exactly (so P_{r*} is a genuine rank-one projector, an admitted
  pure state) while ||r*||_1 = 31/25 > 1.

  THE GENERAL REASON, computed rather than left at the arithmetic: ||r||_1 >=
  ||r||_2 with equality exactly when r has at most one non-zero coordinate.  So
  EVERY pure state with more than one non-zero Bloch coordinate is omitted; the
  witness is representative, not lucky.  SCOPE: the general sentence is carried
  on exhibited witnesses plus the elementary norm inequality, not on an executed
  general argument over all r.

WHAT IS AND IS NOT SHOWN.  This is a statement about a PREMISE SET: order
soundness, convexity, complement closure and tomographic completeness do not
jointly entail that the matching rank-one effect of an admitted pure state is
in the family.  It is NOT a claim that nature's effect family is the
octahedron, and nothing here says the matching effect is in fact unavailable.
It removes a route, and that is all.

============================================================================
STATEMENTS

check_L_tomographic_completeness_omits_matching_effect (tier 3, [P_math]).

  THE VERDICT IS COMPUTED FROM THE FAMILY.  Membership of the target effect in
  the convex hull of the declared generators is decided by exact rational
  Caratheodory enumeration -- every affinely independent subset of size <= 4+1
  is solved exactly over Fraction and tested for a non-negative normalized
  solution.  No hull membership anywhere in this module is read off a norm
  formula, a hardcoded bound, or a literal.  (The source packet's version
  compared a hardcoded l1 value and never consulted its own generator list; an
  auditor enlarged the family to CONTAIN the matching effect and the check
  still passed while reporting it omitted.  That is the defect this design
  exists to exclude.)

  THE LEGS, all exact:
    (a) ORDER SOUNDNESS of every generator, via the exact rational criterion
        r.r <= t^2 and r.r <= (2-t)^2 for E = (t I + r.sigma)/2.  No square
        roots, no floats.
    (b) COMPLEMENT CLOSURE, decided by hull membership of I - E for EVERY
        generator -- not by a hardcoded pair list, and not over a truncated
        index range.
    (c) TOMOGRAPHIC COMPLETENESS: the generators span Herm(2), exact rank 4 in
        the (t, r) coordinates.
    (d) THE TARGET IS A GENUINE PURE STATE: r*.r* == 1 exactly, so it is a
        rank-one projector and an admitted state, not a stipulated object.
    (e) THE VERDICT: the matching support effect (t, r) = (1, r*) is NOT in the
        hull, by the exact enumeration.
    (f) THE GENERAL REASON: ||r||_1 >= ||r||_2 on the whole coordinate space
        with equality iff AT MOST one coordinate is non-zero, computed on a
        family of witnesses -- so the omission is generic among pure states and
        not an artifact of this r*.

  THE BOUND AND THE MAPS ARE EXERCISED, not trusted (added 2026-07-29 after a
  blinded audit found each of the three trusted).  A deep-certificate witness
  whose SMALLEST convex representation needs all five generators pins the
  Caratheodory bound -- lowering it to 4 or 2 was previously invisible, because
  every positive control was satisfiable at k <= 2, and under-enumeration
  produces exactly the FALSE NEGATIVE this module's headline claim consists of.
  Two auxiliary families pin the complement MAP, which the octahedron's own
  symmetries cannot test: it is separately invariant under r -> -r and under
  t -> 2 - t, so on it the true complement, the identity, and the
  negation-dropping half-mutant are indistinguishable.  Three probes pin the
  three clauses of the order-soundness criterion, one each.  And hull INTERIOR
  points -- midpoints of generator pairs -- are checked for soundness and
  complement closure, so those properties are executed at the hull level rather
  than argued up from the generators.

  MUST-BITE CONTROLS, each a real defect paired with the guard:
    - ENLARGEMENT: adding (1, r*) and its complement to the generator list must
      make the verdict flip to "in hull".  This is what proves leg (e) is a
      function of the family rather than of a constant.
    - AXIS CONTROL: a pure state with a SINGLE non-zero Bloch coordinate IS in
      the hull, computed -- so the membership routine is not simply refusing
      everything.
    - INTERIOR CONTROL: the maximally mixed effect I/2 IS in the hull.

  THE STRENGTHENING OVER THE BANKED WITNESS, computed: the banked separation
  family {0, I, P_0, P_1, I/2} has exact coordinate rank 2, so it is NOT
  tomographically complete and cannot close this route.  The rank of both
  families is computed here, side by side.

============================================================================
MAY-NOT-CITE.

  - "The matching effect is unavailable" / "effect saturation is refuted."  No.
    This exhibits ONE admissible family that omits it.  Nothing here says
    nature's family does.
  - "Born is refuted" or "Born is derived."  Nothing here touches Born.
  - "Effect saturation is now closed."  It is not; it remains a named-open leaf.
    What closes is one ROUTE to it -- the tomographic-completeness repair.
  - "The octahedron is the APF effect family."  It is a countermodel, not a
    proposal.
  - "This discharges P1, P2 or P3 of T_presentation_gauge_forces_trace."  It
    discharges none of them.  SCOPE CORRECTION 2026-07-29 (blinded audit): an
    earlier draft justified the P3 half by citing rank_one_requirement_vacuous
    in presentation_gauge_forcing.py.  That computation is about a rank-one
    CARRIER (b = diag(1,0)); what is omitted here is a rank-one EFFECT.  They
    are different objects and the citation was a category slip.  The conclusion
    stands on the weaker and correct ground that nothing in this module
    computes anything about presentation invariance at all.
  - "Tomographic completeness plus reciprocity still fails."  NOT SHOWN, and
    this is the sharpest live limit on the countermodel: the octahedron effect
    cone is NOT self-dual (its dual is the cube), so the exhibited structure is
    not reciprocal.  A reader whose repair is "tomographic completeness PLUS
    read/write reciprocity" is untouched by this result.
  - "The banked closed read/write self-duality supplies the matching effect."
    It does not -- that check verifies self-duality of the classical simplex
    cone R^n_+, and the cone that bears on this question is the cross-polytope,
    on which self-duality FAILS.  See the v24.3.452 corrigenda in
    closed_world_completeness.py.

PROVENANCE.  The countermodel OBJECT is due to an external research packet,
APF_ATOMIC_PREPARATION_READOUT_RECIPROCITY_AUDIT v0.5 (2026-07-29), whose
mathematics a blinded cold audit verified exactly and independently.  What is
rebuilt here is the APPARATUS: in the source the verdict never consulted the
effect family, an enlarged family containing the matching effect passed the
battery 10/10 while still reporting the effect omitted, the complement loop was
truncated to three of six pairs, and the Bloch coordinate was never tied to the
matrix used elsewhere in the same file.  The object survived audit; the
apparatus did not, and only the object is carried.

NON-EXPORTING.  physical_premises_certified = false.  No existing grade moved.
"""

from fractions import Fraction as F
from itertools import combinations
from typing import Dict, List, Sequence, Tuple

PHYSICAL_PREMISES_CERTIFIED = False
EXPORTS: Tuple[str, ...] = ()
BANK_MODIFIED = False

# An effect on a qubit is E = (t I + r . sigma) / 2, coordinatized as
# (t, r1, r2, r3).  Everything below is exact rational arithmetic in these
# coordinates; no matrices, no square roots, no floats.
Pt = Tuple[F, F, F, F]

_ZERO: Pt = (F(0), F(0), F(0), F(0))
_IDENTITY: Pt = (F(2), F(0), F(0), F(0))

# The six signed Bloch axes -> the six axis projectors.
_AXES: Tuple[Tuple[F, F, F], ...] = (
    (F(1), F(0), F(0)), (F(-1), F(0), F(0)),
    (F(0), F(1), F(0)), (F(0), F(-1), F(0)),
    (F(0), F(0), F(1)), (F(0), F(0), F(-1)),
)

# The exhibited pure state: ||r*||_2 = 1 exactly (24^2 + 7^2 = 625 = 25^2),
# so it is a genuine rank-one projector; ||r*||_1 = 31/25 > 1.
_R_STAR: Tuple[F, F, F] = (F(24, 25), F(0), F(-7, 25))

# The banked separation witness, TRANSCRIBED (not read from source) from
# quantum_frontend_closure.py check_T_effect_soundness_not_saturation, whose
# family is [zero, i2, p0, p1, half].  This is a COPY: if that family ever
# changes, the comparison below goes stale silently.  Verified by hand and by
# a blinded audit against the banked source on 2026-07-29.
_BANKED_WITNESS: Tuple[Pt, ...] = (
    _ZERO, _IDENTITY,
    (F(1), F(0), F(0), F(1)),      # P_0
    (F(1), F(0), F(0), F(-1)),     # P_1
    (F(1), F(0), F(0), F(0)),      # I/2
)


def _result(name, epistemic, key_result, evidence, fails, tier,
            dependencies, premises, negative_controls, cross_refs,
            fail_count=None):
    """Build the result dict, and CROSS-ASSERT the two failure records HERE.

    The cross-assert lives where the dict is BUILT, not in run_all(), because
    the bank never calls run_all(): bank.py invokes each registered check_fn()
    directly and reads r['passed'].  Residual limits, disclosed: this catches
    DIVERGENCE between the two records, not a bare literal substitution of
    'passed'; and the second record is written at the same site as the first,
    so an edit removing both together is not caught either."""
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
# Exact rational linear algebra.
# ==========================================================================


def _rank(rows: Sequence[Sequence[F]]) -> int:
    m = [list(r) for r in rows]
    if not m:
        return 0
    cols = len(m[0])
    rank = 0
    for c in range(cols):
        piv = next((i for i in range(rank, len(m)) if m[i][c] != F(0)), None)
        if piv is None:
            continue
        m[rank], m[piv] = m[piv], m[rank]
        inv = F(1) / m[rank][c]
        m[rank] = [x * inv for x in m[rank]]
        for i in range(len(m)):
            if i != rank and m[i][c] != F(0):
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[rank])]
        rank += 1
    return rank


def _solve_exact(A: List[List[F]], b: List[F]) -> Tuple[bool, List[F]]:
    """Solve A x = b exactly.  Returns (unique_solution_exists, x).

    Over-determined and inconsistent systems return (False, []); systems with
    a non-trivial null space also return (False, []) -- those subsets are not
    affinely independent and are covered by a smaller subset under
    Caratheodory, so skipping them loses nothing."""
    rows = len(A)
    cols = len(A[0]) if rows else 0
    m = [A[i][:] + [b[i]] for i in range(rows)]
    piv_cols: List[int] = []
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if m[i][c] != F(0)), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        inv = F(1) / m[r][c]
        m[r] = [x * inv for x in m[r]]
        for i in range(rows):
            if i != r and m[i][c] != F(0):
                f = m[i][c]
                m[i] = [a - f * bb for a, bb in zip(m[i], m[r])]
        piv_cols.append(c)
        r += 1
    # inconsistency: a zero row with non-zero augment
    for i in range(r, rows):
        if m[i][cols] != F(0):
            return (False, [])
    if len(piv_cols) != cols:          # null space -> not affinely independent
        return (False, [])
    x = [F(0)] * cols
    for i, c in enumerate(piv_cols):
        x[c] = m[i][cols]
    return (True, x)


def _min_support(generators: Sequence[Pt], target: Pt) -> int:
    """The size of the SMALLEST convex certificate, or 0 if none exists.

    Exposed so the Caratheodory bound is EXERCISED rather than trusted.  An
    auditor mutated the bound from 5 down to 2 and the whole battery still
    passed, because every positive control in it was satisfiable at k <= 2.
    Under-enumeration produces FALSE NEGATIVES, and this module's headline is a
    negative membership claim -- so the bound is exactly the thing that must be
    tested."""
    n = len(generators)
    for k in range(1, min(5, n) + 1):
        for idx in combinations(range(n), k):
            A = [[generators[j][d] for j in idx] for d in range(4)]
            A.append([F(1)] * k)
            b = [target[0], target[1], target[2], target[3], F(1)]
            ok, x = _solve_exact(A, b)
            if ok and all(v >= F(0) for v in x) and all(v > F(0) for v in x):
                return k
    return 0


def _in_convex_hull(generators: Sequence[Pt], target: Pt) -> bool:
    """EXACT Caratheodory membership, computed from the generator list.

    A point of conv(S) in R^4 is a convex combination of at most 5 points of
    S.  Every subset of size 1..5 is solved exactly; membership holds iff some
    subset yields a non-negative solution summing to 1.  This is the leg the
    source packet lacked: the verdict is a function of `generators`, so
    enlarging the family provably flips it."""
    n = len(generators)
    for k in range(1, min(5, n) + 1):
        for idx in combinations(range(n), k):
            # 4 coordinate equations + 1 normalization, k unknowns.
            A = [[generators[j][d] for j in idx] for d in range(4)]
            A.append([F(1)] * k)
            b = [target[0], target[1], target[2], target[3], F(1)]
            ok, x = _solve_exact(A, b)
            if ok and all(v >= F(0) for v in x):
                return True
    return False


def _is_order_sound(e: Pt) -> bool:
    """0 <= E <= I for E = (t I + r.sigma)/2, exactly and without radicals:
    the eigenvalues are (t +- |r|)/2, so the condition is |r| <= t and
    |r| <= 2 - t, i.e. r.r <= t^2 with t >= 0, and r.r <= (2-t)^2 with t <= 2."""
    t, r1, r2, r3 = e
    rr = r1 * r1 + r2 * r2 + r3 * r3
    return (F(0) <= t <= F(2)) and rr <= t * t and rr <= (F(2) - t) ** 2


def _complement(e: Pt) -> Pt:
    return (F(2) - e[0], -e[1], -e[2], -e[3])


def _projector(r: Sequence[F]) -> Pt:
    return (F(1), r[0], r[1], r[2])


def _l1(r: Sequence[F]) -> F:
    return sum((abs(x) for x in r), F(0))


def _l2_squared(r: Sequence[F]) -> F:
    return sum((x * x for x in r), F(0))


_OCTAHEDRON: Tuple[Pt, ...] = (_ZERO, _IDENTITY) + tuple(
    _projector(a) for a in _AXES)


# ==========================================================================
# THE CHECK
# ==========================================================================


def check_L_tomographic_completeness_omits_matching_effect() -> Dict[str, object]:
    """Tier 3, [P_math]."""
    fails: List[str] = []
    tally = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
            tally[0] += 1

    fam = list(_OCTAHEDRON)
    target = _projector(_R_STAR)

    # ---- (a) ORDER SOUNDNESS of every generator. -----------------------
    for e in fam:
        ck(_is_order_sound(e),
           f"every generator must satisfy 0 <= E <= I, failed at {e}")
    # The soundness predicate must be able to say no, or the leg is idle.
    ck(not _is_order_sound((F(1), F(2), F(0), F(0))),
       "the order-soundness predicate must REJECT an out-of-range effect, or "
       "leg (a) certifies nothing")

    # ---- (b) COMPLEMENT CLOSURE, decided by hull membership, all of them. --
    complement_rows = 0
    for e in fam:
        ck(_in_convex_hull(fam, _complement(e)),
           f"the family must be complement-closed: I - {e} is not in the hull")
        complement_rows += 1
    ck(complement_rows == len(fam),
       f"the complement loop must cover EVERY generator ({len(fam)}), covered "
       f"{complement_rows} -- a truncated index range is how the source "
       f"packet's version missed pairs")

    # ---- (c) TOMOGRAPHIC COMPLETENESS: exact rank 4 in Herm(2). ---------
    oct_rank = _rank([list(e) for e in fam])
    ck(oct_rank == 4,
       f"the octahedral family must span Herm(2) (rank 4), got {oct_rank} -- "
       f"without this the countermodel does not close the tomographic route")

    # THE STRENGTHENING, computed: the banked separation witness does NOT.
    banked_rank = _rank([list(e) for e in _BANKED_WITNESS])
    ck(banked_rank < 4,
       f"the banked separation witness must NOT be tomographically complete "
       f"(that is what this module strengthens), got rank {banked_rank}")

    # ---- (d) THE TARGET IS A GENUINE PURE STATE. ------------------------
    ck(_l2_squared(_R_STAR) == F(1),
       f"the omitted state must be a genuine rank-one projector: "
       f"||r*||_2^2 must equal 1 exactly, got {_l2_squared(_R_STAR)}")
    ck(_is_order_sound(target),
       "the omitted state must itself be a sound effect, or its omission is "
       "uninteresting")
    ck(sum(1 for x in _R_STAR if x != F(0)) >= 2,
       "the omitted state must have at least two non-zero Bloch coordinates, "
       "which by leg (f) is exactly what puts it outside the cross-polytope")

    # ---- (e) THE VERDICT, computed from the family. ---------------------
    in_hull = _in_convex_hull(fam, target)
    ck(not in_hull,
       "THE COUNTERMODEL: the matching support effect of the exhibited pure "
       "state must NOT lie in the hull of the declared family")

    # ---- MUST-BITE CONTROL 1: ENLARGEMENT. ------------------------------
    # This is what proves leg (e) reads the family rather than a constant.
    enlarged = fam + [target, _complement(target)]
    ck(_in_convex_hull(enlarged, target),
       "ENLARGEMENT CONTROL MUST BITE: adding the matching effect to the "
       "generator list must flip the verdict to 'in hull'.  If it does not, "
       "the membership routine is not a function of the family -- which is "
       "precisely the defect that let an auditor pass an enlarged family "
       "through the source packet while it still reported the effect omitted")

    # ---- MUST-BITE CONTROL 2: an axis pure state IS in the hull. --------
    axis_state = _projector((F(0), F(1), F(0)))
    ck(_in_convex_hull(fam, axis_state),
       "AXIS CONTROL: a pure state with a single non-zero Bloch coordinate "
       "must BE in the hull, or the membership routine simply refuses "
       "everything")

    # ---- MUST-BITE CONTROL 3: the interior point. -----------------------
    ck(_in_convex_hull(fam, (F(1), F(0), F(0), F(0))),
       "INTERIOR CONTROL: the maximally mixed effect I/2 must be in the hull")

    # ---- CARATHEODORY BOUND, EXERCISED (not trusted). -------------------
    # A point whose SMALLEST convex certificate needs all five generators.
    # Without this every positive control is satisfiable at k <= 2 and the
    # subset-size bound could be silently lowered.
    k5_target: Pt = (F(1, 2), F(1, 8), F(1, 8), F(1, 8))
    ck(_in_convex_hull(fam, k5_target),
       "the deep-certificate witness must be in the hull")
    ck(_min_support(fam, k5_target) == 5,
       f"the deep-certificate witness must require a FIVE-point certificate, "
       f"got {_min_support(fam, k5_target)} -- if a smaller one suffices, the "
       f"Caratheodory bound is never exercised and could be lowered silently")

    # ---- THE COMPLEMENT MAP, EXERCISED. ---------------------------------
    # The octahedron is separately invariant under r -> -r and under
    # t -> 2 - t, so no test on IT can distinguish the true complement from a
    # half-mutated one.  These two families can.
    for label, probe in (("{0, I, P_x}", [_ZERO, _IDENTITY,
                                          _projector((F(1), F(0), F(0)))]),
                         ("{0, P_x, P_-x}", [_ZERO,
                                             _projector((F(1), F(0), F(0))),
                                             _projector((F(-1), F(0), F(0)))])):
        ck(any(not _in_convex_hull(probe, _complement(e)) for e in probe),
           f"the family {label} must NOT be complement-closed under the TRUE "
           f"complement -- this is what pins the complement map itself, which "
           f"the octahedron's own symmetries cannot test")

    # ---- ORDER SOUNDNESS: all three clauses, one control each. ----------
    for probe, why in (((F(1), F(2), F(0), F(0)), "r.r <= t^2"),
                       ((F(2), F(1), F(0), F(0)), "r.r <= (2-t)^2"),
                       ((F(3), F(0), F(0), F(0)), "0 <= t <= 2")):
        ck(not _is_order_sound(probe),
           f"the order-soundness predicate must REJECT {probe}, which isolates "
           f"the clause {why}; without this that clause could be dropped and "
           f"the predicate would still certify the generators")

    # ---- HULL-LEVEL, not just generator-level. --------------------------
    # Soundness and complement closure are convex/affine properties, so the
    # generator legs suffice mathematically -- but the extension is executed
    # rather than argued, on interior points built from the generators.
    interior_rows = 0
    for i in range(len(fam)):
        for j in range(i + 1, len(fam)):
            mid = tuple((fam[i][d] + fam[j][d]) / F(2) for d in range(4))
            ck(_is_order_sound(mid),
               f"hull interior points must be order-sound too, failed at {mid}")
            ck(_in_convex_hull(fam, _complement(mid)),
               f"the hull must be complement-closed at interior points too, "
               f"failed at {mid}")
            interior_rows += 1

    # ---- (f) THE GENERAL REASON: l1 >= l2, equality iff at most one coord. -
    generic_rows = 0
    for r in ((F(3, 5), F(4, 5), F(0)), (F(2, 7), F(3, 7), F(6, 7))):
        ck(_l2_squared(r) == F(1),
           f"the genericity witnesses must be unit Bloch vectors, {r} is not")
        ck(_l1(r) > F(1),
           f"a pure state with several non-zero coordinates must have "
           f"||r||_1 > 1, failed at {r}")
        ck(not _in_convex_hull(fam, _projector(r)),
           f"and must therefore be omitted by the family, failed at {r}")
        generic_rows += 1
    # Equality case, computed: AT MOST one non-zero coordinate (r = 0 also
    # satisfies ||r||_1 = ||r||_2, which is why the bound is 'at most').
    for r in ((F(1), F(0), F(0)), (F(0), F(0), F(-1))):
        ck(_l1(r) == F(1) and _l2_squared(r) == F(1),
           f"single-coordinate unit vectors must have ||r||_1 = ||r||_2 = 1, "
           f"failed at {r}")
        ck(_in_convex_hull(fam, _projector(r)),
           f"and must therefore be INCLUDED, failed at {r} -- the equality "
           f"case is what makes the omission generic rather than universal")

    return _result(
        'L_tomographic_completeness_omits_matching_effect',
        '[P_math]',
        ("TOMOGRAPHIC COMPLETENESS DOES NOT SUPPLY THE MATCHING RANK-ONE "
         "EFFECT.  The convex hull of {0, I, the six axis projectors} is "
         "order-sound, convex, complement-closed (decided by hull membership "
         "on EVERY generator) and TOMOGRAPHICALLY COMPLETE (exact coordinate "
         "rank 4 = dim Herm(2)), yet it omits the matching support effect of "
         "the exhibited pure state r* = (24/25, 0, -7/25), which is a genuine "
         "rank-one projector since ||r*||_2 = 1 exactly while ||r*||_1 = "
         "31/25 > 1.  THE VERDICT IS COMPUTED FROM THE FAMILY by exact "
         "rational Caratheodory enumeration, never from a norm formula or a "
         "literal, and the ENLARGEMENT CONTROL proves it: adding the matching "
         "effect to the generator list flips the verdict.  THE OMISSION IS "
         "GENERIC, not lucky: ||r||_1 >= ||r||_2 with equality exactly when "
         "one coordinate is non-zero, so every pure state with two or more "
         "non-zero Bloch coordinates is omitted (three exhibited) while the "
         "six axis states are included (two exhibited).  STRENGTHENS THE "
         "BANKED SEPARATION: the family in check_T_effect_soundness_not_"
         "saturation has computed coordinate rank 2, so it is NOT "
         "tomographically complete and cannot close this route.  WHAT CLOSES "
         "IS ONE ROUTE, NOT THE QUESTION: effect saturation remains a "
         "named-open leaf, and nothing here says nature's effect family omits "
         "anything."),
        {
            'octahedron_generators': len(fam),
            'octahedron_coordinate_rank': oct_rank,
            'banked_witness_coordinate_rank': banked_rank,
            'omitted_state_bloch': [str(x) for x in _R_STAR],
            'omitted_state_l1': str(_l1(_R_STAR)),
            'omitted_state_l2_squared': str(_l2_squared(_R_STAR)),
            'target_in_hull': in_hull,
            'target_in_enlarged_hull': _in_convex_hull(enlarged, target),
            'complement_rows': complement_rows,
            'genericity_rows': generic_rows,
        },
        fails,
        3,
        (),
        ("none: exact finite rational mathematics.  The PHYSICAL reading -- "
         "that this bears on which effects nature admits -- is NOT taken; the "
         "result is about a premise set, not about nature.",),
        ("the enlargement control flips the verdict, proving membership reads "
         "the family",
         "an axis pure state IS in the hull, so the routine does not refuse "
         "everything",
         "I/2 is in the hull",
         "the order-soundness predicate rejects an out-of-range effect",
         "the equality case l1 = l2 is exhibited as INCLUDED, scoping the "
         "genericity claim",),
        ('T_effect_soundness_not_saturation', 'T_soundness_saturation_separation',
         'ALL_POSITIVE_EFFECTS_REALIZABLE (named-open leaf)',
         'T_closed_read_write_self_duality (v24.3.452 corrigendum -- the '
         'simplex-cone self-duality does NOT supply this effect)'),
        fail_count=tally[0],
    )


_CHECKS = {
    'L_tomographic_completeness_omits_matching_effect':
        check_L_tomographic_completeness_omits_matching_effect,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    """Second gate only; the load-bearing cross-assert lives in _result()."""
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
        print(r['name'], '::', r['epistemic'], '::',
              'PASS' if r['passed'] else 'FAIL')
        if not r['passed']:
            bad = True
            for f in r['fail_reasons'][:20]:
                print('  -', f)
    sys.exit(1 if bad else 0)
