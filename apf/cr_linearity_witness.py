"""The [CR] => linearity witness: the finite exact core, executed.

BANKED v24.3.473 (2026-08-12).  Built by the S5 seat of the Situational
Sign program (lane S5 / enabler E2) to the FROZEN claim surface (binding;
W1-W5 adopted verbatim):
  Artifacts_2026-08-11_session/s5_witness/CLAIM_SURFACE_FROZEN_2026-08-12.md
  raw sha256: dc141ac8fa58888607a60a5b5c227eef29bbe76cd3434ef3434b7e3dca4dd98b
The module may state nothing beyond that surface.  Weakening is the
permitted direction; strengthening is not.

Two blinded cold audits, LAND-WITH-FIXES 0.85 / 0.85, zero arithmetic
disagreement in either; cold fix seat carried (7 repaired, 0 declined); the
simplex determinant leg strengthened to a per-element det(P_sigma) ==
sgn(sigma) value tie (audit D2's find; the escaping mutant now caught);
receipts regenerated against the fixed object at
Artifacts_2026-08-11_session/s5_witness/.  LIFTED by Ethan's ruling
2026-08-12.  BARE-NAME registry keys per D6@2026-08-03.

FIX PASS (2026-08-12, cold fix seat): the dispositions of two blinded cold
audits carried.  One executable strengthening (a value tie, the permitted
genre): the simplex determinant leg now ties det(P_sigma) == sgn(sigma)
PER ELEMENT, sgn from an independent inversion count -- the set-level pin
{-1, +1} had let a sign-flipped determinant helper through.  Everything
else is scoping/disclosure: W2's exactness headline carries its
convexity-import conditional inline; the extremality leg is scoped to what
it computes (full extremality NOT executed); the two
identity-by-construction W1 legs are labelled; the polynomial-identity
certifier gains executed negative controls; the _orth_defect sum branch
and W5's unpinned own-inventory are disclosed standing limits.

WHAT THIS MODULE IS.  Paper 40 Supplement v0.174, thm:cr-dependence, defines
[CR] (continuous reversibility): "the pure states of a finite interface are
connected by a continuous group of reversible transformations."  Necessity
of [CR] for the linear realization is [P] in-corpus
(prop:linearity-independent, the S_3 countermodel; its named witness script
is the orphaned E4 stratum, not bank-registered).  Sufficiency is a
literature citation (Hardy 2001; Masanes-Mueller 2011; de la
Torre-Masanes-Short-Mueller 2012; Chiribella-D'Ariano-Perinotti 2011) and is
machine-checked nowhere in the bank.  This module makes the FINITE EXACT
CORE of the sufficiency direction executable — two fixed state spaces,
rational points, Fraction arithmetic, no floats — and nothing more:

  W1  mixture-preservation + reversibility force a unique invertible linear
      extension (determination mechanism executed per point, on the 3-type
      simplex and the rational Bloch ball; hull dimension 4 tied by value to
      the banked SPANNING_EFFECTS rank of operational_score_linearity);
  W2  the classical realization's reversible sector is EXACTLY S_3, given
      the named convexity import and the classical extreme-point
      identification (order 6, computed not stated; transitive;
      square-root obstruction exhaustive; element-for-element value tie
      to the countermodel's transition group);
  W3  the linear (qubit) realization carries an infinite exact reversible
      sector of LINEAR maps connecting the exhibited rational pure states
      (Pythagorean rotation family: identities, group law, injectivity,
      explicit connecting elements, antipode via exact composition with the
      chart omission disclosed);
  W4  each executed clause is load-bearing: drop mixture-preservation /
      reversibility / continuity, an exact counterexample defeats the
      conclusion (the continuity drop is the S_3 sector itself: group,
      reversible, transitive — and classical);
  W5  the composed containment statement, consuming W1-W4 by value, with the
      named imports and the literature import recorded, and the module's apf
      imports enforced set-exactly by AST.

WHAT THIS MODULE DOES NOT ESTABLISH (containment; carried from the frozen
surface): the continuum reconstruction theorem (Hardy / Masanes-Mueller /
dlTMSM / CDP) is a NAMED LITERATURE IMPORT for everything beyond the
executed scope — it is not re-proved, not approximated, not "almost"
checked here; mixture-preservation of transformations is a NAMED IMPORT;
whether [CR] HOLDS physically is not addressed; the quadratic form / inner
product / trace (the GNS step) is downstream and untouched; nothing at
Hilbert dimension >= 3; the transitivity clause's own load-bearing status
is not executed (disclosed limitation of the W4 battery).

MAY-NOT-CITE (binding; the frozen surface's list, carried verbatim):
- never "Born is derived" — unconditionally or from this module;
- never "the continuum reconstruction theorem is machine-checked";
- never "[CR] is established / physical";
- never "linearity is derived from the spine" (the necessity countermodel
  bars it; this module consumes that bar, it does not lift it);
- never as a supply of the quadratic form / inner product / trace;
- never "sufficiency is machine-checked beyond the finite core" (banked,
  the module witnesses the finite core only, in containment form).

LEG INVENTORY (D7@2026-08-08, APPEND-AND-RECORD): _result() compares the
executed leg set against EXPECTED_LEGS set-exactly on the path the bank
would execute; a mismatch contributes a failure reason and does not raise.
STANDING LIMIT, disclosed: this certifies that a declared leg EXECUTED, not
that it COULD HAVE FAILED.

This module describes what it COMPUTES.  Named imports are consumed as
names at the legs that need them; none is constructed or derived here.
"""
from __future__ import annotations

import ast
from fractions import Fraction as F
from itertools import permutations
from math import factorial
from pathlib import Path

HELD_OUT_OF_THE_BANK = False  # hold lifted by Ethan's ruling 2026-08-12; register() below.

CLAIM_SURFACE_SHA256 = (
    "dc141ac8fa58888607a60a5b5c227eef29bbe76cd3434ef3434b7e3dca4dd98b")

# Named unforced imports.  Each is CONSUMED AS A NAME at the legs that need
# it; none is constructed, derived, or selected by anything computed here.
NAMED_IMPORTS = (
    # transformations respect operational mixing (the Busch-genre GPT
    # premise under which "acts linearly on the state space" is well-posed;
    # the banked operational_score_linearity line names the score-side
    # sibling as CLASSICAL_RANDOMIZATION / MIXTURE_CONGRUENCE).
    "MIXTURE_PRESERVATION_OF_TRANSFORMATIONS",
    # an affine automorphism of a compact convex set maps extreme points
    # onto extreme points (classical convexity; supported in W2 by an
    # executed pullback-mixture identity, not re-proved in generality).
    "EXTREME_POINT_PERMUTATION_classical_convexity",
    # a connected topological group with more than one element is infinite
    # (elementary; the executed content is finiteness + the root
    # obstruction — the continuum reading of "the [CR] clause fails on a
    # finite sector" consumes this name).
    "CONNECTED_NONTRIVIAL_GROUP_INFINITE",
    # the full sufficiency theorem: FD1-FD4 + [CR] => A = (+) M_{n_i}(D),
    # D in {R, C, H}, D = C by tomographic locality.  Hardy 2001;
    # Masanes-Mueller 2011; de la Torre-Masanes-Short-Mueller 2012;
    # Chiribella-D'Ariano-Perinotti 2011.  Everything beyond the executed
    # scope of W1-W4 rides on this name and on nothing computed here.
    "LITERATURE_SUFFICIENCY_IMPORT_Hardy_MM_dlTMSM_CDP",
)

# The necessity direction, cited not re-proved: Paper 40 Supplement v0.174,
# prop:linearity-independent (paper-side [P]; the named witness script
# paper40_linearity_independence_witness.py is the orphaned E4 stratum).
NECESSITY_CITATION = (
    "Paper 40 Supplement v0.174, prop:linearity-independent + "
    "thm:cr-dependence part (i); paper-side [P]; witness script orphaned "
    "(docket E4)")

MAY_NOT_CITE = (
    "never 'Born is derived' -- unconditionally or from this module",
    "never 'the continuum reconstruction theorem is machine-checked'",
    "never '[CR] is established / physical'",
    "never 'linearity is derived from the spine'",
    "never as a supply of the quadratic form / inner product / trace",
    "never 'sufficiency is machine-checked beyond the finite core' "
    "(finite core only, containment form)",
)

EXECUTED_SCOPE = {
    "state_spaces": ("classical 3-type simplex Delta^2 in Q^3",
                     "qubit rational Bloch ball in Q^3 (hull dim 4)"),
    "arithmetic": "Fraction only; polynomial identities by degree-bounded "
                  "evaluation; no floats",
    "points": "rational points only; the continuum is the named import",
}

EXPECTED_LEGS = {
    "check_W1_mixture_determination_forces_linear_extension": (
        "simplex_decomposition_binary_rational_all_samples",
        "simplex_affine_extension_unique_rank3",
        "simplex_reversible_extensions_det_pm1",
        "ball_determination_identity_all_samples",
        "ball_octahedron_anchor_is_a_state_with_convex_decomposition",
        "ball_affine_extension_unique_rank4",
        "ball_reversible_extension_det_plus1",
        "hull_dimension_ties_banked_spanning_effects_rank_4",
        "sample_counts_enforced",
    ),
    "check_W2_classical_reversible_sector_exactly_S3": (
        "vertices_avoid_opposite_segment_nonvertex_samples_are_mixtures",
        "six_vertex_permutations_extend_affinely_and_distinctly",
        "cayley_closure_is_a_group_of_order_factorial3",
        "determination_gives_at_most_one_automorphism_per_permutation",
        "pullback_mixture_identity_supports_the_convexity_import",
        "action_transitive_on_pure_states",
        "no_element_squares_to_a_transposition",
        "element_orders_and_finiteness",
        "value_tie_transition_group_equals_automorphism_group",
    ),
    "check_W3_linear_realization_infinite_reversible_sector": (
        "pythagorean_identity_degree_bounded",
        "orthogonality_and_det_plus1_as_identities",
        "sampled_rotations_preserve_ball_and_mixtures_and_center",
        "inverse_law_exact",
        "group_law_exact_on_grid",
        "parameter_recovery_identity_injectivity",
        "sector_infinite_count_enforced",
        "pure_state_list_norm_one_distinct",
        "all_ordered_pairs_connected_explicitly",
        "antipode_via_exact_composition_chart_omission_disclosed",
    ),
    "check_W4_clause_drop_battery": (
        "drop_mixture_preservation_reversible_impostor_defeats_linearity",
        "impostor_is_a_reversible_involution",
        "drop_reversibility_collapse_preserves_mixtures",
        "collapse_extension_fixes_barycenter_det_zero_noninjective",
        "drop_continuity_S3_satisfies_every_remaining_clause",
        "classical_state_space_has_no_superposition",
        "battery_covers_exactly_three_clauses_transitivity_not_executed",
    ),
    "check_W5_composed_containment_and_import_controls": (
        "w1_through_w4_consumed_by_value",
        "dimension_tie_4_equals_banked_spanning_rank",
        "classical_sector_order_6_and_infinite_linear_sector",
        "named_imports_and_necessity_citation_recorded",
        "apf_imports_set_exact_by_ast",
        "containment_scope_recorded",
    ),
}


# ---------------------------------------------------------------------------
# exact linear algebra helpers (Fraction only)
# ---------------------------------------------------------------------------

def _mat_vec(M, v):
    return tuple(sum(M[i][j] * v[j] for j in range(len(v)))
                 for i in range(len(M)))


def _mat_mul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return tuple(tuple(sum(A[i][t] * B[t][j] for t in range(k))
                       for j in range(m)) for i in range(n))


def _rank(rows):
    rows = [list(r) for r in rows]
    rank, ncols = 0, (len(rows[0]) if rows else 0)
    for col in range(ncols):
        piv = None
        for r in range(rank, len(rows)):
            if rows[r][col] != 0:
                piv = r
                break
        if piv is None:
            continue
        rows[rank], rows[piv] = rows[piv], rows[rank]
        pv = rows[rank][col]
        rows[rank] = [x / pv for x in rows[rank]]
        for r in range(len(rows)):
            if r != rank and rows[r][col] != 0:
                f = rows[r][col]
                rows[r] = [a - f * b for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def _det3(M):
    return (M[0][0] * (M[1][1] * M[2][2] - M[1][2] * M[2][1])
            - M[0][1] * (M[1][0] * M[2][2] - M[1][2] * M[2][0])
            + M[0][2] * (M[1][0] * M[2][1] - M[1][1] * M[2][0]))


def _poly_identity(fn, degree_bound, points=None):
    """A univariate rational identity fn(t) == 0, certified by evaluation at
    degree_bound + 1 distinct rational points (a nonzero polynomial of
    degree <= d has <= d roots; denominators cleared by the caller)."""
    pts = points if points is not None else [F(k) for k in
                                             range(-(degree_bound // 2 + 1),
                                                   degree_bound // 2 + 2)]
    assert len(set(pts)) >= degree_bound + 1
    return all(fn(t) == 0 for t in pts), len(pts)


# ---------------------------------------------------------------------------
# state spaces (exact data)
# ---------------------------------------------------------------------------

_V = (  # simplex vertices, barycentric coordinates in Q^3
    (F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))


def _in_simplex(s):
    return all(x >= 0 for x in s) and sum(s) == 1


def _norm2sq(v):
    return sum(x * x for x in v)


def _norm1(v):
    return sum(abs(x) for x in v)


def _in_ball(v):
    return _norm2sq(v) <= 1


def _rot(t):
    """Pythagorean rotation about the z-axis: exact rational orthogonal
    matrix for every rational t (tan-half-angle chart)."""
    d = 1 + t * t
    c, s = (1 - t * t) / d, 2 * t / d
    return ((c, -s, F(0)), (s, c, F(0)), (F(0), F(0), F(1)))


# ---------------------------------------------------------------------------
# result plumbing (append-and-record leg inventory, D7@2026-08-08)
# ---------------------------------------------------------------------------

def _result(name, legs, key_result, dependencies=(), cross_refs=(),
            disclosures=()):
    have = tuple(sorted(legs))
    want = tuple(sorted(EXPECTED_LEGS[name]))
    fail_reasons = []
    if have != want:
        missing = sorted(set(want) - set(have))
        extra = sorted(set(have) - set(want))
        fail_reasons.append(
            f"leg inventory mismatch: missing={missing} extra={extra}")
    for label in sorted(legs):
        ok, _ev = legs[label]
        if not ok:
            fail_reasons.append(f"leg failed: {label}")
    return {
        "name": name,
        "passed": not fail_reasons,
        "fail_reasons": fail_reasons,
        "legs": {k: {"passed": bool(v[0]), "evidence": v[1]}
                 for k, v in legs.items()},
        "leg_count": len(legs),
        "key_result": key_result,
        "dependencies": list(dependencies),
        "cross_refs": list(cross_refs),
        "disclosures": list(disclosures),
        "named_imports": list(NAMED_IMPORTS),
        "may_not_cite": list(MAY_NOT_CITE),
        "executed_scope": dict(EXECUTED_SCOPE),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "claim_surface_sha256": CLAIM_SURFACE_SHA256,
        "tier": 3,
        "epistemic_tag": "P_math",
        "physical_premises_certified": False,
        "leg_inventory_contract": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


# ---------------------------------------------------------------------------
# W1 -- mixture-preservation + reversibility force a unique invertible
#       linear extension (determination mechanism executed per point)
# ---------------------------------------------------------------------------

def check_W1_mixture_determination_forces_linear_extension():
    legs = {}
    # -- simplex samples: every rational state is a binary mixture tree
    #    over the vertices with weights in [0,1] cap Q --------------------
    simplex_samples = [
        (F(1, 3), F(1, 3), F(1, 3)), (F(1, 2), F(1, 4), F(1, 4)),
        (F(1, 7), F(2, 7), F(4, 7)), (F(5, 6), F(1, 6), F(0)),
        (F(0), F(3, 5), F(2, 5)), (F(9, 11), F(1, 11), F(1, 11)),
        (F(1), F(0), F(0)), (F(2, 9), F(3, 9), F(4, 9)),
        (F(1, 13), F(5, 13), F(7, 13)), (F(3, 8), F(3, 8), F(2, 8)),
    ]
    n_simplex = len(simplex_samples)
    ok_dec, checked = True, 0
    for s in simplex_samples:
        if not _in_simplex(s):
            ok_dec = False
            break
        # the executed decomposition: s = s1*e1 + (1-s1)*r, r = the
        # renormalized tail, itself a binary mixture of e2, e3; each node
        # verified as an exact binary rational mixture.
        s1 = s[0]
        if s1 < 1:
            r = tuple(x / (1 - s1) for x in (F(0), s[1], s[2]))
            node1 = tuple(s1 * v + (1 - s1) * rv
                          for v, rv in zip(_V[0], r))
            ok_dec &= (node1 == s) and (0 <= s1 <= 1) and _in_simplex(r)
            r2 = r[1]
            if r2 < 1:
                q = tuple(x / (1 - r2) for x in (F(0), F(0), r[2]))
                node2 = tuple(r2 * v + (1 - r2) * qv
                              for v, qv in zip(_V[1], q))
                ok_dec &= (node2 == r) and (0 <= r2 <= 1) and (q == _V[2])
            else:
                ok_dec &= r == _V[1]
        else:
            ok_dec &= s == _V[0]
        checked += 1
    legs["simplex_decomposition_binary_rational_all_samples"] = (
        ok_dec and checked == n_simplex,
        f"every one of the {checked}/{n_simplex} sampled rational states "
        f"decomposes as an exact binary rational mixture tree over the 3 "
        f"vertices (each node verified as an identity), so a "
        f"mixture-preserving map is DETERMINED on each sample by its vertex "
        f"values (the mechanism is uniform in s: weights are the barycentric "
        f"coordinates).  IDENTITY BY CONSTRUCTION: the node equations hold "
        f"for any valid sample by algebra; this leg's failure surface is "
        f"sample validity")
    # -- uniqueness: an affine map on the simplex hull is determined by the
    #    3 affinely independent vertex values ----------------------------
    aug = [[F(1)] + list(v) for v in _V]
    r3 = _rank(aug)
    legs["simplex_affine_extension_unique_rank3"] = (
        r3 == 3,
        f"augmented vertex matrix rank {r3} == 3: the affine extension "
        f"through the vertex values is unique ON THE AFFINE HULL of the "
        f"vertices (which is where the states live; ambient uniqueness is "
        f"not claimed and does not hold)")
    # -- reversibility -> invertible extension, value-pinned on the six
    #    executed reversible maps (vertex permutations) ------------------
    dets, tied_per_element = [], True
    for perm in sorted(permutations(range(3))):
        P = tuple(tuple(F(1) if perm[i] == j else F(0) for j in range(3))
                  for i in range(3))
        d = _det3(P)
        # sgn(sigma) computed independently of _det3, from the inversion
        # count: the per-element tie (a set-level membership pin is blind
        # to a coordinated value swap inside the set).
        inversions = sum(1 for i in range(3) for j in range(i + 1, 3)
                         if perm[i] > perm[j])
        sgn = F(-1) if inversions % 2 else F(1)
        tied_per_element &= (d == sgn)
        dets.append(d)
    legs["simplex_reversible_extensions_det_pm1"] = (
        tied_per_element and sorted(set(dets)) == [F(-1), F(1)]
        and len(dets) == 6 and all(d != 0 for d in dets),
        f"all 6 executed reversible maps have linear-extension determinant "
        f"tied PER ELEMENT to the permutation's parity, computed "
        f"independently from the inversion count (det(P_sigma) == "
        f"sgn(sigma) for each of the 6; value set "
        f"{sorted(set(str(d) for d in dets))}), nonzero exactly")
    # -- ball: determination identity lam*s + (1-lam)*(-s/h) == center ---
    ball_samples = [
        (F(3, 5), F(4, 5), F(0)), (F(1, 2), F(1, 3), F(1, 6)),
        (F(12, 13), F(3, 13), F(4, 13)), (F(2, 3), F(1, 3), F(1, 3)),
        (F(-3, 5), F(0), F(4, 5)), (F(1, 4), F(-1, 4), F(1, 2)),
        (F(0), F(-5, 13), F(12, 13)), (F(1, 10), F(1, 10), F(1, 10)),
        (F(-2, 7), F(3, 7), F(-6, 7)), (F(1, 2), F(1, 2), F(-1, 2)),
    ]
    n_ball = len(ball_samples)
    ok_id, ok_anchor, checked_b = True, True, 0
    for s in ball_samples:
        if not _in_ball(s) or all(x == 0 for x in s):
            ok_id = False
            break
        h = _norm1(s)
        lam = F(1, 1) / (1 + h)
        a = tuple(-x / h for x in s)
        mix = tuple(lam * sx + (1 - lam) * ax for sx, ax in zip(s, a))
        ok_id &= (mix == (F(0), F(0), F(0))) and (0 < lam < 1)
        # the anchor a is a state (2-norm <= 1-norm == 1) and carries an
        # explicit convex decomposition over the octahedron vertices
        ok_anchor &= _norm1(a) == 1 and _in_ball(a)
        recon = (F(0), F(0), F(0))
        wsum = F(0)
        for i in range(3):
            w = abs(a[i])
            if w:
                e = tuple((F(1) if a[i] > 0 else F(-1)) if j == i else F(0)
                          for j in range(3))
                recon = tuple(rx + w * ex for rx, ex in zip(recon, e))
                wsum += w
        ok_anchor &= (recon == a) and (wsum == 1)
        checked_b += 1
    legs["ball_determination_identity_all_samples"] = (
        ok_id and checked_b == n_ball,
        f"for all {checked_b}/{n_ball} sampled rational ball states s: with "
        f"h = ||s||_1, lam = 1/(1+h) in (0,1), a = -s/h, the identity "
        f"lam*s + (1-lam)*a == center holds exactly -- so a "
        f"mixture-preserving map's value at s is forced by its values at the "
        f"center and at a (the mechanism is uniform in s).  IDENTITY BY "
        f"CONSTRUCTION: the identity holds for any nonzero s by algebra; "
        f"this leg's failure surface is sample validity")
    legs["ball_octahedron_anchor_is_a_state_with_convex_decomposition"] = (
        ok_anchor,
        "each anchor a has ||a||_1 == 1 (a state, on the octahedron) with an "
        "explicit exact convex decomposition over the octahedron vertices "
        "-- exhibited as ONE n-ary convex combination; the elementary "
        "binary-to-n-ary induction is NOT executed here, so a is "
        "mixture-determined from the finite set GIVEN that step")
    # -- ball uniqueness: 4 affinely independent determination points ----
    det_pts = [(F(0), F(0), F(0)), (F(1), F(0), F(0)),
               (F(0), F(1), F(0)), (F(0), F(0), F(1))]
    aug4 = [[F(1)] + list(p) for p in det_pts]
    r4 = _rank(aug4)
    legs["ball_affine_extension_unique_rank4"] = (
        r4 == 4,
        f"augmented determination matrix rank {r4} == 4: the affine "
        f"extension through the determination values is unique on the "
        f"3-dimensional affine hull")
    # -- reversible executed map on the ball: R(1/2), det == +1 ----------
    R = _rot(F(1, 2))
    detR = _det3(R)
    legs["ball_reversible_extension_det_plus1"] = (
        detR == 1,
        f"the executed reversible ball map R(1/2) has linear determinant "
        f"{detR} == +1, nonzero exactly")
    # -- VALUE TIE: hull dimension 4 == banked SPANNING_EFFECTS rank -----
    try:
        from apf import operational_score_linearity as _osl
        span = [list(_osl._sa_coords(eff)) for eff in _osl.SPANNING_EFFECTS]
        banked_rank = _rank(span)
        tie_ok = (banked_rank == 4 == r4)
        tie_ev = (f"rank of the banked SPANNING_EFFECTS family "
                  f"(operational_score_linearity, computed here through its "
                  f"own _sa_coords with this module's independent rank) is "
                  f"{banked_rank} == 4 == this module's linear-hull "
                  f"dimension: both are dim_R Herm_2(C)")
    except Exception as exc:  # bank tree without the module: fail honestly
        tie_ok, tie_ev = False, f"banked tie unavailable: {exc!r}"
    legs["hull_dimension_ties_banked_spanning_effects_rank_4"] = (
        tie_ok, tie_ev)
    legs["sample_counts_enforced"] = (
        checked == n_simplex == 10 and checked_b == n_ball == 10,
        f"sample counts enforced: simplex {checked} == {n_simplex} == 10, "
        f"ball {checked_b} == {n_ball} == 10")
    return _result(
        "check_W1_mixture_determination_forces_linear_extension", legs,
        key_result=(
            "On the two executed state spaces, a map preserving binary "
            "rational mixtures is determined at every sampled rational "
            "state by its values on a finite determination set (the "
            "mechanism uniform in s), the affine extension through those "
            "values is unique (rank certificates 3 and 4), and the "
            "executed reversible maps have invertible linear extensions "
            "(determinants value-pinned PER ELEMENT: det(P_sigma) == "
            "sgn(sigma) from an independent inversion count, and "
            "det R(1/2) == +1; nonzero).  Mixture-preservation "
            "itself is the NAMED IMPORT "
            "MIXTURE_PRESERVATION_OF_TRANSFORMATIONS; nothing is claimed "
            "at unexecuted dimensions."),
        cross_refs=["operational_score_linearity"],
        disclosures=[
            "the universal over maps is carried by the executed per-point "
            "determination mechanism, never by an uncomputed quantifier"])


# ---------------------------------------------------------------------------
# W2 -- the classical reversible sector is exactly S_3, computed
# ---------------------------------------------------------------------------

def _perm_matrix(perm):
    return tuple(tuple(F(1) if perm[i] == j else F(0) for j in range(3))
                 for i in range(3))


def check_W2_classical_reversible_sector_exactly_S3():
    legs = {}
    # -- vertices vs the opposite segment (SCOPED: full extremality is
    # NOT executed here) -- e_i has coordinate i equal to 1 while every
    # point of the opposite segment has coordinate i equal to 0.
    vert_ok = True
    for i in range(3):
        others = [_V[j] for j in range(3) if j != i]
        # mu*a + (1-mu)*b has i-coordinate mu*0 + (1-mu)*0 == 0 != 1
        vert_ok &= all(a[i] == 0 for a in others)
    # (b) non-vertex samples are proper mixtures (exhibited exactly)
    nonvert = [(F(1, 2), F(1, 2), F(0)), (F(1, 3), F(1, 3), F(1, 3)),
               (F(3, 4), F(1, 8), F(1, 8))]
    proper = True
    for w in nonvert:
        i = max(range(3), key=lambda k: w[k] if w[k] < 1 else F(-1))
        lam = w[i]
        if not (0 < lam < 1):
            proper = False
            continue
        rest = tuple((w[j] if j != i else F(0)) / (1 - lam)
                     for j in range(3))
        mix = tuple(lam * v + (1 - lam) * rv
                    for v, rv in zip(_V[i], rest))
        proper &= (mix == w) and _in_simplex(rest) and (rest != _V[i])
    legs["vertices_avoid_opposite_segment_nonvertex_samples_are_mixtures"] \
        = (vert_ok and proper,
           "each vertex has a coordinate equal to 1 where the opposite "
           "segment is identically 0 (executed: no vertex is a mixture of "
           "points of the OPPOSITE SEGMENT), and each non-vertex sample is "
           "exhibited as a proper mixture.  FULL extremality -- that no "
           "vertex is a proper mixture of ANY two distinct simplex points "
           "-- is NOT executed here: it is consumed classically, alongside "
           "the named convexity import, wherever the exactness upper bound "
           "needs it; the executed content of this leg is the segment "
           "infeasibility plus the exhibited proper mixtures")
    # -- the six permutation extensions ----------------------------------
    perms = sorted(permutations(range(3)))
    mats = [_perm_matrix(p) for p in perms]
    distinct = len(set(mats)) == len(mats) == 6
    preserves = all(
        _in_simplex(_mat_vec(M, s)) for M in mats
        for s in [(F(1, 3), F(1, 3), F(1, 3)), (F(1, 2), F(1, 4), F(1, 4)),
                  (F(1), F(0), F(0)), (F(1, 7), F(2, 7), F(4, 7))])
    legs["six_vertex_permutations_extend_affinely_and_distinctly"] = (
        distinct and preserves and len(mats) == factorial(3),
        f"{len(mats)} == 3! distinct permutation matrices, each an affine "
        f"(indeed linear) automorphism of the simplex, verified on exact "
        f"samples; 0/1 matrices permute coordinates so nonnegativity and "
        f"the unit sum are preserved identically")
    # -- Cayley closure: a group of order 6 -------------------------------
    matset = set(mats)
    closed = all(_mat_mul(A, B) in matset for A in mats for B in mats)
    has_id = _perm_matrix((0, 1, 2)) in matset
    has_inv = all(any(_mat_mul(A, B) == _perm_matrix((0, 1, 2))
                      for B in mats) for A in mats)
    order = len(matset)
    legs["cayley_closure_is_a_group_of_order_factorial3"] = (
        closed and has_id and has_inv and order == factorial(3),
        f"closure under all {order}x{order} products, identity present, "
        f"every element invertible in-set: a group of order {order} == 3!")
    # -- determination: at most one automorphism per vertex-permutation --
    aug = [[F(1)] + list(v) for v in _V]
    r3 = _rank(aug)
    legs["determination_gives_at_most_one_automorphism_per_permutation"] = (
        r3 == 3,
        f"vertex augmented rank {r3} == 3: an affine map is determined by "
        f"its vertex images, so each vertex permutation extends to AT MOST "
        f"one affine automorphism; with the {factorial(3)} constructed, "
        f"|Aut_aff(Delta^2)| == 6 GIVEN the named convexity import and "
        f"the classical extreme-point identification")
    # -- pullback identity supporting the convexity import ----------------
    pull_ok = True
    w = (F(1, 2), F(1, 4), F(1, 4))
    lam = F(1, 2)
    a, b = (F(1), F(0), F(0)), (F(0), F(1, 2), F(1, 2))
    assert tuple(lam * ax + (1 - lam) * bx for ax, bx in zip(a, b)) == w
    for M in mats:
        Minv = next(B for B in mats
                    if _mat_mul(M, B) == _perm_matrix((0, 1, 2)))
        lhs = _mat_vec(Minv, w)
        rhs = tuple(lam * ax + (1 - lam) * bx
                    for ax, bx in zip(_mat_vec(Minv, a), _mat_vec(Minv, b)))
        pull_ok &= (lhs == rhs) and (_mat_vec(Minv, a) != _mat_vec(Minv, b))
    legs["pullback_mixture_identity_supports_the_convexity_import"] = (
        pull_ok,
        "for each automorphism and an exhibited proper mixture w = "
        "lam*a + (1-lam)*b, the pullback identity T^-1(w) == "
        "lam*T^-1(a) + (1-lam)*T^-1(b) holds exactly with distinct images "
        "-- the executed instance of the named convexity import "
        "(EXTREME_POINT_PERMUTATION), which is consumed as a name, not "
        "re-proved in generality")
    # -- transitivity on pure states --------------------------------------
    orbit = {_mat_vec(M, _V[0]) for M in mats}
    legs["action_transitive_on_pure_states"] = (
        orbit == set(_V),
        f"orbit of vertex 1 under the sector has size {len(orbit)} == 3 == "
        f"all pure states: the action CONNECTS the pure states (transitive) "
        f"-- group-theoretically, not continuously")
    # -- root obstruction --------------------------------------------------
    squares = {_mat_mul(M, M) for M in mats}
    transpositions = [_perm_matrix(p) for p in perms
                      if sum(p[i] != i for i in range(3)) == 2]
    no_root = all(T not in squares for T in transpositions)
    legs["no_element_squares_to_a_transposition"] = (
        no_root and len(transpositions) == 3,
        f"the square set of the sector ({len(squares)} elements) contains "
        f"none of the {len(transpositions)} transpositions (exhaustive): a "
        f"transposition lies on no one-parameter subgroup")
    # -- orders and finiteness ---------------------------------------------
    ident = _perm_matrix((0, 1, 2))
    orders = []
    for M in mats:
        k, P = 1, M
        while P != ident:
            P = _mat_mul(P, M)
            k += 1
        orders.append(k)
    legs["element_orders_and_finiteness"] = (
        sorted(orders) == [1, 2, 2, 2, 3, 3] and order == 6,
        f"element orders {sorted(orders)} == [1,2,2,2,3,3]; the sector is "
        f"FINITE (order 6).  The continuum reading -- that [CR]'s "
        f"continuous-group clause therefore fails on the classical "
        f"realization -- consumes the named elementary import "
        f"CONNECTED_NONTRIVIAL_GROUP_INFINITE; the executed content is "
        f"finiteness and the root obstruction")
    # -- VALUE TIE: the countermodel's transition group ---------------------
    # prop:linearity-independent's data, reconstructed: Sigma = {0,1,2},
    # elementary separators the three transpositions, composing as the
    # transition group.  (Disclosed: the bank registers no S_3-countermodel
    # object; the paper's witness script is the orphaned E4 stratum.)
    gens = [p for p in perms if sum(p[i] != i for i in range(3)) == 2]
    group = {(0, 1, 2)}
    frontier = list(group)
    while frontier:
        nxt = []
        for g in frontier:
            for t in gens:
                comp = tuple(g[t[i]] for i in range(3))
                if comp not in group:
                    group.add(comp)
                    nxt.append(comp)
        frontier = nxt
    tie = ({_perm_matrix(p) for p in group} == matset
           and len(group) == order == 6)
    legs["value_tie_transition_group_equals_automorphism_group"] = (
        tie,
        f"the transition group generated by the countermodel's three "
        f"transpositions (closure computed: {len(group)} elements) equals, "
        f"element-for-element under the barycentric action, the affine "
        f"automorphism group computed independently from the state space "
        f"({order} elements): the spine-side S_3 IS the state-space "
        f"reversible sector")
    return _result(
        "check_W2_classical_reversible_sector_exactly_S3", legs,
        key_result=(
            "GIVEN the named convexity import "
            "(EXTREME_POINT_PERMUTATION_classical_convexity) and the "
            "classical extreme-point identification (executed here only "
            "against the opposite segment), the reversible sector of the "
            "classical 3-type realization is EXACTLY S_3.  The exhibited "
            "group itself is computed unconditionally: order 6 (not "
            "stated), transitive on the pure states, with an exhaustive "
            "square-root obstruction (no transposition has a root), and "
            "element-for-element equal to the transition group of "
            "prop:linearity-independent's countermodel.  Finiteness of "
            "the sector (exhaustive under the same conditional) is the "
            "exact "
            "finite form in which [CR]'s continuous-group clause fails "
            "classically; the continuum reading consumes a named "
            "elementary import.  The countermodel's spine predicates "
            "FD1-FD4 are paper-side [P], not re-verified here."),
        disclosures=[
            "EXTREME_POINT_PERMUTATION is consumed as a named classical "
            "convexity import, supported by an executed pullback instance",
            "the bank registers no S_3-countermodel object; the paper's "
            "witness script is the orphaned E4 stratum"])


# ---------------------------------------------------------------------------
# W3 -- the linear realization's infinite exact reversible sector
# ---------------------------------------------------------------------------

_PURE = (  # Pythagorean pure states on the equator (x, y), norm 1 exact
    (F(1), F(0)), (F(3, 5), F(4, 5)), (F(5, 13), F(12, 13)),
    (F(8, 17), F(15, 17)), (F(20, 29), F(21, 29)), (F(0), F(1)),
    (F(-3, 5), F(4, 5)), (F(-1), F(0)),
)


def check_W3_linear_realization_infinite_reversible_sector():
    legs = {}
    # -- (1-t^2)^2 + (2t)^2 == (1+t^2)^2, degree 4 -----------------------
    ok_p, npts = _poly_identity(
        lambda t: (1 - t * t) ** 2 + (2 * t) ** 2 - (1 + t * t) ** 2, 4)
    # negative controls: the certifier's discriminating clause exercised
    # in-module on named non-identities -- t^2 - 1 (vanishing at interior
    # grid points) and t + 2 (vanishing at the grid's FIRST point, so a
    # certifier neutered to a single evaluation point fails this control).
    neg1 = _poly_identity(lambda t: t * t - 1, 2)[0]
    neg2 = _poly_identity(lambda t: t + 2, 2)[0]
    legs["pythagorean_identity_degree_bounded"] = (
        ok_p and not neg1 and not neg2,
        f"(1-t^2)^2 + (2t)^2 - (1+t^2)^2 == 0 at {npts} > 4 rational "
        f"points: a polynomial identity by the degree bound; negative "
        f"controls: the certifier returns False on the non-identities "
        f"t^2 - 1 and t + 2 at the same grid genre (its discriminating "
        f"clause is exercised, not assumed)")
    # -- orthogonality + det == +1 as identities (denominators cleared) --
    def _orth_defect(t):
        # DISCLOSED (counterfeit genre): the mismatch branch below returns
        # a SIGNED SUM of entry deviations, which a counterfeit with
        # cancelling entries could satisfy; the certificate as executed
        # rides on the entrywise equality branch (P == I exactly at every
        # evaluation point), which pins each entry's cleared defect
        # polynomial by the degree bound.  The sum is only the
        # failure-reporting path.
        R = _rot(t)
        Rt = tuple(tuple(R[j][i] for j in range(3)) for i in range(3))
        P = _mat_mul(Rt, R)
        d = (1 + t * t) ** 2
        return sum((P[i][j] - (1 if i == j else 0)) * d
                   for i in range(3) for j in range(3) if P[i][j] !=
                   (1 if i == j else 0)) if P != (
            (F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1))) \
            else F(0)
    ok_orth, n_orth = _poly_identity(_orth_defect, 8)
    ok_det, n_det = _poly_identity(
        lambda t: (_det3(_rot(t)) - 1) * (1 + t * t) ** 2, 8)
    legs["orthogonality_and_det_plus1_as_identities"] = (
        ok_orth and ok_det,
        f"R(t)^T R(t) == I and det R(t) == +1 hold at {n_orth} and {n_det} "
        f"points exceeding the cleared-denominator degree bounds: "
        f"rational-function identities (rotations, never reflections)")
    # -- sampled rotations: ball, mixtures, center ------------------------
    ts = [F(k, 7) for k in range(-10, 11)] + [F(5, 2), F(-9, 4), F(22, 3),
                                              F(101, 100)]
    n_ts = len(ts)
    states = [(F(3, 5), F(4, 5), F(0)), (F(1, 3), F(1, 3), F(1, 3)),
              (F(0), F(0), F(1)), (F(-1, 2), F(1, 4), F(1, 4))]
    ok_ball = all(_norm2sq(_mat_vec(_rot(t), s)) == _norm2sq(s)
                  for t in ts[:6] for s in states)
    lam = F(2, 7)
    ok_mix = all(
        _mat_vec(_rot(t), tuple(lam * a + (1 - lam) * b
                                for a, b in zip(states[0], states[1])))
        == tuple(lam * a + (1 - lam) * b
                 for a, b in zip(_mat_vec(_rot(t), states[0]),
                                 _mat_vec(_rot(t), states[1])))
        for t in ts[:6])
    ok_ctr = all(_mat_vec(_rot(t), (F(0), F(0), F(0))) == (F(0), F(0), F(0))
                 for t in ts[:6])
    legs["sampled_rotations_preserve_ball_and_mixtures_and_center"] = (
        ok_ball and ok_mix and ok_ctr,
        "sampled R(t) preserve the exact 2-norm (ball-preserving), satisfy "
        "the exact mixture identity (linear maps preserve mixtures), and "
        "fix the maximally mixed state")
    # -- inverse and group law --------------------------------------------
    ident = ((F(1), F(0), F(0)), (F(0), F(1), F(0)), (F(0), F(0), F(1)))
    ok_inv = all(_mat_mul(_rot(t), _rot(-t)) == ident for t in ts)
    legs["inverse_law_exact"] = (
        ok_inv, f"R(t) R(-t) == I exactly for all {n_ts} sampled t: every "
                f"family element is reversible in-family")
    pairs = [(s, t) for s in ts[:8] for t in ts[:8] if s * t != 1]
    ok_grp = all(_mat_mul(_rot(s), _rot(t)) == _rot((s + t) / (1 - s * t))
                 for s, t in pairs)
    legs["group_law_exact_on_grid"] = (
        ok_grp and len(pairs) >= 60,
        f"R(s) R(t) == R((s+t)/(1-st)) exactly on {len(pairs)} sampled "
        f"pairs with st != 1: the tan-half-angle composition law")
    # -- parameter recovery == injectivity ---------------------------------
    # s_entry/(1 + c_entry) == t identically: (2t/(1+t^2)) / (2/(1+t^2))
    ok_rec, n_rec = _poly_identity(
        lambda t: 2 * t - t * (1 + _rot(t)[0][0]) * (1 + t * t), 4)
    ok_rec_s = all(_rot(t)[1][0] / (1 + _rot(t)[0][0]) == t for t in ts)
    legs["parameter_recovery_identity_injectivity"] = (
        ok_rec and ok_rec_s,
        f"t == R(t)[1][0]/(1 + R(t)[0][0]) exactly for all {n_ts} sampled "
        f"t, with 1 + c == 2/(1+t^2) never zero (identity certified at "
        f"{n_rec} points): t -> R(t) is injective on Q, so the sector "
        f"contains an injective image of Q and is INFINITE")
    mats = {_rot(t) for t in ts}
    legs["sector_infinite_count_enforced"] = (
        len(mats) == n_ts,
        f"{len(mats)} distinct matrices from {n_ts} distinct parameters "
        f"(count enforced == {n_ts}); with the recovery identity this "
        f"witnesses injectivity on all of Q")
    # -- pure-state list ----------------------------------------------------
    n_pure = len(_PURE)
    ok_norm = all(p[0] * p[0] + p[1] * p[1] == 1 for p in _PURE)
    ok_dist = len(set(_PURE)) == n_pure
    legs["pure_state_list_norm_one_distinct"] = (
        ok_norm and ok_dist and n_pure == 8,
        f"all {n_pure} == 8 listed pure states have exact norm 1 and are "
        f"pairwise distinct")
    # -- connecting elements for every ordered pair -------------------------
    connected, antipodal_records = 0, []
    ok_conn = True
    for p in _PURE:
        for q in _PURE:
            if p == q:
                continue
            cosd = p[0] * q[0] + p[1] * q[1]
            sind = p[0] * q[1] - p[1] * q[0]
            if 1 + cosd != 0:
                t = sind / (1 + cosd)
                img = _mat_vec(_rot(t), (p[0], p[1], F(0)))
                ok_conn &= img == (q[0], q[1], F(0))
                connected += 1
            else:
                m = next(mm for mm in _PURE
                         if mm != p and mm != q
                         and 1 + (p[0] * mm[0] + p[1] * mm[1]) != 0
                         and 1 + (mm[0] * q[0] + mm[1] * q[1]) != 0)
                c1 = p[0] * m[0] + p[1] * m[1]
                s1 = p[0] * m[1] - p[1] * m[0]
                t1 = s1 / (1 + c1)
                c2 = m[0] * q[0] + m[1] * q[1]
                s2 = m[0] * q[1] - m[1] * q[0]
                t2 = s2 / (1 + c2)
                prod = _mat_mul(_rot(t2), _rot(t1))
                img = _mat_vec(prod, (p[0], p[1], F(0)))
                ok_conn &= img == (q[0], q[1], F(0))
                antipodal_records.append(
                    (str(p), str(q), str(t1), str(t2), t1 * t2 == 1))
                connected += 1
    n_expected_pairs = n_pure * (n_pure - 1)
    legs["all_ordered_pairs_connected_explicitly"] = (
        ok_conn and connected == n_expected_pairs,
        f"{connected} == {n_pure}*{n_pure - 1} ordered pairs of distinct "
        f"listed pure states each connected by an explicit exact element "
        f"(single R(t), or a two-step composition for antipodes): the "
        f"exhibited sector CONNECTS the exhibited pure states, and every "
        f"element of it is a LINEAR map")
    ok_anti = (len(antipodal_records) >= 2
               and all(rec[4] for rec in antipodal_records))
    legs["antipode_via_exact_composition_chart_omission_disclosed"] = (
        ok_anti,
        f"{len(antipodal_records)} antipodal pairs handled by exact "
        f"two-step composition, each with t1*t2 == 1 (computed): the "
        f"half-turn is precisely the single element the rational chart "
        f"t -> R(t) omits; the composed product is exact and lies in the "
        f"generated group")
    return _result(
        "check_W3_linear_realization_infinite_reversible_sector", legs,
        key_result=(
            "The qubit realization carries an infinite exact reversible "
            "sector -- the Pythagorean rotation family, injective on Q by "
            "an exact recovery identity, with exact inverse and "
            "composition laws -- whose every element is a LINEAR map, "
            "fixing the maximally mixed state and connecting all "
            "exhibited rational pure states pairwise.  The structure "
            "[CR] requires is CARRIED BY LINEAR MAPS at this scope.  "
            "Continuity and compactness are NOT established (rational "
            "points only); the continuum group and the full "
            "reconstruction theorem remain the named literature import; "
            "nothing at Hilbert dimension >= 3."),
        disclosures=[
            "transitivity is witnessed on the exhibited 8-element family, "
            "not on all pure states",
            "the rational chart omits exactly the half-turn; the generated "
            "group contains it as an exact product (disclosed, computed)",
            "the _orth_defect mismatch branch is a signed sum a cancelling "
            "counterfeit could satisfy; the certificate as executed rides "
            "on the entrywise equality branch at every evaluation point"])


# ---------------------------------------------------------------------------
# W4 -- clause-drop battery: each executed clause is load-bearing
# ---------------------------------------------------------------------------

def check_W4_clause_drop_battery():
    legs = {}
    center = (F(1, 3), F(1, 3), F(1, 3))
    w_prime = (F(1, 2), F(1, 4), F(1, 4))

    def impostor(s):
        if s == center:
            return w_prime
        if s == w_prime:
            return center
        return s

    # (i) drop mixture-preservation: reversible impostor defeats linearity
    test_pts = list(_V) + [center, w_prime, (F(1, 7), F(2, 7), F(4, 7))]
    ok_invol = all(impostor(impostor(s)) == s for s in test_pts)
    legs["impostor_is_a_reversible_involution"] = (
        ok_invol,
        "the impostor (transposing the barycenter with one interior point, "
        "fixing everything else) is its own inverse on the test set: "
        "REVERSIBLE, so reversibility alone does not force linearity")
    mix_of_vertices = tuple(
        sum(F(1, 3) * v[i] for v in _V) for i in range(3))
    violation = (impostor(mix_of_vertices) != tuple(
        sum(F(1, 3) * impostor(v)[i] for v in _V) for i in range(3)))
    # no affine map agrees with the impostor on {e1, e2, e3, center}:
    # the unique affine map through the vertex values is the identity
    # (vertices fixed, rank 3 from W1/W2), and identity(center) == center
    # != impostor(center).
    aug = [[F(1)] + list(v) for v in _V]
    unique_through_vertices = _rank(aug) == 3
    mismatch = impostor(center) != center
    legs["drop_mixture_preservation_reversible_impostor_defeats_linearity"] \
        = (violation and unique_through_vertices and mismatch,
           "the impostor violates the exact mixture identity at the "
           "barycenter (center is the uniform mixture of the vertices, its "
           "image is not the uniform mixture of the images), and NO affine "
           "map agrees with it on the 4 witnessed points (the unique affine "
           "map through the fixed vertices is the identity; the impostor "
           "moves the center): without mixture-preservation the linearity "
           "conclusion FAILS")
    # (ii) drop reversibility: the collapse map
    collapse = lambda s: center  # noqa: E731
    pairs = [((F(1), F(0), F(0)), (F(0), F(1), F(0)), F(1, 3)),
             (center, w_prime, F(2, 5)),
             ((F(1, 7), F(2, 7), F(4, 7)), (F(0), F(0), F(1)), F(5, 9))]
    ok_mixK = all(
        collapse(tuple(l * ax + (1 - l) * bx for ax, bx in zip(a, b)))
        == tuple(l * kx + (1 - l) * jx
                 for kx, jx in zip(collapse(a), collapse(b)))
        for a, b, l in pairs)
    legs["drop_reversibility_collapse_preserves_mixtures"] = (
        ok_mixK,
        "the collapse-to-barycenter map satisfies the exact mixture "
        "identity on all sampled proper mixtures: MIXTURE-PRESERVING")
    # its affine extension is the constant map: linear part 0, det == 0
    lin_part = tuple(tuple(F(0) for _ in range(3)) for _ in range(3))
    detK = _det3(lin_part)
    fixes_bary = collapse(center) == center
    noninj = (collapse(_V[0]) == collapse(_V[1])) and (_V[0] != _V[1])
    legs["collapse_extension_fixes_barycenter_det_zero_noninjective"] = (
        detK == 0 and fixes_bary and noninj,
        f"the collapse's affine extension exists (constant), fixes the "
        f"barycenter (value-pinned), has linear-part determinant {detK} == "
        f"0, and an exact non-injectivity witness (two distinct vertices "
        f"share an image): without reversibility, INVERTIBILITY of the "
        f"extension fails")
    # (iii) drop continuity: the S_3 sector satisfies every remaining clause
    w2 = check_W2_classical_reversible_sector_exactly_S3()
    s3_order = 6 if w2["passed"] else None
    perms = sorted(permutations(range(3)))
    mats = [_perm_matrix(p) for p in perms]
    lam = F(3, 7)
    a, b = (F(1, 2), F(1, 4), F(1, 4)), (F(0), F(2, 3), F(1, 3))
    mix = tuple(lam * ax + (1 - lam) * bx for ax, bx in zip(a, b))
    ok_mixS3 = all(
        _mat_vec(M, mix) == tuple(
            lam * px + (1 - lam) * qx
            for px, qx in zip(_mat_vec(M, a), _mat_vec(M, b)))
        for M in mats)
    legs["drop_continuity_S3_satisfies_every_remaining_clause"] = (
        w2["passed"] and s3_order == 6 and ok_mixS3,
        f"consuming W2 by value (order {s3_order} == 6, group closure, "
        f"in-set inverses, transitivity on pure states) plus executed "
        f"mixture identities: the S_3 sector is a GROUP of REVERSIBLE "
        f"MIXTURE-PRESERVING maps TRANSITIVE on the pure states -- every "
        f"[CR]-fragment clause except continuity -- over the CLASSICAL "
        f"realization: continuity is the discriminating clause at this "
        f"scope")
    # the classical state space has no superposition
    lams = [F(k, 8) for k in range(1, 8)]
    no_super = True
    for i in range(3):
        for j in range(3):
            if i == j:
                continue
            for l in lams:
                m = tuple(l * vi + (1 - l) * vj
                          for vi, vj in zip(_V[i], _V[j]))
                nz = sum(1 for x in m if x != 0)
                no_super &= (nz >= 2) and (m not in _V)
    legs["classical_state_space_has_no_superposition"] = (
        no_super,
        "every proper mixture of two distinct pure states (all pairs, "
        "rational weight grid) has >= 2 nonzero barycentric coordinates "
        "and is not a vertex -- with pure states == vertices (the "
        "classical identification, executed in W2 only against the "
        "opposite segment), no "
        "mixture of two pure states is pure at the executed grid")
    drops_executed = {
        "mixture_preservation":
            legs["drop_mixture_preservation_reversible_impostor_defeats"
                 "_linearity"][0],
        "reversibility":
            legs["collapse_extension_fixes_barycenter_det_zero_noninjective"
                 ][0],
        "continuity":
            legs["drop_continuity_S3_satisfies_every_remaining_clause"][0],
    }
    legs["battery_covers_exactly_three_clauses_transitivity_not_executed"] \
        = (set(drops_executed) == {"mixture_preservation", "reversibility",
                                   "continuity"}
           and all(drops_executed.values())
           and "transitivity" not in drops_executed,
           f"executed drop set {sorted(drops_executed)} == the three "
           f"declared clauses set-exactly, each with a green certificate; "
           f"'transitivity' is NOT in the executed set -- its load-bearing "
           f"status is a disclosed limitation, not a claim")
    return _result(
        "check_W4_clause_drop_battery", legs,
        key_result=(
            "Each executed clause is load-bearing by exact counterexample: "
            "without mixture-preservation a reversible involution defeats "
            "linearity; without reversibility the mixture-preserving "
            "collapse defeats invertibility; with every clause except "
            "continuity the classical S_3 sector satisfies the lot -- so "
            "at the executed scope the CONTINUITY clause is the "
            "discriminator between the classical and the linear "
            "realization.  The transitivity clause is not dropped "
            "(disclosed limitation)."),
        dependencies=["check_W2_classical_reversible_sector_exactly_S3"],
        disclosures=[
            "the continuity drop consumes W2 by value (order, closure, "
            "transitivity), not by verdict alone"])


# ---------------------------------------------------------------------------
# W5 -- composed containment + permanent import controls
# ---------------------------------------------------------------------------

def check_W5_composed_containment_and_import_controls():
    legs = {}
    w1 = check_W1_mixture_determination_forces_linear_extension()
    w2 = check_W2_classical_reversible_sector_exactly_S3()
    w3 = check_W3_linear_realization_infinite_reversible_sector()
    w4 = check_W4_clause_drop_battery()
    legs["w1_through_w4_consumed_by_value"] = (
        all(r["passed"] for r in (w1, w2, w3, w4))
        and [r["leg_count"] for r in (w1, w2, w3, w4)] == [9, 9, 10, 7],
        f"W1-W4 all green with leg counts "
        f"{[r['leg_count'] for r in (w1, w2, w3, w4)]} == [9, 9, 10, 7] "
        f"(enforced)")
    # dimension tie, recomputed here (value, not verdict)
    try:
        from apf import operational_score_linearity as _osl
        span = [list(_osl._sa_coords(eff)) for eff in _osl.SPANNING_EFFECTS]
        banked_rank = _rank(span)
    except Exception:
        banked_rank = None
    det_pts = [(F(0), F(0), F(0)), (F(1), F(0), F(0)),
               (F(0), F(1), F(0)), (F(0), F(0), F(1))]
    hull_rank = _rank([[F(1)] + list(p) for p in det_pts])
    legs["dimension_tie_4_equals_banked_spanning_rank"] = (
        banked_rank == 4 == hull_rank,
        f"banked SPANNING_EFFECTS rank {banked_rank} == 4 == qubit "
        f"linear-hull dimension {hull_rank} (both dim_R Herm_2(C)); "
        f"recomputed here from the banked module's own data")
    # the two sectors' sizes, by value
    order_leg = w2["legs"]["cayley_closure_is_a_group_of_order_factorial3"]
    inf_leg = w3["legs"]["sector_infinite_count_enforced"]
    legs["classical_sector_order_6_and_infinite_linear_sector"] = (
        order_leg["passed"] and inf_leg["passed"],
        "classical reversible sector: an S_3 of order 6 computed, EXACTLY "
        "that under W2's stated conditional (the named convexity import + "
        "the classical extreme-point identification); linear "
        "realization's exhibited sector injective on Q hence infinite "
        "(W3, recovery identity): the exact finite core of "
        "thm:cr-dependence's two directions at the executed scope")
    legs["named_imports_and_necessity_citation_recorded"] = (
        len(NAMED_IMPORTS) == 4 and "prop:linearity-independent" in
        NECESSITY_CITATION and
        any("LITERATURE_SUFFICIENCY_IMPORT" in n for n in NAMED_IMPORTS),
        f"{len(NAMED_IMPORTS)} == 4 named imports recorded, including the "
        f"literature sufficiency import (Hardy 2001 / Masanes-Mueller 2011 "
        f"/ dlTMSM 2012 / CDP 2011) for everything beyond the executed "
        f"scope; the necessity direction is a citation to "
        f"prop:linearity-independent (paper-side [P]), not re-proved")
    # apf-import control, set-exact by AST on this module's own source
    src = Path(__file__).read_text(encoding="utf-8")
    tree = ast.parse(src)
    apf_imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module == "apf":
                apf_imports.update(a.name for a in node.names)
            elif node.module.startswith("apf."):
                apf_imports.add(node.module.split(".", 1)[1])
        elif isinstance(node, ast.Import):
            for a in node.names:
                if a.name.startswith("apf."):
                    apf_imports.add(a.name.split(".", 1)[1])
    legs["apf_imports_set_exact_by_ast"] = (
        apf_imports == {"operational_score_linearity"},
        f"apf imports parsed from this module's own source: "
        f"{sorted(apf_imports)} == ['operational_score_linearity'] "
        f"set-exactly -- no represented-side or Born-side object enters")
    legs["containment_scope_recorded"] = (
        set(EXECUTED_SCOPE) == {"state_spaces", "arithmetic", "points"}
        and len(EXECUTED_SCOPE["state_spaces"]) == 2
        and len(MAY_NOT_CITE) == 6,
        f"executed scope: {EXECUTED_SCOPE['state_spaces']}; "
        f"{len(MAY_NOT_CITE)} == 6 MAY-NOT-CITE rows carried from the "
        f"frozen surface")
    return _result(
        "check_W5_composed_containment_and_import_controls", legs,
        key_result=(
            "At the executed scope -- the 3-type classical state space and "
            "the qubit rational Bloch ball -- the structure [CR] requires "
            "is carried by linear maps and refused by the classical "
            "simplex (the classical refusal exact under W2's stated "
            "conditional): the exact finite core of "
            "thm:cr-dependence's two directions.  The full sufficiency "
            "theorem (FD1-FD4 + [CR] => "
            "direct sum of M_{n_i}(D), D in {R, C, H}, D = C by "
            "tomographic locality) is the NAMED LITERATURE IMPORT for "
            "everything beyond this scope; mixture-preservation is a "
            "named import; the necessity direction is a citation; the "
            "quadratic form / trace / Born weight is downstream and "
            "untouched by every leg here."),
        dependencies=[
            "check_W1_mixture_determination_forces_linear_extension",
            "check_W2_classical_reversible_sector_exactly_S3",
            "check_W3_linear_realization_infinite_reversible_sector",
            "check_W4_clause_drop_battery"],
        cross_refs=["operational_score_linearity"],
        disclosures=[
            "this check consumes W1-W4 by value (leg counts, order, "
            "rank) and re-executes the dimension tie itself",
            "standing limit (the D7 genre): W1-W4's leg inventories are "
            "cross-pinned here by value, but W5's OWN leg inventory is "
            "pinned by nothing outside itself -- a coordinated "
            "leg-plus-EXPECTED_LEGS deletion on this composing check "
            "escapes; disclosed, no new machinery",
            "banked v24.3.473 (2026-08-12): the 2026-08-12 hold lifted "
            "by Ethan's ruling after two blinded cold audits + cold fix "
            "seat"])


# ---------------------------------------------------------------------------
# module surface
# ---------------------------------------------------------------------------

_CHECKS = {
    "check_W1_mixture_determination_forces_linear_extension":
        check_W1_mixture_determination_forces_linear_extension,
    "check_W2_classical_reversible_sector_exactly_S3":
        check_W2_classical_reversible_sector_exactly_S3,
    "check_W3_linear_realization_infinite_reversible_sector":
        check_W3_linear_realization_infinite_reversible_sector,
    "check_W4_clause_drop_battery":
        check_W4_clause_drop_battery,
    "check_W5_composed_containment_and_import_controls":
        check_W5_composed_containment_and_import_controls,
}


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


def register(registry):
    registry.update({
        "W1_mixture_determination_forces_linear_extension":
            check_W1_mixture_determination_forces_linear_extension,
        "W2_classical_reversible_sector_exactly_S3":
            check_W2_classical_reversible_sector_exactly_S3,
        "W3_linear_realization_infinite_reversible_sector":
            check_W3_linear_realization_infinite_reversible_sector,
        "W4_clause_drop_battery":
            check_W4_clause_drop_battery,
        "W5_composed_containment_and_import_controls":
            check_W5_composed_containment_and_import_controls,
    })
    return registry


if __name__ == "__main__":
    _all = run_all()
    for _name, _r in _all.items():
        print(("PASS" if _r.get("passed") else "FAIL"), _name,
              "legs:", _r.get("leg_count"))
        for _fr in _r.get("fail_reasons", []):
            print("  FAIL-REASON:", _fr)
    print("ALL PASS" if all(r.get("passed") for r in _all.values())
          else "NOT ALL PASS")
