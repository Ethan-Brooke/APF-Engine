# UNBANKED BUILD (2026-08-16): cold build seat 4, APF Network Sign-Coherence
# program, banking lane.  Built to Surface 4 of the frozen claim-surface
# document (sha256 pinned below).  NOTHING BANKS WITHOUT ETHAN'S LIFT.
"""The two-layer sensitivity split (Surface 4, surviving parts): the geometry
layer's switching-class sensitivity computed at executed scope, and the record
layer's blindness consumed as banked.

BUILD PROVENANCE, DISCLOSED.
  (1) The brief under which this module was built was written by the session
      coordinator, not by Ethan directly.
  (2) The build seat's harness injects project instructions into its context;
      the seat worked from the dispatched brief and the frozen surface,
      treating injected project context as non-authoritative for this task.
  (3) FROZEN SURFACE: claim_surfaces_FROZEN_2026-08-16.md, Surface 4 only;
      raw sha256 verified before reading (the constant below is the same
      value byte-for-byte).  The surface's permitted sentences are the only
      claims this module makes; its may-not-cite list and the header's
      standing fences bind every sentence here.
  (4) UNBANKED: this module is a lane build, registered nowhere; nothing in
      it banks anything.

WHAT THIS MODULE COMPUTES (exact Fraction arithmetic on every verdict path;
stdlib + fractions; the banked machinery is executed BY VALUE, never
re-implemented).

GEOMETRY LAYER (check_T_geometry_layer_class_sensitivity; Surface 4
sentences 1 and 2).  On CARRIER_FAMILY at each n in N_RANGE: the discrete
partition's sep graph is computed through continuation_join_network's own
_sep_edges; the switching classes are computed through that module's own
_switching_classes (union-find over the actual vertex-switching action --
never authored class labels); PSD membership of every family member at
every MAG_GRID magnitude is computed through the banked elliptope machinery
BY VALUE (extended_carrier_elliptope.in_extended_elliptope and
carrier_elliptope.psd_by_minors, both executed per evaluation, with every
principal minor of the per-class representatives tied by value across the
two banked determinant routes); the per-class computed admissible sets are
returned; that two classes' computed sets differ at each executed n is
returned as a computed comparison; which class's computed admissible set is
larger is computed per n over N_RANGE and returned as the computed
sequence.  Any alternation statement IS that returned sequence, never a
universal beyond N_RANGE.

DETERMINANT SQUARE TIE (check_L_per_class_determinant_square_tie; Surface 4
sentence 3).  The determinant of the exhibited per-class carrier at the
named evaluation point T_EVAL (at DET_EVAL_N) is computed exactly through
the banked determinant routes and compared, as an exact equality, against
the square of a quantity computed in-module from the computed class
holonomy and extended_carrier_elliptope's own certified_sqrt.  The equality
is a polynomial identity of the equicorrelated construction at the executed
n, DISCLOSED as an identity at the leg (the EE3/T5 disclosure genre); its
falsifiable clauses are named at the leg and legged.

RECORD LAYER, CONSUMED (check_L_record_layer_consumed_gated_live; Surface 4
sentence 4).  The record-layer half of the split is consumed as banked and
gated live, never re-derived: check_L_counted_ledger_fixes_only_the_commit_
record_diagonal (counted_ledger_underdetermination), check_L_record_blind_
invisibility (record_partial_dephasing), check_T_full_record_record_blind_
invisibility (record_coherence_tradeoff), and check_L_selection_ledger_
completeness (born_at_ties -- the clause-(c) exhibit's home) are each
EXECUTED, and each is cited at its own grade and scope, read from its own
returned record and tied by value against the authored citation.

SIGN-CONJUGATION INVARIANCE, CONSUMED AND RE-TIED
(check_T_sign_conjugation_consumed_and_retied; Surface 4 sentence 5).  The
geometry layer's sign-conjugation invariance is consumed from
check_T_extended_elliptope_controls (EE5(d)) and check_T_tradeoff_controls
(T5(b)) at their own SCOPED strength, both executed and gated; where this
module needs the invariance on its own fixtures it re-executes the banked
functions (conj_by_signs, principal_minor_list, in_extended_elliptope)
there and returns the computed ties, including an entrywise value tie of
the banked switching action (continuation_join_network.switch_pattern)
against the banked diagonal sign conjugation on this module's carriers.

SURFACE 5 CITATION (Surface 4 sentence 6).  The per-class admissibility
window content -- thresholds, boundary points, closed forms -- is Surface
5's, computed in class_admissibility_windows.py (a sibling seat's module,
cited here by its planned name).  This module cites that module, imports
nothing from it, and computes none of its content beyond sentence 1's set
comparison: the admissible sets returned here are grid subsets, and no
threshold, boundary point, or closed form is computed or returned.

SCOPE BOUNDS, BY NAME: CARRIER_FAMILY (the named signed-carrier fixture
family), N_RANGE (the executed n values), MAG_GRID (the exact rational
magnitude grid) -- named module-level constants below; every sentence is
quantified over these names and nothing larger.  The named evaluation point
T_EVAL and its executed n (DET_EVAL_N), and the re-tie point TIE_POINT, are
likewise named constants.

LEG INVENTORY (D7@2026-08-08, APPEND-AND-RECORD): _result() compares the
executed leg set against EXPECTED_LEGS set-exactly on the result-assembly
path; a mismatch contributes a failure reason and does not raise.
STANDING LIMIT, disclosed: this certifies that a declared leg EXECUTED,
not that it COULD HAVE FAILED; a computed verdict replaced by a constant
escapes it, as it escapes the raising form equally.

STANDING FENCES (the frozen header's, binding here whether or not restated):
"the transfer is forced" is negative and may not be claimed; "the carrier
gap is closed / narrowed" may not be claimed; "Born is derived" without its
conditional clause may not be claimed; the O2 close and the OT3 vacuity
ruling are quotable only whole; ORIENTATION_COVER_REALIZED is uncertified;
the Paper 9 ladder is not banked; record_coherence_tradeoff is never a
supply; the banked join network supplies no sign; adjacency is not
identification.

MAY-NOT-CITE (Surface 4's own list, verbatim, carried as the module
constant MAY_NOT_CITE below and returned in every record).

This module describes what it COMPUTES.
"""

from fractions import Fraction as F
from itertools import product

# Banked machinery, consumed by import and EXECUTED BY VALUE (nothing below
# is re-implemented in this module):
from apf import extended_carrier_elliptope as _ee
from apf import carrier_elliptope as _ce
from apf import continuation_join_network as _cjn
from apf import record_coherence_tradeoff as _rct
from apf import record_partial_dephasing as _pd
from apf import counted_ledger_underdetermination as _clu
from apf import born_at_ties as _bat

HELD_OUT_OF_THE_BANK = False  # BANKED v24.3.478 (2026-08-16); landing rewire disclosed in the manifest

FROZEN_SURFACE_SHA256 = (
    "440ed2162e5d28f83a9addba5ce49c257dbe0646cefe287c7dbe2df7617f743d")

# Surface 4's may-not-cite list, verbatim from the frozen surface:
MAY_NOT_CITE = (
    "the record layer's blindness as THIS module's content (it is banked; "
    "sentence 4 is consumption); Englert visibility or any "
    "quantum-mechanical identification (the tradeoff module's fence, "
    "carried); record_coherence_tradeoff as a supply (standing fence -- it "
    "is consumed here only as the scoped sign-conjugation precedent); any "
    "bank-wide universal (every gauge-blindness consumption is scoped as "
    "its source scopes it); any physical two-layer claim; any favored-class "
    "statement beyond the returned computed sequence; anything for or "
    "against situational-S.")

# The Surface 5 sibling module, cited by planned name; nothing imported.
SURFACE_5_MODULE_CITED = "class_admissibility_windows.py"

# ---------------------------------------------------------------------------
# scope-bound constants (named; every sentence is quantified over these)
# ---------------------------------------------------------------------------

# The named signed-carrier fixture family.  A member is the symmetric matrix
# with unit diagonal (a named authored choice) and off-diagonal entry
# label_e * t at every edge e of the discrete partition's sep graph at n,
# for a +-1 edge-label pattern and a magnitude t.  The edge set is computed
# through the banked _sep_edges; the label patterns are the exhaustive +-1
# patterns the banked union-find enumerates; the switching classes are
# computed through the banked _switching_classes -- never authored.
CARRIER_FAMILY = {
    "name": "signed_unit_diagonal_single_magnitude_on_sep_of_discrete_"
            "partition",
    "diagonal": "all ones (uniform; authored choice, disclosed)",
    "off_diagonal": "label_e * t at every sep edge e; t from MAG_GRID",
    "edge_set": "continuation_join_network._sep_edges of the discrete "
                "partition at each n in N_RANGE (executed by value)",
    "switching_classes": "continuation_join_network._switching_classes "
                         "(union-find over the actual switching action, "
                         "executed by value; never authored class labels)",
}

N_RANGE = (3, 4)

MAG_GRID = (F(0), F(1, 6), F(1, 4), F(1, 3), F(5, 12), F(1, 2),
            F(7, 12), F(2, 3), F(3, 4), F(1))

# The named evaluation point of the determinant leg, and its executed n.
# 1 + 2*T_EVAL and 1 - 2*T_EVAL are both rational squares (certified
# in-leg through EE's own certified_sqrt, never quoted here), so both
# class branches carry an EE-certified exact square root there.
T_EVAL = F(12, 25)
DET_EVAL_N = 3

# The named re-tie point of the sign-conjugation check (a MAG_GRID member;
# membership of both compared classes at it is gated in-leg, not assumed).
TIE_POINT = F(1, 4)

# Authored expectation for the banked union-find's class counts at the
# executed n, compared against the live execution.  DISCLOSED value tie:
# these are J3's banked pins (kn_switching_classes_2_8_64_union_find,
# continuation_join_network) at K3/K4, re-derived here by executing the
# banked union-find rather than quoted; the class <-> character bijection
# is J3's banked content and is not re-stated or re-proved here.
EXPECTED_CLASS_COUNTS = {3: 2, 4: 8}

# Authored citation list for the record-layer gate (sentence 4), compared
# set-exactly against the names the executed records themselves return.
EXPECTED_RECORD_LAYER_NAMES = (
    "L_counted_ledger_fixes_only_the_commit_record_diagonal",
    "check_L_record_blind_invisibility",
    "check_T_full_record_record_blind_invisibility",
    "L_selection_ledger_completeness",
)

EXPECTED_LEGS = {
    "check_T_geometry_layer_class_sensitivity": [
        "banked_switching_classes_computed_and_counts_enforced",
        "larger_set_class_sequence_computed_per_n",
        "membership_both_banked_routes_agree_over_grid",
        "per_class_admissible_sets_two_classes_differ",
        "representative_minors_tied_across_banked_routes",
        "within_class_membership_constant_over_grid",
    ],
    "check_L_per_class_determinant_square_tie": [
        "carriers_gated_members_at_named_point",
        "determinant_tied_across_banked_routes_by_value",
        "nonvacuity_distinct_class_determinants_and_certified_sqrts",
        "square_equality_exact_per_class_identity_disclosed",
    ],
    "check_L_record_layer_consumed_gated_live": [
        "citation_set_exact_consumption_only",
        "clause_c_home_gated_at_reading_grade",
        "counted_ledger_diagonal_fix_gated_at_grade",
        "full_record_invisibility_gated_at_grade_and_scope",
        "record_blind_invisibility_gated_at_grade_and_scope",
    ],
    "check_T_sign_conjugation_consumed_and_retied": [
        "banked_invariance_sources_gated_at_scoped_strength",
        "conjugation_reexecuted_on_own_fixtures_minor_ties",
        "membership_and_diagonal_preserved_on_own_fixtures",
        "nonvacuity_mixed_sign_vector_moves_cells",
        "switching_action_ties_conjugation_entrywise",
    ],
}


# ---------------------------------------------------------------------------
# result plumbing (append-and-record leg inventory, D7@2026-08-08, sited on
# the result-assembly path)
# ---------------------------------------------------------------------------

def _result(name, legs, key_result, disclosures=(), citations=()):
    fails = []
    have = sorted(legs)
    want = EXPECTED_LEGS[name]
    if have != want:
        missing = sorted(set(want) - set(have))
        extra = sorted(set(have) - set(want))
        fails.append(
            "leg inventory mismatch: missing=%r extra=%r" % (missing, extra))
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
        "scope_bounds": {
            "CARRIER_FAMILY": CARRIER_FAMILY["name"],
            "N_RANGE": list(N_RANGE),
            "MAG_GRID": [str(t) for t in MAG_GRID],
            "T_EVAL": str(T_EVAL), "DET_EVAL_N": DET_EVAL_N,
            "TIE_POINT": str(TIE_POINT),
        },
        "citations": list(citations),
        "disclosures": list(disclosures),
        "surface_5_cited_not_computed": SURFACE_5_MODULE_CITED,
        "may_not_cite": MAY_NOT_CITE,
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": FROZEN_SURFACE_SHA256,
        "inventory_note": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


def _no_float(values):
    return all(isinstance(v, F) for v in values)


# ---------------------------------------------------------------------------
# family glue (thin construction only; every decision runs through the
# banked machinery imported above)
# ---------------------------------------------------------------------------

def _ones(n):
    return tuple(F(1) for _ in range(n))


def _carrier(labels, edges, idx, t, n):
    """The CARRIER_FAMILY member at (pattern, t): unit diagonal, entry
    label_e * t at each sep edge."""
    W = [[F(1) if i == j else F(0) for j in range(n)] for i in range(n)]
    for e in edges:
        i, j = e
        v = F(labels[idx[e]]) * t
        W[i][j] = v
        W[j][i] = v
    return W


def _class_data(n):
    """Edges, patterns, index, classes and per-class (min-representative,
    computed holonomy character) at n -- everything through the banked
    machinery by value."""
    E = _cjn._sep_edges([[i] for i in range(n)], n)
    pats, idx, classes = _cjn._switching_classes(E, range(n))
    basis = _cjn._fundamental_cycles(list(range(n)), E)
    reps = []
    for cls in classes:
        rep = min(cls)
        char = _cjn.holonomy_character(rep, idx, basis)
        reps.append((rep, char))
    return E, pats, idx, classes, basis, reps


def _find_class(reps, classes, char):
    """The classes whose computed min-representative character equals
    `char` (located by computed search, never authored)."""
    return [k for k, (_rep, c) in enumerate(reps) if c == char]


# ---------------------------------------------------------------------------
# sentences 1 + 2 -- the geometry layer's class sensitivity, computed
# ---------------------------------------------------------------------------

def check_T_geometry_layer_class_sensitivity():
    """Surface 4 sentences 1 and 2: per-class PSD membership over MAG_GRID
    through the banked elliptope machinery by value; per-class admissible
    sets returned; two classes' sets differ, returned as a computed
    comparison; the larger-set class computed per n and returned as the
    computed sequence."""
    legs = {}

    per_n = {}
    n_eval = 0
    agree_ok = True
    class_count_ok = True
    coverage_ok = True
    for n in N_RANGE:
        E, pats, idx, classes, basis, reps = _class_data(n)
        m = len(E)
        class_count_ok = (class_count_ok
                          and len(classes) == EXPECTED_CLASS_COUNTS[n]
                          and len(pats) == 2 ** m
                          and sum(len(c) for c in classes) == len(pats))
        member_verdicts = []
        for k, cls in enumerate(classes):
            rows = []
            for p in cls:
                row = []
                for t in MAG_GRID:
                    W = _carrier(p, E, idx, t, n)
                    v1 = _ee.in_extended_elliptope(W, _ones(n))
                    v2 = _ce.psd_by_minors(W)
                    agree_ok = agree_ok and (v1 == v2)
                    n_eval += 1
                    row.append(v1)
                rows.append(row)
            member_verdicts.append(rows)
        per_n[n] = (E, idx, classes, reps, member_verdicts, m)
        coverage_ok = coverage_ok and all(
            len(rows) == len(classes[k])
            and all(len(r) == len(MAG_GRID) for r in rows)
            for k, rows in enumerate(member_verdicts))
    expected_eval = sum(
        (2 ** (n * (n - 1) // 2)) * len(MAG_GRID) for n in N_RANGE)
    legs["banked_switching_classes_computed_and_counts_enforced"] = (
        class_count_ok and len(per_n) == len(N_RANGE),
        "at each n in %r the discrete partition's sep graph is computed "
        "through the banked _sep_edges and the switching classes through "
        "the banked _switching_classes (union-find over the actual "
        "switching action); the class counts computed live equal the "
        "authored expectation %r -- DISCLOSED value tie: those pins are "
        "J3's banked kn_switching_classes figures at K3/K4, re-derived by "
        "executing the banked union-find here, not quoted; the class <-> "
        "character bijection is J3's banked content, consumed not "
        "re-proved -- and the enumerated patterns partition exactly into "
        "the classes (pattern and member totals enforced)"
        % (list(N_RANGE), EXPECTED_CLASS_COUNTS))

    legs["membership_both_banked_routes_agree_over_grid"] = (
        agree_ok and n_eval == expected_eval and coverage_ok,
        "PSD membership computed for EVERY family member at EVERY MAG_GRID "
        "magnitude through BOTH banked routes by value -- "
        "extended_carrier_elliptope.in_extended_elliptope at the unit "
        "diagonal and carrier_elliptope.psd_by_minors -- with the two "
        "verdicts equal at every one of the %d evaluations (count enforced "
        "== sum over n of 2^m x grid size = %d); DISCLOSED (the EE2 "
        "precedent): the two banked routes share the all-principal-minors "
        "algorithm genre, so this agreement certifies convention agreement "
        "and drift between the banked modules, not an independent "
        "recomputation; the value content of the cross-route tie lives in "
        "the representative-minors leg below" % (n_eval, expected_eval))

    # value tie on the per-class representatives: every principal minor of
    # every representative carrier at every grid point, this build's calls
    # into EE's det against carrier_elliptope's det_exact on the same
    # submatrix -- BY VALUE, across the two banked modules
    n_minor_ties = 0
    minor_ok = True
    for n in N_RANGE:
        E, idx, classes, reps, _mv, m = per_n[n]
        for (rep, _char) in reps:
            for t in MAG_GRID:
                W = _carrier(rep, E, idx, t, n)
                for S, v in _ee.principal_minor_list(W):
                    minor_ok = minor_ok and (
                        v == _ce.det_exact(_ee.submatrix(W, S)))
                    n_minor_ties += 1
    expected_minor_ties = sum(
        EXPECTED_CLASS_COUNTS[n] * len(MAG_GRID) * (2 ** n - 1)
        for n in N_RANGE)
    legs["representative_minors_tied_across_banked_routes"] = (
        minor_ok and n_minor_ties == expected_minor_ties,
        "every principal minor of every per-class representative carrier "
        "at every grid magnitude is computed through "
        "extended_carrier_elliptope's own det/submatrix and tied BY VALUE "
        "against carrier_elliptope's own det_exact on the same submatrix: "
        "%d minor value ties (count enforced == classes x grid x "
        "(2^n - 1) summed over N_RANGE = %d)"
        % (n_minor_ties, expected_minor_ties))

    # within-class constancy of the membership verdict at every grid point
    # (the banked membership function re-executed on every member of every
    # class -- the sentence-5 re-execution genre applied to membership; the
    # per-class admissible set below is thereby a set of the CLASS, not of
    # a chosen member)
    const_ok = True
    n_const = 0
    for n in N_RANGE:
        _E, _idx, classes, _reps, member_verdicts, _m = per_n[n]
        for rows in member_verdicts:
            for col in range(len(MAG_GRID)):
                vals = {r[col] for r in rows}
                const_ok = const_ok and len(vals) == 1
                n_const += 1
    expected_const = sum(
        EXPECTED_CLASS_COUNTS[n] * len(MAG_GRID) for n in N_RANGE)
    legs["within_class_membership_constant_over_grid"] = (
        const_ok and n_const == expected_const,
        "at every (class, grid point) the membership verdict is constant "
        "across every member of the class (%d constancy checks, count "
        "enforced == classes x grid summed over N_RANGE = %d), each "
        "verdict computed through the banked membership function -- so "
        "the per-class admissible sets below are sets of the CLASS as "
        "computed, not of a chosen member" % (n_const, expected_const))

    # per-class admissible sets; the two compared classes located by
    # computed character; the sets-differ comparison, computed
    admissible = {}
    differ_ok = True
    located_ok = True
    compared = {}
    for n in N_RANGE:
        _E, _idx, classes, reps, member_verdicts, m = per_n[n]
        dim_h1 = m - n + 1
        entries = []
        for k in range(len(classes)):
            adm = [MAG_GRID[col] for col in range(len(MAG_GRID))
                   if member_verdicts[k][0][col]]
            entries.append({"character": [int(c) for c in reps[k][1]],
                            "admissible": [str(t) for t in adm],
                            "size": len(adm)})
        admissible[n] = entries
        triv = _find_class(reps, classes, (1,) * dim_h1)
        allm = _find_class(reps, classes, (-1,) * dim_h1)
        located_ok = located_ok and len(triv) == 1 and len(allm) == 1
        if located_ok:
            kt, kf = triv[0], allm[0]
            set_t = {MAG_GRID[c] for c in range(len(MAG_GRID))
                     if member_verdicts[kt][0][c]}
            set_f = {MAG_GRID[c] for c in range(len(MAG_GRID))
                     if member_verdicts[kf][0][c]}
            compared[n] = (kt, kf, set_t, set_f)
            differ_ok = differ_ok and (set_t != set_f)
    legs["per_class_admissible_sets_two_classes_differ"] = (
        located_ok and differ_ok and len(admissible) == len(N_RANGE)
        and all(len(admissible[n]) == EXPECTED_CLASS_COUNTS[n]
                for n in N_RANGE),
        "the per-class computed admissible sets are returned in this "
        "record's key_result for every class at every n in N_RANGE (entry "
        "counts enforced against the class counts); the two compared "
        "classes are located by COMPUTED character search (the class of "
        "the all-plus-one character and the class of the all-minus-one "
        "character, each found exactly once at each n, enforced), and "
        "their computed sets DIFFER at every executed n -- returned as a "
        "computed comparison: %r"
        % ({n: compared[n][2] != compared[n][3] for n in sorted(compared)}))

    # sentence 2: the larger-set class per n, as the computed sequence
    sequence = []
    larger_ok = located_ok
    for n in N_RANGE:
        if n not in compared:
            larger_ok = False
            continue
        kt, kf, set_t, set_f = compared[n]
        if len(set_t) == len(set_f):
            larger_ok = False
            continue
        larger_k = kt if len(set_t) > len(set_f) else kf
        _E, _idx, classes, reps, _mv, _m = per_n[n]
        entry = {
            "n": n,
            "larger_class_character": [int(c) for c in reps[larger_k][1]],
            "sizes": {"all_plus_character": len(set_t),
                      "all_minus_character": len(set_f)},
        }
        sequence.append(entry)
        # per-entry consistency conjunct: the appended
        # larger_class_character must be the character of the strictly
        # larger size carried in this same entry
        larger_ok = larger_ok and (
            entry["larger_class_character"] == [int(c) for c in reps[
                kt if entry["sizes"]["all_plus_character"]
                > entry["sizes"]["all_minus_character"] else kf][1]])
    legs["larger_set_class_sequence_computed_per_n"] = (
        larger_ok and len(sequence) == len(N_RANGE),
        "which compared class's computed admissible set is larger is "
        "computed per n (strictness enforced) and returned as the computed "
        "sequence of length %d (enforced == len(N_RANGE)); any alternation "
        "statement IS that returned sequence, never a universal beyond "
        "N_RANGE; whether one class is 'favored' is not stated -- the "
        "sequence is the whole content" % len(sequence))

    return _result(
        "check_T_geometry_layer_class_sensitivity", legs,
        key_result={
            "per_class_admissible_sets": {str(n): admissible[n]
                                          for n in N_RANGE},
            "two_classes_differ_per_n": {
                str(n): compared[n][2] != compared[n][3]
                for n in sorted(compared)},
            "larger_set_class_sequence": sequence,
            "membership_evaluations": n_eval,
            "minor_value_ties": n_minor_ties,
        },
        disclosures=[
            "the unit diagonal and the single-magnitude shape of "
            "CARRIER_FAMILY are authored choices, disclosed; the edge "
            "sets, class partitions and characters are computed through "
            "the banked machinery by value",
            "the class-count expectation is a value tie to J3's banked "
            "union-find pins at K3/K4, re-derived by executing the banked "
            "union-find; the class <-> character bijection is J3's banked "
            "content, consumed not re-proved",
            "the two banked membership routes share the "
            "all-principal-minors algorithm genre (EE2 precedent); the "
            "agreement leg certifies convention agreement and drift, and "
            "the representative-minors leg carries the value ties",
            "no threshold, boundary point, or closed form is computed or "
            "returned: the per-class window content is Surface 5's "
            "(class_admissibility_windows.py, a sibling seat), cited and "
            "not computed beyond this check's set comparison",
        ],
        citations=[
            "continuation_join_network (banked): _sep_edges, "
            "_switching_classes, _fundamental_cycles, holonomy_character "
            "-- executed by value",
            "extended_carrier_elliptope (banked): in_extended_elliptope, "
            "principal_minor_list, det, submatrix -- executed by value",
            "carrier_elliptope (banked): psd_by_minors, det_exact -- "
            "executed by value",
        ])


# ---------------------------------------------------------------------------
# sentence 3 -- the per-class determinant square tie at the named point
# ---------------------------------------------------------------------------

def check_L_per_class_determinant_square_tie():
    """Surface 4 sentence 3: the determinant of the exhibited per-class
    carrier at the named evaluation point, computed exactly and compared as
    an exact equality against the square of an in-module computed quantity;
    the equality is a polynomial identity of the construction, DISCLOSED as
    such, with its falsifiable clauses named and legged."""
    legs = {}
    n = DET_EVAL_N
    E, pats, idx, classes, basis, reps = _class_data(n)
    dim_h1 = len(E) - n + 1
    triv = _find_class(reps, classes, (1,) * dim_h1)
    allm = _find_class(reps, classes, (-1,) * dim_h1)
    located = len(triv) == 1 and len(allm) == 1

    rows = []
    gate_ok = located
    for k in (triv + allm) if located else []:
        rep, char = reps[k]
        W = _carrier(rep, E, idx, T_EVAL, n)
        member = _ee.in_extended_elliptope(W, _ones(n))
        diag_ok = _ee.diag_of(W) == _ones(n)
        gate_ok = gate_ok and member and diag_ok
        rows.append((k, rep, char, W))
    legs["carriers_gated_members_at_named_point"] = (
        gate_ok and len(rows) == 2,
        "the two exhibited per-class carriers (the computed "
        "min-representatives of the two computed-character classes at "
        "n = %d) are each gated at the named evaluation point T_EVAL = %s: "
        "unit diagonal computed through the banked diag_of, membership "
        "computed through the banked in_extended_elliptope -- %d carriers "
        "gated (enforced)" % (n, T_EVAL, len(rows)))

    det_vals = {}
    tie_ok = gate_ok
    for (k, rep, char, W) in rows:
        d1 = _ee.det(W)
        d2 = _ce.det_exact(W)
        tie_ok = tie_ok and d1 == d2 and _no_float([d1, d2])
        det_vals[k] = d1
    legs["determinant_tied_across_banked_routes_by_value"] = (
        tie_ok and len(det_vals) == 2,
        "each exhibited carrier's determinant at T_EVAL is computed "
        "through extended_carrier_elliptope's own det AND through "
        "carrier_elliptope's own det_exact on the same matrix, tied by "
        "value (%d ties, enforced); computed values %r"
        % (len(det_vals), {str(k): str(v) for k, v in det_vals.items()}))

    # the in-module quantity: q = (1 - h*t) * certified_sqrt(1 + 2*h*t),
    # with h the COMPUTED class holonomy (the single fundamental-cycle
    # character at this n) and the sqrt EE's own certified route
    q_vals = {}
    sq_ok = gate_ok
    sqrt_ok = gate_ok
    for (k, rep, char, W) in rows:
        h = F(char[0])
        s = _ee.certified_sqrt(1 + 2 * h * T_EVAL)
        sqrt_ok = (sqrt_ok and s is not None and s >= 0
                   and s * s == 1 + 2 * h * T_EVAL)
        if s is None:
            continue
        q = (1 - h * T_EVAL) * s
        q_vals[k] = q
        sq_ok = sq_ok and det_vals[k] == q * q and _no_float([q])
    legs["square_equality_exact_per_class_identity_disclosed"] = (
        sq_ok and sqrt_ok and len(q_vals) == 2,
        "per class, the carrier determinant at T_EVAL equals EXACTLY the "
        "square of the in-module quantity q = (1 - h*t) * "
        "certified_sqrt(1 + 2*h*t), h the COMPUTED class holonomy and the "
        "sqrt EE's own certified route (re-squaring enforced in-leg): "
        "%d exact square equalities (enforced).  DISCLOSED IDENTITY "
        "(EE3/T5 genre): det = (1 - h t)^2 (1 + 2 h t) is a polynomial "
        "identity of the unit-diagonal equicorrelated construction at "
        "n = %d, so the equality cannot fail while both sides implement "
        "that construction; the FALSIFIABLE clauses of this leg, named: "
        "(i) EE's certified_sqrt exists and re-squares exactly at T_EVAL "
        "on BOTH branches (it fails at any t where 1 + 2ht is not a "
        "rational square), (ii) the determinant is computed through EE's "
        "det and tied by value to carrier_elliptope's det_exact in the "
        "sibling leg (drift between the banked routes reddens it), "
        "(iii) the membership and diagonal gates, (iv) the non-vacuity "
        "leg below" % (len(q_vals), n))

    kt = triv[0] if located else None
    kf = allm[0] if located else None
    nonvac = (located and kt in det_vals and kf in det_vals
              and det_vals[kt] != det_vals[kf]
              and kt in q_vals and kf in q_vals
              and q_vals[kt] != q_vals[kf]
              and rows[0][2] != rows[1][2])
    legs["nonvacuity_distinct_class_determinants_and_certified_sqrts"] = (
        nonvac,
        "non-vacuity, computed: the two classes' computed characters "
        "differ, their carrier determinants at T_EVAL differ (%r), and "
        "their in-module quantities differ (%r) -- the square tie reads "
        "two genuinely distinct per-class values, not one value twice"
        % ({str(k): str(v) for k, v in det_vals.items()},
           {str(k): str(v) for k, v in q_vals.items()}))

    return _result(
        "check_L_per_class_determinant_square_tie", legs,
        key_result={
            "named_evaluation_point": str(T_EVAL),
            "executed_n": n,
            "per_class": [
                {"character": [int(c) for c in char],
                 "determinant": str(det_vals.get(k)),
                 "in_module_quantity": str(q_vals.get(k))}
                for (k, rep, char, W) in rows],
        },
        disclosures=[
            "the square equality is a construction identity, disclosed at "
            "the leg with its falsifiable clauses named (the EE3/T5 "
            "disclosure genre)",
            "T_EVAL is an authored named constant, chosen so both class "
            "branches carry an EE-certified exact square root; the choice "
            "is disclosed as authored and the certification is executed, "
            "not assumed",
            "no threshold or window content is computed here: T_EVAL "
            "membership is gated through the banked machinery, and the "
            "window itself is Surface 5's (class_admissibility_windows.py)",
        ],
        citations=[
            "extended_carrier_elliptope (banked): det, diag_of, "
            "certified_sqrt, in_extended_elliptope -- executed by value",
            "carrier_elliptope (banked): det_exact -- executed by value",
            "continuation_join_network (banked): the class machinery, as "
            "in the geometry check",
        ])


# ---------------------------------------------------------------------------
# sentence 4 -- the record layer, consumed as banked and gated live
# ---------------------------------------------------------------------------

# INHERITED RED (E1@2026-08-28: sub-lemma L_cost_C1 of check_L_cost
# demoted off 'P' to a POSTULATE).  THIS CHECK HOLDS NO VIEW ABOUT
# L_cost_C1: it reddens because its proximate anchor reddened, and that
# anchor is check_L_selection_ledger_completeness (born_at_ties.py).
# The leg that reads C1's status literal is in
# check_L_selection_ledger_completeness (born_at_ties.py); this red is
# inherited from it, and a reader who counts it as a separate finding
# over-counts the corpus's damage.
# NOT to be widened, tuned green, or reverted: the predicate is
# satisfiable and clears when C1 is discharged or the anchor's
# predicate is ruled.
def check_L_record_layer_consumed_gated_live():
    """Surface 4 sentence 4: the record-layer half of the split is consumed
    as banked, never re-derived; the four banked checks are executed live
    and cited at their own grades and scopes, each grade and scope READ
    from the executed record and tied against the authored citation."""
    legs = {}

    r_clu = _clu.check_L_counted_ledger_fixes_only_the_commit_record_diagonal()
    r_pd = _pd.check_L_record_blind_invisibility()
    r_rct = _rct.check_T_full_record_record_blind_invisibility()
    r_bat = _bat.check_L_selection_ledger_completeness()

    ok = (r_clu.get("passed") is True and not r_clu.get("fail_reasons")
          and r_clu.get("epistemic", "").startswith("P_math")
          and r_clu.get("tier") == 3
          and len(r_clu.get("conditional_on", [])) > 0
          and len(r_clu.get("forbidden_premises", [])) > 0)
    legs["counted_ledger_diagonal_fix_gated_at_grade"] = (ok, (
        "check_L_counted_ledger_fixes_only_the_commit_record_diagonal "
        "EXECUTED live and passing, cited at its own grade (record "
        "epistemic %r, tier %r, read from the executed record) and at its "
        "own scope: its record carries %d named conditional clauses and "
        "%d forbidden premises, both consumed as that module states them; "
        "its content -- the commit-record read fixes exactly the diagonal "
        "of the operator -- is BANKED content consumed here, not this "
        "module's"
        % (r_clu.get("epistemic"), r_clu.get("tier"),
           len(r_clu.get("conditional_on", [])),
           len(r_clu.get("forbidden_premises", [])))))

    ok = (r_pd.get("passed") is True and not r_pd.get("fail_reasons")
          and r_pd.get("epistemic_tag") == "[P_math]"
          and r_pd.get("tier") == 3
          and "scoped to this index-set model" in r_pd.get("key_result", "")
          and len(r_pd.get("may_not_cite", [])) > 0)
    legs["record_blind_invisibility_gated_at_grade_and_scope"] = (ok, (
        "check_L_record_blind_invisibility EXECUTED live and passing, "
        "cited at its own grade (epistemic tag %r, tier %r, read from the "
        "executed record) and its own scope (its key_result states the "
        "discharge is scoped to its index-set model -- substring tie "
        "enforced against the executed record); its may-not-cite list (%d "
        "clauses) is carried as that module states it"
        % (r_pd.get("epistemic_tag"), r_pd.get("tier"),
           len(r_pd.get("may_not_cite", [])))))

    ok = (r_rct.get("passed") is True and not r_rct.get("fail_reasons")
          and r_rct.get("epistemic") == "P_math"
          and r_rct.get("tier") == 3
          and "banked SR/PD/EE model" in r_rct.get("genre_note", "")
          and len(r_rct.get("may_not_cite", [])) > 0)
    legs["full_record_invisibility_gated_at_grade_and_scope"] = (ok, (
        "check_T_full_record_record_blind_invisibility EXECUTED live and "
        "passing, cited at its own grade (epistemic %r, tier %r) and its "
        "own scope (its genre_note states every sentence is about the "
        "banked SR/PD/EE model -- substring tie enforced against the "
        "executed record); its may-not-cite list (%d clauses, including "
        "the Englert/visibility bar) is carried as that module states it; "
        "record_coherence_tradeoff is consumed here as a citation target "
        "and, in the sign-conjugation check, as the scoped precedent -- "
        "never as a supply (standing fence, carried)"
        % (r_rct.get("epistemic"), r_rct.get("tier"),
           len(r_rct.get("may_not_cite", [])))))

    readings = r_bat.get("artifacts", {}).get("readings", {})
    ok = (r_bat.get("passed") is True and not r_bat.get("fail_reasons")
          and r_bat.get("epistemic") == "P_structural_reading"
          and r_bat.get("tier") == 4
          and "R-sel-LC" in readings and "R-event-model" in readings
          and "RECORDED NOT COUNTED" in readings.get("R-event-model", ""))
    legs["clause_c_home_gated_at_reading_grade"] = (ok, (
        "check_L_selection_ledger_completeness (born_at_ties) -- the "
        "clause-(c) exhibit's home (the sign-twist exhibit: phases are "
        "not counted and cannot carry a bias into the record) -- EXECUTED "
        "live and passing, cited at its own grade (%r, tier %r, read from "
        "the executed record) UNDER ITS TWO NAMED READINGS (both present "
        "in the executed record's artifacts, enforced), with the "
        "R-event-model reading's sign-class field carried exactly as that "
        "record states it: RECORDED NOT COUNTED, consumed by nothing "
        "(substring tie enforced against the executed record)"
        % (r_bat.get("epistemic"), r_bat.get("tier"))))

    got_names = tuple(r.get("name") for r in (r_clu, r_pd, r_rct, r_bat))
    ok = (got_names == EXPECTED_RECORD_LAYER_NAMES
          and len(set(got_names)) == 4)
    legs["citation_set_exact_consumption_only"] = (ok, (
        "the four executed records' own returned names tie the authored "
        "citation list set-exactly and in order (%d records, all "
        "distinct, enforced): the record-layer half of the split is "
        "CONSUMED as banked -- nothing of it is re-derived, re-stated, or "
        "re-graded in this module, and the record layer's blindness is "
        "those modules' content, not this module's (Surface 4's "
        "may-not-cite, carried)" % len(got_names)))

    return _result(
        "check_L_record_layer_consumed_gated_live", legs,
        key_result={
            "consumed": [
                {"name": r.get("name"),
                 "grade": r.get("epistemic", r.get("epistemic_tag")),
                 "tier": r.get("tier"),
                 "passed": bool(r.get("passed"))}
                for r in (r_clu, r_pd, r_rct, r_bat)],
            "consumption_note": (
                "gated live, cited at their own grades and scopes; "
                "nothing re-derived"),
        },
        disclosures=[
            "this check's own computation is the gate execution and the "
            "grade/scope value ties; the cited content is banked and "
            "carries its own grades -- in particular the clause-(c) home "
            "is [P_structural_reading] under its two named readings, and "
            "is consumed at exactly that strength",
            "no physical two-layer claim is made anywhere in this module; "
            "the 'two layers' are the computed geometry-layer sensitivity "
            "(this module's checks 1-2) and the banked record-layer "
            "results consumed here",
        ],
        citations=[
            "counted_ledger_underdetermination.check_L_counted_ledger_"
            "fixes_only_the_commit_record_diagonal (banked)",
            "record_partial_dephasing.check_L_record_blind_invisibility "
            "(banked)",
            "record_coherence_tradeoff.check_T_full_record_record_blind_"
            "invisibility (banked)",
            "born_at_ties.check_L_selection_ledger_completeness (banked; "
            "[P_structural_reading | R-sel-LC + R-event-model])",
        ])


# ---------------------------------------------------------------------------
# sentence 5 -- sign-conjugation invariance, consumed and re-tied
# ---------------------------------------------------------------------------

def check_T_sign_conjugation_consumed_and_retied():
    """Surface 4 sentence 5: the geometry layer's sign-conjugation
    invariance consumed from check_T_extended_elliptope_controls and
    check_T_tradeoff_controls at their own SCOPED strength; re-executed on
    this module's own fixtures through the banked functions, with the
    computed ties returned."""
    legs = {}

    r_ee = _ee.check_T_extended_elliptope_controls()
    r_t5 = _rct.check_T_tradeoff_controls()
    ee_leg = r_ee.get("legs", {}).get(
        "offdiagonal_signs_enter_only_as_fiber_coordinates")
    t5_leg = r_t5.get("legs", {}).get(
        "fiber_sign_membership_preserved_minors_tied_scoped", {})
    ok = (r_ee.get("passed") is True and ee_leg is True
          and r_ee.get("epistemic") == "P_math"
          and r_t5.get("passed") is True
          and t5_leg.get("passed") is True
          and "scoped to these banked" in t5_leg.get("evidence", ""))
    legs["banked_invariance_sources_gated_at_scoped_strength"] = (ok, (
        "both banked sources EXECUTED live and passing: "
        "check_T_extended_elliptope_controls (EE5(d), leg read True from "
        "the executed record, grade %r) and check_T_tradeoff_controls "
        "(T5(b), leg read passing from the executed record, its evidence "
        "stating its own scope -- substring tie enforced); the invariance "
        "is consumed AT THAT SCOPED STRENGTH: each source scopes it to "
        "its own objects, and no bank-wide gauge-blindness universal is "
        "stated or used here (Surface 4's may-not-cite, carried)"
        % r_ee.get("epistemic")))

    # re-execution on this module's own fixtures: the two compared-class
    # representative carriers at TIE_POINT, at each n in N_RANGE
    fixtures = []
    gate_ok = True
    for n in N_RANGE:
        E, pats, idx, classes, basis, reps = _class_data(n)
        dim_h1 = len(E) - n + 1
        for char_want in ((1,) * dim_h1, (-1,) * dim_h1):
            ks = _find_class(reps, classes, char_want)
            gate_ok = gate_ok and len(ks) == 1
            if len(ks) != 1:
                continue
            rep, char = reps[ks[0]]
            W = _carrier(rep, E, idx, TIE_POINT, n)
            gate_ok = gate_ok and _ee.in_extended_elliptope(W, _ones(n))
            fixtures.append((n, E, idx, rep, char, W))

    n_tie = 0
    n_mem = 0
    inv_ok = gate_ok and len(fixtures) == 2 * len(N_RANGE)
    mem_ok = inv_ok
    for (n, E, idx, rep, char, W) in fixtures:
        base = _ee.principal_minor_list(W)
        for sigma in product((F(1), F(-1)), repeat=n):
            WC = _ee.conj_by_signs(W, sigma)
            mem_ok = (mem_ok
                      and _ee.diag_of(WC) == _ee.diag_of(W)
                      and _ee.in_extended_elliptope(WC, _ones(n)))
            n_mem += 1
            for (S1, v1), (S2, v2) in zip(base,
                                          _ee.principal_minor_list(WC)):
                inv_ok = inv_ok and S1 == S2 and v1 == v2
                n_tie += 1
    expected_mem = sum(2 * 2 ** n for n in N_RANGE)
    expected_tie = sum(2 * 2 ** n * (2 ** n - 1) for n in N_RANGE)
    legs["conjugation_reexecuted_on_own_fixtures_minor_ties"] = (
        inv_ok and n_tie == expected_tie,
        "on this module's own fixtures (the two compared-class "
        "representative carriers at TIE_POINT = %s, at each n in N_RANGE; "
        "membership at the fixture point gated through the banked "
        "function), EVERY diagonal sign conjugation is re-executed "
        "through EE's own conj_by_signs and every principal minor is tied "
        "by value through EE's own principal_minor_list against the base "
        "carrier: %d minor value ties (count enforced == fixtures x 2^n x "
        "(2^n - 1) = %d).  DISCLOSED IDENTITY (the EE5/T5 precedent, "
        "carried): the minor equality is an exercised identity -- the "
        "sign factors square out of every principal minor -- so this tie "
        "certifies that the banked route EXECUTES sign-blind on these "
        "fixtures; its falsifiable clauses are the diagonal preservation "
        "and membership legs and the non-vacuity leg below"
        % (TIE_POINT, n_tie, expected_tie))

    legs["membership_and_diagonal_preserved_on_own_fixtures"] = (
        mem_ok and n_mem == expected_mem,
        "under every conjugation of every fixture the diagonal is "
        "preserved (computed through EE's own diag_of) and membership is "
        "preserved (computed through EE's own in_extended_elliptope): %d "
        "conjugated memberships (count enforced == fixtures x 2^n = %d)"
        % (n_mem, expected_mem))

    # the banked switching action ties the banked conjugation, entrywise,
    # on this module's carriers: switching at vertex v then building the
    # carrier equals conjugating the built carrier by the vertex sign
    # vector -- a cross-machinery VALUE tie (join-network machinery vs
    # elliptope machinery), computed on every fixture and every vertex
    n_sw = 0
    sw_ok = gate_ok
    for (n, E, idx, rep, char, W) in fixtures:
        for v in range(n):
            switched = _cjn.switch_pattern(rep, idx, E, v)
            W_sw = _carrier(switched, E, idx, TIE_POINT, n)
            sigma_v = tuple(F(-1) if i == v else F(1) for i in range(n))
            WC = _ee.conj_by_signs(W, sigma_v)
            sw_ok = sw_ok and all(
                W_sw[i][j] == WC[i][j]
                for i in range(n) for j in range(n))
            n_sw += 1
    expected_sw = sum(2 * n for n in N_RANGE)
    legs["switching_action_ties_conjugation_entrywise"] = (
        sw_ok and n_sw == expected_sw,
        "the banked switching action (continuation_join_network's own "
        "switch_pattern) and the banked diagonal sign conjugation (EE's "
        "own conj_by_signs) are tied ENTRYWISE on this module's carriers: "
        "for every fixture and every vertex, the carrier of the switched "
        "pattern equals the conjugated carrier entry-for-entry (%d "
        "vertex ties, count enforced == fixtures x n = %d); disclosed as "
        "a tie, never an identification of the two banked modules' "
        "objects, and stated for the executed single-vertex switchings "
        "only"
        % (n_sw, expected_sw))

    nonvac_moves = 0
    nonvac_ok = gate_ok
    for (n, E, idx, rep, char, W) in fixtures:
        sig_mix = tuple(F(-1) if i == 0 else F(1) for i in range(n))
        WC = _ee.conj_by_signs(W, sig_mix)
        moved = [(i, j) for i in range(n) for j in range(n)
                 if sig_mix[i] * sig_mix[j] == F(-1) and W[i][j] != F(0)]
        nonvac_ok = (nonvac_ok and len(moved) >= 1
                     and all(WC[i][j] == sig_mix[i] * sig_mix[j] * W[i][j]
                             for i in range(n) for j in range(n))
                     and all(WC[i][j] != W[i][j] for (i, j) in moved))
        nonvac_moves += len(moved)
    legs["nonvacuity_mixed_sign_vector_moves_cells"] = (
        nonvac_ok and nonvac_moves > 0,
        "non-vacuity, computed on every fixture: a mixed sign vector "
        "moves at least one nonzero off-diagonal cell (in total %d moved "
        "cells across the fixtures, enforced nonzero), every conjugated "
        "entry equals its predicted sigma_i sigma_j multiple by value, "
        "and every moved cell genuinely changes -- the conjugation is a "
        "real map on these fixtures, not a no-op" % nonvac_moves)

    return _result(
        "check_T_sign_conjugation_consumed_and_retied", legs,
        key_result={
            "sources": [
                {"name": r_ee.get("name"),
                 "grade": r_ee.get("epistemic"),
                 "passed": bool(r_ee.get("passed"))},
                {"name": r_t5.get("name"),
                 "grade": r_t5.get("epistemic"),
                 "passed": bool(r_t5.get("passed"))}],
            "fixture_count": len(fixtures),
            "minor_value_ties": n_tie,
            "switching_conjugation_entry_ties": n_sw,
        },
        disclosures=[
            "the invariance is consumed at each source's own scoped "
            "strength; this check's re-execution extends it to this "
            "module's fixtures by computation, and to nothing else",
            "the minor-tie clause is a disclosed exercised identity (the "
            "EE5/T5 precedent); diagonal preservation, membership "
            "execution, the entrywise switching tie, and non-vacuity are "
            "its falsifiable clauses",
            "record_coherence_tradeoff enters this check only as the "
            "scoped sign-conjugation precedent (its T5(b) leg), never as "
            "a supply (standing fence, carried)",
        ],
        citations=[
            "extended_carrier_elliptope.check_T_extended_elliptope_"
            "controls (banked), EE5(d), at its own scope",
            "record_coherence_tradeoff.check_T_tradeoff_controls "
            "(banked), T5(b), at its own scope",
        ])


# ---------------------------------------------------------------------------
# module surface -- NO registration (unbanked lane build; nothing banks
# without Ethan's lift)
# ---------------------------------------------------------------------------

ALL_CHECKS = [
    check_T_geometry_layer_class_sensitivity,
    check_L_per_class_determinant_square_tie,
    check_L_record_layer_consumed_gated_live,
    check_T_sign_conjugation_consumed_and_retied,
]


_CHECKS = {fn.__name__: fn for fn in ALL_CHECKS}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    results = []
    for fn in ALL_CHECKS:
        r = fn()
        results.append(r)
        status = "PASS" if r["passed"] else "FAIL"
        print("[%s] %s  legs=%d" % (status, r["name"], r["leg_count"]))
        for reason in r["fail_reasons"]:
            print("   -", reason)
    print("%d/%d checks pass" % (sum(r["passed"] for r in results),
                                 len(results)))
    return results


if __name__ == "__main__":
    import sys
    _rs = run_all()
    sys.exit(0 if all(r["passed"] for r in _rs) else 1)
