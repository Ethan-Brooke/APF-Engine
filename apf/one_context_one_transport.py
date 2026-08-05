"""One capacity frame plus one natural transport: the unistochastic criterion
for when the transport forces the trace.

UNREGISTERED -- this module ships without a register() entry point, pending its
blinded audit.  No manifest change, no EXPECTED change.  It supersedes the
mathematical content of the held predecessor (one_context_one_transport_HELD)
under the 2026-08-04 plain-shape design ruling: the mathematics enters the
corpus as an ordinary module; the bank's own battery and future audits are the
verification story, the same as for every other banked module.

SETTING.  A capacity frame E on C^n is the set of rank-one projectors onto an
orthonormal basis (the capacity basis).  A cost functional is a Hermitian R.
The two premises, for one unitary transport U:

  (i)  UNIFORM FRAME COST, ONE GLOBAL eps:  R_ii = eps for every i.
  (ii) NATURALITY:  U* R U = R.

A SURVIVOR is a Hermitian K with zero diagonal and U* K U = K.  Premises
(i) + (ii) hold exactly when R = eps I + K with K a survivor, so the whole
question is whether the survivor space is zero.  FORCING means: every R
satisfying (i) and (ii) is a real multiple of the identity -- a statement
QUANTIFIED OVER R.

THE CRITERION (check_T_unistochastic_overlap_criterion, tier 4, [P_math]).
Let U have eigenbasis V (columns) and let B_ik = |V_ik|^2 be the unistochastic
overlap matrix of the eigenbasis with the capacity basis; B is doubly
stochastic.  When U has simple spectrum, the commutant Comm(U)_sa is
parametrized by the real eigen-coefficients p, and the restricted diagonal
conditional expectation D_E acts on it as p |-> B p.  Then

  FORCING  <=>  U has simple spectrum  AND  det B != 0,

and on the simple-spectrum side dim(survivors) = nullity(B).  Both directions
are computed on structured exact families (identity, rational rotations, a
non-symmetric rational orthogonal basis, Fourier/shift, diagonal phases,
degenerate transports) and on 100 seeded Haar samples at n = 2..5 under a
stated float tolerance.

STATEMENTS (full statements in the check docstrings).

  (a) check_L_premises_reduce_to_survivor_space [P_math]: solution dimension
      = 1 + dim(survivors) on a four-member battery; the forced line is
      exhibited to BE R = eps I; each premise shown load-bearing.
  (b) check_T_unistochastic_overlap_criterion [P_math]: the criterion, both
      directions; overlap orientation (row index first) fixed by value on a
      non-symmetric witness; det B pinned exactly on every member; a
      12-member classification battery occupying all three quadrants; a
      100-sample seeded float control.
  (c) check_L_simple_spectrum_is_necessary [P_math]: dim Comm(U)_sa =
      sum m^2 (eight patterns, two conjugations); every partition of n <= 8
      has sum m^2 >= n, equality exactly at all-ones (66 partitions);
      dim(survivors) >= sum m^2 - n attained at diag(1,1,i) with survivors
      span{X_12, Y_12} and the positive definite non-scalar solution
      R = I + (3/10) X_12; at diag(1,1,i,i) the survivor dimension is 4 and
      the self-adjoint commutant dimension is 8 -- the 8 is the commutant.
  (d) check_L_diagonal_expectation_and_qubit_residual [P_math]: D_E is a
      conditional expectation (idempotent, unital, trace-preserving); for
      every non-scalar qubit transport, exactly at symbolic theta and phi,
      U*RU - R = [-2 sin^2(phi) r_perp - 2 cos(phi)sin(phi)(r x m)].sigma,
      vanishing iff r || m; det B = m_z, forced iff m_z != 0; the loose
      "residual proportional to r x m" reading exhibited false at phi=pi/2.
  (e) check_L_forcing_is_quantified_over_R [P_math] -- THE QUANTIFIER
      FENCE: eps I satisfies (i)+(ii) for EVERY transport; at the n = 2
      shift det B = 0 and the premise system is two-dimensional, non-scalar
      co-solution (7/4) I + (1/2) sigma_x exhibited.  The correct statement
      is FORCING, quantified over R -- not an iff at solvability.
  (f) check_L_mixing_is_not_monotone [P_math]: det B_s = (1-s)^(n-1) on the
      flat path; off it, an exact n = 3 pair (V1 = rot(pi/4) (+) 1,
      V2 = (1/3)[[2,2,-1],[-1,2,2],[2,-1,2]]) has every row of B2 majorized
      by the matching row of B1 AND the concatenated 9-vector majorized --
      more mixed under every Schur-concave measure -- yet det B1 = 0 with a
      survivor while det B2 = 1/9 and the trace is forced.
  (g) check_L_singular_B_survivors_are_positive [P_math]: cyclic shifts at
      n = 2,3,4: simple spectrum, B = J/n, det B = 0, n-1 survivors;
      eps I + tK positive definite on the symmetric radius
      |t| < eps/||K||_op, sharp as a two-sided radius; the n = 2 survivor
      is sigma_x and I + sigma_x/2
      (spectrum {1/2, 3/2}) is the banked prior-art control.  eps > 0 is a
      PREMISE: survivors are trace-free hence indefinite, Tr R = n eps.
  (h) check_L_det_B_genericity_and_conditioning [P_numerical_scope] --
      seeded Monte Carlo MEASUREMENTS, not theorems: seed 20260731, 4000
      Haar samples per n over n = 2,3,4,5,6,8; median |det B| falls 0.5018
      -> 1.243e-05 (factor 4.037e4) while median cond(B) grows only 1.993
      -> 34.30 (factor 17.21); at n = 8 EXACTLY 2 of 4000 samples sit at or
      above 1e-3.  det B is not identically zero (computed); the
      measure-zero fact for polynomial zero sets is CITED.  Nine GENERIC
      singular-B points located by bisection at n = 3,4,5 (seed 20260804):
      entries bounded away from zero, nullity(B) = 1, survivor dim 1.

WITHDRAWN CLAIMS -- fences, not results.  None of the following may be
asserted, cited, or re-derived from this module:

  1. "R = eps I is forced if and only if (a) and (b)", read as solvability.
     Mis-quantified and false: eps I solves the premises for every transport,
     the n = 2 shift included, where (b) fails.  The correct object is
     forcing, quantified over R (check (e)).
  2. "Mixing is a liability, and it is monotone."  Refuted by the exact
     n = 3 unistochastic pair in check (f): forcing fails at the LESS mixed
     matrix.  Monotonicity is a property of the flat path only.
  3. "Above n ~ 5 a typical transport sits near the failure locus" (the
     four-orders fragility wording).  The determinant's fall is a scale
     artifact of O(1/n) entries; the distance-to-failure statement is the
     conditioning, which degrades like 1/n -- a factor 17, not four orders
     (check (h)).

PRIOR-ART DELTA.  The CONCLUSION -- a natural functional is forced to the
trace -- is banked territory: check_T_presentation_gauge_forces_trace
(presentation_gauge_forcing.py) reaches psi = c*Tr from a presentation group
with scalar commutant, and atomic_equal_cost_frame banks the orbit-side route
through a spanning family of equal-cost rays.  THIS module's delta is the
CRITERION: the unistochastic overlap matrix, the commutant-intersection
criterion, simple-spectrum necessity via sum m^2, one-transport forcing
quantified over R, and the restricted diagonal conditional expectation.  None
of these was previously stated in the corpus (established by a semantic sweep
across the tree and Papers 5/14/40 during the predecessor's fourth audit).
No uniqueness-in-literature claim is made beyond the corpus.

MAY-NOT-CITE.

  - Any physical claim.  The premises -- that the capacity frame is physical,
    that a physical transport acts on the cost functional by naturality, and
    that one global eps prices the whole frame
    (COHERENT_TRANSPORT_COST_SCALAR_NATURALITY) -- are OPEN, and the last is
    a near neighbour of the conclusion.  The mathematics is exact and
    conditional; nothing here certifies a premise.
  - "Born is derived" / "the trace is derived from A1."  Nothing here.
  - The three withdrawn wordings above, in any paraphrase.
  - "det B != 0 is generic, therefore large-n applications are safe."  The
    genericity is measure-theoretic; any application at large n owes a
    quantitative conditioning margin (check (h)).
  - Positivity claims without the eps > 0 premise (check (g)).

NON-EXPORTING.  PHYSICAL_PREMISES_CERTIFIED = False.  No grade moved.
"""

from fractions import Fraction
from typing import Dict, List, Tuple

import sympy as sp
from sympy import I as _i

PHYSICAL_PREMISES_CERTIFIED = False
EXPORTS: Tuple[str, ...] = ()
BANK_MODIFIED = False

# ---------------------------------------------------------------------------
# exact linear algebra (sympy; no floating point on this path)
# ---------------------------------------------------------------------------

def _herm_basis(n: int) -> List[sp.Matrix]:
    """Real-linear basis of the Hermitian n x n matrices; dimension n^2."""
    out: List[sp.Matrix] = []
    for i in range(n):
        M = sp.zeros(n, n); M[i, i] = 1; out.append(M)
    for i in range(n):
        for j in range(i + 1, n):
            M = sp.zeros(n, n); M[i, j] = 1;   M[j, i] = 1;   out.append(M)   # X_ij
            M = sp.zeros(n, n); M[i, j] = -_i; M[j, i] = _i;  out.append(M)   # Y_ij
    return out


def _real_coords(M: sp.Matrix, n: int) -> List[sp.Expr]:
    c = [sp.re(sp.simplify(M[i, i])) for i in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            c.append(sp.re(sp.simplify(M[i, j])))
            c.append(sp.im(sp.simplify(M[i, j])))
    return c


def _naturality_matrix(U: sp.Matrix, n: int) -> sp.Matrix:
    """Real n^2 x n^2 matrix of X |-> U* X U - X on the Hermitian space."""
    B = _herm_basis(n)
    Ud = U.conjugate().T
    return sp.Matrix([_real_coords(sp.expand(Ud * b * U - b), n) for b in B]).T


def _diag_rows(n: int) -> sp.Matrix:
    B = _herm_basis(n)
    return sp.Matrix([[sp.re(sp.simplify(b[i, i])) for b in B] for i in range(n)])


def _commutant_sa_dim(U: sp.Matrix, n: int) -> int:
    """dim_R {X = X* : U* X U = X}."""
    return n * n - _naturality_matrix(U, n).rank()


def _survivor_space(U: sp.Matrix, n: int) -> List[sp.Matrix]:
    """A basis of {K = K* : U* K U = K, diag K = 0} -- the survivors."""
    A = sp.Matrix.vstack(_naturality_matrix(U, n), _diag_rows(n))
    B = _herm_basis(n)
    out = []
    for v in A.nullspace():
        M = sp.zeros(n, n)
        for k, b in enumerate(B):
            M = M + v[k] * b
        out.append(sp.expand(M))
    return out


def _survivor_dim(U: sp.Matrix, n: int) -> int:
    A = sp.Matrix.vstack(_naturality_matrix(U, n), _diag_rows(n))
    return n * n - A.rank()


def _frame_solution_space(U: sp.Matrix, n: int):
    """Solve the FULL premise system exactly, eps carried as an unknown.

    Unknowns: the n^2 real coordinates of Hermitian R plus one eps.  Rows:
    naturality U* R U = R and diag(R)_i = eps.  Returns (dim, basis) with
    basis entries (R matrix, eps value)."""
    HB = _herm_basis(n)
    ncoord = n * n
    rows: List[List[sp.Expr]] = []
    Nm = _naturality_matrix(U, n)
    for r in range(Nm.rows):
        rows.append([Nm[r, c] for c in range(ncoord)] + [sp.Integer(0)])
    Dg = _diag_rows(n)
    for i in range(n):
        rows.append([Dg[i, c] for c in range(ncoord)] + [sp.Integer(-1)])
    A = sp.Matrix(rows)
    ns = A.nullspace()
    basis = []
    for v in ns:
        M = sp.zeros(n, n)
        for k, b in enumerate(HB):
            M = M + v[k] * b
        basis.append((sp.expand(M), sp.simplify(v[ncoord])))
    return len(ns), basis


def _multiplicities(U: sp.Matrix) -> List[int]:
    return sorted((int(m) for m in U.eigenvals().values()), reverse=True)


def _overlap_matrix(V: sp.Matrix, n: int) -> sp.Matrix:
    """B_ik = |V_ik|^2 for V unitary -- ROW index first (fixed by value in
    check (b) on a non-symmetric witness)."""
    return sp.Matrix(n, n, lambda i, k: sp.expand(sp.Abs(V[i, k]) ** 2))


def _is_unitary(M: sp.Matrix, n: int) -> bool:
    D = sp.expand(M * M.conjugate().T - sp.eye(n))
    return D == sp.zeros(n, n) or sp.simplify(D) == sp.zeros(n, n)


def _cyclic_shift(n: int) -> sp.Matrix:
    return sp.Matrix(n, n, lambda i, j: 1 if (j - i) % n == 1 else 0)


def _fourier(n: int) -> sp.Matrix:
    w = sp.exp(2 * sp.pi * _i / n)
    return sp.Matrix(n, n,
                     lambda j, k: sp.expand(sp.expand_complex(w ** (j * k)))) / sp.sqrt(n)


def _rot(n, i, j, c, s):
    M = sp.eye(n); M[i, i] = c; M[j, j] = c; M[i, j] = -s; M[j, i] = s
    return M


def _eigs_exact(M: sp.Matrix) -> List[sp.Expr]:
    out = []
    for val, mult in M.eigenvals().items():
        out.extend([sp.nsimplify(sp.simplify(val))] * int(mult))
    return sorted(out, key=lambda z: (sp.re(z), sp.im(z)))


def _op_norm_herm(M: sp.Matrix) -> sp.Expr:
    return max((sp.Abs(v) for v in _eigs_exact(M)), key=lambda z: sp.nsimplify(z))


def _is_pos_def(M: sp.Matrix) -> bool:
    return all(sp.simplify(v) > 0 for v in _eigs_exact(M))


def _is_pos_semidef(M: sp.Matrix) -> bool:
    return all(sp.simplify(v) >= 0 for v in _eigs_exact(M))


def _in_span(M: sp.Matrix, basis: List[sp.Matrix]) -> bool:
    n = M.shape[0]
    cols = sp.Matrix([_real_coords(b, n) for b in basis]).T
    aug = cols.row_join(sp.Matrix(_real_coords(M, n)))
    return cols.rank() == aug.rank()


def _maj(row_small, row_big) -> bool:
    """row_small majorized by row_big: sorted partial sums never exceed,
    totals equal."""
    a = sorted((sp.nsimplify(x) for x in row_small), reverse=True)
    b = sorted((sp.nsimplify(x) for x in row_big), reverse=True)
    pa, pb = sp.Integer(0), sp.Integer(0)
    for k in range(len(a)):
        pa += a[k]; pb += b[k]
        if sp.simplify(pa - pb) > 0:
            return False
    return sp.simplify(pa - pb) == 0


# ---------------------------------------------------------------------------
# float helpers (numpy, pinned seeds; MEASUREMENTS, graded as such)
# ---------------------------------------------------------------------------

def _haar_np(rng, n):
    import numpy as np
    z = (rng.normal(size=(n, n)) + 1j * rng.normal(size=(n, n))) / np.sqrt(2)
    q, r = np.linalg.qr(z)
    return q * (np.diagonal(r) / np.abs(np.diagonal(r)))


def _surv_dim_float(U, tol=1e-8):
    import numpy as np
    n = U.shape[0]
    HB = []
    for a in range(n):
        E = np.zeros((n, n), complex); E[a, a] = 1; HB.append(E)
    for a in range(n):
        for b in range(a + 1, n):
            E = np.zeros((n, n), complex); E[a, b] = 1; E[b, a] = 1; HB.append(E)
            E = np.zeros((n, n), complex); E[a, b] = -1j; E[b, a] = 1j; HB.append(E)
    rows = []
    for h in HB:
        D = U.conj().T @ h @ U - h
        rows.append([np.real(np.trace(g.conj().T @ D)) / np.real(np.trace(g.conj().T @ g))
                     for g in HB])
    A = np.array(rows).T
    Dg = np.array([[np.real(h[a, a]) for h in HB] for a in range(n)])
    A = np.vstack([A, Dg])
    sv = np.linalg.svd(A, compute_uv=False)
    return A.shape[1] - int((sv > tol * max(1.0, sv[0])).sum())


_G4 = lambda x: float(f"{x:.4g}")   # 4 significant figures, for float pins


# ---------------------------------------------------------------------------
# result shape
# ---------------------------------------------------------------------------

def _result(name, tier, epistemic, legs, fails, key_result):
    for k, v in legs.items():
        if v is not True:
            fails.append(f"leg not True: {k}")
    return {
        "name": name, "passed": not fails, "legs": dict(legs),
        "fails": list(fails), "key_result": key_result,
        "tier": tier, "epistemic": epistemic,
        "physical_premises_certified": PHYSICAL_PREMISES_CERTIFIED,
    }


# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def check_L_premises_reduce_to_survivor_space():
    """(a) Premises (i)+(ii) are exactly R = eps I + K with K a survivor."""
    legs, fails = {}, []
    bat = [
        ("diagonal_phases_n3", sp.diag(1, _i, -1), 3),
        ("cyclic_shift_n3", _cyclic_shift(3), 3),
        ("degenerate_n3", sp.diag(1, 1, _i), 3),
        ("sigma_x_n2", sp.Matrix([[0, 1], [1, 0]]), 2),
    ]
    dims = []
    eps_ok = []
    for lab, U, n in bat:
        d_full, _ = _frame_solution_space(U, n)
        d_surv = _survivor_dim(U, n)
        dims.append((lab, d_full, d_surv))
        epsI = sp.eye(n) * sp.Rational(7, 3)
        eps_ok.append(
            _is_unitary(U, n)
            and sp.expand(U.conjugate().T * epsI * U - epsI) == sp.zeros(n, n)
            and all(sp.simplify(epsI[k, k] - sp.Rational(7, 3)) == 0 for k in range(n)))
    legs["solution_dim_is_one_plus_survivor_dim"] = (
        dims == [("diagonal_phases_n3", 1, 0), ("cyclic_shift_n3", 3, 2),
                 ("degenerate_n3", 3, 2), ("sigma_x_n2", 2, 1)]
        and all(d == 1 + s for _, d, s in dims))
    legs["eps_identity_satisfies_both_premises_everywhere"] = (
        eps_ok == [True, True, True, True])
    legs["forced_case_is_exactly_diagonal_phases"] = (
        sorted(lab for lab, _, s in dims if s == 0) == ["diagonal_phases_n3"])
    # the surviving line where forcing holds IS eps I, exhibited
    d1, basis1 = _frame_solution_space(sp.diag(1, _i, -1), 3)
    M1, eps1 = basis1[0]
    legs["forced_line_is_spanned_by_eps_identity"] = (
        d1 == 1 and sp.expand(M1 - eps1 * sp.eye(3)) == sp.zeros(3, 3)
        and sp.simplify(eps1) == 1)
    # premise (i) load-bearing: drop the frame, a non-scalar natural R survives
    Ud = sp.diag(1, _i, -1)
    Rnp = sp.diag(1, 2, 5)
    legs["premise_i_load_bearing"] = (
        sp.expand(Ud.conjugate().T * Rnp * Ud - Rnp) == sp.zeros(3, 3)
        and [str(Rnp[k, k]) for k in range(3)] == ["1", "2", "5"])
    # premise (ii) load-bearing: drop naturality, a non-scalar uniform R survives
    Rnn = sp.Matrix([[1, 1], [1, 1]])
    legs["premise_ii_load_bearing"] = (
        all(Rnn[k, k] == 1 for k in range(2))
        and [str(v) for v in _eigs_exact(Rnn)] == ["0", "2"]
        and Rnn != sp.eye(2))
    return _result("check_L_premises_reduce_to_survivor_space", 3, "P_math",
                   legs, fails,
                   {"battery_dims": dims,
                    "statement": "solution dim = 1 (the eps line) + dim(survivors)"})


def check_T_unistochastic_overlap_criterion():
    """(b) THE CRITERION: forcing <=> simple spectrum AND det B != 0;
    dim(survivors) = nullity(B) on the simple-spectrum side."""
    legs, fails = {}, []
    # V_asym: rational orthogonal with non-symmetric |V|^2 -- the battery
    # member on which B p and B^T p differ, and the orientation witness below
    V_asym = sp.Matrix([[2, 2, -1], [-1, 2, 2], [2, -1, 2]]) / 3
    Vs = [("identity_n3", sp.eye(3), 3),
          ("rational_rotation_n2", _rot(2, 0, 1, sp.Rational(3, 5), sp.Rational(4, 5)), 2),
          ("rational_rotation_n3", _rot(3, 0, 2, sp.Rational(5, 13), sp.Rational(12, 13)), 3),
          ("fourier_n2", _fourier(2), 2),
          ("fourier_n3", _fourier(3), 3),
          ("fourier_n4", _fourier(4), 4),
          ("asymmetric_n3", V_asym, 3)]
    LAMS = [sp.Integer(1), _i, sp.Integer(-1), -_i]

    ds_bad, de_bad = [], []
    table = []
    for lab, V, n in Vs:
        if not _is_unitary(V, n):
            ds_bad.append((lab, "not unitary"))
            continue
        B = _overlap_matrix(V, n)
        rowsums = [sp.simplify(sum(B[i, k] for k in range(n)) - 1) for i in range(n)]
        colsums = [sp.simplify(sum(B[i, k] for i in range(n)) - 1) for k in range(n)]
        nonneg = all(sp.simplify(B[i, k]) >= 0 for i in range(n) for k in range(n))
        if not (all(x == 0 for x in rowsums) and all(x == 0 for x in colsums) and nonneg):
            ds_bad.append((lab, "not doubly stochastic"))
        # the restricted diagonal conditional expectation: D_E(V diag(p) V*) = B p
        ps = sp.symbols(f"p0:{n}", real=True)
        M = sp.expand(V * sp.diag(*ps) * V.conjugate().T)
        for i in range(n):
            diff = sp.simplify(sp.re(M[i, i]) - sum(B[i, k] * ps[k] for k in range(n)))
            if diff != 0:
                de_bad.append((lab, i, str(diff)))
        # reconstruct a simple-spectrum U with eigenbasis V and read off the criterion
        U = sp.Matrix(n, n, lambda a, b: sp.simplify(
            sp.expand(V * sp.diag(*[LAMS[k % 4] for k in range(n)]) * V.conjugate().T)[a, b]))
        if not _is_unitary(U, n):
            ds_bad.append((lab, "reconstructed U not unitary"))
            continue
        d = _survivor_dim(U, n)
        table.append((lab, str(sp.simplify(B.det())), n - B.rank(), d))
    legs["overlap_is_doubly_stochastic_all_members"] = (ds_bad == [] and len(table) == 7)
    legs["diagonal_restriction_is_B_p"] = (de_bad == [])
    legs["survivor_dim_equals_nullity_B_both_directions"] = (
        table == [("identity_n3", "1", 0, 0),
                  ("rational_rotation_n2", "-7/25", 0, 0),
                  ("rational_rotation_n3", "-119/169", 0, 0),
                  ("fourier_n2", "0", 1, 1),
                  ("fourier_n3", "0", 2, 2),
                  ("fourier_n4", "0", 3, 3),
                  ("asymmetric_n3", "1/9", 0, 0)]
        and all(d == nul for _, _, nul, d in table)
        and all((d == 0) == (det != "0") for _, det, _, d in table)
        and len([r for r in table if r[1] == "0"]) == 3
        and len([r for r in table if r[1] != "0"]) == 4)

    # orientation fixed by VALUE: B_ik = |V_ik|^2 reads the ROW index first.
    # The six structured members have symmetric |V|^2; V_asym does not.
    B_asym = _overlap_matrix(V_asym, 3)
    legs["orientation_fixed_by_value"] = (
        _is_unitary(V_asym, 3)
        and sp.expand(B_asym - B_asym.T) != sp.zeros(3, 3)
        and [str(B_asym[0, 2]), str(B_asym[2, 0])] == ["1/9", "4/9"])
    # negative probe: the unitarity test rejects a non-unitary matrix
    legs["unitarity_probe_rejects_nonunitary"] = (
        not _is_unitary(sp.Matrix([[1, 1], [0, 1]]), 2))

    # the composed classification, all three quadrants occupied
    build = [
        ("diagonal_phases_n2", sp.diag(1, _i), 2, sp.eye(2)),
        ("diagonal_phases_n3", sp.diag(1, _i, -1), 3, sp.eye(3)),
        ("diagonal_phases_n4", sp.diag(1, _i, -1, -_i), 4, sp.eye(4)),
        ("rotated_simple_n2", None, 2, _rot(2, 0, 1, sp.Rational(3, 5), sp.Rational(4, 5))),
        ("rotated_simple_n3", None, 3, _rot(3, 0, 2, sp.Rational(5, 13), sp.Rational(12, 13))),
        ("fourier_reconstructed_n3", None, 3, _fourier(3)),
        ("shift_n2", _cyclic_shift(2), 2, _fourier(2)),
        ("shift_n3", _cyclic_shift(3), 3, _fourier(3)),
        ("shift_n4", _cyclic_shift(4), 4, _fourier(4)),
        ("degenerate_n3", sp.diag(1, 1, _i), 3, sp.eye(3)),
        ("degenerate_n4", sp.diag(1, 1, _i, _i), 4, sp.eye(4)),
        ("identity_n3", sp.eye(3), 3, sp.eye(3)),
    ]
    cases = []
    cls_bad = []
    for lab, U, n, V in build:
        if U is None:
            U = sp.Matrix(n, n, lambda a, b: sp.simplify(
                sp.expand(V * sp.diag(*[LAMS[k % 4] for k in range(n)])
                          * V.conjugate().T)[a, b]))
        if not _is_unitary(U, n):
            cls_bad.append((lab, "not unitary"))
            continue
        simple = (len(U.eigenvals()) == n)
        detB = str(sp.simplify(_overlap_matrix(V, n).det())) if simple else "n/a"
        d = _survivor_dim(U, n)
        forced = (d == 0)
        predicate = simple and detB != "0" and detB != "n/a"
        if forced != predicate:
            cls_bad.append((lab, d, detB))
        cases.append((lab, simple, detB, d))
    q_forced = [c for c in cases if c[3] == 0]
    q_simple_singular = [c for c in cases if c[1] and c[2] == "0"]
    q_degenerate = [c for c in cases if not c[1]]
    legs["forcing_coincides_with_predicate_on_all_12"] = (
        cls_bad == [] and len(cases) == 12
        and [c[3] for c in cases] == [0, 0, 0, 0, 0, 2, 1, 2, 3, 2, 4, 6])
    legs["all_three_quadrants_occupied"] = (
        [len(q_forced), len(q_simple_singular), len(q_degenerate)] == [5, 4, 3]
        and [c[0] for c in q_forced if c[2] == "0"] == []
        and [c[0] for c in q_degenerate if c[3] == 0] == [])

    # seeded float control: generic random instances, stated tolerance.
    # A MEASUREMENT: this leg is float and its verdict depends on the tolerance.
    import numpy as np
    rng = np.random.default_rng(20260731)
    mismatches, tested = [], 0
    for n in (2, 3, 4, 5):
        for _ in range(25):
            V = _haar_np(rng, n)
            lam = np.exp(1j * rng.uniform(0, 2 * np.pi, n))
            U = V @ np.diag(lam) @ V.conj().T
            B = np.abs(V) ** 2
            pred = abs(np.linalg.det(B)) > 1e-8
            got = (_surv_dim_float(U) == 0)
            tested += 1
            if pred != got:
                mismatches.append((n, float(abs(np.linalg.det(B)))))
    legs["float_control_100_haar_samples_agree"] = (mismatches == [] and tested == 100)

    return _result("check_T_unistochastic_overlap_criterion", 4, "P_math",
                   legs, fails,
                   {"criterion_table": table,
                    "classification": cases,
                    "float_control": {"seed": 20260731, "samples": tested,
                                      "tolerance": "1e-8 relative"},
                    "statement": "FORCING (quantified over R) <=> simple spectrum "
                                 "AND det B != 0; dim(survivors) = nullity(B); "
                                 "verified on the stated exact families and "
                                 "100 seeded Haar samples"})


def check_L_simple_spectrum_is_necessary():
    """(c) Simple spectrum is necessary, via sum of squared multiplicities."""
    legs, fails = {}, []
    # dim Comm(U)_sa = sum m^2, in two conjugations each
    LAM = [sp.Integer(1), _i, sp.Integer(-1), -_i,
           sp.Rational(3, 5) + sp.Rational(4, 5) * _i]
    patterns = [(2, (1, 1), 2), (2, (2,), 4),
                (3, (2, 1), 5), (3, (1, 1, 1), 3),
                (4, (2, 2), 8), (4, (3, 1), 10), (4, (1, 1, 1, 1), 4),
                (5, (2, 2, 1), 9)]
    comm_bad = []
    for n, mult, want in patterns:
        spec = []
        for a, m in enumerate(mult):
            spec.extend([LAM[a]] * m)
        D = sp.diag(*spec)
        Vr = _rot(n, 0, n - 1, sp.Rational(3, 5), sp.Rational(4, 5))
        for conj, V in (("diag", sp.eye(n)), ("rotated", Vr)):
            U = sp.expand(V * D * V.conjugate().T)
            d = _commutant_sa_dim(U, n)
            if not (_is_unitary(U, n) and d == want == sum(m * m for m in mult)):
                comm_bad.append((n, mult, conj, d))
    legs["commutant_dim_is_sum_of_squared_multiplicities"] = (
        comm_bad == [] and len(patterns) == 8)

    # every partition of every n <= 8: sum m^2 >= n, equality iff all ones
    def partitions(n, mx=None):
        if mx is None:
            mx = n
        if n == 0:
            yield ()
            return
        for k in range(min(n, mx), 0, -1):
            for rest in partitions(n - k, k):
                yield (k,) + rest
    below, equal, total = [], [], 0
    for n in range(1, 9):
        for p in partitions(n):
            total += 1
            s2 = sum(m * m for m in p)
            if s2 < n:
                below.append((n, p))
            if s2 == n:
                equal.append((n, p))
    legs["sum_m_squared_at_least_n_equality_iff_simple"] = (
        below == [] and total == 66 and len(equal) == 8
        and all(all(m == 1 for m in p) for _, p in equal))

    # degenerate transports admit survivors; dimensions pinned by value
    wit = []
    for n, spec in ((3, (1, 1, _i)), (4, (1, 1, _i, _i)), (4, (1, 1, 1, -1))):
        U = sp.diag(*spec)
        m = tuple(_multiplicities(U))
        wit.append((n, m, _survivor_dim(U, n)))
    legs["degenerate_transports_admit_survivors"] = (
        wit == [(3, (2, 1), 2), (4, (2, 2), 4), (4, (3, 1), 6)]
        and all(d >= sum(x * x for x in m) - n for n, m, d in wit))

    # the corrected figure: at diag(1,1,i,i) the SURVIVOR dimension is 4;
    # 8 is the self-adjoint COMMUTANT dimension (2^2 + 2^2)
    Udeg4 = sp.diag(1, 1, _i, _i)
    legs["degenerate_n4_survivor_four_commutant_eight"] = (
        [_survivor_dim(Udeg4, 4), _commutant_sa_dim(Udeg4, 4)] == [4, 8])

    # the named witness: bound attained, survivors exhibited, positivity no rescue
    U = sp.diag(1, 1, _i)
    surv = _survivor_space(U, 3)
    X12 = sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])
    Y12 = sp.Matrix([[0, -_i, 0], [_i, 0, 0], [0, 0, 0]])
    R = sp.eye(3) + sp.Rational(3, 10) * X12
    legs["bound_attained_survivors_are_X12_Y12"] = (
        sum(x * x for x in _multiplicities(U)) - 3 == 2
        and len(surv) == 2
        and _in_span(X12, surv) and _in_span(Y12, surv))
    legs["positive_definite_nonscalar_solution_exists"] = (
        [str(v) for v in _eigs_exact(R)] == ["7/10", "1", "13/10"]
        and _is_pos_def(R)
        and sp.expand(U.conjugate().T * R * U - R) == sp.zeros(3, 3)
        and all(R[k, k] == 1 for k in range(3)))
    return _result("check_L_simple_spectrum_is_necessary", 3, "P_math",
                   legs, fails,
                   {"partitions_scanned": total,
                    "witnesses": wit,
                    "statement": "degenerate spectrum => survivors exist; "
                                 "positivity does not rescue"})


def check_L_diagonal_expectation_and_qubit_residual():
    """(d) D_E is a conditional expectation; the exact qubit residual identity."""
    legs, fails = {}, []
    # D_E: X |-> diag part.  Idempotent, unital, trace-preserving -- symbolically.
    xs = sp.symbols("x0:9", real=True)
    X = sp.Matrix(3, 3, lambda a, b: xs[3 * a + b])
    E = lambda M: sp.diag(*[M[i, i] for i in range(3)])
    legs["diagonal_expectation_is_conditional_expectation"] = (
        sp.simplify(E(E(X)) - E(X)) == sp.zeros(3, 3)
        and E(sp.eye(3)) == sp.eye(3)
        and sp.simplify(sp.trace(E(X)) - sp.trace(X)) == 0)

    # the qubit residual, at symbolic theta and phi
    th, ph = sp.symbols("theta phi", real=True)
    mx, my, mz = sp.symbols("m_x m_y m_z", real=True)
    r0, rx, ry, rz = sp.symbols("r_0 r_x r_y r_z", real=True)
    Id = sp.eye(2)
    sx = sp.Matrix([[0, 1], [1, 0]])
    sy = sp.Matrix([[0, -_i], [_i, 0]])
    sz = sp.Matrix([[1, 0], [0, -1]])
    M = mx * sx + my * sy + mz * sz
    U = sp.exp(_i * th) * (sp.cos(ph) * Id + _i * sp.sin(ph) * M)
    R = r0 * Id + rx * sx + ry * sy + rz * sz
    res = sp.expand(U.conjugate().T * R * U - R).subs(mx ** 2, 1 - my ** 2 - mz ** 2)
    coeff = [sp.simplify(sp.expand(sp.trace(s * res) / 2)) for s in (Id, sx, sy, sz)]
    r = sp.Matrix([rx, ry, rz]); m = sp.Matrix([mx, my, mz])
    rperp = r - (m.dot(r)) * m
    rxm = r.cross(m)
    pred = [-2 * sp.sin(ph) ** 2 * rperp[k] - 2 * sp.cos(ph) * sp.sin(ph) * rxm[k]
            for k in range(3)]
    diffs = [str(sp.simplify(sp.expand_trig(sp.expand(coeff[k + 1] - pred[k])
                                            .subs(mx ** 2, 1 - my ** 2 - mz ** 2))))
             for k in range(3)]
    legs["global_phase_and_scalar_part_cancel"] = (str(sp.simplify(coeff[0])) == "0")
    legs["residual_identity_at_symbolic_phi"] = (diffs == ["0", "0", "0"])

    # the vanishing criterion, symbolic: r_perp . (r x m) = 0 identically and
    # |r_perp|^2 = |r x m|^2 mod |m|^2 = 1, so with the residual identity
    # above, |U*RU - R|^2 = 4 sin^2(phi) |r_perp|^2 -- zero iff r_perp = 0
    # whenever sin(phi) != 0
    _mod_m = lambda e: sp.simplify(
        sp.rem(sp.expand(e), mx ** 2 + my ** 2 + mz ** 2 - 1, mx))
    legs["residual_norm_identity_symbolic"] = (
        sp.simplify(sp.expand(rperp.dot(rxm))) == 0
        and _mod_m(rperp.dot(rperp) - rxm.dot(rxm)) == 0
        and _mod_m(sum(x * x for x in pred)
                   - 4 * sp.sin(ph) ** 2 * rperp.dot(rperp)) == 0)

    # vanishing criterion at every non-involutive phi tested: residual = 0 iff r || m
    subs_g = {mx: 0, my: 0, mz: 1}
    bad, noninv = [], 0
    for k in range(1, 12):
        phv = sp.pi * sp.Rational(k, 12)
        if sp.simplify(sp.sin(phv)) == 0:
            continue
        if sp.simplify(sp.cos(phv)) != 0:
            noninv += 1
        c = [sp.simplify(x.subs(subs_g).subs(ph, phv)) for x in coeff[1:]]
        Jm = sp.Matrix([[sp.simplify(sp.diff(ci, v)) for v in (rx, ry)] for ci in c])
        zero_at = all(sp.simplify(ci.subs({rx: 0, ry: 0})) == 0 for ci in c)
        indep = all(sp.simplify(sp.diff(ci, v)) == 0 for ci in c for v in (r0, rz))
        if not (Jm.rank() == 2 and zero_at and indep):
            bad.append(str(phv))
    legs["residual_vanishes_exactly_on_r_parallel_m"] = (bad == [] and noninv == 10)

    # the loose proportionality reading is FALSE at phi = pi/2
    at_half = [sp.simplify(x.subs(subs_g).subs(ph, sp.pi / 2)
                           .subs({rx: 1, ry: 0, rz: 0})) for x in coeff[1:]]
    rxm_at = [sp.simplify(x.subs(subs_g).subs({rx: 1, ry: 0, rz: 0}))
              for x in (rxm[0], rxm[1], rxm[2])]
    legs["residual_not_proportional_to_r_cross_m"] = (
        [str(x) for x in at_half] == ["-2", "0", "0"]
        and [str(x) for x in rxm_at] == ["0", "-1", "0"]
        and str(sp.simplify(at_half[0] * rxm_at[1] - at_half[1] * rxm_at[0])) == "2")

    # det B = m_z, exactly, with the sign a basis convention and |det B| invariant
    mzs = sp.Symbol("m_z", real=True)
    Bq = sp.Matrix([[(1 + mzs) / 2, (1 - mzs) / 2], [(1 - mzs) / 2, (1 + mzs) / 2]])
    concrete = []
    for mzv in (sp.Rational(3, 5), sp.Rational(1, 2), sp.Integer(1)):
        Mv = sp.sqrt(1 - mzv ** 2) * sx + mzv * sz
        cols = []
        for val, mult, vs in Mv.eigenvects():
            for v in vs:
                cols.append(sp.simplify(v / sp.sqrt((v.conjugate().T * v)[0, 0])))
        V = sp.Matrix.hstack(*cols)
        Bv = sp.Matrix(2, 2, lambda a, b: sp.simplify(sp.Abs(V[a, b]) ** 2))
        concrete.append(str(sp.simplify(sp.Abs(Bv.det()) - sp.Abs(mzv))))
    legs["qubit_det_B_equals_mz"] = (
        str(sp.simplify(Bq.det() - mzs)) == "0"
        and str(sp.simplify(Bq[:, [1, 0]].det() + mzs)) == "0"
        and concrete == ["0", "0", "0"])
    return _result("check_L_diagonal_expectation_and_qubit_residual", 3, "P_math",
                   legs, fails,
                   {"residual_identity": "U*RU - R = (-2 sin^2 phi) r_perp . sigma "
                                         "+ (-2 cos phi sin phi) (r x m) . sigma",
                    "qubit": "det B = m_z; forced iff m_z != 0"})


def check_L_forcing_is_quantified_over_R():
    """(e) THE QUANTIFIER FENCE: forcing is uniqueness over R, not solvability
    at eps I.  R = eps I satisfies both premises for every transport."""
    legs, fails = {}, []
    eps = sp.Rational(7, 4)
    # eps I solves the premises on every battery member
    solves_bad = []
    for lab, U, n in [("shift_n2", _cyclic_shift(2), 2),
                      ("shift_n3", _cyclic_shift(3), 3),
                      ("diagonal_phases_n3", sp.diag(1, _i, -1), 3),
                      ("degenerate_n3", sp.diag(1, 1, _i), 3)]:
        Rid = eps * sp.eye(n)
        if not (sp.expand(U.conjugate().T * Rid * U - Rid) == sp.zeros(n, n)
                and all(sp.simplify(Rid[i, i] - eps) == 0 for i in range(n))):
            solves_bad.append(lab)
    legs["eps_identity_solves_premises_on_every_member"] = (solves_bad == [])

    # at the n=2 shift: premises hold at eps I, condition (b) fails
    Ush = _cyclic_shift(2)
    Bsh = _overlap_matrix(_fourier(2), 2)
    legs["shift_n2_satisfies_premises_while_det_B_vanishes"] = (
        str(sp.simplify(Bsh.det())) == "0"
        and len(Ush.eigenvals()) == 2)   # simple spectrum: (b), not (a), fails
    # and the premise system there is TWO-dimensional: eps I is a solution
    # but not the only one
    d_sh, _ = _frame_solution_space(Ush, 2)
    surv = _survivor_space(Ush, 2)
    sx = sp.Matrix([[0, 1], [1, 0]])
    # sigma_z lies off the survivor span -- the span test's negative probe
    legs["shift_n2_premise_system_is_two_dimensional"] = (
        d_sh == 2 and len(surv) == 1 and _in_span(sx, surv)
        and not _in_span(sp.Matrix([[1, 0], [0, -1]]), surv))
    # the non-scalar co-solution, exhibited with its spectrum
    Rns = eps * sp.eye(2) + sp.Rational(1, 2) * sx
    legs["nonscalar_cosolution_exhibited"] = (
        sp.expand(Ush.conjugate().T * Rns * Ush - Rns) == sp.zeros(2, 2)
        and all(sp.simplify(Rns[i, i] - eps) == 0 for i in range(2))
        and [str(v) for v in _eigs_exact(Rns)] == ["5/4", "9/4"]
        and sp.expand(Rns - Rns[0, 0] * sp.eye(2)) != sp.zeros(2, 2))
    return _result("check_L_forcing_is_quantified_over_R", 3, "P_math",
                   legs, fails,
                   {"correct_statement": "for every R satisfying (i) and (ii), "
                                         "R is a real multiple of the identity "
                                         "<=> simple spectrum AND det B != 0",
                    "witness": "n=2 shift: eps I admissible, det B = 0, "
                               "solution space dimension 2"})


def check_L_mixing_is_not_monotone():
    """(f) det B_s = (1-s)^(n-1) along the flat path; off the path an exact
    n = 3 pair refutes monotonicity in the majorization order."""
    legs, fails = {}, []
    s = sp.symbols("s", real=True)
    path_bad = []
    for n in (2, 3, 4, 5):
        Bs = (1 - s) * sp.eye(n) + s * sp.ones(n, n) / n
        d = sp.simplify(Bs.det())
        if not (sp.simplify(d - (1 - s) ** (n - 1)) == 0
                and sp.simplify(d.subs(s, 0)) == 1
                and sp.simplify(d.subs(s, 1)) == 0):
            path_bad.append(n)
    legs["flat_path_det_is_one_minus_s_to_n_minus_one"] = (path_bad == [])

    # the counterexample pair: both exactly orthogonal, both simple spectrum
    rt2 = sp.sqrt(2) / 2
    V1 = sp.Matrix([[rt2, -rt2, 0], [rt2, rt2, 0], [0, 0, 1]])
    V2 = sp.Matrix([[2, 2, -1], [-1, 2, 2], [2, -1, 2]]) / 3
    B1 = _overlap_matrix(V1, 3)
    B2 = _overlap_matrix(V2, 3)
    spec3 = [sp.Integer(1), _i, sp.Integer(-1)]
    U1 = sp.Matrix(3, 3, lambda a, b: sp.simplify(
        sp.expand(V1 * sp.diag(*spec3) * V1.conjugate().T)[a, b]))
    U2 = sp.Matrix(3, 3, lambda a, b: sp.simplify(
        sp.expand(V2 * sp.diag(*spec3) * V2.conjugate().T)[a, b]))
    legs["pair_is_unitary_with_simple_spectra"] = (
        _is_unitary(V1, 3) and _is_unitary(V2, 3)
        and _is_unitary(U1, 3) and _is_unitary(U2, 3)
        and [len(U1.eigenvals()), len(U2.eigenvals())] == [3, 3])
    legs["determinants_zero_and_one_ninth"] = (
        [str(sp.simplify(B1.det())), str(sp.simplify(B2.det()))] == ["0", "1/9"])

    # anti-vacuity: the majorization predicate must reject the reverse direction
    legs["majorization_predicate_rejects_reverse"] = (
        [_maj([sp.Rational(1, 2), sp.Rational(1, 2), sp.Integer(0)],
              [sp.Rational(4, 9), sp.Rational(4, 9), sp.Rational(1, 9)]),
         _maj([sp.Rational(4, 9), sp.Rational(4, 9), sp.Rational(1, 9)],
              [sp.Rational(1, 2), sp.Rational(1, 2), sp.Integer(0)])] == [False, True])
    # the totals clause decides here: partial sums never exceed, totals differ
    legs["majorization_predicate_rejects_unequal_totals"] = (
        _maj([sp.Rational(1, 2), sp.Rational(1, 4), sp.Integer(0)],
             [sp.Rational(1, 2), sp.Rational(1, 2), sp.Integer(0)]) is False)
    # row-wise majorization, strict on every row
    maj_rows = [_maj([B2[r, c] for c in range(3)], [B1[r, c] for c in range(3)])
                for r in range(3)]
    strict = [bool(sp.simplify(max(B2[r, c] for c in range(3))
                               - max(B1[r, c] for c in range(3))) < 0) for r in range(3)]
    legs["B2_rows_majorized_by_B1_rows_strictly"] = (
        maj_rows == [True, True, True] and strict == [True, True, True])
    # and on the concatenated 9-vector, with the partial sums pinned exactly
    a9 = sorted((sp.nsimplify(B2[r, c]) for r in range(3) for c in range(3)), reverse=True)
    b9 = sorted((sp.nsimplify(B1[r, c]) for r in range(3) for c in range(3)), reverse=True)
    pa = [str(sp.nsimplify(sum(a9[:k + 1]))) for k in range(9)]
    pb = [str(sp.nsimplify(sum(b9[:k + 1]))) for k in range(9)]
    legs["B2_9vector_majorized_by_B1_9vector"] = (
        pa == ["4/9", "8/9", "4/3", "16/9", "20/9", "8/3", "25/9", "26/9", "3"]
        and pb == ["1", "3/2", "2", "5/2", "3", "3", "3", "3", "3"]
        and _maj([B2[r, c] for r in range(3) for c in range(3)],
                 [B1[r, c] for r in range(3) for c in range(3)]))
    # a second, independent mixing measure orders the pair the same way
    pur1 = sp.simplify(sum(B1[a, b] ** 2 for a in range(3) for b in range(3)))
    pur2 = sp.simplify(sum(B2[a, b] ** 2 for a in range(3) for b in range(3)))
    legs["purity_orders_the_pair"] = (
        [str(pur1), str(pur2)] == ["2", "11/9"] and bool(pur2 < pur1))
    # forcing fails at the LESS mixed matrix and holds at the MORE mixed one
    legs["forcing_fails_at_the_less_mixed_matrix"] = (
        [_survivor_dim(U1, 3), _survivor_dim(U2, 3)] == [1, 0])
    return _result("check_L_mixing_is_not_monotone", 3, "P_math",
                   legs, fails,
                   {"B1": "[[1/2,1/2,0],[1/2,1/2,0],[0,0,1]]",
                    "B2": "[[4/9,4/9,1/9],[1/9,4/9,4/9],[4/9,1/9,4/9]]",
                    "reading": "B2 is more mixed under every Schur-concave "
                               "measure, yet B2 forces and B1 does not; "
                               "monotonicity holds on the flat path only"})


def check_L_singular_B_survivors_are_positive():
    """(g) Singular B is a real failure mode: survivors exist, are positive
    definite inside the symmetric radius |t| < eps/||K||_op -- sharp as a
    two-sided radius -- and need eps > 0."""
    legs, fails = {}, []
    rows = []
    rad_bad = []
    for n in (2, 3, 4):
        U = _cyclic_shift(n)
        B = _overlap_matrix(_fourier(n), n)
        flat_ok = all(sp.simplify(B[a, b] - sp.Rational(1, n)) == 0
                      for a in range(n) for b in range(n))
        surv = _survivor_space(U, n)
        K = surv[0]
        nrm = _op_norm_herm(K)
        eps = sp.Integer(1)
        rr = eps / nrm
        R_in = [eps * sp.eye(n) + sg * sp.Rational(1, 2) * rr * K for sg in (1, -1)]
        R_edge = [eps * sp.eye(n) + sg * rr * K for sg in (1, -1)]
        R_out = [eps * sp.eye(n) + sg * sp.Rational(3, 2) * rr * K for sg in (1, -1)]
        ok = (_is_unitary(U, n)
              and len(U.eigenvals()) == n
              and flat_ok
              and str(sp.simplify(B.det())) == "0"
              and all(sp.simplify(K[a, a]) == 0 for a in range(n))
              and sp.expand(U.conjugate().T * K * U - K) == sp.zeros(n, n)
              and all(_is_pos_def(M) for M in R_in)
              and all(_is_pos_semidef(M) for M in R_edge)
              and any(not _is_pos_def(M) for M in R_edge)
              and any(not _is_pos_semidef(M) for M in R_out)
              and all(sp.expand(M - M[0, 0] * sp.eye(n)) != sp.zeros(n, n)
                      for M in R_in))
        if not ok:
            rad_bad.append(n)
        rows.append((n, len(surv), str(sp.nsimplify(nrm))))
    legs["shift_survivors_positive_on_sharp_two_sided_radius"] = (
        rad_bad == []
        and rows == [(2, 1, "1"), (3, 2, "2"), (4, 3, "1")])

    # negative-dominant probe: the operator norm reads max |lambda|, not max lambda
    legs["op_norm_negative_dominant_probe"] = (
        str(sp.nsimplify(_op_norm_herm(sp.diag(-2, 1, 1)))) == "2")

    # the sharpness is of the SYMMETRIC radius: at n = 3 the survivor spectrum
    # is (-1, -1, 2), and positivity extends one-sidedly past +eps/||K||_op
    K3 = _survivor_space(_cyclic_shift(3), 3)[0]
    t3 = sp.Rational(11, 10) / _op_norm_herm(K3)
    legs["n3_positivity_extends_one_sidedly_past_symmetric_radius"] = (
        [str(v) for v in _eigs_exact(K3)] == ["-1", "-1", "2"]
        and _is_pos_def(sp.eye(3) + t3 * K3)
        and not _is_pos_semidef(sp.eye(3) - t3 * K3))

    # the n = 2 survivor is sigma_x; the prior-art control reproduced
    sx = sp.Matrix([[0, 1], [1, 0]])
    surv2 = _survivor_space(_cyclic_shift(2), 2)
    R_prior = sp.eye(2) + sp.Rational(1, 2) * sx
    legs["n2_survivor_is_sigma_x_prior_art_control"] = (
        len(surv2) == 1 and _in_span(sx, surv2)
        and [str(v) for v in _eigs_exact(R_prior)] == ["1/2", "3/2"]
        and _is_pos_def(R_prior)
        and all(R_prior[k, k] == 1 for k in range(2)))

    # eps > 0 is a premise: every survivor is trace-free hence indefinite
    cnt, tf_bad = 0, []
    for n in (2, 3, 4):
        for b in _herm_basis(n):
            if all(b[a, a] == 0 for a in range(n)):
                cnt += 1
                ev = _eigs_exact(b)
                if not (sp.simplify(sp.Integer(0) + sum(ev)) == 0
                        and any(sp.simplify(v) > 0 for v in ev)
                        and any(sp.simplify(v) < 0 for v in ev)):
                    tf_bad.append((n, str(b)))
    legs["zero_diagonal_hermitian_is_tracefree_indefinite"] = (
        cnt == 20 and tf_bad == [])
    # Tr R = n eps, so eps <= 0 admits no positive solution
    epsym = sp.Symbol("eps")
    tr_diff = sp.simplify(
        sp.trace(sp.eye(3) * epsym
                 + sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])) - 3 * epsym)
    nonpos = []
    for epsv in (sp.Integer(0), sp.Integer(-1)):
        any_pos = False
        for k in range(-6, 7):
            Rm = epsv * sp.eye(2) + sp.Rational(k, 4) * sx
            if _is_pos_semidef(Rm) and sp.simplify(sp.trace(Rm)) > 0:
                any_pos = True
        nonpos.append(any_pos)
    legs["no_positive_solution_at_nonpositive_eps"] = (
        str(tr_diff) == "0" and nonpos == [False, False])
    return _result("check_L_singular_B_survivors_are_positive", 3, "P_math",
                   legs, fails,
                   {"shift_battery": rows,
                    "prior_art_control": "R = I + sigma_x/2, spectrum {1/2, 3/2}",
                    "radius": "|t| < eps/||K||_op, sharp as a symmetric "
                              "two-sided radius; at n = 3 positivity extends "
                              "one-sidedly past +eps/||K||_op"})


def check_L_det_B_genericity_and_conditioning():
    """(h) Seeded Monte Carlo SCOPE: det B != 0 is generic; |det B| falls with
    n as a scale artifact while the conditioning degrades only like 1/n; nine
    generic singular-B points located by bisection.  Float measurements at
    pinned seeds, graded [P_numerical_scope], pins at 4 significant figures."""
    import numpy as np
    legs, fails = {}, []
    # exact half: det B is not the zero polynomial
    legs["det_B_not_identically_zero"] = (
        str(sp.simplify(_overlap_matrix(sp.eye(4), 4).det())) == "1")

    SEED, NSAMP = 20260731, 4000
    rng = np.random.default_rng(SEED)
    meds, conds, cnts, mins = [], [], [], []
    for n in (2, 3, 4, 5, 6, 8):
        dl, cl = [], []
        for _ in range(NSAMP):
            Bm = np.abs(_haar_np(rng, n)) ** 2
            dl.append(abs(np.linalg.det(Bm)))
            cl.append(np.linalg.cond(Bm))
        ds = np.array(dl); cs = np.array(cl)
        meds.append(float(np.median(ds)))
        conds.append(float(np.median(cs)))
        cnts.append(int(np.sum(ds >= 1e-3)))
        mins.append(float(ds.min()))
    legs["median_det_B_pinned_and_decreasing"] = (
        [_G4(x) for x in meds] == [0.5018, 0.1073, 0.02207, 0.003934,
                                   0.000627, 1.243e-05]
        and all(meds[k] > meds[k + 1] for k in range(5)))
    legs["median_cond_B_pinned_and_increasing"] = (
        [_G4(x) for x in conds] == [1.993, 5.205, 9.431, 14.26, 19.77, 34.3]
        and all(conds[k] < conds[k + 1] for k in range(5)))
    # THE WITHDRAWAL, computed: the determinant ratio dwarfs the conditioning
    # ratio, so the determinant's fall does not measure distance to failure
    legs["conditioning_two_orders_below_determinant_ratio"] = (
        [_G4(meds[0] / meds[-1]), _G4(conds[-1] / conds[0]),
         _G4((meds[0] / meds[-1]) / (conds[-1] / conds[0]))]
        == [40370.0, 17.21, 2345.0])
    legs["tail_counts_pinned_n8_exactly_two"] = (
        cnts == [3998, 3974, 3867, 3253, 1469, 2]
        and all(m > 0 for m in mins))

    # nine GENERIC singular-B points at n = 3, 4, 5, located by bisection on
    # unitary paths V0 exp(i t H) at seed 20260804; at each point every entry
    # of B is bounded away from zero, nullity(B) = 1, survivor dim = 1
    def _u_exp(H, t):
        lam, Q = np.linalg.eigh(H)
        return Q @ np.diag(np.exp(1j * t * lam)) @ Q.conj().T
    rng2 = np.random.default_rng(20260804)
    points = []
    for n in (3, 4, 5):
        found = 0
        while found < 3:
            V0 = _haar_np(rng2, n)
            a = rng2.normal(size=(n, n)) + 1j * rng2.normal(size=(n, n))
            H = (a + a.conj().T) / 2
            f = lambda t: np.linalg.det(np.abs(V0 @ _u_exp(H, t)) ** 2)
            ts = np.linspace(0.0, 3.0, 61)
            vals = [f(t) for t in ts]
            root = None
            for k in range(60):
                if vals[k] != 0.0 and vals[k + 1] != 0.0 \
                        and np.sign(vals[k]) != np.sign(vals[k + 1]):
                    lo, hi = ts[k], ts[k + 1]
                    for _ in range(80):
                        mid = (lo + hi) / 2
                        if np.sign(f(mid)) == np.sign(f(lo)):
                            lo = mid
                        else:
                            hi = mid
                    root = (lo + hi) / 2
                    break
            if root is None:
                continue
            V = V0 @ _u_exp(H, root)
            B = np.abs(V) ** 2
            sv = np.linalg.svd(B, compute_uv=False)
            lam = np.exp(1j * (0.7 + 1.1 * np.arange(n)))   # distinct phases
            U = V @ np.diag(lam) @ V.conj().T
            points.append({
                "n": n, "root": _G4(root),
                "abs_det": abs(float(f(root))),
                "min_entry": _G4(float(B.min())),
                "nullity": int((sv < 1e-7 * sv[0]).sum()),
                "second_sv_rel": float(sv[-2] / sv[0]),
                "surv_dim": _surv_dim_float(U),
            })
            found += 1
    legs["nine_singular_points_roots_pinned"] = (
        [p["root"] for p in points] == [0.3918, 0.2439, 2.501, 0.3943, 0.6746,
                                        0.09801, 1.292, 0.605, 0.3098]
        and [p["n"] for p in points] == [3, 3, 3, 4, 4, 4, 5, 5, 5])
    legs["entries_bounded_away_from_zero"] = (
        [p["min_entry"] for p in points] == [0.03252, 0.006519, 0.002894,
                                             0.01541, 0.02381, 0.06569,
                                             0.01162, 0.02063, 0.006332]
        and all(p["min_entry"] > 2e-3 for p in points))
    legs["nullity_one_survivor_dim_one_at_each_point"] = (
        all(p["abs_det"] < 1e-12 for p in points)
        and [p["nullity"] for p in points] == [1] * 9
        and [p["surv_dim"] for p in points] == [1] * 9
        and all(p["second_sv_rel"] > 0.05 for p in points))
    return _result("check_L_det_B_genericity_and_conditioning", 3,
                   "P_numerical_scope", legs, fails,
                   {"seed_haar": SEED, "samples_per_n": NSAMP,
                    "seed_bisection": 20260804,
                    "median_det_by_n": [_G4(x) for x in meds],
                    "median_cond_by_n": [_G4(x) for x in conds],
                    "reading": "the determinant's fall is an n-dependent "
                               "scale; the distance-to-failure statement is "
                               "the conditioning, factor 17.21 across n=2..8"})


ALL_CHECKS = [
    check_L_premises_reduce_to_survivor_space,
    check_T_unistochastic_overlap_criterion,
    check_L_simple_spectrum_is_necessary,
    check_L_diagonal_expectation_and_qubit_residual,
    check_L_forcing_is_quantified_over_R,
    check_L_mixing_is_not_monotone,
    check_L_singular_B_survivors_are_positive,
    check_L_det_B_genericity_and_conditioning,
]


def run_all():
    results = []
    for fn in ALL_CHECKS:
        r = fn()
        results.append(r)
        status = "PASS" if r["passed"] else "FAIL"
        n_true = sum(1 for v in r["legs"].values() if v is True)
        print(f"[{status}] {r['name']}  legs={n_true}/{len(r['legs'])}")
        if not r["passed"]:
            for f in r["fails"]:
                print("   -", f)
    print(f"{sum(r['passed'] for r in results)}/{len(results)} checks pass")
    return results


# Registered v24.3.467 (2026-08-04) after blinded cold audit LAND-WITH-FIXES
# 0.89 (zero MAJORs, zero arithmetic disagreements) + separate cold fix seat
# (all six coverage-gap mutants re-run CAUGHT).  BARE-NAME keys per D6.
def register(registry):
    registry.update({fn.__name__.replace("check_", "", 1): fn for fn in ALL_CHECKS})
    return registry

if __name__ == "__main__":
    run_all()
