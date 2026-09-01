"""An equal-cost atomic frame forces the trace, and needs n^2 members.

Staged 2026-07-29 (v24.3.456 slot) and held pending audits per the standing
rule that an audit of a source packet is not an audit of the code that enters
the bank.

AUDIT RECORD: blinded cold LAND-WITH-FIXES 0.86 (2026-07-29, statement + code
only, no lineage; the auditor rebuilt the claim in a different parametrization
and confirmed it at n = 2..5) + LAND-WITH-FIXES 0.85 (2026-08-04, D1-queue
blinded cold audit; the six .456-owed fixes found uncarried and carried by a
separate fix seat, auditor's escapes re-run) + LAND-WITH-FIXES 0.88
(2026-08-04, third blinded cold audit, zero arithmetic disagreements; MAJOR-1
-- the single-deletion legs are a row-count tautology for any n^2-ray family,
now disclosed in the statement, (c), (d) and key_result and removed from
negative_controls -- plus five MINORs carried by a separate cold fix seat,
auditor's battery re-run post-fix).  Fixes carried by separate cold fix seats
each round.  Banked as v24.3.466 (2026-08-04).

WHAT THIS ADDS, AGAINST THE PRIOR ART (read this first).

check_T_presentation_gauge_forces_trace (presentation_gauge_forcing.py,
v24.3.443) reaches psi = c Tr from a presentation GROUP with scalar commutant.
This module banks the ORBIT-SIDE route to the same conclusion: uniform cost on a
rich enough family of rank-one atomic rays.  The two are assumption-disjoint --
one uses a group action, the other a spanning ray family -- and neither
dominates.

  THE THEOREM.  Let R be Hermitian on C^n and let the normalized self-cost
  q_R(v) = v* R v / <v,v> be EQUAL across the family of rank-one rays

      e_i   (coordinate),   e_i + e_j   (real),   e_i + i e_j   (quarter-phase)

  for all i < j.  Then R = c I.  The family has exactly n^2 members
  (n + 2 * C(n,2) = n^2), and n^2 is CARDINALITY MINIMAL: m rays impose at most
  m - 1 independent equal-cost equations on an n^2-parameter Hermitian R, so
  m >= n^2 is forced.  Deleting any single member leaves a non-scalar
  survivor -- a row-count consequence that holds for ANY family of n^2 rays
  (n^2 - 1 rays give at most n^2 - 2 equations, nullity >= 2), not a special
  property of this frame.

  BOTH QUADRATURES ARE NECESSARY, and each failure is exhibited:
    - drop the quarter-phase rays and I + sigma_y/2 survives (imaginary
      off-diagonal unconstrained);
    - drop the real superpositions and I + sigma_x/2 survives (real
      off-diagonal unconstrained).
  Both survivors are computed PSD, so POSITIVITY DOES NOT RESCUE a deficient
  frame -- which is the repair a reader reaches for first.

WHAT THIS IS NOT.  A source packet presented this route as reducing the
disputed uniform-cost premise "to orbit typing rather than a new cost axiom."
It is not a reduction.  One unproven premise (uniform elementary self-cost) is
replaced by THREE -- frame transitivity, orbit-separator typing, and the type
identification that a rank-one projector IS a one-separator structure -- and
none of the three is executed anywhere.  Nor does the banked count-only cost
theorem supply the last of them: symmetry_cost_floor prices #separated_pairs in
the ORBIT PARTITION OF A FINITE CARRIER, which is a different carrier from a
projective ray in M_n(C), and the type-transfer between them is the whole
content and is not even given a definition.  The mathematics below is exact and
premise-free; the PHYSICAL reading that these rays carry one elementary cost is
neither derived nor claimed here.

============================================================================
STATEMENTS

check_L_atomic_equal_cost_frame_forces_trace (tier 3, [P_math]).

  (a) THE FRAME FORCES THE TRACE, SOLVED: the equal-cost linear system is built
      from the rays and solved exactly over Q at n = 2, 3, 4.  The solution
      space has dimension exactly 1 and is spanned by I -- asserted by
      exhibiting that the returned basis vector IS the identity, not merely by
      counting the nullity, since a nullity count cannot tell which line
      survived.

  (b) THE COUNT AND THE OBJECT: the frame has exactly n^2 members, asserted
      against n^2 and against the enumeration n + 2*C(n,2); and each ray
      vector is pinned by value to its label -- the advertised {0, 1, i}
      entry pattern is rebuilt from the name and asserted entrywise, at
      every n run.

  (c) CARDINALITY MINIMALITY: for every ray count m the rank of the system
      built from those m rays is computed and is at most m - 1.  The per-m
      bound is a row-count identity (m rays yield m - 1 difference rows), so
      that leg exercises _rank and cannot fail for any frame; the computed
      content is the full-frame rank n^2 - 1, and the m >= n^2 conclusion is
      argued from the bound plus nullity 1.  Executed at n = 2, 3.

  (d) SINGLE DELETIONS: deleting any single member of the full frame raises
      the nullity above 1, at n = 2 and n = 3, every deletion executed.
      This is a row-count consequence for ANY family of n^2 rays (one
      deletion leaves n^2 - 2 rows, so nullity >= 2); the legs cannot fail
      for any frame passing the count legs and are retained as a
      _rref_nullspace exercise, not as a property of this frame.

  (e) BOTH QUADRATURES NECESSARY, with the survivors EXHIBITED and verified:
      without the quarter-phase rays I + sigma_y/2 satisfies every remaining
      equal-cost equation and is non-scalar; without the real superpositions
      I + sigma_x/2 does.  Each survivor is verified to be Hermitian, non-scalar
      and PSD, and verified to actually SATISFY the reduced system -- so this is
      a construction, not a nullity count.  Executed at n = 2 only, where each
      quadrature family has exactly one member, dropped by name.

  (f) POSITIVITY DOES NOT RESCUE: both survivors are PSD (det and trace
      computed positive, which decides positive DEFINITENESS at 2x2; PSD a
      fortiori), so adding a positivity premise to a deficient frame does not
      restore the conclusion.

  (g) OFF-FRAME COST VALUES: _cost_row is tied by VALUE to an independent
      complex-arithmetic evaluation of v*Rv and <v,v> -- explicit complex
      matrix-vector products over exact rationals -- on probe rays whose
      entries have nonzero real and imaginary parts and non-unit norms,
      against Hermitian R with nonzero Re and Im off-diagonal entries.
      Executed at n = 2 (4 probes x 3 matrices) and n = 3 (2 probes x 2
      matrices).  Each matrix literal is machine-checked to have nonzero Re
      and Im in every off-diagonal entry, symmetric to the probe-quality leg.

============================================================================
MAY-NOT-CITE.

  - "The uniform-cost premise is reduced to orbit typing."  It is not.  One
    premise is replaced by three, none of them executed.
  - "Paper 40's count-only cost theorem proves every rank-one projector is one
    separator."  It does not.  symmetry_cost_floor prices separated pairs in an
    orbit partition of a finite carrier; the transfer to a projective ray is
    undefined, let alone proved.
  - "Born is derived", or "the trace is derived from A1."  Nothing here.  The
    conclusion R = cI is a fact about a linear system, conditional on a physical
    equal-cost premise that is NOT supplied.
  - "This supersedes T_presentation_gauge_forces_trace."  It does not.  The two
    routes are assumption-disjoint and neither dominates; this one needs a
    spanning ray family where that one needs a group with scalar commutant.
  - "n^2 rays are physically available."  Not shown.  Which rays are admitted is
    exactly the open question.

PROVENANCE.  The frame OBJECT is from the external packet
APF_GAUGE_TRACE_CONNECTED_LOOP_AND_ATOMIC_FRAME v0.4 (2026-07-29), where a
blinded cold audit found it correct, exact and mutation-resistant -- including
an attempted positivity rescue of a deficient frame, which failed.  It was one
of the few items in that packet whose apparatus survived.  Rebuilt here to solve
and exhibit rather than to count, and re-sited: the source presented it as a
premise reduction, which it is not.

NON-EXPORTING.  physical_premises_certified = false.  No existing grade moved.
"""

from fractions import Fraction as F
from typing import Dict, List, Sequence, Tuple

PHYSICAL_PREMISES_CERTIFIED = False
EXPORTS: Tuple[str, ...] = ()
BANK_MODIFIED = False

# A Hermitian R on C^n is coordinatized by n^2 REAL parameters, in this order:
#   R_ii for i in 0..n-1            (n of them)
#   Re R_ij, Im R_ij for i < j      (2 * C(n,2) of them)
# A ray is (v_re, v_im), a complex vector given by its real and imaginary parts.
Ray = Tuple[Tuple[F, ...], Tuple[F, ...]]


def _param_index(n: int) -> Tuple[Dict[int, int], Dict[Tuple[int, int], int],
                                  Dict[Tuple[int, int], int], int]:
    diag = {i: i for i in range(n)}
    re_ix: Dict[Tuple[int, int], int] = {}
    im_ix: Dict[Tuple[int, int], int] = {}
    p = n
    for i in range(n):
        for j in range(i + 1, n):
            re_ix[(i, j)] = p
            im_ix[(i, j)] = p + 1
            p += 2
    return diag, re_ix, im_ix, p


def _cost_row(v: Ray, n: int) -> Tuple[List[F], F]:
    """The linear functional q_R(v) in the real parameters, and <v,v>.

    q_R(v) = sum_i |v_i|^2 R_ii + 2 sum_{i<j} (a_ij Re R_ij - b_ij Im R_ij),
    where a_ij + i b_ij = conj(v_i) v_j."""
    diag, re_ix, im_ix, total = _param_index(n)
    row = [F(0)] * total
    vr, vi = v
    norm = F(0)
    for i in range(n):
        m2 = vr[i] * vr[i] + vi[i] * vi[i]
        row[diag[i]] += m2
        norm += m2
    for i in range(n):
        for j in range(i + 1, n):
            # conj(v_i) v_j = (vr_i - i vi_i)(vr_j + i vi_j)
            a = vr[i] * vr[j] + vi[i] * vi[j]
            b = vr[i] * vi[j] - vi[i] * vr[j]
            row[re_ix[(i, j)]] += F(2) * a
            row[im_ix[(i, j)]] += F(-2) * b
    return row, norm


def _full_frame(n: int) -> List[Tuple[str, Ray]]:
    """The n^2 atomic rays: coordinate, real superposition, quarter-phase."""
    rays: List[Tuple[str, Ray]] = []
    for i in range(n):
        vr = [F(0)] * n
        vi = [F(0)] * n
        vr[i] = F(1)
        rays.append((f"e{i}", (tuple(vr), tuple(vi))))
    for i in range(n):
        for j in range(i + 1, n):
            vr = [F(0)] * n
            vi = [F(0)] * n
            vr[i] = F(1)
            vr[j] = F(1)
            rays.append((f"e{i}+e{j}", (tuple(vr), tuple(vi))))
    for i in range(n):
        for j in range(i + 1, n):
            vr = [F(0)] * n
            vi = [F(0)] * n
            vr[i] = F(1)
            vi[j] = F(1)
            rays.append((f"e{i}+ie{j}", (tuple(vr), tuple(vi))))
    return rays


def _equal_cost_system(rays: Sequence[Tuple[str, Ray]], n: int) -> List[List[F]]:
    """Rows expressing q_R(v_k)/<v_k,v_k> = q_R(v_0)/<v_0,v_0>."""
    if not rays:
        return []
    base_row, base_norm = _cost_row(rays[0][1], n)
    eqs: List[List[F]] = []
    for _, v in rays[1:]:
        row, norm = _cost_row(v, n)
        eqs.append([a / norm - b / base_norm for a, b in zip(row, base_row)])
    return eqs


def _rref_nullspace(rows: List[List[F]], ncols: int) -> List[List[F]]:
    """Exact null space basis of the system."""
    m = [r[:] for r in rows]
    piv_cols: List[int] = []
    r = 0
    for c in range(ncols):
        p = next((i for i in range(r, len(m)) if m[i][c] != F(0)), None)
        if p is None:
            continue
        m[r], m[p] = m[p], m[r]
        inv = F(1) / m[r][c]
        m[r] = [x * inv for x in m[r]]
        for i in range(len(m)):
            if i != r and m[i][c] != F(0):
                f = m[i][c]
                m[i] = [a - f * b for a, b in zip(m[i], m[r])]
        piv_cols.append(c)
        r += 1
    free = [c for c in range(ncols) if c not in piv_cols]
    basis: List[List[F]] = []
    for fc in free:
        vec = [F(0)] * ncols
        vec[fc] = F(1)
        for i, pc in enumerate(piv_cols):
            vec[pc] = -m[i][fc]
        basis.append(vec)
    return basis


def _rank(rows: List[List[F]], ncols: int) -> int:
    return ncols - len(_rref_nullspace(rows, ncols))


def _identity_params(n: int) -> List[F]:
    _, _, _, total = _param_index(n)
    vec = [F(0)] * total
    for i in range(n):
        vec[i] = F(1)
    return vec


def _is_scalar(vec: Sequence[F], n: int) -> bool:
    diag, re_ix, im_ix, _ = _param_index(n)
    if any(vec[re_ix[k]] != F(0) or vec[im_ix[k]] != F(0) for k in re_ix):
        return False
    return all(vec[diag[i]] == vec[diag[0]] for i in range(n))


def _result(name, epistemic, key_result, evidence, fails, tier,
            dependencies, premises, negative_controls, cross_refs,
            fail_count=None):
    """Build the result dict, and CROSS-ASSERT the two failure records HERE.

    The cross-assert lives where the dict is BUILT, because the bank never calls
    run_all().  Disclosed residual limits: it catches DIVERGENCE between the two
    records, not a bare literal substitution of 'passed'; and both records are
    written at the same site, so an edit removing both is not caught."""
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


def check_L_atomic_equal_cost_frame_forces_trace() -> Dict[str, object]:
    """Tier 3, [P_math]."""
    fails: List[str] = []
    tally = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
            tally[0] += 1

    counts: Dict[int, int] = {}
    nullities: Dict[int, int] = {}
    dims_run: List[int] = []
    deletion_rows = 0
    pinned_rays = 0
    for n in (2, 3, 4):
        dims_run.append(n)
        _, _, _, total = _param_index(n)
        ck(total == n * n,
           f"the Hermitian parameter count must be n^2 (n={n}), got {total}")
        frame = _full_frame(n)
        # ---- (b) THE COUNT. ---------------------------------------------
        ck(len(frame) == n * n,
           f"the frame must have exactly n^2 = {n * n} members (n={n}), got "
           f"{len(frame)}")
        ck(len(frame) == n + 2 * (n * (n - 1) // 2),
           f"the frame count must match the enumeration n + 2*C(n,2) (n={n})")
        ck(len({name for name, _ in frame}) == len(frame),
           f"frame members must be distinct (n={n})")
        counts[n] = len(frame)

        # The frame OBJECT, pinned by value: rebuild each advertised vector
        # from its label ({0, 1, i} entry pattern) and assert entrywise
        # equality, tying vector to label.
        for nm, (vr_t, vi_t) in frame:
            evr = [F(0)] * n
            evi = [F(0)] * n
            if "+ie" in nm:
                left, right = nm.split("+ie")
                evr[int(left[1:])] = F(1)
                evi[int(right)] = F(1)
            elif "+e" in nm:
                left, right = nm.split("+e")
                evr[int(left[1:])] = F(1)
                evr[int(right)] = F(1)
            else:
                evr[int(nm[1:])] = F(1)
            ck((tuple(evr), tuple(evi)) == (vr_t, vi_t),
               f"ray {nm} must carry exactly the entries its label "
               f"advertises (n={n}): got re={vr_t}, im={vi_t}")
            pinned_rays += 1

        # ---- (a) THE FRAME FORCES THE TRACE, SOLVED. --------------------
        eqs = _equal_cost_system(frame, n)
        basis = _rref_nullspace(eqs, total)
        nullities[n] = len(basis)
        ck(len(basis) == 1,
           f"the equal-cost solution space must be ONE-dimensional (n={n}), "
           f"got {len(basis)}")
        # Which line survived, EXHIBITED -- a nullity count cannot say.
        if len(basis) == 1:
            v = basis[0]
            ck(_is_scalar(v, n),
               f"the surviving line must be SCALAR (n={n}); a nullity of 1 "
               f"alone does not say which line it is")
            ident = _identity_params(n)
            lead = next((x for x in v if x != F(0)), F(1))
            ck([x / lead for x in v] == ident,
               f"the surviving line must be spanned by the IDENTITY (n={n})")

        # _is_scalar's diagonal-constancy clause, exercised on every run:
        # zero off-diagonals with unequal diagonals is not scalar.
        nonconst = _identity_params(n)
        nonconst[1] = F(2)
        ck(not _is_scalar(nonconst, n),
           f"_is_scalar must reject a zero-off-diagonal vector with unequal "
           f"diagonals (n={n})")

        # ---- (c) CARDINALITY MINIMALITY.  The per-m bound r <= m - 1 is a
        # row-count identity (m rays yield m - 1 rows) and cannot fail for
        # any frame; the contentful leg is the full-frame rank n^2 - 1. ----
        if n <= 3:
            for m in range(1, len(frame) + 1):
                sub = frame[:m]
                r = _rank(_equal_cost_system(sub, n), total)
                ck(r <= m - 1,
                   f"m rays can impose at most m-1 independent equal-cost "
                   f"equations (n={n}, m={m}); got rank {r}")
            ck(_rank(eqs, total) == total - 1,
               f"the full frame must impose exactly n^2 - 1 independent "
               f"equations (n={n})")

        # ---- (d) IRREDUNDANCY: every single deletion. -------------------
        if n <= 3:
            # A row-count consequence for ANY n^2-ray family (one deletion
            # leaves n^2 - 2 rows, nullity >= 2); retained as a
            # _rref_nullspace exercise, not as a property of this frame.
            for k in range(len(frame)):
                reduced = frame[:k] + frame[k + 1:]
                b2 = _rref_nullspace(_equal_cost_system(reduced, n), total)
                ck(len(b2) > 1,
                   f"deleting frame member {frame[k][0]} must raise the "
                   f"nullity above 1 (n={n}), got {len(b2)}")
                deletion_rows += 1

    ck(deletion_rows == 2 * 2 + 3 * 3,
       f"the single-deletion legs must execute for every frame member at "
       f"n = 2 (4 members) and n = 3 (9 members); got {deletion_rows}")

    # ---- (e) + (f) BOTH QUADRATURES, survivors EXHIBITED and PSD (n = 2,
    # where each quadrature family has exactly one member). ---------------
    n = 2
    _, _, _, total = _param_index(n)
    diag, re_ix, im_ix, _ = _param_index(n)
    frame = _full_frame(n)
    quadrature_rows = 0
    survivors: Dict[str, List[str]] = {}
    for label, dropped_prefix, survivor in (
            ("no_quarter_phase", "e0+ie1", "sigma_y"),
            ("no_real_superposition", "e0+e1", "sigma_x")):
        reduced = [(nm, v) for nm, v in frame if nm != dropped_prefix]
        ck(len(reduced) == len(frame) - 1,
           f"exactly one ray must be dropped for {label} (n = 2: each "
           f"quadrature family has one member, matched by name)")
        eqs = _equal_cost_system(reduced, n)
        # The survivor, WRITTEN DOWN and then verified to satisfy the system.
        R = [F(0)] * total
        R[diag[0]] = F(1)
        R[diag[1]] = F(1)
        if survivor == "sigma_y":
            R[im_ix[(0, 1)]] = F(1, 2)
        else:
            R[re_ix[(0, 1)]] = F(1, 2)
        satisfies = all(sum(a * b for a, b in zip(row, R)) == F(0)
                        for row in eqs)
        ck(satisfies,
           f"the exhibited survivor I + {survivor}/2 must SATISFY the reduced "
           f"equal-cost system ({label}) -- a nullity count is not a witness")
        ck(not _is_scalar(R, n),
           f"the survivor must be NON-SCALAR ({label}), or the quadrature is "
           f"not shown necessary")
        # det > 0 and trace > 0, computed exactly: positive definite at
        # 2x2, hence PSD.
        off2 = R[re_ix[(0, 1)]] ** 2 + R[im_ix[(0, 1)]] ** 2
        det = R[diag[0]] * R[diag[1]] - off2
        trace = R[diag[0]] + R[diag[1]]
        ck(det > F(0) and trace > F(0),
           f"the survivor must be PSD ({label}) -- POSITIVITY DOES NOT RESCUE "
           f"a deficient frame; det={det}, tr={trace}")
        # And the FULL frame must exclude it, or the deletion is not what does
        # the work.
        full_eqs = _equal_cost_system(frame, n)
        ck(not all(sum(a * b for a, b in zip(row, R)) == F(0)
                   for row in full_eqs),
           f"the FULL frame must EXCLUDE the survivor ({label}), or the "
           f"dropped quadrature is not load-bearing")
        survivors[label] = [str(x) for x in R]
        quadrature_rows += 1

    # ---- (g) OFF-FRAME COST VALUES, tied by VALUE. ----------------------
    # _cost_row's real-coordinatized row, contracted with a Hermitian R's
    # parameter vector, is compared by exact value against an independent
    # evaluation of v*Rv by explicit complex matrix-vector arithmetic over
    # (re, im) Fraction pairs; <v,v> is compared against v*Iv by the same
    # route.  The probe rays have nonzero real and imaginary parts in every
    # entry and non-unit norms, so they lie off the frame, whose entries
    # are in {0, 1, i}.  Each R is written down twice, as a parameter
    # vector and as a complex matrix literal, so the two routes share no
    # construction code.
    def cmul(x, y):
        return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])

    def cconj(x):
        return (x[0], -x[1])

    def herm_form(v, rmat, dim):
        """v* R v by explicit complex matrix-vector arithmetic."""
        vre, vim = v
        vc = [(vre[i], vim[i]) for i in range(dim)]
        acc = (F(0), F(0))
        for i in range(dim):
            for j in range(dim):
                t = cmul(cmul(cconj(vc[i]), rmat[i][j]), vc[j])
                acc = (acc[0] + t[0], acc[1] + t[1])
        return acc

    probes_and_mats = [
        (2,
         [("2+3i,5-7i", ((F(2), F(5)), (F(3), F(-7)))),
          ("1/2+i/3,-2+i", ((F(1, 2), F(-2)), (F(1, 3), F(1)))),
          ("3-2i,-1+4i", ((F(3), F(-1)), (F(-2), F(4)))),
          ("-5+2i,7+3i", ((F(-5), F(7)), (F(2), F(3))))],
         [("R1", [F(1), F(2), F(3), F(4)],
           [[(F(1), F(0)), (F(3), F(4))],
            [(F(3), F(-4)), (F(2), F(0))]]),
          ("R2", [F(-1), F(1, 2), F(2), F(-5)],
           [[(F(-1), F(0)), (F(2), F(-5))],
            [(F(2), F(5)), (F(1, 2), F(0))]]),
          ("R3", [F(7), F(3), F(-1, 3), F(2)],
           [[(F(7), F(0)), (F(-1, 3), F(2))],
            [(F(-1, 3), F(-2)), (F(3), F(0))]])]),
        (3,
         [("1+2i,-3+i,2-5i",
           ((F(1), F(-3), F(2)), (F(2), F(1), F(-5)))),
          ("1/2-i,2+3i,-1+i/4",
           ((F(1, 2), F(2), F(-1)), (F(-1), F(3), F(1, 4))))],
         [("R4",
           [F(1), F(2), F(3), F(1), F(2), F(-2), F(1), F(3), F(-1)],
           [[(F(1), F(0)), (F(1), F(2)), (F(-2), F(1))],
            [(F(1), F(-2)), (F(2), F(0)), (F(3), F(-1))],
            [(F(-2), F(-1)), (F(3), F(1)), (F(3), F(0))]]),
          ("R5",
           [F(-1), F(4), F(1, 2), F(-3), F(1, 2), F(1), F(-1), F(2), F(3)],
           [[(F(-1), F(0)), (F(-3), F(1, 2)), (F(1), F(-1))],
            [(F(-3), F(-1, 2)), (F(4), F(0)), (F(2), F(3))],
            [(F(1), F(1)), (F(2), F(-3)), (F(1, 2), F(0))]])]),
    ]
    value_ties = 0
    off_frame_probes = 0
    matrix_quality_legs = 0
    for dim, probes, mats in probes_and_mats:
        ident_mat = [[(F(1) if i == j else F(0), F(0)) for j in range(dim)]
                     for i in range(dim)]
        # Matrix quality, machine-checked symmetric to the probe-quality
        # leg: every off-diagonal entry of every R literal has nonzero Re
        # and nonzero Im.
        for rname, params, rmat in mats:
            ck(all(rmat[i][j][0] != F(0) and rmat[i][j][1] != F(0)
                   for i in range(dim) for j in range(dim) if i != j),
               f"matrix {rname} must have nonzero Re and Im in every "
               f"off-diagonal entry (n={dim})")
            matrix_quality_legs += 1
        for pname, v in probes:
            vre, vim = v
            ck(all(vre[i] != F(0) and vim[i] != F(0) for i in range(dim)),
               f"probe {pname} must have nonzero real and imaginary parts "
               f"in every entry (n={dim})")
            row, norm = _cost_row(v, dim)
            den = herm_form(v, ident_mat, dim)
            ck(den[1] == F(0),
               f"<v,v> must be real (n={dim}, probe {pname}); independent "
               f"route gave Im part {den[1]}")
            ck(norm == den[0] and norm != F(1),
               f"_cost_row's <v,v> must equal the independent complex-route "
               f"v*Iv by VALUE and be non-unit (n={dim}, probe {pname}): "
               f"{norm} vs {den[0]}")
            off_frame_probes += 1
            for rname, params, rmat in mats:
                num = herm_form(v, rmat, dim)
                ck(num[1] == F(0),
                   f"v*Rv must be real for Hermitian {rname} (n={dim}, "
                   f"probe {pname}); independent route gave Im {num[1]}")
                contracted = sum(a * b for a, b in zip(row, params))
                ck(contracted == num[0],
                   f"_cost_row contracted with {rname} must equal the "
                   f"independent complex-route v*Rv by VALUE (n={dim}, "
                   f"probe {pname}): {contracted} vs {num[0]}")
                value_ties += 1

    return _result(
        'L_atomic_equal_cost_frame_forces_trace',
        'P_math',
        ("AN EQUAL-COST ATOMIC FRAME FORCES THE TRACE, AND NEEDS n^2 MEMBERS.  "
         "Equal normalized self-cost q_R(v) = v*Rv/<v,v> across the n^2 rank-one "
         "rays {e_i, e_i + e_j, e_i + i e_j} forces R = cI: the system is SOLVED "
         "exactly over Q at n = 2, 3, 4, the solution space is one-dimensional, "
         "and the surviving line is EXHIBITED to be the identity rather than "
         "merely counted -- a nullity of 1 does not say which line survived.  "
         "CARDINALITY MINIMALITY: m rays impose at most m - 1 independent "
         "equations -- a row-count identity, since m rays yield m - 1 "
         "difference rows, so the per-m leg exercises _rank rather than "
         "distinguishing this frame.  The computed content is the full-frame "
         "rank n^2 - 1; the conclusion m >= n^2 is argued from the row-count "
         "bound plus the need for nullity 1 on n^2 parameters.  "
         "Single deletions raise the nullity at n = 2 and "
         "3, every deletion executed; nullity >= 2 after one deletion is the "
         "same row-count identity, holding for ANY n^2-ray family, retained "
         "as a solver exercise.  BOTH "
         "QUADRATURES ARE NECESSARY (executed at n = 2, where each quadrature "
         "family has exactly one member, dropped by name), with survivors "
         "written down and verified to satisfy the reduced system: drop the "
         "quarter-phase ray and I + sigma_y/2 survives, drop the real "
         "superposition and I + sigma_x/2 survives, each non-scalar, each "
         "verified EXCLUDED by the full frame.  POSITIVITY DOES NOT RESCUE: "
         "both survivors are PSD (det and trace computed positive, which "
         "decides positive definiteness at 2x2, PSD a fortiori), so adding "
         "positivity to a deficient frame does "
         "not restore the conclusion.  _cost_row IS TIED BY VALUE on "
         "off-frame probe rays -- entries with nonzero real and imaginary "
         "parts, non-unit norms -- to an independent complex-arithmetic "
         "evaluation of v*Rv and <v,v>, against Hermitian R with nonzero Re "
         "and Im off-diagonal entries, at n = 2 and 3.  THIS IS NOT A "
         "PREMISE REDUCTION: the source framing that uniform cost reduces to "
         "orbit typing replaces one unproven premise with three, none executed, "
         "and the banked count-only cost theorem does NOT supply the type "
         "identification -- symmetry_cost_floor prices separated pairs in the "
         "orbit partition of a finite carrier, a different carrier from a "
         "projective ray.  The mathematics here is premise-free; the physical "
         "equal-cost reading is neither derived nor claimed."),
        {
            'dimensions': dims_run,
            'frame_sizes': {str(k): v for k, v in counts.items()},
            'solution_dimensions': {str(k): v for k, v in nullities.items()},
            'single_deletion_rows': deletion_rows,
            'label_pinned_rays': pinned_rays,
            'matrix_quality_legs': matrix_quality_legs,
            'quadrature_rows': quadrature_rows,
            'exhibited_survivors': survivors,
            'off_frame_probes': off_frame_probes,
            'off_frame_value_ties': value_ties,
        },
        fails,
        3,
        (),
        ("none for the mathematics.  The PHYSICAL premise that these rays carry "
         "one elementary separator cost is NOT supplied here, and the source's "
         "claim that it reduces to orbit typing is refused in the docstring.",),
        ("the surviving line is exhibited as the identity, not counted",
         "each ray vector is pinned entrywise to its label",
         "each quadrature survivor is verified to SATISFY the reduced system "
         "and to be EXCLUDED by the full one",
         "both survivors are computed PSD, so positivity does not rescue",
         "_cost_row equals an independent complex-route v*Rv and <v,v> by "
         "VALUE on off-frame probes",),
        ('T_presentation_gauge_forces_trace (assumption-disjoint sibling route)',
         'L_presentation_gauge_invariant_lines',
         'L_cost_floor_at_maximal_symmetry (does NOT supply the type '
         'identification -- different carrier)'),
        fail_count=tally[0],
    )


_CHECKS = {
    'L_atomic_equal_cost_frame_forces_trace':
        check_L_atomic_equal_cost_frame_forces_trace,
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
