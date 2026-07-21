"""Finite certificates for the APF quantum front-end gap-closure pass.

The module separates quantum *soundness* from optional *saturation*.
It certifies exact finite mathematical implications and negative controls;
it does not certify that the named APF physical premises obtain in nature.

Definition (used in key results and the certificate scope): an
*extension-sound process* is a process whose Choi-corner extension exists and
preserves positivity -- its local action extends as the identity on the
independently maintained same-type reference while the joint positive cone is
preserved.

Fortification pass 2026-07-20: cold-audit fixes carried (computed partial
transpose, executed readout congruence with negative control, D4 composite
algebra, finite Jordan-von-Neumann polarization leg, symbolic dual-action
span exclusion, dependency contract re-billed to the installed held-holonomy
granularity).

Bank landing v24.3.430 (2026-07-20): registered in the theorem bank
(family ``quantum.frontend_closure``, 10 checks); NON-exporting at the
physical gate -- every result carries physical_premises_certified=False.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from fractions import Fraction as F
from itertools import combinations, product
from typing import Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

Matrix = List[List[F]]
Vector = List[F]
FAMILY = "quantum.frontend_closure"
PAPER_TARGETS = (
    "Paper 5",
    "Paper 5 Technical Supplement",
    "Paper 14",
)


def _shape(a: Matrix) -> Tuple[int, int]:
    return len(a), len(a[0]) if a else 0


def _zero(r: int, c: int) -> Matrix:
    return [[F(0) for _ in range(c)] for _ in range(r)]


def _eye(n: int) -> Matrix:
    return [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]


def _transpose(a: Matrix) -> Matrix:
    return [[a[i][j] for i in range(len(a))] for j in range(len(a[0]))]


def _add(a: Matrix, b: Matrix) -> Matrix:
    assert _shape(a) == _shape(b)
    return [[a[i][j] + b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def _sub(a: Matrix, b: Matrix) -> Matrix:
    assert _shape(a) == _shape(b)
    return [[a[i][j] - b[i][j] for j in range(len(a[0]))] for i in range(len(a))]


def _scal(s: F, a: Matrix) -> Matrix:
    return [[s * x for x in row] for row in a]


def _mm(a: Matrix, b: Matrix) -> Matrix:
    ar, ac = _shape(a)
    br, bc = _shape(b)
    if ac != br:
        raise ValueError("matrix shape mismatch")
    return [[sum(a[i][k] * b[k][j] for k in range(ac)) for j in range(bc)]
            for i in range(ar)]


def _mv(a: Matrix, v: Vector) -> Vector:
    if not a or len(a[0]) != len(v):
        raise ValueError("matrix/vector shape mismatch")
    return [sum(a[i][j] * v[j] for j in range(len(v))) for i in range(len(a))]


def _dot(x: Vector, y: Vector) -> F:
    return sum(a * b for a, b in zip(x, y))


def _eq(a: Matrix, b: Matrix) -> bool:
    return _shape(a) == _shape(b) and all(
        a[i][j] == b[i][j]
        for i in range(len(a)) for j in range(len(a[0]))
    )


def _det2(a: Matrix) -> F:
    if _shape(a) != (2, 2):
        raise ValueError("det2 requires 2x2")
    return a[0][0] * a[1][1] - a[0][1] * a[1][0]


def _is_psd_2(a: Matrix) -> bool:
    return (
        _shape(a) == (2, 2)
        and a[0][1] == a[1][0]
        and a[0][0] >= 0
        and a[1][1] >= 0
        and _det2(a) >= 0
    )


def _rank(a: Matrix) -> int:
    if not a:
        return 0
    m = [row[:] for row in a]
    r, c = _shape(m)
    rank = 0
    col = 0
    while rank < r and col < c:
        pivot = next((i for i in range(rank, r) if m[i][col] != 0), None)
        if pivot is None:
            col += 1
            continue
        m[rank], m[pivot] = m[pivot], m[rank]
        p = m[rank][col]
        m[rank] = [x / p for x in m[rank]]
        for i in range(r):
            if i == rank:
                continue
            q = m[i][col]
            if q:
                m[i] = [m[i][j] - q * m[rank][j] for j in range(c)]
        rank += 1
        col += 1
    return rank


def _partial_transpose(rho: Matrix, d1: int, d2: int) -> Matrix:
    """Exact partial transpose on the SECOND tensor factor of a d1*d2 matrix.

    Index convention: row/column index (i, a) is flattened as i*d2 + a.
    (PT rho)[(i,a),(j,b)] = rho[(i,b),(j,a)].
    """
    n = d1 * d2
    if _shape(rho) != (n, n):
        raise ValueError("partial transpose requires a (d1*d2) x (d1*d2) matrix")
    out = _zero(n, n)
    for i in range(d1):
        for j in range(d1):
            for a in range(d2):
                for b in range(d2):
                    out[i * d2 + a][j * d2 + b] = rho[i * d2 + b][j * d2 + a]
    return out


def _det(a: Matrix) -> F:
    """Exact determinant by Laplace expansion (small matrices only)."""
    n = len(a)
    if n == 0:
        return F(1)
    if n == 1:
        return a[0][0]
    total = F(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in a[1:]]
        term = a[0][j] * _det(minor)
        total += term if j % 2 == 0 else -term
    return total


def _psd_by_principal_minors(a: Matrix) -> bool:
    """Exact PSD certificate for a symmetric matrix.

    A symmetric matrix is positive semidefinite iff ALL principal minors
    (not only the leading ones) are nonnegative.  Exact over Fractions.
    """
    n = len(a)
    if any(a[i][j] != a[j][i] for i in range(n) for j in range(n)):
        return False
    for k in range(1, n + 1):
        for idx in combinations(range(n), k):
            sub_m = [[a[i][j] for j in idx] for i in idx]
            if _det(sub_m) < 0:
                return False
    return True


def _matrix_strings(a: Matrix) -> List[List[str]]:
    return [[str(x) for x in row] for row in a]


def _result(name: str, epistemic: str, key_result: str,
            dependencies: Sequence[str], artifacts: Mapping[str, object],
            fails: Sequence[str], premises: Sequence[str] = (),
            negative_controls: Sequence[str] = (),
            cross_refs: Sequence[str] = ()) -> Dict[str, object]:
    passed = not fails
    return {
        "name": name,
        "family": FAMILY,
        "epistemic": epistemic,
        "tier": 4,
        "passed": passed,
        "status": "PASS" if passed else "FAIL",
        "scope": "finite mathematical witness",
        "physical_premises_certified": False,
        "premises": list(premises),
        "negative_controls": list(negative_controls),
        "paper_targets": list(PAPER_TARGETS),
        "key_result": key_result,
        "dependencies": list(dependencies),
        "cross_refs": list(cross_refs),
        "artifacts": dict(artifacts),
        "fail_reasons": list(fails),
    }


@dataclass(frozen=True)
class FrontendClosureCertificate:
    finite_fragment_rank: bool
    ordered_score_bilinearization: bool
    dual_action_without_reverse_saturation: bool
    canonical_readout_quotient: bool
    effect_soundness_separated_from_saturation: bool
    operator_system_density_extension: bool
    composite_tensor_quotient: bool
    held_to_observable_descent_criterion: bool
    same_type_reference_cp_test: bool
    dependency_contract_acyclic: bool
    physical_premises_certified: bool
    core_scope: str
    remaining_physical_kernel: Tuple[str, ...]
    optional_saturation_claims: Tuple[str, ...]


def check_T_finite_protocol_fragment_rank() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # Four preparation profiles evaluated on three terminal tests.
    score_table: Matrix = [
        [F(1), F(0), F(1, 2)],
        [F(0), F(1), F(1, 2)],
        [F(1, 2), F(1, 2), F(1)],
        [F(1, 3), F(2, 3), F(1, 2)],
    ]
    fragment_rank = _rank(score_table)
    ck(fragment_rank == 3, "the shipped four-profile/three-test table has exact rank three")

    # Rank is a property of the table, not the shape: a 4x3 table with two
    # dependent rows (row3 = row1 + row2, row4 = 2*row1 + row2) has rank 2.
    deficient_table: Matrix = [
        [F(1), F(0), F(1)],
        [F(0), F(1), F(1)],
        [F(1), F(1), F(2)],
        [F(2), F(1), F(3)],
    ]
    deficient_rank = _rank(deficient_table)
    ck(deficient_rank == 2,
       "the rank-deficient 4x3 control must have exact rank two")

    # Per-fragment finiteness alone gives no uniform global rank.
    growing_ranks = []
    for n in range(1, 8):
        growing_ranks.append(_rank(_eye(n)))
    ck(growing_ranks == list(range(1, 8)),
       "identity fragments provide an exact unbounded-rank negative control")

    return _result(
        "T_finite_protocol_fragment_rank",
        "P_math",
        ("Every fixed finite protocol/readout table has a finite score-profile "
         "span; the shipped table has exact computed rank three, and a same-shape "
         "4x3 control has exact rank two, so the rank is a property of the table, "
         "not the shape.  A single uniform rank bound over all finite fragments "
         "is a strictly stronger global statement: the identity-table sequence "
         "has finite rank at every stage and unbounded ranks across stages."),
        [],
        {
            "score_table": _matrix_strings(score_table),
            "fragment_rank": fragment_rank,
            "deficient_control_table": _matrix_strings(deficient_table),
            "deficient_control_rank": deficient_rank,
            "coordinate_count": 3,
            "growing_fragment_ranks": growing_ranks,
            "uniform_global_rank_derived": False,
        },
        fails,
        premises=("fixed_finite_protocol_fragment", "finite_exact_readout_coordinates"),
        negative_controls=("the n-by-n identity score tables have rank n",),
        cross_refs=("Paper 5 Q1", "Paper 44 finite/continuum seam"),
    )


def check_T_ordered_score_bilinearization() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    lam = F(2, 3)
    k = [[F(1), lam], [-lam, F(1)]]
    b = _scal(F(1, 2), _add(k, _transpose(k)))
    a = _scal(F(1, 2), _sub(k, _transpose(k)))
    ck(_eq(b, _eye(2)), "the symmetric part must be the Euclidean ledger form")
    ck(not _eq(a, _zero(2, 2)), "the ordered score must retain a nonzero alternating part")
    ck(_is_psd_2(b) and _det2(b) > 0, "the symmetric part must be positive definite")

    grid = [F(-2), F(-1), F(0), F(1), F(2)]
    checked = 0
    for x1, x2, y1, y2 in product(grid, repeat=4):
        x = [x1, x2]
        y = [y1, y2]
        qx = _dot(x, _mv(k, x))
        qy = _dot(y, _mv(k, y))
        qxy = _dot([x1 + y1, x2 + y2], _mv(k, [x1 + y1, x2 + y2]))
        qxmy = _dot([x1 - y1, x2 - y2], _mv(k, [x1 - y1, x2 - y2]))
        ck(qx == _dot(x, x), "alternating score component must vanish on the diagonal")
        ck(qxy + qxmy == 2 * qx + 2 * qy,
           "the derived diagonal must satisfy the parallelogram identity")
        checked += 1

    # Executed finite Jordan-von-Neumann leg.  An additive score TABLE on a
    # finite grid of a 2-dimensional rational space is defined from a bilinear
    # form kjvn but ACCESSED only through the table interface; the candidate
    # bilinear form is DERIVED by polarization B(u,v) = (q(u+v)-q(u)-q(v))/2
    # from q(u) = s(u,u) and verified slotwise additive on the grid, and it
    # reproduces kjvn's symmetric part.
    kjvn: Matrix = [[F(1), F(1)], [F(0), F(2)]]  # deliberately non-symmetric
    table_dom = range(-6, 7)
    score_lookup: Dict[Tuple[F, F], F] = {}
    for t0, t1 in product(table_dom, repeat=2):
        u = [F(t0), F(t1)]
        score_lookup[(u[0], u[1])] = _dot(u, _mv(kjvn, u))

    def q_score(u: Vector) -> F:
        return score_lookup[(u[0], u[1])]

    def pol(u: Vector, v: Vector) -> F:
        return (q_score([u[0] + v[0], u[1] + v[1]]) - q_score(u) - q_score(v)) / 2

    ksym = _scal(F(1, 2), _add(kjvn, _transpose(kjvn)))
    small_vecs = [[F(x), F(y)] for x, y in product(range(-2, 3), repeat=2)]
    jvn_pol_cases = 0
    for u in small_vecs:
        for v in small_vecs:
            ck(pol(u, v) == _dot(u, _mv(ksym, v)),
               "polarization must reproduce the symmetric part of the generating form")
            jvn_pol_cases += 1
    jvn_add_cases = 0
    probe = [[F(x), F(y)] for x, y in product(range(-1, 2), repeat=2)]
    for u in probe:
        for up in probe:
            for v in probe:
                usum = [u[0] + up[0], u[1] + up[1]]
                ck(pol(usum, v) == pol(u, v) + pol(up, v),
                   "the derived form must be additive in the first slot")
                ck(pol(v, usum) == pol(v, u) + pol(v, up),
                   "the derived form must be additive in the second slot")
                jvn_add_cases += 1

    # Negative control: a cubic perturbation of the score must break the
    # derived slot additivity (computed, asserted as failing).
    def q_bad(u: Vector) -> F:
        return q_score(u) + u[0] ** 3

    def pol_bad(u: Vector, v: Vector) -> F:
        return (q_bad([u[0] + v[0], u[1] + v[1]]) - q_bad(u) - q_bad(v)) / 2

    cubic_violation = False
    for u in probe:
        for up in probe:
            for v in probe:
                usum = [u[0] + up[0], u[1] + up[1]]
                if pol_bad(usum, v) != pol_bad(u, v) + pol_bad(up, v):
                    cubic_violation = True
                    break
            if cubic_violation:
                break
        if cubic_violation:
            break
    ck(cubic_violation,
       "the cubic-perturbed score must fail the derived-additivity leg")

    return _result(
        "T_ordered_score_bilinearization",
        "P_math",
        ("Conditional on one completed ordered score, a typed preparation/test "
         "role isomorphism, and a faithful nonnegative diagonal, the symmetric "
         "part is a positive ledger form.  The alternating orientation data "
         "survives off diagonal, while the diagonal derives the parallelogram "
         "identity.  The Jordan-von-Neumann direction is EXECUTED on a finite "
         "grid: an additive score table, accessed only through the score "
         "interface, polarizes to a form that is slotwise additive and equals "
         "the generating form's symmetric part, while a cubic perturbation is "
         "computed to fail derived additivity.  The completion from the finite "
         "grid to the infinite space stays a named premise; the physical score "
         "and the role isomorphism are not constructed here."),
        [],
        {
            "ordered_score_operator": _matrix_strings(k),
            "symmetric_ledger_form": _matrix_strings(b),
            "alternating_part": _matrix_strings(a),
            "grid_cases_checked": checked,
            "parallelogram_derived": True,
            "jvn_generating_form": _matrix_strings(kjvn),
            "jvn_symmetric_part": _matrix_strings(ksym),
            "jvn_polarization_matches_symmetric_part": True,
            "jvn_polarization_cases": jvn_pol_cases,
            "jvn_slot_additivity_cases": jvn_add_cases,
            "jvn_derived_bilinearity": True,
            "jvn_cubic_control_fails": cubic_violation,
            "physical_ordered_score_constructed": False,
            "boundary_role_isomorphism_derived": False,
        },
        fails,
        premises=(
            "separately_additive_completed_two_ended_score",
            "typed_boundary_role_linear_isomorphism",
            "faithful_nonnegative_diagonal_score",
            "jordan_von_neumann_completion_beyond_the_finite_grid",
        ),
        negative_controls=(
            "nonzero alternating score data is invisible on the scalar diagonal",
            "a cubic score perturbation breaks derived polarization additivity",
        ),
        cross_refs=("Paper 1 disjoint-score additivity", "Paper 5 Q2A"),
    )


def check_T_dual_action_without_physical_reverse_saturation() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    i2 = _eye(2)
    n = [[F(0), F(1)], [F(0), F(0)]]
    n_dual = _transpose(n)
    # Exact symbolic span-exclusion.  For ALL rational a, b the (1,0) entry of
    # a*I + b*N equals a*I[1][0] + b*N[1][0]; both base entries are identically
    # zero, so the entry is 0 for every coefficient pair, while N^T has (1,0)
    # entry 1 != 0.  Hence N^T is outside span{I,N} -- a one-line proof over
    # symbolic coefficients, no coefficient grid required.
    ck(i2[1][0] == 0 and n[1][0] == 0,
       "the (1,0) entries of I and N vanish, so (aI+bN)[1][0] == 0 identically")
    ck(n_dual[1][0] != 0,
       "N^T has nonzero (1,0) entry, hence lies outside span{I,N} for all a,b")
    # Finite grid scan retained as corroboration only.
    in_phys = any(_eq(n_dual, _add(_scal(F(a), i2), _scal(F(b), n)))
                  for a, b in product(range(-3, 4), repeat=2))
    ck(not in_phys, "grid corroboration: the algebraic dual is outside the physical algebra")

    checks = 0
    for e0, e1, p0, p1 in product(range(-2, 3), repeat=4):
        e = [F(e0), F(e1)]
        p = [F(p0), F(p1)]
        ck(_dot(e, _mv(n, p)) == _dot(_mv(n_dual, e), p),
           "the algebraic dual action must satisfy the two-ended pairing identity")
        checks += 1

    return _result(
        "T_dual_action_without_physical_reverse_saturation",
        "P_math",
        ("Every represented preparation-side process has a unique dual action "
         "on terminal tests once the two-ended pairing is nondegenerate.  The "
         "dual need not be an admitted reverse dynamics.  Therefore the "
         "observable adjoint envelope can be constructed without assuming "
         "physical reverse saturation for every irreversible process."),
        ["T_ordered_score_bilinearization"],
        {
            "physical_generator_N": _matrix_strings(n),
            "algebraic_dual_N_star": _matrix_strings(n_dual),
            "span_exclusion_symbolic": True,
            "entry_10_identically_zero_on_span": True,
            "N_T_entry_10": str(n_dual[1][0]),
            "dual_in_physical_upper_triangular_algebra": in_phys,
            "pairing_cases_checked": checks,
        },
        fails,
        premises=("nondegenerate_two_ended_pairing",),
        negative_controls=(
            "N^T is not in Alg{I,N}: (aI+bN)[1][0]=0 identically while N^T[1][0]=1",
        ),
        cross_refs=("Paper 37 mathematical adjoint versus physical reversal", "Paper 5 Q2"),
    )


def check_T_canonical_readout_quotient() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # Commutative finite C*-algebra R^3 with pointwise product; the readout
    # map is an EXECUTED function, and the kernel is DERIVED from it.
    zero2 = (F(0), F(0))

    def mul(x: Tuple[F, F, F], y: Tuple[F, F, F]) -> Tuple[F, F, F]:
        return (x[0] * y[0], x[1] * y[1], x[2] * y[2])

    def readout(x: Tuple[F, F, F]) -> Tuple[F, F]:
        return (x[0], x[1])

    def nc(x: Tuple[F, F, F]) -> Tuple[F, F]:
        # Non-congruence control map: NOT an algebra homomorphism.
        return (x[0] + x[2], x[1])

    rng = [F(v) for v in range(-2, 3)]
    samples = [tuple(F(v) for v in xyz) for xyz in product(range(-2, 3), repeat=3)]

    # Kernel derived from the executed readout, then identified with
    # span{(0,0,1)} by membership BOTH directions on the grid.
    kernel = [x for x in samples if readout(x) == zero2]
    ck(all(x[0] == 0 and x[1] == 0 for x in kernel),
       "every derived kernel element lies on the e3 line")
    kernel_set = set(kernel)
    ck(all((F(0), F(0), t) in kernel_set for t in rng),
       "every grid multiple of e3 lies in the derived kernel")
    ck(len(kernel) == len(rng),
       "on the grid, the derived kernel is exactly the e3 line")

    # Ideal leg: the derived kernel absorbs products on both sides.
    for k in kernel:
        for b in samples:
            ck(readout(mul(k, b)) == zero2,
               "the derived kernel must be a right-absorbing ideal")
            ck(readout(mul(b, k)) == zero2,
               "the derived kernel must be a left-absorbing ideal")

    # Congruence leg: for kernel-equivalent pairs (a ~ b iff readout(a) ==
    # readout(b)), products remain equivalent on both sides.
    small = [tuple(F(v) for v in xyz) for xyz in product(range(-1, 2), repeat=3)]
    congruence_cases = 0
    for a in small:
        for t in rng:
            b = (a[0], a[1], a[2] + t)
            ck(readout(a) == readout(b), "the shifted pair must be kernel-equivalent")
            for c in small:
                ck(readout(mul(a, c)) == readout(mul(b, c)),
                   "right products of equivalent elements must stay equivalent")
                ck(readout(mul(c, a)) == readout(mul(c, b)),
                   "left products of equivalent elements must stay equivalent")
                congruence_cases += 1

    # Quotient product table COMPUTED on representatives (u,v,0) and matched
    # against the componentwise product on R^2.
    table_cases = 0
    for u1 in rng:
        for v1 in rng:
            for u2 in rng:
                for v2 in rng:
                    got = readout(mul((u1, v1, F(0)), (u2, v2, F(0))))
                    ck(got == (u1 * u2, v1 * v2),
                       "the computed quotient table must be the componentwise R^2 product")
                    table_cases += 1
    quotient_table_sample = {
        "({}, {})*({}, {})".format(u1, v1, u2, v2):
            [str(x) for x in readout(mul((u1, v1, F(0)), (u2, v2, F(0))))]
        for u1 in (F(-1), F(0), F(1)) for v1 in (F(-1), F(0), F(1))
        for u2 in (F(-1), F(0), F(1)) for v2 in (F(-1), F(0), F(1))
        if abs(u1) + abs(v1) + abs(u2) + abs(v2) <= 2
    }

    # Negative control: the non-congruence map nc(x) = (x0+x2, x1).  Its
    # derived kernel is NOT an ideal, and the congruence leg FAILS for it.
    nc_kernel_witness = (F(1), F(0), F(-1))
    ck(nc(nc_kernel_witness) == zero2, "the nc-kernel witness must be nc-null")
    nc_absorber = (F(1), F(1), F(0))
    nc_product = mul(nc_kernel_witness, nc_absorber)
    ck(nc(nc_product) != zero2,
       "computed: the nc kernel fails absorption, hence it is not an ideal")
    nc_pair_a = (F(0), F(0), F(0))
    nc_pair_b = nc_kernel_witness
    ck(nc(nc_pair_a) == nc(nc_pair_b), "the nc control pair must be nc-equivalent")
    nc_c = (F(1), F(0), F(0))
    nc_congruence_violated = nc(mul(nc_pair_a, nc_c)) != nc(mul(nc_pair_b, nc_c))
    ck(nc_congruence_violated,
       "computed: the congruence leg must FAIL for the non-congruence map")

    return _result(
        "T_canonical_readout_quotient",
        "P_math",
        ("For a declared closed-context algebra and strong contextual "
         "equivalence, the full involutive quotient is canonical and its "
         "self-adjoint part is the observable space.  The witness EXECUTES the "
         "readout, derives its kernel, verifies the two-sided ideal and "
         "congruence properties on the grid, and computes the quotient product "
         "table, which matches the componentwise R^2 product; the non-"
         "congruence control map is computed to fail both.  The witness is "
         "commutative, so its identity involution is honest here; the "
         "noncommutative involutive case is carried by the operator-system and "
         "dual-action checks.  Completed-record context totality, linear score "
         "separation, certain-effect typing, and physical realization remain "
         "separate APF obligations."),
        ["T_dual_action_without_physical_reverse_saturation"],
        {
            "source_algebra": "R^3 with pointwise product",
            "readout_map": "executed function (x,y,z) -> (x,y)",
            "kernel_derived_from_readout": True,
            "kernel_basis": [["0", "0", "1"]],
            "kernel_is_two_sided_ideal": True,
            "congruence_verified": True,
            "congruence_cases": congruence_cases,
            "quotient_product_table_cases": table_cases,
            "quotient_table_matches_componentwise_R2": True,
            "quotient_product_table_sample": quotient_table_sample,
            "involution": ("identity involution; honest on this commutative "
                           "witness -- the noncommutative case is carried by "
                           "the operator-system and dual-action checks"),
            "nc_kernel_not_ideal_witness": [str(x) for x in nc_product],
            "nc_kernel_not_ideal": True,
            "nc_congruence_fails": nc_congruence_violated,
            "sample_kernel_size": len(kernel),
            "full_algebra_before_self_adjoint_part": True,
            "completed_record_context_totality_derived": False,
            "certain_effect_typed": False,
        },
        fails,
        premises=("strong_closed_boundary_contextual_equivalence",),
        negative_controls=(
            "a hidden third summand remains invisible if the domain is enlarged beyond actual closed readouts",
            "nc(x) = (x0+x2, x1): kernel is not an ideal and congruence fails (computed)",
        ),
        cross_refs=("Paper 1 two-sided contextual congruence", "Paper 5 Q2C"),
    )


def check_T_effect_soundness_not_saturation() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    i2 = _eye(2)
    zero = _zero(2, 2)
    p0 = [[F(1), F(0)], [F(0), F(0)]]
    p1 = [[F(0), F(0)], [F(0), F(1)]]
    half = _scal(F(1, 2), i2)
    pplus = [[F(1, 2), F(1, 2)], [F(1, 2), F(1, 2)]]
    physical = [zero, i2, p0, p1, half]

    for e in physical:
        ck(_is_psd_2(e), "every admitted effect must be positive")
        ck(_is_psd_2(_sub(i2, e)), "every admitted effect must be bounded by the order unit")
    ck(_is_psd_2(pplus) and _is_psd_2(_sub(i2, pplus)),
       "the excluded P+ projector is a valid algebraic effect")
    ck(not any(_eq(pplus, e) for e in physical),
       "the sound physical effect set must be a proper nonsaturated subset")

    return _result(
        "T_effect_soundness_not_saturation",
        "P_math",
        ("Quantum soundness requires only that every physical effect embed as "
         "a positive contraction.  Equality with the entire matrix interval "
         "[0,I] is a separate effect-saturation theorem.  A restricted effect "
         "set can be perfectly quantum while omitting valid POVM effects."),
        ["T_canonical_readout_quotient"],
        {
            "physical_effect_count": len(physical),
            "excluded_positive_effect": _matrix_strings(pplus),
            "sound": True,
            "saturated": False,
        },
        fails,
        premises=("order_sound_physical_readouts",),
        negative_controls=("the positive projector |+><+| is algebraically valid but not admitted",),
        cross_refs=("Paper 5 Q3 effect completion",),
    )


def check_T_operator_system_state_extension() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    z = F(1, 3)

    def rho(x: F) -> Matrix:
        return [[(F(1) + z) / 2, x / 2], [x / 2, (F(1) - z) / 2]]

    rho0 = rho(F(0))
    rho1 = rho(F(1, 2))
    ck(_is_psd_2(rho0) and _is_psd_2(rho1), "both density extensions must be positive")
    ck(sum(rho0[i][i] for i in range(2)) == 1, "rho0 must be normalized")
    ck(sum(rho1[i][i] for i in range(2)) == 1, "rho1 must be normalized")
    exp_z0 = rho0[0][0] - rho0[1][1]
    exp_z1 = rho1[0][0] - rho1[1][1]
    ck(exp_z0 == z and exp_z1 == z,
       "both density matrices must agree on the operator system span{I,Z}")
    ck(not _eq(rho0, rho1), "the extension must be nonunique before tomography completes")

    return _result(
        "T_operator_system_state_extension",
        "P_math",
        ("A positive normalized state on the physical operator system already "
         "admits a density-operator extension to the generated matrix algebra. "
         "State completion is not required for existence.  Tomographic "
         "completeness is required only for uniqueness and for claiming that "
         "every algebraic density is physically preparable."),
        ["T_effect_soundness_not_saturation"],
        {
            "operator_system": "span_R{I,Z} in M2",
            "declared_expectation_Z": str(z),
            "density_extension_0": _matrix_strings(rho0),
            "density_extension_1": _matrix_strings(rho1),
            "extensions_unique": False,
        },
        fails,
        premises=("positive_unital_state_on_physical_operator_system",),
        negative_controls=("two distinct density matrices agree on span{I,Z}",),
        cross_refs=("finite-dimensional positive extension theorem", "Paper 5 Born representation"),
    )


def check_T_composite_tensor_quotient() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # Real algebra witness: the diagonal subalgebra D4 of M4 realized as
    # C^2 (x) C^2, diagonal entries indexed by pairs (i,a) flattened as i*2+a.
    def diag4(d: Sequence[F]) -> Matrix:
        return [[d[i] if i == j else F(0) for j in range(4)] for i in range(4)]

    def emb_a(a: Tuple[F, F]) -> Matrix:
        # a (x) I on the diagonal: (a0, a0, a1, a1).
        return diag4([a[0], a[0], a[1], a[1]])

    def emb_b(b: Tuple[F, F]) -> Matrix:
        # I (x) b on the diagonal: (b0, b1, b0, b1).
        return diag4([b[0], b[1], b[0], b[1]])

    grid2 = [(F(x), F(y)) for x, y in product(range(-2, 3), repeat=2)]

    # Executed commutation of the two embeddings over the grid.
    commutation_cases = 0
    for a in grid2:
        for b in grid2:
            ck(_eq(_mm(emb_a(a), emb_b(b)), _mm(emb_b(b), emb_a(a))),
               "the tensor-split embeddings must commute exactly")
            commutation_cases += 1

    # Executed unitality.
    one2 = (F(1), F(1))
    ck(_eq(emb_a(one2), _eye(4)), "emb_a must be unital")
    ck(_eq(emb_b(one2), _eye(4)), "emb_b must be unital")

    # Executed injectivity: distinct grid elements have distinct images.
    imgs_a = {tuple(emb_a(a)[i][i] for i in range(4)) for a in grid2}
    imgs_b = {tuple(emb_b(b)[i][i] for i in range(4)) for b in grid2}
    ck(len(imgs_a) == len(grid2), "emb_a must be injective on the grid")
    ck(len(imgs_b) == len(grid2), "emb_b must be injective on the grid")

    # Executed generation: diagonal coordinates of products emb_a(a)emb_b(b)
    # span D4 -- exact rank-4 computation.
    prod_rows: Matrix = []
    for a in grid2:
        for b in grid2:
            m = _mm(emb_a(a), emb_b(b))
            prod_rows.append([m[i][i] for i in range(4)])
    generation_rank = _rank(prod_rows)
    ck(generation_rank == 4, "products of the images must span D4 (rank 4)")

    # Quotient: the corner/conditional-expectation onto entries with second
    # index = 0, a surjective *-homomorphism D4 -> D2.
    def quotient(m4: Matrix) -> Matrix:
        return [[m4[0][0], F(0)], [F(0), m4[2][2]]]

    ck(_eq(quotient(_eye(4)), _eye(2)), "the quotient map must be unital")
    grid4 = [tuple(F(v) for v in d) for d in product(range(-1, 2), repeat=4)]
    quotient_mult_cases = 0
    for dx in grid4:
        for dy in grid4:
            x4 = diag4(list(dx))
            y4 = diag4(list(dy))
            ck(_eq(quotient(_mm(x4, y4)), _mm(quotient(x4), quotient(y4))),
               "the corner quotient must be exactly multiplicative on D4")
            quotient_mult_cases += 1
    ck(all(_eq(quotient(emb_a(a)), [[a[0], F(0)], [F(0), a[1]]]) for a in grid2),
       "the quotient must restrict to the identity on the first factor, hence surjective")
    kernel_positions = [1, 3]
    ck(all(quotient(diag4([F(1) if i == p else F(0) for i in range(4)]))
           == _zero(2, 2) for p in kernel_positions),
       "the quotient kernel must contain the second-index-1 diagonal units")

    # Negative control: genuinely non-commuting 2x2 witnesses embedded WITHOUT
    # the tensor split (both into the same top-left corner of M4).
    nilp_up = [[F(0), F(1)], [F(0), F(0)]]
    nilp_dn = [[F(0), F(0)], [F(1), F(0)]]

    def corner_embed(m2: Matrix) -> Matrix:
        out = _zero(4, 4)
        for i in range(2):
            for j in range(2):
                out[i][j] = m2[i][j]
        return out

    ea_bad = corner_embed(nilp_up)
    eb_bad = corner_embed(nilp_dn)
    control_fails = not _eq(_mm(ea_bad, eb_bad), _mm(eb_bad, ea_bad))
    ck(control_fails,
       "computed: the corner-embedded non-commuting pair must FAIL the commutation leg")

    return _result(
        "T_composite_tensor_quotient",
        "P_math",
        ("Commuting subsystem embeddings induce a surjective *-homomorphism "
         "from the algebraic tensor product onto the generated physical "
         "composite.  Executed here on the diagonal subalgebra D4 of M4 as "
         "C^2 (x) C^2: commutation, unitality, injectivity, and rank-4 "
         "generation of the tensor-split embeddings are computed exactly, the "
         "corner conditional expectation D4 -> D2 is verified unital, "
         "multiplicative, and surjective with the second-index-1 units in its "
         "kernel, and a corner-embedded non-commuting pair is computed to fail "
         "the commutation leg.  Tensor faithfulness is needed only to make the "
         "quotient injective; a constrained or superselected quotient remains "
         "an ordinary finite-dimensional quantum algebra."),
        ["T_held_to_observable_descent_criterion"],
        {
            "algebra": "diagonal subalgebra D4 of M4 as C^2 (x) C^2",
            "unconstrained_tensor_dimension": 4,
            "physical_composite_dimension": 2,
            "commutation_verified": True,
            "commutation_cases": commutation_cases,
            "unital": True,
            "injective": True,
            "generation_rank": generation_rank,
            "quotient_map": "corner conditional expectation onto second index = 0",
            "quotient_multiplicative": True,
            "quotient_multiplicativity_cases": quotient_mult_cases,
            "quotient_surjective": True,
            "quotient_kernel_positions": kernel_positions,
            "kernel_dimension": 2,
            "noncommuting_control_fails_commutation": control_fails,
            "tensor_faithful": False,
            "quantum_composite_still_valid": True,
        },
        fails,
        premises=(
            "commuting_unital_subsystem_embeddings",
            "generated_physical_composite",
            "orientation_synchronized_embeddings_across_typed_sectors",
        ),
        negative_controls=(
            "the corner quotient has a nonzero kernel (second-index-1 units)",
            "a corner-embedded non-commuting pair fails the commutation leg (computed)",
        ),
        cross_refs=("Paper 5 Q4C",),
    )


def check_T_held_to_observable_descent_criterion() -> Dict[str, object]:
    """Exact criterion separating naturality from complex module closure.

    Commutation with J alone only makes the represented algebra real-linear and
    J-compatible.  Invariance under left multiplication by J (equivalently,
    unital module closure) puts J inside the represented algebra and makes it a
    central complex scalar.
    """
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    i2 = _eye(2)
    j = [[F(0), F(-1)], [F(1), F(0)]]
    ck(_eq(_mm(j, j), _scal(F(-1), i2)), "J must square to -I")

    samples: List[Matrix] = []
    for a, b in product(range(-3, 4), repeat=2):
        x = [[F(a), F(-b)], [F(b), F(a)]]
        samples.append(x)
        ck(_eq(_mm(x, j), _mm(j, x)), "complex-linear samples must commute with J")
        jx = _mm(j, x)
        # JX has complex form with parameters (-b,a).
        expected = [[F(-b), F(-a)], [F(a), F(-b)]]
        ck(_eq(jx, expected), "the complex-linear algebra must be closed under J multiplication")

    # Negative control: R.I commutes with J but is not closed under J multiplication.
    real_scalar_samples = [_scal(F(a), i2) for a in range(-3, 4)]
    commutes_only = all(_eq(_mm(x, j), _mm(j, x)) for x in real_scalar_samples)
    contains_j = any(_eq(x, j) for x in real_scalar_samples)
    ck(commutes_only, "real scalars must commute with J")
    ck(not contains_j, "commutation alone must not put J in the represented algebra")

    return _result(
        "T_held_to_observable_descent_criterion",
        "P_math",
        ("A faithful represented real algebra becomes complex at the Held-to-"
         "observable seam only when it is a unital module over the transported "
         "quarter-turn: J A is contained in A.  Naturality/commutation alone is "
         "insufficient.  Under module closure, J=J1 lies in the algebra, is "
         "central, and squares to -I."),
        [
            "T_canonical_readout_quotient",
            "T_held_circle_quarter_turn",
            "T_held_jet_naturality",
        ],
        {
            "J": _matrix_strings(j),
            "complex_linear_samples_checked": len(samples),
            "module_closed": True,
            "commutation_only_negative_control": "R.I",
            "commutation_only_contains_J": contains_j,
        },
        fails,
        premises=(
            "faithful_action_of_the_Q2_observable_envelope_on_the_Held_carrier",
            "represented_generators_are_Held_morphisms",
            "J_module_closure_of_the_represented_observable_envelope",
            "common_phase_record_nullity",
            "generator_completeness_of_the_represented_observable_envelope",
            "finite_real_Cstar_classification_of_the_descended_algebra",
        ),
        negative_controls=(
            "the real scalar algebra R.I commutes with J but does not contain J",
        ),
        cross_refs=("Paper 5 Q4 Held-to-observable bridge",),
    )


def check_T_same_type_reference_chosen_cp() -> Dict[str, object]:
    """Choi/CP certificate with a computed partial transpose.

    Definition: an *extension-sound process* is a process whose Choi-corner
    extension exists and preserves positivity -- its local action extends as
    the identity on the maintained same-type reference with the joint positive
    cone preserved.
    """
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    # Bell density COMPUTED from the (unnormalized) bell vector (1,0,0,1):
    # rho = |phi+><phi+| = v v^T / 2 in basis 00,01,10,11.
    bell_vec: Vector = [F(1), F(0), F(0), F(1)]
    bell: Matrix = [[bell_vec[i] * bell_vec[j] / 2 for j in range(4)]
                    for i in range(4)]
    ck(sum(bell[i][i] for i in range(4)) == 1, "the Bell density must be normalized")

    # Partial transpose COMPUTED on the second factor and matched against the
    # audited matrix.
    pt = _partial_transpose(bell, 2, 2)
    pt_expected: Matrix = [
        [F(1, 2), F(0), F(0), F(0)],
        [F(0), F(0), F(1, 2), F(0)],
        [F(0), F(1, 2), F(0), F(0)],
        [F(0), F(0), F(0), F(1, 2)],
    ]
    ck(_eq(pt, pt_expected),
       "the computed partial transpose must match the audited matrix")

    # Exact negative-eigendirection witness.  The unnormalized vector
    # v = (0,1,-1,0) is an exact eigenvector of pt with eigenvalue -1/2
    # (no square roots needed), and its quadratic form is strictly negative.
    antisym: Vector = [F(0), F(1), F(-1), F(0)]
    ck(_mv(pt, antisym) == [F(-1, 2) * x for x in antisym],
       "pt v must equal -v/2 exactly: the -1/2 eigendirection is exhibited")
    negative_witness = _dot(antisym, _mv(pt, antisym))
    ck(negative_witness == -1 and negative_witness < 0,
       "the 2x2 same-type reference must expose the transpose map as non-CP")

    # (The former single-system transpose-positivity leg was vacuous: on real
    # symmetric samples vv^T the transpose is the identity map.  Replaced by
    # executed Choi computations below.)

    def _choi(chan: Callable[[Matrix], Matrix]) -> Matrix:
        c = _zero(4, 4)
        for i in range(2):
            for j in range(2):
                e_ij = [[F(1) if (r, s) == (i, j) else F(0) for s in range(2)]
                        for r in range(2)]
                out = chan(e_ij)
                for a in range(2):
                    for b in range(2):
                        c[i * 2 + a][j * 2 + b] = out[a][b]
        return c

    # Positive arm 1: the identity channel on M2 is CP -- its computed Choi
    # matrix is the (unnormalized) Bell density, certified PSD by the exact
    # all-principal-minors computation on the 4x4.
    choi_id = _choi(lambda x: x)
    ck(_eq(choi_id, [[bell_vec[i] * bell_vec[j] for j in range(4)]
                     for i in range(4)]),
       "the identity-channel Choi matrix must be the scaled Bell density")
    ck(_psd_by_principal_minors(choi_id),
       "the identity-channel Choi matrix must be exactly PSD")

    # Positive arm 2: the dephasing channel diag(.) is CP -- its computed Choi
    # matrix is diag(1,0,0,1), certified PSD the same way.
    def deph(x: Matrix) -> Matrix:
        return [[x[i][j] if i == j else F(0) for j in range(2)] for i in range(2)]

    choi_deph = _choi(deph)
    ck(_eq(choi_deph, [[F(1) if i == j and i in (0, 3) else F(0)
                        for j in range(4)] for i in range(4)]),
       "the dephasing Choi matrix must be diag(1,0,0,1)")
    ck(_psd_by_principal_minors(choi_deph),
       "the dephasing Choi matrix must be exactly PSD")

    # Corroboration: the transpose channel's computed Choi matrix (the swap)
    # fails the same exact PSD certificate.
    choi_transpose = _choi(_transpose)
    ck(not _psd_by_principal_minors(choi_transpose),
       "the transpose-channel Choi matrix must fail the exact PSD certificate")

    return _result(
        "T_same_type_reference_chosen_cp",
        "P_math",
        ("For each used input block M_n(C), an independently maintained same-type "
         "reference is Choi-complete only when the physical composite contains "
         "a tensor-faithful full positive Choi corner and the local operation "
         "extends as identity while preserving its joint positive cone (an "
         "extension-sound process: its Choi-corner extension exists and "
         "preserves positivity).  One whole-system reference may supply all "
         "blockwise corners.  Executed here: the Bell density is built from "
         "the bell vector, its partial transpose is computed and carries the "
         "exact -1/2 eigendirection (0,1,-1,0), the identity and dephasing "
         "channels are certified CP by exact all-principal-minors PSD "
         "computations on their computed 4x4 Choi matrices, and the transpose "
         "channel's Choi matrix fails the same certificate."),
        ["T_composite_tensor_quotient"],
        {
            "bell_vector": [str(x) for x in bell_vec],
            "bell_state": _matrix_strings(bell),
            "partial_transpose": _matrix_strings(pt),
            "partial_transpose_computed_from_bell": True,
            "eigenvalue_minus_half_witnessed": True,
            "negative_vector": [str(x) for x in antisym],
            "negative_quadratic_value": str(negative_witness),
            "choi_identity_channel": _matrix_strings(choi_id),
            "choi_identity_psd": True,
            "choi_dephasing_channel": _matrix_strings(choi_deph),
            "choi_dephasing_psd": True,
            "choi_transpose_channel": _matrix_strings(choi_transpose),
            "choi_transpose_not_psd": True,
        },
        fails,
        premises=(
            "independently_maintained_same_type_reference",
            "tensor_faithful_Choi_corner",
            "local_identity_extension",
            "joint_positive_state_preservation",
        ),
        negative_controls=(
            "matrix transpose is positive but not completely positive: its "
            "partial extension has the exact eigenvalue -1/2 on (0,1,-1,0) and "
            "its Choi matrix fails the exact PSD certificate",
        ),
        cross_refs=("Choi theorem", "Paper 5 Q5"),
    )


CORE_DEPENDENCIES: Dict[str, Tuple[str, ...]] = {
    "ORDERED_SCORE_SELF_DUAL_LEDGER": (
        "COMPLETED_ORDERED_SCORE",
        "BOUNDARY_ROLE_ISOMORPHISM",
        "FAITHFUL_NONNEGATIVE_DIAGONAL_SCORE",
    ),
    "TYPE_CORRECT_READOUT_BRIDGE": (
        "STRONG_CONTEXTUAL_CONGRUENCE",
        "DECLARED_CLOSED_BOUNDARY_ALGEBRA",
        "FULL_INVOLUTIVE_QUOTIENT",
        "COMPLETED_RECORD_CONTEXT_TOTALITY",
        "LINEAR_SCORE_SEPARATION",
        "CERTAIN_EFFECT_DISCARD_TYPING",
        "PHYSICAL_READOUT_REALIZATION",
        "ORDER_SOUND_READOUTS",
    ),
    "HELD_NATURAL_COMPLEX_ORIENTATION": (
        # Re-billed 2026-07-20 to the installed held-holonomy granularity.
        # GENERATOR_NATURALITY is SPLIT: the naturality half lives here as
        # JET_NATURALITY; the completeness half is gated at descent.
        "ORDERED_SCORE_SELF_DUAL_LEDGER",
        "OCCUPIED_SMOOTH_RECOMBINING_HELD_GERM",
        "COHERENT_LOOP_REVERSAL",
        "REVERSAL_IS_INVERSE",
        "Q2_LEDGER_ADJOINT",
        "FAITHFUL_ACTION",
        "EFFECTIVE_IMAGE_LIE_SUBGROUP",
        "TRIVIAL_ORIENTATION_MONODROMY",
        "JET_NATURALITY",
    ),
    "HELD_TO_OBSERVABLE_DESCENT": (
        "HELD_NATURAL_COMPLEX_ORIENTATION",
        "TYPE_CORRECT_READOUT_BRIDGE",
        "REPRESENTED_HELD_GENERATORS_ACT_ON_OBSERVABLE_CARRIER",
        "J_MODULE_CLOSURE_OF_OBSERVABLE_ENVELOPE",
        "COMMON_PHASE_RECORD_NULLITY",
        # Centrality gates (held-holonomy granularity):
        "GENERATOR_COMPLETENESS",
        "FINITE_REAL_CSTAR_CLASSIFICATION",
    ),
    "FINITE_FRAGMENT_KINEMATIC_SOUNDNESS": (
        "FINITE_PROTOCOL_FRAGMENT",
        "ORDERED_SCORE_SELF_DUAL_LEDGER",
        "TYPE_CORRECT_READOUT_BRIDGE",
        "HELD_TO_OBSERVABLE_DESCENT",
    ),
    "DENSITY_REPRESENTATION": (
        "FINITE_FRAGMENT_KINEMATIC_SOUNDNESS",
        "POSITIVE_OPERATOR_SYSTEM_STATE",
    ),
    "POVM_SOUNDNESS": (
        "FINITE_FRAGMENT_KINEMATIC_SOUNDNESS",
        "MEASUREMENT_NORMALIZATION",
    ),
    "COMPOSITE_SOUNDNESS": (
        "FINITE_FRAGMENT_KINEMATIC_SOUNDNESS",
        "COMMUTING_UNITAL_SUBSYSTEM_EMBEDDINGS",
        "GENERATED_PHYSICAL_COMPOSITE",
        "ORIENTATION_SYNCHRONIZED_EMBEDDINGS",
    ),
    "CP_SOUNDNESS": (
        "FINITE_FRAGMENT_KINEMATIC_SOUNDNESS",
        "CHOI_FAITHFUL_SAME_TYPE_REFERENCE",
        "TENSOR_FAITHFUL_CHOI_CORNER",
        "LOCAL_IDENTITY_EXTENSION",
        "JOINT_POSITIVITY_PRESERVATION",
    ),
    "FINITE_FRAGMENT_QUANTUM_SOUNDNESS": (
        "DENSITY_REPRESENTATION",
        "POVM_SOUNDNESS",
        "COMPOSITE_SOUNDNESS",
        "CP_SOUNDNESS",
        "NORMALIZATION_ACCOUNTING",
    ),
    "GLOBAL_FINITE_MATRIX_COLLAPSE": (
        "FINITE_FRAGMENT_QUANTUM_SOUNDNESS",
        "COMPATIBLE_GLOBAL_REFINEMENT",
        "UNIFORM_FINITE_OPERATIONAL_RANK",
    ),
    "FULL_TENSOR_EQUALITY": (
        "COMPOSITE_SOUNDNESS",
        "TENSOR_FAITHFULNESS",
    ),
    "EFFECT_SATURATION": ("FINITE_FRAGMENT_KINEMATIC_SOUNDNESS", "ALL_POSITIVE_EFFECTS_REALIZABLE"),
    "STATE_SATURATION": ("DENSITY_REPRESENTATION", "ALL_DENSITIES_PREPARABLE"),
    "MEASUREMENT_SATURATION": ("POVM_SOUNDNESS", "ALL_POVMS_IMPLEMENTABLE"),
    "PROCESS_SATURATION": ("CP_SOUNDNESS", "ALL_COMPATIBLE_CP_MAPS_REALIZABLE"),
    # Explicit quarantined orphan: named in the graph with empty deps so the
    # reverse-saturation fence polices a real node, and nothing consumes it.
    "PHYSICAL_REVERSE_SATURATION": (),
}

# --- (g) QGC <-> held_holonomy premise reconciliation (installed vocabulary) ---
PREMISE_RECONCILIATION: Dict[str, str] = {
    "FAITHFUL_NONNEGATIVE_DIAGONAL_SCORE": "positive_quadratic_ledger_form",
    "Q2_LEDGER_ADJOINT": "Q2_reversal_is_ledger_adjoint",
    "REVERSAL_IS_INVERSE": "reversed_loop_is_inverse",
    "FAITHFUL_ACTION": "faithful_first_order_action",
    "EFFECTIVE_IMAGE_LIE_SUBGROUP": "effective_image_is_a_Lie_subgroup_of_SO2",
    "GENERATOR_COMPLETENESS": "generator_completeness",
    "FINITE_REAL_CSTAR_CLASSIFICATION": "finite_real_Cstar_completion",
    "ORIENTATION_SYNCHRONIZED_EMBEDDINGS": "orientation_synchronization_across_typed_sectors",
    "JET_NATURALITY": "jet_functoriality",
}


def _complete_graph(graph: Mapping[str, Sequence[str]]) -> Dict[str, Tuple[str, ...]]:
    out = {k: tuple(v) for k, v in graph.items()}
    for deps in graph.values():
        for dep in deps:
            out.setdefault(dep, ())
    return out


def _find_cycle(graph: Mapping[str, Sequence[str]]) -> Optional[Tuple[str, ...]]:
    g = _complete_graph(graph)
    visiting: List[str] = []
    done = set()

    def dfs(node: str) -> Optional[Tuple[str, ...]]:
        if node in visiting:
            i = visiting.index(node)
            return tuple(visiting[i:] + [node])
        if node in done:
            return None
        visiting.append(node)
        for d in g[node]:
            c = dfs(d)
            if c:
                return c
        visiting.pop()
        done.add(node)
        return None

    for n in g:
        c = dfs(n)
        if c:
            return c
    return None


def _depends_on(graph: Mapping[str, Sequence[str]], start: str, target: str) -> bool:
    g = _complete_graph(graph)
    seen = set()
    stack = [start]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        for d in g.get(n, ()):
            if d == target:
                return True
            stack.append(d)
    return False


def check_T_quantum_gap_reclassification_contract() -> Dict[str, object]:
    fails: List[str] = []

    def ck(cond: bool, msg: str) -> None:
        if not cond:
            fails.append(msg)

    cycle = _find_cycle(CORE_DEPENDENCIES)
    ck(cycle is None, "the canonical soundness/saturation dependency graph must be acyclic")

    optional = (
        "EFFECT_SATURATION", "STATE_SATURATION", "MEASUREMENT_SATURATION",
        "PROCESS_SATURATION", "FULL_TENSOR_EQUALITY", "GLOBAL_FINITE_MATRIX_COLLAPSE",
    )
    for node in optional:
        ck(not _depends_on(CORE_DEPENDENCIES, "FINITE_FRAGMENT_QUANTUM_SOUNDNESS", node),
           f"core soundness must not consume optional node {node}")

    ck(_depends_on(CORE_DEPENDENCIES, "CP_SOUNDNESS", "CHOI_FAITHFUL_SAME_TYPE_REFERENCE"),
       "CP soundness must declare the Choi-faithful same-type reference premise")
    ck(not _depends_on(CORE_DEPENDENCIES, "FINITE_FRAGMENT_QUANTUM_SOUNDNESS",
                       "PHYSICAL_REVERSE_SATURATION"),
       "general physical reverse saturation must not be load-bearing")
    ck(_depends_on(CORE_DEPENDENCIES, "HELD_NATURAL_COMPLEX_ORIENTATION",
                   "ORDERED_SCORE_SELF_DUAL_LEDGER"),
       "the Held circle must consume the independently established ledger")
    ck(not _depends_on(CORE_DEPENDENCIES, "ORDERED_SCORE_SELF_DUAL_LEDGER",
                       "HELD_NATURAL_COMPLEX_ORIENTATION"),
       "the ledger must not be derived from the Held circle")
    ck(_depends_on(CORE_DEPENDENCIES, "FINITE_FRAGMENT_QUANTUM_SOUNDNESS",
                   "HELD_TO_OBSERVABLE_DESCENT"),
       "finite-fragment soundness must declare the Held-to-observable bridge")

    # Contract tripwires at the installed held-holonomy granularity.
    ck(_depends_on(CORE_DEPENDENCIES, "HELD_NATURAL_COMPLEX_ORIENTATION",
                   "REVERSAL_IS_INVERSE"),
       "the Held orientation must declare reversal-is-inverse: reversal "
       "admission alone yields only a monoid")
    ck(_depends_on(CORE_DEPENDENCIES, "HELD_TO_OBSERVABLE_DESCENT",
                   "GENERATOR_COMPLETENESS"),
       "descent must declare the generator-completeness centrality gate")
    ck(_depends_on(CORE_DEPENDENCIES, "HELD_TO_OBSERVABLE_DESCENT",
                   "FINITE_REAL_CSTAR_CLASSIFICATION"),
       "descent must declare the finite real C*-classification centrality gate")
    ck(_depends_on(CORE_DEPENDENCIES, "COMPOSITE_SOUNDNESS",
                   "ORIENTATION_SYNCHRONIZED_EMBEDDINGS"),
       "composite soundness must declare orientation synchronization across embeddings")
    ck(_depends_on(CORE_DEPENDENCIES, "DENSITY_REPRESENTATION",
                   "POSITIVE_OPERATOR_SYSTEM_STATE"),
       "density representation must declare the positive operator-system state")
    # Negative tripwires: naturality-only names must not smuggle generator
    # completeness anywhere in their ancestry.
    naturality_only_nodes = sorted(
        node for node in _complete_graph(CORE_DEPENDENCIES) if "NATURALITY" in node
    )
    ck("JET_NATURALITY" in naturality_only_nodes,
       "the split naturality node must be present in the graph")
    for node in naturality_only_nodes:
        ck(not _depends_on(CORE_DEPENDENCIES, node, "GENERATOR_COMPLETENESS"),
           f"naturality-only node {node} must not carry generator completeness")
    ck(not _depends_on(CORE_DEPENDENCIES, "HELD_NATURAL_COMPLEX_ORIENTATION",
                       "GENERATOR_COMPLETENESS"),
       "the orientation node consumes naturality only; completeness is gated at descent")
    # Quarantined orphan: present, explicit, empty deps, consumed by nothing.
    ck(CORE_DEPENDENCIES.get("PHYSICAL_REVERSE_SATURATION") == (),
       "PHYSICAL_REVERSE_SATURATION must be an explicit empty-deps orphan node")
    ck(all("PHYSICAL_REVERSE_SATURATION" not in deps
           for node, deps in CORE_DEPENDENCIES.items()),
       "no node may consume the quarantined reverse-saturation orphan")
    ck(len(PREMISE_RECONCILIATION) >= 9,
       "the QGC/held-holonomy premise reconciliation must carry all nine rows")

    mutated = dict(CORE_DEPENDENCIES)
    mutated["ORDERED_SCORE_SELF_DUAL_LEDGER"] = ("HELD_NATURAL_COMPLEX_ORIENTATION",)
    mutated_cycle = _find_cycle(mutated)
    ck(mutated_cycle is not None, "a ledger-from-quantum-soundness cycle must be detected")

    return _result(
        "T_quantum_gap_reclassification_contract",
        "P_structural_instrument",
        ("The finite-fragment theorem is dependency-independent of uniform "
         "global rank, full effect/state/measurement availability, full tensor "
         "equality, and process saturation.  It explicitly retains the physical "
         "ordered-score/self-duality bridge, type-correct readout bridge, "
         "Held-to-observable descent, generated composite embeddings, and the "
         "Choi-faithful reference gate.  Re-billed to the installed "
         "held-holonomy granularity: the Held orientation declares reversal-"
         "is-inverse, the Q2 ledger adjoint, faithful action, the Lie-image "
         "gate, and jet naturality (the naturality half of the former "
         "GENERATOR_NATURALITY); generator completeness and the finite real "
         "C*-classification gate descent, not orientation; composite soundness "
         "declares orientation-synchronized embeddings; physical reverse "
         "saturation is an explicit quarantined orphan the fence polices.  The "
         "Held circle consumes the ledger, while a ledger-from-Held mutation "
         "is machine-rejected."),
        [
            "T_finite_protocol_fragment_rank",
            "T_ordered_score_bilinearization",
            "T_dual_action_without_physical_reverse_saturation",
            "T_canonical_readout_quotient",
            "T_effect_soundness_not_saturation",
            "T_operator_system_state_extension",
            "T_composite_tensor_quotient",
            "T_held_to_observable_descent_criterion",
            "T_same_type_reference_chosen_cp",
        ],
        {
            "dependency_contract": {k: list(v) for k, v in CORE_DEPENDENCIES.items()},
            "canonical_cycle": cycle,
            "ledger_cycle_mutation_detected": mutated_cycle is not None,
            "ledger_cycle_mutation": list(mutated_cycle) if mutated_cycle else None,
            "held_consumes_ordered_score_ledger": True,
            "ledger_depends_on_held": False,
            "held_to_observable_descent_declared": True,
            "general_physical_reverse_saturation_load_bearing": False,
            "reversal_is_inverse_declared_at_orientation": True,
            "generator_completeness_gates_descent": True,
            "finite_real_cstar_classification_gates_descent": True,
            "orientation_synchronization_gates_composite": True,
            "physical_reverse_saturation_quarantined_orphan": True,
            "naturality_only_nodes": naturality_only_nodes,
            "premise_reconciliation": dict(PREMISE_RECONCILIATION),
            "optional_saturation_nodes": list(optional),
        },
        fails,
        premises=(
            "finite_fragment_protocol_typing",
            "ordered_score_additivity",
            "order_sound_readouts",
            "held_natural_complex_orientation",
        ),
        negative_controls=(
            "ORDERED_SCORE_SELF_DUAL_LEDGER <- HELD_NATURAL_COMPLEX_ORIENTATION cycle mutation",
        ),
        cross_refs=("Paper 5 Q1-Q5", "Paper 33 dependency-certificate discipline"),
    )


_CHECKS: Dict[str, Callable[[], Dict[str, object]]] = {
    "T_finite_protocol_fragment_rank": check_T_finite_protocol_fragment_rank,
    "T_ordered_score_bilinearization": check_T_ordered_score_bilinearization,
    "T_dual_action_without_physical_reverse_saturation": check_T_dual_action_without_physical_reverse_saturation,
    "T_canonical_readout_quotient": check_T_canonical_readout_quotient,
    "T_effect_soundness_not_saturation": check_T_effect_soundness_not_saturation,
    "T_operator_system_state_extension": check_T_operator_system_state_extension,
    "T_composite_tensor_quotient": check_T_composite_tensor_quotient,
    "T_held_to_observable_descent_criterion": check_T_held_to_observable_descent_criterion,
    "T_same_type_reference_chosen_cp": check_T_same_type_reference_chosen_cp,
    "T_quantum_gap_reclassification_contract": check_T_quantum_gap_reclassification_contract,
}


def register(registry: Dict[str, object]) -> Dict[str, object]:
    registry.update(_CHECKS)
    return registry


def run_all() -> Dict[str, Dict[str, object]]:
    return {name: fn() for name, fn in _CHECKS.items()}


def build_certificate(results: Optional[Mapping[str, Mapping[str, object]]] = None) -> FrontendClosureCertificate:
    rs = dict(results) if results is not None else run_all()

    def passed(name: str) -> bool:
        return bool(rs[name]["passed"])

    return FrontendClosureCertificate(
        finite_fragment_rank=passed("T_finite_protocol_fragment_rank"),
        ordered_score_bilinearization=passed("T_ordered_score_bilinearization"),
        dual_action_without_reverse_saturation=passed("T_dual_action_without_physical_reverse_saturation"),
        canonical_readout_quotient=passed("T_canonical_readout_quotient"),
        effect_soundness_separated_from_saturation=passed("T_effect_soundness_not_saturation"),
        operator_system_density_extension=passed("T_operator_system_state_extension"),
        composite_tensor_quotient=passed("T_composite_tensor_quotient"),
        held_to_observable_descent_criterion=passed("T_held_to_observable_descent_criterion"),
        same_type_reference_cp_test=passed("T_same_type_reference_chosen_cp"),
        dependency_contract_acyclic=passed("T_quantum_gap_reclassification_contract"),
        physical_premises_certified=False,
        core_scope=(
            "finite protocol fragments: complex quantum soundness for actual states, "
            "effects, measurements, composites, and extension-sound processes"
        ),
        remaining_physical_kernel=(
            "completed_ordered_score_boundary_role_isomorphism_and_faithful_diagonal",
            "type_correct_readout_quotient_boundary_architecture_context_totality_score_separation_certain_effect_physical_realization_and_order_soundness",
            "occupied_natural_Held_realization_and_Held_to_observable_descent",
            "commuting_unital_subsystem_embeddings_generating_each_used_composite",
            "blockwise_Choi_faithful_same_type_reference_tensor_corners_local_identity_extension_joint_positivity_and_normalization_for_CP",
            "compatible_global_refinement_only_if_one_nonfragmentary_algebra_is_claimed",
        ),
        optional_saturation_claims=(
            "uniform_global_finite_rank",
            "all_positive_effects_realizable",
            "all_density_operators_preparable",
            "all_POVMs_implementable",
            "tensor_faithfulness",
            "all_compatible_CP_instruments_realizable",
        ),
    )


IE_DECLARATIONS = (
    {
        "input_id": "quantum:frontend_closure_conditional_certificate",
        "axis": "ROUTE",
        "route": "quantum_frontend_gap_closure",
        "expect_export": False,
        "payload": {
            "name": "frontend_closure_conditional_certificate",
            "closure_kind": "obstruction_named",
            "obstruction_class": "QUANTUM_FRONTEND_PHYSICAL_PREMISES_REQUIRED",
            "source_checks": list(_CHECKS),
            "open_obligations": [
                "completed_ordered_score_boundary_role_isomorphism_and_faithful_diagonal",
                "type_correct_readout_quotient_boundary_architecture_context_totality_score_separation_certain_effect_physical_realization_and_order_soundness",
                "occupied_natural_Held_realization_and_Held_to_observable_descent",
                "commuting_unital_subsystem_embeddings_generating_each_used_composite",
                "blockwise_Choi_faithful_same_type_reference_tensor_corners_local_identity_extension_joint_positivity_and_normalization_for_CP",
                "compatible_global_refinement_only_if_one_nonfragmentary_algebra_is_claimed",
            ],
            "knockout_summary": (
                "The finite fragment soundness schemas pass: bilinearization "
                "with the executed Jordan-von Neumann leg, dual action, "
                "readout quotient with executed congruence, effect/state "
                "soundness, composite tensor quotient with executed "
                "commutation, Held-to-observable descent, Choi-corner CP with "
                "computed partial transpose, and the reclassification "
                "contract at held-holonomy granularity. The physical front "
                "end remains conditional on the named premise package; "
                "physical_premises_certified=false."
            ),
            "target_value_consumed": False,
        },
        "note": (
            "Conditional Paper-5 front-end certificate. Soundness is "
            "separated from optional saturation; the named physical premise "
            "package is required before any export."
        ),
    },
)

if __name__ == "__main__":
    import json
    import sys

    results = run_all()
    cert = build_certificate(results)
    payload = {
        "module": "quantum_frontend_closure_v0_2",
        "family": FAMILY,
        "check_count": len(results),
        "checks": {name: ("PASS" if r["passed"] else "FAIL") for name, r in results.items()},
        "all_pass": all(bool(r["passed"]) for r in results.values()),
        "certificate": asdict(cert),
    }
    print(json.dumps(payload, indent=2, sort_keys=True))
    sys.exit(0 if payload["all_pass"] else 1)
