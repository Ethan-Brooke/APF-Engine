"""The carrier-consistent functionals are an elliptope; eps*Tr is its center.

Built 2026-08-03 by the first seat on ``Reference - CHARTER - The Carrier
Transfer (2026-08-03)``, research successor to
``apf/word_carrier_transfer.py``.

AUDIT RECORD: blinded cold audits LAND-WITH-FIXES 0.84 (2026-08-03) +
LAND-WITH-FIXES 0.85 different-day (2026-08-04); fixes carried by separate
fix seats each round. Banked v24.3.465 (2026-08-04).

------------------------------------------------------------------------------
WHAT THIS MODULE COMPUTES (exact arithmetic; stdlib + fractions)
------------------------------------------------------------------------------

The word module localized the carrier gap: word-priced data determines the
diagonal of the represented algebra's functional and leaves the
off-diagonal free. This module parametrizes the freedom exactly and
computes where the Born point sits inside it.

E1 -- THE FREE SECTOR IS THE ELLIPTOPE
(check_T_carrier_consistent_functionals_are_elliptope). On the SYMMETRIC
test sector, a linear functional with the carrier-fixed diagonal
(psi(E_ii) = eps) is nonnegative on the PSD cone iff its symmetric
coefficient matrix W is PSD. The iff rests on PSD-cone self-duality
(cited); computed here: three distinct elliptope samples (center, the
rank-one J, an interior point -- determinants eps^3 * {1, 0, 1/2}, tied by
value) are nonnegative on a rational rank-one grid, and a non-PSD W with
the carrier diagonal has an explicit rational negative witness. The free
sector's dimension is n(n-1)/2 = |Pairs(X)| -- one degree of freedom per
carrier distinction (it is the symmetric hollow sector Sym_0; the
ANTISYMMETRIC sector, dim n(n-1)/2 = dim so(n), is a SEPARATE freedom on
which every symmetric test element is silent -- Tr(A M) = 0, computed).
Do not conflate the two; the pair count happens to equal both dimensions.

E2 -- THE TWO MODELS ARE THE CENTER AND A RANK-ONE POINT
(check_T_two_models_center_and_extreme). eps*Tr is the center W = eps*I;
the all-ones functional is W = eps*J, rank one (all 2x2 minors vanish,
computed; extremality of rank-one correlation matrices is cited, not
computed). The segment between them is PSD at five DISTINCT rational
samples (in the elliptope for all t by convexity of the PSD cone, cited).
Both endpoints extend the word module's computed argmin diagonal.

E3 -- THE MISSING LEMMA, LOCALIZED -- AND FORKED ON ITS OWN READING
(check_L_missing_lemma_is_center_selection). Formalize "a superposition
of k separators resolves k distinctions" as
phi((sum_S s)^*(sum_S s)) = |S| eps over separator sets S. Computed facts,
on the SYMMETRIC SLICE of the carrier-consistent family:

  (i) The diagonal part is AUTOMATIC: Tr(x_S^* x_S) = |S| for every set of
      distinct ordered pairs (computed across every enumerated S at
      n = 3, 4). The lemma's entire content is the off-diagonal.
  (ii) Under the reading "independent = distinct distinctions", the
      constraint system has FULL RANK on the symmetric off-diagonal
      unknowns at n = 3 and n = 4: solution set { W = eps I }, the center.
  (iii) THE FORK (audit-1 finding, now a leg): at every computed
      instance (n = 3, 4, set sizes 2-3), every binding constraint
      comes from a set whose superposition is RANK-DEFICIENT -- two
      separators sharing a source index, e.g. x = E_01 + E_02 =
      |0>(<1| + <2|), rank one. The SOURCE index is itself read by a
      leg: every coefficient of the system equals twice the number of
      separators of S sharing a source index at that unknown, on every
      row (15 at n = 3, 124 at n = 4), computed by a second path (in
      this file) and tied to the system builder entrywise, with the
      target-sharing count as the discriminating control -- it differs
      from the source-sharing count on every row.
      Under the readings "independent = rank(x_S) = |S|" or "pairwise
      vertex-disjoint" the constraint set is EMPTY (computed: zero rows
      at n = 3, 4) and the k-resolution
      identity is satisfied by EVERY point of the elliptope, selecting
      nothing. Admitted-set counts for both readings are computed and
      pinned as a leg: rank-|S| admits (9, 2) sets at n = 3 and
      (42, 44) at n = 4 (sizes 2, 3); vertex-disjoint admits (0, 0) at
      n = 3 and (12, 0) at n = 4. At n = 3 the vertex-disjoint reading
      admits ZERO sets at either size (two disjoint pairs need >= 4
      vertices), so the EMPTY claim in that cell is vacuous; only
      n = 4, size 2 (12 admitted sets) carries content for that
      reading. So the sharpened open problem, exactly: DOES A
      RANK-DEFICIENT SUPERPOSITION OF k SOURCE-SHARING SEPARATORS RESOLVE
      k DISTINCTIONS? Which independence reading the lemma means is a
      charter-level ruling, not decided here.
  (iv) No constraint touches the ANTISYMMETRIC sector (x^*x is symmetric;
      antisymmetric coefficients identically zero, computed). On M_n(R)
      the solution set under reading (ii) is eps*I + {antisymmetric};
      the "center selection" statement lives on the symmetric slice.

E4 -- THE BORN POINT IS THE UNIQUE DETERMINANT-MAXIMAL POINT
(check_T_trace_is_determinant_maximal). Hadamard / AM-GM: for W PSD with
diag W = eps, det W <= eps^n with equality iff W = eps I (general theorem,
cited; the audit-1 seat supplied the AM-GM proof). Computed: the n = 2
closed form det = eps^2 - w^2 exactly; an eps-relative PSD-filtered
rational grid at n = 3 (the filter DISCRIMINATES: 49 of 125 grid points
survive, computed) with det <= eps^3 and equality only at the center; the
four rank-one sign-pattern points all have det 0. A second-unit re-run at
3*eps computes the degree-3 scaling by value (sample dets and the grid
maximum scale by 27; the argmax stays the center), and a control matrix
with every off-diagonal entry 2*eps has det = 5*eps^3 > 0 while its 2x2
principal minors are -3*eps^2 < 0; the minor test returns False on it,
computed. READING, in this
docstring and in no leg: det W measures the volume of distinguishable
states the functional supports; if a maximal-capacity selection principle
has a carrier-side ancestor, it selects Born. Whether it has one is the
open question this module sharpens, not answers.

E5 -- WORD-ROUTE STRENGTHENINGS ON FRESH CARRIERS
(check_L_word_route_strengthenings). (i) the K2-component kernel rule on
two carriers the word module does not compute: three K2s (-> 3) and
K2 + K4 (-> 1); (ii) the distance law psi(x x^T) = (2 - 2 dist) eps on P4
and C5 at every non-adjacent pair.

------------------------------------------------------------------------------
PREMISES (data below; declarations, audited from outside, not
self-enforced)
------------------------------------------------------------------------------
CONSUMED: the word module's PREMISES_CONSUMED (imported), plus
REAL_SYMMETRIC_TEST_SECTOR. eps is read through the word module's
probed_eps(); an extensionally correct bypass of that probe is invisible
BY EXTENSIONALITY (same note as the word module).
NOT CONSUMED: P1; P2 presentation gauge; P3; CYCLICITY; the eps*Tr
stipulation; DET_MAX_SELECTION_PRINCIPLE (E4 computes where det-max
points; it does not adopt det-max); any resolution of the E3 fork.

MAY NOT CITE (PERMANENT, ruled SC1@2026-09-01):
- "Born is derived" / "the carrier gap is closed". Parametrized and
  located, not closed.
- "Maximal capacity selects Born" as a result (reading, unlicensed).
- "The missing lemma is proved" (localized, not proved).
- "The missing lemma is equivalent to W = eps I" WITHOUT the two
  qualifiers: symmetric slice only, and only under the
  distinct-distinctions reading -- under rank-|S| independence the
  identity is automatic and selects nothing (the E3 fork).
- Any sentence attributing content here to what the module PREVENTS.
"""

from fractions import Fraction as F
from itertools import combinations, product

from apf.word_carrier_transfer import (
    all_pairs, argmin_values, uniform_cost, fiber_kernel_dim,
    unit_matrix, matmul, probed_eps,
    PREMISES_CONSUMED as WORD_PREMISES_CONSUMED,
)

PREMISES_CONSUMED = frozenset(WORD_PREMISES_CONSUMED) | frozenset({
    "REAL_SYMMETRIC_TEST_SECTOR",
})
PREMISES_NOT_CONSUMED = frozenset({
    "P1_SANDWICH_REALIZATION", "P2_PRESENTATION_GAUGE", "P3_UNDERIVED",
    "CYCLICITY", "PHI_EQ_EPS_TR_STIPULATION", "DET_MAX_SELECTION_PRINCIPLE",
})

# ---------------------------------------------------------------------------
# exact helpers
# ---------------------------------------------------------------------------

def sym_from_offdiag(n, eps, off):
    W = [[eps if i == j else F(0) for j in range(n)] for i in range(n)]
    for (i, j), v in off.items():
        W[i][j] = v
        W[j][i] = v
    return W

def quad_form(W, x, n):
    return sum(W[i][j] * x[i] * x[j] for i in range(n) for j in range(n))

def det_exact(W):
    n = len(W)
    if n == 1:
        return W[0][0]
    tot = F(0)
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in W[1:]]
        tot += (-1) ** j * W[0][j] * det_exact(minor)
    return tot

def psd_by_minors(W):
    n = len(W)
    for r in range(1, n + 1):
        for S in combinations(range(n), r):
            sub = [[W[i][j] for j in S] for i in S]
            if det_exact(sub) < 0:
                return False
    return True

def _elliptope_samples(u):
    """The three E1 elliptope samples (center, rank-one J, interior) at
    unit u."""
    return [
        sym_from_offdiag(3, u, {}),
        sym_from_offdiag(3, u, {(0, 1): u, (0, 2): u, (1, 2): u}),
        sym_from_offdiag(3, u, {(0, 1): F(1, 2) * u, (1, 2): F(1, 2) * u}),
    ]

def _expected_sample_dets(u):
    """Expected determinants of _elliptope_samples(u), degree 3 in u."""
    return [u ** 3, F(0), F(1, 2) * u ** 3]

def _det_bound(u):
    """The Hadamard/AM-GM determinant bound at unit u, degree 3 in u."""
    return u ** 3

def _e4_psd_grid(u):
    """The E4 grid scan at unit u: all 125 grid points, and (point, det)
    for the PSD survivors."""
    gridvals = [F(a, 2) * u for a in range(-2, 3)]
    allpts = list(product(gridvals, repeat=3))
    dets = []
    for w01, w02, w12 in allpts:
        W = sym_from_offdiag(3, u, {(0, 1): w01, (0, 2): w02, (1, 2): w12})
        if psd_by_minors(W):
            dets.append(((w01, w02, w12), det_exact(W)))
    return allpts, dets

def mt(a, n):
    return [[a[j][i] for j in range(n)] for i in range(n)]

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

def _sum_units(n, S):
    x = [[F(0)] * n for _ in range(n)]
    for (i, j) in S:
        u = unit_matrix(n, i, j)
        x = [[x[r][c] + u[r][c] for c in range(n)] for r in range(n)]
    return x

def _e3_system(n, eps, admit):
    """Rows (coeff-vector, rhs, S, rank_x) of the k-resolution system over
    the symmetric off-diagonal unknowns, for separator sets S of size 2..3
    passing the ``admit`` predicate."""
    seps = [(i, j) for i in range(n) for j in range(n) if i != j]
    unknowns = [(i, j) for i in range(n) for j in range(i + 1, n)]
    rows = []
    traces = []
    for size in (2, 3):
        for S in combinations(seps, size):
            if not admit(S):
                continue
            x = _sum_units(n, S)
            xsx = matmul(mt(x, n), x, n)
            traces.append((sum(xsx[i][i] for i in range(n)), len(S)))
            const = eps * sum(xsx[i][i] for i in range(n))
            coeff = [xsx[i][j] + xsx[j][i] for (i, j) in unknowns]
            rhs = F(len(S)) * eps - const
            if any(c != 0 for c in coeff) or rhs != 0:
                rows.append((coeff, rhs, S, matrix_rank(x)))
    return rows, traces, unknowns

def _rank_deficient(S, n):
    return matrix_rank(_sum_units(n, S)) < len(S)

def _vertex_disjoint(S):
    seen = set()
    for (i, j) in S:
        if i in seen or j in seen:
            return False
        seen.update((i, j))
    return True

def _admitted_counts(n, admit):
    """Number of separator sets of sizes (2, 3) passing ``admit``."""
    seps = [(i, j) for i in range(n) for j in range(n) if i != j]
    return tuple(sum(1 for S in combinations(seps, size) if admit(S))
                 for size in (2, 3))

# ---------------------------------------------------------------------------
# set-exact leg inventory
# ---------------------------------------------------------------------------

EXPECTED_LEGS = {
    "check_T_carrier_consistent_functionals_are_elliptope": [
        "antisymmetric_part_invisible_on_symmetric_sector",
        "converse_nonpsd_has_negative_witness",
        "forward_distinct_samples_nonnegative_dets_tied",
    ],
    "check_T_two_models_center_and_extreme": [
        "allones_is_rank_one",
        "center_and_extreme_extend_word_diagonal",
        "segment_psd_at_distinct_samples",
    ],
    "check_L_missing_lemma_is_center_selection": [
        "admitted_set_counts_pinned_both_readings",
        "antisymmetric_sector_untouched",
        "binding_coefficients_read_the_source_slot",
        "constraint_system_kernel_zero_n3_n4",
        "independence_fork_rank_deficient_only",
        "k_resolution_diagonal_part_automatic",
    ],
    "check_T_trace_is_determinant_maximal": [
        "extreme_points_have_det_zero",
        "n2_closed_form_exact",
        "n3_grid_det_max_only_at_center",
        "positivity_predicate_negative_control",
        "psd_filter_discriminates",
        "psd_test_rejects_positive_det_negative_minor",
        "second_unit_degree_three_scaling",
    ],
    "check_L_word_route_strengthenings": [
        "distance_law_on_p4_and_c5",
        "k2_rule_fresh_carriers",
    ],
}

def _result(name, legs, fails, key_result):
    exp = EXPECTED_LEGS[name]
    got = sorted(legs)
    if got != exp:
        raise AssertionError(f"{name}: leg inventory mismatch: {got} != {exp}")
    for k, v in legs.items():
        if v is not True:
            fails.append(f"leg not True: {k}")
    return {
        "name": name, "passed": not fails, "legs": dict(legs),
        "fails": list(fails), "key_result": key_result,
        "tier": 3, "epistemic": "P_math",
        "status": "banked v24.3.465 (2026-08-04)",
    }

# ---------------------------------------------------------------------------
# checks
# ---------------------------------------------------------------------------

def check_T_carrier_consistent_functionals_are_elliptope():
    legs, fails = {}, []
    eps = probed_eps()[0]
    n = 3
    grid = [F(a) for a in (-2, -1, 0, 1, 2)]
    samples = _elliptope_samples(eps)
    dets = [det_exact(W) for W in samples]
    qvals = [quad_form(W, x, n) for W in samples for x in product(grid, repeat=n)]
    legs["forward_distinct_samples_nonnegative_dets_tied"] = (
        dets == _expected_sample_dets(eps)
        and len(set(map(str, [tuple(map(tuple, W)) for W in samples]))) == 3
        and all(psd_by_minors(W) for W in samples)
        and all(v >= 0 for v in qvals) and len(qvals) == 3 * 5 ** n)
    Vbad = sym_from_offdiag(n, eps, {(0, 1): eps, (0, 2): eps, (1, 2): -eps})
    xw = (F(-2), F(1), F(1))
    legs["converse_nonpsd_has_negative_witness"] = (
        det_exact(Vbad) == -4 * eps ** 3
        and quad_form(Vbad, xw, n) == -4 * eps
        and quad_form(Vbad, xw, n) < 0)
    A = [[F(0), F(3), F(-1)], [F(-3), F(0), F(2)], [F(1), F(-2), F(0)]]
    traces = [sum(A[i][j] * x[j] * x[i] for i in range(n) for j in range(n))
              for x in product(grid, repeat=n)]
    legs["antisymmetric_part_invisible_on_symmetric_sector"] = (
        all(t == 0 for t in traces) and len(traces) == 5 ** n)
    return _result("check_T_carrier_consistent_functionals_are_elliptope",
                   legs, fails,
                   {"sample_dets": [str(d) for d in dets],
                    "witness_value": str(quad_form(Vbad, xw, n))})

def check_T_two_models_center_and_extreme():
    legs, fails = {}, []
    eps = probed_eps()[0]
    n = 3
    I = sym_from_offdiag(n, eps, {})
    J = sym_from_offdiag(n, eps, {(i, j): eps
                                  for i in range(n) for j in range(i + 1, n)})
    minors2 = [det_exact([[J[i][i], J[i][j]], [J[j][i], J[j][j]]])
               for i in range(n) for j in range(n) if i != j]
    legs["allones_is_rank_one"] = (
        all(m == 0 for m in minors2) and len(minors2) == n * (n - 1)
        and det_exact(J) == 0 and J[0][0] == eps)
    ts = [F(0), F(1, 4), F(1, 2), F(3, 4), F(1)]
    seg = [[[(1 - t) * I[i][j] + t * J[i][j] for j in range(n)]
            for i in range(n)] for t in ts]
    legs["segment_psd_at_distinct_samples"] = (
        all(psd_by_minors(W) for W in seg) and len(seg) == 5
        and len(set(ts)) == 5)
    word_diag, _ = argmin_values(uniform_cost(n, eps), 6, "set",
                                 closed_only=True)
    legs["center_and_extreme_extend_word_diagonal"] = (
        all(I[i][i] == word_diag[(i, i)] == J[i][i] for i in range(n))
        and len(word_diag) == n)
    return _result("check_T_two_models_center_and_extreme", legs, fails,
                   {"segment_dets": [str(det_exact(W)) for W in seg]})

def check_L_missing_lemma_is_center_selection():
    legs, fails = {}, []
    eps = probed_eps()[0]
    systems = {}
    for n in (3, 4):
        rows, traces, unknowns = _e3_system(n, eps, admit=lambda S: True)
        rows_rk, _, _ = _e3_system(n, eps,
                                   admit=lambda S, n=n: not _rank_deficient(S, n))
        rows_vd, _, _ = _e3_system(n, eps, admit=_vertex_disjoint)
        systems[n] = {
            "rows": len(rows),
            "rank": matrix_rank([r[0] for r in rows]) if rows else 0,
            "cols": len(unknowns),
            "rows_full_rank_reading": len(rows_rk),
            "rows_vertex_disjoint_reading": len(rows_vd),
            "all_binding_rows_rank_deficient": all(
                rk < len(S) for _, _, S, rk in rows),
            "traces": traces,
        }
    legs["constraint_system_kernel_zero_n3_n4"] = all(
        systems[n]["rank"] == systems[n]["cols"] for n in (3, 4))
    legs["independence_fork_rank_deficient_only"] = all(
        systems[n]["rows_full_rank_reading"] == 0
        and systems[n]["rows_vertex_disjoint_reading"] == 0
        and systems[n]["all_binding_rows_rank_deficient"]
        and systems[n]["rows"] > 0
        for n in (3, 4))
    legs["k_resolution_diagonal_part_automatic"] = all(
        all(tr == k for tr, k in systems[n]["traces"])
        and len(systems[n]["traces"]) > 0
        for n in (3, 4))
    # THE LOAD SLOT, READ.  x_S^* x_S couples two separators of S exactly
    # when they share a SOURCE index; x_S x_S^* would couple those sharing
    # a TARGET.  Every coefficient of the system built above is predicted
    # here from the source-sharing count by a path independent of the
    # builder and tied to it entrywise; the target-sharing prediction is
    # the discriminating control and every row is required to separate the
    # two.  This is the leg that reads the SOURCE-index half of the
    # E3 (iii) fork sentence; the rank-deficiency half is read by
    # independence_fork_rank_deficient_only.
    # SCOPE: both paths live in this file, so an edit carried on the
    # builder AND on the prediction below is invisible here.  No module
    # downstream consumes this system, so that coordinated edit is
    # invisible to the lane as well.
    slot_ok, slot_rows, slot_differ, slot_counts = True, 0, 0, []
    for n in (3, 4):
        rows, _, unknowns = _e3_system(n, eps, admit=lambda S: True)
        slot_counts.append(len(rows))
        for coeff, _, S, _ in rows:
            src_pred = [F(2 * sum(1 for i in range(n)
                                  if (i, p) in S and (i, q) in S))
                        for (p, q) in unknowns]
            tgt_pred = [F(2 * sum(1 for j in range(n)
                                  if (p, j) in S and (q, j) in S))
                        for (p, q) in unknowns]
            slot_ok = slot_ok and coeff == src_pred
            slot_rows += 1
            slot_differ += 1 if src_pred != tgt_pred else 0
    legs["binding_coefficients_read_the_source_slot"] = (
        slot_ok and slot_counts == [15, 124]
        and slot_differ == slot_rows)
    # antisymmetric coefficients of every binding row vanish identically
    anti = []
    for n in (3, 4):
        rows, _, _ = _e3_system(n, eps, admit=lambda S: True)
        for _, _, S, _ in rows:
            x = _sum_units(n, S)
            xsx = matmul(mt(x, n), x, n)
            anti.extend(xsx[i][j] - xsx[j][i]
                        for i in range(n) for j in range(i + 1, n))
    legs["antisymmetric_sector_untouched"] = (
        all(a == 0 for a in anti) and len(anti) > 0)
    rk_counts = {n: _admitted_counts(n, lambda S, n=n: not _rank_deficient(S, n))
                 for n in (3, 4)}
    vd_counts = {n: _admitted_counts(n, _vertex_disjoint) for n in (3, 4)}
    legs["admitted_set_counts_pinned_both_readings"] = (
        rk_counts[3] == (9, 2) and rk_counts[4] == (42, 44)
        and vd_counts[3] == (0, 0) and vd_counts[4] == (12, 0))
    ksys = {str(n): {k: v for k, v in systems[n].items() if k != "traces"}
            for n in (3, 4)}
    return _result("check_L_missing_lemma_is_center_selection", legs, fails,
                   {"systems": ksys,
                    "rows_separating_source_from_target_slot":
                        [slot_differ, slot_rows],
                    "admitted_counts_rank_reading": {str(n): rk_counts[n]
                                                     for n in (3, 4)},
                    "admitted_counts_vertex_disjoint": {str(n): vd_counts[n]
                                                        for n in (3, 4)}})

def check_T_trace_is_determinant_maximal():
    legs, fails = {}, []
    eps = probed_eps()[0]
    ws = sorted({F(a, b) for a in (-2, -1, 0, 1, 2) for b in (1, 2, 3)})
    pairs = [(det_exact(sym_from_offdiag(2, eps, {(0, 1): w * eps})),
              (F(1) - w ** 2) * eps ** 2) for w in ws]
    legs["n2_closed_form_exact"] = (
        all(a == b for a, b in pairs) and len(pairs) == len(ws)
        and all(a <= eps ** 2 for a, _ in pairs))
    allpts, dets = _e4_psd_grid(eps)
    at_max = [p for p, d in dets if d == _det_bound(eps)]
    legs["n3_grid_det_max_only_at_center"] = (
        len(dets) > 20 and all(d <= _det_bound(eps) for _, d in dets)
        and at_max == [(F(0), F(0), F(0))])
    legs["psd_filter_discriminates"] = (
        len(allpts) == 125 and len(dets) < len(allpts) and len(dets) == 49)
    extremes = [sym_from_offdiag(3, eps, {(0, 1): s1 * eps, (0, 2): s2 * eps,
                                          (1, 2): s1 * s2 * eps})
                for s1 in (1, -1) for s2 in (1, -1)]
    legs["extreme_points_have_det_zero"] = (
        all(det_exact(W) == 0 for W in extremes)
        and all(psd_by_minors(W) for W in extremes) and len(extremes) == 4)
    u2 = 3 * eps
    sdets1 = [det_exact(W) for W in _elliptope_samples(eps)]
    sdets2 = [det_exact(W) for W in _elliptope_samples(u2)]
    allpts2, dets2 = _e4_psd_grid(u2)
    at_max2 = [p for p, d in dets2 if d == _det_bound(u2)]
    legs["second_unit_degree_three_scaling"] = (
        u2 == 3 * eps and u2 != eps
        and sdets2 == _expected_sample_dets(u2)
        and sdets2 == [27 * d for d in sdets1]
        and _det_bound(u2) == 27 * _det_bound(eps)
        and len(allpts2) == 125 and len(dets2) == 49
        and all(d <= _det_bound(u2) for _, d in dets2)
        and at_max2 == [(F(0), F(0), F(0))]
        and max(d for _, d in dets2) == 27 * max(d for _, d in dets))
    # NEGATIVE CONTROL ON THE POSITIVITY PREDICATE (shape taken from the
    # leg positivity_predicate_negative_control in
    # counted_ledger_underdetermination).  Every LEADING principal
    # minor of diag(0, -1, 0) is zero, so a leading-minor test admits it;
    # psd_by_minors ranges over ALL principal minors and returns False.
    # The rank-one points this check leans on are singular, which is
    # exactly where the two tests differ.
    lead_pass = [[F(0), F(0), F(0)], [F(0), F(-1), F(0)],
                 [F(0), F(0), F(0)]]
    lead_minors = [det_exact([[lead_pass[i][j] for j in range(k)]
                              for i in range(k)]) for k in range(1, 4)]
    legs["positivity_predicate_negative_control"] = (
        len(lead_minors) == 3 and all(m == 0 for m in lead_minors)
        and psd_by_minors(lead_pass) is False
        and psd_by_minors(sym_from_offdiag(3, eps, {})) is True)
    Wc = sym_from_offdiag(3, eps, {(0, 1): 2 * eps, (0, 2): 2 * eps,
                                   (1, 2): 2 * eps})
    m2 = det_exact([[Wc[0][0], Wc[0][1]], [Wc[1][0], Wc[1][1]]])
    legs["psd_test_rejects_positive_det_negative_minor"] = (
        det_exact(Wc) == 5 * eps ** 3 and det_exact(Wc) > 0
        and m2 == -3 * eps ** 2 and m2 < 0
        and psd_by_minors(Wc) is False)
    return _result("check_T_trace_is_determinant_maximal", legs, fails,
                   {"n3_psd_grid_points": len(dets),
                    "n3_grid_points_total": len(allpts)})

def check_L_word_route_strengthenings():
    legs, fails = {}, []
    eps = probed_eps()[0]
    three_k2 = [frozenset((0, 1)), frozenset((2, 3)), frozenset((4, 5))]
    k2_k4 = [frozenset((0, 1))] + [frozenset(p)
                                   for p in combinations((2, 3, 4, 5), 2)]
    legs["k2_rule_fresh_carriers"] = (
        fiber_kernel_dim(three_k2, 6, "set") == 3
        and fiber_kernel_dim(k2_k4, 5, "set") == 1
        and fiber_kernel_dim(three_k2, 6, "multiset") == 0)
    checked = []
    for edges, dist in [
        ({frozenset((0, 1)): eps, frozenset((1, 2)): eps,
          frozenset((2, 3)): eps},
         {(0, 2): 2, (0, 3): 3, (1, 3): 2}),
        ({frozenset((i, (i + 1) % 5)): eps for i in range(5)},
         {(0, 2): 2, (1, 3): 2, (1, 4): 2, (2, 4): 2, (0, 3): 2}),
    ]:
        nv = len({v for d in edges for v in d})
        vals, _ = argmin_values(edges, 8, "set", closed_only=False)
        for (i, j), dij in dist.items():
            x = [F(0)] * nv
            x[i], x[j] = F(1), F(-1)
            psi_val = sum(vals[(a, b)] * x[a] * x[b]
                          for a in range(nv) for b in range(nv))
            checked.append((psi_val, (2 - 2 * dij) * eps))
    legs["distance_law_on_p4_and_c5"] = (
        all(a == b for a, b in checked) and len(checked) == 8
        and all(a < 0 for a, _ in checked))
    return _result("check_L_word_route_strengthenings", legs, fails,
                   {"distance_law_pairs_checked": len(checked)})

ALL_CHECKS = [
    check_T_carrier_consistent_functionals_are_elliptope,
    check_T_two_models_center_and_extreme,
    check_L_missing_lemma_is_center_selection,
    check_T_trace_is_determinant_maximal,
    check_L_word_route_strengthenings,
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
# registration -- BARE-name keys per the 2026-08-03 D6 ruling (canonical for
# new modules; by-name gates check both spellings)
# ---------------------------------------------------------------------------

_CHECKS = {
    'T_carrier_consistent_functionals_are_elliptope':
        check_T_carrier_consistent_functionals_are_elliptope,
    'T_two_models_center_and_extreme': check_T_two_models_center_and_extreme,
    'L_missing_lemma_is_center_selection':
        check_L_missing_lemma_is_center_selection,
    'T_trace_is_determinant_maximal': check_T_trace_is_determinant_maximal,
    'L_word_route_strengthenings': check_L_word_route_strengthenings,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


if __name__ == "__main__":
    run_all()
