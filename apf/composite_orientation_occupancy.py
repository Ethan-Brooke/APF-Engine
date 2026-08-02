"""THE COMPOSITE ORIENTATION COEFFICIENT -- what the real theory does with it.

v24.3.464.  Three checks, tier 3, all [P_math], NON-EXPORTING, ppc=false,
no [P] moved.

------------------------------------------------------------------------------
WHAT THIS MODULE COMPUTES
------------------------------------------------------------------------------
v24.3.463 identified the one direction of a real bipartite state space that no
product of local observables can read: Lambda^2(R^n) (x) Lambda^2(R^m), which
at (2,2) is the single coordinate along J (x) J.  That result is about the
SPACE.  It says nothing about any state's coefficient along that coordinate.

This module computes three facts about the coefficient itself, at (2,2).

  (1) THE SELECTION VERDICT DOES NOT READ IT.  The composite-only subspace is
      the orthogonal complement of the local-product span inside Sym(R^4).  Its
      dimension is 1.  Three valid states are exhibited whose coefficients along
      it are +1/32, -1/32 and 0 -- three distinct values -- and the dimension of
      the complement is the same 1 in every case, because it is a property of
      the space and not of any state in it.  The integer whose sign the
      field-selection check reads at R is that dimension -- a quantity of the
      space, computed with no state in the argument list.

  (2) REACHABILITY OF THE COORDINATE IS FIELD-DEPENDENT.  Over R, J (x) J lies
      outside the span of {A (x) B : A, B symmetric}: computed here by exact
      rank, independently of the sibling.  Over C, with Y = iJ, the same matrix
      is -Y (x) Y with Y Hermitian and Y^2 = I -- a product of two local
      observables -- and the singlet has <Y (x) Y> = -1.  One matrix, two
      fields, opposite verdicts on whether a local measurement can see it.

  (3) THE ZERO SECTOR IS NONEMPTY, CONVEX AND ORTHOGONALLY CLOSED.  The set of
      valid real states with coefficient exactly zero contains the maximally
      mixed state and every product state tested; it is an intersection of the
      PSD cone with two hyperplanes, and the exhibited midpoints stay inside it;
      and under local orthogonal conjugation the coefficient is multiplied by
      det(O_A) det(O_B), because O^T J O = det(O) J on O(2).  Zero therefore
      stays zero at all 320 conjugations tested, and the coefficient behaves as
      a PSEUDOSCALAR: a reflection on one side reverses its sign.  The eight
      generators are a SAMPLE of O(2), not a spanning set of it, and the legs
      report finite counts rather than a universal.

------------------------------------------------------------------------------
THE READING, AND IT IS A READING
------------------------------------------------------------------------------
Facts (1)-(3) are arithmetic.  What follows is how we read them, and it is
recorded here rather than in any leg, because no leg computes it.

Nothing in the three computations forces a physical composite to carry a
non-zero coefficient.  Fact (3) exhibits a nonempty sector where it is zero and
stays zero; fact (1) shows the framework's own exclusion of R never consults it;
fact (2) shows the question cannot even be posed field-neutrally, since the
coordinate is invisible in one field and an ordinary product observable in the
other.  Asked inside R the coefficient may be zero forever with nothing
inconsistent; asked inside C it is populated by any entangled state, but the
field one wanted to derive has been assumed.

On our reading that places the occupancy question in the QAC genre --
per-interface, read off the world, not derived -- alongside every other
occupancy question this corpus has posed.  `core.py` states the general posture:
A1 admits both the occupied and the unoccupied world and is silent on which.
`check_T_contention_law_granularity_occupancy_fork` reached the same
classification for a different structure and declined to adopt the charge.

THE READING IS NOT A LEG AND MUST NOT BE CITED AS A THEOREM.  This module does
not prove that occupancy is underivable.  It computes that the three named
routes do not deliver it.

------------------------------------------------------------------------------
GRADE, PREMISES, DEPENDENCIES
------------------------------------------------------------------------------
All three checks are [P_math].  NO REGIME PREMISE IS CONSUMED ANYWHERE.

  THE [P_regime] HALF IS NOT TAKEN.  check_T_field_selection_complex is graded
  [P_regime + P_math].  Its [P_regime] half is the step from a positive defect
  to INADMISSIBILITY, which rests on Composite-Continuation Tomography being
  the selected regime.  Nothing here consumes it, and nothing here may be cited
  for an inadmissibility verdict.

  MODELLING DEFINITION -- named first, because it is where the physics enters:
  LOCAL_PRODUCT_OBSERVABLE_MODEL -- "what a pair of local measurements can read"
  is modelled as the real span of {A (x) B : A in Sym(R^n), B in Sym(R^m)}.
  This is the standard local-tomography span and it is a DEFINITION OF THE
  MODEL, not a theorem proved here.  It is the same modelling choice
  v24.3.463 makes, adopted deliberately so the two modules are comparable.

  LOCAL_ORTHOGONAL_CONJUGATION -- "a local transformation" is modelled in
  check 3 as rho |-> (O_A (x) O_B) rho (O_A (x) O_B)^T with O_A, O_B in O(2).
  This is NARROWER than "every local operation".  Local channels, local
  measurements and local post-selection are NOT covered, and no leg claims
  they are.

  PSD_CONE_CONVEXITY -- the PSD matrices form a convex cone.  Used to close
  the convexity leg from exhibited endpoints.

  NAMED STANDARD IMPORT:
    O2_PSEUDOSCALAR -- for O in O(2), O^T J O = det(O) J.  Elementary; it is
    re-derived here on eight sampled elements rather than cited.

DEPENDENCIES.  The arithmetic of check_T_field_selection_complex (the functions
K_dim_real and composite_defect) at ONE point, (2,2), as a cross-check that the
dimension computed here geometrically agrees with the integer the bank computes
combinatorially.  The graded check is never called.

------------------------------------------------------------------------------
KNOWN LIMITS
------------------------------------------------------------------------------
Everything below is a weakness of this module, stated as one.

  SHAPE, AND IT IS STRUCTURAL RATHER THAN UNTESTED.  Every computation is at
  (2,2), where the composite-only complement is ONE-dimensional so that "the
  coefficient" is a single number.  The complement has dimension 3 at (2,3) and
  9 at (3,3), where there is no scalar for a det-times-det law to act on, so
  the pseudoscalar framing does not merely lack a proof off (2,2) -- it does
  not apply there.  The identity O^T J O = det(O) J is a two-dimensional fact
  and fails at 3x3.

  THE ZERO SECTOR IS NOT CHARACTERIZED.  Check 3 exhibits members and closes
  convexity from exhibited endpoints plus the cone property.  It does not
  compute the sector's dimension, its extreme points, or whether it is closed
  under any operation wider than local orthogonal conjugation.

  THE NORMALIZATION DIFFERS FROM THE SIBLING'S AND BOTH ARE CORRECT.  The
  coefficient here is <rho, J (x) J> / <J (x) J, J (x) J>, so the sibling's
  witness pair reads +-1/32.  composite_only_direction.py reports the SAME two
  states at +-1/8, using the raw pairing.  <J (x) J, J (x) J> = 4 is the whole
  of the difference, and any comparison across the two modules must divide.

  THE COMPLEX SIDE IS ONE WITNESS.  Fact (2)'s complex half exhibits Y = iJ and
  the singlet.  It does not survey the complex product span or characterize
  which complex states have non-zero <Y (x) Y>.

  THE SIGN OF J IS NOT PINNED AGAINST A COORDINATED FLIP.  Flipping J to -J
  ALONE is caught, at C/Y_is_i_times_J, because Y_C is a frozen literal.
  Flipping J to -J AND Y to -Y together escapes every leg.  That is not a gap
  in the legs: the object under study is the tensor SQUARE J (x) J, and
  (-J) (x) (-J) = J (x) J, as does (-Y) (x) (-Y) = Y (x) Y.  The factor's sign
  is not an observable of the square.  Nothing here fixes an orientation
  convention on J itself and nothing here may be cited for one.

  THE CONJUGATION ORDER IS NOT PINNED, AND CANNOT BE HERE.  A mutation
  replacing O^T J O by O J O^T escapes every leg.  That is not a gap in the
  legs: for any 2x2 M, both M^T J M and M J M^T equal det(M) J, since that
  identity is what det means in two dimensions.  The module therefore fixes no
  conjugation-order convention and must not be cited as evidence for one.

  THE QUANTIFIER CANNOT SEPARATE 1 FROM True.  all_of compares against
  [True] * n and Python has 1 == True, so an integer 1 in the verdict stream
  reads as a pass.  Truthy non-bools that are not numerically equal to True --
  a string, a list -- are refused, and that is what the leg states.  The
  bool-exactness that does hold everywhere is in _leg, which is where every
  recorded verdict passes.

  VACUITY AT A QUANTIFIER SITE.  Bare `all(...)` is avoided in favour of
  all_of(n, ...), which takes the size of the quantified sequence at the call
  site.  A two-site edit that empties the sequence and moves n to 0 together
  still passes; that limit is inherited from the sibling and is not closed here.
"""

from __future__ import annotations

import hashlib
from fractions import Fraction as F
from typing import Dict, FrozenSet, List, Sequence, Tuple

Mat = Tuple[Tuple[F, ...], ...]
# A complex rational is an ordered pair (re, im) of Fractions.
CNum = Tuple[F, F]
CMat = Tuple[Tuple[CNum, ...], ...]

MODULE_TIER = 3
PHYSICAL_PREMISES_CERTIFIED = False
EXPORTS: Tuple[str, ...] = ()
BANK_MODIFIED = False


# ==========================================================================
# Exact rational linear algebra over R.  Fractions only; no floats anywhere.
# ==========================================================================


def mat(rows: Sequence[Sequence[object]]) -> Mat:
    return tuple(tuple(F(x) for x in r) for r in rows)


def eye(n: int) -> Mat:
    return tuple(tuple(F(1) if i == j else F(0) for j in range(n))
                 for i in range(n))


def add(a: Mat, b: Mat) -> Mat:
    return tuple(tuple(x + y for x, y in zip(ra, rb)) for ra, rb in zip(a, b))


def sub(a: Mat, b: Mat) -> Mat:
    return tuple(tuple(x - y for x, y in zip(ra, rb)) for ra, rb in zip(a, b))


def scale(c, a: Mat) -> Mat:
    c = F(c)
    return tuple(tuple(c * x for x in r) for r in a)


def mm(a: Mat, b: Mat) -> Mat:
    n, k, m = len(a), len(b), len(b[0])
    return tuple(tuple(sum((a[i][t] * b[t][j] for t in range(k)), F(0))
                       for j in range(m)) for i in range(n))


def transpose(a: Mat) -> Mat:
    return tuple(tuple(a[i][j] for i in range(len(a)))
                 for j in range(len(a[0])))


def trace(a: Mat) -> F:
    return sum((a[i][i] for i in range(len(a))), F(0))


def kron(a: Mat, b: Mat) -> Mat:
    na, ma, nb, mb = len(a), len(a[0]), len(b), len(b[0])
    return tuple(
        tuple(a[i // nb][j // mb] * b[i % nb][j % mb] for j in range(ma * mb))
        for i in range(na * nb))


def hs(a: Mat, b: Mat) -> F:
    """Hilbert-Schmidt pairing <a, b> = sum_ij a_ij b_ij = Tr(a^T b)."""
    return sum((x * y for ra, rb in zip(a, b) for x, y in zip(ra, rb)), F(0))


def flat(a: Mat) -> List[F]:
    return [x for r in a for x in r]


def is_symmetric(a: Mat) -> bool:
    n = len(a)
    return all_of(n * n, (a[i][j] == a[j][i]
                          for i in range(n) for j in range(n)))


def rank(vectors: Sequence[Sequence[F]]) -> int:
    """Exact rank by fraction-free-enough Gaussian elimination."""
    rows = [list(v) for v in vectors]
    if not rows:
        return 0
    ncols = len(rows[0])
    r = 0
    for c in range(ncols):
        piv = None
        for i in range(r, len(rows)):
            if rows[i][c] != 0:
                piv = i
                break
        if piv is None:
            continue
        rows[r], rows[piv] = rows[piv], rows[r]
        pv = rows[r][c]
        rows[r] = [x / pv for x in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c] != 0:
                f = rows[i][c]
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[r])]
        r += 1
        if r == len(rows):
            break
    return r


def mat_rank(ms: Sequence[Mat]) -> int:
    return rank([flat(m) for m in ms])


def in_span(v: Mat, basis: Sequence[Mat]) -> bool:
    """True iff v lies in the real span of `basis`.  Rank test, exact."""
    base = mat_rank(basis)
    return mat_rank(list(basis) + [v]) == base


def principal_minor(a: Mat, idx: Sequence[int]) -> F:
    sub_m = mat([[a[i][j] for j in idx] for i in idx])
    return det(sub_m)


def det(m: Mat) -> F:
    """Exact determinant by elimination with pivoting."""
    n = len(m)
    rows = [list(r) for r in m]
    sign = F(1)
    d = F(1)
    for c in range(n):
        piv = None
        for i in range(c, n):
            if rows[i][c] != 0:
                piv = i
                break
        if piv is None:
            return F(0)
        if piv != c:
            rows[c], rows[piv] = rows[piv], rows[c]
            sign = -sign
        d *= rows[c][c]
        pv = rows[c][c]
        for i in range(c + 1, n):
            if rows[i][c] != 0:
                f = rows[i][c] / pv
                rows[i] = [x - f * y for x, y in zip(rows[i], rows[c])]
    return sign * d


def is_psd(a: Mat) -> bool:
    """A symmetric matrix is PSD iff EVERY principal minor is >= 0.

    Leading principal minors are NOT sufficient for the semidefinite case --
    diag(0, -1) has both leading minors 0 and would pass that weaker test.
    All 2^n - 1 principal minors are taken here.
    """
    n = len(a)
    if not is_symmetric(a):
        return False
    for mask in range(1, 1 << n):
        idx = [i for i in range(n) if (mask >> i) & 1]
        if principal_minor(a, idx) < 0:
            return False
    return True


# ==========================================================================
# Exact complex-rational arithmetic.  Pairs of Fractions; no floats.
# ==========================================================================


def c(re, im=0) -> CNum:
    return (F(re), F(im))


def cadd(x: CNum, y: CNum) -> CNum:
    return (x[0] + y[0], x[1] + y[1])


def cmul(x: CNum, y: CNum) -> CNum:
    return (x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0])


def cconj(x: CNum) -> CNum:
    return (x[0], -x[1])


def cmat(rows: Sequence[Sequence[CNum]]) -> CMat:
    return tuple(tuple(r) for r in rows)


def real_to_c(a: Mat) -> CMat:
    return tuple(tuple((x, F(0)) for x in r) for r in a)


def cmm(a: CMat, b: CMat) -> CMat:
    n, k, m = len(a), len(b), len(b[0])
    out = []
    for i in range(n):
        row = []
        for j in range(m):
            acc = c(0)
            for t in range(k):
                acc = cadd(acc, cmul(a[i][t], b[t][j]))
            row.append(acc)
        out.append(tuple(row))
    return tuple(out)


def cdagger(a: CMat) -> CMat:
    return tuple(tuple(cconj(a[i][j]) for i in range(len(a)))
                 for j in range(len(a[0])))


def ckron(a: CMat, b: CMat) -> CMat:
    na, ma, nb, mb = len(a), len(a[0]), len(b), len(b[0])
    return tuple(
        tuple(cmul(a[i // nb][j // mb], b[i % nb][j % mb])
              for j in range(ma * mb))
        for i in range(na * nb))


def cscale(z: CNum, a: CMat) -> CMat:
    return tuple(tuple(cmul(z, x) for x in r) for r in a)


def ctrace(a: CMat) -> CNum:
    acc = c(0)
    for i in range(len(a)):
        acc = cadd(acc, a[i][i])
    return acc


def c_is_hermitian(a: CMat) -> bool:
    n = len(a)
    d = cdagger(a)
    return all_of(n * n, (a[i][j] == d[i][j]
                          for i in range(n) for j in range(n)))


def c_equal(a: CMat, b: CMat) -> bool:
    n, m = len(a), len(a[0])
    return all_of(n * m, (a[i][j] == b[i][j]
                          for i in range(n) for j in range(m)))


# ==========================================================================
# The objects
# ==========================================================================

J = mat([[0, -1], [1, 0]])                     # the symplectic form on R^2
I2 = eye(2)
I4 = eye(4)
X = mat([[0, 1], [1, 0]])
Z = mat([[1, 0], [0, -1]])
JJ = kron(J, J)                                # the composite-only direction

# Y = iJ, Hermitian, Y^2 = I.
Y_C: CMat = cmat([[c(0), c(0, -1)], [c(0, 1), c(0)]])


def sym_basis(n: int) -> List[Mat]:
    """A spanning set of Sym(R^n): E_ii and E_ij + E_ji for i < j."""
    out = []
    for i in range(n):
        rows = [[F(0)] * n for _ in range(n)]
        rows[i][i] = F(1)
        out.append(mat(rows))
    for i in range(n):
        for j in range(i + 1, n):
            rows = [[F(0)] * n for _ in range(n)]
            rows[i][j] = F(1)
            rows[j][i] = F(1)
            out.append(mat(rows))
    return out


def product_span_basis(n: int, m: int) -> List[Mat]:
    """{A (x) B : A in sym_basis(n), B in sym_basis(m)} -- the model of what a
    pair of local measurements can read.  LOCAL_PRODUCT_OBSERVABLE_MODEL."""
    return [kron(a, b) for a in sym_basis(n) for b in sym_basis(m)]


def o2_generators() -> List[Mat]:
    """A spanning set of O(2) sufficient to exercise both components.

    Four rotations (det +1) and four reflections (det -1), all with rational
    entries so the arithmetic stays exact.  The rotations use the Pythagorean
    triple (3, 4, 5) so that a non-trivial rational rotation is present and
    the identity is not carrying the leg alone.  This is a SAMPLE of O(2), not
    a spanning set of it; every leg drawn from it reports a finite count.
    """
    a, b = F(3, 5), F(4, 5)
    rots = [
        eye(2),
        mat([[0, -1], [1, 0]]),
        mat([[-1, 0], [0, -1]]),
        mat([[a, -b], [b, a]]),
    ]
    refls = [
        mat([[1, 0], [0, -1]]),
        mat([[0, 1], [1, 0]]),
        mat([[-1, 0], [0, 1]]),
        mat([[a, b], [b, -a]]),
    ]
    return rots + refls


def partial_trace_b(rho: Mat) -> Mat:
    """Trace out the SECOND factor of a 4x4 matrix on R^2 (x) R^2."""
    return mat([[rho[2 * i][2 * j] + rho[2 * i + 1][2 * j + 1]
                 for j in range(2)] for i in range(2)])


def partial_trace_a(rho: Mat) -> Mat:
    """Trace out the FIRST factor of a 4x4 matrix on R^2 (x) R^2."""
    return mat([[rho[i][j] + rho[i + 2][j + 2]
                 for j in range(2)] for i in range(2)])


def orientation_coefficient(rho: Mat) -> F:
    """The state's coordinate along the composite-only direction.

    <rho, J (x) J> / <J (x) J, J (x) J>.  Normalized so that the coefficient
    of JJ itself is 1.
    """
    return hs(rho, JJ) / hs(JJ, JJ)


def witness(t) -> Mat:
    """rho(t) = I/4 + (X(x)X + Z(x)Z)/16 + t * (J(x)J).

    The sibling's witness family.  t = +1/32, -1/32 and 0 are the three
    states used here.
    """
    t = F(t)
    base = add(scale(F(1, 4), I4),
               scale(F(1, 16), add(kron(X, X), kron(Z, Z))))
    return add(base, scale(t, JJ))


# ==========================================================================
# Leg plumbing.  Identical in shape to the sibling's, deliberately.
# ==========================================================================


def all_of(n: int, verdicts) -> bool:
    """`all(...)` with the SIZE OF WHAT WAS QUANTIFIED written into the call.

    True iff `verdicts` yields EXACTLY n items and every one is literally True.
    A bare `all(P(x) for x in [])` is True with nothing evaluated and the leg
    inventory cannot tell the difference; the count is therefore taken from the
    sequence the quantifier actually consumed.
    """
    vs = list(verdicts)
    return len(vs) == n and vs == [True] * n


def _leg_digest(labels) -> str:
    return hashlib.sha256(
        '\n'.join(sorted(labels)).encode('utf-8')).hexdigest()


def _leg(legs: Dict[str, bool], label: str, verdict) -> None:
    """Record one leg.  Raises on a duplicate label and on a non-bool verdict.

    Coercion is refused rather than performed: a bare generator expression, a
    container, a callable or a Fraction all read TRUTHY under bool(), and what
    would be recorded is then a fact about the object's type rather than the
    value of a predicate.
    """
    if label in legs:
        raise AssertionError(
            f"duplicate leg label {label!r} -- two writes to one key, so one "
            f"of the two predicate values would not be in the record")
    if verdict is not True and verdict is not False:
        raise AssertionError(
            f"leg {label!r} was handed a {type(verdict).__name__}, not a bool")
    legs[label] = verdict


def _enforce_leg_inventory(record: dict) -> None:
    """The four inventory quantities, computed on the record being returned.

    IT IS HERE AND NOT ONLY IN run_all() because verify_all enumerates a
    module's `check_`-prefixed attributes and calls each DIRECTLY; a module's
    own run_all() is never invoked by it.  A siting in run_all() is dead on the
    bank path -- the defect v24.3.450 is on record for.

    RAISE, NOT `passed = False`.  A false predicate is a claim of this module
    turning out untrue: the record is intact, the failing labels are in it, and
    a reader can act on it -- returned as passed=False, a FLAG.  A broken
    inventory means the record no longer describes what ran, so no field of it
    should be read at all -- raised, a FAIL.
    """
    name = record['name']
    if name not in EXPECTED_LEGS:
        raise AssertionError(f"{name}: no frozen leg inventory for this check")
    if name not in EXPECTED_LEG_COUNTS or name not in EXPECTED_LEG_DIGEST:
        raise AssertionError(f"{name}: no frozen leg-count / leg-digest literal")
    frozen: FrozenSet[str] = EXPECTED_LEGS[name]
    labels = list(record['leg_labels'])
    if set(labels) != set(frozen):
        raise AssertionError(
            f"{name}: the evaluated leg inventory does not match the frozen "
            f"literal -- missing {sorted(set(frozen) - set(labels))[:8]}, "
            f"unexpected {sorted(set(labels) - set(frozen))[:8]}")
    if not (len(labels) == record['legs_evaluated']
            == record['legs_expected'] == len(frozen)
            == EXPECTED_LEG_COUNTS[name]):
        raise AssertionError(
            f"{name}: leg counts disagree with the frozen literal "
            f"({len(labels)} labels, {record['legs_evaluated']} evaluated, "
            f"{record['legs_expected']} expected, {len(frozen)} frozen set, "
            f"{EXPECTED_LEG_COUNTS[name]} frozen count)")
    for source, ls in (('evaluated', labels), ('expected', sorted(frozen))):
        got = _leg_digest(ls)
        if got != EXPECTED_LEG_DIGEST[name]:
            raise AssertionError(
                f"{name}: the {source} leg-label digest {got[:16]} does not "
                f"match the frozen literal {EXPECTED_LEG_DIGEST[name][:16]}")
    rederived = (not record['fail_reasons']
                 and not record['leg_inventory_missing']
                 and not record['leg_inventory_unexpected'])
    if record['passed'] != rederived:
        raise AssertionError(
            f"{name}: the reported verdict {record['passed']} disagrees with "
            f"the verdict re-derived from the returned records {rederived}")


def _result(name, epistemic, key_result, evidence, legs, tier,
            dependencies, premises, negative_controls, cross_refs):
    """Build the result dict from the leg inventory.  No verdict is written
    down anywhere; `passed` is computed here and only here."""
    expected: FrozenSet[str] = EXPECTED_LEGS[name]
    seen = set(legs)
    missing = tuple(sorted(expected - seen))
    unexpected = tuple(sorted(seen - expected))
    fail_reasons = tuple(label for label, verdict in legs.items()
                         if not verdict)
    passed = (seen == expected) and all(legs.values())
    record = {
        'name': name,
        'epistemic': epistemic,
        'passed': passed,
        'tier': tier,
        'key_result': key_result,
        'summary': (('FAILED LEGS: ' + ', '.join(fail_reasons[:6]))
                    if fail_reasons else None),
        'evidence': evidence,
        'fail_reasons': list(fail_reasons),
        'leg_inventory_missing': list(missing),
        'leg_inventory_unexpected': list(unexpected),
        'legs_evaluated': len(legs),
        'legs_expected': len(expected),
        'leg_labels': sorted(legs),
        'dependencies': list(dependencies),
        'premises': list(premises),
        'negative_controls': list(negative_controls),
        'cross_refs': list(cross_refs),
        'physical_premises_certified': PHYSICAL_PREMISES_CERTIFIED,
        'exports': list(EXPORTS),
        'bank_modified': BANK_MODIFIED,
    }
    _enforce_leg_inventory(record)
    return record


# ==========================================================================
# CHECK 1 -- the selection verdict does not read the coefficient
# ==========================================================================


def check_L_composite_orientation_is_selection_invisible():
    """[P_math].  The integer whose sign the field-selection check reads
    at R is the DIMENSION of the composite-only subspace.  That dimension is a
    property of the space: three valid states with three distinct coefficients
    along the subspace, sharing both marginals, leave it unchanged."""
    _NAME = 'check_L_composite_orientation_is_selection_invisible'
    legs: Dict[str, bool] = {}
    ev: Dict[str, object] = {}

    def L(label: str, verdict) -> None:
        _leg(legs, label, verdict)

    epistemic = (
        "[P_math | structural premises: LOCAL_PRODUCT_OBSERVABLE_MODEL. "
        "Consumes only the arithmetic of check_T_field_selection_complex, at "
        "one shape, as a cross-check; the [P_regime] CCT half is not taken.]")

    # The size guard inside all_of is what stops an emptied comprehension
    # from reading True.  Nothing pinned the guard itself, so a one-line
    # edit disabled it for every leg in the module.  Exercised directly.
    L('Q/the_quantifier_refuses_a_short_sequence',
      all_of(2, (True,)) is False and all_of(1, (True,)) is True)
    L('Q/the_quantifier_refuses_an_emptied_sequence',
      all_of(3, iter(())) is False)
    L('Q/the_quantifier_refuses_a_truthy_non_bool',
      all_of(1, ('x',)) is False and all_of(1, ([1],)) is False)

    # ---- the space -------------------------------------------------------
    prod = product_span_basis(2, 2)
    sym4 = sym_basis(4)
    dim_sym4 = mat_rank(sym4)
    dim_prod = mat_rank(prod)
    L('S/sym4_has_dimension_10', dim_sym4 == 10)
    L('S/product_span_has_dimension_9', dim_prod == 9)
    L('S/complement_has_dimension_1', dim_sym4 - dim_prod == 1)
    L('S/product_span_is_inside_sym4',
      all_of(9, (in_span(p, sym4) for p in prod)))
    ev['dim_sym4'] = dim_sym4
    ev['dim_product_span'] = dim_prod

    # ---- the direction spans the complement ------------------------------
    L('D/JJ_is_symmetric', is_symmetric(JJ))
    L('D/JJ_is_not_in_the_product_span', not in_span(JJ, prod))
    L('D/JJ_is_in_sym4', in_span(JJ, sym4))
    L('D/product_span_plus_JJ_spans_sym4',
      mat_rank(list(prod) + [JJ]) == dim_sym4)
    L('D/JJ_is_orthogonal_to_every_product_basis_element',
      all_of(9, (hs(p, JJ) == 0 for p in prod)))

    # ---- three valid states, three distinct coefficients ------------------
    ts = [F(1, 32), F(-1, 32), F(0)]
    states = [witness(t) for t in ts]
    coeffs = [orientation_coefficient(s) for s in states]
    L('W/three_states_are_symmetric',
      all_of(3, (is_symmetric(s) for s in states)))
    L('W/three_states_have_unit_trace',
      all_of(3, (trace(s) == 1 for s in states)))
    L('W/three_states_are_psd', all_of(3, (is_psd(s) for s in states)))
    # PSD CONTROL.  diag(0, -1) has BOTH leading principal minors equal to 0
    # and is not PSD.  A helper that tested only leading minors would accept
    # it; this leg is what makes the all-principal-minors form load-bearing.
    L('W/the_psd_test_rejects_a_matrix_that_passes_the_leading_minor_test',
      is_psd(mat([[0, 0], [0, -1]])) is False)
    L('W/the_psd_test_accepts_a_genuine_psd_matrix',
      is_psd(mat([[2, 1], [1, 2]])) is True)
    L('W/the_direction_has_coefficient_one_in_its_own_normalization',
      orientation_coefficient(JJ) == 1)
    L('W/three_coefficients_are_the_three_parameters',
      all_of(3, (co == t for co, t in zip(coeffs, ts))))
    L('W/three_coefficients_are_pairwise_distinct',
      len(set(coeffs)) == 3)
    L('W/the_zero_state_has_zero_coefficient', coeffs[2] == 0)
    L('W/the_two_signed_states_are_negatives_in_the_coefficient',
      coeffs[0] == -coeffs[1] and coeffs[0] != 0)
    ev['coefficients'] = [str(x) for x in coeffs]

    # ---- the states are locally indistinguishable ------------------------
    diff = sub(states[0], states[1])
    L('L/the_difference_is_a_multiple_of_JJ', is_scalar_multiple_ok(diff, JJ))
    L('L/every_product_observable_agrees_on_the_pair',
      all_of(9, (hs(p, diff) == 0 for p in prod)))
    L('L/the_pair_differs_as_matrices', diff != tuple(tuple(F(0)
                                                            for _ in range(4))
                                                      for _ in range(4)))

    # ---- what the three states share, and what they do not ----------------
    # The three agree on BOTH local marginals -- computed, not asserted -- and
    # they are told apart by the product span itself: adjoining a state with a
    # non-zero coefficient raises its rank, adjoining the t = 0 state does not.
    marg_a = [partial_trace_b(s) for s in states]
    marg_b = [partial_trace_a(s) for s in states]
    L('M/all_three_share_one_left_marginal',
      all_of(2, (m == marg_a[0] for m in marg_a[1:])))
    L('M/all_three_share_one_right_marginal',
      all_of(2, (m == marg_b[0] for m in marg_b[1:])))
    L('M/the_shared_marginals_are_the_maximally_mixed_qubit',
      marg_a[0] == scale(F(1, 2), I2) and marg_b[0] == scale(F(1, 2), I2))
    # ORIENTATION CONTROL.  Every state above has maximally mixed marginals on
    # both sides, so a swap of the two partial-trace helpers would be invisible
    # to the three legs above.  This asymmetric state fixes the orientation:
    # |0><0| (x) I/2 has left marginal |0><0| and right marginal I/2.
    p0 = mat([[1, 0], [0, 0]])
    asym = kron(p0, scale(F(1, 2), I2))
    L('M/the_orientation_control_is_a_valid_state',
      is_psd(asym) and trace(asym) == 1)
    L('M/the_orientation_control_has_distinct_marginals',
      partial_trace_b(asym) != partial_trace_a(asym))
    L('M/tracing_out_the_second_factor_returns_the_first',
      partial_trace_b(asym) == p0)
    L('M/tracing_out_the_first_factor_returns_the_second',
      partial_trace_a(asym) == scale(F(1, 2), I2))
    ranks = [mat_rank(list(prod) + [s]) for s in states]
    L('M/the_two_signed_states_leave_the_product_span',
      all_of(2, (r == 10 for r in ranks[:2])))
    L('M/the_zero_state_lies_inside_the_product_span', ranks[2] == 9)
    L('M/the_rank_test_separates_the_states_the_marginals_cannot',
      len(set(ranks)) == 2 and marg_a[0] == marg_a[1])
    ev['ranks_with_state_adjoined'] = ranks

    # ---- cross-check against the bank's own combinatorial integer ---------
    bank_delta, bank_ok = _bank_defect_at_2_2()
    L('B/the_bank_arithmetic_was_reachable', bank_ok)
    L('B/the_geometric_and_combinatorial_integers_agree',
      bank_delta == dim_sym4 - dim_prod)
    ev['bank_delta_R_2_2'] = bank_delta

    key_result = (
        f"Sym(R^4) has dimension {dim_sym4}; the local-product span has "
        f"dimension {dim_prod}; the composite-only complement is "
        f"{dim_sym4 - dim_prod}-dimensional and is spanned by J (x) J.  Three "
        f"valid states with coefficients {ev['coefficients']} along it leave "
        f"that dimension unchanged, and the bank's combinatorial "
        f"Delta_R(2,2) = {bank_delta} agrees with it.  The integer whose "
        f"sign the field-selection check reads at R is that dimension; the "
        f"three states are separated only by the rank test {ranks}, never by "
        f"their marginals.")

    return _result(
        _NAME, epistemic, key_result, ev, legs, MODULE_TIER,
        dependencies=('check_T_field_selection_complex (arithmetic only)',),
        premises=('LOCAL_PRODUCT_OBSERVABLE_MODEL',),
        negative_controls=(
            'JJ is exhibited OUTSIDE the product span, so the complement is '
            'not empty by construction',
            'the three coefficients are checked pairwise distinct, so the '
            'invariance leg is not quantified over one repeated state'),
        cross_refs=(
            'check_L_real_composite_only_direction_is_lambda_tensor_lambda',))


def is_scalar_multiple_ok(a: Mat, b: Mat) -> bool:
    """True iff a = lambda * b for some rational lambda, b non-zero."""
    fa, fb = flat(a), flat(b)
    nz = [i for i, x in enumerate(fb) if x != 0]
    if not nz:
        return False
    lam = fa[nz[0]] / fb[nz[0]]
    return all_of(len(fa), (x == lam * y for x, y in zip(fa, fb)))


def _bank_defect_at_2_2():
    """Delta_R(2,2) from the bank's own arithmetic, never the graded check.

    Returns (value, reachable).  If the import fails the value is recomputed
    from the same closed form locally and `reachable` is False, so the leg
    that reads it records the difference rather than silently substituting.
    """
    try:
        from apf.quantum_admissibility import K_dim_real, composite_defect
        return composite_defect(K_dim_real, 2, 2), True
    except Exception:
        # K_R(n) = n(n+1)/2; Delta_R(2,2) = K_R(4) - K_R(2)^2 = 10 - 9 = 1.
        def k(n):
            return n * (n + 1) // 2
        return k(4) - k(2) * k(2), False


# ==========================================================================
# CHECK 2 -- reachability of the coordinate is field-dependent
# ==========================================================================


def check_L_composite_orientation_reachability_is_field_dependent():
    """[P_math].  One matrix, two fields, opposite verdicts.  Over R, J (x) J
    lies outside the span of products of local symmetric observables.  Over C,
    with Y = iJ Hermitian and Y^2 = I, the same matrix is -Y (x) Y -- a product
    of two local observables -- and the singlet gives <Y (x) Y> = -1.  The
    question of whether a local measurement can see the coordinate has no
    field-independent answer."""
    _NAME = 'check_L_composite_orientation_reachability_is_field_dependent'
    legs: Dict[str, bool] = {}
    ev: Dict[str, object] = {}

    def L(label: str, verdict) -> None:
        _leg(legs, label, verdict)

    epistemic = (
        "[P_math | structural premises: LOCAL_PRODUCT_OBSERVABLE_MODEL. "
        "The complex half is ONE witness pair and does not survey the "
        "complex product span.]")

    L('Q/the_quantifier_refuses_a_short_sequence',
      all_of(2, (True,)) is False and all_of(1, (True,)) is True)
    L('Q/the_quantifier_refuses_an_emptied_sequence',
      all_of(3, iter(())) is False)

    # ---- the real vantage -------------------------------------------------
    prod = product_span_basis(2, 2)
    L('R/JJ_is_outside_the_real_product_span', not in_span(JJ, prod))
    L('R/every_real_local_pairing_with_JJ_vanishes',
      all_of(9, (hs(p, JJ) == 0 for p in prod)))
    # The structural reason, computed rather than asserted: Tr(A J) = 0 for
    # every symmetric A, because J is antisymmetric.
    sb2 = sym_basis(2)
    L('R/trace_of_symmetric_against_J_vanishes',
      all_of(3, (trace(mm(a, J)) == 0 for a in sb2)))
    L('R/J_is_antisymmetric', transpose(J) == scale(-1, J))
    # PAIRING CONTROL.  Every argument this module hands to hs() is symmetric,
    # and on symmetric arguments Tr(a^T b) and Tr(a b) agree -- so the pairing
    # convention is invisible to every other leg.  E_01 pins it: hs is 1 where
    # the untransposed trace is 0.
    e01 = mat([[0, 1], [0, 0]])
    L('R/the_pairing_is_the_transposed_trace_not_the_plain_trace',
      hs(e01, e01) == 1 and trace(mm(e01, e01)) == 0)
    L('R/the_two_pairings_agree_on_symmetric_arguments',
      all_of(9, (hs(a, b) == trace(mm(a, b)) for a in sb2 for b in sb2)))
    # The factorization identity hs(A (x) B, J (x) J) = Tr(A^T J) Tr(B^T J).
    # Tested on SYMMETRIC arguments, where both sides are 0 and the identity
    # cannot discriminate, AND on a set including NON-symmetric arguments,
    # where both sides are non-zero and it can.  The second set is what makes
    # the leg non-vacuous; the first is the case the module actually uses.
    gen2 = list(sb2) + [J, mat([[0, 1], [0, 0]]), mat([[1, 2], [3, 4]])]
    L('R/the_product_trace_factorizes_on_symmetric_arguments',
      all_of(9, (hs(kron(a, b), JJ) == trace(mm(a, transpose(J)))
                 * trace(mm(b, transpose(J)))
                 for a in sb2 for b in sb2)))
    L('R/the_product_trace_factorizes_on_thirty_six_general_arguments',
      all_of(36, (hs(kron(a, b), JJ) == trace(mm(a, transpose(J)))
                  * trace(mm(b, transpose(J)))
                  for a in gen2 for b in gen2)))
    L('R/the_factorization_is_non_zero_somewhere',
      hs(kron(J, J), JJ) != 0
      and trace(mm(J, transpose(J))) != 0)

    # ---- the complex vantage ----------------------------------------------
    L('C/Y_is_hermitian', c_is_hermitian(Y_C))
    L('C/Y_squares_to_the_identity',
      c_equal(cmm(Y_C, Y_C), real_to_c(I2)))
    L('C/Y_is_i_times_J',
      c_equal(Y_C, cscale(c(0, 1), real_to_c(J))))
    minus_YY = cscale(c(-1), ckron(Y_C, Y_C))
    L('C/minus_Y_tensor_Y_equals_J_tensor_J',
      c_equal(minus_YY, real_to_c(JJ)))
    L('C/Y_tensor_Y_is_hermitian', c_is_hermitian(ckron(Y_C, Y_C)))
    L('C/J_tensor_J_is_hermitian_over_C', c_is_hermitian(real_to_c(JJ)))

    # ---- the singlet occupies it ------------------------------------------
    singlet = _singlet_density()
    L('C/singlet_is_hermitian', c_is_hermitian(singlet))
    L('C/singlet_has_unit_trace', ctrace(singlet) == c(1))
    L('C/singlet_is_idempotent', c_equal(cmm(singlet, singlet), singlet))
    exp_YY = ctrace(cmm(singlet, ckron(Y_C, Y_C)))
    L('C/singlet_expectation_of_Y_tensor_Y_is_minus_one', exp_YY == c(-1))
    L('C/singlet_expectation_is_real', exp_YY[1] == 0)
    L('C/singlet_expectation_is_non_zero', exp_YY != c(0))
    ev['singlet_expectation_YY'] = f"{exp_YY[0]} + {exp_YY[1]}i"

    # ---- a product state does not ----------------------------------------
    prod_state = _product_density()
    exp_prod = ctrace(cmm(prod_state, ckron(Y_C, Y_C)))
    L('C/product_state_is_hermitian', c_is_hermitian(prod_state))
    L('C/product_state_has_unit_trace', ctrace(prod_state) == c(1))
    L('C/product_state_expectation_of_Y_tensor_Y_is_zero', exp_prod == c(0))

    # ---- the two membership verdicts, each computed the same way ----------
    # Both sides are decided by SPAN MEMBERSHIP, not by exhibiting a witness on
    # one side and testing membership on the other.  The complex product span
    # is built from the Hermitian basis {I, X, Y, Z} on each factor and the
    # membership test is an exact real rank over the 32 real coordinates of a
    # 4x4 complex matrix.
    cprod = complex_product_span_basis()
    L('F/the_complex_product_span_has_sixteen_elements', len(cprod) == 16)
    L('F/the_complex_product_span_is_sixteen_dimensional_over_R',
      c_mat_rank(cprod) == 16)
    L('F/every_complex_product_basis_element_is_hermitian',
      all_of(16, (c_is_hermitian(p) for p in cprod)))
    real_reachable = in_span(JJ, prod)
    complex_reachable = c_in_span(real_to_c(JJ), cprod)
    L('F/JJ_is_in_the_complex_product_span', complex_reachable is True)
    L('F/the_two_membership_verdicts_differ_on_one_matrix',
      real_reachable != complex_reachable)
    # NEGATIVE CONTROL on the complex test: a NON-Hermitian matrix must fail
    # membership, so the complex span test is not accepting everything.
    non_herm = cmat([[c(0), c(1)], [c(0), c(0)]])
    L('F/the_complex_span_test_rejects_a_non_hermitian_matrix',
      c_in_span(ckron(non_herm, real_to_c(I2)), cprod) is False)
    ev['real_reachable'] = real_reachable
    ev['complex_reachable'] = complex_reachable

    key_result = (
        "J (x) J lies outside the real local-product span and every real "
        "local pairing with it vanishes, because Tr(A J) = 0 for symmetric A. "
        "Over C the same matrix is -Y (x) Y with Y = iJ Hermitian and "
        "Y^2 = I, a product of two local observables, and the singlet returns "
        f"<Y (x) Y> = {ev['singlet_expectation_YY']} while a product state "
        "returns 0.  The membership verdict for one matrix differs between "
        "the two spans.")

    return _result(
        _NAME, epistemic, key_result, ev, legs, MODULE_TIER,
        dependencies=(),
        premises=('LOCAL_PRODUCT_OBSERVABLE_MODEL',),
        negative_controls=(
            'a product state is exhibited with expectation exactly 0, so the '
            'singlet leg is not passing on a functional that is non-zero on '
            'everything',
            'the expectation is checked to have zero imaginary part, so a '
            'complex value is not being compared against a real literal'),
        cross_refs=(
            'check_L_bipartite_chsh_blind_to_composite_only_direction',))


def complex_product_span_basis() -> List[CMat]:
    """{A (x) B} with A, B ranging over the Hermitian basis {I, X, Y, Z}."""
    herm = [real_to_c(I2), real_to_c(X), Y_C, real_to_c(Z)]
    return [ckron(a, b) for a in herm for b in herm]


def c_flat(a: CMat) -> List[F]:
    """A complex matrix as its real coordinate vector: re and im interleaved."""
    return [x for r in a for z in r for x in (z[0], z[1])]


def c_mat_rank(ms: Sequence[CMat]) -> int:
    return rank([c_flat(m) for m in ms])


def c_in_span(v: CMat, basis: Sequence[CMat]) -> bool:
    """True iff v is in the REAL span of `basis`.  The Hermitian matrices form
    a real vector space, so a real rank over the 2 n^2 coordinates is the right
    test; a complex span would be the wrong question here."""
    base = c_mat_rank(basis)
    return c_mat_rank(list(basis) + [v]) == base


def _singlet_density() -> CMat:
    """|Psi^-><Psi^-| on C^2 (x) C^2, exact, in the basis 00, 01, 10, 11."""
    h = F(1, 2)
    zc = c(0)
    return cmat([
        [zc, zc, zc, zc],
        [zc, c(h), c(-h), zc],
        [zc, c(-h), c(h), zc],
        [zc, zc, zc, zc],
    ])


def _product_density() -> CMat:
    """|0><0| (x) |0><0|, exact."""
    p0 = cmat([[c(1), c(0)], [c(0), c(0)]])
    return ckron(p0, p0)


# ==========================================================================
# CHECK 3 -- the zero sector is nonempty, convex and orthogonally closed
# ==========================================================================


def check_L_composite_orientation_zero_sector_is_closed():
    """[P_math].  The valid real states whose coefficient along J (x) J is
    exactly zero form a nonempty set, closed under convex combination, and
    carried into itself by every local orthogonal conjugation -- because
    O^T J O = det(O) J on O(2), so the coefficient is a pseudoscalar and is
    multiplied by det(O_A) det(O_B).  Zero stays zero."""
    _NAME = 'check_L_composite_orientation_zero_sector_is_closed'
    legs: Dict[str, bool] = {}
    ev: Dict[str, object] = {}

    def L(label: str, verdict) -> None:
        _leg(legs, label, verdict)

    epistemic = (
        "[P_math | structural premises: LOCAL_ORTHOGONAL_CONJUGATION "
        "(NARROWER than 'every local operation' -- local channels, "
        "measurements and post-selection are NOT covered) and "
        "PSD_CONE_CONVEXITY. Named import: O2_PSEUDOSCALAR, re-derived here.]")

    L('Q/the_quantifier_refuses_a_short_sequence',
      all_of(2, (True,)) is False and all_of(1, (True,)) is True)
    L('Q/the_quantifier_refuses_an_emptied_sequence',
      all_of(3, iter(())) is False)

    # ---- nonempty ---------------------------------------------------------
    members = [
        scale(F(1, 4), I4),                              # maximally mixed
        witness(0),                                      # the t = 0 witness
        kron(mat([[1, 0], [0, 0]]), mat([[1, 0], [0, 0]])),
        kron(mat([[F(1, 2), 0], [0, F(1, 2)]]),
             mat([[1, 0], [0, 0]])),
        scale(F(1, 4), add(I4, kron(Z, Z))),
    ]
    L('N/five_members_are_symmetric',
      all_of(5, (is_symmetric(s) for s in members)))
    L('N/five_members_have_unit_trace',
      all_of(5, (trace(s) == 1 for s in members)))
    L('N/five_members_are_psd', all_of(5, (is_psd(s) for s in members)))
    L('N/five_members_have_zero_coefficient',
      all_of(5, (orientation_coefficient(s) == 0 for s in members)))
    L('N/five_members_were_formed', len(members) == 5)
    # DISTINCTNESS.  Without it, five copies of one state pass every leg below:
    # the midpoints are that state, and I/4 is invariant under every orthogonal
    # conjugation, so the closure legs would be trivially green.
    L('N/five_members_are_pairwise_distinct', len(set(members)) == 5)

    # ---- the coefficient is a genuine functional, not identically zero ----
    outside = [witness(F(1, 32)), witness(F(-1, 32))]
    L('N/two_exhibited_states_lie_OUTSIDE_the_sector',
      all_of(2, (orientation_coefficient(s) != 0 for s in outside)))
    L('N/the_coefficient_is_not_identically_zero_on_valid_states',
      all_of(2, (is_psd(s) and trace(s) == 1 for s in outside)))

    # ---- convex -----------------------------------------------------------
    mids = []
    for i in range(len(members)):
        for j in range(i + 1, len(members)):
            mids.append(add(scale(F(1, 2), members[i]),
                            scale(F(1, 2), members[j])))
    L('V/ten_midpoints_were_formed', len(mids) == 10)
    L('V/ten_midpoints_are_psd', all_of(10, (is_psd(m) for m in mids)))
    L('V/ten_midpoints_have_unit_trace',
      all_of(10, (trace(m) == 1 for m in mids)))
    L('V/ten_midpoints_have_zero_coefficient',
      all_of(10, (orientation_coefficient(m) == 0 for m in mids)))
    # A non-halfway combination too, so the leg is not testing t = 1/2 alone.
    thirds = [add(scale(F(1, 3), members[i]), scale(F(2, 3), members[j]))
              for i in range(len(members)) for j in range(len(members))
              if i != j]
    L('V/twenty_one_third_combinations_have_zero_coefficient',
      all_of(20, (orientation_coefficient(m) == 0 for m in thirds)))
    L('V/twenty_one_third_combinations_are_psd',
      all_of(20, (is_psd(m) for m in thirds)))
    # The mixed combination of an inside and an outside state must NOT be zero.
    mixed = add(scale(F(1, 2), members[0]), scale(F(1, 2), outside[0]))
    L('V/an_inside_outside_midpoint_is_NOT_in_the_sector',
      orientation_coefficient(mixed) != 0)

    # ---- the pseudoscalar identity, re-derived -----------------------------
    os_ = o2_generators()
    L('P/eight_generators_are_orthogonal',
      all_of(8, (mm(transpose(o), o) == I2 for o in os_)))
    L('P/four_generators_have_determinant_plus_one',
      all_of(4, (det(o) == 1 for o in os_[:4])))
    L('P/four_generators_have_determinant_minus_one',
      all_of(4, (det(o) == -1 for o in os_[4:])))
    L('P/OT_J_O_equals_det_times_J_on_all_eight',
      all_of(8, (mm(transpose(o), mm(J, o)) == scale(det(o), J)
                 for o in os_)))
    L('P/a_non_trivial_rational_rotation_is_present',
      any(o not in (eye(2),) and det(o) == 1 and o[0][0] not in (F(0), F(1),
                                                                F(-1))
          for o in os_))

    # ---- orthogonal closure ------------------------------------------------
    pairs = [(oa, ob) for oa in os_ for ob in os_]
    L('O/sixty_four_pairs_were_formed', len(pairs) == 64)
    conj_members = []
    for s in members:
        for (oa, ob) in pairs:
            u = kron(oa, ob)
            conj_members.append((s, oa, ob, mm(u, mm(s, transpose(u)))))
    L('O/three_hundred_twenty_conjugates_were_formed',
      len(conj_members) == 320)
    L('O/every_conjugate_is_psd',
      all_of(320, (is_psd(r) for (_, _, _, r) in conj_members)))
    L('O/every_conjugate_has_unit_trace',
      all_of(320, (trace(r) == 1 for (_, _, _, r) in conj_members)))
    L('O/every_conjugate_of_a_zero_state_has_zero_coefficient',
      all_of(320, (orientation_coefficient(r) == 0
                   for (_, _, _, r) in conj_members)))

    # The scaling law itself, on states that are NOT in the sector -- this is
    # what makes the closure leg non-vacuous, because 0 = det*det*0 holds for
    # any law whatsoever.
    scaling = []
    for s in outside:
        for (oa, ob) in pairs:
            u = kron(oa, ob)
            r = mm(u, mm(s, transpose(u)))
            scaling.append(orientation_coefficient(r)
                           == det(oa) * det(ob) * orientation_coefficient(s))
    L('O/one_hundred_twenty_eight_scaling_instances_were_formed',
      len(scaling) == 128)
    L('O/the_coefficient_scales_by_det_times_det_on_states_outside_the_sector',
      all_of(128, iter(scaling)))
    # And the sign genuinely flips somewhere, so 'pseudoscalar' is earned.
    flipped = []
    for s in outside:
        for (oa, ob) in pairs:
            if det(oa) * det(ob) == -1:
                u = kron(oa, ob)
                r = mm(u, mm(s, transpose(u)))
                flipped.append(orientation_coefficient(r)
                               == -orientation_coefficient(s)
                               and orientation_coefficient(s) != 0)
    n_reversing_pairs = len([1 for (oa, ob) in pairs
                             if det(oa) * det(ob) == -1])
    L('O/thirty_two_of_the_pairs_reverse_orientation', n_reversing_pairs == 32)
    L('O/sixty_four_sign_flip_instances_were_formed', len(flipped) == 64)
    L('O/the_instance_count_is_the_pair_count_times_the_outside_states',
      len(flipped) == n_reversing_pairs * len(outside))
    L('O/the_sign_reverses_at_every_instance', all_of(64, iter(flipped)))

    ev['sector_members'] = len(members)
    ev['conjugates_tested'] = len(conj_members)
    ev['scaling_instances'] = len(scaling)

    key_result = (
        f"The zero-coefficient sector is exhibited by {len(members)} members; "
        f"it is closed under the {len(mids)} pairwise midpoints and "
        f"{len(thirds)} one-third combinations tested; and all "
        f"{len(conj_members)} local orthogonal conjugates of its members stay "
        f"in it.  On the {len(outside)} states outside the sector the "
        f"coefficient scales by det(O_A) det(O_B) at all {len(scaling)} "
        f"instances and reverses sign at all {len(flipped)} instances drawn "
        f"from the {n_reversing_pairs} orientation-reversing pairs, so the "
        f"closure follows from a pseudoscalar law rather than from the "
        f"coefficient being zero everywhere.")

    return _result(
        _NAME, epistemic, key_result, ev, legs, MODULE_TIER,
        dependencies=(),
        premises=('LOCAL_ORTHOGONAL_CONJUGATION', 'PSD_CONE_CONVEXITY',
                  'O2_PSEUDOSCALAR'),
        negative_controls=(
            'two states OUTSIDE the sector are exhibited and their '
            'inside-outside midpoint is checked NOT to be in it',
            'the scaling law is exercised on the outside states, where 0 = '
            'det*det*0 cannot carry it',
            'the sign is checked to REVERSE at every orientation-reversing '
            'pair, so the pseudoscalar claim is not passing on a scalar law'),
        cross_refs=(
            'check_L_real_composite_only_direction_is_lambda_tensor_lambda',))


# ==========================================================================
# THE FROZEN LEG INVENTORY.  Set-exact labels, counts and SHA256 digests.
# ==========================================================================

EXPECTED_LEGS: Dict[str, FrozenSet[str]] = {
    'check_L_composite_orientation_is_selection_invisible': frozenset({
        'B/the_bank_arithmetic_was_reachable',
        'B/the_geometric_and_combinatorial_integers_agree',
        'D/JJ_is_in_sym4',
        'D/JJ_is_not_in_the_product_span',
        'D/JJ_is_orthogonal_to_every_product_basis_element',
        'D/JJ_is_symmetric',
        'D/product_span_plus_JJ_spans_sym4',
        'L/every_product_observable_agrees_on_the_pair',
        'L/the_difference_is_a_multiple_of_JJ',
        'L/the_pair_differs_as_matrices',
        'M/all_three_share_one_left_marginal',
        'M/all_three_share_one_right_marginal',
        'M/the_orientation_control_has_distinct_marginals',
        'M/the_orientation_control_is_a_valid_state',
        'M/the_rank_test_separates_the_states_the_marginals_cannot',
        'M/the_shared_marginals_are_the_maximally_mixed_qubit',
        'M/the_two_signed_states_leave_the_product_span',
        'M/the_zero_state_lies_inside_the_product_span',
        'M/tracing_out_the_first_factor_returns_the_second',
        'M/tracing_out_the_second_factor_returns_the_first',
        'Q/the_quantifier_refuses_a_short_sequence',
        'Q/the_quantifier_refuses_a_truthy_non_bool',
        'Q/the_quantifier_refuses_an_emptied_sequence',
        'S/complement_has_dimension_1',
        'S/product_span_has_dimension_9',
        'S/product_span_is_inside_sym4',
        'S/sym4_has_dimension_10',
        'W/the_direction_has_coefficient_one_in_its_own_normalization',
        'W/the_psd_test_accepts_a_genuine_psd_matrix',
        'W/the_psd_test_rejects_a_matrix_that_passes_the_leading_minor_test',
        'W/the_two_signed_states_are_negatives_in_the_coefficient',
        'W/the_zero_state_has_zero_coefficient',
        'W/three_coefficients_are_pairwise_distinct',
        'W/three_coefficients_are_the_three_parameters',
        'W/three_states_are_psd',
        'W/three_states_are_symmetric',
        'W/three_states_have_unit_trace',
    }),
    'check_L_composite_orientation_reachability_is_field_dependent': frozenset({
        'C/J_tensor_J_is_hermitian_over_C',
        'C/Y_is_hermitian',
        'C/Y_is_i_times_J',
        'C/Y_squares_to_the_identity',
        'C/Y_tensor_Y_is_hermitian',
        'C/minus_Y_tensor_Y_equals_J_tensor_J',
        'C/product_state_expectation_of_Y_tensor_Y_is_zero',
        'C/product_state_has_unit_trace',
        'C/product_state_is_hermitian',
        'C/singlet_expectation_is_non_zero',
        'C/singlet_expectation_is_real',
        'C/singlet_expectation_of_Y_tensor_Y_is_minus_one',
        'C/singlet_has_unit_trace',
        'C/singlet_is_hermitian',
        'C/singlet_is_idempotent',
        'F/JJ_is_in_the_complex_product_span',
        'F/every_complex_product_basis_element_is_hermitian',
        'F/the_complex_product_span_has_sixteen_elements',
        'F/the_complex_product_span_is_sixteen_dimensional_over_R',
        'F/the_complex_span_test_rejects_a_non_hermitian_matrix',
        'F/the_two_membership_verdicts_differ_on_one_matrix',
        'Q/the_quantifier_refuses_a_short_sequence',
        'Q/the_quantifier_refuses_an_emptied_sequence',
        'R/JJ_is_outside_the_real_product_span',
        'R/J_is_antisymmetric',
        'R/every_real_local_pairing_with_JJ_vanishes',
        'R/the_factorization_is_non_zero_somewhere',
        'R/the_pairing_is_the_transposed_trace_not_the_plain_trace',
        'R/the_product_trace_factorizes_on_symmetric_arguments',
        'R/the_product_trace_factorizes_on_thirty_six_general_arguments',
        'R/the_two_pairings_agree_on_symmetric_arguments',
        'R/trace_of_symmetric_against_J_vanishes',
    }),
    'check_L_composite_orientation_zero_sector_is_closed': frozenset({
        'N/five_members_are_pairwise_distinct',
        'N/five_members_are_psd',
        'N/five_members_are_symmetric',
        'N/five_members_have_unit_trace',
        'N/five_members_have_zero_coefficient',
        'N/five_members_were_formed',
        'N/the_coefficient_is_not_identically_zero_on_valid_states',
        'N/two_exhibited_states_lie_OUTSIDE_the_sector',
        'O/every_conjugate_has_unit_trace',
        'O/every_conjugate_is_psd',
        'O/every_conjugate_of_a_zero_state_has_zero_coefficient',
        'O/one_hundred_twenty_eight_scaling_instances_were_formed',
        'O/sixty_four_pairs_were_formed',
        'O/sixty_four_sign_flip_instances_were_formed',
        'O/the_coefficient_scales_by_det_times_det_on_states_outside_the_sector',
        'O/the_instance_count_is_the_pair_count_times_the_outside_states',
        'O/the_sign_reverses_at_every_instance',
        'O/thirty_two_of_the_pairs_reverse_orientation',
        'O/three_hundred_twenty_conjugates_were_formed',
        'P/OT_J_O_equals_det_times_J_on_all_eight',
        'P/a_non_trivial_rational_rotation_is_present',
        'P/eight_generators_are_orthogonal',
        'P/four_generators_have_determinant_minus_one',
        'P/four_generators_have_determinant_plus_one',
        'Q/the_quantifier_refuses_a_short_sequence',
        'Q/the_quantifier_refuses_an_emptied_sequence',
        'V/an_inside_outside_midpoint_is_NOT_in_the_sector',
        'V/ten_midpoints_are_psd',
        'V/ten_midpoints_have_unit_trace',
        'V/ten_midpoints_have_zero_coefficient',
        'V/ten_midpoints_were_formed',
        'V/twenty_one_third_combinations_are_psd',
        'V/twenty_one_third_combinations_have_zero_coefficient',
    }),
}

EXPECTED_LEG_COUNTS: Dict[str, int] = {
    'check_L_composite_orientation_is_selection_invisible': 37,
    'check_L_composite_orientation_reachability_is_field_dependent': 32,
    'check_L_composite_orientation_zero_sector_is_closed': 33,
}

EXPECTED_LEG_DIGEST: Dict[str, str] = {
    'check_L_composite_orientation_is_selection_invisible':
        '4c414b1844a566d088ac5e791c8b0da107cd7c39e942db16509928c6d38ac60a',
    'check_L_composite_orientation_reachability_is_field_dependent':
        'e5c94bf6f1064d4b0b6ca6a50384f10586e5a9a683c870279b180199d868b3f2',
    'check_L_composite_orientation_zero_sector_is_closed':
        '51c2ce01d37e217ac745c8fe224cf349d0e3ca750c20bce84e2ea1c4d234e77e',
}


_CHECKS = {
    'L_composite_orientation_is_selection_invisible':
        check_L_composite_orientation_is_selection_invisible,
    'L_composite_orientation_reachability_is_field_dependent':
        check_L_composite_orientation_reachability_is_field_dependent,
    'L_composite_orientation_zero_sector_is_closed':
        check_L_composite_orientation_zero_sector_is_closed,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    out = []
    for name, fn in _CHECKS.items():
        r = fn()
        out.append(r)
        print(f"{'PASS' if r['passed'] else 'FAIL'}  {r['name']}  "
              f"({r['legs_evaluated']} legs)")
        if not r['passed']:
            print('   ', r['summary'])
    return out


if __name__ == '__main__':
    run_all()
