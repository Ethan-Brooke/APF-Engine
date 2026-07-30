"""Two-ray rigidity on M2(C): certainty at two distinct nonorthogonal pure
states, plus complete positivity, forces the identity.

WHAT THIS ADDS, AGAINST THE PRIOR ART (read this first).

apf/gauge_without_sandwich_countermodel.py (v24.3.445/.446) classifies the
covariant state maps and closes the sharpness fence with complete positivity,
and records that dephasing survives every fence banked there -- it is CP, and CP
does not reach it.  This module says what does.

    A CPTP map on M2(C) fixing two DISTINCT NONORTHOGONAL pure states is the
    identity.

The word DISTINCT is load-bearing and is the first thing to get right.
"Distinct unit vectors with <v,w> != 0" is FALSE as a hypothesis: v = (1,0) and
w = i(1,0) are distinct unit vectors with overlap i != 0 and the SAME projector,
and dephasing fixes both and is not the identity.  The condition is distinct
RAYS -- linearly independent projectors with Tr(pq) != 0.  That correction is
executed below, not merely stated.

THE DIVISION OF LABOUR, which is the point of the module.  Three antecedents are
load-bearing and each has a computed witness that isolates it:

  - NONORTHOGONALITY.  Dephasing is CP and fixes |0><0| and |1><1|, which are
    antipodal in Bloch -- an ORTHOGONAL pair.  It fails the hypothesis, and it
    is nonorthogonality that excludes it, NOT complete positivity.
  - COMPLETE POSITIVITY.  Transposition fixes |0><0| and |+><+| -- genuinely
    nonorthogonal -- and is positive and trace preserving but not CP.  CP is
    what excludes it.
  - AFFINE LINEARITY.  F(rho) = (1 - 4 det rho) rho + 4 det rho (I/2) fixes
    EVERY pure state -- det rho = 0 there, so this is one line, not a finding
    from a sample -- and is not the identity, so it survives both calibrations
    and an arbitrarily dense pure-ray cover.  So "two rays are enough" is FALSE
    without the affine premise named alongside CP.

    SCOPE CORRIGENDUM, after blinded audit: F is positive and trace preserving
    ON THE TRACE-ONE SLICE ONLY, and "it dies only to affinity" is WITHDRAWN.
    F(I) = -I, so on the positive cone F is neither positive nor trace
    preserving, and cone positivity kills it as well as affinity.  Both facts are
    executed below.  What survives is the narrower and true claim: on states, F
    is a positive trace-preserving non-affine map fixing every pure state, so a
    dense pure-ray cover plus positivity plus normalization does NOT force the
    identity -- affinity is doing work that neither of the other two antecedents
    does.

And the orthogonal-pair survivor set is exhibited rather than asserted: with
|0><0| and |1><1| more than one CP survivor exists, so two ORTHOGONAL
calibrations are not enough.  (The full survivor set is a disk; this module's
slice sees only a segment of it and does not compute the disk.  The word is not
used below.)

METHOD.  The theorem is reached TWICE, by routes with different weaknesses, and
the primary route is now the general one.

PRIMARY -- the Kraus / Cauchy-Schwarz elimination (leg L4b).  Not a scan and not
slice-restricted.  If a CPTP map fixes a pure state then every Kraus operator has
that state's vector as an eigenvector, because a sum of PSD matrices equal to a
rank-one PSD matrix has each summand supported in the range of the sum.  Two
DISTINCT fixed pure states therefore give every Kraus operator two eigenvectors,
which by distinctness span C^2, so A_k is fixed by its two eigenvalues
(lam_k, mu_k).  Trace preservation reads off as three exact equations, and the
(1,2) equation -- which is the one carrying the factor c, hence the one that needs
NONORTHOGONALITY to be non-vacuous -- gives sum conj(lam_k) mu_k = sum |lam_k|^2
= 1.  Cauchy-Schwarz then forces sum |mu_k|^2 >= 1 while the (2,2) equation forces
it <= 1, so equality holds, so sum |mu_k - lam_k|^2 = 0, so mu_k = lam_k, so every
A_k is a scalar and the channel is the identity.

WHAT IS IMPORTED IN THAT ROUTE, all THREE standard and all three named rather
than re-proved.  (1) THE KRAUS / CHOI REPRESENTATION THEOREM -- that a CPTP map
is sum_k A_k rho A_k* with sum_k A_k* A_k = I.  This is the route's starting
object: without it there are no Kraus operators to have eigenvectors, and an
earlier version of this header claimed the import list was complete with only
two entries, which was wrong.  (2) THE RANGE STEP -- a sum of PSD matrices equal
to a rank-one PSD matrix has every summand supported in the range of the sum.
(3) THE CAUCHY-SCHWARZ INEQUALITY.  Note it is the INEQUALITY and not the
equality condition: the proof gets sum |mu|^2 >= 1 from Cauchy-Schwarz and
sum |mu|^2 <= 1 from equation (2,2), and concludes from the two bounds; the
proportionality clause of the equality case is never invoked.  What is
EXECUTED: that the claimed operator family really does fix both projectors; that
the three equations are exactly what sum A* A = I reads off, checked on rows that
are not all TP-satisfying so the identity is not verified only at zero; that on a
stated exact value set, at Kraus rank 2 AND at rank 3, every trace-preserving
solution has mu = lam; and that at c = 0 -- the orthogonal case -- the same search
admits mu != lam, with the explicit dephasing pair as the named survivor.  The
finite search CORROBORATES the general statement.  Step (iv) is what proves it,
and the search is not billed as the proof.

SECONDARY -- the finite exact grid scan (leg L4), retained as a corroborating fast
path.  The map is parametrized in the Bloch picture, the two fixed points are
imposed, and PSD is tested on a stated rational grid; the two fixed-point
conditions leave SIX free parameters and this scan fixes the translation t = 0 and
scans three.  That restriction is real and is why the scan is secondary rather
than the evidence.  Its grid is pinned, because a grid reduced to the identity
point still certified uniqueness.

The old second-pair scan is DELETED, and the elimination is why it is not
rebuilt.  Its parametrization was pinned by the first fixed-point condition
alone, before positivity or the second pair was consulted, so it certified
nothing about the complex slice.  The elimination never coordinatizes a real
slice at all -- it is an operator argument over arbitrary Kraus rank -- so there
is no complex-slice gap left for such a scan to cover.  Its vacuity is asserted
below as a record leg.

A leg that checks overlaps and spans without ever constructing a channel proves
nothing about channels -- every such leg evaluates true for transposition, which
is the counterexample to dropping CP.

GRADE [P_math].  Exact rational arithmetic in the Bloch picture with an exact
Choi PSD test.  NON-EXPORTING, physical_premises_certified = False.

MAY NOT CITE ON THE STRENGTH OF THIS MODULE.
  - "Born is derived."  Standing corpus bar.
  - "Two nonorthogonal calibrations are enough."  Three antecedents are
    load-bearing; the det-family survives a dense pure-ray cover.
  - "Complete positivity forces Born."  With two nonorthogonal calibrations it
    forces the IDENTITY MAP.  That is not Born.
  - "The countermodel landscape is closed."  Unchanged; this does not close it.
  - "Dephasing is refuted."  Its exclusion premise is named.  That is not a
    refutation of a map.
  - "This supersedes the presentation-gauge route."  It is a different premise
    set and the two are incomparable.
  - "The theorem is computed by Choi elimination."  The PRIMARY route is the
    Kraus / Cauchy-Schwarz elimination, which is general in the Kraus rank; the
    Choi grid scan is secondary and is restricted to a t = 0 slice.  Cite the
    route, not "elimination" unqualified.
  - "The elimination is exhaustively verified."  It is PROVED at step (iv) and
    CORROBORATED by a finite search at Kraus rank 2 and 3 over a stated value
    set.  The search is not exhaustive over C, and the rank-3 row runs on a
    stated four-value subset.
  - "The range step and Cauchy-Schwarz are derived here."  Both are NAMED
    STANDARD IMPORTS, as is the Kraus/Choi representation theorem -- three, not
    two.
  - "The elimination is executed."  Steps (i) and (iv), the two that carry the
    mathematics, are a proof-of-record in this header.  What EXECUTES is the
    read-off of the three equations, the finite corroboration, and the
    witnesses.
  - "The det-family is positive and trace preserving."  On the trace-one slice
    only.  F(I) = -I.
  - "The det-family dies only to affinity."  WITHDRAWN; cone positivity also
    excludes it.
  - "The orthogonal-pair survivors form a disk."  True but not computed here.
"""

from fractions import Fraction as F
from itertools import combinations, product
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


def _cs(s: F, a: Cx) -> Cx:
    return (s * a[0], s * a[1])


# --- helpers for the L4b elimination.  Named apart from the Bloch machinery
# above because they act on C^2 vectors and 2x2 complex matrices directly; the
# elimination is an operator statement, not a Bloch-picture one.
def _csub(a: Cx, b: Cx) -> Cx:
    return (a[0] - b[0], a[1] - b[1])


def _cconj(a: Cx) -> Cx:
    return (a[0], -a[1])


def _cabs2(a: Cx) -> F:
    return a[0] * a[0] + a[1] * a[1]


def _mv(A: Mat, v: List[Cx]) -> List[Cx]:
    out = []
    for i in range(len(A)):
        acc = ZERO
        for j in range(len(v)):
            acc = _ca(acc, _cm(A[i][j], v[j]))
        out.append(acc)
    return out


def _sv(c: Cx, v: List[Cx]) -> List[Cx]:
    return [_cm(c, x) for x in v]


def _ovl(u: List[Cx], v: List[Cx]) -> Cx:
    """<u|v>, conjugate-linear in the first argument."""
    acc = ZERO
    for a, b in zip(u, v):
        acc = _ca(acc, _cm(_cconj(a), b))
    return acc


def _m2mul(A: Mat, B: Mat) -> Mat:
    return [[_ca(_cm(A[i][0], B[0][j]), _cm(A[i][1], B[1][j]))
             for j in range(2)] for i in range(2)]


def _m2dag(A: Mat) -> Mat:
    return [[_cconj(A[j][i]) for j in range(2)] for i in range(2)]


# psi = |0>, phi = (3/5)|0> + (4/5)|1>.  Distinct as states, overlap 3/5 != 0.
_PSI: List[Cx] = [ONE, ZERO]
_PHI: List[Cx] = [(F(3, 5), F(0)), (F(4, 5), F(0))]


def _madd(A: Mat, B: Mat) -> Mat:
    return [[_ca(A[i][j], B[i][j]) for j in range(len(A[0]))] for i in range(len(A))]


def _mscale(s: F, A: Mat) -> Mat:
    return [[_cs(s, A[i][j]) for j in range(len(A[0]))] for i in range(len(A))]


def _mcmul(c: Cx, A: Mat) -> Mat:
    return [[_cm(c, A[i][j]) for j in range(len(A[0]))] for i in range(len(A))]


ID2: Mat = [[ONE, ZERO], [ZERO, ONE]]
SX: Mat = [[ZERO, ONE], [ONE, ZERO]]
SY: Mat = [[ZERO, (F(0), F(-1))], [IU, ZERO]]
SZ: Mat = [[ONE, ZERO], [ZERO, (F(-1), F(0))]]
PAULI = (SX, SY, SZ)

Bloch = List[F]
Chan = Tuple[List[List[F]], List[F]]        # (M, t): r -> M r + t


def _act(ch: Chan, r: Bloch) -> Bloch:
    M, t = ch
    return [sum((M[i][j] * r[j] for j in range(3)), F(0)) + t[i] for i in range(3)]


def _state(r: Bloch) -> Mat:
    acc = ID2
    for k in range(3):
        acc = _madd(acc, _mscale(r[k], PAULI[k]))
    return _mscale(F(1, 2), acc)


def _phi(ch: Chan, A: Mat) -> Mat:
    """Complex-linear extension from the Herm basis: Phi(I) = I + t.sigma,
    Phi(sigma_k) = (M e_k).sigma.  Defined for ARBITRARY 2x2 complex A, which
    is what the Choi construction needs."""
    M, t = ch

    def tr(X: Mat) -> Cx:
        return _ca(X[0][0], X[1][1])

    a0 = tr(A)
    ak: List[Cx] = []
    for k in range(3):
        P = PAULI[k]
        prod = [[_ca(_cm(A[i][0], P[0][j]), _cm(A[i][1], P[1][j])) for j in range(2)]
                for i in range(2)]
        ak.append(tr(prod))
    PhiI = ID2
    for k in range(3):
        PhiI = _madd(PhiI, _mscale(t[k], PAULI[k]))
    out = _mcmul(_cs(F(1, 2), a0), PhiI)
    for k in range(3):
        Mk: Mat = [[ZERO, ZERO], [ZERO, ZERO]]
        for j in range(3):
            Mk = _madd(Mk, _mscale(M[j][k], PAULI[j]))
        out = _madd(out, _mcmul(_cs(F(1, 2), ak[k]), Mk))
    return out


def _choi(ch: Chan) -> Mat:
    C: Mat = [[ZERO] * 4 for _ in range(4)]
    for i in range(2):
        for j in range(2):
            E: Mat = [[ZERO, ZERO], [ZERO, ZERO]]
            E[i][j] = ONE
            B = _phi(ch, E)
            for a in range(2):
                for b in range(2):
                    C[2 * i + a][2 * j + b] = B[a][b]
    return C


def _psd(C: Mat) -> bool:
    n = len(C)

    def det(sub: Mat) -> Cx:
        m = len(sub)
        if m == 1:
            return sub[0][0]
        acc = ZERO
        for j in range(m):
            minor = [[sub[i][k] for k in range(m) if k != j] for i in range(1, m)]
            term = _cm(sub[0][j], det(minor))
            acc = _ca(acc, term if j % 2 == 0 else (-term[0], -term[1]))
        return acc

    for size in range(1, n + 1):
        for idx in combinations(range(n), size):
            sub = [[C[a][b] for b in idx] for a in idx]
            d = det(sub)
            if d[1] != 0 or d[0] < 0:
                return False
    return True


IDENT: Chan = ([[F(1) if i == j else F(0) for j in range(3)] for i in range(3)],
               [F(0)] * 3)
DEPH: Chan = ([[F(0)] * 3, [F(0)] * 3, [F(0), F(0), F(1)]], [F(0)] * 3)
TRANS: Chan = ([[F(1), F(0), F(0)], [F(0), F(-1), F(0)], [F(0), F(0), F(1)]],
               [F(0)] * 3)

R_Z: Bloch = [F(0), F(0), F(1)]     # |0><0|
R_MZ: Bloch = [F(0), F(0), F(-1)]   # |1><1|  -- ORTHOGONAL to |0>
R_X: Bloch = [F(1), F(0), F(0)]     # |+><+|  -- NONorthogonal to |0>
R_Y: Bloch = [F(0), F(1), F(0)]     # |+i><+i|


def _det_family(rho: Mat) -> Mat:
    """F(rho) = (1 - 4 det rho) rho + 4 det rho (I/2).  Positive, trace
    preserving, fixes every PURE state, NOT affine-linear, not the identity."""
    d = _ca(_cm(rho[0][0], rho[1][1]), (-_cm(rho[0][1], rho[1][0])[0],
                                        -_cm(rho[0][1], rho[1][0])[1]))
    lam = F(1) - 4 * d[0]
    out = _mscale(lam, rho)
    return _madd(out, _mscale(4 * d[0] / 2, ID2))


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


GRID = (F(-1), F(-1, 2), F(0), F(1, 3), F(1, 2), F(1))


# ==========================================================================
def check_L_two_ray_pure_fixed_point_rigidity_M2() -> Dict[str, object]:
    """Tier 3, [P_math]."""
    fails: List[str] = []

    tally = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
            tally[0] += 1

    # ---- L0: the harness must certify the identity before anything else.
    ck(_psd(_choi(IDENT)),
       "SANITY: the identity channel must be CP -- if this fails the Choi "
       "builder is wrong and every verdict below is noise")
    ck(_act(IDENT, R_Z) == R_Z and _act(IDENT, R_X) == R_X,
       "SANITY: and it must fix both calibration states")

    # ---- L1: DISTINCTNESS is the hypothesis, and it is not automatic.
    # v = (1,0) and w = i(1,0) are distinct unit vectors with overlap i != 0
    # and the SAME projector.  Exhibited so the corrected hypothesis is
    # exercised rather than assumed.
    ck(R_Z != R_X, "the two calibration states must be DISTINCT as rays")
    ck(sum((R_Z[k] * R_X[k] for k in range(3)), F(0)) != F(-1),
       "and NONORTHOGONAL -- not antipodal in Bloch")
    # Built from the vectors, not asserted: v = (1,0), w = i(1,0).
    v: List[Cx] = [ONE, ZERO]
    w: List[Cx] = [IU, ZERO]

    def _proj(u: List[Cx]) -> Mat:
        return [[_cm(u[a], (u[b][0], -u[b][1])) for b in range(2)] for a in range(2)]

    def _ip(u: List[Cx], z: List[Cx]) -> Cx:
        return _ca(_cm((u[0][0], -u[0][1]), z[0]), _cm((u[1][0], -u[1][1]), z[1]))

    ck(v != w and _ip(v, w) != ZERO,
       "the counterexample vectors must be DISTINCT with NONZERO overlap -- "
       "v = (1,0), w = i(1,0), <v,w> = i")
    ck(_proj(v) == _proj(w),
       "yet their PROJECTORS must be EQUAL -- so 'distinct unit vectors with "
       "nonzero overlap' does NOT imply distinct rays, and the hypothesis of "
       "this theorem is distinct RAYS")
    # entry-wise, so there is no `A == B` for a mutation to collapse to `A == A`
    Pv = _proj(v)
    ck(Pv[0][0] == ONE and Pv[0][1] == ZERO and Pv[1][0] == ZERO
       and Pv[1][1] == ZERO,
       "and that shared projector must BE |0><0| entry by entry")
    ck(_act(DEPH, R_Z) == R_Z and DEPH != IDENT,
       "which DEPHASING fixes while not being the identity -- the counterexample "
       "the corrected hypothesis rules out")

    # ---- L1b: THE AFFINE SECTOR IS EXERCISED.  Found by mutation: every
    # channel this module builds has translation t = 0, so deleting t from _act
    # and from _phi -- the Choi builder every verdict below depends on -- changed
    # no result and both mutations escaped.  A translation-carrying channel is
    # built here and its action is checked against a hand-computed image, so the
    # translation is load-bearing somewhere in the module.
    SHIFT: Chan = ([[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]],
                   [F(0), F(0), F(1, 2)])
    ck(_act(SHIFT, R_X) == [F(1), F(0), F(1, 2)],
       "the affine part must ACT: a channel with t = (0,0,1/2) must send the "
       "Bloch vector (1,0,0) to (1,0,1/2), or the translation is dead code and "
       "every verdict that reads _act is blind to it")
    ck(_act(SHIFT, R_Z) != R_Z,
       "and that channel must NOT fix |0><0|, so it is a genuine translation "
       "and not a disguised identity")
    ck(_phi(SHIFT, ID2) != _phi(IDENT, ID2),
       "and the translation must reach _phi as well -- the Choi builder every "
       "CP verdict in this module depends on")
    ck(_act(([[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]],
             [F(0)] * 3), R_X) == R_X,
       "while the t = 0 control must still fix it, so the row above is about the "
       "translation and not about a broken matrix action")

    # ---- L2: NONORTHOGONALITY is what excludes dephasing, not CP.
    ck(_act(DEPH, R_Z) == R_Z and _act(DEPH, R_MZ) == R_MZ,
       "dephasing must fix |0><0| and |1><1|")
    ck(R_Z == [-x for x in R_MZ],
       "and that pair must be ANTIPODAL in Bloch, i.e. ORTHOGONAL states -- so "
       "dephasing does not satisfy the hypothesis")
    ck(_act(DEPH, R_X) != R_X,
       "dephasing must FAIL the cross-basis calibration at |+><+|")
    # ONE named Choi matrix, ASSERTED to be dephasing's before it is tested.  The
    # earlier two-line form asserted a property of DEPH while taking PSD of a
    # separately-written expression, so substituting the identity inside that
    # expression survived: the verdict and the assertion were not the same object.
    choi_deph = _choi(DEPH)
    ck(choi_deph[0][3] == ZERO and choi_deph[1][2] == ZERO,
       "the Choi matrix under test must be DEPHASING's -- BOTH coherence corners "
       "vanish, where the identity has 1 at (0,3) and transposition has 1 at "
       "(1,2) -- so no swapped object can carry the CP verdict below")
    deph_cp = _psd(choi_deph)
    ck(deph_cp,
       "and dephasing must BE completely positive -- so complete positivity "
       "does NOT exclude it, and the premise that does is nonorthogonality")

    # ---- L3: COMPLETE POSITIVITY is what excludes transposition.
    ck(_act(TRANS, R_Z) == R_Z and _act(TRANS, R_X) == R_X,
       "transposition must fix |0><0| and |+><+| -- a genuinely NONORTHOGONAL "
       "pair, so it satisfies the calibration hypothesis")
    trans_cp = _psd(_choi(TRANS))
    ck(_act(TRANS, R_Y) == [-x for x in R_Y] and TRANS != IDENT,
       "and the non-CP verdict must be tied to TRANSPOSITION specifically: it "
       "must flip sigma_y, which the identity and the depolarizing maps do not")
    ck(_choi(TRANS) != _choi(IDENT),
       "and the Choi matrix under test must be TRANSPOSITION's, distinct from "
       "the identity's")
    ck(not trans_cp,
       "but transposition must NOT be completely positive -- CP is what "
       "excludes it, and CP is load-bearing exactly here")
    ck(TRANS != IDENT, "and it must not be the identity, or it is no witness")

    # ---- L4: THE THEOREM, by Choi elimination.
    # Fixing |0><0| and |+><+| pins six of the twelve affine parameters, leaving
    # six free: the translation t and the middle column.  This scan pins t = 0
    # and scans the three column entries -- three of the six, NOT "the
    # remainder", which an earlier comment claimed and the header contradicted.
    # The fixed-point filter below is baked into the parametrization and rejects
    # nothing (0 of 216 candidates); what this leg tests is complete positivity.
    ck(GRID == (F(-1), F(-1, 2), F(0), F(1, 3), F(1, 2), F(1)) and len(GRID) == 6,
       "the scan grid must be the stated six-point grid -- pinned, because a "
       "grid reduced to the identity point still certifies uniqueness")
    survivors = []
    for m01 in GRID:
        for m11 in GRID:
            for m21 in GRID:
                cand: Chan = ([[F(1), m01, F(0)],
                               [F(0), m11, F(0)],
                               [F(0), m21, F(1)]], [F(0)] * 3)
                if _act(cand, R_Z) != R_Z or _act(cand, R_X) != R_X:
                    continue
                if _psd(_choi(cand)):
                    survivors.append((m01, m11, m21))
    ck(survivors == [(F(0), F(1), F(0))],
       "THE THEOREM: the ONLY CP survivor fixing both nonorthogonal states is "
       "the identity (survivors: %s)" % (survivors,))

    # THE SECOND-PAIR SCAN IS DELETED, not retained as a fixture.  Its
    # parametrization was pinned by the first fixed-point condition alone, before
    # positivity or the second pair was consulted, so it certified nothing about
    # the complex slice -- deleting complete positivity from it left it passing.
    # The vacuity is asserted here so the deletion is on the record, and the
    # rebuild (scan the free directions: column 1 and t) is fix item 1.
    scan2_would_be_vacuous = all(
        _act(([[F(1), F(0), m], [F(0), F(1), F(0)], [F(0), F(0), F(1)]],
              [F(0)] * 3), R_Z) != R_Z
        for m in (F(1), F(-1), F(1, 2)))
    ck(scan2_would_be_vacuous,
       "RECORD: the deleted second-pair scan was vacuous -- its first "
       "fixed-point condition alone pinned every scanned parameter, so no "
       "fixed-point condition alone pinned every scanned parameter. What this "
       "leg records is THAT VACUITY; that no complex-slice claim rests on a scan "
       "is a property of the module, asserted in the header, not computed here")
    survivors_y = "DELETED -- vacuous by construction, see the record leg above"

    # ==================================================================
    # L4b: THE KRAUS / CAUCHY-SCHWARZ ELIMINATION.
    #
    # This SUPERSEDES the grid as the route to the theorem, and it is what
    # closes fix items 1 and 2 of the landing note together: it is general in
    # the Kraus rank, it is not a scan, and because it never coordinatizes a
    # "real slice" at all there is no complex-slice gap left for a second-pair
    # scan to cover.  The grid above is retained as a corroborating fast path,
    # not as the evidence.
    #
    # THE ARGUMENT, in the five steps the note names:
    #  (i)   RANGE STEP.  If sum_k A_k rho A_k* = rho with rho = |psi><psi|
    #        rank one, every summand is PSD and the sum is rank one, so each
    #        A_k|psi> lies in span{|psi>}: A_k|psi> = lam_k |psi>.  Same at
    #        |phi>: A_k|phi> = mu_k |phi>.
    #  (ii)  DISTINCTNESS makes {psi, phi} a basis of C^2, so each A_k is
    #        determined by (lam_k, mu_k).  With psi = (1,0) and phi = (a,b),
    #        b != 0, and c := a/b, that operator is exactly
    #             A_k = [[lam_k, (mu_k - lam_k) c], [0, mu_k]].
    #        NONORTHOGONALITY is <psi|phi> = conj(a) != 0, i.e. c != 0.
    #  (iii) TRACE PRESERVATION sum_k A_k* A_k = I reads off as three exact
    #        equations:
    #             (1,1)  sum |lam_k|^2                     = 1
    #             (1,2)  c * sum conj(lam_k)(mu_k - lam_k)  = 0
    #             (2,2)  |c|^2 sum |mu_k - lam_k|^2 + sum |mu_k|^2 = 1
    #  (iv)  Since c != 0, (1,2) gives sum conj(lam_k) mu_k = sum |lam_k|^2 = 1.
    #        CAUCHY-SCHWARZ on the vectors (lam_k), (mu_k) then forces
    #        sum |mu_k|^2 >= 1, while (2,2) forces sum |mu_k|^2 <= 1.  Hence
    #        equality, hence |c|^2 sum |mu_k - lam_k|^2 = 0, hence -- c being
    #        non-zero -- mu_k = lam_k for every k.
    #  (v)   Then A_k = lam_k I and Phi(rho) = (sum |lam_k|^2) rho = rho.
    #
    # WHAT IS EXECUTED AND WHAT IS IMPORTED, stated so the grade can be read.
    # IMPORTED, both standard and both NAMED rather than re-proved here: the
    # range step (a sum of PSD matrices equal to a rank-one PSD matrix has every
    # summand supported in the range of the sum) and the Cauchy-Schwarz equality
    # condition.  EXECUTED below: that the claimed operator family really does
    # fix both projectors; that the three TP equations are exactly what
    # sum A* A = I reads off; that on a stated exact value set at Kraus rank 2
    # AND rank 3 every TP solution has mu = lam; and that at c = 0 the same
    # search admits mu != lam, which is what makes nonorthogonality
    # load-bearing rather than decorative.  The finite search CORROBORATES the
    # general statement; step (iv) is what proves it.  The search is not billed
    # as the proof.
    # ==================================================================
    def _kr(lam, mu, cc):
        """The step-(ii) operator, built from its eigenvalues alone."""
        return [[lam, _cm(_csub(mu, lam), cc)], [ZERO, mu]]

    # (ii) EXECUTED: the family fixes both projectors.  a = 3/5, b = 4/5, so
    # c = 3/4 and <psi|phi> = 3/5 != 0 -- genuinely nonorthogonal, and the same
    # overlap the module's own two rays carry.
    C_NO = (F(3, 4), F(0))
    fixes_rows = 0
    for lam, mu in ((( F(3, 5), F(0)), (F(0), F(4, 5))),
                    ((F(1), F(0)),     (F(0), F(1))),
                    ((F(0), F(1)),     (F(-1), F(0)))):
        A = _kr(lam, mu, C_NO)
        ck(_mv(A, _PSI) == _sv(lam, _PSI),
           "step (ii): the built operator must send psi to lam*psi")
        ck(_mv(A, _PHI) == _sv(mu, _PHI),
           "step (ii): the built operator must send phi to mu*phi")
        fixes_rows += 1
    ck(fixes_rows == 3, "the step-(ii) battery must have run")
    # and the two rays must be DISTINCT and NONORTHOGONAL, or (ii)/(iv) are void
    ck(_PSI != _PHI and _ovl(_PSI, _PHI) == (F(3, 5), F(0)),
       "the calibration rays must be distinct with overlap 3/5 != 0 -- "
       "distinctness is what makes {psi,phi} a basis and nonorthogonality is "
       "what makes c != 0")
    ck(C_NO != ZERO, "and c must be non-zero, which is step (iv)'s divisor")
    # CONJUGATE-LINEARITY OF THE OVERLAP, tested where it is VISIBLE.  Found by
    # mutation: both calibration vectors have real entries, so making _ovl
    # linear instead of conjugate-linear in its first slot changes nothing about
    # the assertion above and the module could not see it.  <i*e0 | e0> = -i
    # under the correct convention and +i under the wrong one, so this row
    # separates them; the nonorthogonality reading depends on the overlap being
    # the inner product it is billed as.
    ck(_ovl([IU, ZERO], [ONE, ZERO]) == (F(0), F(-1)),
       "the overlap must be CONJUGATE-linear in its first argument: "
       "<i*e0|e0> = -i, not +i -- untestable on the real calibration pair, so "
       "it is pinned here on a complex one")
    ck(_ovl([ONE, ZERO], [IU, ZERO]) == IU,
       "and linear in its second: <e0|i*e0> = +i")

    # (iii) EXECUTED: the three equations ARE sum A* A - I, read off exactly.
    def _tp_residual(lams, mus, cc):
        acc = [[ZERO, ZERO], [ZERO, ZERO]]
        for lam, mu in zip(lams, mus):
            A = _kr(lam, mu, cc)
            acc = _madd(acc, _m2mul(_m2dag(A), A))
        return [[_csub(acc[i][j], ONE if i == j else ZERO)
                 for j in range(2)] for i in range(2)]

    def _three_eqs(lams, mus, cc):
        e11 = sum((_cabs2(l) for l in lams), F(0)) - F(1)
        acc = ZERO
        for l, m in zip(lams, mus):
            acc = _ca(acc, _cm(_cconj(l), _csub(m, l)))
        e12 = _cm(cc, acc)
        e22 = (_cabs2(cc) * sum((_cabs2(_csub(m, l)) for l, m in zip(lams, mus)), F(0))
               + sum((_cabs2(m) for m in mus), F(0))) - F(1)
        return e11, e12, e22

    eq_rows = 0
    for lams, mus in ((((F(3, 5), F(0)), (F(0), F(4, 5))),
                       ((F(3, 5), F(0)), (F(0), F(4, 5)))),
                      (((F(1), F(0)), (F(0), F(0))),
                       ((F(0), F(0)), (F(0), F(1)))),
                      (((F(1, 2), F(0)), (F(0), F(1, 2))),
                       ((F(1, 3), F(0)), (F(0), F(2, 3))))):
        R = _tp_residual(list(lams), list(mus), C_NO)
        e11, e12, e22 = _three_eqs(list(lams), list(mus), C_NO)
        # the residual's three independent entries ARE the three equations
        ck(R[0][0] == (e11, F(0)),
           "step (iii): residual entry (1,1) must equal sum|lam|^2 - 1")
        ck(R[0][1] == e12,
           "step (iii): residual entry (1,2) must equal c*sum conj(lam)(mu-lam)")
        ck(R[1][1] == (e22, F(0)),
           "step (iii): residual entry (2,2) must equal "
           "|c|^2 sum|mu-lam|^2 + sum|mu|^2 - 1")
        ck(R[1][0] == _cconj(R[0][1]),
           "and the residual must be Hermitian, so (2,1) carries no new equation")
        eq_rows += 1
    ck(eq_rows == 3,
       "the read-off battery must have run on all three rows (a count only -- "
       "non-vacuity is the assertion immediately below, not this one)")
    ck(any(_three_eqs(list(l), list(m), C_NO) != (F(0), ZERO, F(0))
           for l, m in ((((F(1, 2), F(0)), (F(0), F(1, 2))),
                         ((F(1, 3), F(0)), (F(0), F(2, 3)))),)),
       "and at least one of those rows must VIOLATE the equations, or the "
       "read-off was only ever tested at zero")

    # (iv) EXECUTED as corroboration: over a stated exact value set, at Kraus
    # rank 2 AND rank 3, every TP solution has mu = lam.
    _VALS = ((F(0), F(0)), (F(1), F(0)), (F(-1), F(0)), (F(1, 2), F(0)),
             (F(0), F(1)), (F(3, 5), F(0)), (F(4, 5), F(0)))
    ck(set(_VALS) == {(F(0), F(0)), (F(1), F(0)), (F(-1), F(0)), (F(1, 2), F(0)),
                      (F(0), F(1)), (F(3, 5), F(0)), (F(4, 5), F(0))}
       and len(_VALS) == 7,
       "the elimination value set must be SET-EXACT against the stated seven "
       "values -- a length plus a membership test is not a contract, and two "
       "different seven-element sets escaped it: one reduced to roots of unity, "
       "one with 4/5 removed, which is the only value admitting a non-phase "
       "trace-preserving solution")
    # The rank-3 sweep runs on a REDUCED four-value subset: the full seven at
    # rank 3 is 7^3 x 7^3 = 117,649 exact PSD-free residual evaluations, which is
    # too slow to sit in a banked check.  The subset is stated, it retains 0 and
    # the complex entry, and the point of the rank-3 row is that the conclusion
    # is not a rank-2 artifact -- not that it is exhaustive.  An off-line sweep
    # of the full seven at rank 3 was also run and agreed (12 solutions, none
    # with mu != lam); that is recorded, not relied on.
    _VALS3 = (ZERO, ONE, (F(0), F(1)), (F(3, 5), F(0)))
    ck(set(_VALS3) == {ZERO, ONE, (F(0), F(1)), (F(3, 5), F(0))}
       and len(_VALS3) == 4 and set(_VALS3) <= set(_VALS),
       "the rank-3 subset must be SET-EXACT against the stated four values and "
       "a subset of the seven -- reducing it to roots of unity escaped a "
       "length-plus-membership guard")

    def _is_tp(lams, mus, cc):
        R = _tp_residual(list(lams), list(mus), cc)
        return R[0][0] == ZERO and R[0][1] == ZERO and R[1][1] == ZERO

    elim = {}
    for rank, vals in ((2, _VALS), (3, _VALS3)):
        for cc, tag in ((C_NO, 'nonorth'), (ZERO, 'orth')):
            tot = bad = 0
            for lams in product(vals, repeat=rank):
                for mus in product(vals, repeat=rank):
                    if _is_tp(lams, mus, cc):
                        tot += 1
                        if lams != mus:
                            bad += 1
            elim[(rank, tag)] = (tot, bad)
    for rank in (2, 3):
        tot, bad = elim[(rank, 'nonorth')]
        ck(tot > 0 and bad == 0,
           "THE ELIMINATION at Kraus rank %d: every trace-preserving solution "
           "must have mu = lam (found %d solutions, %d with mu != lam)"
           % (rank, tot, bad))
        tot0, bad0 = elim[(rank, 'orth')]
        ck(bad0 > 0,
           "NONORTHOGONALITY IS LOAD-BEARING at Kraus rank %d: with c = 0 the "
           "SAME search must admit mu != lam (found %d such) -- otherwise the "
           "premise is decorative and the elimination proves too much"
           % (rank, bad0))
    # THE OFF-DIAGONAL EQUATION IS LOAD-BEARING, AND THE SWEEP DOES NOT SHOW IT.
    # Found by mutation: dropping the (1,2) condition from _is_tp leaves the
    # sweep passing, because dropping a constraint only ADMITS more solutions and
    # on this value set none of the extra ones has mu != lam.  So the sweep
    # corroborates the CONCLUSION without isolating the step that carries
    # nonorthogonality -- exactly the "a battery measures where its author
    # aimed" failure.  The witness below closes it.
    #
    # Solving the (1,1) and (2,2) equations at Kraus rank 1 with lam = 1 gives
    # 25 x^2 - 18 x - 7 = 0, whose roots are x = 1 (the identity) and
    # x = -7/25.  The second root satisfies BOTH diagonal equations EXACTLY,
    # has mu != lam, and is rejected by the off-diagonal equation ALONE.
    _W_LAM = [ONE]
    _W_MU = [(F(-7, 25), F(0))]
    _w_e11, _w_e12, _w_e22 = _three_eqs(_W_LAM, _W_MU, C_NO)
    ck(_w_e11 == F(0),
       "the off-diagonal witness must satisfy the (1,1) equation exactly")
    ck(_w_e22 == F(0),
       "and the (2,2) equation exactly -- it is a genuine root of the diagonal "
       "system, not an approximation")
    ck(_W_MU != _W_LAM,
       "and it must have mu != lam, or it is no witness at all")
    ck(_w_e12 != ZERO,
       "but it must VIOLATE the off-diagonal equation -- that equation is the "
       "one carrying the factor c, so this is where nonorthogonality does its "
       "work in the elimination")
    _w_res = _tp_residual(_W_LAM, _W_MU, C_NO)
    ck(_w_res[0][0] == ZERO and _w_res[1][1] == ZERO and _w_res[0][1] != ZERO,
       "and the full residual must vanish on BOTH diagonal entries while the "
       "off-diagonal entry does not -- so the witness is excluded by exactly "
       "one of the three equations")
    ck(not _is_tp(_W_LAM, _W_MU, C_NO),
       "so _is_tp must REJECT it: this is the guard that catches an _is_tp "
       "which drops the off-diagonal condition, which the sweep does not catch")

    # and the orthogonal survivor must be DEPHASING, not any old solution
    ck(_is_tp([ONE, ZERO], [ZERO, ONE], ZERO),
       "and at c = 0 the explicit dephasing Kraus pair lam=(1,0), mu=(0,1) "
       "must itself be trace preserving -- the named survivor, not a nameless one")

    # (v) EXECUTED: mu = lam collapses the operator to a scalar.
    for lam in ((F(3, 5), F(0)), (F(0), F(1)), (F(-1), F(0))):
        A = _kr(lam, lam, C_NO)
        ck(A == [[lam, ZERO], [ZERO, lam]],
           "step (v): mu = lam must collapse the operator to lam*I, which is "
           "what makes the channel the identity")

    # ---- L5: the ORTHOGONAL-pair survivor set, exhibited.
    surv_o = []
    for m00 in GRID:
        for m01 in GRID:
            for m11 in GRID:
                cand: Chan = ([[m00, m01, F(0)],
                               [F(0), m11, F(0)],
                               [F(0), F(0), F(1)]], [F(0)] * 3)
                if _act(cand, R_Z) != R_Z or _act(cand, R_MZ) != R_MZ:
                    continue
                if _psd(_choi(cand)):
                    surv_o.append((m00, m01, m11))
    ck(len(surv_o) > 1 and any(s != (F(1), F(0), F(1)) for s in surv_o),
       "NEGATIVE CONTROL: with an ORTHOGONAL calibration pair the CP survivors "
       "are NOT unique (%d found, at least one not the identity) -- so 'two "
       "orthogonal calibrations are enough' is FALSE" % len(surv_o))

    # ---- L6: AFFINITY is a THIRD load-bearing antecedent, uncontrolled by the
    # other two.  The det-family fixes every pure state and is not the identity.
    pures = [R_Z, R_MZ, R_X, [F(-1), F(0), F(0)], R_Y, [F(0), F(-1), F(0)]]
    fixes_all = all(_det_family(_state(r)) == _state(r) for r in pures)
    ck(len({tuple(r) for r in pures}) == len(pures) == 6,
       "the pure-ray battery must contain SIX DISTINCT rays, or 'fixes every "
       "pure state' is six copies of one witness")
    ck(fixes_all,
       "THIRD ANTECEDENT: the det-family must fix EVERY pure state tested (%d) "
       "-- so it survives both calibrations AND an arbitrarily dense pure-ray "
       "cover" % len(pures))
    mixed = _state([F(0), F(0), F(1, 2)])
    ck(_det_family(mixed) != mixed,
       "and it must NOT be the identity on a MIXED state, or it is no "
       "counterexample")
    # SCOPE, EXECUTED: F is positive and trace preserving on the TRACE-ONE slice
    # only.  On the cone it is neither, and F(I) = -I is the witness.  So "dies
    # only to affinity" is withdrawn -- cone positivity excludes it too.
    FI = _det_family(ID2)
    ck(FI == _mscale(F(-1), ID2),
       "SCOPE: F(I) must equal -I -- the witness that F is NOT positive and NOT "
       "trace preserving on the positive cone (got %s)" % (FI,))
    ck(_ca(FI[0][0], FI[1][1]) != _ca(ID2[0][0], ID2[1][1]),
       "and its trace must differ from the input's, so 'trace preserving' is a "
       "trace-one-slice statement and not a property of the map")
    cone_pos_fails = (FI[0][0][0] < 0)
    ck(cone_pos_fails,
       "and cone positivity must FAIL on it, so 'the det-family dies only to "
       "affinity' is WITHDRAWN: positivity on the cone excludes it as well")
    # and positivity ON THE SLICE, which is the claim that survives
    slice_pos = True
    for r in pures + [[F(0), F(0), F(1, 2)], [F(1, 3), F(0), F(0)],
                      [F(1, 5), F(0), F(2, 5)]]:
        img = _det_family(_state(r))
        d = img[0][0][0] * img[1][1][0] - (img[0][1][0] * img[1][0][0]
                                          - img[0][1][1] * img[1][0][1])
        if img[0][0][0] < 0 or img[1][1][0] < 0 or d < 0:
            slice_pos = False
    ck(slice_pos,
       "while ON the trace-one slice F must be positive on every tested state -- "
       "the narrower claim that survives")

    tr_ok = True
    for r in pures + [[F(0), F(0), F(1, 2)], [F(1, 3), F(0), F(0)]]:
        s = _state(r)
        img = _det_family(s)
        if _ca(img[0][0], img[1][1]) != _ca(s[0][0], s[1][1]):
            tr_ok = False
    ck(tr_ok,
       "and it must be trace preserving, or it is excluded by normalization "
       "rather than by affinity")

    key = (
        "TWO-RAY RIGIDITY ON M2(C), WITH ITS THREE ANTECEDENTS SEPARATED. A CPTP "
        "map fixing two DISTINCT NONORTHOGONAL pure states is the identity. "
        "PROVED by the Kraus / Cauchy-Schwarz elimination, general in the Kraus "
        "rank: fixing a pure state makes its vector an eigenvector of every "
        "Kraus operator (range step, IMPORTED), distinctness makes the two "
        "eigenvectors a basis of C^2, trace preservation reads off as three "
        "exact equations, and the equation carrying the factor c -- the one that "
        "NEEDS nonorthogonality to be non-vacuous -- with Cauchy-Schwarz "
        "(IMPORTED) squeezes sum|mu|^2 between >= 1 and <= 1, forcing mu = lam, "
        "hence every Kraus operator scalar, hence the identity. CORROBORATED, "
        "not proved, by an exact finite search: at Kraus rank 2 over seven "
        "stated values and at rank 3 over a stated four-value subset, every "
        "trace-preserving solution has mu = lam (%d and %d solutions, ZERO "
        "with mu != lam). NONORTHOGONALITY IS LOAD-BEARING AND COMPUTED AS SUCH: "
        "at c = 0 the SAME search admits mu != lam (%d and %d such), with the "
        "explicit dephasing Kraus pair as the named survivor. A secondary "
        "finite Choi grid scan corroborates on a t = 0 slice; it is not the "
        "evidence, and no complex-slice claim rests on a scan -- the "
        "elimination never coordinatizes a slice. DISTINCT is load-bearing: "
        "v = (1,0) and w = i(1,0) are distinct unit vectors with nonzero "
        "overlap and the SAME projector, so the hypothesis is distinct RAYS. "
        "THE DIVISION OF LABOUR, each with its own witness: nonorthogonality "
        "excludes dephasing (which IS completely positive, and fixes an "
        "ORTHOGONAL pair, so CP does not reach it); complete positivity "
        "excludes transposition (which fixes a nonorthogonal pair and is "
        "positive and trace preserving but not CP); and AFFINITY is a third "
        "load-bearing antecedent that neither of the other two controls -- "
        "F(rho) = (1 - 4 det rho) rho + 4 det rho (I/2) fixes EVERY pure state, "
        "is not the identity, and is positive and trace preserving ON THE "
        "TRACE-ONE SLICE ONLY: F(I) = -I, so cone positivity excludes it too "
        "and 'dies only to affinity' is WITHDRAWN. With an ORTHOGONAL "
        "calibration pair the CP survivors are not unique. So 'two "
        "nonorthogonal calibrations are enough' is FALSE as stated: three "
        "antecedents carry the theorem."
        % (elim[(2, 'nonorth')][0], elim[(3, 'nonorth')][0],
           elim[(2, 'orth')][1], elim[(3, 'orth')][1])
    )
    return _result(
        'L_two_ray_pure_fixed_point_rigidity_M2',
        'P_math | THREE NAMED STANDARD IMPORTS: the Kraus/Choi representation '
        'theorem, the PSD-range step, and the Cauchy-Schwarz INEQUALITY '
        '(not its equality condition). The general proof is a '
        'proof-of-record in the module header and is NOT executed; what '
        'executes is the read-off, the corroborating finite search and the '
        'witnesses. Exact rational and Gaussian-rational arithmetic '
        'throughout; no physical premise consumed',
        key,
        {
            "cp_survivors_nonorthogonal_real_pair": [list(map(str, s)) for s in survivors],
            "cp_survivors_nonorthogonal_complex_pair": survivors_y,
            "elimination_rank2_nonorth_solutions": elim[(2, 'nonorth')][0],
            "elimination_rank2_nonorth_mu_ne_lam": elim[(2, 'nonorth')][1],
            "elimination_rank3_nonorth_solutions": elim[(3, 'nonorth')][0],
            "elimination_rank3_nonorth_mu_ne_lam": elim[(3, 'nonorth')][1],
            "elimination_rank2_orth_mu_ne_lam": elim[(2, 'orth')][1],
            "elimination_rank3_orth_mu_ne_lam": elim[(3, 'orth')][1],
            "elimination_imports_named": ["Kraus/Choi representation theorem",
                                         "PSD-range step",
                                         "Cauchy-Schwarz inequality"],
            "cp_survivors_orthogonal_pair_count": len(surv_o),
            "dephasing_is_CP": deph_cp,
            "transposition_is_CP": trans_cp,
            "det_family_fixes_all_tested_pure_states": fixes_all,
            "det_family_trace_preserving": tr_ok,
            "antecedents": ["distinct nonorthogonal rays", "complete positivity",
                            "affine linearity"],
        },
        fails, 3,
        (),   # no A1 edge: nothing here consumes a capacity axiom or a cost floor
        (),
        ("dephasing: CP, fixes an ORTHOGONAL pair, not the identity",
         "transposition: fixes a nonorthogonal pair, not CP, not the identity",
         "the det-family: fixes every pure state, trace preserving, not affine, "
         "not the identity",
         "the orthogonal calibration pair leaves more than one CP survivor"),
        ('L_covariant_state_maps_are_exactly_the_depolarizing_line',
         'L_complete_positivity_closes_the_sharpness_fence',
         'L_coherence_sector_separation'),
        fail_count=tally[0],
    )


_CHECKS = {
    'L_two_ray_pure_fixed_point_rigidity_M2': check_L_two_ray_pure_fixed_point_rigidity_M2,

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
