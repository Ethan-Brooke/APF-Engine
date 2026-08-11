"""The correlation-elliptope bridge: containments and projections, computed exactly.

BANKED v24.3.470 (2026-08-11). Built to the frozen claim surface sha256
3207ac0577ee09c6092b9a99859e1e2316fd003acd52cdd56ca4c6e9ddf6a96d
(Artifacts_2026-08-11_session/s4_bridge/CLAIM_SURFACE_FROZEN_2026-08-11.md).
Two blinded cold audits, LAND-WITH-FIXES 0.86 / 0.87, zero arithmetic
disagreement in either; cold fix seat carried; receipts regenerated with
the fixed object. LIFTED by Ethan's ruling 2026-08-11. Records:
Artifacts_2026-08-11_session/{s4_bridge,returns}. BARE-NAME registry keys
per D6@2026-08-03.

------------------------------------------------------------------------------
WHAT THIS MODULE COMPUTES (exact rational arithmetic; stdlib + fractions)
------------------------------------------------------------------------------

B1 (geometry, check_B1_elliptope_strictly_contains_cut): the eps-scaled
elliptope {W psd, diag W = eps} strictly contains eps*CUT(K_n) at n = 3,
by an exhibited PSD matrix with the carrier diagonal violating an exhibited
facet whose validity is verified on every scaled cut vertex; both named
carrier points are inside the classical body (eps*I as barycentre with
explicit weights; eps*J as a scaled vertex with explicit sign vector).
eps is read through word_carrier_transfer.probed_eps(). The free-sector
dimension n(n-1)/2 is tied by value, at n = 3, 4, 5, to the nullity of the
commit-record resolution map computed through
counted_ledger_underdetermination's own helpers, and at n = 3 to the banked
check's returned evidence.

B2 (the projection, named, check_B2_projection_named): the (2,2,2) reading
of the gap lives on the PROJECTION of the elliptope onto the four
disjoint-party cross coordinates (the Tsirelson body), not on the elliptope.
S^2 < 8 holds on the witness and is NOT sufficient for membership
(counterexample E = (1, 1, 1/5, -1/5): the two forced completion values
differ, computed by exact polynomial interpolation). The banked CHSH witness value is PARSED
from T_correlation_ladder_exact_rational_chsh_witness's banked return and
its E-vector is read from that module's own IE declaration -- never a
literal here; the witness is outside the Boole polytope by CALLING
ijc_boolean_defender_bridge.feasbool_structural on it, and inside the body
by the genuine PSD completion of the actual witness at
(x, y) = (-7/100, -29/100), with a unit-diagonal leg and the cross block
pinned entrywise to a second in-process read of the banked surface. The disjoint-party
(2,2,2) cover is a CHOICE, disclosed as one in the returned record.

B3 (the containment direction, check_B3_projection_exit_implies_cut_exit):
every cut vector of K_5 restricts, on every disjoint-party cover, to a
deterministic Boole vertex satisfying every CHSH facet (executed
exhaustively: 32 vectors x 15 covers), which is the vertex-restriction
argument for: projection exit => full CUT exit. Its strictness: the
frustrated C_5 at magnitude 1/2 exits CUT(K_5) by a pentagonal facet at
depth 1/2 (facet validity verified on every cut vector; the balanced C_5
control has zero violations over the full odd hypermetric family
b in {-2..2}^5), while every one of the 15 disjoint-party covers is
Boole-feasible with facet maximum 3/2 -- each cover's maximum tied by value
to the banked decider's own returned value. The sign classes are tied to
global_defect_margin's parity law by value (chi and best defect fraction
computed through that module's own functions).

B4 (non-identity controls, check_B4_non_identity_controls): CERT1 -- the
frustrated triangle at magnitude 1/4 is PSD and INSIDE CUT(K_3) by explicit
nonnegative weights (frustration does not force exit); the same sign class
at magnitude 1/2 exits (the membership machinery discriminates). CERT4 --
the balanced-sign behaviour E = (24/25, 24/25, 4/5, 44/125) is realized by
explicit rational unit vectors (an elliptope point) and is OUTSIDE the
Boole polytope by the banked decider, at CHSH 296/125 (exit does not force
frustration). Both are permanent negative controls on any frustration-class
<-> exit-class identification; the identification is never stated here.

B5 (presentation content, check_B5_presentation_fraction): the counted
fraction of admissible signed presentations (complete-multipartite support,
signed unit coefficients on k distinct ordered off-diagonal cells) whose
loads X^T X carry a negative entry -- a certificate of leaving the
completely positive cone, since entrywise nonnegativity is necessary for
complete positivity -- stated per (n, k) with denominators and computed
percentages, never as a universal. The vacuous cells ((4,2) and all of
n = 5 under k in {2, 3}) are vacuous STRUCTURALLY: the minimal nonempty
complete-multipartite edge count exceeds k, computed by enumeration and
tied to the direct count of zero.

------------------------------------------------------------------------------
PREMISES
------------------------------------------------------------------------------
CONDITIONAL (declared per-check in `conditional_on`): the carrier-fixed
diagonal consumed by B1 and B2 rests on NONEMPTY_ENFORCEMENT_PRESENTATION
and on the SET support convention (psi_min(E_ii) = eps under SET);
REAL_SYMMETRIC_TEST_SECTOR travels with carrier_elliptope's parametrization,
which this module consumes and re-proves nothing of. B3, B4, B5 state facts
about correlation matrices, sign patterns, and loads as mathematical
objects; their conditional_on lists are empty.
FORBIDDEN_PREMISES is ENFORCED: _result() fails any check whose declared
premise records intersect the forbidden set (executed guard, not
decoration).

LEG INVENTORY (D7@2026-08-08, APPEND-AND-RECORD): _result() compares the
executed leg set against EXPECTED_LEGS set-exactly on the path the bank
would execute; a mismatch contributes a failure reason and does not raise.
STANDING LIMIT, disclosed: this certifies that a declared leg EXECUTED,
not that it COULD HAVE FAILED.

MAY NOT CITE (the frozen surface's never-stated list, binding here):
- "the two lanes are one lane" -- the excess-reachability computation is a
  SEPARATE named computation, still unrun.
- any frustration-class <-> exit-class identification (B4 carries the
  computed refutation in both directions).
- anything about entanglement or separability of quantum states (states
  never appear in this module; cones and polytopes do).
- "the framework is non-classical because its functional set exceeds the
  classical one" (eps*I is classical -- computed in B1).
- anything from real_form_chsh_countermodel.
This module describes what it COMPUTES. Identities and choices are
disclosed as such in the returned records.
"""

from fractions import Fraction as F
from itertools import combinations, product
import re

HELD_OUT_OF_THE_BANK = False  # lifted by Ethan's ruling 2026-08-11; banked v24.3.470

FORBIDDEN_PREMISES = frozenset({
    "COST_REPRESENTATION_ON_LOADS", "DEF_REALIZATION_SIGNED_CONTRACTION",
    "FD3_VALUATION_CONVENTION", "P1_SANDWICH_REALIZATION",
    "DAGGER_SANDWICH_REALIZATION", "ROOTLESS_LOOP_CYCLICITY",
    "P2_PRESENTATION_GAUGE", "MD_SUPER_NODISCOUNT",
})

DIAGONAL_PREMISES = ("NONEMPTY_ENFORCEMENT_PRESENTATION", "SET_SUPPORT_MODE")

EXPECTED_LEGS = {
    "check_B1_elliptope_strictly_contains_cut": [
        "all_ones_point_is_scaled_vertex",
        "center_is_barycentre_entrywise",
        "eps_probed_and_positive",
        "facets_valid_on_every_scaled_vertex",
        "free_sector_dim_tied_to_counted_ledger_nullity",
        "non_psd_control_rejected",
        "witness_in_elliptope_with_diagonal_pinned",
        "witness_violates_a_valid_scaled_facet",
    ],
    "check_B2_projection_named": [
        "banked_witness_return_parsed_not_restated",
        "completion_cross_block_pinned_to_banked_read",
        "completion_is_psd_with_unit_diagonal",
        "decider_called_on_the_witness_value_tied",
        "pr_box_control_has_no_completion",
        "s_squared_below_8_on_the_witness",
        "s_squared_insufficient_by_exact_counterexample",
        "witness_E_read_from_banked_surface_ties_value",
    ],
    "check_B3_projection_exit_implies_cut_exit": [
        "balanced_control_zero_violations_full_odd_family",
        "cut_vertices_restrict_to_boole_vertices",
        "every_cover_boole_feasible_max_tied_by_value",
        "frustrated_c5_exits_pentagonal_facet",
        "pentagonal_facet_valid_on_every_cut_vector",
        "sign_classes_tied_to_banked_parity_law",
    ],
    "check_B4_non_identity_controls": [
        "cert1_class_frustrated_by_banked_parity",
        "cert1_control_same_class_exits_at_magnitude_half",
        "cert1_frustrated_triangle_is_psd_unit_diagonal",
        "cert1_inside_cut_by_explicit_weights",
        "cert4_class_balanced_by_banked_parity",
        "cert4_exits_boole_decider_value_tied",
        "cert4_realized_by_explicit_unit_vectors",
        "cert4_second_decider_concurs",
    ],
    "check_B5_presentation_fraction": [
        "admissibility_filter_bites",
        "nonvacuous_cells_have_proper_fractions",
        "unsigned_control_loads_nonnegative",
        "vacuous_cells_vacuous_by_two_routes",
    ],
}

# ---------------------------------------------------------------------------
# exact helpers
# ---------------------------------------------------------------------------

def _psd(M):
    """Symmetric PSD over Q by symmetric Gaussian elimination (exact)."""
    n = len(M)
    M = [row[:] for row in M]
    for i in range(n):
        if M[i][i] < 0:
            return False
        if M[i][i] == 0:
            if any(M[i][j] != 0 for j in range(n)):
                return False
            continue
        for j in range(i + 1, n):
            f = M[j][i] / M[i][i]
            for k in range(i, n):
                M[j][k] -= f * M[i][k]
    # every pivot was sign-checked at its own iteration and row i never
    # changes after step i, so reaching here means no rejection remains
    return True


def _det(M):
    """Exact determinant by fraction Gaussian elimination with row swaps."""
    n = len(M)
    M = [row[:] for row in M]
    sign = 1
    for i in range(n):
        piv = next((r for r in range(i, n) if M[r][i] != 0), None)
        if piv is None:
            return F(0)
        if piv != i:
            M[i], M[piv] = M[piv], M[i]
            sign = -sign
        for r in range(i + 1, n):
            f = M[r][i] / M[i][i]
            for c in range(i, n):
                M[r][c] -= f * M[i][c]
    out = F(sign)
    for i in range(n):
        out *= M[i][i]
    return out


def _quad_coeffs(f):
    """Coefficients (c2, c1, c0) of a quadratic f by interpolation at
    0, 1, -1, with a fourth-point consistency check at 2 (the degree
    assumption is verified, not asserted)."""
    v0, v1, vm = f(F(0)), f(F(1)), f(F(-1))
    c2 = (v1 + vm - 2 * v0) / 2
    c1 = (v1 - vm) / 2
    c0 = v0
    if f(F(2)) != c2 * 4 + c1 * 2 + c0:
        raise AssertionError("_quad_coeffs: input is not quadratic")
    return (c2, c1, c0)


def _cut_vertex_offdiag_tuples(n):
    """Distinct off-diagonal coordinate tuples of the cut-polytope
    generators v v^T, v in {+-1}^n (unit scale)."""
    unk = list(combinations(range(n), 2))
    return sorted({tuple(F(v[i] * v[j]) for i, j in unk)
                   for v in product((1, -1), repeat=n)})


def _triangle_facets(n):
    """The triangle inequalities row.x >= -1 (unit scale) on the
    off-diagonal coordinates."""
    unk = list(combinations(range(n), 2))
    idx = {p: k for k, p in enumerate(unk)}
    out = []
    for (a, b, c) in combinations(range(n), 3):
        e = [idx[(a, b)], idx[(a, c)], idx[(b, c)]]
        for sg in ((1, 1, 1), (1, -1, -1), (-1, 1, -1), (-1, -1, 1)):
            row = [F(0)] * len(unk)
            for k, s in zip(e, sg):
                row[k] = F(s)
            out.append((tuple(row), F(-1)))
    return out


_C5_EDGES = ((0, 1), (1, 2), (2, 3), (3, 4), (0, 4))


def _c5_matrix(signs, mag):
    """Unit-diagonal C_5 correlation matrix: entries +-mag on the cycle
    edges (signs in cycle-edge order), zero on both chords."""
    C = [[F(1) if i == j else F(0) for j in range(5)] for i in range(5)]
    for (i, j), s in zip(_C5_EDGES, signs):
        C[i][j] = C[j][i] = F(s) * mag
    return C


def _hyper_form(bvec, C):
    """The hypermetric form Q_b(C) = sum_{i<j} b_i b_j C_ij."""
    m = len(bvec)
    return sum(F(bvec[i] * bvec[j]) * C[i][j]
               for i in range(m) for j in range(i + 1, m))


def _k5_cut_matrices():
    return [[[F(v[i] * v[j]) if i != j else F(1) for j in range(5)]
             for i in range(5)] for v in product((1, -1), repeat=5)]


def _disjoint_party_covers():
    """All 15 (4-subset, disjoint-bipartition) covers of K_5."""
    out = []
    for sub in combinations(range(5), 4):
        a, b, c, d = sub
        for (A, B) in (((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))):
            out.append((A, B))
    return out


def _cover_E(C, cover):
    (A, B) = cover
    return (C[A[0]][B[0]], C[A[0]][B[1]], C[A[1]][B[0]], C[A[1]][B[1]])


_CHSH_SIGNS = ((1, 1, 1, -1), (1, 1, -1, 1), (1, -1, 1, 1), (-1, 1, 1, 1),
               (-1, -1, -1, 1), (-1, -1, 1, -1), (-1, 1, -1, -1),
               (1, -1, -1, -1))


def _chsh_max(E):
    return max(sum(F(s) * e for s, e in zip(sg, E)) for sg in _CHSH_SIGNS)


def _partitions(coll):
    coll = list(coll)
    if not coll:
        yield []
        return
    first, rest = coll[0], coll[1:]
    for s in _partitions(rest):
        for i, b in enumerate(s):
            yield s[:i] + [[first] + b] + s[i + 1:]
        yield [[first]] + s


def _realizable_configs(n):
    """Separated-pair sets of partitions = complete multipartite edge sets."""
    out = set()
    for p in _partitions(range(n)):
        blk = {v: i for i, b in enumerate(p) for v in b}
        out.add(frozenset(frozenset((a, b))
                          for a, b in combinations(range(n), 2)
                          if blk[a] != blk[b]))
    return out


def _load_of(cells, signs, n):
    x = [[F(0)] * n for _ in range(n)]
    for (i, j), s in zip(cells, signs):
        x[i][j] += F(s)
    return [[sum(x[k][i] * x[k][j] for k in range(n)) for j in range(n)]
            for i in range(n)]


def _witness_completion(E, x, y):
    """The (2,2)-scenario Gram completion of a behaviour E at intra-party
    values (x, y): rows/cols ordered (a1, a2, b1, b2)."""
    return [[F(1), x, E[0], E[1]],
            [x, F(1), E[2], E[3]],
            [E[0], E[2], F(1), y],
            [E[1], E[3], y, F(1)]]


# ---------------------------------------------------------------------------
# result plumbing (append-and-record; forbidden premises enforced)
# ---------------------------------------------------------------------------

def _result(name, legs, key_result, conditional_on=(), choice_imports=(),
            cross_refs=(), disclosures=()):
    fails = []
    have = tuple(sorted(legs))
    want = tuple(EXPECTED_LEGS[name])
    if have != want:
        missing = sorted(set(want) - set(have))
        extra = sorted(set(have) - set(want))
        fails.append("leg inventory mismatch: missing=%s extra=%s"
                     % (missing, extra))
    hits = sorted(set(conditional_on) & FORBIDDEN_PREMISES)
    if hits:
        fails.append("forbidden premise declared: %s" % hits)
    for label in sorted(legs):
        ok, ev = legs[label]
        if not ok:
            fails.append("%s: %s" % (label, ev))
    return {
        "name": name,
        "passed": not fails,
        "tier": 3,
        "epistemic": "P_math",
        "legs": {k: {"passed": bool(v[0]), "evidence": v[1]}
                 for k, v in legs.items()},
        "leg_count": len(legs),
        "fail_reasons": fails,
        "key_result": key_result,
        "conditional_on": sorted(conditional_on),
        "choice_imports": list(choice_imports),
        "forbidden_premises": sorted(FORBIDDEN_PREMISES),
        "cross_refs": list(cross_refs),
        "disclosures": list(disclosures),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "inventory_note": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


# ---------------------------------------------------------------------------
# B1 -- geometry: the eps-scaled elliptope strictly contains eps*CUT(K_3)
# ---------------------------------------------------------------------------

def check_B1_elliptope_strictly_contains_cut():
    """B1: strict containment at n = 3 with the carrier diagonal pinned;
    both named carrier points classical; the free-sector dimension tied to
    the counted ledger's nullity by value at n = 3, 4, 5."""
    from apf.word_carrier_transfer import probed_eps
    import apf.counted_ledger_underdetermination as clu

    legs = {}
    eps = probed_eps()[0]
    legs["eps_probed_and_positive"] = (
        eps > 0, {"eps": str(eps), "read_through": "word_carrier_transfer.probed_eps()"})

    n = 3
    unk = list(combinations(range(n), 2))
    facets = _triangle_facets(n)
    verts = [tuple(eps * c for c in v) for v in _cut_vertex_offdiag_tuples(n)]

    # the witness: carrier diagonal, every off-diagonal -eps/2
    W = [[eps if i == j else -eps / 2 for j in range(n)] for i in range(n)]
    x = tuple(W[i][j] for i, j in unk)
    legs["witness_in_elliptope_with_diagonal_pinned"] = (
        _psd(W) and all(W[i][i] == eps for i in range(n)),
        {"diag": [str(W[i][i]) for i in range(n)],
         "offdiag": [str(c) for c in x],
         "note": "the diagonal is compared entrywise to eps, not assumed "
                 "from a variable name"})

    viol = [(r, b) for (r, b) in facets
            if sum(a * c for a, c in zip(r, x)) < b * eps]
    worst = min((sum(a * c for a, c in zip(r, x)) - b * eps)
                for (r, b) in facets)
    legs["witness_violates_a_valid_scaled_facet"] = (
        len(viol) > 0 and worst < 0,
        {"violated_facets": len(viol), "worst_slack": str(worst)})

    valid = all(sum(a * c for a, c in zip(r, v)) >= b * eps
                for (r, b) in facets for v in verts)
    n_triples = len(list(combinations(range(n), 3)))
    legs["facets_valid_on_every_scaled_vertex"] = (
        valid and len(verts) == 2 ** (n - 1)
        and len(facets) == 4 * n_triples,
        {"vertex_classes": len(verts), "facets": len(facets),
         "note": "counts enforced against 2^(n-1) vertex classes and "
                 "4 sign patterns per vertex triple"})

    # eps*I is the barycentre: explicit weights over ALL 8 sign vectors
    svecs = list(product((1, -1), repeat=n))
    w = F(1, len(svecs))
    avg = [[sum(w * eps * F(v[i] * v[j]) for v in svecs) for j in range(n)]
           for i in range(n)]
    target = [[eps if i == j else F(0) for j in range(n)] for i in range(n)]
    legs["center_is_barycentre_entrywise"] = (
        avg == target and w > 0 and w * len(svecs) == 1,
        {"weight_each": str(w), "sign_vectors": len(svecs),
         "reproduces": "eps*I entrywise, diagonal included",
         "leg_class": "identity-level control, not a measurement"})

    ones = (1, 1, 1)
    J = [[eps * F(ones[i] * ones[j]) for j in range(n)] for i in range(n)]
    legs["all_ones_point_is_scaled_vertex"] = (
        all(J[i][j] == eps for i in range(n) for j in range(n))
        and tuple(J[i][j] for i, j in unk) in verts,
        {"sign_vector": ones,
         "leg_class": "identity-level control, not a measurement"})

    bad = [[eps, 2 * eps, F(0)], [2 * eps, eps, F(0)], [F(0), F(0), eps]]
    qbad = sum(bad[i][j] * (1, -1, 0)[i] * (1, -1, 0)[j]
               for i in range(n) for j in range(n))
    zp = [[F(0), eps], [eps, F(0)]]
    legs["non_psd_control_rejected"] = (
        (not _psd(bad)) and qbad == -2 * eps and qbad < 0
        and not _psd(zp),
        {"quad_form_at_(1,-1,0)": str(qbad),
         "zero_pivot_control": "[[0, eps], [eps, 0]] rejected (exercises "
                               "the zero-pivot branch of the predicate)"})

    # free-sector dimension == counted-ledger nullity, by value, n = 3,4,5
    tie_rows = {}
    ok_tie = True
    for m in (3, 4, 5):
        B = clu._sym_basis(m)
        E = clu._projectors(m)
        rows = [[clu._hs(Ek, P) for P in B] for Ek in E]
        nullity = len(B) - clu._rank(rows)
        pairs = len(list(combinations(range(m), 2)))
        tie_rows[m] = {"nullity": nullity, "pairs": pairs}
        ok_tie &= (nullity == pairs)
    banked = clu.check_L_counted_ledger_fixes_only_the_commit_record_diagonal()
    ev = banked["legs"]["resolution_read_rank_and_nullity_real"]["evidence"]
    ok_tie &= (banked["passed"] is True and ev["nullity"] == tie_rows[3]["nullity"])
    legs["free_sector_dim_tied_to_counted_ledger_nullity"] = (
        ok_tie and len(tie_rows) == 3,
        {"rows": {str(k): v for k, v in tie_rows.items()},
         "banked_n3_evidence": ev,
         "note": "nullity computed through the sibling's own _projectors/"
                 "_sym_basis/_hs/_rank; at n = 3 also read from the banked "
                 "return",
         "leg_class": "identity plus cross-module tie; the tie is the "
                      "discriminating content"})

    return _result(
        "check_B1_elliptope_strictly_contains_cut", legs,
        key_result=(
            f"At n = {n}, eps = {eps}: an exhibited PSD matrix with the "
            f"carrier diagonal violates {len(viol)} valid facets (worst "
            f"slack {worst}); eps*I is the barycentre of {len(svecs)} "
            f"scaled cut generators and eps*J is a scaled vertex; the "
            f"free-sector dimension equals the counted-ledger nullity at "
            f"n = {sorted(tie_rows)} by value."),
        conditional_on=DIAGONAL_PREMISES,
        cross_refs=["T_carrier_consistent_functionals_are_elliptope",
                    "L_counted_ledger_fixes_only_the_commit_record_diagonal"],
        disclosures=(
            ["REAL_SYMMETRIC_TEST_SECTOR travels with carrier_elliptope's "
             "parametrization, consumed and not re-proved",
             "the containment direction (every scaled cut generator is in "
             "the elliptope) is identity-level -- eps*vv^T is PSD with "
             "diagonal eps -- disclosed, not executed by a leg",
             "facet validity is executed on the scaled cut generators; "
             "validity on all of eps*CUT is the linearity step, disclosed"]
            + (["stated limitation: the probed eps equals 1, so the "
                "eps-scaling in this check is multiplicatively unexercised "
                "at the probed value; the eps tie pins sign and "
                "mode-coherence, not magnitude"] if eps == 1 else [])))


# ---------------------------------------------------------------------------
# B2 -- the projection, named
# ---------------------------------------------------------------------------

def check_B2_projection_named():
    """B2: the (2,2,2) reading lives on the projection of the elliptope
    onto the four disjoint-party cross coordinates (the Tsirelson body);
    S^2 < 8 held on the witness and refuted as sufficient; the banked
    witness is placed in the gap by calling the deciders on the actual
    object."""
    from apf.fencea_hinge_trichotomy import (
        check_T_correlation_ladder_exact_rational_chsh_witness as _banked,
        IE_DECLARATIONS)
    from apf.ijc_boolean_defender_bridge import feasbool_structural

    legs = {}
    r = _banked()
    m = re.search(r"IJCStr at \|S\| = (\d+)/(\d+)", r["key_result"])
    S_banked = F(int(m.group(1)), int(m.group(2))) if m else None
    legs["banked_witness_return_parsed_not_restated"] = (
        r.get("passed") is True and S_banked is not None and S_banked > 2,
        {"parsed_value": str(S_banked),
         "source": "T_correlation_ladder_exact_rational_chsh_witness "
                   "key_result, regex-parsed"})

    decls = [d for d in IE_DECLARATIONS
             if d.get("input_id") == "contextuality:native_ladder_chsh_violation"]
    E = tuple(F(v) for v in decls[0]["payload"]["E"]) if len(decls) == 1 else ()
    S = (E[0] + E[1] + E[2] - E[3]) if len(E) == 4 else None
    legs["witness_E_read_from_banked_surface_ties_value"] = (
        len(decls) == 1 and len(E) == 4 and S is not None
        and abs(S) == S_banked,
        {"E": [str(e) for e in E], "S": str(S),
         "tie": "computed |S| from the IE-declared E equals the value "
                "parsed from the banked return (two banked surfaces, one "
                "value)"})

    fb = feasbool_structural(E)
    legs["decider_called_on_the_witness_value_tied"] = (
        fb["feasible"] is False and fb["branch"] == "IJCStr"
        and F(fb["max_chsh_value"]) == abs(S),
        {"branch": fb["branch"], "max_chsh_value": fb["max_chsh_value"],
         "tie": "the decider's facet maximum equals |S| computed here"})

    x, y = F(-7, 100), F(-29, 100)
    G = _witness_completion(E, x, y)
    E_second = tuple(F(v) for v in decls[0]["payload"]["E"])
    cross = (G[0][2], G[0][3], G[1][2], G[1][3])
    legs["completion_cross_block_pinned_to_banked_read"] = (
        cross == E_second,
        {"cross_block": [str(c) for c in cross],
         "note": "the completion's cross block is compared entrywise to a "
                 "second in-process read of the banked IE declaration; the "
                 "construction is thereby pinned to the object whose S is "
                 "checked"})
    legs["completion_is_psd_with_unit_diagonal"] = (
        _psd(G) and all(G[i][i] == 1 for i in range(4)),
        {"x": str(x), "y": str(y),
         "diag": [str(G[i][i]) for i in range(4)]})

    legs["s_squared_below_8_on_the_witness"] = (
        S * S < 8,
        {"S_squared": str(S * S),
         "note": "necessity instance; sufficiency is refuted by the next leg"})

    # the exact counterexample: E' = (1, 1, 1/5, -1/5)
    Ec = (F(1), F(1), F(1, 5), F(-1, 5))
    Sc = Ec[0] + Ec[1] + Ec[2] - Ec[3]

    def m1(t):
        return _det([[F(1), t, Ec[0]], [t, F(1), Ec[2]], [Ec[0], Ec[2], F(1)]])

    def m2(t):
        return _det([[F(1), t, Ec[1]], [t, F(1), Ec[3]], [Ec[1], Ec[3], F(1)]])

    c1 = _quad_coeffs(m1)
    c2 = _quad_coeffs(m2)
    r1, r2 = Ec[2], Ec[3]
    ok_counter = (
        Sc * Sc < 8
        and c1 == (F(-1), 2 * r1, -r1 * r1)      # m1(t) = -(t - r1)^2
        and c2 == (F(-1), 2 * r2, -r2 * r2)      # m2(t) = -(t - r2)^2
        and r1 != r2
        and m1(r2) < 0 and m2(r1) < 0)
    legs["s_squared_insufficient_by_exact_counterexample"] = (
        ok_counter,
        {"E_counter": [str(e) for e in Ec], "S_squared": str(Sc * Sc),
         "minor1_coeffs": [str(c) for c in c1],
         "minor2_coeffs": [str(c) for c in c2],
         "forced_values": [str(r1), str(r2)],
         "note": "each principal minor is a negated perfect square forcing "
                 "a distinct intra-party value, so no PSD completion exists "
                 "although S^2 < 8"})

    # PR-box control: S^2 = 16 > 8, and no completion (forced y = 1, then
    # a principal minor is negative)
    Epr = (F(1), F(1), F(1), F(-1))
    Spr = Epr[0] + Epr[1] + Epr[2] - Epr[3]

    def mpr(t):
        return _det([[F(1), Epr[0], Epr[1]], [Epr[0], F(1), t],
                     [Epr[1], t, F(1)]])

    cpr = _quad_coeffs(mpr)
    forced_y = Epr[0] * Epr[1]
    second = _det([[F(1), Epr[2], Epr[3]], [Epr[2], F(1), forced_y],
                   [Epr[3], forced_y, F(1)]])
    legs["pr_box_control_has_no_completion"] = (
        Spr * Spr > 8
        and cpr == (F(-1), 2 * forced_y, -forced_y * forced_y)
        and second < 0,
        {"S_squared": str(Spr * Spr), "forced_y": str(forced_y),
         "second_minor_at_forced_y": str(second)})

    return _result(
        "check_B2_projection_named", legs,
        key_result=(
            f"The banked witness (|S| = {S_banked}, parsed) is outside the "
            f"Boole polytope by the called decider and inside the "
            f"projection body by the genuine completion at (x, y) = "
            f"({x}, {y}); S^2 < 8 held on the witness and is not "
            f"sufficient "
            f"(counterexample S^2 = {Sc * Sc} with contradictory forced "
            f"completion values {r1} and {r2})."),
        conditional_on=DIAGONAL_PREMISES,
        choice_imports=[
            "the disjoint-party (2,2,2) cover: which four coordinates are "
            "read is a CHOICE, disclosed, not supplied by anything banked"],
        cross_refs=["T_correlation_ladder_exact_rational_chsh_witness",
                    "T_ijc_boolean_defender_bridge"],
        disclosures=[
            "the projection discards the intra-party entries; membership "
            "requires exhibiting a completion, which is what the "
            "counterexample leg shows S^2 < 8 cannot certify",
            "the completion body carries unit diagonal (the correlator "
            "convention); B1's carrier body carries diagonal eps; the "
            "relation between the two scalings is not computed here"])


# ---------------------------------------------------------------------------
# B3 -- projection exit implies CUT exit; strictness on the frustrated C_5
# ---------------------------------------------------------------------------

def check_B3_projection_exit_implies_cut_exit():
    """B3: the vertex-restriction argument executed exhaustively, and its
    strictness: the frustrated C_5 exits CUT(K_5) while every
    disjoint-party cover stays Boole-feasible."""
    from apf.ijc_boolean_defender_bridge import feasbool_structural
    import apf.global_defect_margin as gdm

    legs = {}
    covers = _disjoint_party_covers()
    cutvecs = list(product((1, -1), repeat=5))
    det_verts = {(F(a0 * b0), F(a0 * b1), F(a1 * b0), F(a1 * b1))
                 for a0, a1, b0, b1 in product((1, -1), repeat=4)}
    ok_restrict = all(
        (F(v[A[0]] * v[B[0]]), F(v[A[0]] * v[B[1]]),
         F(v[A[1]] * v[B[0]]), F(v[A[1]] * v[B[1]])) in det_verts
        and _chsh_max((F(v[A[0]] * v[B[0]]), F(v[A[0]] * v[B[1]]),
                       F(v[A[1]] * v[B[0]]), F(v[A[1]] * v[B[1]]))) <= 2
        for v in cutvecs for (A, B) in covers)
    legs["cut_vertices_restrict_to_boole_vertices"] = (
        ok_restrict and len(cutvecs) == 32 and len(covers) == 15
        and len(det_verts) == 8,
        {"cut_vectors": len(cutvecs), "covers": len(covers),
         "distinct_boole_vertices": len(det_verts),
         "note": "every cut generator restricts, on every cover, to a "
                 "deterministic vertex satisfying every CHSH facet; a "
                 "nonnegative mixture then satisfies them too, so "
                 "projection exit implies full CUT exit"})

    frustrated = (1, 1, 1, 1, -1)
    balanced = (1, 1, 1, 1, 1)
    Cf = _c5_matrix(frustrated, F(1, 2))
    Cb = _c5_matrix(balanced, F(1, 2))
    bvec = (1, -1, 1, -1, 1)
    cutmats = _k5_cut_matrices()
    bound = min(_hyper_form(bvec, M) for M in cutmats)
    formula_bound = (F(1) - sum(F(c * c) for c in bvec)) / 2
    legs["pentagonal_facet_valid_on_every_cut_vector"] = (
        bound == formula_bound and len(cutmats) == 32,
        {"b": bvec, "enumerated_min": str(bound),
         "formula_(1-sum_b_sq)/2": str(formula_bound),
         "note": "the bound is computed by two routes: exhaustive "
                 "enumeration and the odd-sum identity"})

    val = _hyper_form(bvec, Cf)
    depth = bound - val
    legs["frustrated_c5_exits_pentagonal_facet"] = (
        val < bound and depth == F(1, 2),
        {"value": str(val), "bound": str(bound), "depth": str(depth)})

    fam = [bv for bv in product(range(-2, 3), repeat=5) if sum(bv) % 2 != 0]
    from math import comb
    expected_fam = sum(comb(5, k) * (2 ** k) * (3 ** (5 - k))
                       for k in (1, 3, 5))
    viols = 0
    for bv in fam:
        bd = min(_hyper_form(bv, M) for M in cutmats)
        if _hyper_form(bv, Cb) < bd:
            viols += 1
    legs["balanced_control_zero_violations_full_odd_family"] = (
        viols == 0 and len(fam) == expected_fam,
        {"family_size": len(fam), "expected_by_parity_count": expected_fam,
         "violations": viols})

    per_cover = []
    ok_cover = True
    for cover in covers:
        Ecov = _cover_E(Cf, cover)
        fb = feasbool_structural(Ecov)
        own_max = _chsh_max(Ecov)
        ok_cover &= (fb["feasible"] is True
                     and F(fb["max_chsh_value"]) == own_max)
        per_cover.append(own_max)
    overall = max(per_cover)
    legs["every_cover_boole_feasible_max_tied_by_value"] = (
        ok_cover and len(per_cover) == 15 and overall == F(3, 2),
        {"covers": len(per_cover), "overall_max": str(overall),
         "tie": "each cover's own facet maximum equals the banked "
                "decider's returned max_chsh_value, entrywise over covers",
         "note": "the overall maximum is pinned by value; it sits strictly "
                 "below the facet bound 2 on every cover while the same "
                 "matrix exits CUT(K_5) -- the containment is strictly "
                 "one-way"})

    chi_f = gdm._cycle_product(frustrated)
    chi_b = gdm._cycle_product(balanced)
    df = gdm._best_third_boat_defect_fraction(frustrated)
    db = gdm._best_third_boat_defect_fraction(balanced)
    own_chi_f = 1 if sum(1 for s in frustrated if s < 0) % 2 == 0 else -1
    legs["sign_classes_tied_to_banked_parity_law"] = (
        chi_f == -1 and chi_b == 1 and own_chi_f == chi_f
        and df == F(1, len(frustrated)) and db == 0,
        {"chi_frustrated": chi_f, "chi_balanced": chi_b,
         "best_defect_frustrated": str(df), "best_defect_balanced": str(db),
         "tie": "chi and best defect fraction computed through "
                "global_defect_margin's own functions; own parity route "
                "agrees"})

    return _result(
        "check_B3_projection_exit_implies_cut_exit", legs,
        key_result=(
            f"Projection exit implies CUT exit (vertex-restriction "
            f"argument; the vertex part executed on {len(cutvecs)} cut "
            f"vectors x {len(covers)} covers, the mixture step is "
            f"linearity, disclosed), and "
            f"strictly: the frustrated C_5 exits CUT(K_5) at depth "
            f"{depth} while all {len(per_cover)} covers stay "
            f"Boole-feasible with facet maximum {overall}."),
        cross_refs=["T_ijc_boolean_defender_bridge", "T_global_defect_margin"],
        disclosures=[
            "'invisible to every cover' is scoped to the banked (2,2,2) "
            "classification; a pentagon-scenario decider is not banked"])


# ---------------------------------------------------------------------------
# B4 -- non-identity controls (CERT1 and CERT4)
# ---------------------------------------------------------------------------

def check_B4_non_identity_controls():
    """B4: the two permanent negative controls. CERT1: frustration does
    not force exit (magnitude 1/4 triangle inside CUT). CERT4: exit does
    not force frustration (balanced class outside the Boole polytope)."""
    from apf.ijc_boolean_defender_bridge import feasbool_structural
    from apf.third_boat_no_extension import _in_local_polytope
    import apf.global_defect_margin as gdm

    legs = {}
    n = 3
    a = F(-1, 4)
    M = [[F(1) if i == j else a for j in range(n)] for i in range(n)]
    minors = (M[0][0],
              _det([[M[0][0], M[0][1]], [M[1][0], M[1][1]]]),
              _det(M))
    legs["cert1_frustrated_triangle_is_psd_unit_diagonal"] = (
        _psd(M) and all(M[i][i] == 1 for i in range(n))
        and minors == (F(1), F(15, 16), F(25, 32)),
        {"offdiag": str(a),
         "leading_principal_minors": [str(v) for v in minors],
         "caveat": "elliptope-level certificate; whether magnitude-1/4 "
                   "frustrated triangles arise as normalized loads of "
                   "admissible presentations is not computed here"})

    classes = [(1, 1, 1), (1, 1, -1), (1, -1, 1), (1, -1, -1)]
    weights = [F(1, 16), F(5, 16), F(5, 16), F(5, 16)]
    mix = [[sum(w * F(v[i] * v[j]) for w, v in zip(weights, classes))
            for j in range(n)] for i in range(n)]
    legs["cert1_inside_cut_by_explicit_weights"] = (
        mix == M and all(w >= 0 for w in weights) and sum(weights) == 1,
        {"weights": [str(w) for w in weights],
         "vertex_classes": classes,
         "note": "the mixture reproduces the matrix entrywise, diagonal "
                 "included"})

    tri_signs = (-1, -1, -1)
    legs["cert1_class_frustrated_by_banked_parity"] = (
        gdm._cycle_product(tri_signs) == -1
        and sum(1 for s in tri_signs if s < 0) % 2 == 1,
        {"chi": gdm._cycle_product(tri_signs),
         "tie": "chi through global_defect_margin's own _cycle_product; "
                "own odd-negative-edge route agrees"})

    M2 = [[F(1) if i == j else F(-1, 2) for j in range(n)] for i in range(n)]
    unk = list(combinations(range(n), 2))
    x2 = tuple(M2[i][j] for i, j in unk)
    facets = _triangle_facets(n)
    verts = _cut_vertex_offdiag_tuples(n)
    viol2 = [(r, b) for (r, b) in facets
             if sum(c * v for c, v in zip(r, x2)) < b]
    valid2 = all(sum(c * v for c, v in zip(r, vv)) >= b
                 for (r, b) in facets for vv in verts)
    legs["cert1_control_same_class_exits_at_magnitude_half"] = (
        len(viol2) > 0 and valid2,
        {"violated_facets": len(viol2),
         "note": "the same sign class at magnitude 1/2 violates a facet "
                 "valid on every vertex, so the membership machinery "
                 "discriminates and CERT1's insideness is not vacuous"})

    a1, a2 = (F(1), F(0)), (F(3, 5), F(4, 5))
    b1, b2 = (F(24, 25), F(7, 25)), (F(24, 25), F(-7, 25))

    def dot(u, v):
        return u[0] * v[0] + u[1] * v[1]

    E4 = (dot(a1, b1), dot(a1, b2), dot(a2, b1), dot(a2, b2))
    vecs = (a1, a2, b1, b2)
    Gram = [[dot(u, v) for v in vecs] for u in vecs]
    legs["cert4_realized_by_explicit_unit_vectors"] = (
        all(dot(u, u) == 1 for u in vecs) and _psd(Gram)
        and all(Gram[i][i] == 1 for i in range(4))
        and (Gram[0][2], Gram[0][3], Gram[1][2], Gram[1][3]) == E4,
        {"E": [str(e) for e in E4],
         "vectors": [[str(c) for c in u] for u in vecs],
         "note": "the full Gram matrix is an elliptope point whose cross "
                 "block is the behaviour, entrywise"})

    S4 = E4[0] + E4[1] + E4[2] - E4[3]
    fb4 = feasbool_structural(E4)
    legs["cert4_exits_boole_decider_value_tied"] = (
        fb4["feasible"] is False and fb4["branch"] == "IJCStr"
        and F(fb4["max_chsh_value"]) == _chsh_max(E4)
        and _chsh_max(E4) == S4 and S4 > 2,
        {"S": str(S4), "decider_max": fb4["max_chsh_value"],
         "tie": "the decider's facet maximum equals the facet maximum "
                "computed here, equals the CHSH value of the behaviour"})

    sgns = tuple(1 if e > 0 else -1 for e in E4)
    legs["cert4_class_balanced_by_banked_parity"] = (
        sgns == (1, 1, 1, 1) and gdm._cycle_product(sgns) == 1,
        {"signs": sgns, "chi": gdm._cycle_product(sgns),
         "note": "all four correlators positive: the balanced switching "
                 "class of the 4-cycle, chi through the sibling's own "
                 "function",
         "leg_class": "identity/control; the discriminating content is "
                      "the tie to the sibling's parity function"})

    legs["cert4_second_decider_concurs"] = (
        _in_local_polytope(E4) is False
        and _in_local_polytope((F(0),) * 4) is True,
        {"note": "verdict-level control through "
                 "third_boat_no_extension._in_local_polytope, disclosed as "
                 "verdict-level (the value tie is the previous leg)"})

    return _result(
        "check_B4_non_identity_controls", legs,
        key_result=(
            f"CERT1: the frustrated triangle at magnitude {a} is inside "
            f"CUT(K_3) by explicit weights (and the same class at "
            f"magnitude 1/2 exits). CERT4: the balanced-sign behaviour "
            f"exits the Boole polytope at CHSH {S4} by the called "
            f"decider. Frustration does not force exit and exit does not "
            f"force frustration, each by an exhibited object."),
        cross_refs=["T_ijc_boolean_defender_bridge", "T_third_boat_iff_local",
                    "T_global_defect_margin"],
        disclosures=[
            "CERT4's behaviour is a mathematical object; no claim that any "
            "APF presentation realizes it"])


# ---------------------------------------------------------------------------
# B5 -- presentation content: counted fractions per (n, k)
# ---------------------------------------------------------------------------

def check_B5_presentation_fraction():
    """B5: the counted fraction of admissible signed presentations whose
    loads carry a negative entry, per (n, k) with denominators; vacuity at
    the empty cells established by two routes."""
    legs = {}
    table = {}
    min_edges = {}
    filter_rows = {}
    for n in (3, 4, 5):
        R = _realizable_configs(n)
        pairs = len(list(combinations(range(n), 2)))
        filter_rows[n] = {"realizable": len(R), "edge_sets": 2 ** pairs}
        nonempty = [len(s) for s in R if s]
        min_edges[n] = min(nonempty)
        cells = [(i, j) for i in range(n) for j in range(n) if i != j]
        for k in (2, 3):
            tot = neg = 0
            for Sset in combinations(cells, k):
                if frozenset(frozenset(c) for c in Sset) not in R:
                    continue
                for sg in product((1, -1), repeat=k):
                    g = _load_of(Sset, sg, n)
                    tot += 1
                    if any(g[i][j] < 0 for i in range(n) for j in range(n)):
                        neg += 1
            table[(n, k)] = (neg, tot)

    legs["admissibility_filter_bites"] = (
        all(v["realizable"] < v["edge_sets"] for v in filter_rows.values())
        and len(filter_rows) == 3,
        {**{str(k): v for k, v in filter_rows.items()},
         "leg_class": "control, not a measurement"})

    nonvac = {nk: c for nk, c in table.items() if c[1] > 0}
    vac = {nk: c for nk, c in table.items() if c[1] == 0}
    pinned = {(3, 2): (6, 48), (3, 3): (48, 160), (4, 3): (72, 256)}
    legs["nonvacuous_cells_have_proper_fractions"] = (
        len(nonvac) == 3
        and all(0 < neg < tot for (neg, tot) in nonvac.values())
        and nonvac == pinned,
        {**{f"n{n}_k{k}": f"{neg}/{tot}"
            for (n, k), (neg, tot) in sorted(nonvac.items())},
         "regression_pin": "the computed cells are compared equal to the "
                           "pinned exact fractions (regression anchor)"})

    legs["vacuous_cells_vacuous_by_two_routes"] = (
        len(vac) == 3
        and all(min_edges[n] > k for (n, k) in vac)
        and all(neg == 0 and tot == 0 for (neg, tot) in vac.values()),
        {"vacuous_cells": sorted(str(nk) for nk in vac),
         "min_nonempty_complete_multipartite_edges":
             {str(n): m for n, m in min_edges.items()},
         "note": "route 1: the direct count is zero; route 2: the minimal "
                 "nonempty complete-multipartite edge count on n vertices, "
                 "computed by partition enumeration, exceeds k"})

    ok_pos = True
    pos_count = 0
    for n in (3, 4, 5):
        R = _realizable_configs(n)
        cells = [(i, j) for i in range(n) for j in range(n) if i != j]
        for k in (2, 3):
            for Sset in combinations(cells, k):
                if frozenset(frozenset(c) for c in Sset) not in R:
                    continue
                g = _load_of(Sset, (1,) * k, n)
                pos_count += 1
                ok_pos &= all(g[i][j] >= 0
                              for i in range(n) for j in range(n))
    legs["unsigned_control_loads_nonnegative"] = (
        ok_pos and pos_count > 0
        and pos_count == sum(tot // (2 ** k)
                             for (_n, k), (_neg, tot) in table.items()),
        {"all_plus_supports_checked": pos_count,
         "note": "the checked support count is enforced against the "
                 "per-cell totals, not printed"})

    frac_bits = []
    for (n, k), (neg, tot) in sorted(nonvac.items()):
        pct = float(100 * F(neg, tot))
        frac_bits.append(f"(n={n}, k={k}): {neg}/{tot} = {pct:.2f}%")
    return _result(
        "check_B5_presentation_fraction", legs,
        key_result=(
            "Of the counted admissible signed presentations, the loads "
            "with a negative entry (a certificate of leaving the "
            "completely positive cone) are: " + "; ".join(frac_bits)
            + ". The remaining (n, k) cells in the computed window are "
            "vacuous structurally. Percentages are of the counted cells "
            "only, never universal."),
        cross_refs=[],
        disclosures=[
            "the exit certificate is a negative entry: entrywise "
            "nonnegativity is necessary for complete positivity (a CP "
            "factorization has nonnegative entries -- identity-level); "
            "the n <= 4 converse (doubly-nonnegative = completely "
            "positive) is cited, not computed, and no leg uses it"])


# ---------------------------------------------------------------------------
# module surface
# ---------------------------------------------------------------------------

_CHECKS = {
    "check_B1_elliptope_strictly_contains_cut":
        check_B1_elliptope_strictly_contains_cut,
    "check_B2_projection_named": check_B2_projection_named,
    "check_B3_projection_exit_implies_cut_exit":
        check_B3_projection_exit_implies_cut_exit,
    "check_B4_non_identity_controls": check_B4_non_identity_controls,
    "check_B5_presentation_fraction": check_B5_presentation_fraction,
}


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


# Registered v24.3.470 (2026-08-11) after two blinded cold audits, both
# LAND-WITH-FIXES (0.86 / 0.87) with zero arithmetic disagreement, a cold
# fix seat, and Ethan's lift ruling of 2026-08-11.  BARE-NAME keys per
# D6@2026-08-03.
def register(registry):
    registry.update({
        "B1_elliptope_strictly_contains_cut":
            check_B1_elliptope_strictly_contains_cut,
        "B2_projection_named": check_B2_projection_named,
        "B3_projection_exit_implies_cut_exit":
            check_B3_projection_exit_implies_cut_exit,
        "B4_non_identity_controls": check_B4_non_identity_controls,
        "B5_presentation_fraction": check_B5_presentation_fraction,
    })
    return registry


if __name__ == "__main__":
    for _name, _r in run_all().items():
        print(("PASS" if _r.get("passed") else "FAIL"), _name,
              "legs:", _r.get("leg_count"))
        for _fr in _r.get("fail_reasons", []):
            print("  FAIL-REASON:", _fr)
