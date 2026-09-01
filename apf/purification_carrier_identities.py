"""The purification fibre and the carrier identities, at rectangular shapes.

WHAT THIS ADDS, AGAINST THE PRIOR ART (read this first).

The bank carries check_T_presentation_gauge_forces_trace (presentation_gauge_
forcing.py, v24.3.443) at [P_structural | P1 open, P2 gauge, P3 underived], and
check_T_same_type_reference_chosen_cp (quantum_frontend_closure.py), which
already computes the identity channel's Choi matrix at n = 2 and asserts it
equals the scaled Bell density -- |Omega><Omega| IS ALREADY IN THE BANK.

This module adds two exact finite results and nothing else:

  (1) THE PURIFICATION FIBRE AT FIXED SHAPE.  For b in M_{n x r}(C) the fibre of
      the local load quotient q(b) = b b* is exactly the right-unitary orbit
      b U(r) -- INCLUDING at rank deficiency.  That last clause retires a
      standing fence: the lane record had scoped the fibre reading to
      full-support loads on the ground that rank-deficient loads connect by
      partial isometries rather than unitaries.  At FIXED SHAPE the partial
      isometry extends and the orbit is still one U(r) orbit.

  (2) THE CARRIER IDENTITIES AT RECTANGULAR SHAPES.  The four vec/Choi
      identities at (n, r) = (2,2), (3,2), (2,3), (3,3), (4,3).  The one that
      carries the content is |bU>> = (I (x) U^T)|b>>: right-unitary freedom acts
      ENTIRELY on the reference leg, which IDENTIFIES the gauge group with the
      purification fibre.  It does NOT by itself show gauge is more than an
      asserted symmetry -- the same identity holds for arbitrary A (executed),
      so what selects the unitaries is load preservation, i.e. P2, which stays
      open.

NEITHER RESULT DISCHARGES ANYTHING.  P1 stays open, P2 stays a claim about
nature, P3 stays downstream of the carrier gate.  A companion attempt to build a
P2 discharge on top of (1) was cut on 2026-07-28 and killed by two blinded
auditors as CIRCULAR -- for q(b) = b b*, "q is the complete observable quotient"
IS the banked P2 in a second vocabulary.  Do not rebuild it.

============================================================================
STATEMENTS

check_L_purification_orbit_fibre (tier 3,
[P_math | the general statement is IMPORTED: polar decomposition plus extension
of the connecting partial isometry off the support]).

  INVARIANCE, computed: (bU)(bU)* = b b* on five shapes against an exact
  unitary pool.
  COMPLETENESS, computed as a FINITE WITNESS that is CARRIER-CONTINGENT and
  billed as such: over a bounded Gaussian-integer box -- genuinely Gaussian,
  real and imaginary parts both swept -- every carrier c with c c* = b b* is
  reached as c = bU by an EXHIBITED unitary, at FULL RANK (32 of 32) and at RANK
  DEFICIENCY (8 of 8), the connecting group being the 32-element MONOMIAL
  Gaussian-unitary group at n = 2 (all elements built, distinct, closed under
  multiplication, each verified unitary).  TWO SCOPE FACTS, EXECUTED IN-CHECK
  AND NOT TO BE DROPPED WHEN THIS IS QUOTED: the witness is NOT the general
  theorem -- an exact non-monomial Gaussian-rational unitary [[h,h],[h,-h]],
  h = (1+i)/2, lies outside the group and connects an in-box pair it does not
  reach; and the FULL-RANK half is ORBIT-BLIND, since with b = I the test
  reduces to U == c, so 32 of 32 is a fact about U(2) intersect M2(Z[i]) and
  only the 8 of 8 rank-deficient half is orbit-sensitive.
  CONTROLS: a non-unitary right move CHANGES the load, so invariance is not
  vacuous; and the two witnesses are verified to differ in rank by their load
  determinants, so the rank-deficient case is genuinely tested.

  FENCE, IN THE STATEMENT: fixed carrier shape.  Across shapes the claim is
  FALSE -- b = [1 0] (1x2) and c = [1] (1x1) share a load with no connecting
  unitary, because no unitary changes shape.

check_L_identity_carrier_vectorization (tier 3, [P_math]).

  Tr_R |b>><<b| = b b*, <<b|b>> = Tr(b* b), <<b|(e (x) I)|b>> = Tr(b* e b) =
  Tr(b b* e), and |bU>> = (I (x) U^T)|b>>, at (2,2), (3,2), (2,3), (3,3), (4,3).
  P3 rides Tr_R |Omega><Omega| = I at n = 2, 3, 4.
  CONTROLS: the effect probe is asserted NON-ZERO and NON-SCALAR (with a zero
  probe the sandwich identity degenerates to 0 == 0 and proves nothing); SWAP is
  computed NOT to be of the local form e (x) I while the genuine local effect
  IS, and SWAP fails the sandwich identity; a self-overlap is computed on a
  COMPLEX carrier and cross-checked against the norm, which fails the moment the
  inner product drops its conjugate -- a real carrier cannot see conjugation at
  all; and a non-unitary right move changes the marginal.  The vec law
  |bA>> = (I (x) A^T)|b>> is executed with a NON-UNITARY A as well, so it
  carries no unitarity content on its own.

============================================================================
MAY-NOT-CITE.

  - "Born is derived."  Nothing here touches Born.
  - "P2 is discharged" or "reduced."  The orbit-fibre route to P2 is CIRCULAR;
    two blinded auditors killed it on 2026-07-28.
  - "P3 is discharged."  The carrier's UNNORMALIZED marginal is I (which is what
    the code computes; I/n is the normalized form and is not computed here), and
    the carrier is K5, an open physical gate.
  - "The purification fibre theorem is proved here."  The general statement is
    an imported standard fact; what is proved is a finite witness at fixed shape.
  - "The fibre is the orbit across shapes."  False; the fence is in the
    statement.
  - "The full-support scope of T_presentation_gauge_forces_trace is retired."
    It is NOT.  That scope has a separate and still-live ground: at rank
    deficiency the invariance hypothesis is VACUOUS, so psi = c*Tr does not
    follow there.  Executed against the banked scorer by the audit: with
    b = [[1,0],[0,0]] and the non-tracial PSD weight R = diag(1,5), the score is
    constant across the full right-unitary fibre.  What this module retires is
    only the PARTIAL-ISOMETRY ground for that scope, not the scope.
  - "The completeness witness proves the general theorem."  It is
    CARRIER-CONTINGENT, executed: an exact non-monomial Gaussian-rational
    unitary connects an in-box pair the 32-element group does not reach.
  - "32 of 32 is a fibre fact."  With b = I it reduces to U == c, i.e. to
    U(2) intersect M2(Z[i]).  Only the 8 of 8 rank-deficient half is
    orbit-sensitive.
  - "|Omega><Omega| is new."  It is banked, at n = 2, in
    check_T_same_type_reference_chosen_cp.  This is an extension to general n
    and to rectangular carriers.

NON-EXPORTING.  physical_premises_certified = false.  No existing grade moved.
"""

from fractions import Fraction as F
from itertools import product
from typing import Dict, List, Optional, Tuple

PHYSICAL_PREMISES_CERTIFIED = False
EXPORTS: Tuple[str, ...] = ()
BANK_MODIFIED = False

G = Tuple[F, F]
Mat = List[List[G]]
Vec = List[G]

ZERO: G = (F(0), F(0))
ONE: G = (F(1), F(0))
IMAG: G = (F(0), F(1))


def _g(re, im=0) -> G:
    return (F(re), F(im))


def _add(a: G, b: G) -> G:
    return (a[0] + b[0], a[1] + b[1])


def _sub(a: G, b: G) -> G:
    return (a[0] - b[0], a[1] - b[1])


def _mul(a: G, b: G) -> G:
    return (a[0] * b[0] - a[1] * b[1], a[0] * b[1] + a[1] * b[0])


def _conj(a: G) -> G:
    return (a[0], -a[1])


def _gsum(xs) -> G:
    acc = ZERO
    for x in xs:
        acc = _add(acc, x)
    return acc


def _shape(A: Mat) -> Tuple[int, int]:
    return (len(A), len(A[0]) if A else 0)


def _mm(A: Mat, B: Mat) -> Mat:
    n, k = _shape(A)
    k2, m = _shape(B)
    assert k == k2, "inner dimensions must agree"
    return [[_gsum(_mul(A[i][p], B[p][j]) for p in range(k)) for j in range(m)]
            for i in range(n)]


def _dag(A: Mat) -> Mat:
    n, m = _shape(A)
    return [[_conj(A[j][i]) for j in range(n)] for i in range(m)]


def _transpose(A: Mat) -> Mat:
    n, m = _shape(A)
    return [[A[j][i] for j in range(n)] for i in range(m)]


def _tr(A: Mat) -> G:
    return _gsum(A[i][i] for i in range(len(A)))


def _eye(n: int) -> Mat:
    return [[ONE if i == j else ZERO for j in range(n)] for i in range(n)]


def _zeros(n: int, m: Optional[int] = None) -> Mat:
    m = n if m is None else m
    return [[ZERO for _ in range(m)] for _ in range(n)]


def _kron(A: Mat, B: Mat) -> Mat:
    an, am = _shape(A)
    bn, bm = _shape(B)
    out = _zeros(an * bn, am * bm)
    for i in range(an):
        for j in range(am):
            for k in range(bn):
                for l in range(bm):
                    out[i * bn + k][j * bm + l] = _mul(A[i][j], B[k][l])
    return out


def _mv(A: Mat, v: Vec) -> Vec:
    return [_gsum(_mul(A[i][j], v[j]) for j in range(len(v))) for i in range(len(A))]


def _inner(v: Vec, w: Vec) -> G:
    return _gsum(_mul(_conj(a), b) for a, b in zip(v, w))


def _outer(v: Vec) -> Mat:
    return [[_mul(a, _conj(b)) for b in v] for a in v]


def _is_unitary(U: Mat) -> bool:
    n, m = _shape(U)
    return n == m and _mm(_dag(U), U) == _eye(n)


def _det2(A: Mat) -> G:
    return _sub(_mul(A[0][0], A[1][1]), _mul(A[0][1], A[1][0]))


def _vec_columns(b: Mat) -> Vec:
    """|b>> = (b (x) I_r)|Omega_r>; component (i, j) at index i*r + j is b[i][j]."""
    n, r = _shape(b)
    return [b[i][j] for i in range(n) for j in range(r)]


def _omega(r: int) -> Vec:
    return _vec_columns(_eye(r))


def _partial_trace_reference(H: Mat, n: int, r: int) -> Mat:
    return [[_gsum(H[i * r + j][k * r + j] for j in range(r)) for k in range(n)]
            for i in range(n)]


# --- exact unitary families ------------------------------------------------

_GAUSSIAN_UNITS: Tuple[G, ...] = (ONE, _g(-1), IMAG, _g(0, -1))


def _monomial_gaussian_unitaries() -> List[Mat]:
    """The FULL monomial Gaussian-unitary group at n = 2: 2 permutations x 4
    phases x 4 phases = 32 elements.  Built, not sampled -- this is what makes
    the completeness witness close over a genuinely Gaussian box."""
    out: List[Mat] = []
    for perm in (0, 1):
        for u in _GAUSSIAN_UNITS:
            for v in _GAUSSIAN_UNITS:
                if perm == 0:
                    out.append([[u, ZERO], [ZERO, v]])
                else:
                    out.append([[ZERO, u], [v, ZERO]])
    return out


def _rot345(r: int) -> Mat:
    U = _eye(r)
    U[0][0] = _g(F(3, 5))
    U[0][1] = _g(F(-4, 5))
    U[1][0] = _g(F(4, 5))
    U[1][1] = _g(F(3, 5))
    return U


def _unitary_pool(r: int) -> List[Mat]:
    """A mixed pool for the INVARIANCE leg across shapes: exact rational
    rotations, quarter phases, and a swap."""
    pool = [_eye(r)]
    if r >= 2:
        pool.append(_rot345(r))
        sw = _eye(r)
        sw[0][0] = ZERO
        sw[1][1] = ZERO
        sw[0][1] = ONE
        sw[1][0] = ONE
        pool.append(sw)
    for a in range(r):
        ph = _eye(r)
        ph[a][a] = IMAG
        pool.append(ph)
    return pool


_CARRIERS: Dict[Tuple[int, int], Mat] = {
    (2, 2): [[_g(1), _g(0, 2)], [_g(3), _g(0, -1)]],
    (3, 2): [[_g(1), _g(2)], [_g(0, 1), _g(-1)], [_g(2), _g(0, 3)]],
    (2, 3): [[_g(1), _g(0, 1), _g(2)], [_g(0), _g(3), _g(-1)]],
    (3, 3): [[_g(1), _g(0, 1), _g(2)], [_g(0), _g(3), _g(-1)],
             [_g(4), _g(1), _g(0, -2)]],
    (4, 3): [[_g(1), _g(0, 1), _g(2)], [_g(0), _g(3), _g(-1)],
             [_g(4), _g(1), _g(0, -2)], [_g(0, 2), _g(-1), _g(1)]],
}
_SHAPES: Tuple[Tuple[int, int], ...] = ((2, 2), (3, 2), (2, 3), (3, 3), (4, 3))


def _result(name, epistemic, key_result, evidence, fails, tier,
            dependencies, premises, negative_controls, cross_refs,
            fail_count=None):
    """Build the result dict, and CROSS-ASSERT the two failure records HERE.

    CORRIGENDUM 2026-07-28 (execution audit, MAJOR): the cross-assert used to
    live only in this module's run_all().  The bank does NOT call run_all() --
    bank.py invokes each registered check_fn() directly and reads r['passed']
    (bank.py, the `r = check_fn()` / `if r['passed']:` loop).  So the guarantee
    did not travel on the banked path: a mutation forcing 'passed' True was
    demonstrated to report PASS to the bank with 359 recorded failures.  The
    assert now lives at the point the dict is BUILT, so it travels with the
    dict wherever the dict goes, and run_all() remains as a second gate.

    RESIDUAL LIMIT, DISCLOSED RATHER THAN OVERCLAIMED: this catches DIVERGENCE
    between the two failure records -- the realistic tampering, where a repair
    patches one recording site and not the other, and which is what previously
    escaped on the banked path.  It does NOT catch a bare literal substitution
    of the verdict itself ('passed': True), because nothing downstream
    re-derives that field: bank.py reads it.  No code inside a module can
    defend against an arbitrary edit to its own return statement; that is a
    property of the bank's contract, not of this module, and the earlier
    v24.3.449 commit message claimed the protection more broadly than is true."""
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
# LEG 1 -- the purification fibre at fixed shape.
# ==========================================================================

_WIT_FULL: Mat = [[ONE, ZERO], [ZERO, ONE]]
_WIT_RANK_DEFICIENT: Mat = [[ONE, ZERO], [ONE, ZERO]]


def check_L_purification_orbit_fibre() -> Dict[str, object]:
    """Tier 3, [P_math | general statement via polar decomposition IMPORTED]."""
    fails: List[str] = []
    tally = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
            tally[0] += 1

    # ---- (i) INVARIANCE across five shapes. --------------------------------
    invariance_rows = 0
    for (n, r) in _SHAPES:
        b = _CARRIERS[(n, r)]
        load = _mm(b, _dag(b))
        for U in _unitary_pool(r):
            ck(_is_unitary(U), f"the probe must be exactly unitary (r={r})")
            ck(_mm(_mm(b, U), _dag(_mm(b, U))) == load,
               f"a right-unitary move must preserve the load (n={n}, r={r})")
            invariance_rows += 1
    # POOL COMPOSITION, asserted.  A pool of identity copies passes any
    # row-count threshold while making both the invariance leg and the U^T
    # identity read 1 = 1.
    p2 = _unitary_pool(2)
    ck(len({tuple(tuple(r) for r in U) for U in p2}) == len(p2),
       "the unitary pool must have distinct elements")
    ck(any(_transpose(U) != U for U in p2),
       "the pool must contain a NON-SYMMETRIC unitary, or U^T is untested")
    ck(any(sum(1 for x in row if x != ZERO) > 1 for U in p2 for row in U),
       "the pool must contain a NON-MONOMIAL unitary, or the rotation leg is idle")
    ck(any(any(x[1] != 0 for x in row) for U in p2 for row in U),
       "the pool must contain a COMPLEX element, or conjugation is untested here")

    # ---- (ii) COMPLETENESS: exhaustive over a GENUINELY GAUSSIAN box. ------
    group = _monomial_gaussian_unitaries()
    ck(len(group) == 32,
       f"the monomial Gaussian-unitary group at n=2 has 32 elements, got {len(group)}")
    for U in group:
        ck(_is_unitary(U), "every element of the connecting group must be unitary")
    keys = {tuple(tuple(r) for r in U) for U in group}
    ck(len(keys) == 32, f"the group's elements must be distinct, got {len(keys)}")
    closed = all(tuple(tuple(r) for r in _mm(U, V)) in keys
                 for U in group for V in group)
    ck(closed, "the connecting group must be closed under multiplication")

    vals = (F(-1), F(0), F(1))
    box_counts: Dict[str, int] = {}
    unreached: List[str] = []
    complex_carriers_seen = 0
    for label, b in (("full_rank", _WIT_FULL),
                     ("rank_deficient", _WIT_RANK_DEFICIENT)):
        load = _mm(b, _dag(b))
        found = 0
        for e in product(vals, repeat=8):
            c = [[(e[0], e[1]), (e[2], e[3])], [(e[4], e[5]), (e[6], e[7])]]
            if _mm(c, _dag(c)) != load:
                continue
            found += 1
            if any(x[1] != 0 for row in c for x in row):
                complex_carriers_seen += 1
            if not any(_mm(b, U) == c for U in group):
                unreached.append(f"{label}:{e}")
        box_counts[label] = found
    # EXACT counts, not `found > 0`: the banked sentence quotes 32 and 8, so the
    # check must assert 32 and 8.
    ck(box_counts == {'full_rank': 32, 'rank_deficient': 8},
       f"the box hits must be exactly 32 and 8, got {box_counts}")
    ck(tuple(vals) == (F(-1), F(0), F(1)),
       "the box sweep must be the frozen value set")
    ck(not unreached,
       f"every same-load carrier in the Gaussian box must be reached by an "
       f"exhibited unitary; unreached={unreached[:3]}")
    # THE RANK-DEFICIENT WITNESS MUST BE NON-DEGENERATE.  The zero matrix passes
    # a det-only test and a `found > 0` test while proving nothing.
    rd_load_full = _mm(_WIT_RANK_DEFICIENT, _dag(_WIT_RANK_DEFICIENT))
    ck(any(x != ZERO for row in _WIT_RANK_DEFICIENT for x in row),
       "the rank-deficient witness must be non-zero")
    ck(any(x != ZERO for row in rd_load_full for x in row),
       "the rank-deficient witness must have a non-zero load")
    ck(box_counts['rank_deficient'] >= 2,
       "the rank-deficient box must have more than one member")
    # the box must actually be GAUSSIAN, or the certificate is a real-only claim
    ck(complex_carriers_seen > 0,
       "the box must contain carriers with a non-zero imaginary part, or the "
       "'Gaussian' billing is false")

    # ---- (ii-b) TWO DISCLOSURES THE AUDIT FORCED, both executed. -----------
    # (a) The group is NOT the Gaussian-rational unitaries.  An exact
    # non-monomial Gaussian-rational unitary exists and is outside it, so the
    # completeness witness is CARRIER-CONTINGENT: for other in-box carriers the
    # connecting unitary is outside the 32-element group.
    h = _g(F(1, 2), F(1, 2))
    U_nonmono: Mat = [[h, h], [h, (-h[0], -h[1])]]
    ck(_is_unitary(U_nonmono),
       "the non-monomial witness must be exactly unitary")
    ck(tuple(tuple(r) for r in U_nonmono) not in keys,
       "the non-monomial unitary must lie OUTSIDE the 32-element group, or the "
       "carrier-contingency disclosure is empty")
    b_alt: Mat = [[ONE, ONE], [ZERO, ZERO]]
    c_alt = _mm(b_alt, U_nonmono)
    ck(_mm(b_alt, _dag(b_alt)) == _mm(c_alt, _dag(c_alt)),
       "the alternative carrier pair must share a load")
    ck(not any(_mm(b_alt, U) == c_alt for U in group),
       "and must NOT be connected by the 32-element group -- this is why the "
       "witness is billed as carrier-contingent, not as the general theorem")
    # (b) The FULL-RANK half is orbit-blind: with b = I, _mm(b, U) == c reduces
    # to U == c, so 32/32 computes U(2) intersect M2(Z[i]), a fact about the
    # box's arithmetic.  Only the RANK-DEFICIENT half is orbit-sensitive.
    ck(_WIT_FULL == _eye(2),
       "the full-rank witness is the identity, which is what makes its half of "
       "the box computation orbit-blind")
    rd_load_b = _mm(_WIT_RANK_DEFICIENT, _dag(_WIT_RANK_DEFICIENT))
    orbit_blind_rd = 0
    for e in product(vals, repeat=8):
        c = [[(e[0], e[1]), (e[2], e[3])], [(e[4], e[5]), (e[6], e[7])]]
        if _mm(c, _dag(c)) != rd_load_b:
            continue
        if not any(U == c for U in group):     # the orbit map DELETED
            orbit_blind_rd += 1
    ck(orbit_blind_rd == 8,
       f"with the orbit map deleted the rank-deficient half must FAIL on all 8 "
       f"members -- that is what makes it orbit-sensitive; got {orbit_blind_rd}")

    # ---- (iii) the rank-deficient case is genuinely rank deficient. --------
    rd_det = _det2(_mm(_WIT_RANK_DEFICIENT, _dag(_WIT_RANK_DEFICIENT)))
    full_det = _det2(_mm(_WIT_FULL, _dag(_WIT_FULL)))
    ck(rd_det == ZERO, "the rank-deficient witness must have singular load")
    ck(full_det != ZERO, "the full-rank witness must have nonsingular load")

    # ---- (iv) CONTROL: a non-unitary right move changes the load. ----------
    b = _CARRIERS[(2, 2)]
    Nb: Mat = [[ONE, ONE], [ZERO, ONE]]
    ck(not _is_unitary(Nb), "the control must not be unitary")
    ck(_mm(_mm(b, Nb), _dag(_mm(b, Nb))) != _mm(b, _dag(b)),
       "a non-unitary right move must CHANGE the load, or invariance is vacuous")

    # ---- (v) THE SHAPE FENCE, EXECUTED.  Across shapes the claim is FALSE. -
    wide: Mat = [[ONE, ZERO]]          # 1 x 2
    narrow: Mat = [[ONE]]              # 1 x 1
    ck(_mm(wide, _dag(wide)) == _mm(narrow, _dag(narrow)),
       "the cross-shape witnesses must share a load")
    ck(_shape(wide) != _shape(narrow),
       "the cross-shape witnesses must differ in shape, so no unitary connects them")

    return _result(
        'L_purification_orbit_fibre',
        '[P_math | general statement via polar decomposition IMPORTED]',
        ("At FIXED SHAPE n x r the fibre of the local load quotient q(b) = b b* "
         "is exactly the right-unitary orbit b U(r).  Invariance is computed on "
         "five shapes against an exact unitary pool.  Completeness is computed "
         "as an EXHAUSTIVE finite witness over a bounded GAUSSIAN-integer box -- "
         "real and imaginary parts both swept, and the box verified to contain "
         "carriers with non-zero imaginary part -- with the connecting group the "
         "FULL 32-element monomial Gaussian-unitary group at n = 2, every element "
         "built and verified unitary: 32 of 32 same-load carriers reached at full "
         "rank, 8 of 8 at RANK DEFICIENCY, none unreached.  THE FENCE THIS "
         "REMOVES: the fibre reading was scoped to full-support loads on the "
         "ground that rank-deficient loads connect by partial isometries; at "
         "fixed shape the isometry extends and the orbit is still one U(r) orbit. "
         "THE FENCE THIS KEEPS, executed: across shapes the claim is FALSE -- "
         "[1 0] and [1] share a load and no unitary connects them, because no "
         "unitary changes shape.  THE GENERAL THEOREM IS IMPORTED: polar "
         "decomposition plus extension off the support is standard and is NOT "
         "proved here.  This does NOT discharge P2; the orbit-fibre route to P2 "
         "is circular and was killed by two blinded audits on 2026-07-28."),
        {
            'shapes_tested': [list(s) for s in _SHAPES],
            'invariance_rows_computed': invariance_rows,
            'connecting_group_order': len(group),
            'same_load_box_hits': dict(box_counts),
            'complex_carriers_in_box': complex_carriers_seen,
            'carriers_unreached': unreached,
            'rank_deficient_load_det': [str(rd_det[0]), str(rd_det[1])],
            'full_rank_load_det': [str(full_det[0]), str(full_det[1])],
            'general_statement_is_imported': 'polar_decomposition',
        },
        fails,
        3,
        (),
        ('FIXED_CARRIER_SHAPE',),
        ("a non-unitary right move changes the load",
         "the rank-deficient witness has singular load and the full-rank one does not",
         "across shapes the claim is false: [1 0] and [1] share a load",),
        ('T_presentation_gauge_forces_trace',),
        fail_count=tally[0],
    )


# ==========================================================================
# LEG 2 -- the carrier identities at rectangular shapes.
# ==========================================================================

def _is_local_form(M: Mat, n: int, r: int) -> bool:
    """An operator of the form e (x) I is block diagonal in the reference index."""
    for i in range(n):
        for k in range(n):
            for j in range(r):
                for l in range(r):
                    if j != l and M[i * r + j][k * r + l] != ZERO:
                        return False
    return True


def _herm_probe(n: int) -> Mat:
    """A genuinely COMPLEX Hermitian probe.  The earlier form
    A[i][j] = (i+1, (i*j) % 3) cancelled to a real matrix at every n -- the
    imaginary decoration vanished under A + A*, so the effect side never saw a
    complex effect.  Here the imaginary part is antisymmetric and survives."""
    A = [[_g(i + 1, i - j) for j in range(n)] for i in range(n)]
    return [[_add(A[i][j], _conj(A[j][i])) for j in range(n)] for i in range(n)]


def _is_scalar(M: Mat, n: int) -> bool:
    d = M[0][0]
    for i in range(n):
        for j in range(n):
            if i == j and M[i][j] != d:
                return False
            if i != j and M[i][j] != ZERO:
                return False
    return True


def check_L_identity_carrier_vectorization() -> Dict[str, object]:
    """Tier 3, [P_math].  The four identities, rectangular, with four controls."""
    fails: List[str] = []
    tally = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
            tally[0] += 1

    rows = 0
    for (n, r) in _SHAPES:
        b = _CARRIERS[(n, r)]
        v = _vec_columns(b)
        H = _outer(v)

        # THE EFFECT PROBE MUST BE NON-ZERO AND NON-SCALAR, or identity 3
        # degenerates: with e = 0 both sides are 0 and the leg proves nothing.
        e = _herm_probe(n)
        ck(any(x != ZERO for row in e for x in row),
           f"the effect probe must be non-zero (n={n})")
        ck(not _is_scalar(e, n),
           f"the effect probe must be non-scalar (n={n}), or the sandwich "
           f"identity is insensitive to the effect's structure")
        ck(_dag(e) == e, f"the effect probe must be Hermitian (n={n})")
        ck(any(x[1] != 0 for row in e for x in row),
           f"the effect probe must be genuinely COMPLEX (n={n}); a real probe "
           f"cannot exercise conjugation on the effect side")

        ck(_partial_trace_reference(H, n, r) == _mm(b, _dag(b)),
           f"Tr_R |b>><<b| must equal b b* (n={n}, r={r})")
        ck(_inner(v, v) == _tr(_mm(_dag(b), b)),
           f"<<b|b>> must equal Tr(b* b) (n={n}, r={r})")
        lhs = _inner(v, _mv(_kron(e, _eye(r)), v))
        ck(lhs == _tr(_mm(_dag(b), _mm(e, b))),
           f"a local effect must give Tr(b* e b) (n={n}, r={r})")
        ck(lhs == _tr(_mm(_mm(b, _dag(b)), e)),
           f"and must equal Tr(b b* e) (n={n}, r={r})")
        for U in _unitary_pool(r):
            ck(_vec_columns(_mm(b, U)) == _mv(_kron(_eye(n), _transpose(U)), v),
               f"|bU>> must equal (I (x) U^T)|b>> (n={n}, r={r})")
        rows += 1
    # SET-EXACT against a frozen literal.  `rows == len(_SHAPES)` was a
    # tautology: rows counts iterations of the loop over _SHAPES, so deleting a
    # shape escaped while the key_result kept certifying five.
    _CANON = ((2, 2), (3, 2), (2, 3), (3, 3), (4, 3))
    ck(tuple(_SHAPES) == _CANON,
       f"the shape list must match the frozen canonical tuple exactly, got {_SHAPES}")
    ck(rows == 5, f"exactly five shapes must run, got {rows}")

    # P3 rides identity 5.
    p3_ns = []
    for n in (2, 3, 4):
        om = _omega(n)
        ck(_partial_trace_reference(_outer(om), n, n) == _eye(n),
           f"the identity carrier must have full-support marginal I (n={n})")
        p3_ns.append(n)
    # SET-exact, not a count: `p3_rows == 3` passed for (2, 2, 2).
    ck(set(p3_ns) == {2, 3, 4}, f"P3 must run at n = 2, 3, 4, got {sorted(set(p3_ns))}")

    # THE VEC LAW CARRIES NO UNITARITY CONTENT, executed.  |bA>> = (I (x) A^T)|b>>
    # holds for ARBITRARY A, so the identity does not by itself distinguish gauge
    # from any right multiplication.  What makes U-and-only-U the gauge is that
    # it preserves the LOAD -- which is P2, and P2 is not discharged here.
    A_nonunitary: Mat = [[ONE, _g(2)], [ZERO, ONE]]
    ck(not _is_unitary(A_nonunitary), "the arbitrary-A witness must be non-unitary")
    b22 = _CARRIERS[(2, 2)]
    ck(_vec_columns(_mm(b22, A_nonunitary))
       == _mv(_kron(_eye(2), _transpose(A_nonunitary)), _vec_columns(b22)),
       "the vec law must hold for ARBITRARY A, which is why the gauge reading "
       "rests on load preservation (P2) and not on this identity")
    ck(_mm(_mm(b22, A_nonunitary), _dag(_mm(b22, A_nonunitary)))
       != _mm(b22, _dag(b22)),
       "and a non-unitary A changes the load, which is what unitarity buys")

    # CONTROL A: SWAP is not of the local form, the genuine effect is, and only
    # the genuine effect reproduces the sandwich.
    b = _CARRIERS[(2, 2)]
    v = _vec_columns(b)
    e = _herm_probe(2)
    SW = _zeros(4, 4)
    for i, j in ((0, 0), (1, 2), (2, 1), (3, 3)):
        SW[i][j] = ONE
    ck(not _is_local_form(SW, 2, 2), "SWAP must NOT be of the local form e (x) I")
    ck(_is_local_form(_kron(e, _eye(2)), 2, 2),
       "the genuine local effect must BE of the local form, or the test is inverted")
    ck(_inner(v, _mv(_kron(e, _eye(2)), v)) == _tr(_mm(_dag(b), _mm(e, b))),
       "the local effect must reproduce the sandwich")
    ck(_inner(v, _mv(SW, v)) != _tr(_mm(_dag(b), _mm(e, b))),
       "SWAP must not reproduce the sandwich, or locality is vacuous")

    # CONTROL B: conjugation is load-bearing, and only a COMPLEX carrier sees it.
    psi_i: Vec = [ONE, IMAG]
    ck(_inner(psi_i, psi_i) == _g(2),
       "a complex carrier's self-inner-product must be its squared norm; this "
       "fails the moment the inner product drops its conjugate")
    ck(_inner(psi_i, [ONE, _g(0, -1)]) == ZERO,
       "the complex carrier must be exactly orthogonal to its conjugate partner")

    # CONTROL C: a non-unitary right move changes the marginal.
    Nb: Mat = [[ONE, ONE], [ZERO, ONE]]
    ck(_mm(_mm(b, Nb), _dag(_mm(b, Nb))) != _mm(b, _dag(b)),
       "a non-unitary right move must change the marginal")

    return _result(
        'L_identity_carrier_vectorization',
        'P_math',
        ("The four carrier identities at RECTANGULAR shapes (2,2), (3,2), (2,3), "
         "(3,3), (4,3): the local marginal of |b>> is the load b b*, its norm is "
         "Tr(b* b), a LOCAL effect e (x) I contracts to the sandwich "
         "Tr(b* e b) = Tr(b b* e), and right-unitary freedom acts entirely on the "
         "reference leg, |bU>> = (I (x) U^T)|b>>.  The last identity IDENTIFIES "
         "the gauge group with the purification fibre -- but carries NO unitarity "
         "content on its own: it holds for ARBITRARY A, executed here with a "
         "non-unitary witness, so what selects the unitaries is load preservation, "
         "which is P2 and is NOT discharged.  P3 rides the carrier's "
         "marginal being I at n = 2, 3, 4 -- which does not discharge P3, since "
         "the carrier is K5, an open physical gate.  FOUR CONTROLS: the effect "
         "probe is asserted non-zero, non-scalar and Hermitian, without which the "
         "sandwich identity degenerates to 0 == 0; SWAP is computed not to be of "
         "the local form while the genuine effect is, and only the genuine effect "
         "reproduces the sandwich; conjugation is exercised on a COMPLEX carrier, "
         "since a real one cannot see it; and a non-unitary right move changes "
         "the marginal.  PRIOR ART DISCLOSED: check_T_same_type_reference_chosen_"
         "cp already computes |Omega><Omega| at n = 2 as the identity channel's "
         "Choi matrix.  This is an EXTENSION to general n and to rectangular "
         "carriers, not a first sighting."),
        {
            'shapes_tested': [list(s) for s in _SHAPES],
            'shape_rows_computed': rows,
            'p3_marginal_ns': sorted(set(p3_ns)),
            'swap_is_local_form': _is_local_form(SW, 2, 2),
            'genuine_effect_is_local_form': _is_local_form(_kron(e, _eye(2)), 2, 2),
            'effect_probe_is_scalar': _is_scalar(_herm_probe(3), 3),
            'complex_self_inner': [str(_inner(psi_i, psi_i)[0]),
                                   str(_inner(psi_i, psi_i)[1])],
        },
        fails,
        3,
        (),
        (),
        ("the effect probe is non-zero, non-scalar and genuinely complex",
         "SWAP is not of the local form and fails the sandwich identity",
         "conjugation is exercised on a complex carrier",
         "a non-unitary right move changes the marginal",),
        ('T_same_type_reference_chosen_cp', 'T_presentation_gauge_forces_trace'),
        fail_count=tally[0],
    )


_CHECKS = {
    'L_purification_orbit_fibre': check_L_purification_orbit_fibre,
    'L_identity_carrier_vectorization': check_L_identity_carrier_vectorization,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    """Recompute `passed`, and CROSS-ASSERT two independent failure records.

    A 2026-07-28 foreign audit collapsed a sibling battery from 40/40 to 3/40 by
    replacing `'passed': not fails` with a literal.  A second audit then defeated
    the repair one level down, by emptying `fail_reasons` at source while the
    recompute stayed intact.  So each check now carries `fail_count`, incremented
    by the assertion helper on a counter that is NOT the list; the two are
    cross-asserted here.  Tampering with either alone is caught."""
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
            for f in r['fail_reasons']:
                print('  -', f)
    sys.exit(1 if bad else 0)
