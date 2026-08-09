"""The no-discount route: the signed 2-set system, its unique solution, the chain closure.

Built 2026-08-03 by a cold build seat on Ethan Brooke's R1/R2 ruling of
2026-08-03 (``Reference - RULING MEMO - The Independence Fork and the
No-Discount Route (2026-08-03)``): R1 adopts the no-discount route as the
charter's Branch D candidate over the independence fork; R2 charters this
build. Research successor to ``apf/word_carrier_transfer.py`` and
``apf/carrier_elliptope.py``, whose machinery it imports.

AUDIT RECORD: blinded cold audits LAND-WITH-FIXES 0.86 (2026-08-03) +
LAND-WITH-FIXES 0.87 different-day second audit with manifest access
(2026-08-04); fixes carried by separate fix seats each round. Banked
v24.3.465 (2026-08-04).

THE NAMED RESIDUAL, first and plainly (memo Sec. 4). The premise
MD_SUPER_NODISCOUNT -- no superposition of k distinct separators is
enforced at a discount below its separator count, phi(x*x) >= k eps, an
inequality with +-1 coefficients and 2-element sets sufficing -- is
CONSUMED HERE AND NOT DERIVED. It asserts two things this module cannot
and does not establish: (i) that phi(x*x) is the enforcement cost of the
presentation x (load semantics -- adjacent to, but not the same as, the
H4 QUADRATIC_LEDGER posit; do not conflate, that fence stands); (ii) that
MD's "costs do not cancel" applies at the realized level, to signed
superpositions the carrier itself cannot write. This module computes what
follows if the premise is granted. It does not certify the premise, price
it, or move its epistemic status. Every returned record carries it: the
``conditional_on`` field is the sorted residual-premise list.

------------------------------------------------------------------------------
WHAT THIS MODULE COMPUTES (exact arithmetic; stdlib + fractions; shared
machinery imported from the two held siblings, not duplicated)
------------------------------------------------------------------------------

Setting, inherited: the carrier-consistent functionals on the symmetric
test sector are parametrized by symmetric W with diag W = eps (the
elliptope module's E1); the diagonal value eps is the word module's
A2-argmin transfer at the uniform floor, not a stipulation. Separators
realize as matrix units s_ij -> E_ij (LINEAR_REALIZATION_TARGET); a
signed superposition of a 2-element separator set is x = e1 E_ab + e2
E_cd with e in {+1,-1}; its cost under W is phi_W(x^T x).

N1 -- THE SIGNED 2-SET SYSTEM AND ITS UNIQUE SOLUTION
(check_T_nodiscount_center_selection). The full inequality system
{ phi_W(x^T x) >= 2 eps : x a signed 2-element separator combination },
built by matrix arithmetic at n = 3, 4, 5 (and re-run at a scaled eps).
Computed facts: (a) every form has constant part exactly 2 eps, so the
center W = eps I satisfies EVERY inequality with zero slack -- 60 / 264 /
760 forms; (b) the forms that constrain the off-diagonal at all number
12 / 48 / 120 (n x C(n-1,2) source-sharing sets times four sign
patterns; the memo's "12 and 48 inequality forms" at n = 3, 4 is
reproduced exactly under that count); (c) every binding form is an AXIS
form -- exactly one nonzero coefficient, +-2, on a single unknown W_ij,
and its set shares a source vertex; the binding sets are EXACTLY the
source-sharing sets (target-sharing, chain, disjoint and reversed pairs
all contribute constant forms); (d) since both +2 W_ij >= 0 and
-2 W_ij >= 0 appear for every unknown, the solution set on the symmetric
slice is the single point W = eps I -- the forced-solution vector is
computed from the rows and covers every unknown; (e) every +- off-diagonal
perturbation of the center (six signed magnitudes per unknown) violates
at least one form, by computed negative minimum slack; (f) the memo's two
hand identities, phi((s01 +- s02)^T (s01 +- s02)) = 2 eps +- 2 W_12, as
explicit legs -- computed by an independent double-sum path AND matched
against the system builder's row for that set, at base and scaled eps;
(g) every binding row's signed combination is RANK-DEFICIENT (matrix
rank 1 against |S| = 2, computed for every binding row at every run),
and either restricted reading empties the binding set: admitting only
full-rank signed combinations leaves 36 / 168 / 520 rows and ZERO
binding, admitting only vertex-disjoint sets leaves 0 / 48 / 240 rows
and ZERO binding (n = 3, 4, 5). The independence fork is therefore
RESTATED here, not demoted: the rank-deficient sets the fork contests
are exactly the sets that carry the inequality's off-diagonal content,
inherited with >= in place of =. Anyone who denies that
|0>(<1| +- <2|) resolves two distinctions will equally deny that it
costs at least 2 eps.

N2 -- THE RECOVERED EQUALITY (check_L_recovered_k_resolution_equality).
The missing lemma demanded an EQUALITY: phi(x*x) = k eps for
superpositions of k separators. The no-discount route does not assume it;
it gets it back: granted the inequality, N1 forces W = eps I, and AT THE
CENTER the equality holds for every signed and unsigned separator set of
sizes 2 and 3 -- computed over all 220 forms at n = 3 (and again at a
scaled eps) and all 2024 at n = 4, with the diagonal part Tr(x^T x) = k
verified separately (the equality's entire off-diagonal content vanishes
at the center). The discount control, at base and scaled eps: at
W_12 = +eps/2 the minus combination prices at eps < 2 eps, at
W_12 = -eps/2 the plus combination does -- EITHER sign of the
off-diagonal hands one signed combination a discount, which is the
memo's Sec. 3 mechanism, here as exact values.

Over the parametrized family the two premises are EQUIVALENT: the
no-discount inequality and the missing-lemma equality have the same
solution set {W = eps I} on the symmetric slice (the inequality half is
N1's computation in this module; the equality half is
check_L_missing_lemma_is_center_selection in carrier_elliptope,
kernel zero at n = 3, 4), so the recovered
equality is the converse half of an equivalence -- the premise trade is
a change of vocabulary and of plausibility, not of logical content. The
+-1 coefficient restriction in the premise as written is NECESSARY: at
the center, x = (s01 + s02)/2 prices eps/2, below 2 eps (computed). The
norm-relative general form (auditor-supplied) carries no such
restriction: phi(x*x) >= eps*||x||_F^2 for all x iff W - eps I is PSD,
and a PSD matrix with zero diagonal is zero, so diag W = eps forces
W = eps I for all n and all real coefficients. A leg computes sampled
instances and finite witnesses at n = 3, base and scaled eps: at the center the bound holds
with exact EQUALITY on every sample; at a strict-slack W (diagonal
2 eps) it holds as an inequality; at two violating W (the family point
W_12 = eps/2 and the all-ones eps J) the rational witness x = s01 - s02
prices below eps*||x||_F^2 (at eps and at ZERO respectively); and a
sampled family scan passes the PSD test only at the center. A second leg
computes the countermodel: W = eps J has the word-route diagonal (tied
by value to the argmin diagonal), is PSD by principal minors, and prices
(s01 - s02)^T (s01 - s02) at exactly ZERO -- the no-discount inequality
excludes a functional the carrier machinery itself produces, which is
the premise's exclusionary content as a computed fact.

N3 -- THE CHAIN CLOSURE (check_T_chain_closure_sandwich_symmetry). The
word module's argmin diagonal is recomputed (psi(E_ii) = eps at the
uniform floor, n = 3 and 4). The sandwich-symmetry fact: b^T e b is
symmetric for symmetric e -- computed over a 3 x 3 rational sample grid
(nine sandwich elements from PSD effect samples, PSD computed by
principal minors, through non-symmetric b samples; the control
sandwiches a non-symmetric e through a NON-IDENTITY b and comes out
non-symmetric); therefore every antisymmetric coefficient
matrix scores ZERO on every sandwich element (computed, with a nonzero
control on a non-symmetric element) -- the antisymmetric freedom is inert
for sandwich scores. The conjunction leg then computes, in one tied
expression: {the N1 system's forced solution, recomputed at n = 3 and 4,
covers every unknown and forces zero} AND {the argmin diagonal is eps}
AND {the sample sandwich elements are symmetric} AND {the functional
whose off-diagonal is the forced dictionary agrees with eps*Tr on
every sample sandwich element, at base and scaled diagonal, while a
control functional with a NON-FORCED off-diagonal disagrees on at least
one element at each scale}. That is the computed form of: no-discount premise + argmin
diagonal + elliptope parametrization pin psi = eps*Tr on all
sandwich-readable elements at the computed sizes.

N4 -- PREMISES AS DATA (check_L_premise_inventory_set_exact). The
consumed and not-consumed premise sets are module-level data, compared
set-exactly against explicit literals; a leg verifies the two sets are
disjoint, that no forbidden premise appears in the consumed set, and that
MD_SUPER_NODISCOUNT is flagged as the named residual inside the consumed
set. The imported machinery's premises are carried, not hidden: the
consumed set contains the word module's full inventory plus the elliptope
module's REAL_SYMMETRIC_TEST_SECTOR.

READING, in this docstring and in NO leg and NO returned field: a nonzero
off-diagonal W_12 is a cost cancellation between two enforced
distinctions -- either sign of it enforces one signed combination below
its separator count -- and MD forbids cancellations. On that reading,
Born pricing is the unique no-discount pricing ON THE SYMMETRIC SLICE --
the qualifier the elliptope sibling's sector premise fences: every
x^T x is symmetric, and the antisymmetric freedom scores zero on every
symmetric element (N3's inertness computation), so the forms decide
nothing off the slice. The independence fork is restated, not demoted:
the contentious rank-deficient sets enter through an inequality in MD's
own vocabulary rather than through an exact-pricing claim -- >= in place
of =, on the same sets (N1 (g)). Whether MD's non-cancellation clause
reaches signed superpositions the carrier cannot write is exactly the
residual premise, and it is not decided here.

eps NOTE: eps enters only through the word module's probed_eps() (the
singleton probe on the banked ``symmetry_cost_floor.config_cost``). An
extensionally correct bypass of that probe is invisible BY EXTENSIONALITY
(the siblings' note, carried). At the unit probe eps = 1, so any mutation
substituting a value-equal literal for eps is likewise invisible by
extensionality. The scaled re-runs (3*eps in N1/N2, 3*eps diagonal in
N3) are leg content: each leg that consumes them asserts two distinct
scales, tied by value (scaled == 3 * base).

------------------------------------------------------------------------------
PREMISES, SET-EXACT (carried as data below; declarations, audited from
outside, not self-enforced)
------------------------------------------------------------------------------
CONSUMED: MD_SUPER_NODISCOUNT (THE NAMED RESIDUAL, memo Sec. 4 -- see the
status block; not derived here); LINEAR_REALIZATION_TARGET (signed
combinations exist in the target); FD3_FLOOR; FD4_FINITE_CARRIER;
A2_ARGMIN (the word-route diagonal); REAL_SYMMETRIC_TEST_SECTOR; plus the
imported word machinery's DEF_APS_STRUCTURE_COST, EQUAL_COST_UNIFORMITY,
CARRIER_COMPLETENESS, NONEMPTY_ENFORCEMENT_PRESENTATION.
NOT CONSUMED: P1_SANDWICH_REALIZATION; P2_PRESENTATION_GAUGE;
P3_UNDERIVED; CYCLICITY; PHI_EQ_EPS_TR_STIPULATION (the trace form is
here the unique solution of the inequality system, not a declaration);
DET_MAX_SELECTION_PRINCIPLE (no longer load-bearing for this route, per
the memo's R3); MISSING_LEMMA_EQUALITY_AS_PREMISE (the equality is
recovered at the solution, N2 -- it is an output, not an input).

MAY NOT CITE, while the residual is undischarged:
- "Born is derived." The conclusion is conditional on the named residual.
- "MD implies Born." Whether MD's clause reaches signed superpositions is
  the residual itself (memo Sec. 4 (ii)), not a theorem here.
- "The residual is discharged" / "MD_SUPER_NODISCOUNT is proved". It is
  consumed as a premise and flagged as such in the data.
- "The carrier gap is closed" / "the missing lemma is proved". The
  equality of N2 is recovered CONDITIONALLY, at the solution the premise
  forces; over the family the premise and the equality are EQUIVALENT
  (same solution set), so the carrier crossing is restated in MD's
  vocabulary, not removed.
- Any sentence attributing content here to what the module PREVENTS. It
  computes; it does not prevent.
"""

from fractions import Fraction as F
from itertools import combinations, product

from apf.word_carrier_transfer import (
    probed_eps, matmul, unit_matrix, argmin_values, uniform_cost,
)
from apf.carrier_elliptope import (
    mt, sym_from_offdiag, matrix_rank, psd_by_minors,
    PREMISES_CONSUMED as ELL_PREMISES_CONSUMED,
)

# ---------------------------------------------------------------------------
# premises as data (N4)
# ---------------------------------------------------------------------------

PREMISES_CONSUMED = frozenset(ELL_PREMISES_CONSUMED) | frozenset({
    "MD_SUPER_NODISCOUNT",
})
RESIDUAL_PREMISES = frozenset({
    "MD_SUPER_NODISCOUNT",
})
PREMISES_NOT_CONSUMED = frozenset({
    "P1_SANDWICH_REALIZATION", "P2_PRESENTATION_GAUGE", "P3_UNDERIVED",
    "CYCLICITY", "PHI_EQ_EPS_TR_STIPULATION", "DET_MAX_SELECTION_PRINCIPLE",
    "MISSING_LEMMA_EQUALITY_AS_PREMISE",
})

# ---------------------------------------------------------------------------
# exact helpers (only what the siblings do not already export)
# ---------------------------------------------------------------------------

def separators(n):
    """The ordered separators s_ij, i != j, realized as matrix units E_ij."""
    return [(i, j) for i in range(n) for j in range(n) if i != j]

def signed_combo(n, S, signs):
    """x = sum_t signs[t] * E_{S[t]} as an exact n x n matrix."""
    x = [[F(0)] * n for _ in range(n)]
    for (i, j), e in zip(S, signs):
        x[i][j] += e
    return x

def phi_of(W, M, n):
    """phi_W(M) = sum_ij W_ij M_ij, the coefficient-matrix pairing."""
    return sum(W[i][j] * M[i][j] for i in range(n) for j in range(n))

def fro2(x, n):
    """||x||_F^2 = sum_ij x_ij^2, exact."""
    return sum(x[i][j] * x[i][j] for i in range(n) for j in range(n))

def mat_sub(P, Q, n):
    """P - Q, exact."""
    return [[P[i][j] - Q[i][j] for j in range(n)] for i in range(n)]

def nodiscount_system(n, eps):
    """Every signed 2-element separator-set form at size n. Returns
    (rows, unknowns): unknowns are the off-diagonal positions (i, j),
    i < j, of the symmetric slice W = eps*I + w; each row is
    (coeff, const, S, signs) representing phi_W(x^T x) = const + coeff.w,
    so the no-discount inequality for the row reads
    const + coeff.w >= 2*eps."""
    seps = separators(n)
    unk = [(i, j) for i in range(n) for j in range(i + 1, n)]
    rows = []
    for S in combinations(seps, 2):
        for signs in product((1, -1), repeat=2):
            x = signed_combo(n, S, signs)
            g = matmul(mt(x, n), x, n)
            const = eps * sum(g[i][i] for i in range(n))
            coeff = tuple(g[i][j] + g[j][i] for (i, j) in unk)
            rows.append((coeff, const, S, signs))
    return rows, unk

def forced_solution(rows, unk, eps):
    """The axis-pair deduction: a row with exactly one nonzero
    coefficient c on unknown u and constant part exactly 2*eps reads
    c * w_u >= 0; the pair {+2 w_u >= 0, -2 w_u >= 0} forces w_u = 0.
    Returns (axis_pairs, forced) where forced maps each unknown position
    covered by BOTH signs to F(0); an uncovered unknown is absent (the
    caller must check coverage)."""
    axis_pairs = set()
    for coeff, const, S, signs in rows:
        nz = [(u, c) for u, c in enumerate(coeff) if c != 0]
        if len(nz) == 1 and const == 2 * eps:
            axis_pairs.add(nz[0])
    forced = {}
    for u, pos in enumerate(unk):
        if {(u, F(2)), (u, F(-2))} <= axis_pairs:
            forced[pos] = F(0)
    return axis_pairs, forced

# ---------------------------------------------------------------------------
# result plumbing: set-exact leg inventory enforced on the check path
# ---------------------------------------------------------------------------

EXPECTED_LEGS = {
    "check_T_nodiscount_center_selection": [
        "binding_row_counts_12_48_120",
        "binding_rows_all_axis_and_source_sharing",
        "binding_sets_rank_deficient_restrictions_empty",
        "center_satisfies_every_form_with_zero_slack",
        "every_offdiagonal_perturbation_violates",
        "hand_identity_plus_minus_two_w12",
        "unique_solution_forced_zero_all_unknowns",
    ],
    "check_L_recovered_k_resolution_equality": [
        "center_equality_all_signed_sets_sizes_2_3",
        "countermodel_epsJ_prices_zero",
        "diagonal_part_trace_equals_k",
        "either_sign_of_offdiagonal_hands_a_discount",
        "norm_relative_psd_sampled_witnessed",
        "unsigned_subset_counted",
    ],
    "check_T_chain_closure_sandwich_symmetry": [
        "antisymmetric_freedom_inert_with_control",
        "argmin_diagonal_eps_at_uniform_floor",
        "conjunction_pins_eps_trace_on_sandwich",
        "sandwich_symmetric_with_nonsymmetric_control",
    ],
    "check_L_premise_inventory_set_exact": [
        "consumed_set_exact",
        "forbidden_absent_and_disjoint",
        "not_consumed_set_exact",
        "residual_named_and_inside_consumed",
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
        "name": name,
        "passed": not fails,
        "legs": dict(legs),
        "fails": list(fails),
        "key_result": key_result,
        "conditional_on": sorted(RESIDUAL_PREMISES),
        "tier": 3,
        "epistemic": "P_math",
        "status": "banked v24.3.465 (2026-08-04)",
    }

# ---------------------------------------------------------------------------
# N1
# ---------------------------------------------------------------------------

def check_T_nodiscount_center_selection():
    legs, fails = {}, []
    eps = probed_eps()[0]
    runs = [(3, eps), (4, eps), (5, eps), (3, 3 * eps)]
    totals, slack_ok, binding_counts = [], [], []
    axis_ok, forced_ok, pert_mins = [], [], []
    unk_sizes, src_counts, per_set_ok = [], [], []
    rank_ok, restr = [], []
    for n, e in runs:
        rows, unk = nodiscount_system(n, e)
        unk_sizes.append(len(unk))
        totals.append(len(rows))
        slacks = [const - 2 * e for coeff, const, S, signs in rows]
        slack_ok.append(all(s == 0 for s in slacks))
        binding = [(coeff, S, signs) for coeff, const, S, signs in rows
                   if any(c != 0 for c in coeff)]
        binding_counts.append(len(binding))
        ax = len(binding) > 0
        for coeff, S, signs in binding:
            nz = [(u, c) for u, c in enumerate(coeff) if c != 0]
            ax = ax and len(nz) == 1 and nz[0][1] in (F(2), F(-2))
            ax = ax and len({a for (a, b) in S}) == 1
        src_sets = {S for S in {r[2] for r in rows}
                    if len({a for (a, b) in S}) == 1}
        ax = ax and ({S for _, S, _ in binding} == src_sets)
        axis_ok.append(ax)
        src_counts.append(len(src_sets))
        per_set = {}
        for _, S, _ in binding:
            per_set[S] = per_set.get(S, 0) + 1
        per_set_ok.append(set(per_set) == src_sets and len(per_set) > 0
                          and all(v == 4 for v in per_set.values()))
        rank_ok.append(len(binding) > 0 and all(
            matrix_rank(signed_combo(n, S, signs)) < len(S)
            for _, S, signs in binding))
        fr_bind = fr_total = vd_bind = vd_total = 0
        for coeff, const, S, signs in rows:
            b = any(c != 0 for c in coeff)
            if matrix_rank(signed_combo(n, S, signs)) == len(S):
                fr_total += 1
                fr_bind += 1 if b else 0
            if len({v for ij in S for v in ij}) == 2 * len(S):
                vd_total += 1
                vd_bind += 1 if b else 0
        restr.append((fr_bind, fr_total, vd_bind, vd_total))
        axis_pairs, forced = forced_solution(rows, unk, e)
        want = {(u, v) for u in range(len(unk)) for v in (F(2), F(-2))}
        forced_ok.append(axis_pairs == want
                         and sorted(forced) == sorted(unk)
                         and all(v == F(0) for v in forced.values()))
        deltas = [e, -e, e / 2, -e / 2, e / 7, -e / 7]
        for u in range(len(unk)):
            for d in deltas:
                w = [F(0)] * len(unk)
                w[u] = d
                pert_mins.append(min(
                    sum(c * wv for c, wv in zip(coeff, w))
                    for coeff, S, signs in binding))
    legs["center_satisfies_every_form_with_zero_slack"] = (
        totals == [60, 264, 760, 60] and slack_ok == [True] * 4
        and [n for n, _ in runs] == [3, 4, 5, 3]
        and len({e for _, e in runs}) == 2
        and runs[3][1] == 3 * runs[0][1] and runs[3][1] != runs[0][1])
    legs["binding_row_counts_12_48_120"] = (
        binding_counts == [12, 48, 120, 12]
        and src_counts == [3, 12, 30, 3]
        and binding_counts == [4 * c for c in src_counts]
        and per_set_ok == [True] * 4)
    legs["binding_rows_all_axis_and_source_sharing"] = (
        axis_ok == [True] * 4)
    legs["binding_sets_rank_deficient_restrictions_empty"] = (
        rank_ok == [True] * 4
        and restr == [(0, 36, 0, 0), (0, 168, 0, 48),
                      (0, 520, 0, 240), (0, 36, 0, 0)])
    legs["unique_solution_forced_zero_all_unknowns"] = (
        forced_ok == [True] * 4 and unk_sizes == [3, 6, 10, 3])
    legs["every_offdiagonal_perturbation_violates"] = (
        len(pert_mins) == 6 * (3 + 6 + 10 + 3)
        and all(m < 0 for m in pert_mins))
    # the memo's two hand identities, by an independent double-sum path
    # and by row lookup in the system builder, at base and scaled eps
    hand, hand_es = [], []
    for e in (eps, 3 * eps):
        hand_es.append(e)
        w_val = e / 3
        Wp = sym_from_offdiag(3, e, {(1, 2): w_val})
        vals = {}
        for sgn in (1, -1):
            x = signed_combo(3, ((0, 1), (0, 2)), (1, sgn))
            g = matmul(mt(x, 3), x, 3)
            vals[sgn] = phi_of(Wp, g, 3)
        rows3, unk3 = nodiscount_system(3, e)
        rp = [r for r in rows3
              if r[2] == ((0, 1), (0, 2)) and r[3] == (1, 1)]
        rm = [r for r in rows3
              if r[2] == ((0, 1), (0, 2)) and r[3] == (1, -1)]
        hand.append(
            vals[1] == 2 * e + 2 * w_val
            and vals[-1] == 2 * e - 2 * w_val
            and vals[1] != vals[-1]
            and len(rp) == 1 and len(rm) == 1
            and rp[0][1] == 2 * e and rm[0][1] == 2 * e
            and rp[0][0] == (F(0), F(0), F(2))
            and rm[0][0] == (F(0), F(0), F(-2))
            and unk3 == [(0, 1), (0, 2), (1, 2)])
    legs["hand_identity_plus_minus_two_w12"] = (
        hand == [True, True] and len(hand_es) == 2
        and hand_es[1] == 3 * hand_es[0] and hand_es[0] != hand_es[1])
    return _result("check_T_nodiscount_center_selection", legs, fails,
                   {"row_totals": totals,
                    "binding_counts": binding_counts,
                    "perturbation_tests": len(pert_mins),
                    "runs": [[n, str(e)] for n, e in runs]})

# ---------------------------------------------------------------------------
# N2
# ---------------------------------------------------------------------------

def check_L_recovered_k_resolution_equality():
    legs, fails = {}, []
    eps = probed_eps()[0]
    runs = [(3, eps), (4, eps), (3, 3 * eps)]
    totals, eq_ok, tr_ok, unsigned_counts = [], [], [], []
    for n, e in runs:
        Wc = sym_from_offdiag(n, e, {})
        seps = separators(n)
        phis, ks, trs = [], [], []
        unsigned = 0
        for k in (2, 3):
            for S in combinations(seps, k):
                for signs in product((1, -1), repeat=k):
                    x = signed_combo(n, S, signs)
                    g = matmul(mt(x, n), x, n)
                    phis.append(phi_of(Wc, g, n))
                    ks.append(k)
                    trs.append(sum(g[i][i] for i in range(n)))
                    if all(s == 1 for s in signs):
                        unsigned += 1
        totals.append(len(phis))
        eq_ok.append(phis == [F(k) * e for k in ks]
                     and len(phis) == len(ks) and len(phis) > 0)
        tr_ok.append(trs == [F(k) for k in ks] and len(trs) == len(ks))
        unsigned_counts.append(unsigned)
    legs["center_equality_all_signed_sets_sizes_2_3"] = (
        eq_ok == [True] * 3 and totals == [220, 2024, 220]
        and [n for n, _ in runs] == [3, 4, 3]
        and len({e for _, e in runs}) == 2
        and runs[2][1] == 3 * runs[0][1] and runs[2][1] != runs[0][1])
    legs["diagonal_part_trace_equals_k"] = (tr_ok == [True] * 3)
    # ties the COUNT of all-plus sign tuples, not their identity; the
    # all-minus subset yields the same count by sign symmetry
    legs["unsigned_subset_counted"] = (unsigned_counts == [35, 286, 35])
    # the discount mechanism, as exact values, at base and scaled eps:
    # either sign of W_12 hands one of the two signed combinations a
    # price below 2*e
    disc = []
    for e in (eps, 3 * eps):
        for w_off in (e / 2, -e / 2):
            Woff = sym_from_offdiag(3, e, {(1, 2): w_off})
            vals = []
            for sgn in (1, -1):
                x = signed_combo(3, ((0, 1), (0, 2)), (1, sgn))
                g = matmul(mt(x, 3), x, 3)
                vals.append(phi_of(Woff, g, 3))
            disc.append((e, min(vals)))
    legs["either_sign_of_offdiagonal_hands_a_discount"] = (
        len(disc) == 4
        and [m for _, m in disc] == [e for e, _ in disc]
        and all(m < 2 * e for e, m in disc)
        and len({e for e, _ in disc}) == 2
        and disc[2][0] == 3 * disc[0][0] and disc[2][0] != disc[0][0])
    # the norm-relative general form, sampled instances and finite
    # witnesses, base and scaled:
    # phi_W(x^T x) >= e * ||x||_F^2 (sampled / witnessed) against
    # psd_by_minors(W - e*I), with the sampled family scan passing the
    # PSD test only at the center
    iff_ok, iff_es = [], []
    for e in (eps, 3 * eps):
        iff_es.append(e)
        xs = [
            [[F(0), F(1, 2), F(1, 2)], [F(0)] * 3, [F(0)] * 3],
            signed_combo(3, ((0, 1), (0, 2)), (1, -1)),
            [[F(1), F(1, 2), F(0)], [F(0), F(1), F(-1)],
             [F(2), F(0), F(1, 3)]],
            unit_matrix(3, 0, 0),
        ]
        gs = [matmul(mt(x, 3), x, 3) for x in xs]
        eI = sym_from_offdiag(3, e, {})
        Wc = sym_from_offdiag(3, e, {})
        Wa = sym_from_offdiag(3, 2 * e, {(0, 1): e / 2, (0, 2): e / 2,
                                         (1, 2): e / 2})
        dir_a = (psd_by_minors(mat_sub(Wc, eI, 3))
                 and psd_by_minors(mat_sub(Wa, eI, 3))
                 and len(xs) == 4
                 and all(phi_of(Wc, g, 3) == e * fro2(x, 3)
                         for x, g in zip(xs, gs))
                 and all(phi_of(Wa, g, 3) >= e * fro2(x, 3)
                         for x, g in zip(xs, gs)))
        half = phi_of(Wc, gs[0], 3)
        necess = (half == e / 2 and half < 2 * e
                  and half == e * fro2(xs[0], 3))
        Wb1 = sym_from_offdiag(3, e, {(1, 2): e / 2})
        WbJ = sym_from_offdiag(3, e, {(0, 1): e, (0, 2): e, (1, 2): e})
        dir_b = ((not psd_by_minors(mat_sub(Wb1, eI, 3)))
                 and (not psd_by_minors(mat_sub(WbJ, eI, 3)))
                 and phi_of(Wb1, gs[1], 3) == e
                 and phi_of(Wb1, gs[1], 3) < e * fro2(xs[1], 3)
                 and phi_of(WbJ, gs[1], 3) == F(0)
                 and phi_of(WbJ, gs[1], 3) < e * fro2(xs[1], 3))
        fam = [psd_by_minors(mat_sub(sym_from_offdiag(3, e, {(i, j): mv}),
                                     eI, 3))
               for (i, j) in ((0, 1), (0, 2), (1, 2))
               for mv in (e, -e, e / 2, -e / 2)]
        center_only = (fam == [False] * 12 and len(fam) == 12
                       and psd_by_minors(mat_sub(Wc, eI, 3)))
        iff_ok.append(dir_a and necess and dir_b and center_only)
    legs["norm_relative_psd_sampled_witnessed"] = (
        iff_ok == [True, True] and len(iff_es) == 2
        and iff_es[1] == 3 * iff_es[0] and iff_es[0] != iff_es[1])
    # the countermodel: W = eps*J has the word-route diagonal, is PSD,
    # and prices (s01 - s02)^T (s01 - s02) at exactly zero
    WJ = [[eps for _ in range(3)] for _ in range(3)]
    vals3, _ = argmin_values(uniform_cost(3, eps), 6, "set",
                             closed_only=True)
    xm = signed_combo(3, ((0, 1), (0, 2)), (1, -1))
    gm = matmul(mt(xm, 3), xm, 3)
    pj = phi_of(WJ, gm, 3)
    legs["countermodel_epsJ_prices_zero"] = (
        [WJ[i][i] for i in range(3)] == [vals3[(i, i)] for i in range(3)]
        and [WJ[i][i] for i in range(3)] == [eps] * 3
        and psd_by_minors(WJ)
        and pj == F(0) and pj < 2 * eps)
    return _result("check_L_recovered_k_resolution_equality", legs, fails,
                   {"equality_forms_checked": totals,
                    "unsigned_forms": unsigned_counts,
                    "discount_minima": [str(m) for _, m in disc]})

# ---------------------------------------------------------------------------
# N3
# ---------------------------------------------------------------------------

def check_T_chain_closure_sandwich_symmetry():
    legs, fails = {}, []
    eps = probed_eps()[0]
    diags = []
    for n in (3, 4):
        vals, _ = argmin_values(uniform_cost(n, eps), 6, "set",
                                closed_only=True)
        diags.append([vals[(i, i)] for i in range(n)])
    legs["argmin_diagonal_eps_at_uniform_floor"] = (
        diags == [[eps] * 3, [eps] * 4])
    n = 3
    b_samples = [
        [[F(1), F(2), F(0)], [F(0), F(1), F(-1)], [F(3), F(0), F(1)]],
        [[F(0), F(1), F(1)], [F(1), F(0), F(2)], [F(-1), F(1), F(0)]],
        [[F(2), F(0), F(0)], [F(0), F(3), F(0)], [F(0), F(0), F(5)]],
    ]
    e_samples = [
        [[F(1), F(0), F(2)], [F(0), F(1), F(0)], [F(2), F(0), F(5)]],
        [[F(2), F(1), F(0)], [F(1), F(2), F(1)], [F(0), F(1), F(2)]],
        [[F(1), F(0), F(0)], [F(0), F(1), F(0)], [F(0), F(0), F(1)]],
    ]
    e_sym_flags = [e == mt(e, n) for e in e_samples]
    e_psd_flags = [psd_by_minors(e) for e in e_samples]
    sandwiches, sym_flags = [], []
    for e in e_samples:
        for b in b_samples:
            M = matmul(matmul(mt(b, n), e, n), b, n)
            sandwiches.append(M)
            sym_flags.append(M == mt(M, n))
    e_ns = unit_matrix(n, 0, 1)
    b_ctl = b_samples[0]
    b_id = [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]
    M_ns = matmul(matmul(mt(b_ctl, n), e_ns, n), b_ctl, n)
    legs["sandwich_symmetric_with_nonsymmetric_control"] = (
        sym_flags == [True] * 9 and len(sandwiches) == 9
        and e_sym_flags == [True] * 3
        and e_psd_flags == [True] * 3
        and len(set(str(M) for M in sandwiches)) > 1
        and e_ns != mt(e_ns, n)
        and b_ctl != b_id
        and M_ns != mt(M_ns, n))
    A = [[F(0), F(3), F(-1)], [F(-3), F(0), F(2)], [F(1), F(-2), F(0)]]
    inert_vals = [phi_of(A, M, n) for M in sandwiches]
    control_val = phi_of(A, unit_matrix(n, 0, 1), n)
    legs["antisymmetric_freedom_inert_with_control"] = (
        A == [[-A[j][i] for j in range(n)] for i in range(n)]
        and inert_vals == [F(0)] * 9 and len(inert_vals) == 9
        and control_val == F(3) and control_val != 0)
    # the conjunction: {no-discount system's forced solution, recomputed}
    # + {argmin diagonal} + {sandwich symmetry} pin psi = eps*Tr on every
    # sample sandwich element; the off-diagonal dictionary handed to the
    # constructor is the forced solution, and a
    # control functional with a non-forced off-diagonal disagrees with
    # the trace on at least one sandwich element at each scale
    forced_cover = []
    for m in (3, 4):
        rows, unk = nodiscount_system(m, eps)
        axis_pairs, forced = forced_solution(rows, unk, eps)
        want = {(u, v) for u in range(len(unk)) for v in (F(2), F(-2))}
        forced_cover.append(axis_pairs == want
                            and sorted(forced) == sorted(unk))
    rows3, unk3 = nodiscount_system(3, eps)
    _, forced3 = forced_solution(rows3, unk3, eps)
    off_used = dict(forced3)
    pin, bad_ctl, ds = [], [], []
    for scale in (F(1), F(3)):
        d = scale * eps
        ds.append(d)
        W_sol = sym_from_offdiag(3, d, off_used)
        psi_vals = [phi_of(W_sol, M, 3) for M in sandwiches]
        trace_vals = [d * sum(M[i][i] for i in range(3))
                      for M in sandwiches]
        pin.append(psi_vals == trace_vals and len(psi_vals) == 9
                   and len(set(str(v) for v in trace_vals)) > 1)
        W_bad = sym_from_offdiag(3, d, {(1, 2): d / 2})
        bad_vals = [phi_of(W_bad, M, 3) for M in sandwiches]
        bad_ctl.append(len(bad_vals) == 9
                       and any(bv != tv for bv, tv
                               in zip(bad_vals, trace_vals)))
    legs["conjunction_pins_eps_trace_on_sandwich"] = (
        forced_cover == [True, True]
        and sorted(forced3) == [(0, 1), (0, 2), (1, 2)]
        and sorted(off_used) == sorted(unk3)
        and len(off_used) == 3
        and diags[0] == [eps] * 3
        and sym_flags == [True] * 9
        and pin == [True, True]
        and bad_ctl == [True, True]
        and len(ds) == 2 and ds[1] == 3 * ds[0] and ds[0] != ds[1])
    return _result("check_T_chain_closure_sandwich_symmetry", legs, fails,
                   {"sandwich_elements": len(sandwiches),
                    "forced_offdiag_values": [str(v)
                                              for v in forced3.values()],
                    "diag_n3": [str(v) for v in diags[0]]})

# ---------------------------------------------------------------------------
# N4
# ---------------------------------------------------------------------------

def check_L_premise_inventory_set_exact():
    legs, fails = {}, []
    legs["consumed_set_exact"] = (
        sorted(PREMISES_CONSUMED) == [
            "A2_ARGMIN", "CARRIER_COMPLETENESS", "DEF_APS_STRUCTURE_COST",
            "EQUAL_COST_UNIFORMITY", "FD3_FLOOR", "FD4_FINITE_CARRIER",
            "LINEAR_REALIZATION_TARGET", "MD_SUPER_NODISCOUNT",
            "NONEMPTY_ENFORCEMENT_PRESENTATION",
            "REAL_SYMMETRIC_TEST_SECTOR",
        ]
        and ELL_PREMISES_CONSUMED < PREMISES_CONSUMED)
    legs["not_consumed_set_exact"] = (
        sorted(PREMISES_NOT_CONSUMED) == [
            "CYCLICITY", "DET_MAX_SELECTION_PRINCIPLE",
            "MISSING_LEMMA_EQUALITY_AS_PREMISE", "P1_SANDWICH_REALIZATION",
            "P2_PRESENTATION_GAUGE", "P3_UNDERIVED",
            "PHI_EQ_EPS_TR_STIPULATION",
        ])
    forbidden_hits = sorted(PREMISES_CONSUMED & PREMISES_NOT_CONSUMED)
    absent = [p for p in sorted(PREMISES_NOT_CONSUMED)
              if p not in PREMISES_CONSUMED]
    legs["forbidden_absent_and_disjoint"] = (
        forbidden_hits == [] and absent == sorted(PREMISES_NOT_CONSUMED)
        and len(absent) == 7)
    legs["residual_named_and_inside_consumed"] = (
        sorted(RESIDUAL_PREMISES) == ["MD_SUPER_NODISCOUNT"]
        and RESIDUAL_PREMISES < PREMISES_CONSUMED
        and not (RESIDUAL_PREMISES & PREMISES_NOT_CONSUMED))
    return _result("check_L_premise_inventory_set_exact", legs, fails,
                   {"consumed": len(PREMISES_CONSUMED),
                    "not_consumed": len(PREMISES_NOT_CONSUMED),
                    "residual": len(RESIDUAL_PREMISES),
                    "what_this_check_establishes":
                        "These legs read name lists declared in this "
                        "file and literal copies of them written in the "
                        "same file. PREMISES_CONSUMED, read by "
                        "consumed_set_exact, forbidden_absent_and_disjoint "
                        "and residual_named_and_inside_consumed, is built "
                        "from the premise set imported from "
                        "carrier_elliptope, and consumed_set_exact reads "
                        "that imported set directly as well. None "
                        "establishes that a "
                        "listed premise is consumed, that an unlisted one "
                        "is not, or that any name denotes anything, and a "
                        "rename carried on every copy is invisible here."})

# ---------------------------------------------------------------------------

ALL_CHECKS = [
    check_T_nodiscount_center_selection,
    check_L_recovered_k_resolution_equality,
    check_T_chain_closure_sandwich_symmetry,
    check_L_premise_inventory_set_exact,
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
    'T_nodiscount_center_selection': check_T_nodiscount_center_selection,
    'L_recovered_k_resolution_equality': check_L_recovered_k_resolution_equality,
    'T_chain_closure_sandwich_symmetry': check_T_chain_closure_sandwich_symmetry,
    'L_premise_inventory_set_exact': check_L_premise_inventory_set_exact,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


if __name__ == "__main__":
    run_all()
