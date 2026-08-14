# BANKED v24.3.476 (2026-08-14): built and held under the Supplier Search
# charter Phase 2, twice blind-audited, fixes carried, LIFTED by Ethan
# 2026-08-14; registered with bare-name keys per D6@2026-08-03.
"""The extended-carrier elliptope: fixed non-uniform nonnegative diagonal.

Built 2026-08-14 by a cold build seat under the frozen claim surface
``CLAIM_SURFACE_EE_extended_carrier_elliptope_2026-08-14.md`` (Supplier
Search charter Phase 2, prerequisite 3 of 3). The surface binds: weaken
with disclosure, strengthen nothing.

------------------------------------------------------------------------------
WHAT THIS MODULE COMPUTES (exact arithmetic; stdlib + fractions)
------------------------------------------------------------------------------

This module states the extended-carrier elliptope as a GENERALIZATION of
the banked ``carrier_elliptope`` theorem: the index set stays finite, and
the uniform diagonal eps is generalized to a FIXED NON-UNIFORM nonnegative
diagonal d. The banked theorem is the uniform-diagonal special case, and
EE2 recovers it BY VALUE through the banked module's own machinery.
GEOMETRY ONLY: the module characterizes a set of matrices and proves its
elementary PSD facts. No record vocabulary, no visibility, no tradeoff
law.

EE1 -- THE CHARACTERIZATION (check_T_extended_carrier_elliptope).
On a finite index set with fixed diagonal d_i >= 0, the carrier-consistent
functional set is {W symmetric PSD : diag(W) = d}. Membership is decided
by the principal-minors route (the banked ``psd_by_minors`` genre,
implemented independently here); on the exercised family the minors route
and the definitional quadratic-form route agree, a non-PSD matrix with the
correct diagonal carries an explicit rational negative witness, and the
free sector's dimension -- the symmetric hollow directions at fixed
diagonal -- is COMPUTED by exact Gaussian elimination on a genuinely
COUPLED spanning set (the pair directions together with all their
pairwise sums, so the set is linearly dependent -- rank strictly below
the row count, enforced) and ENFORCED equal to the pair count at n = 3
and n = 4, with a corrupted-set control (replacing one direction by a
combination of the others drops the rank by exactly one, computed); at
the interior point of the exercised n = 3 family every pair direction
is exhibited as a two-sided admissible perturbation with an exact
rational step -- the perturbed matrices stay IN the elliptope
(membership recomputed) and ON the fiber (diagonal preserved).

EE2 -- THE UNIFORM RESTRICTION RECOVERS THE BANKED THEOREM, BY VALUE
(check_L_uniform_restriction_recovers_banked). Restricting the extended
construction to a uniform diagonal reproduces the banked module's objects
executed THROUGH THAT MODULE'S OWN module-level functions
(``sym_from_offdiag``, ``det_exact``, ``psd_by_minors``) on shared
instances: matrices entrywise, every principal minor by value (this
module's determinant against the banked determinant on the same index
subsets), at two distinct uniform units. A real cross-module value tie,
not a verdict comparison.

EE3 -- THE PER-CELL MINOR BOUND (check_L_per_cell_minor_bound).
|W_ij| <= sqrt(d_i d_j) as PSD necessity: the 2x2 principal minor at
(i, j) IS d_i d_j - W_ij^2, tied by value against this module's
determinant on the extracted submatrix, so the SQUARED form
W_ij^2 <= d_i d_j is legged everywhere in exact Fractions; on diagonals
whose pairwise products are perfect squares of rationals the sqrt is
certified exactly (s_ij >= 0 and s_ij^2 = d_i d_j) and the bound legged
in the |W_ij| <= s_ij form. The zero-diagonal forcing -- d_i = 0 forces
W_ij = 0 for all j -- is computed on a diagonal with zero and nonzero
entries interleaved: every PSD survivor of an exhaustive rational grid
has zero off-diagonal entries at every zero cell, the survivor count
equals a computed expectation, and each single-entry violation is
minor-detected. Genre: a zero diagonal entry forces zeros in its row
and column of every PSD completion; no downstream law is stated.

EE4 -- ACHIEVEMENT (check_L_rank_one_achievement). Rank-one PSD
completions achieving the per-cell bounds on two matched-diagonal
families: v with v_i^2 = d_i (enforced), all 2^n sign vectors, so
W = v v^T has diag(W) = d and |W_ij| = s_ij as EXACT EQUALITY -- a
polynomial identity discharged in exact arithmetic on the constructed
witnesses, equality and not <= only. Every entry's SIGN is pinned by
value (W_ij = sigma_i sigma_j b_i b_j per cell), and the completions
are enforced pairwise distinct with the collapse disclosed: sigma and
-sigma construct the SAME matrix, so the 2^n iterated sign vectors
yield exactly 2^(n-1) distinct completions per family, counted and
enforced. PSD is certified by minors, not asserted: every size-1
principal minor equals d_i and every principal minor of size >= 2
vanishes, computed.

EE5 -- PERMANENT CONTROLS (check_T_extended_elliptope_controls).
(a) A diagonal-violating W is rejected, with the first mismatched index
located by computation; and a PSD impostor whose diagonal is a
PERMUTATION of d -- equal as a multiset, unequal as a tuple -- is
rejected, pinning the entrywise position-sensitive diagonal-fixing
convention. (b) An indefinite W with the correct diagonal is
rejected, minor-detected: the exercised instance passes every 2x2
principal minor and fails at size 3, the failing subset found by search,
its value tied against the banked ``det_exact`` on the same submatrix.
(c) The exercised extended family's diagonal is ENFORCED genuinely
non-uniform -- at least two distinct diagonal values on every
load-bearing extended instance; the EE2 uniform diagonal is deliberately
uniform, being the restriction instance, and is excluded from this leg
with that disclosure. (d) No sign-class datum is read or supplied,
scoped to this module: membership is invariant under diagonal sign
conjugation (every principal minor equal by value across all sign
vectors -- an exercised IDENTITY, the sign factors square out of every
principal determinant, disclosed as such), so the off-diagonal signs
enter only as fiber coordinates; the conjugation itself is pinned
non-vacuously on an exercised witness (a mixed sign vector moves every
mixed-sign off-diagonal cell of a nowhere-zero-off-diagonal member,
and every conjugated entry equals its predicted sigma_i sigma_j
multiple by value); a scoped source scan for supply tokens
is carried as a proxy with its limitation disclosed at the site -- it
covers exactly three spellings in this file and adjudicates nothing
else.

------------------------------------------------------------------------------
PREMISES
------------------------------------------------------------------------------
CONSUMED: exact rational arithmetic only. The banked ``carrier_elliptope``
module-level functions are EXECUTED as value-tie targets in EE2 and
EE5(b); nothing is consumed from them as a premise, and nothing here
reads the word module's probed eps -- units and diagonals are explicit
arguments throughout.

STANDING LIMIT (disclosed per D7@2026-08-08): the leg-inventory contract
below certifies that a declared leg EXECUTED, not that it COULD HAVE
FAILED; a multi-site rename or a computed verdict replaced by a constant
escapes it, as it escapes the raising form equally.

MAY NOT CITE while the hold stands (and the first five permanently):
- Any tradeoff law in any form; none appears here and none may be
  attributed to this module.
- Any Englert or visibility/distinguishability identification; no record
  vocabulary exists in this module.
- Anything for or against situational-S.
- Any sign-class supply or read claim -- EE5(d) exists to bar exactly
  that.
- Any claim that the extension is "the physical carrier": it is a stated
  index-set generalization of a banked theorem, and this module says only
  what it computes.
- Any bank-wide universal.
"""

from fractions import Fraction as F
from itertools import combinations, product

# Value-tie targets: the banked module's own module-level machinery,
# executed on shared instances in EE2 and EE5(b). Imported for execution,
# not consumed as premises.
from apf.carrier_elliptope import (
    sym_from_offdiag as banked_sym_from_offdiag,
    det_exact as banked_det_exact,
    psd_by_minors as banked_psd_by_minors,
)

# ---------------------------------------------------------------------------
# the load-bearing diagonals (module constants; EE5(c) enforces
# non-uniformity on every extended instance)
# ---------------------------------------------------------------------------

# Extended (non-uniform) diagonals. Pairwise products are perfect squares
# of rationals by construction, so every sqrt in EE3/EE4 stays exact.
DIAG_MAIN = (F(1), F(4), F(9, 4))
DIAG_SECOND = (F(9, 4), F(1, 4), F(4))
# Zero and nonzero diagonal entries interleaved (EE3 forcing).
DIAG_ZERO_CELLS = (F(4), F(0), F(9), F(0))
# Correct-diagonal indefinite control lives at this diagonal (EE5(b)).
DIAG_INDEF = (F(1), F(1), F(4))

EXTENDED_DIAGONALS = (DIAG_MAIN, DIAG_SECOND, DIAG_ZERO_CELLS, DIAG_INDEF)

# The EE2 restriction units: deliberately UNIFORM (the restriction
# instance), excluded from the EE5(c) non-uniformity leg by disclosure.
UNIFORM_UNITS = (F(2, 3), F(1))

# ---------------------------------------------------------------------------
# exact helpers (this module's own route; the banked functions above are
# tie targets, never silently substituted)
# ---------------------------------------------------------------------------

def pairs(n):
    return [(i, j) for i in range(n) for j in range(i + 1, n)]

def ext_matrix(d, off):
    """Symmetric W with fixed diagonal d and off-diagonal dict off."""
    n = len(d)
    W = [[d[i] if i == j else F(0) for j in range(n)] for i in range(n)]
    for (i, j), v in off.items():
        W[i][j] = v
        W[j][i] = v
    return W

def det(W):
    """Exact determinant by cofactor expansion over Q."""
    n = len(W)
    if n == 1:
        return W[0][0]
    tot = F(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in W[1:]]
        tot += (-1) ** j * W[0][j] * det(minor)
    return tot

def submatrix(W, S):
    return [[W[i][j] for j in S] for i in S]

def principal_minor_list(W):
    """(subset, minor value) for every nonempty principal subset, in a
    fixed canonical order."""
    n = len(W)
    out = []
    for r in range(1, n + 1):
        for S in combinations(range(n), r):
            out.append((S, det(submatrix(W, S))))
    return out

def psd_all_minors(W):
    return all(v >= 0 for _, v in principal_minor_list(W))

def diag_of(W):
    return tuple(W[i][i] for i in range(len(W)))

def in_extended_elliptope(W, d):
    """Membership: symmetric, diag(W) = d, PSD by the all-principal-minors
    route."""
    n = len(d)
    sym = all(W[i][j] == W[j][i] for i in range(n) for j in range(n))
    return sym and diag_of(W) == tuple(d) and psd_all_minors(W)

def quad_form(W, x):
    n = len(W)
    return sum(W[i][j] * x[i] * x[j] for i in range(n) for j in range(n))

def matrix_rank(M):
    """Exact rank by Gaussian elimination over Q."""
    A = [row[:] for row in M]
    rows, cols = len(A), len(A[0]) if A else 0
    rank = 0
    for c in range(cols):
        piv = next((r for r in range(rank, rows) if A[r][c] != 0), None)
        if piv is None:
            continue
        A[rank], A[piv] = A[piv], A[rank]
        A[rank] = [v / A[rank][c] for v in A[rank]]
        for r in range(rows):
            if r != rank and A[r][c] != 0:
                A[r] = [a - A[r][c] * b for a, b in zip(A[r], A[rank])]
        rank += 1
    return rank

def certified_sqrt(q):
    """The exact nonnegative rational square root of q, or None if q is
    not a perfect square of a rational. Certified by re-squaring, never
    by floats."""
    if q < 0:
        return None
    num, den = q.numerator, q.denominator
    rn, rd = _isqrt(num), _isqrt(den)
    if rn is None or rd is None:
        return None
    s = F(rn, rd)
    return s if s * s == q else None

def _isqrt(m):
    if m < 0:
        return None
    r = int(m ** 0.5)  # float SEED only; certification is exact below
    while r * r > m:
        r -= 1
    while (r + 1) * (r + 1) <= m:
        r += 1
    return r if r * r == m else None

def rank_one(v):
    n = len(v)
    return [[v[i] * v[j] for j in range(n)] for i in range(n)]

def conj_by_signs(W, sigma):
    n = len(W)
    return [[sigma[i] * sigma[j] * W[i][j] for j in range(n)]
            for i in range(n)]

def _main_family():
    """The load-bearing EE1 family at DIAG_MAIN: the diagonal point, a
    rank-one point, and an interior convex combination."""
    d = DIAG_MAIN
    n = len(d)
    Wdiag = ext_matrix(d, {})
    v = tuple(certified_sqrt(di) for di in d)
    Wone = rank_one(v)
    Wint = [[(Wdiag[i][j] + Wone[i][j]) / 2 for j in range(n)]
            for i in range(n)]
    return d, [Wdiag, Wone, Wint]

# ---------------------------------------------------------------------------
# set-exact leg inventory -- append-and-record per D7@2026-08-08, sited in
# the result-assembly path the bank would execute
# ---------------------------------------------------------------------------

EXPECTED_LEGS = {
    "check_T_extended_carrier_elliptope": [
        "converse_nonpsd_negative_witness_and_minor",
        "diag_fixed_and_enforced_on_family",
        "free_sector_dimension_computed_and_enforced",
        "membership_minors_agree_with_quadratic_forms",
    ],
    "check_L_uniform_restriction_recovers_banked": [
        "construction_matches_banked_entrywise",
        "determinants_and_membership_through_banked_machinery",
        "principal_minors_tie_by_value",
    ],
    "check_L_per_cell_minor_bound": [
        "exact_sqrt_certified_bound_on_perfect_square_products",
        "squared_bound_is_two_by_two_minor_necessity",
        "violating_entry_minor_detected",
        "zero_diagonal_forces_zero_offdiagonal",
    ],
    "check_L_rank_one_achievement": [
        "achievement_exact_equality",
        "matched_diagonal_construction_enforced",
        "psd_certified_by_minors_rank_one",
    ],
    "check_T_extended_elliptope_controls": [
        "diagonal_violating_rejected",
        "indefinite_correct_diagonal_minor_detected",
        "nonuniform_diagonal_enforced_on_load_bearing_family",
        "offdiagonal_signs_enter_only_as_fiber_coordinates",
    ],
}

def _result(name, legs, fails, key_result):
    exp = EXPECTED_LEGS[name]
    got = sorted(legs)
    if got != exp:
        # append-and-record: the mismatch is a failure reason, and the
        # rest of the check's verdicts still return in the same pass
        fails.append(f"leg inventory mismatch: {got} != {exp}")
    for k, v in legs.items():
        if v is not True:
            fails.append(f"leg not True: {k}")
    return {
        "name": name, "passed": not fails, "legs": dict(legs),
        "fails": list(fails), "key_result": key_result,
        "tier": 3, "epistemic": "P_math",
        "status": "BANKED v24.3.476 (2026-08-14; lifted by Ethan)",
    }

# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def check_T_extended_carrier_elliptope():
    """EE1: the set {W symmetric PSD : diag(W) = d} on a fixed non-uniform
    nonnegative diagonal, membership by the principal-minors route; free
    sector dimension by exact rank on a coupled spanning set, with a
    corrupted-set control and two-sided interior perturbations that stay
    in the elliptope and on the fiber."""
    legs, fails = {}, []
    d, family = _main_family()
    n = len(d)

    # the family is exercised AT the fixed diagonal, and its members are
    # genuinely distinct instances
    legs["diag_fixed_and_enforced_on_family"] = (
        d == DIAG_MAIN
        and all(diag_of(W) == d for W in family)
        and len({tuple(map(tuple, W)) for W in family}) == len(family)
        and len(family) >= 3)

    # the minors route agrees with the definitional quadratic-form route
    # on the PSD side of the exercised family, on a full rational grid
    grid = [F(a) for a in (-2, -1, 0, 1, 2)]
    qvals = [quad_form(W, x) for W in family for x in product(grid, repeat=n)]
    legs["membership_minors_agree_with_quadratic_forms"] = (
        all(in_extended_elliptope(W, d) for W in family)
        and all(v >= 0 for v in qvals)
        and len(qvals) == len(family) * len(grid) ** n)

    # converse: correct diagonal, not PSD -- explicit rational negative
    # witness, and the detecting minor located with a negative value
    Wbad = ext_matrix(d, {(0, 1): F(3)})
    xw = (F(2), F(-1), F(0))
    bad_minors = [(S, v) for S, v in principal_minor_list(Wbad) if v < 0]
    legs["converse_nonpsd_negative_witness_and_minor"] = (
        diag_of(Wbad) == d
        and quad_form(Wbad, xw) < 0
        and not in_extended_elliptope(Wbad, d)
        and len(bad_minors) >= 1
        and (0, 1) in [S for S, _ in bad_minors])

    # free sector at fixed diagonal: the symmetric hollow directions.
    # The dimension is computed by exact rank on a genuinely COUPLED
    # spanning set -- the pair directions PLUS all their pairwise sums,
    # so the set is linearly dependent by construction (rank strictly
    # below the row count, enforced) -- and enforced equal to
    # the pair count at n = 3 and n = 4. A corrupted spanning set is
    # asserted to CHANGE the rank: replacing one pair direction by a
    # combination of the others drops the rank by exactly one while
    # the row count stays put.
    free_ok = True
    dims = {}
    for m in (3, 4):
        dirs = []
        for (i, j) in pairs(m):
            B = [[F(0)] * m for _ in range(m)]
            B[i][j] = B[j][i] = F(1)
            dirs.append([B[r][c] for r in range(m) for c in range(m)])
        coupled = dirs + [[a + b for a, b in zip(u2, v2)]
                          for u2, v2 in combinations(dirs, 2)]
        dims[m] = matrix_rank(coupled)
        k = m * (m - 1) // 2
        free_ok = free_ok and dims[m] == len(pairs(m)) == k
        # the coupled set is genuinely dependent: rank strictly below
        # the row count
        free_ok = free_ok and len(coupled) > dims[m]
        # corrupted-set control: direction 0 replaced by dirs[1]+dirs[2]
        corrupted = ([[a + b for a, b in zip(dirs[1], dirs[2])]]
                     + dirs[1:])
        free_ok = (free_ok and len(corrupted) == k
                   and matrix_rank(corrupted) == k - 1)

    # at the interior point of the exercised family, every pair
    # direction is a two-sided admissible perturbation with an exact
    # rational step: Wint +/- t*D_ij stays IN the elliptope (membership
    # recomputed, PSD and diagonal both) -- the dimension count is tied
    # to the object, not only to the ambient coordinate space
    Wint = family[2]
    pert_ok, steps = True, {}
    for (i, j) in pairs(n):
        t, found = F(1), None
        for _ in range(8):
            Wp = [row[:] for row in Wint]
            Wm = [row[:] for row in Wint]
            Wp[i][j] = Wp[j][i] = Wint[i][j] + t
            Wm[i][j] = Wm[j][i] = Wint[i][j] - t
            if (in_extended_elliptope(Wp, d)
                    and in_extended_elliptope(Wm, d)):
                found = t
                break
            t = t / 2
        pert_ok = pert_ok and found is not None
        steps[(i, j)] = found
    # a diagonal direction leaves the fiber
    Wpert = ext_matrix(d, {})
    Wpert[0][0] = Wpert[0][0] + F(1)
    legs["free_sector_dimension_computed_and_enforced"] = (
        free_ok and pert_ok and len(steps) == len(pairs(n))
        and diag_of(Wpert) != d)

    return _result("check_T_extended_carrier_elliptope", legs, fails,
                   {"diagonal": [str(x) for x in d],
                    "family_dets": [str(det(W)) for W in family],
                    "free_sector_dims": {str(m): dims[m] for m in dims},
                    "interior_two_sided_steps": {
                        f"{i},{j}": str(v) for (i, j), v in steps.items()},
                    "witness_value": str(quad_form(Wbad, xw))})

def check_L_uniform_restriction_recovers_banked():
    """EE2: the uniform-diagonal restriction reproduces the banked
    carrier_elliptope objects executed through that module's own
    functions, entrywise and by value, on shared instances.

    DISCLOSED: the two sides share the cofactor / all-principal-minors
    algorithm (this module's det and psd_all_minors are the same route
    as the banked det_exact and psd_by_minors), so the tie certifies
    convention agreement and drift against the banked module, not an
    independent recomputation -- a defect shared by the common
    algorithm would pass both sides symmetrically."""
    legs, fails = {}, []
    n = 3
    # shared instance shapes: the banked module's three elliptope samples
    # plus its non-PSD witness shape, built at each unit
    def shared_offs(u):
        return [
            {},
            {(0, 1): u, (0, 2): u, (1, 2): u},
            {(0, 1): u / 2, (1, 2): u / 2},
            {(0, 1): u, (0, 2): u, (1, 2): -u},
        ]

    entry_ties, minor_ties, det_ties, mem_ok = [], [], [], []
    for u in UNIFORM_UNITS:
        d_uniform = (u,) * n
        for off in shared_offs(u):
            ours = ext_matrix(d_uniform, off)
            theirs = banked_sym_from_offdiag(n, u, off)
            entry_ties.append(all(
                ours[i][j] == theirs[i][j]
                for i in range(n) for j in range(n)))
            # every principal minor: this module's determinant against the
            # banked determinant on the same index subsets -- BY VALUE
            for S, v in principal_minor_list(ours):
                minor_ties.append(v == banked_det_exact(submatrix(theirs, S)))
            det_ties.append(det(ours) == banked_det_exact(theirs))
            mem_ok.append(
                in_extended_elliptope(ours, d_uniform)
                == banked_psd_by_minors(theirs))
    n_instances = sum(len(shared_offs(u)) for u in UNIFORM_UNITS)
    legs["construction_matches_banked_entrywise"] = (
        len(UNIFORM_UNITS) == 2
        and UNIFORM_UNITS[0] != UNIFORM_UNITS[1]
        and all(entry_ties) and len(entry_ties) == n_instances)
    legs["principal_minors_tie_by_value"] = (
        all(minor_ties) and len(minor_ties) == n_instances * (2 ** n - 1))
    # the shared family carries both membership verdicts (the last shape
    # in shared_offs is the banked module's non-PSD witness), so the
    # agreement below is exercised on both sides of the membership
    # boundary; the value content of the tie lives in the minors leg
    both_sides = [banked_psd_by_minors(
        banked_sym_from_offdiag(n, u, off))
        for u in UNIFORM_UNITS for off in shared_offs(u)]
    legs["determinants_and_membership_through_banked_machinery"] = (
        all(det_ties) and len(det_ties) == n_instances
        and all(mem_ok) and len(mem_ok) == n_instances
        and True in both_sides and False in both_sides)
    return _result("check_L_uniform_restriction_recovers_banked", legs, fails,
                   {"units": [str(u) for u in UNIFORM_UNITS],
                    "instances_tied": n_instances,
                    "minor_values_tied": len(minor_ties)})

def check_L_per_cell_minor_bound():
    """EE3: |W_ij| <= sqrt(d_i d_j) as 2x2-principal-minor PSD necessity,
    exact throughout; zero-diagonal forcing on a diagonal with zero and
    nonzero entries interleaved. Genre: a zero diagonal entry forces
    zeros in its row and column of every PSD completion; no downstream
    law stated."""
    legs, fails = {}, []
    d, family = _main_family()
    n = len(d)

    # the 2x2 principal minor at (i, j) IS d_i d_j - W_ij^2 -- an
    # algebraic IDENTITY for every symmetric W, disclosed as such; its
    # role here is a value tie on the det implementation (a wrong-sign
    # or wrong-scale det reddens it). The squared bound that follows is
    # the real inequality, legged on the PSD family.
    sq_ok, sq_count = True, 0
    for W in family:
        for (i, j) in pairs(n):
            m2 = det(submatrix(W, (i, j)))
            sq_ok = sq_ok and m2 == d[i] * d[j] - W[i][j] ** 2
            sq_ok = sq_ok and W[i][j] ** 2 <= d[i] * d[j]
            sq_count += 1
    legs["squared_bound_is_two_by_two_minor_necessity"] = (
        sq_ok and sq_count == len(family) * len(pairs(n)))

    # on perfect-square pairwise products the sqrt is certified exactly
    # and the bound legged in |W_ij| <= s_ij form
    s_ok, s_count = True, 0
    for dd in (DIAG_MAIN, DIAG_SECOND):
        for (i, j) in pairs(len(dd)):
            s = certified_sqrt(dd[i] * dd[j])
            s_ok = s_ok and s is not None and s >= 0 and s * s == dd[i] * dd[j]
            s_count += 1
    fam_ok = True
    for W in family:
        for (i, j) in pairs(n):
            s_ij = certified_sqrt(d[i] * d[j])
            fam_ok = (fam_ok and s_ij is not None
                      and abs(W[i][j]) <= s_ij)
    legs["exact_sqrt_certified_bound_on_perfect_square_products"] = (
        s_ok and s_count == len(pairs(3)) * 2 and fam_ok)

    # a violating entry is minor-detected: strictly beyond the certified
    # bound at one cell, the 2x2 minor there goes negative and membership
    # fails
    s01 = certified_sqrt(d[0] * d[1])
    Wv = ext_matrix(d, {(0, 1): s01 + F(1, 2)})
    legs["violating_entry_minor_detected"] = (
        det(submatrix(Wv, (0, 1))) < 0
        and not in_extended_elliptope(Wv, d))

    # zero-diagonal forcing on the zero/nonzero-interleaved diagonal:
    # exhaustive rational grid over all off-diagonal cells; every PSD
    # survivor vanishes at every zero-cell entry; the survivor count
    # equals a computed expectation (the free cell's admissible grid
    # values); each single-entry violation is minor-detected
    dz = DIAG_ZERO_CELLS
    nz = len(dz)
    zero_idx = [i for i in range(nz) if dz[i] == 0]
    gridvals = [F(-1), F(0), F(1)]
    pz = pairs(nz)
    survivors = []
    for combo in product(gridvals, repeat=len(pz)):
        off = {p: v for p, v in zip(pz, combo)}
        W = ext_matrix(dz, off)
        if psd_all_minors(W):
            survivors.append(off)
    zero_touch = [p for p in pz if p[0] in zero_idx or p[1] in zero_idx]
    free_cells = [p for p in pz if p not in zero_touch]
    expected_survivors = 1
    for (i, j) in free_cells:
        expected_survivors *= sum(
            1 for g in gridvals if g * g <= dz[i] * dz[j])
    forced = all(
        all(off[p] == 0 for p in zero_touch) for off in survivors)
    single_detected = all(
        det(submatrix(ext_matrix(dz, {p: g}), p)) < 0
        for p in zero_touch for g in gridvals if g != 0)
    legs["zero_diagonal_forces_zero_offdiagonal"] = (
        len(zero_idx) >= 2 and len(free_cells) >= 1
        and 0 < len(survivors) < len(gridvals) ** len(pz)
        and len(survivors) == expected_survivors
        and forced and single_detected)

    return _result("check_L_per_cell_minor_bound", legs, fails,
                   {"zero_cell_diagonal": [str(x) for x in dz],
                    "grid_candidates": len(gridvals) ** len(pz),
                    "psd_survivors": len(survivors)})

def check_L_rank_one_achievement():
    """EE4: rank-one PSD completions achieving the per-cell bounds with
    EXACT EQUALITY on matched-diagonal families; every entry sign
    pinned by value; sigma and -sigma construct the same matrix, so the
    2^n sign vectors yield exactly 2^(n-1) distinct completions per
    family, counted and enforced; PSD certified by minors."""
    legs, fails = {}, []
    families = (DIAG_MAIN, DIAG_SECOND)

    con_ok, con_count = True, 0
    eq_ok, eq_count = True, 0
    psd_ok, psd_count = True, 0
    sign_ok, distinct_ok = True, True
    distinct_counts = []
    for dd in families:
        n = len(dd)
        base = tuple(certified_sqrt(di) for di in dd)
        con_ok = con_ok and all(b is not None and b * b == di
                                for b, di in zip(base, dd))
        completions = set()
        for sigma in product((F(1), F(-1)), repeat=n):
            v = tuple(s * b for s, b in zip(sigma, base))
            W = rank_one(v)
            con_ok = con_ok and diag_of(W) == dd
            con_count += 1
            # the SIGN of every entry is pinned BY VALUE: W_ij equals
            # sigma_i sigma_j b_i b_j per cell, computed entrywise
            sign_ok = sign_ok and all(
                W[i][j] == sigma[i] * sigma[j] * base[i] * base[j]
                for i in range(n) for j in range(n))
            completions.add(tuple(map(tuple, W)))
            # achievement as exact equality: |W_ij| = s_ij, a polynomial
            # identity discharged on the constructed witness (genre
            # disclosed: identity given the enforced construction, not an
            # independent measurement)
            for (i, j) in pairs(n):
                s = certified_sqrt(dd[i] * dd[j])
                eq_ok = eq_ok and abs(W[i][j]) == s
                eq_count += 1
            # PSD by minors: size-1 minors are the diagonal, size >= 2
            # minors vanish (the rank-one witness), all nonnegative
            for S, val in principal_minor_list(W):
                psd_ok = psd_ok and (
                    val == dd[S[0]] if len(S) == 1 else val == 0)
                psd_ok = psd_ok and val >= 0
                psd_count += 1
            psd_ok = psd_ok and in_extended_elliptope(W, dd)
        # sigma and -sigma construct the SAME matrix (W depends on
        # sigma only through the products sigma_i sigma_j), so the 2^n
        # iterated sign vectors yield exactly 2^(n-1) distinct
        # completions -- counted and ENFORCED, the collapse disclosed
        distinct_counts.append(len(completions))
        distinct_ok = distinct_ok and len(completions) == 2 ** (n - 1)

    n_patterns = sum(2 ** len(dd) for dd in families)
    legs["matched_diagonal_construction_enforced"] = (
        len(families) == 2 and con_ok and con_count == n_patterns
        and sign_ok and distinct_ok)
    legs["achievement_exact_equality"] = (
        eq_ok and eq_count == sum(
            2 ** len(dd) * len(pairs(len(dd))) for dd in families))
    legs["psd_certified_by_minors_rank_one"] = (
        psd_ok and psd_count == sum(
            2 ** len(dd) * (2 ** len(dd) - 1) for dd in families))

    return _result("check_L_rank_one_achievement", legs, fails,
                   {"families": [[str(x) for x in dd] for dd in families],
                    "sign_vectors_iterated": n_patterns,
                    "distinct_completions_per_family": distinct_counts,
                    "equalities_checked": eq_count})

def check_T_extended_elliptope_controls():
    """EE5: permanent controls -- diagonal violation rejected; indefinite
    with correct diagonal rejected minor-detected; non-uniformity
    enforced; no sign-class datum read or supplied (scoped)."""
    legs, fails = {}, []
    d = DIAG_MAIN
    n = len(d)

    # (a) diagonal-violating W rejected, first mismatched index located;
    # AND a PSD impostor whose diagonal is a PERMUTATION of d -- equal
    # as a multiset, unequal as a tuple (both computed) -- is rejected.
    # This is the control that pins the ENTRYWISE position-sensitive
    # diagonal-fixing convention.
    Wwrong = ext_matrix(d, {})
    Wwrong[1][1] = d[1] + F(1)
    mismatch = [i for i in range(n) if diag_of(Wwrong)[i] != d[i]]
    d_perm = (d[1], d[0], d[2])
    Wperm = ext_matrix(d_perm, {})
    legs["diagonal_violating_rejected"] = (
        not in_extended_elliptope(Wwrong, d)
        and psd_all_minors(Wwrong)
        and mismatch == [1]
        and sorted(d_perm) == sorted(d) and d_perm != d
        and psd_all_minors(Wperm)
        and not in_extended_elliptope(Wperm, d))

    # (b) indefinite with the CORRECT diagonal, minor-detected: passes
    # every 2x2 principal minor, fails at size 3; the failing subset
    # found by search; its value tied against the banked determinant on
    # the same submatrix
    di = DIAG_INDEF
    Wind = ext_matrix(di, {(0, 1): F(1), (0, 2): F(2), (1, 2): F(-2)})
    two_by_two = [det(submatrix(Wind, S))
                  for S in combinations(range(3), 2)]
    neg = [(S, v) for S, v in principal_minor_list(Wind) if v < 0]
    neg_sizes = sorted({len(S) for S, _ in neg})
    tie_ok = all(v == banked_det_exact(submatrix(Wind, S)) for S, v in neg)
    legs["indefinite_correct_diagonal_minor_detected"] = (
        diag_of(Wind) == di
        and all(v >= 0 for v in two_by_two) and len(two_by_two) == 3
        and len(neg) >= 1 and neg_sizes == [3]
        and tie_ok
        and not in_extended_elliptope(Wind, di)
        and banked_psd_by_minors(Wind) is False)

    # (c) the load-bearing extended family is genuinely non-uniform --
    # at least two distinct diagonal values on every extended instance;
    # the zero-cell diagonal carries both zero and nonzero cells. The
    # EE2 UNIFORM_UNITS diagonals are deliberately uniform (they ARE the
    # restriction instance) and are excluded here by that disclosure.
    legs["nonuniform_diagonal_enforced_on_load_bearing_family"] = (
        len(EXTENDED_DIAGONALS) == 4
        and all(len(set(dd)) >= 2 for dd in EXTENDED_DIAGONALS)
        and all(x >= 0 for dd in EXTENDED_DIAGONALS for x in dd)
        and any(x == 0 for x in DIAG_ZERO_CELLS)
        and any(x > 0 for x in DIAG_ZERO_CELLS))

    # (d) no sign-class datum read or supplied, scoped to this module.
    # Content: membership is invariant under diagonal sign conjugation --
    # every principal minor of sigma W sigma equals the corresponding
    # minor of W BY VALUE, for all sign vectors -- so off-diagonal signs
    # enter only as fiber coordinates. DISCLOSED IDENTITY: the minor
    # equality is an exact identity of the conjugation (the sign factors
    # square away inside every principal determinant), so this clause
    # compares the module's minor route to itself and cannot fail while
    # the route is sign-blind; it certifies that the route EXECUTES
    # sign-blind, and a route that read signs would redden it. The
    # falsifiable clauses of this leg are the diagonal preservation,
    # the NON-VACUITY pin on the conjugation below, and the scan
    # below. Proxy: a scoped scan of this
    # module's own source for identifier-shaped sign-class supply
    # tokens; the scan is a proxy for the predicate, disclosed as such
    # (a supplier under a name not on the list escapes the scan -- and
    # the module's own fence prose necessarily NAMES the barred
    # vocabulary, which is why the scan covers identifier forms only;
    # the invariance computation above is the leg's content). The scan
    # covers exactly the three spellings listed, in this file's own
    # source, and adjudicates nothing else -- not imported objects,
    # not data under any other name.
    _, family = _main_family()
    inv_ok, inv_count = True, 0
    for W in family:
        base_minors = principal_minor_list(W)
        for sigma in product((F(1), F(-1)), repeat=n):
            WC = conj_by_signs(W, sigma)
            inv_ok = inv_ok and diag_of(WC) == diag_of(W)
            for (S, v), (S2, v2) in zip(base_minors,
                                        principal_minor_list(WC)):
                inv_ok = inv_ok and S == S2 and v == v2
                inv_count += 1
    # NON-VACUITY: the conjugation is pinned as a real map, not a
    # no-op. On the rank-one member (every off-diagonal nonzero) with
    # the mixed sign vector (1, -1, 1), every conjugated entry equals
    # its predicted sigma_i sigma_j multiple BY VALUE, and the
    # conjugated matrix differs from the original at every mixed-sign
    # cell, computed entrywise.
    Wnv = family[1]
    sig_nv = (F(1), F(-1), F(1))
    WCnv = conj_by_signs(Wnv, sig_nv)
    moved = [(i, j) for (i, j) in pairs(n)
             if sig_nv[i] * sig_nv[j] == -1]
    nonvac_ok = (
        all(Wnv[i][j] != 0 for (i, j) in pairs(n))
        and all(WCnv[i][j] == sig_nv[i] * sig_nv[j] * Wnv[i][j]
                for i in range(n) for j in range(n))
        and len(moved) >= 1
        and all(WCnv[i][j] != Wnv[i][j] for (i, j) in moved))
    with open(__file__, encoding="utf-8") as fh:
        src = fh.read()
    tokens = ["sign" + "_class", "SIGN" + "_CLASS", "situational" + "_S"]
    scan_ok = all(t not in src for t in tokens)
    # the leg is named for what it COMPUTES (the invariance); what it
    # asserts, scoped to this module, is that no sign-class datum is
    # read or supplied
    legs["offdiagonal_signs_enter_only_as_fiber_coordinates"] = (
        inv_ok
        and inv_count == len(family) * 2 ** n * (2 ** n - 1)
        and nonvac_ok
        and scan_ok)

    return _result("check_T_extended_elliptope_controls", legs, fails,
                   {"negative_minor_subsets": [list(S) for S, _ in neg],
                    "negative_minor_values": [str(v) for _, v in neg],
                    "sign_conjugation_minor_ties": inv_count,
                    "conjugation_moved_cells": [list(p) for p in moved]})

ALL_CHECKS = [
    check_T_extended_carrier_elliptope,
    check_L_uniform_restriction_recovers_banked,
    check_L_per_cell_minor_bound,
    check_L_rank_one_achievement,
    check_T_extended_elliptope_controls,
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

# ---------------------------------------------------------------------------
# registration -- bare-name keys per D6@2026-08-03.
# ---------------------------------------------------------------------------

_CHECKS = {
    'T_extended_carrier_elliptope': check_T_extended_carrier_elliptope,
    'L_uniform_restriction_recovers_banked':
        check_L_uniform_restriction_recovers_banked,
    'L_per_cell_minor_bound': check_L_per_cell_minor_bound,
    'L_rank_one_achievement': check_L_rank_one_achievement,
    'T_extended_elliptope_controls': check_T_extended_elliptope_controls,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


if __name__ == "__main__":
    run_all()
