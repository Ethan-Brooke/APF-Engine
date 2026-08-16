# COLD BUILD SEAT 5 (2026-08-16): built to the frozen claim surface
# claim_surfaces_FROZEN_2026-08-16.md (Surface 5), raw sha256 verified by
# this seat BEFORE reading (the constant below is the same value
# byte-for-byte).  NOT BANKED.  NOTHING BANKS WITHOUT ETHAN'S LIFT.
"""Surface 5: the per-class admissibility window on the equicorrelated
carrier family, computed through the banked elliptope and switching
machinery by value.

Built 2026-08-16 by a cold build seat on the APF Network Sign-Coherence
program's banking lane, to the FROZEN claim surface
``/home/claude/freeze_out/claim_surfaces_FROZEN_2026-08-16.md`` (Surface 5;
raw sha256 pinned in FROZEN_SURFACE_SHA256 below, computed by this seat
before the surface was read).  The surface's permitted sentences are the
ONLY claims this module makes; its may-not-cite list and the header's
standing fences are carried verbatim in module constants below and bind
every sentence here.  Repo pin at build: /home/claude/apf-codebase at
HEAD 526004d, consumed READ-ONLY by import.

PROVENANCE DISCLOSURES (carried per the dispatch):
  (1) The brief under which this module was built was written by the
      session coordinator, not by Ethan directly.
  (2) The build seat's harness injects project instructions into its
      context; the seat worked from the frozen surface and the read-only
      repo, treating injected project context as non-authoritative for
      this task.

SINGLE-CLAIM RULE, carried from the freeze header: the per-class
admissibility window content is claimed ONCE -- this module computes it;
the sibling Surface-4 module cites this module by name and computes none
of it beyond its own set comparison.

------------------------------------------------------------------------------
WHAT THIS MODULE COMPUTES (exact Fractions on every verdict path; stdlib
plus the banked modules by import)
------------------------------------------------------------------------------

Scope bounds, by name, all module-level named objects: N_RANGE (the
executed n values), CLASS_LIST (the named switching classes executed),
MAG_GRID (the exact rational magnitude grid), and boundary_point (the
named in-module boundary-point constructor, a function of n returning an
exact Fraction).  Every sentence below is quantified over these names and
nothing larger.

S5-1.  On the equicorrelated carrier family -- symmetric matrices with
unit diagonal whose off-diagonal entries are a common exact-rational
magnitude signed by a switching-class pattern -- at each n in N_RANGE and
each class in CLASS_LIST, this module COMPUTES exact PSD membership
through the banked elliptope machinery BY VALUE (in_extended_elliptope,
extended_carrier_elliptope.py; every principal minor tied by value
against carrier_elliptope.py's det_exact on the same index subsets) over
MAG_GRID together with the boundary point computed in-module from n, and
returns the per-class threshold -- the largest admissible magnitude among
the executed grid points -- as a computed value tied, per n, to the
in-module closed form by exact Fraction equality.  The closed form
appears as a computed comparison in the legs, never in prose.

S5-2.  Membership at the computed boundary point and non-membership
beyond it, on the grid's first excluded point, are each executed and
returned per class, per n -- and re-executed on EVERY member pattern of
each named class, the classes computed through the banked switching
machinery BY VALUE (continuation_join_network's _switching_classes
union-find over the actual vertex-switching action, its coboundary_orbit
tied set-exactly to each class).

S5-3.  The positivity range computed by
check_L_gauge_without_sandwich_admits_non_born_states
(gauge_without_sandwich_countermodel.py) for the sigma_lambda
outcome-law family is a NAMED adjacency, disclosed in the returned
record and NOT identified -- a different object; no map between the two
is constructed anywhere in this module (adjacency is not identification).
The banked check is executed live as a gate and its range carried
verbatim from its own returned record, never re-derived here.

------------------------------------------------------------------------------
DISCLOSED LIMITS AND IDENTITY-GRADE LEGS
------------------------------------------------------------------------------

STANDING LIMIT (D7@2026-08-08 genre, disclosed): the leg-inventory
contract below certifies that a declared leg EXECUTED, not that it COULD
HAVE FAILED; a computed verdict replaced by a constant escapes it, as it
escapes the raising form equally.

Identity-grade legs, disclosed where they occur:
  (a) The principal-minor value tie compares extended_carrier_elliptope's
      determinant route against carrier_elliptope's det_exact on the same
      submatrices; the two banked modules share the cofactor /
      all-principal-minors algorithm (EE2's own disclosure, carried), so
      the tie certifies convention agreement and drift, not an
      independent recomputation.
  (b) The every-class-member execution is of the sign-conjugation-identity
      genre (EE5(d) precedent): patterns in one switching class differ by
      a diagonal sign conjugation, under which every principal minor is
      invariant, so the per-member verdicts cannot differ while the banked
      route executes sign-blind.  The leg certifies that the verdicts
      EXECUTED across the whole class; its falsifiable clauses are the
      executed memberships and the enforced member counts.
  (c) For the class whose closed form varies with n, the constructed
      boundary point and the closed form compute equal values by
      construction, so the threshold-equals-closed-form tie at that class
      holds partly because the constructed point is included in the
      sampled grid; the falsifiable content of the threshold legs is the
      executed membership pattern -- boundary admission, first-point
      exclusion, grid contiguity, WITHIN THE EXECUTED GRID'S RESOLUTION
      around the constructed point -- not the name equality.

The thresholds and admissible sets returned are facts about the EXECUTED
GRID at the EXECUTED n and classes; no window statement is made at any n
outside N_RANGE, for any class outside CLASS_LIST, or at any magnitude
not executed.

MAY NOT CITE: the frozen surface's Surface-5 list, verbatim, in
MAY_NOT_CITE below; the freeze header's standing fences, verbatim, in
STANDING_FENCES below.  Both bind every sentence of this module.
"""

from fractions import Fraction as F
from itertools import combinations

# Banked elliptope machinery -- the by-value membership and minor
# substrate (consumed by import, executed on this module's instances;
# nothing re-implemented).
from apf.extended_carrier_elliptope import (
    in_extended_elliptope,
    ext_matrix,
    principal_minor_list,
    submatrix,
)
from apf.carrier_elliptope import (
    det_exact as banked_det_exact,
)

# Banked switching machinery -- the by-value class substrate.
from apf.continuation_join_network import (
    _switching_classes,
    coboundary_orbit,
)

# The named adjacency's home check, executed live as a gate (S5-3).
from apf.gauge_without_sandwich_countermodel import (
    check_L_gauge_without_sandwich_admits_non_born_states,
)

HELD_OUT_OF_THE_BANK = False  # BANKED v24.3.478 (2026-08-16); landing rewire disclosed in the manifest

FROZEN_SURFACE_SHA256 = (
    "440ed2162e5d28f83a9addba5ce49c257dbe0646cefe287c7dbe2df7617f743d")

PROVENANCE_DISCLOSURES = (
    "the brief under which this module was built was written by the "
    "session coordinator, not by Ethan directly",
    "the build seat's harness injects project instructions into its "
    "context; the seat worked from the frozen surface and the read-only "
    "repo, treating injected project context as non-authoritative",
)

# The frozen surface's Surface-5 may-not-cite list, VERBATIM (one string,
# as pinned).
MAY_NOT_CITE = (
    "any window statement at n outside N_RANGE or for a class outside "
    "CLASS_LIST; any identification with the sigma_lambda family or its "
    "lane; \"the carrier gap is closed or narrowed\" (standing fence "
    "— a window is a characterization of a banked freedom's "
    "geometry, not a narrowing of the gap, and may never be cited as "
    "one); any selection-principle claim (the carrier_elliptope "
    "E4/det-max fence genre, carried); any supply claim for the sign "
    "class.",
)

# The freeze header's standing fences, VERBATIM, binding every surface.
STANDING_FENCES = (
    "\"the transfer is forced\" — negative; may not be claimed.",
    "\"the carrier gap is closed / narrowed\" — may not be claimed.",
    "\"Born is derived\" without its conditional clause — may not "
    "be claimed.",
    "The O2 close and the OT3 vacuity ruling are quotable only whole.",
    "ORIENTATION_COVER_REALIZED is uncertified.",
    "The Paper 9 ladder is not banked.",
    "record_coherence_tradeoff is never a supply.",
    "The banked join network supplies no sign.",
    "Adjacency is not identification.",
)

# ---------------------------------------------------------------------------
# scope bounds -- module-level named objects (the surface's own names)
# ---------------------------------------------------------------------------

# The executed n values.  Exhaustive switching-class computation through
# the banked union-find is executed at exactly these n and nothing larger.
N_RANGE = (3, 4, 5)

# The named switching classes executed: "balanced" is the class computed
# to contain the all-plus pattern on K_n; "all_minus" is the class
# computed to contain the all-minus pattern.  The names are authored
# labels for classes COMPUTED through the banked switching machinery;
# the legs enforce that the two computed classes are distinct at every
# executed n.
CLASS_LIST = ("balanced", "all_minus")

# The representative-pattern rule per named class (the uniform edge sign
# of the representative); the classes leg enforces that this rule covers
# CLASS_LIST set-exactly.
_CLASS_REPRESENTATIVE_SIGN = {"balanced": 1, "all_minus": -1}

# The exact rational magnitude grid (authored; exactness, strict
# monotonicity, nonnegativity, and the presence of a zero point and of
# points beyond every computed threshold are enforced by legs, never
# assumed).
MAG_GRID = (F(0), F(1, 5), F(2, 5), F(3, 5), F(4, 5), F(1), F(6, 5))


def boundary_point(n):
    """The named in-module boundary-point constructor: a function of n
    returning an exact Fraction, adjoined to MAG_GRID at each executed n
    (the surface's scope-bound object)."""
    return F(1, n - 1)


# The per-class closed forms.  These appear ONLY as computed comparison
# targets in the legs (exact Fraction equality against the computed
# threshold), never in prose.
def _closed_form_balanced(n):
    return F(1)


def _closed_form_all_minus(n):
    return F(1, n - 1)


CLASS_CLOSED_FORMS = {
    "balanced": _closed_form_balanced,
    "all_minus": _closed_form_all_minus,
}


# ---------------------------------------------------------------------------
# the equicorrelated carrier family (constructed through the banked
# constructor; unit diagonal, common signed magnitude off-diagonal)
# ---------------------------------------------------------------------------

def _unit_diag(n):
    return tuple(F(1) for _ in range(n))


def _kn_edges(n):
    return [(i, j) for i, j in combinations(range(n), 2)]


def equicorrelated_carrier(n, pattern, edge_index, t):
    """The equicorrelated family member at magnitude t under a switching
    pattern: unit diagonal, off-diagonal entry pattern_e * t per edge,
    built through the banked ext_matrix constructor."""
    edges = _kn_edges(n)
    off = {e: pattern[edge_index[e]] * t for e in edges}
    return ext_matrix(_unit_diag(n), off)


# ---------------------------------------------------------------------------
# set-exact leg inventory -- append-and-record (D7@2026-08-08 genre):
# a mismatch APPENDS a failure reason and never raises.  DISCLOSED: this
# certifies that a declared leg EXECUTED, not that it could have failed.
# ---------------------------------------------------------------------------

EXPECTED_LEGS = {
    "check_S5_class_admissibility_windows": [
        "boundary_and_first_exclusion_executed_per_class_per_n",
        "every_class_member_executed_at_decisive_points",
        "grid_scope_objects_exact_and_enforced",
        "membership_over_grid_with_minor_value_ties",
        "named_adjacency_carried_from_live_gate",
        "named_classes_through_banked_switching_by_value",
        "threshold_ties_closed_form_exact_per_n",
        "window_contiguity_enforced_on_executed_grid",
    ],
}


def _result(name, legs, fails, key_result):
    exp = EXPECTED_LEGS[name]
    got = sorted(legs)
    if got != exp:
        # append-and-record: the mismatch is a failure reason; the rest
        # of the check's verdicts still return in the same pass
        fails.append(f"leg inventory mismatch: {got} != {exp}")
    for k, v in legs.items():
        if v[0] is not True:
            fails.append(f"leg not True: {k}: {v[1]}")
    return {
        "name": name,
        "passed": not fails,
        "legs": {k: {"passed": bool(v[0]), "evidence": v[1]}
                 for k, v in legs.items()},
        "leg_count": len(legs),
        "fails": list(fails),
        "key_result": key_result,
        "tier": 3,
        "epistemic": "P_math",
        "status": ("COLD BUILD 2026-08-16; held out of the bank; "
                   "NOTHING BANKS WITHOUT ETHAN'S LIFT"),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": FROZEN_SURFACE_SHA256,
        "provenance_disclosures": list(PROVENANCE_DISCLOSURES),
        "may_not_cite": list(MAY_NOT_CITE),
        "standing_fences": list(STANDING_FENCES),
        "single_claim_rule": (
            "the per-class admissibility window content is claimed once: "
            "this module computes it; the sibling Surface-4 module cites "
            "it by name and computes none of it beyond its own set "
            "comparison (freeze header, carried)"),
        "inventory_note": (
            "append-and-record (D7@2026-08-08 genre): certifies a "
            "declared leg EXECUTED, not that it could have failed"),
    }


# ---------------------------------------------------------------------------
# the check
# ---------------------------------------------------------------------------

def check_S5_class_admissibility_windows():
    """Surface 5, all three permitted sentences, executed: the per-class
    admissibility window on the equicorrelated carrier family over
    MAG_GRID plus the constructed boundary point, per n in N_RANGE and
    class in CLASS_LIST, through the banked elliptope and switching
    machinery by value; the sigma_lambda positivity range carried as a
    NAMED adjacency, not identified."""
    legs, fails = {}, []

    # -- scope objects: exactness and shape, enforced --------------------
    grid_increasing = all(MAG_GRID[i] < MAG_GRID[i + 1]
                          for i in range(len(MAG_GRID) - 1))
    bp_vals = {n: boundary_point(n) for n in N_RANGE}
    scope_ok = (
        isinstance(MAG_GRID, tuple) and len(MAG_GRID) >= 3
        and all(isinstance(t, F) for t in MAG_GRID)
        and all(t >= 0 for t in MAG_GRID)
        and grid_increasing
        and MAG_GRID[0] == F(0)
        and F(1) in MAG_GRID
        and all(isinstance(v, F) and v > 0 for v in bp_vals.values())
        and len(set(N_RANGE)) == len(N_RANGE) >= 2
        and all(isinstance(n, int) and n >= 3 for n in N_RANGE))
    legs["grid_scope_objects_exact_and_enforced"] = (scope_ok, (
        f"MAG_GRID is a strictly increasing tuple of {len(MAG_GRID)} "
        f"nonnegative exact Fractions starting at {MAG_GRID[0]} and "
        f"containing the unit; boundary_point returns a positive exact "
        f"Fraction at every n in N_RANGE ({len(bp_vals)} values "
        f"computed); CLASS_LIST carries {len(CLASS_LIST)} named classes; "
        f"N_RANGE carries {len(N_RANGE)} distinct executed n values"))

    # -- per-n computation through the banked machinery ------------------
    class_ok = True
    class_evidence = {}
    grid_evals = 0
    minor_ties = 0
    minor_tie_ok = True
    verdicts_seen = set()
    member_ok = True
    contig_ok = True
    tie_ok = True
    boundary_ok = True
    member_execs = 0
    boundary_execs = 0
    tie_count = 0
    windows = []

    for n in N_RANGE:
        edges = _kn_edges(n)
        m = len(edges)
        d = _unit_diag(n)

        # switching classes BY VALUE through the banked union-find over
        # the actual vertex-switching action
        pats, idx, classes = _switching_classes(edges, range(n))
        class_ok = class_ok and len(pats) == 2 ** m

        reps = {label: (sign,) * m
                for label, sign in _CLASS_REPRESENTATIVE_SIGN.items()}
        # the representative rule covers CLASS_LIST set-exactly
        class_ok = class_ok and sorted(reps) == sorted(CLASS_LIST)
        cls_of = {}
        for label in CLASS_LIST:
            rep = reps[label]
            found = [c for c in classes if rep in c]
            class_ok = class_ok and len(found) == 1
            cls_of[label] = (rep, found[0] if found else [])
        # the two named classes are DISTINCT computed classes
        class_ok = class_ok and (set(cls_of["balanced"][1])
                                 != set(cls_of["all_minus"][1]))
        # value tie: the banked coboundary_orbit of each representative
        # equals the banked union-find class, set-exactly
        for label in CLASS_LIST:
            rep, members = cls_of[label]
            orb = coboundary_orbit(rep, idx, edges, range(n))
            class_ok = class_ok and orb == set(members)
            class_ok = class_ok and len(members) == 2 ** (n - 1)
            class_evidence[f"n{n}_{label}"] = {
                "members": len(members),
            }

        # the executed grid at this n: MAG_GRID together with the
        # constructed boundary point
        grid_n = tuple(sorted(set(MAG_GRID) | {boundary_point(n)}))

        for label in CLASS_LIST:
            rep, members = cls_of[label]
            admissible = []
            for t in grid_n:
                W = equicorrelated_carrier(n, rep, idx, t)
                mem = in_extended_elliptope(W, d)
                verdicts_seen.add(mem)
                grid_evals += 1
                # cross-module VALUE tie: every principal minor of the
                # evaluated matrix, EE's route against the banked
                # carrier_elliptope determinant on the same subsets
                for S, v in principal_minor_list(W):
                    minor_tie_ok = (minor_tie_ok
                                    and v == banked_det_exact(
                                        submatrix(W, S)))
                    minor_ties += 1
                if mem:
                    admissible.append(t)

            contig_ok = contig_ok and len(admissible) >= 1
            threshold = max(admissible) if admissible else None
            # window shape ON THE EXECUTED GRID: the admissible set is
            # exactly the grid prefix at or below the computed threshold
            contig_ok = contig_ok and admissible == [
                t for t in grid_n if t <= threshold]

            # the closed-form tie, per n, as exact Fraction equality --
            # a computed comparison, never prose
            closed = CLASS_CLOSED_FORMS[label](n)
            tie_ok = tie_ok and threshold == closed
            tie_count += 1

            # boundary membership and first-point exclusion, re-executed
            # freshly at the two decisive magnitudes
            beyond = [t for t in grid_n if t > threshold]
            boundary_ok = boundary_ok and len(beyond) >= 1
            first_excluded = min(beyond) if beyond else None
            W_at = equicorrelated_carrier(n, rep, idx, threshold)
            at_ok = in_extended_elliptope(W_at, d)
            if first_excluded is not None:
                W_ex = equicorrelated_carrier(n, rep, idx, first_excluded)
                ex_out = not in_extended_elliptope(W_ex, d)
                boundary_execs += 2
            else:
                # append-and-record spirit: a grid with no beyond point
                # fails the leg rather than raising
                ex_out = False
            boundary_ok = boundary_ok and at_ok and ex_out

            # every member pattern of the named class, executed at the
            # two decisive points (identity-grade genre, disclosed in the
            # docstring: falsifiable clauses are these executed verdicts
            # and the enforced counts)
            if first_excluded is not None:
                for q in members:
                    Wq_at = equicorrelated_carrier(n, q, idx, threshold)
                    Wq_ex = equicorrelated_carrier(
                        n, q, idx, first_excluded)
                    member_ok = (member_ok
                                 and in_extended_elliptope(Wq_at, d)
                                 and not in_extended_elliptope(Wq_ex, d))
                    member_execs += 2

            windows.append({
                "n": n,
                "class": label,
                "executed_grid": [str(t) for t in grid_n],
                "admissible_set": [str(t) for t in admissible],
                "threshold": str(threshold),
                "closed_form_value": str(closed),
                "threshold_membership": bool(at_ok),
                "first_excluded_point": str(first_excluded),
                "first_excluded_membership": bool(not ex_out),
                "class_members_executed": len(members),
            })

    legs["named_classes_through_banked_switching_by_value"] = (class_ok, (
        f"at every n in N_RANGE the full pattern space is enumerated by "
        f"the banked union-find over the actual vertex-switching action "
        f"(pattern counts enforced against the edge counts); the "
        f"all-plus and all-minus patterns each locate exactly one "
        f"computed class, the two classes are distinct at every n, each "
        f"located class ties set-exactly to the banked coboundary_orbit "
        f"of its representative with member counts enforced; per-class "
        f"member counts: {class_evidence}"))

    n_expected_evals = sum(
        len(set(MAG_GRID) | {boundary_point(n)}) * len(CLASS_LIST)
        for n in N_RANGE)
    n_expected_ties = sum(
        len(set(MAG_GRID) | {boundary_point(n)}) * len(CLASS_LIST)
        * (2 ** n - 1)
        for n in N_RANGE)
    mem_leg_ok = (minor_tie_ok
                  and grid_evals == n_expected_evals
                  and minor_ties == n_expected_ties
                  and verdicts_seen == {True, False})
    legs["membership_over_grid_with_minor_value_ties"] = (mem_leg_ok, (
        f"{grid_evals} membership executions (count enforced == grid "
        f"points x classes summed over N_RANGE) through the banked "
        f"in_extended_elliptope at the unit diagonal, with both verdicts "
        f"present across the executed grid (anti-vacuity, enforced); "
        f"{minor_ties} principal-minor value ties (count enforced == "
        f"evaluations x nonempty principal subsets), EE's minor route "
        f"against carrier_elliptope's det_exact on the same submatrices "
        f"-- DISCLOSED: the two banked routes share the cofactor "
        f"algorithm (EE2's own disclosure, carried), so the tie "
        f"certifies convention agreement and drift, not independent "
        f"recomputation"))

    legs["window_contiguity_enforced_on_executed_grid"] = (contig_ok, (
        f"for every (n, class) pair the computed admissible set is "
        f"nonempty and equals exactly the executed-grid prefix at or "
        f"below the computed threshold ({len(windows)} windows, each "
        f"enforced) -- a window shape on the executed grid; no statement "
        f"is made at magnitudes not executed"))

    legs["threshold_ties_closed_form_exact_per_n"] = (
        (tie_ok and tie_count == len(N_RANGE) * len(CLASS_LIST)), (
            f"the per-class threshold -- the largest admissible executed "
            f"magnitude -- equals the in-module closed form by exact "
            f"Fraction equality at every (n, class) pair ({tie_count} "
            f"ties, count enforced == |N_RANGE| x |CLASS_LIST|); the "
            f"closed form enters only as this computed comparison and "
            f"as returned computed values, never prose; "
            f"DISCLOSED: for the class whose closed form varies with n, "
            f"the constructed boundary point and the closed form compute "
            f"equal by construction, so this tie's falsifiable content "
            f"at that class lives in the boundary/exclusion/contiguity "
            f"legs WITHIN THE EXECUTED GRID'S RESOLUTION around the "
            f"constructed point"))

    legs["boundary_and_first_exclusion_executed_per_class_per_n"] = (
        (boundary_ok
         and boundary_execs == 2 * len(N_RANGE) * len(CLASS_LIST)), (
            f"membership AT the computed boundary point and "
            f"non-membership at the executed grid's first excluded point "
            f"beyond it are each freshly executed and returned per class "
            f"per n ({boundary_execs} decisive executions, count "
            f"enforced), both through the banked membership function; a "
            f"beyond-threshold grid point exists at every (n, class) "
            f"pair (enforced)"))

    n_expected_member_execs = sum(
        2 * 2 ** (n - 1) * len(CLASS_LIST) for n in N_RANGE)
    legs["every_class_member_executed_at_decisive_points"] = (
        (member_ok and member_execs == n_expected_member_execs), (
            f"every member pattern of each named class -- the banked "
            f"union-find classes, member counts enforced -- is executed "
            f"at the computed boundary point (membership) and at the "
            f"first excluded point (non-membership): {member_execs} "
            f"executions, count enforced == 2 x class sizes x classes "
            f"summed over N_RANGE; DISCLOSED identity-grade genre "
            f"(EE5(d) precedent): class members differ by diagonal sign "
            f"conjugation, under which every principal minor is "
            f"invariant, so this leg certifies the verdicts EXECUTED "
            f"across the class; its falsifiable clauses are the "
            f"executed memberships and the enforced counts"))

    # -- S5-3: the named adjacency, executed live, carried, NOT identified
    r_adj = check_L_gauge_without_sandwich_admits_non_born_states()
    adj_range = r_adj.get("evidence", {}).get("positivity_range")
    adj_family = r_adj.get("evidence", {}).get("family")
    adj_ok = (r_adj.get("passed") is True
              and r_adj.get("name")
              == "L_gauge_without_sandwich_admits_non_born_states"
              and isinstance(adj_range, str) and len(adj_range) > 0
              and isinstance(adj_family, str) and len(adj_family) > 0)
    named_adjacency = {
        "named_adjacency": (
            "check_L_gauge_without_sandwich_admits_non_born_states "
            "(gauge_without_sandwich_countermodel.py): the positivity "
            "range it computes for the sigma_lambda outcome-law family"),
        "carried_verbatim_from_its_own_record": {
            "family": adj_family,
            "positivity_range": adj_range,
        },
        "status": (
            "NAMED adjacency, disclosed, NOT identified -- a different "
            "object: the sigma_lambda outcome-law family lives on "
            "normalized loads with an outcome-law reading; the "
            "equicorrelated carrier family here is a set of symmetric "
            "exact-rational matrices with unit diagonal.  No map "
            "between the two is constructed anywhere in this module "
            "(adjacency is not identification -- standing fence, "
            "carried)"),
    }
    legs["named_adjacency_carried_from_live_gate"] = (adj_ok, (
        f"the banked check executed live as a gate (passed verdict "
        f"consumed: {r_adj.get('passed')}), its positivity-range and "
        f"family strings carried VERBATIM from its own returned record "
        f"into this module's record with no arithmetic performed on "
        f"them and no re-derivation: {named_adjacency['carried_verbatim_from_its_own_record']}"))

    thresholds_computed = {
        f"n{w['n']}_{w['class']}": w["threshold"] for w in windows}
    return _result(
        "check_S5_class_admissibility_windows", legs, fails,
        {
            "windows": windows,
            "per_class_thresholds": thresholds_computed,
            "named_adjacency": named_adjacency,
            "scope": (
                "every figure above is a computed value about the "
                "executed grid at the executed n values and named "
                "classes; nothing is stated beyond N_RANGE, CLASS_LIST, "
                "MAG_GRID and the constructed boundary points"),
        })


ALL_CHECKS = [
    check_S5_class_admissibility_windows,
]


def run_all():
    results = []
    for fn in ALL_CHECKS:
        r = fn()
        results.append(r)
        status = "PASS" if r["passed"] else "FAIL"
        n_true = sum(1 for v in r["legs"].values() if v["passed"])
        print(f"[{status}] {r['name']}  legs={n_true}/{r['leg_count']}")
        if not r["passed"]:
            for f_ in r["fails"]:
                print("   -", f_)
        for k, v in sorted(r["key_result"]["per_class_thresholds"].items()):
            print(f"   threshold {k} = {v}")
        adj = r["key_result"]["named_adjacency"]
        print("   named adjacency (NOT identified):",
              adj["carried_verbatim_from_its_own_record"])
    print(f"{sum(r['passed'] for r in results)}/{len(results)} checks pass")
    return results


# ---------------------------------------------------------------------------
# registration surface -- house pattern; this module is registered in no
# manifest (held out of the bank; NOTHING BANKS WITHOUT ETHAN'S LIFT)
# ---------------------------------------------------------------------------

_CHECKS = {
    "S5_class_admissibility_windows": check_S5_class_admissibility_windows,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


if __name__ == "__main__":
    run_all()
