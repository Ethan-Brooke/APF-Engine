"""What the admitted presentation family is, and what it cannot see.

WHAT THIS ADDS, AGAINST THE PRIOR ART (read this first).

apf/presentation_gauge_forcing.py (v24.3.443) runs its forcing on an admitted
generator family -- transpositions and quarter-phases -- and carries a subgroup
reading as a named failure mode.  apf/gauge_without_sandwich_countermodel.py
(v24.3.446) computes that under that finite family the covariant-map space is
strictly larger than under the full group, and that the extra direction is
dephasing.  Neither module computes WHAT the admitted family is as a group.
This module mechanizes that; the project header already carries the same finding
in prose, so the contribution is execution, not discovery.

This module computes four things and nothing else:

  (a) every admitted generator is MONOMIAL -- one nonzero entry per row and per
      column -- and the group they generate is monomial throughout, of order
      4^n * n!;
  (b) that group sits STRICTLY INSIDE the normalizer of the diagonal MASA:
      diag((3+4i)/5, 1) is unitary, monomial, normalizes the MASA, and is not in
      it.  The relation is INCLUSION, not identity;
  (c) covariance of the diagonal conditional expectation under conjugation by U
      holds for EVERY element of the admitted group (exhaustive, 32 and 384) and
      FAILS for one exhibited non-monomial unitary on the basis-projector probe,
      which the naive all-ones probe passes.  SCOPE, after audit: the forward
      direction is exhaustive over the group; the converse is ONE witness at
      n = 2, so this is an instance and not a computed equivalence.  The
      one-line reason it is an equivalence -- U E_kk U* diagonal forces one
      nonzero per column -- is stated, not executed;
  (d) the covariant-map dimensions on Herm(2): 3 under the admitted family, 6
      under a rotation-generated subgroup, 2 after adding one rotation to the
      admitted family.

WHAT IS DELIBERATELY NOT HERE.  No claim about what (a)-(d) MEAN.  Earlier
attempts to state the meaning were reduced twice by four independent blinded
auditors, each time because a true computed fact had been escalated one notch in
the prose: "exactly the stabilizer" (it is a proper subgroup of an infinite
group), "a preferred basis and nothing else" (a rotation-generated subgroup
leaves a six-dimensional space and distinguishes a DIFFERENT basis), and "the
same map" as the .412 conditional expectation (unitarily conjugate, not equal).
The reading belongs in the lane record.  This module states only what its legs
compute.

METHOD NOTE, and the reason the legs run in this order.  Covariance cannot name
a map.  The whole family a*diag + b*offdiag with a != b commutes with monomial
conjugation, so a covariance-first battery certifies "the extra direction is
dephasing" while X -> offdiag(X) is installed.  The map is therefore IDENTIFIED
first -- idempotence, trace preservation, and equality with sum_i Q_i X Q_i --
and only then is its covariance tested.

GRADE [P_math].  Exact rational arithmetic over Q[i].  NON-EXPORTING,
physical_premises_certified = False.

MAY NOT CITE ON THE STRENGTH OF THIS MODULE.
  - "The admitted family is exactly the stabilizer of the presentation basis."
    FALSE; leg (b) computes the counterexample.
  - "The gap between the two gauge readings is a preferred basis."  Only if the
    realizable subgroup is the monomial one; leg (d) computes the alternative.
  - "Covariance is EQUIVALENT to monomiality."  The forward half is exhaustive
    over the admitted group; the converse is one witness at n = 2.
  - "A rotation-generated subgroup."  The tested object is six POWERS of one
    rotation, not a closed subgroup; the commutant coincides, but the leg does
    not compute that.
  - "That turns out to answer the question they leave open" / "the strict
    inclusion costs nothing on this axis."  Both are meaning claims, and this
    module declares it makes none.  Withdrawn.
  - "Dephasing is the only basis-sensitive direction."  Two directions were
    tested, not the space.
  - "Dephasing is refuted."  Nothing here refutes a map.
  - "Born is derived."  Standing corpus bar.
"""

from fractions import Fraction as F
from typing import Dict, List, Tuple

Cx = Tuple[F, F]
Mat = List[List[Cx]]

ZERO: Cx = (F(0), F(0))
ONE: Cx = (F(1), F(0))
IU: Cx = (F(0), F(1))


def _ca(a: Cx, b: Cx) -> Cx:
    return (a[0] + b[0], a[1] + b[1])


def _cm(a: Cx, b: Cx) -> Cx:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _conj(a: Cx) -> Cx:
    return (a[0], -a[1])


def _zeros(n: int) -> Mat:
    return [[ZERO] * n for _ in range(n)]


def _eye(n: int) -> Mat:
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def _mm(A: Mat, B: Mat) -> Mat:
    n, k, m = len(A), len(B), len(B[0])
    out = _zeros(n) if n == m else [[ZERO] * m for _ in range(n)]
    for i in range(n):
        for j in range(m):
            acc = ZERO
            for p in range(k):
                acc = _ca(acc, _cm(A[i][p], B[p][j]))
            out[i][j] = acc
    return out


def _dag(A: Mat) -> Mat:
    return [[_conj(A[j][i]) for j in range(len(A))] for i in range(len(A[0]))]


def _tr(A: Mat) -> Cx:
    acc = ZERO
    for i in range(len(A)):
        acc = _ca(acc, A[i][i])
    return acc


# ---- the admitted family, as presentation_gauge_forcing defines it ---------
def _transpositions(n: int) -> List[Mat]:
    out = []
    for i in range(n - 1):
        M = _eye(n)
        M[i][i] = ZERO
        M[i + 1][i + 1] = ZERO
        M[i][i + 1] = ONE
        M[i + 1][i] = ONE
        out.append(M)
    return out


def _quarter_phases(n: int) -> List[Mat]:
    out = []
    for i in range(n):
        M = _eye(n)
        M[i][i] = IU
        out.append(M)
    return out


def _admitted(n: int) -> List[Mat]:
    return _transpositions(n) + _quarter_phases(n)


def _madd_ok(P: Mat, Q: Mat) -> bool:
    """P + Q == I and P Q == 0: a complete orthogonal pair."""
    n = len(P)
    s = [[_ca(P[i][j], Q[i][j]) for j in range(n)] for i in range(n)]
    z = _mm(P, Q)
    return s == _eye(n) and all(z[i][j] == ZERO for i in range(n) for j in range(n))


def _monomial(M: Mat, n: int) -> bool:
    rows = all(sum(1 for j in range(n) if M[i][j] != ZERO) == 1 for i in range(n))
    cols = all(sum(1 for i in range(n) if M[i][j] != ZERO) == 1 for j in range(n))
    return rows and cols


def _generate(gens: List[Mat], n: int) -> set:
    grp = {tuple(tuple(r) for r in _eye(n))}
    frontier = list(grp)
    while frontier:
        nxt = []
        for t in frontier:
            A = [list(r) for r in t]
            for g in gens:
                P = tuple(tuple(r) for r in _mm(A, g))
                if P not in grp:
                    grp.add(P)
                    nxt.append(P)
        frontier = nxt
    return grp


# ---- the map, identified before its covariance is tested ------------------
def _diag_map(M: Mat, n: int) -> Mat:
    return [[M[i][j] if i == j else ZERO for j in range(n)] for i in range(n)]


def _depol_map(M: Mat, n: int) -> Mat:
    t = _tr(M)
    return [[(t[0] / n, t[1] / n) if i == j else ZERO for j in range(n)]
            for i in range(n)]


def _cond_exp_spec(M: Mat, projectors: List[Mat], n: int) -> Mat:
    """sum_pi Q_pi M Q_pi over an ARBITRARY orthogonal projector family.  The
    diagonal case is _cond_exp; this general form is what makes the route
    genuinely independent of the map under test -- on a NON-diagonal family the
    two must come apart, and that is asserted."""
    acc = _zeros(n)
    for Q in projectors:
        T = _mm(_mm(Q, M), Q)
        acc = [[_ca(acc[i][j], T[i][j]) for j in range(n)] for i in range(n)]
    return acc


def _diag_projectors(n: int) -> List[Mat]:
    out = []
    for q in range(n):
        Q = _zeros(n)
        Q[q][q] = ONE
        out.append(Q)
    return out


def _cond_exp(M: Mat, n: int) -> Mat:
    """The independent comparison route at the DIAGONAL family.  It goes through
    the general spec form below, so a mutation of the route is exercised BOTH by
    the identification legs and by the independence leg -- a validation that runs
    on its own private copy of the logic validates nothing."""
    return _cond_exp_spec(M, _diag_projectors(n), n)


def _nullspace(rows: List[List[F]], dim: int) -> List[List[F]]:
    m = [r[:] for r in rows]
    piv_col: List[int] = []
    piv = 0
    for c in range(dim):
        sel = None
        for r in range(piv, len(m)):
            if m[r][c] != 0:
                sel = r
                break
        if sel is None:
            continue
        m[piv], m[sel] = m[sel], m[piv]
        pv = m[piv][c]
        m[piv] = [x / pv for x in m[piv]]
        for r in range(len(m)):
            if r != piv and m[r][c] != 0:
                f = m[r][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[piv])]
        piv_col.append(c)
        piv += 1
    free = [c for c in range(dim) if c not in piv_col]
    out = []
    for fc in free:
        v = [F(0)] * dim
        v[fc] = F(1)
        for r, c in enumerate(piv_col):
            v[c] = -m[r][fc]
        out.append(v)
    return out


def _herm_basis(n: int) -> List[Mat]:
    B = []
    for i in range(n):
        M = _zeros(n)
        M[i][i] = ONE
        B.append(M)
    for i in range(n):
        for j in range(i + 1, n):
            M = _zeros(n)
            M[i][j] = ONE
            M[j][i] = ONE
            B.append(M)
            M = _zeros(n)
            M[i][j] = IU
            M[j][i] = (F(0), F(-1))
            B.append(M)
    return B


def _probes(n: int) -> List[Mat]:
    """Basis projectors -- the SHARP probe -- plus the all-ones load."""
    out = []
    for k in range(n):
        E = _zeros(n)
        E[k][k] = ONE
        out.append(E)
    out.append([[ONE] * n for _ in range(n)])
    return out


def _rank(rows: List[List[F]]) -> int:
    m = [r[:] for r in rows]
    if not m:
        return 0
    dim = len(m[0])
    piv = 0
    for c in range(dim):
        sel = None
        for r in range(piv, len(m)):
            if m[r][c] != 0:
                sel = r
                break
        if sel is None:
            continue
        m[piv], m[sel] = m[sel], m[piv]
        pv = m[piv][c]
        m[piv] = [x / pv for x in m[piv]]
        for r in range(len(m)):
            if r != piv and m[r][c] != 0:
                f = m[r][c]
                m[r] = [a - f * b for a, b in zip(m[r], m[piv])]
        piv += 1
    return piv


def _coords(M: Mat, n: int) -> List[F]:
    out = [M[i][i][0] for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            out.append(M[i][j][0])
            out.append(M[i][j][1])
    return out


def _conj_matrix(g: Mat, n: int) -> List[List[F]]:
    B = _herm_basis(n)
    cols = [_coords(_mm(_mm(g, Bk), _dag(g)), n) for Bk in B]
    return [[cols[k][r] for k in range(len(B))] for r in range(len(B))]


def _commutant_rows(n: int, gens: List[Mat]) -> List[List[F]]:
    """The single shared linear system for [Phi, C_g] = 0.  BOTH the dimension
    and the explicit solutions come from here, so the cross-validation below
    exercises the same code path it certifies."""
    d = n * n
    Cs = [_conj_matrix(g, n) for g in gens]
    rows: List[List[F]] = []
    for C in Cs:
        for a in range(d):
            for b in range(d):
                row = [F(0)] * (d * d)
                for k in range(d):
                    row[a * d + k] += C[k][b]
                    row[k * d + b] -= C[a][k]
                rows.append(row)
    return rows


def _cov_map_dim(n: int, gens: List[Mat]) -> int:
    """dim of the covariant MAPS on Herm(n): the commutant of {C_g}."""
    d = n * n
    return d * d - _rank(_commutant_rows(n, gens))


ROT: Mat = [[(F(3, 5), F(0)), (F(-4, 5), F(0))],
            [(F(4, 5), F(0)), (F(3, 5), F(0))]]
DPHASE: Mat = [[(F(3, 5), F(4, 5)), ZERO], [ZERO, ONE]]

# STABILITY PROBES.  The 3 and the 2 below are only interesting if they are
# properties of the KIND of element added -- monomial or not -- rather than of
# the particular ROT and DPHASE chosen.  A second Pythagorean rotation and a
# second Gaussian-rational unit phase, both off the 5-12-13 triple instead of
# 3-4-5, make that testable.
ROT2: Mat = [[(F(5, 13), F(0)), (F(-12, 13), F(0))],
             [(F(12, 13), F(0)), (F(5, 13), F(0))]]
DPHASE2: Mat = [[(F(5, 13), F(12, 13)), ZERO], [ZERO, ONE]]
UC: Mat = [[(F(3, 5), F(0)), (F(0), F(4, 5))],
           [(F(0), F(4, 5)), (F(3, 5), F(0))]]


def _result(name, epistemic, key, ev, fails, tier, deps, prem, ncs, xrefs,
            fail_count=None):
    """Build the result dict, and CROSS-ASSERT the two failure records HERE.

    THE PATTERN IS v24.3.450's, AND THE REASON IT IS AT THIS SITE MATTERS.  An
    execution audit on 2026-07-28 showed that a cross-assert living only in a
    module's run_all() does not travel on the banked path: bank.py invokes each
    registered check_fn() directly and reads r['passed'], and never calls
    run_all() or reads fail_count.  A mutation forcing 'passed' True was
    demonstrated to report PASS to the bank with the failures still recorded.
    The assert therefore lives at the point the dict is BUILT, so it travels
    with the dict wherever the dict goes; run_all() remains a second gate.

    RESIDUAL LIMIT, DISCLOSED RATHER THAN OVERCLAIMED: this catches DIVERGENCE
    between the two failure records -- the realistic tampering, where a repair
    patches one recording site and not the other, and which is what escaped on
    the banked path.  It does NOT catch a bare literal substitution of the
    verdict itself, because nothing downstream re-derives that field: bank.py
    reads it.  No code inside a module can defend against an arbitrary edit to
    its own return statement; that is a property of the bank's contract, not of
    this module."""
    counted = len(fails) if fail_count is None else fail_count
    if len(fails) != counted:
        raise AssertionError(
            f"{name}: failure records disagree -- fail_reasons has "
            f"{len(fails)} entries, the independent counter says {counted}")
    return {
        'fail_count': counted,
        'name': name, 'epistemic': epistemic, 'passed': (counted == 0), 'tier': tier,
        'fail_reasons': fails, 'dependencies': list(deps), 'premises': list(prem),
        'negative_controls': list(ncs), 'cross_refs': list(xrefs),
        'physical_premises_certified': False, 'exports': [], 'bank_modified': False,
        'key_result': key, 'evidence': ev,
    }


# ==========================================================================
def check_L_admitted_presentation_family_is_monomial() -> Dict[str, object]:
    """Tier 3, [P_math]."""
    fails: List[str] = []

    tally = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
            tally[0] += 1

    # ---- E0: the predicate must be pinned on BOTH clauses, and the probe set
    # must contain the basis projectors.
    ck(not _monomial([[ONE, ZERO], [ONE, ZERO]], 2),
       "the monomiality predicate must reject one-per-ROW-but-not-per-column")
    ck(not _monomial([[ONE, ONE], [ZERO, ZERO]], 2),
       "and one-per-COLUMN-but-not-per-row")
    ck(_monomial([[ZERO, ONE], [ONE, ZERO]], 2),
       "and must accept a genuine monomial matrix, or it is a constant")
    for n in (2, 3):
        pr = _probes(n)
        ck(len(pr) == n + 1
           and all(any(P[k][k] == ONE and all(P[a][b] == ZERO
                                              for a in range(n) for b in range(n)
                                              if (a, b) != (k, k))
                       for P in pr) for k in range(n)),
           "the probe set must CONTAIN every basis projector at n=%d -- the "
           "all-ones load alone is a false positive" % n)

    # ---- E1: IDENTIFY the map before any covariance leg touches it.
    ident = True
    wit = 0
    for n in (2, 3, 4):
        for X in _probes(n) + _herm_basis(n)[:4]:
            DX = _diag_map(X, n)
            wit += 1
            if _diag_map(DX, n) != DX or _tr(DX) != _tr(X) or DX != _cond_exp(X, n):
                ident = False
    ck(ident and wit == 24,
       "IDENTIFICATION: the map under test must be idempotent, trace "
       "preserving, and equal to sum_i Q_i X Q_i on every witness (%d tested) "
       "-- covariance alone cannot name a map" % wit)
    ck(any(_diag_map(X, 2) != X for X in _probes(2)),
       "and at least one witness must be OFF the fixed set, or the "
       "identification is vacuous")
    # The comparison route must be INDEPENDENT of the map under test.  On a
    # NON-diagonal projector family the conditional expectation must come APART
    # from the diagonal map; if it does not, the route is a copy and the
    # identification above is circular.
    Pp = [[(F(1, 2), F(0)), (F(1, 2), F(0))], [(F(1, 2), F(0)), (F(1, 2), F(0))]]
    Pm = [[(F(1, 2), F(0)), (F(-1, 2), F(0))], [(F(-1, 2), F(0)), (F(1, 2), F(0))]]
    Gw = [[ONE, (F(1, 3), F(0))], [(F(1, 3), F(0)), (F(2), F(0))]]
    ck(_mm(Pp, Pp) == Pp and _mm(Pm, Pm) == Pm
       and _madd_ok(Pp, Pm),
       "the non-diagonal projector family must be a genuine complete family of "
       "orthogonal projectors, or the independence test below is meaningless")
    ck(_cond_exp_spec(Gw, [Pp, Pm], 2) != _diag_map(Gw, 2),
       "INDEPENDENCE: on a NON-diagonal projector family the conditional "
       "expectation must DIFFER from the diagonal map -- otherwise the "
       "comparison route is a copy of the map under test and the "
       "identification is circular")
    ck(_cond_exp_spec(Gw, [Pp, Pm], 2)
       != _cond_exp_spec(Gw, [[[ONE, ZERO], [ZERO, ZERO]],
                              [[ZERO, ZERO], [ZERO, ONE]]], 2),
       "and the two projector families must give DIFFERENT images, or the "
       "spec argument is being ignored")

    # ---- E2: the admitted family is monomial and closes at 4^n * n!.
    sizes = {}
    mono = True
    grp2 = None
    for n in (2, 3):
        gens = _admitted(n)
        if not all(_monomial(g, n) for g in gens):
            mono = False
        grp = _generate(gens, n)
        if not all(_monomial([list(r) for r in t], n) for t in grp):
            mono = False
        fact = 1
        for k in range(2, n + 1):
            fact *= k
        sizes["n%d" % n] = len(grp)
        ck(len(grp) == (4 ** n) * fact,
           "the generated group must have order 4^n * n! at n=%d (expect %d, got "
           "%d) -- asserting the order is what catches a truncated closure"
           % (n, (4 ** n) * fact, len(grp)))
        if n == 2:
            grp2 = grp
    ck(mono, "every admitted generator and every element generated must be "
             "monomial")

    # ---- E3: the inclusion in the normalizer is STRICT.
    ck(_mm(_dag(DPHASE), DPHASE) == _eye(2),
       "the inclusion witness must be unitary")
    ck(_monomial(DPHASE, 2),
       "and monomial, hence in the normalizer of the diagonal MASA")
    ck(grp2 is not None and len(next(iter(grp2))) == 2 and len(grp2) == 32,
       "the membership test must run against the n=2 group specifically -- "
       "otherwise a 2x2 witness is trivially 'not in' a group of 3x3 matrices")
    ck(tuple(tuple(r) for r in _transpositions(2)[0]) in grp2,
       "and a KNOWN member must be found in it, or 'not in' carries no "
       "information")
    # and the normalizer property, computed rather than inferred from monomiality
    ck(all(_diag_map(_mm(_mm(DPHASE, D), _dag(DPHASE)), 2)
           == _mm(_mm(DPHASE, D), _dag(DPHASE))
           for D in _diag_projectors(2)),
       "and the witness must actually NORMALIZE the diagonal MASA -- computed, "
       "not inferred from monomiality")
    strict = tuple(tuple(r) for r in DPHASE) not in grp2
    ck(strict,
       "and NOT in the admitted group -- the admitted family is a PROPER "
       "subgroup of the basis-line stabilizer, never 'exactly' it")

    # ---- E4: covariance under the whole admitted group, on the sharp probe.
    cov = True
    for n in (2, 3):
        grp = _generate(_admitted(n), n)
        ck(len(grp) == sizes["n%d" % n],
           "E4 must scan the SAME group E2 pinned at n=%d" % n)
        pairs = 0
        for t in grp:
            U = [list(r) for r in t]
            for X in _probes(n):
                pairs += 1
                if (_diag_map(_mm(_mm(U, X), _dag(U)), n)
                        != _mm(_mm(U, _diag_map(X, n)), _dag(U))):
                    cov = False
        seen_probes = {tuple(tuple(r) for r in X) for X in _probes(n)}
        ck(pairs == len(grp) * (n + 1) and len(seen_probes) == n + 1,
           "and it must test every (element, probe) pair at n=%d over n+1 "
           "DISTINCT probes -- a length product alone is satisfied by one probe "
           "repeated" % n)
    ck(cov,
       "the identified map must be covariant under EVERY element of the "
       "admitted group, on basis projectors as well as the all-ones load")

    # ---- E5: the naive probe is a false positive; the sharp one is an iff.
    ck(_mm(_dag(UC), UC) == _eye(2), "the converse witness must be unitary")
    ck(not _monomial(UC, 2), "and NON-monomial")
    J = [[ONE, ONE], [ONE, ONE]]
    E00 = [[ONE, ZERO], [ZERO, ZERO]]
    naive_fp = (_diag_map(_mm(_mm(UC, J), _dag(UC)), 2)
                == _mm(_mm(UC, _diag_map(J, 2)), _dag(UC)))
    ck(naive_fp,
       "CONVERSE: a NON-monomial unitary PASSES the all-ones probe, so that "
       "probe cannot certify 'exactly the monomial elements'")
    ck(_diag_map(_mm(_mm(UC, E00), _dag(UC)), 2)
       != _mm(_mm(UC, _diag_map(E00, 2)), _dag(UC)),
       "and the BASIS-PROJECTOR probe catches it -- covariance on e_kk forces "
       "one nonzero per column, which is monomiality")

    # ---- E6: one non-monomial element removes the direction; the depolarizing
    # direction survives it, so E6 is about this map and not about conjugation.
    hp = [[(F(1, 2), F(0))] * 2 for _ in range(2)]
    dw = [[ONE, ONE], [ONE, ZERO]]   # separates diag / depol / identity
    brk = (_diag_map(_mm(_mm(ROT, hp), _dag(ROT)), 2)
           != _mm(_mm(ROT, _diag_map(hp, 2)), _dag(ROT)))
    ck(not _monomial(ROT, 2), "the rotation probe must be NON-monomial")
    ck(brk, "and must BREAK covariance of the identified map")
    # THE CONTROL, run at a witness where the three maps genuinely DIFFER.  The
    # earlier version ran at hp, where diag(hp) and depol(hp) are both I/2 --
    # the control coincided with the map under test on its own witness and could
    # not fail.  Third instance of that defect on this lane; the fix is to make
    # the witness the same object the distinctness assertion is about.
    ck(_depol_map(dw, 2) != _diag_map(dw, 2) and _depol_map(dw, 2) != dw
       and _diag_map(dw, 2) != dw,
       "the control witness must SEPARATE the three maps, or the control below "
       "cannot fail")
    ck(_diag_map(_mm(_mm(ROT, dw), _dag(ROT)), 2)
       != _mm(_mm(ROT, _diag_map(dw, 2)), _dag(ROT)),
       "and the identified map must break covariance AT THAT SAME witness, or "
       "the control and the positive case are not comparable")
    ck(_depol_map(_mm(_mm(ROT, dw), _dag(ROT)), 2)
       == _mm(_mm(ROT, _depol_map(dw, 2)), _dag(ROT)),
       "CONTROL: at that witness the depolarizing direction IS covariant under "
       "the same non-monomial element -- so the break is a fact about the "
       "identified map, not about conjugation. NOTE the honest limit: depol is "
       "covariant under EVERY unitary, so this control shows the break is "
       "map-specific and does NOT show it is ROT-specific")
    ck(_depol_map(dw, 2) != _diag_map(dw, 2)
       and _depol_map(dw, 2) != dw and _diag_map(dw, 2) != dw,
       "and the control map must be DISTINCT from both the map under test and "
       "the identity, or a control that cannot fail has been installed")

    # ---- E7: the covariant-MAP dimensions on Herm(2), computed locally.
    rt = True
    for n in (2, 3):
        for B in _herm_basis(n):
            c = _coords(B, n)
            rec = _zeros(n)
            for k, Bk in enumerate(_herm_basis(n)):
                if c[k] != 0:
                    for a in range(n):
                        for b in range(n):
                            rec[a][b] = _ca(rec[a][b],
                                            (Bk[a][b][0] * c[k], Bk[a][b][1] * c[k]))
            if rec != B:
                rt = False
    ck(rt, "the Herm-coordinate map must round-trip, or the dimensions below "
           "are noise")
    pows = []
    P = _eye(2)
    for _ in range(6):
        P = _mm(P, ROT)
        pows.append(P)
    ck(all(_mm(_dag(g), g) == _eye(2) for g in pows)
       and any(not _monomial(g, 2) for g in pows),
       "the rotation subgroup must be unitary and contain a NON-monomial "
       "element, or it is not the object the comparison needs")
    # CROSS-VALIDATION: the dimension routine must produce solutions that are
    # ACTUALLY covariant.  A transposed system can report the same dimension
    # while solving for a different object; reconstruct each nullspace basis
    # vector as a map on Herm-coordinates and check it commutes with every
    # conjugation matrix.
    def _cov_solutions(n: int, gens: List[Mat]) -> List[List[F]]:
        return _nullspace(_commutant_rows(n, gens), (n * n) ** 2)

    def _commutes_all(vec: List[F], n: int, gens: List[Mat]) -> bool:
        d = n * n
        Phi = [[vec[i * d + j] for j in range(d)] for i in range(d)]
        for g in gens:
            C = _conj_matrix(g, n)
            PC = [[sum((Phi[i][k] * C[k][j] for k in range(d)), F(0))
                   for j in range(d)] for i in range(d)]
            CP = [[sum((C[i][k] * Phi[k][j] for k in range(d)), F(0))
                   for j in range(d)] for i in range(d)]
            if PC != CP:
                return False
        return True

    sols = _cov_solutions(2, _admitted(2))
    ck(len(sols) == 3 and all(_commutes_all(v, 2, _admitted(2)) for v in sols),
       "CROSS-VALIDATION: every solution the dimension routine returns must "
       "ACTUALLY commute with each conjugation matrix (%d solutions) -- this is "
       "what catches a routine that reports the right dimension for the wrong "
       "object" % len(sols))
    bad = [F(1)] + [F(0)] * (len(sols[0]) - 1) if sols else []
    ck(bad and not _commutes_all(bad, 2, _admitted(2)),
       "and a non-covariant vector must FAIL that test, or the validation is "
       "vacuous")

    dims = {
        "admitted": _cov_map_dim(2, _admitted(2)),
        "six_powers_of_one_rotation": _cov_map_dim(2, pows),
        "admitted_plus_rotation": _cov_map_dim(2, _admitted(2) + [ROT]),
        "admitted_plus_phase": _cov_map_dim(2, _admitted(2) + [DPHASE]),
    }
    ck(dims == {"admitted": 3, "six_powers_of_one_rotation": 6,
                "admitted_plus_rotation": 2, "admitted_plus_phase": 3},
       "the covariant-MAP dimensions on Herm(2) must be exactly "
       "{admitted 3, rotation subgroup 6, admitted+rotation 2, "
       "admitted+phase 3} (got %s) -- absolute values, not just orderings"
       % (dims,))

    # STABILITY, EXECUTED.  Without these rows the 3 and the 2 above are two
    # facts about ROT and DPHASE, and the reading they support -- that what
    # matters is whether the added element is MONOMIAL, not which element it is
    # -- would be an inference from a single instance each.  Both probes are
    # built off the 5-12-13 triple rather than 3-4-5, so they share no entry
    # with the originals.
    # DISTINCTNESS OF THE PROBES, ASSERTED.  Found by mutation: setting
    # ROT2 = ROT or DPHASE2 = DPHASE passed every length, membership and
    # non-contamination guard below, collapsing the stability rows onto the
    # single-probe rows already computed -- so the "property of the KIND, not of
    # the element" reading was untested.  The comment claiming the probes "share
    # no entry with the originals" is now a check.
    ck(ROT2 != ROT and DPHASE2 != DPHASE,
       "the stability probes must DIFFER from the originals, or the pair rows "
       "are the single rows under another name and the kind-not-element reading "
       "is untested")
    ck(all(ROT2[i][j] != ROT[i][j] for i in range(2) for j in range(2))
       and DPHASE2[0][0] != DPHASE[0][0],
       "and they must share no entry with them -- 5-12-13 against 3-4-5, which "
       "is what the comment claims and what this now checks")
    ck(_monomial(DPHASE2, 2) and not _monomial(ROT2, 2),
       "the stability probes must be typed as claimed: the second phase "
       "MONOMIAL, the second rotation NOT -- otherwise the rows below test "
       "something other than the monomial/non-monomial split")
    ck(all(_mm(_dag(U), U) == _eye(2) for U in (ROT2, DPHASE2)),
       "and both stability probes must be exactly unitary")
    # THE GENERATOR LISTS ARE COMPOSED, ASSERTED, THEN USED.  Found by mutation:
    # because one rotation already cuts the dimension to 2, aliasing the
    # two-rotation list onto the one-rotation list leaves every numeric row
    # unchanged, so the pair rows could silently test nothing.  A count and a
    # membership assertion on each list is what makes them carry information.
    _adm2 = _admitted(2)
    lists = {
        "admitted_plus_phase2": _adm2 + [DPHASE2],
        "admitted_plus_rotation2": _adm2 + [ROT2],
        "admitted_plus_two_phases": _adm2 + [DPHASE, DPHASE2],
        "admitted_plus_two_rotations": _adm2 + [ROT, ROT2],
    }
    for nm, gens in lists.items():
        extra = 2 if nm.startswith("admitted_plus_two") else 1
        ck(len(gens) == len(_adm2) + extra,
           "the %s generator list must extend the admitted family by exactly "
           "%d element(s) (got %d)" % (nm, extra, len(gens) - len(_adm2)))
    ck(DPHASE in lists["admitted_plus_two_phases"]
       and DPHASE2 in lists["admitted_plus_two_phases"],
       "the two-phase list must contain BOTH phases, or the pair row is the "
       "single row under another name")
    ck(ROT in lists["admitted_plus_two_rotations"]
       and ROT2 in lists["admitted_plus_two_rotations"],
       "and the two-rotation list must contain BOTH rotations")
    ck(DPHASE2 not in lists["admitted_plus_rotation2"]
       and ROT2 not in lists["admitted_plus_phase2"],
       "and the single-probe lists must not carry the other probe, or the two "
       "columns are not independent")
    stab = {nm: _cov_map_dim(2, gens) for nm, gens in lists.items()}
    ck(stab == {"admitted_plus_phase2": 3, "admitted_plus_rotation2": 2,
                "admitted_plus_two_phases": 3,
                "admitted_plus_two_rotations": 2},
       "STABILITY: adding ANY tested monomial phase must leave the dimension at "
       "3 and adding ANY tested rotation must cut it to 2, singly and in pairs "
       "(got %s) -- so the 3 and the 2 are properties of the monomial/"
       "non-monomial split and not of the particular probe" % (stab,))
    ck(stab["admitted_plus_two_phases"] == dims["admitted"]
       and stab["admitted_plus_two_rotations"] < dims["admitted"],
       "and the split must be the SAME one the single-probe rows report: "
       "phases change nothing, rotations strictly cut")
    # DISCLOSED: the pair rows CORROBORATE and do not DISCRIMINATE.  One
    # rotation already cuts to 2, so the two-rotation row cannot come out
    # differently; what makes it worth running is the composition assertion
    # above, not the number it returns.  Stated so the row is not read as
    # independent evidence.
    ck(stab["admitted_plus_rotation2"] == stab["admitted_plus_two_rotations"],
       "and the single- and two-rotation rows must AGREE -- recorded as the "
       "reason the pair row is corroborating rather than discriminating")

    # THE ORDERING IS A GATE, NOT PROSE.  Without this, installing X -> offdiag(X)
    # fails the identification while the evidence dict still reports the
    # covariance verdict and the dimensions FOR THE WRONG MAP, quotable from a
    # failing run.
    ck(ident,
       "GATE: the covariance and dimension verdicts above are reported only if "
       "the map was IDENTIFIED -- if identification failed, every downstream "
       "verdict in this check describes some other map and must not be read")

    key = (
        "WHAT THE ADMITTED PRESENTATION FAMILY IS. (a) Every admitted generator "
        "is MONOMIAL and the generated group is monomial throughout, of order "
        "4^n * n! -- 32 at n = 2, 384 at n = 3, asserted rather than reported. "
        "(b) That group sits STRICTLY INSIDE the normalizer of the diagonal MASA: "
        "diag((3+4i)/5, 1) is unitary, monomial, normalizes the MASA and is not "
        "in the group, so the relation is INCLUSION and not identity. (c) "
        "Covariance of the diagonal conditional expectation holds for EVERY "
        "element of the admitted group when tested on basis projectors, and "
        "FAILS for an exhibited non-monomial unitary. SCOPE, because the word "
        "EQUIVALENT would overstate it: the forward half is exhaustive over the "
        "admitted group, the converse is ONE witness at n = 2, and the one-line "
        "reason the two are equivalent in general is stated in this module and "
        "NOT executed -- so what is computed is an implication plus an instance, "
        "not an equivalence. The naive all-ones "
        "probe is a computed FALSE POSITIVE, passed by the non-monomial unitary "
        "[[3/5, 4i/5], [4i/5, 3/5]] and caught by the sharp probe. The map is "
        "IDENTIFIED first, by idempotence, trace preservation and equality with "
        "sum_i Q_i X Q_i, because covariance alone cannot name a map: the whole "
        "family a*diag + b*offdiag with a != b commutes with monomial "
        "conjugation. (d) The covariant-MAP dimensions on Herm(2) are 3 under "
        "the admitted family, 6 under SIX POWERS of one rotation (a SET, not a "
        "closed subgroup -- the closed-subgroup commutant is NOT computed here), "
        "2 after one rotation is added, and 3 again after a monomial phase is "
        "added. STABILITY, computed: any tested monomial phase leaves the 3 and "
        "any tested rotation cuts to the 2, singly and in pairs, on probes built "
        "off 5-12-13 rather than 3-4-5 and asserted distinct from the originals "
        "-- so the split is a property of whether the added element is MONOMIAL, "
        "not of which element it is. The pair rows CORROBORATE and do not "
        "DISCRIMINATE, because one rotation already cuts. WHAT THESE FACTS "
        "MEAN IS NOT STATED HERE and belongs to the lane record; three earlier "
        "attempts to state it were reduced by blinded audit for escalating a "
        "computed fact one notch."
    )
    return _result(
        'L_admitted_presentation_family_is_monomial',
        'P_math -- exact arithmetic over Q[i]; no physical premise consumed',
        key,
        {
            "generated_group_orders": sizes,
            "all_elements_monomial": mono,
            "inclusion_in_normalizer_is_strict": strict,
            "identified_map_covariant_on_sharp_probe": None if not ident else cov,
            "non_monomial_element_breaks_covariance": brk,
            "naive_all_ones_probe_is_a_false_positive": naive_fp,
            # GATED ON THE IDENTIFICATION.  Without this a failing run still
            # published the covariance verdict and all four dimensions, quotable
            # as facts about whatever map the mutation installed.
            "covariant_map_dimensions_herm2": (dims if ident else None),
            "covariant_map_dimension_stability": (stab if ident else None),
        },
        fails, 3,
        (),   # no A1 edge: nothing here consumes a capacity axiom or a cost floor
        (),
        ("a one-per-row-only and a one-per-column-only matrix are both rejected",
         "a non-monomial unitary passes the all-ones probe and is caught by the "
         "basis-projector probe",
         "the depolarizing direction survives the non-monomial element",
         "the control map is distinct from both the map under test and the "
         "identity",
         "adding a monomial phase leaves the covariant-map dimension unchanged"),
        ('T_presentation_gauge_forces_trace',
         'L_covariant_state_maps_are_exactly_the_depolarizing_line',
         'L_commutative_no_unresolved_hold',
         'L_coherence_sector_separation'),
        fail_count=tally[0],
    )


_CHECKS = {
    'L_admitted_presentation_family_is_monomial': check_L_admitted_presentation_family_is_monomial,

}

CHECKS = tuple(_CHECKS.values())


def register(registry):
    """The bank's entry point.  bank.py imports the module and calls this with
    the live REGISTRY; a module without it registers nothing and shows up as a
    gap, which is exactly how this one was caught before landing."""
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, object]:
    """Recompute `passed`, and cross-assert the two failure records.

    A SECOND gate only: the load-bearing cross-assert lives in _result(),
    because the bank never calls this function -- it calls register() and then
    each check_fn() directly."""
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
        out[r['name']] = r
    return out


if __name__ == '__main__':
    for name, r in run_all().items():
        print(('PASS  ' if r['passed'] else 'FAIL  ') + name)
        for f in r['fail_reasons']:
            print('   - ' + f)
