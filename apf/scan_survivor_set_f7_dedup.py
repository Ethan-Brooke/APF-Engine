"""The fermion-scan survivor set, and the two F7 dedup readings.

A computed pin on the seven-filter survivor set over the template
universe that gauge.py's own Phase-1 loop enumerates, plus the
per-CPT-class agreement between the scan's stateful first-seen dedup
and the pure canonical-representative predicate -- the substitution the
companion-repo standalone relies on and states nowhere.

BANKED at v24.3.480 (2026-08-28).  Built to the FROZEN claim surface:

    Artifacts_2026-08-28_session/build_freeze/CLAIM_SURFACE_FROZEN_2026-08-28.md
    raw sha256:
    5f72fd9a90f40cb4188f1019fce1d21ff42cf9773885108f4f4b23383e4f2465

This module registers one check under the bare-name key per
D6@2026-08-03; `HELD_OUT_OF_THE_BANK` is False and `register()` is live.
`EXPECTED_REGISTRY_SIZE` lives in apf/_module_manifest.py and is NOT
touched by this file; the module is counted there.  WHAT LIFTED THE
HOLD: three blinded cold audits by seats that did not write it, all
LAND-WITH-FIXES (0.86, 0.82, 0.85), two cold fix passes carrying their
findings, and a subtractive pass.

WHAT THIS MODULE COMPUTES.  Exact integer and Fraction arithmetic on
every verdict path; no float enters a comparison.

  (1) The template universe.  gauge.py's own Phase-1 statements -- its
      `_SU3` / `_SU2` tables, its `_af` / `_ch` / `_s3` / `_wi` / `_an`
      / `_ck` helpers and its enumeration loop -- are executed VERBATIM
      out of `check_T_field`'s own source, and the ordered and
      deduplicated counts they produce are compared BY VALUE against
      this module's own `combinations_with_replacement` enumeration.

  (2) Seven filter predicate sets over that universe, each population
      asserted set-exactly against a declared table.

  (3) The intersection of the seven, under the TOTAL spectator-reduction
      variant of F6.  The surviving templates are pinned as a declared
      SET, not as a count, with their DOF multiset and the uniqueness of
      the minimum-DOF member computed as separate channels.

  (4) The two F7 readings -- the scan's stateful first-seen dedup and
      the pure canonical-representative predicate -- compared per CPT
      class, on the full universe AND on the filtered stream.  BOTH
      agreements are FORCED by a computed conjugation closure -- of the
      universe and of the stream respectively -- and this module
      declares that rather than reporting either as a result (see THE
      STANDING LIMITS, item 1).

  (5) Executed controls, in-module: three F6 mutants, a one-sided
      anomaly filter, a DOF-functional edit, and an order-permutation
      sweep run over every one of them and over seven pseudo-random
      subsets carrying no physics.

THE STANDING LIMITS.

  1. THE FULL-UNIVERSE HALF OF THE F7 AGREEMENT IS TRUE BY
     CONSTRUCTION, AND THIS MODULE SAYS SO RATHER THAN REPORTING IT AS
     A RESULT.  The universe is closed under SU(3) conjugation (computed
     set-exactly here) and the canonical representative is a MINIMUM
     over a one- or two-element orbit, so at most one member of any
     class can satisfy `sorted(t) == canonical(t)`, and a first-seen
     dedup keeps exactly one by definition.  Over the full universe the
     two readings therefore agree for reasons that have nothing to do
     with the filters.  THE FILTERED-STREAM HALF IS FORCED TOO, BY THE
     SAME MECHANISM.  The F1-F6 stream is computed closed under SU(3)
     conjugation (leg
     `f7_stream_conjugation_closure_computed_set_exact`); given that
     closure, `f7_filtered_stream_agreement_computed` and
     `rt6_intersection_matches_the_stateful_pipeline_output` both
     follow: a closed stream retains exactly one member per class under
     any consistent choice.  THE ONE COMPUTED FACT BEHIND THE HEADLINE
     EQUIVALENCE IS THE CLOSURE; the other two legs restate it on their
     own domains.  THIS FORCING IS A DISCLOSURE, NOT A COMPUTATION: no
     leg here computes it.  The executed one-sided control breaks the
     CLOSURE, and the agreement fails with it.

  2. THE FILTERED-STREAM LEG'S FAILURE CHANNEL IS NON-CONJUGATION-
     CLOSURE OF THE STREAM, NOT THE REPRESENTATIVE CONVENTION.
     Measured: a coordinated minimum-to-maximum edit of the canonical
     representative leaves the per-class agreement standing, because a
     conjugation-closed stream retains exactly one member per class
     under ANY consistent choice.  That edit is caught HERE, but by the
     cross-module CPT tie against gauge.py's own `_ck`, not by the
     agreement leg.  Stated so that no reader takes the agreement leg
     for a test of the convention.

  3. THE F6 USED HERE IS NOT gauge.py's F6.  This module's F6 is the
     spectator-reduction variant the standalone's order sweep uses.
     gauge.py's Phase-1 `_an` is the uniform-dimension variant.  The two
     are INCOMPARABLE over the universe (computed: neither contains the
     other), so the four-member survivor set pinned here is NOT
     gauge.py's Phase-1 output and must not be read as it.  A tie to
     gauge's `_an` IS carried, against the standalone's own
     transcription of it.

  4. NO SIBLING SUPPLIES THE SPECTATOR-REDUCTION PREDICATE.  Its
     definition is transcribed from the companion-repo standalone, which
     is not importable from this repository.  There is no cross-module
     value tie for F6.

  5. THE gauge.py TIE IS BY SOURCE EXTRACTION, BECAUSE gauge.py EXPOSES
     NO MODULE-LEVEL API FOR ANY OF IT.  `_SU3`, `_cr`, `_af` and the
     Phase-1 loop are all local to `check_T_field`.  This module parses
     that function's own source and executes the selected statements
     verbatim.  If `check_T_field` is restructured so the statements
     cannot be located, every leg FAILS with the reason; there is no
     fallback to a private copy.

  6. THE ORDER SWEEP IS A CONTROL, NOT A RESULT, AND ITS LEG IS
     UNFALSIFIABLE ON PURPOSE.  Every clause of
     `controls_order_sweep_is_satisfied_by_every_variant_executed` is
     forced: set intersection is commutative and associative whatever
     the sets are, and the ordering count is 7! whatever the sets are.
     The leg is here to EXHIBIT that.  A SECOND LEG IS UNFALSIFIABLE
     UNDER DATA AND IS NAMED HERE FOR THE SAME REASON:
     `declared_barred_tokens_absent_from_name_key_result_and_summary`
     scans three surfaces that interpolate only computed integers and
     lists of integers, so no assignment of the underlying data can put
     a barred token in them.  It is a SOURCE guard -- falsifiable by an
     edit to the returned prose, which is what it is for, and by
     nothing else.

  7. THE LEG INVENTORY IS APPEND-AND-RECORD (D7@2026-08-08).  A
     mismatch contributes a failure reason and does not raise: it
     certifies that a declared leg EXECUTED, not that it COULD HAVE
     FAILED.

  8. MUTATIONS THAT ESCAPE THE BATTERY THIS SEAT RAN.

     (a) Replacing the survivor-set leg's COMPUTED set with the declared
         inventory neuters that one leg and nothing else reddens.  The
         composed edits (that neuter PLUS a real filter change) are both
         caught, by the population leg and the F6-mutant control.  A
         filter change that moved the survivor set while preserving its
         DOF multiset, its CPT classes and every filter population is
         not exhibited here and is not claimed impossible.

     (b) Sourcing the universe from this module's own enumeration
         instead of gauge.py's harvested one changes nothing observable,
         because the two sets are computed EQUAL.  That much is an
         invariance rather than a blind spot.

     Under a COORDINATED cross-file edit, with gauge.py's own `_ck`
     moved to `max` as well, the `_ck` tie does NOT catch it, because
     both sides move together; the convention is held there by the other
     two legs.

  9. TWO CLAUSE-LEVEL FORCED ITEMS, NAMED RATHER THAN DROPPED.  In
     `controls_f6_mutants_move_the_survivor_set` the constant-false
     row's `survivors == 0` and its `moved_the_survivor_set` are both
     forced -- an intersection with the empty set is empty, and an empty
     set differs from a non-empty pinned one.  The leg is falsifiable as
     a whole -- the battery reddens it -- so this is a clause-level note
     and not a dead leg.  WHAT REMAINS OF THE DOF-FUNCTIONAL CONTROL IS
     ONE INEQUALITY, AND ITS NAME PROMISES MORE THAN IT COMPUTES:
     `controls_dof_functional_edit_moves_multiset_not_survivor_set`
     computes only that the mutated DOF multiset differs from the
     declared one.  It does not re-run the pipeline, so the survivor
     set's behaviour under the edit is asserted by the leg's NAME and
     computed by no clause of it.  Measured: no data mutation aimed at
     this module moved this leg, including the DOF functional's own
     product-to-sum edit, which reddens four OTHER legs and not this
     one.  The edit that does move it is one to the control's own mutant
     functional; an edit to its declared comparand would move it too,
     and no claim is made that those are the only two ways.

 10. PLACING THIS FILE UNDER apf/ REDDENS A DRIFT NET, AND THAT
     LANDING OBLIGATION IS DISCHARGED ELSEWHERE, NOT HERE.  Measured:
     with the file copied to `apf/` in an otherwise clean tree and no
     map entry, `T_config_demand_register_split_bank_respected` raises
     `clause (b): no new net-matching file outside the disposition
     map`.  The file name matches the tier-0 net.  The entry was
     written at landing, in `apf/gravity.py`'s disposition map
     (`'scan_survivor_set_f7_dedup.py': ('L', 'fence')`); nothing in
     this file writes it.

     A SECOND LANDING OBLIGATION, DISCHARGED.  The sub-grade was ruled
     at landing: the module-level `GRADE` and the returned `epistemic`
     field both read `P_structural_exhaustive`, not the bare
     `P_structural`.  The corpus's own guard for the bare form --
     `check_no_bare_pstructural.py`, which asserts that a
     structural-meta mark carries one of the sub-grades -- could not
     have seen this module either way: the guard matches a string
     LITERAL at the `epistemic=` site and this module's grade is behind
     a name.  Measured: the guard's output is byte-identical with and
     without this file under `apf/`.  It is also ALREADY RED at HEAD
     596ae1e (exit 1, 53 bare sites), so it could not have reported a
     new red in any case -- the corpus's permanently-red-tripwire
     genre.
"""

from fractions import Fraction
from itertools import combinations_with_replacement, permutations
import ast
import inspect
import math
import random
import textwrap


HELD_OUT_OF_THE_BANK = False

CLAIM_SURFACE_SHA256 = (
    "5f72fd9a90f40cb4188f1019fce1d21ff42cf9773885108f4f4b23383e4f2465")

CHECK_NAME = "L_scan_survivor_set_and_F7_dedup_equivalence"

# The frozen surface bars these tokens from the object's NAME, its
# key_result and its summary.  Enforced on the verdict path.
BARRED_TOKENS = ("invariance", "invariant", "order-independent",
                 "order independent")

GRADE = "P_structural_exhaustive"

MAY_NOT_CITE = (
    "filter-order invariance, order-independence of the pipeline, or any "
    "number of orderings 'verified' in a sense that could have failed",
    "that the fermion scan is order-independent -- the scan's real F7 IS "
    "stateful and order-dependent; only a per-class count agreement is "
    "computed here",
    "that the total spectator-reduction variant is canonical F6, or that "
    "the two agree anywhere beyond what is computed",
    "that this module's four-member survivor set is gauge.py's Phase-1 "
    "output -- the F6 variants are incomparable and both facts are "
    "computed here",
    "as a verification of the fermion scan's physics, its caps, or its "
    "filters' adequacy",
    "as clearing the companion-repo standalone for banking -- this banks "
    "one computation out of it",
    "as evidence about the standalone's VERSION_LOCK provenance chain, "
    "which is not read here",
)

# --------------------------------------------------------------------------
# DECLARED inventories.  Each is compared against a computed quantity on
# the verdict path.  A declared figure that is not compared is a defect.
# --------------------------------------------------------------------------

DECLARED_UNIVERSE_ORDERED = 4680
DECLARED_UNIVERSE_DISTINCT = 1680

DECLARED_FILTER_POPULATIONS = {
    "F1": 348, "F2": 1344, "F3": 1650, "F4": 96,
    "F5": 840, "F6": 48, "F7": 864,
}

DECLARED_SURVIVORS = (
    (("1", "1"), ("1", "2"), ("3", "1"), ("3", "1"), ("3b", "2")),
    (("1", "1"), ("1", "1"), ("1", "2"), ("3", "1"), ("3", "1"), ("3b", "2")),
    (("1", "1"), ("1", "2"), ("3", "1"), ("3", "1"), ("3b", "2"), ("8", "1")),
    (("1", "1"), ("1", "1"), ("1", "2"), ("3", "1"), ("3", "1"),
     ("3b", "2"), ("8", "1")),
)
DECLARED_SURVIVOR_DOF = (45, 48, 69, 72)
DECLARED_MIN_DOF = 45

DECLARED_CPT_CLASSES = 864
DECLARED_CLASS_SIZE_HISTOGRAM = {1: 48, 2: 816}

DECLARED_F6_STREAM_SIZE = 8

DECLARED_F6_MUTANT_SURVIVOR_COUNTS = {
    "F6_constant_true": 6,
    "F6_parity_on_length": 3,
    "F6_constant_false": 0,
}

DECLARED_GAUGE_AN_POPULATION = 26
DECLARED_AN_MINUS_SPEC = 2
DECLARED_SPEC_MINUS_AN = 24

DECLARED_ONE_SIDED_STATEFUL = 12
DECLARED_ONE_SIDED_PURE = 4

DECLARED_ORDERINGS = 5040

EXPECTED_LEGS = {CHECK_NAME: (
    "controls_dof_functional_edit_moves_multiset_not_survivor_set",
    "controls_f6_mutants_move_the_survivor_set",
    "controls_one_sided_anomaly_filter_breaks_the_stream_agreement",
    "controls_order_sweep_is_satisfied_by_every_variant_executed",
    "declared_barred_tokens_absent_from_name_key_result_and_summary",
    "f6_variant_incomparability_with_gauge_an_computed",
    "f7_filtered_stream_agreement_computed",
    "f7_full_universe_agreement_computed_and_declared_by_construction",
    "f7_stream_conjugation_closure_computed_set_exact",
    "gauge_af_predicate_ties_the_composed_f1_f2_by_value",
    "gauge_an_ties_the_standalone_uniform_dimension_variant_by_value",
    "gauge_b0_su2_ties_by_value",
    "gauge_b0_su3_ties_by_value",
    "gauge_content_predicate_ties_by_value",
    "gauge_cpt_canonical_ties_by_value",
    "gauge_cubic_anomaly_ties_by_value",
    "gauge_dof_functional_ties_by_value",
    "gauge_generation_count_and_rep_list_tie_by_value",
    "gauge_phase1_loop_supplies_the_universe_by_value",
    "gauge_s3_predicate_ties_f4_cubic_by_value",
    "gauge_wi_predicate_ties_f5_witten_by_value",
    "gauge_witten_parity_ties_by_value",
    "rt6_intersection_matches_the_stateful_pipeline_output",
    "seven_filter_populations_set_exact",
    "survivor_dof_multiset_set_exact",
    "survivor_min_dof_member_is_unique",
    "survivor_set_declared_set_exact",
)}


# --------------------------------------------------------------------------
# This module's own transcription of the scan's tables and filters.
# Transcribed from the companion-repo standalone, which is not importable
# from this repository.  Everything that CAN be tied to gauge.py by value
# is tied below; F6's spectator-reduction variant cannot be.
# --------------------------------------------------------------------------

SU3 = {
    "1":  {"dim": 1, "T": Fraction(0),    "A": Fraction(0)},
    "3":  {"dim": 3, "T": Fraction(1, 2), "A": Fraction(1, 2)},
    "3b": {"dim": 3, "T": Fraction(1, 2), "A": Fraction(-1, 2)},
    "6":  {"dim": 6, "T": Fraction(5, 2), "A": Fraction(7, 2)},
    "6b": {"dim": 6, "T": Fraction(5, 2), "A": Fraction(-7, 2)},
    "8":  {"dim": 8, "T": Fraction(3),    "A": Fraction(0)},
}
SU2 = {
    "1": {"dim": 1, "T": Fraction(0)},
    "2": {"dim": 2, "T": Fraction(1, 2)},
}
CONJ3 = {"3": "3b", "3b": "3", "6": "6b", "6b": "6", "8": "8", "1": "1"}
COLORED_REPS = ("3", "3b", "6", "6b", "8")
N_GEN = 3
AF3_BOUND = Fraction(11)
AF2_BOUND = Fraction(22, 3)
AF_COEFF = Fraction(2, 3)


def b0_su3(t):
    return AF3_BOUND - AF_COEFF * sum(
        SU3[a]["T"] * SU2[b]["dim"] for a, b in t) * N_GEN


def b0_su2(t):
    return AF2_BOUND - AF_COEFF * sum(
        SU2[b]["T"] * SU3[a]["dim"] for a, b in t) * N_GEN


def cubic_anomaly(t):
    return sum(SU3[a]["A"] * SU2[b]["dim"] for a, b in t)


def witten_parity(t):
    return sum(SU3[a]["dim"] for a, b in t if b == "2") % 2


def dof(t):
    return sum(SU3[a]["dim"] * SU2[b]["dim"] for a, b in t) * N_GEN


def f1_af_su3(t):
    return b0_su3(t) > 0


def f2_af_su2(t):
    return b0_su2(t) > 0


def f3_content(t):
    """Doublet-singlet CONTENT.  Not a chirality test."""
    return (any(SU3[a]["dim"] > 1 and b == "2" for a, b in t)
            and any(SU3[a]["dim"] > 1 and b == "1" for a, b in t))


def f4_cubic(t):
    return cubic_anomaly(t) == 0


def f5_witten(t):
    return witten_parity(t) == 0


def conjugate(t):
    return tuple(sorted((CONJ3[a], b) for a, b in t))


def cpt_canonical(t):
    return min(tuple(sorted(t)), conjugate(t))


def f7_pure(t):
    return tuple(sorted(t)) == cpt_canonical(t)


def f6_spectator_reduction(t):
    """The TOTAL spectator-reduction variant.  Not canonical F6."""
    spectators = []
    remaining = list(t)
    for f in t:
        if (SU3[f[0]]["dim"] > 1 and f[1] == "1"
                and SU3[f[0]]["A"] == 0):
            spectators.append(f)
            remaining.remove(f)
    if spectators:
        if not any(SU3[a]["dim"] > 1 for a, _ in remaining):
            return False
        return f6_spectator_reduction(tuple(remaining))
    cd = [f for f in t if SU3[f[0]]["dim"] > 1 and f[1] == "2"]
    cs = [f for f in t if SU3[f[0]]["dim"] > 1 and f[1] == "1"]
    ld = [f for f in t if SU3[f[0]]["dim"] == 1 and f[1] == "2"]
    ls = [f for f in t if SU3[f[0]]["dim"] == 1 and f[1] == "1"]
    if len(cd) != 1 or not ld:
        return False
    Nc = SU3[cd[0][0]]["dim"]
    if not all(SU3[a]["dim"] == Nc for a, _ in cs):
        return False
    if len(cs) == 2 and len(ls) >= 1:
        d = 4 + 4 * (Nc ** 2 - 1)
        return math.isqrt(d) ** 2 == d
    if len(cs) == 1 and len(ls) >= 1:
        v = Fraction(4 * Nc ** 2, 3 + Nc ** 2)
        p, q = v.numerator, v.denominator
        return math.isqrt(p * q) ** 2 == p * q
    return False


def f6_uniform_dimension(t):
    """The standalone's transcription of gauge.py's Phase-1 `_an`.

    Carried here only so that the transcription claim can be TIED to
    gauge.py's own function by value; it is not this module's F6.
    """
    cd = [f for f in t if SU3[f[0]]["dim"] > 1 and f[1] == "2"]
    cs = [f for f in t if SU3[f[0]]["dim"] > 1 and f[1] == "1"]
    ld = [f for f in t if SU3[f[0]]["dim"] == 1 and f[1] == "2"]
    ls = [f for f in t if SU3[f[0]]["dim"] == 1 and f[1] == "1"]
    if len(cd) != 1 or not ld:
        return False
    Nc = SU3[cd[0][0]]["dim"]
    if not all(SU3[a]["dim"] == Nc for a, _ in cs):
        return False
    if len(cs) == 2 and len(ls) >= 1:
        d = 4 + 4 * (Nc ** 2 - 1)
        return math.isqrt(d) ** 2 == d
    if len(cs) == 1 and len(ls) >= 1:
        v = Fraction(4 * Nc ** 2, 3 + Nc ** 2)
        p, q = v.numerator, v.denominator
        return math.isqrt(p * q) ** 2 == p * q
    return False


def enumerate_local():
    """This module's own enumeration, tied by value to gauge.py's."""
    out = []
    for cd_rep in COLORED_REPS:
        for n_cs in range(0, 4):
            for combo in combinations_with_replacement(COLORED_REPS, n_cs):
                for has_ld in (True, False):
                    for n_ls in range(0, 3):
                        t = [(cd_rep, "2")]
                        t += [(c, "1") for c in combo]
                        if has_ld:
                            t.append(("1", "2"))
                        t += [("1", "1")] * n_ls
                        out.append(tuple(t))
    return out


# --------------------------------------------------------------------------
# gauge.py's OWN Phase-1 statements, executed verbatim out of its source.
# gauge.py exposes none of this at module level (every name below is local
# to check_T_field), so the tie is by source extraction.  Failure to locate
# the statements is reported as a failure, never worked around.
# --------------------------------------------------------------------------

_GAUGE_ASSIGN = ("_SU3", "_SU2", "_cr", "_AF3", "_AF2", "_c23", "Ng")
_GAUGE_DEF = ("_af", "_ch", "_s3", "_wi", "_an", "_ck")

_GAUGE_CACHE = {}


def _gauge_phase1():
    """Execute gauge.check_T_field's own tables, helpers and Phase-1 loop.

    The loop's first filter call is intercepted so that every template the
    loop constructs is harvested; nothing else in the loop is altered, so
    the caps, the representation list, the ordered `_product` enumeration
    and the construction order are gauge.py's own.
    """
    if _GAUGE_CACHE:
        return _GAUGE_CACHE
    from itertools import product as _product
    from apf import gauge as _gauge

    tree = ast.parse(textwrap.dedent(inspect.getsource(_gauge.check_T_field)))
    fn = tree.body[0]
    picked, loop = [], None
    for node in fn.body:
        if (isinstance(node, ast.Assign) and len(node.targets) == 1
                and isinstance(node.targets[0], ast.Name)
                and node.targets[0].id in _GAUGE_ASSIGN):
            picked.append(node)
        elif (isinstance(node, ast.FunctionDef)
              and node.name in _GAUGE_DEF):
            picked.append(node)
        elif (isinstance(node, ast.For)
              and isinstance(node.target, ast.Name)
              and node.target.id == "cd"
              and isinstance(node.iter, ast.Name)
              and node.iter.id == "_cr"):
            loop = node
    got_assign = tuple(n.targets[0].id for n in picked
                       if isinstance(n, ast.Assign))
    got_def = tuple(n.name for n in picked if isinstance(n, ast.FunctionDef))
    missing = (sorted(set(_GAUGE_ASSIGN) - set(got_assign))
               + sorted(set(_GAUGE_DEF) - set(got_def))
               + ([] if loop is not None else ["phase1_loop"]))
    if missing:
        raise RuntimeError(
            "gauge.check_T_field no longer exposes the Phase-1 statements "
            "this tie reads: missing %r" % (missing,))

    # `Ng` is NOT supplied here: gauge.py's own `Ng = dag_get('N_gen', ...)`
    # statement is among the extracted assignments and runs against the live
    # DAG through gauge.py's own accessor, so the generation count this
    # module multiplies by is gauge.py's, not a literal of this file's.
    from apf.apf_utils import dag_get as _dag_get
    ns = {"Fraction": Fraction, "_math": math, "_product": _product,
          "dag_get": _dag_get, "check": lambda *a, **k: None,
          "tested": 0, "survivors": [], "seen": set()}
    body = ast.Module(body=picked, type_ignores=[])
    ast.fix_missing_locations(body)
    exec(compile(body, "<gauge.check_T_field:extract>", "exec"), ns)

    harvest = []

    def _af_harvest(t):
        harvest.append(t)
        return False

    real_af = ns["_af"]
    ns["_af"] = _af_harvest
    loop_mod = ast.Module(body=[loop], type_ignores=[])
    ast.fix_missing_locations(loop_mod)
    exec(compile(loop_mod, "<gauge.check_T_field:phase1>", "exec"), ns)
    ns["_af"] = real_af

    _GAUGE_CACHE.update({
        "ordered": ns["tested"],
        "harvest": tuple(harvest),
        "distinct": frozenset(harvest),
        "SU3": ns["_SU3"], "SU2": ns["_SU2"], "cr": ns["_cr"],
        "AF3": ns["_AF3"], "AF2": ns["_AF2"], "c23": ns["_c23"],
        "Ng": ns["Ng"],
        "af": real_af, "ch": ns["_ch"], "s3": ns["_s3"],
        "wi": ns["_wi"], "an": ns["_an"], "ck": ns["_ck"],
    })
    return _GAUGE_CACHE


# --------------------------------------------------------------------------
# analysis, computed once
# --------------------------------------------------------------------------

_ANALYSIS = {}


def _order_sweep(pred_sets):
    """Fold the seven sets in every ordering and count disagreements.

    The fold starts from the first set of each ordering rather than from a
    copy of the universe; every predicate set is a subset of the universe,
    so intersecting the universe first is the identity and the fold is the
    same one in the same order.
    """
    names = list(pred_sets)
    ref = None
    disagreements = 0
    orderings = 0
    for order in permutations(names):
        surv = set(pred_sets[order[0]])
        for k in order[1:]:
            surv &= pred_sets[k]
        fs = frozenset(surv)
        if ref is None:
            ref = fs
        elif fs != ref:
            disagreements += 1
        orderings += 1
    return orderings, disagreements, (ref if ref is not None else frozenset())


def _stateful_dedup(stream, canon):
    seen = set()
    out = []
    for t in stream:
        c = canon(t)
        if c in seen:
            continue
        seen.add(c)
        out.append(t)
    return out


def _per_class_counts(items, canon):
    d = {}
    for t in items:
        d[canon(t)] = d.get(canon(t), 0) + 1
    return d


def _analysis():
    if _ANALYSIS:
        return _ANALYSIS
    g = _gauge_phase1()
    universe = tuple(sorted(g["distinct"]))
    local = enumerate_local()

    P = {
        "F1": {t for t in universe if f1_af_su3(t)},
        "F2": {t for t in universe if f2_af_su2(t)},
        "F3": {t for t in universe if f3_content(t)},
        "F4": {t for t in universe if f4_cubic(t)},
        "F5": {t for t in universe if f5_witten(t)},
        "F6": {t for t in universe if f6_spectator_reduction(t)},
        "F7": {t for t in universe if f7_pure(t)},
    }
    orderings, disagreements, survivors = _order_sweep(P)

    classes = {}
    for t in universe:
        classes.setdefault(cpt_canonical(t), []).append(t)
    size_hist = {}
    for members in classes.values():
        size_hist[len(members)] = size_hist.get(len(members), 0) + 1

    universe_sorted = {tuple(sorted(t)) for t in universe}
    stream = [t for t in universe
              if all(t in P[k] for k in ("F1", "F2", "F3", "F4", "F5", "F6"))]
    stream_sorted = {tuple(sorted(t)) for t in stream}
    stream_closed = all(conjugate(t) in stream_sorted for t in stream)
    stateful = _stateful_dedup(stream, cpt_canonical)
    pure = [t for t in stream if f7_pure(t)]

    # --- controls, executed ---
    mutant_f6 = {
        "F6_constant_true": lambda t: True,
        "F6_parity_on_length": lambda t: len(t) % 2 == 0,
        "F6_constant_false": lambda t: False,
    }
    mutant_rows = {}
    for label, pred in mutant_f6.items():
        Q = dict(P)
        Q["F6"] = {t for t in universe if pred(t)}
        n_ord, n_dis, surv = _order_sweep(Q)
        mutant_rows[label] = {
            "survivors": len(surv), "orderings": n_ord,
            "order_disagreements": n_dis,
            "moved_the_survivor_set": frozenset(surv) != survivors,
        }
    rng = random.Random(11)
    # min(): the sample size must not be a cliff.  At the shipped
    # universe (1680 templates) this IS 1300 and no returned value
    # moves.
    R = {("R%d" % i): set(rng.sample(list(universe),
                                     min(1300, len(universe))))
         for i in range(7)}
    r_ord, r_dis, r_surv = _order_sweep(R)

    one_sided = [t for t in universe
                 if f1_af_su3(t) and f2_af_su2(t) and f3_content(t)
                 and cubic_anomaly(t) <= 0 and f5_witten(t)
                 and f6_spectator_reduction(t)]
    os_stateful = _stateful_dedup(one_sided, cpt_canonical)
    os_pure = [t for t in one_sided if f7_pure(t)]

    def dof_mutant(t):
        return sum(SU3[a]["dim"] + SU2[b]["dim"] for a, b in t) * N_GEN

    an_set = {t for t in universe if g["an"](t)}
    spec_set = P["F6"]

    _ANALYSIS.update({
        "gauge_ordered": g["ordered"],
        "gauge_harvest": len(g["harvest"]),
        "universe": universe,
        "local": local,
        "P": P,
        "orderings": orderings,
        "order_disagreements": disagreements,
        "survivors": survivors,
        "survivor_dof": tuple(sorted(dof(t) for t in survivors)),
        "classes": classes,
        "class_size_hist": size_hist,
        "universe_conj_closed": all(conjugate(t) in universe_sorted
                                    for t in universe),
        "universe_per_class": _per_class_counts(
            [t for t in universe if f7_pure(t)], cpt_canonical),
        "stream": stream,
        "stream_closed": stream_closed,
        "stateful": stateful,
        "pure": pure,
        "mutant_rows": mutant_rows,
        "random_sweep": {"orderings": r_ord, "disagreements": r_dis,
                         "survivors": len(r_surv)},
        "one_sided": {"stateful": len(os_stateful), "pure": len(os_pure),
                      "per_class_equal": (
                          _per_class_counts(os_stateful, cpt_canonical)
                          == _per_class_counts(os_pure, cpt_canonical))},
        "dof_mutant_multiset": tuple(sorted(dof_mutant(t)
                                            for t in survivors)),
        "an_population": len(an_set),
        "an_minus_spec": len(an_set - spec_set),
        "spec_minus_an": len(spec_set - an_set),
        "an_ties_uniform": all(
            g["an"](t) == f6_uniform_dimension(t) for t in universe),
        "gauge_fns": g,
    })
    return _ANALYSIS


# --------------------------------------------------------------------------
# result envelope
# --------------------------------------------------------------------------

def _result(name, legs, key_result, summary, epistemic):
    fails = []
    if epistemic != GRADE:
        fails.append("grade mismatch: returned %r, declared %r"
                     % (epistemic, GRADE))
    have = tuple(sorted(legs))
    want = tuple(EXPECTED_LEGS[name])
    if have != want:
        fails.append("leg inventory mismatch: missing=%r extra=%r"
                     % (sorted(set(want) - set(have)),
                        sorted(set(have) - set(want))))
    for label in sorted(legs):
        ok, ev = legs[label]
        if not ok:
            fails.append("%s: %s" % (label, ev))
    return {
        "name": name,
        "passed": not fails,
        "tier": 3,
        "epistemic": epistemic,
        "legs": {k: {"passed": bool(v[0]), "evidence": v[1]}
                 for k, v in legs.items()},
        "leg_count": len(legs),
        "fail_reasons": fails,
        "key_result": key_result,
        "summary": summary,
        "dependencies": [],
        "cross_refs": ["T_field"],
        "may_not_cite": list(MAY_NOT_CITE),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": CLAIM_SURFACE_SHA256,
        "inventory_note": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


def check_L_scan_survivor_set_and_F7_dedup_equivalence():
    """L_scan_survivor_set_and_F7_dedup_equivalence [P_structural].

    Pins the seven-filter survivor set over the template universe that
    gauge.py's own Phase-1 loop enumerates, and computes the
    per-CPT-class agreement of the scan's two F7 readings on the full
    universe and on the filtered stream.  BOTH halves are forced by a
    computed conjugation closure -- of the universe and of the stream
    respectively -- and are declared as such rather than reported as
    results.  The one computed fact behind them is the closure, which an
    executed control breaks.

    Every figure in the returned sentences is computed at return time.
    """
    legs = {}
    # The handler covers the gauge.py EXTRACTION and nothing else.
    # Anything that is not an extraction failure RAISES.
    try:
        _gauge_phase1()
    except Exception as exc:
        reason = "gauge.py Phase-1 extraction failed: %r" % (exc,)
        for label in EXPECTED_LEGS[CHECK_NAME]:
            legs[label] = (False, reason)
        return _result(CHECK_NAME, legs,
                       key_result="not computed: " + reason,
                       summary="not computed: " + reason,
                       epistemic=GRADE)
    A = _analysis()

    U = A["universe"]
    g = A["gauge_fns"]
    P = A["P"]

    # ---- (1) the universe, by value, out of gauge.py's own loop --------
    # The tie compares gauge.py's OWN harvested set against this module's
    # own enumeration, and separately requires the universe every other leg
    # consumes to BE gauge's set.  Reading the gauge side through `U` would
    # make the equality a self-comparison the moment `U` is sourced
    # elsewhere; the two clauses are kept apart for that reason.
    gauge_set = set(g["distinct"])
    local_set = set(A["local"])
    legs["gauge_phase1_loop_supplies_the_universe_by_value"] = (
        (A["gauge_ordered"] == DECLARED_UNIVERSE_ORDERED
         and A["gauge_harvest"] == DECLARED_UNIVERSE_ORDERED
         and len(gauge_set) == DECLARED_UNIVERSE_DISTINCT
         and len(local_set) == DECLARED_UNIVERSE_DISTINCT
         and gauge_set == local_set
         and set(U) == gauge_set
         and len(U) == DECLARED_UNIVERSE_DISTINCT),
        ("gauge.check_T_field's own Phase-1 statements constructed {0} "
         "ordered tuples over {1} distinct templates; this module's "
         "combinations_with_replacement enumeration produced {2} tuples "
         "over {3} distinct templates; the two DISTINCT SETS are equal "
         "({4}), and the universe every other leg consumes is gauge's own "
         "set ({5})".format(
             A["gauge_ordered"], len(gauge_set), len(A["local"]),
             len(local_set), gauge_set == local_set, set(U) == gauge_set)))

    # ---- (2) the table ties, by value, quantity by quantity ------------
    def _tie(fn_local, fn_gauge, label, kind):
        bad = [t for t in U if fn_local(t) != fn_gauge(t)]
        return ((not bad and len(U) == DECLARED_UNIVERSE_DISTINCT),
                ("{0} computed from gauge.check_T_field's own tables and "
                 "from this module's, compared as {1} on all {2} "
                 "templates: {3} disagreements".format(
                     label, kind, len(U), len(bad))))

    gS3, gS2, gNg = g["SU3"], g["SU2"], g["Ng"]
    legs["gauge_generation_count_and_rep_list_tie_by_value"] = (
        (N_GEN == gNg and tuple(g["cr"]) == tuple(COLORED_REPS)
         and AF3_BOUND == g["AF3"] and AF2_BOUND == g["AF2"]
         and AF_COEFF == g["c23"]),
        ("the generation count this module multiplies by ({0}) is read "
         "from gauge.check_T_field's own `Ng = dag_get('N_gen', ...)` "
         "statement executed against the live DAG, and equals this "
         "module's N_GEN ({1}); the colored-rep list, both asymptotic-"
         "freedom bounds and the Weyl coefficient are compared as computed "
         "values against gauge's own: {2}, {3}, {4}, {5}".format(
             gNg, N_GEN, tuple(g["cr"]) == tuple(COLORED_REPS),
             AF3_BOUND == g["AF3"], AF2_BOUND == g["AF2"],
             AF_COEFF == g["c23"])))
    legs["gauge_b0_su3_ties_by_value"] = _tie(
        b0_su3,
        lambda t: g["AF3"] - g["c23"] * sum(
            gS3[a]["T"] * gS2[b]["dim"] for a, b in t) * gNg,
        "b0(SU(3))", "exact Fractions")
    legs["gauge_b0_su2_ties_by_value"] = _tie(
        b0_su2,
        lambda t: g["AF2"] - g["c23"] * sum(
            gS2[b]["T"] * gS3[a]["dim"] for a, b in t) * gNg,
        "b0(SU(2))", "exact Fractions")
    legs["gauge_cubic_anomaly_ties_by_value"] = _tie(
        cubic_anomaly,
        lambda t: sum(gS3[a]["A"] * gS2[b]["dim"] for a, b in t),
        "the [SU(3)]^3 anomaly sum", "exact Fractions")
    legs["gauge_witten_parity_ties_by_value"] = _tie(
        witten_parity,
        lambda t: sum(gS3[a]["dim"] for a, b in t if b == "2") % 2,
        "the Witten parity residue", "integers")
    legs["gauge_dof_functional_ties_by_value"] = _tie(
        dof,
        lambda t: sum(gS3[a]["dim"] * gS2[b]["dim"] for a, b in t) * gNg,
        "the Weyl DOF functional", "integers")
    legs["gauge_content_predicate_ties_by_value"] = _tie(
        f3_content, g["ch"], "the F3 doublet-singlet content predicate",
        "computed predicate values")
    # The three helpers gauge.py defines that no leg above reads.  Each
    # tie CALLS gauge's own extracted function; the four legs above
    # compare quantities built from gauge's TABLES, which is a weaker
    # thing.
    legs["gauge_af_predicate_ties_the_composed_f1_f2_by_value"] = _tie(
        lambda t: f1_af_su3(t) and f2_af_su2(t), g["af"],
        "gauge.check_T_field's own `_af` asymptotic-freedom predicate "
        "against this module's F1-and-F2 composed", "computed predicate values")
    legs["gauge_s3_predicate_ties_f4_cubic_by_value"] = _tie(
        f4_cubic, g["s3"],
        "gauge.check_T_field's own `_s3` cubic-anomaly predicate against "
        "this module's F4", "computed predicate values")
    legs["gauge_wi_predicate_ties_f5_witten_by_value"] = _tie(
        f5_witten, g["wi"],
        "gauge.check_T_field's own `_wi` Witten-parity predicate against "
        "this module's F5", "computed predicate values")
    legs["gauge_cpt_canonical_ties_by_value"] = _tie(
        cpt_canonical, g["ck"], "the CPT canonical representative",
        "computed tuples")
    legs["gauge_an_ties_the_standalone_uniform_dimension_variant_by_value"] = (
        (A["an_ties_uniform"]
         and A["an_population"] == DECLARED_GAUGE_AN_POPULATION),
        ("gauge.check_T_field's own `_an` and THIS MODULE'S COPY of the "
         "standalone's uniform-dimension variant agree on all {0} "
         "templates and admit {1}, compared as computed predicate values. "
         "SCOPE: the companion-repo standalone is not importable from "
         "this repository and is not executed here, so this ties gauge.py "
         "to a transcription, not to the standalone's own "
         "object".format(len(U), A["an_population"])))

    # ---- (3) populations, the intersection, the pin --------------------
    pops = {k: len(v) for k, v in P.items()}
    legs["seven_filter_populations_set_exact"] = (
        pops == DECLARED_FILTER_POPULATIONS,
        ("over the {0} distinct templates each of the seven filters is "
         "computed as a predicate set with populations {1}, each asserted "
         "set-exactly against the declared table {2}".format(
             len(U), pops, DECLARED_FILTER_POPULATIONS)))

    surv_sorted = frozenset(tuple(sorted(t)) for t in A["survivors"])
    legs["survivor_set_declared_set_exact"] = (
        surv_sorted == frozenset(DECLARED_SURVIVORS),
        ("under the TOTAL spectator-reduction variant of F6 the "
         "intersection of the seven sets has exactly {0} members, and the "
         "computed member SET is compared against a declared inventory of "
         "{1} templates: equal={2}".format(
             len(A["survivors"]), len(DECLARED_SURVIVORS),
             surv_sorted == frozenset(DECLARED_SURVIVORS))))
    legs["survivor_dof_multiset_set_exact"] = (
        A["survivor_dof"] == DECLARED_SURVIVOR_DOF,
        ("the survivors' DOF multiset is {0}, compared set-exactly against "
         "the declared {1}".format(list(A["survivor_dof"]),
                                   list(DECLARED_SURVIVOR_DOF))))
    n_at_min = sum(1 for d in A["survivor_dof"]
                   if d == min(A["survivor_dof"])) if A["survivor_dof"] else 0
    legs["survivor_min_dof_member_is_unique"] = (
        (n_at_min == 1 and min(A["survivor_dof"]) == DECLARED_MIN_DOF),
        ("{0} of the {1} survivors sit at the minimum DOF {2}".format(
            n_at_min, len(A["survivors"]),
            min(A["survivor_dof"]) if A["survivor_dof"] else None)))

    # ---- (4) the two F7 readings ---------------------------------------
    uni_counts = set(A["universe_per_class"].values())
    legs["f7_full_universe_agreement_computed_and_declared_by_construction"] = (
        (len(A["classes"]) == DECLARED_CPT_CLASSES
         and A["class_size_hist"] == DECLARED_CLASS_SIZE_HISTOGRAM
         and A["universe_conj_closed"]
         and uni_counts == {1}
         and len(A["universe_per_class"]) == DECLARED_CPT_CLASSES),
        ("the universe carries {0} CPT classes with size histogram {1} and "
         "is computed closed under SU(3) conjugation ({2}); the pure "
         "canonical-representative predicate selects exactly {3} member in "
         "each class and a first-seen dedup keeps exactly one by "
         "definition. DECLARED BY CONSTRUCTION, NOT REPORTED AS A RESULT: "
         "closure plus a minimum over a one- or two-element orbit forces "
         "this agreement whatever the filters do, so on this domain the "
         "two readings cannot disagree.".format(
             len(A["classes"]), A["class_size_hist"],
             A["universe_conj_closed"], sorted(uni_counts))))

    st_counts = _per_class_counts(A["stateful"], cpt_canonical)
    pu_counts = _per_class_counts(A["pure"], cpt_canonical)
    legs["f7_filtered_stream_agreement_computed"] = (
        (st_counts == pu_counts
         and len(A["stream"]) == DECLARED_F6_STREAM_SIZE
         and sorted(dof(t) for t in A["stateful"])
         == sorted(dof(t) for t in A["pure"])
         == list(DECLARED_SURVIVOR_DOF)),
        ("on the {0}-member F1-F6 stream the scan's stateful first-seen F7 "
         "dedup keeps {1} templates and the pure canonical-representative "
         "predicate keeps {2}; the per-class counts are equal ({3}) and "
         "both DOF multisets are {4}. This is the equivalence the "
         "standalone relies on and never states. FORCED, NOT REPORTED AS "
         "AN INDEPENDENT RESULT: given the computed conjugation closure "
         "of this stream it could not have failed. The executed one-sided "
         "control below breaks that CLOSURE, and the agreement fails "
         "with it.".format(
             len(A["stream"]), len(A["stateful"]), len(A["pure"]),
             st_counts == pu_counts,
             sorted(dof(t) for t in A["stateful"]))))
    legs["f7_stream_conjugation_closure_computed_set_exact"] = (
        A["stream_closed"],
        ("the sorted-form set of the {0}-member F1-F6 stream is computed "
         "closed under SU(3) conjugation: {1}. This is the fact the "
         "filtered-stream agreement rides on, and it is what the "
         "one-sided control breaks.".format(
             len(A["stream"]), A["stream_closed"])))

    legs["rt6_intersection_matches_the_stateful_pipeline_output"] = (
        (sorted(dof(t) for t in A["survivors"])
         == sorted(dof(t) for t in A["stateful"])
         and {cpt_canonical(t) for t in A["survivors"]}
         == {cpt_canonical(t) for t in A["stateful"]}),
        ("the seven-set intersection (pure F7) and the scan's own "
         "filter-then-stateful-dedup pipeline reach the same {0} CPT "
         "classes with the same DOF multiset {1}; the standalone's "
         "undisclosed F7 substitution is computed benign on this stream. "
         "FORCED by the same computed stream closure as the two legs "
         "above, in both clauses; it is retained as the pipeline-shaped "
         "statement of that closure and is disclosed here rather than "
         "counted as a third independent fact".format(
             len({cpt_canonical(t) for t in A["survivors"]}),
             sorted(dof(t) for t in A["survivors"]))))

    # ---- (5) the F6-variant fact ---------------------------------------
    legs["f6_variant_incomparability_with_gauge_an_computed"] = (
        (A["an_minus_spec"] == DECLARED_AN_MINUS_SPEC
         and A["spec_minus_an"] == DECLARED_SPEC_MINUS_AN
         and A["an_minus_spec"] > 0 and A["spec_minus_an"] > 0),
        ("gauge.py's Phase-1 F6 (`_an`, uniform dimension) admits {0} "
         "templates and this module's spectator-reduction F6 admits {1}; "
         "{2} are admitted by `_an` alone and {3} by the spectator variant "
         "alone, so NEITHER CONTAINS THE OTHER and the survivor set pinned "
         "here is not gauge.py's Phase-1 output".format(
             A["an_population"], len(P["F6"]),
             A["an_minus_spec"], A["spec_minus_an"])))

    # ---- (6) controls, executed ----------------------------------------
    rows = A["mutant_rows"]
    counts_ok = all(
        rows[k]["survivors"] == DECLARED_F6_MUTANT_SURVIVOR_COUNTS[k]
        and rows[k]["moved_the_survivor_set"] for k in rows)
    legs["controls_f6_mutants_move_the_survivor_set"] = (
        (counts_ok and set(rows) == set(DECLARED_F6_MUTANT_SURVIVOR_COUNTS)),
        ("three F6 mutants move the intersection to {0} against the "
         "declared {1} members, and each moved set differs from the pinned "
         "one: {2}. FORCED CLAUSES, NAMED: the constant-false row's "
         "survivor count and its moved-the-set flag are both forced; the "
         "other two rows are not".format(
             {k: rows[k]["survivors"] for k in sorted(rows)},
             len(DECLARED_SURVIVORS),
             {k: rows[k]["moved_the_survivor_set"] for k in sorted(rows)})))

    sweep_rows = {k: rows[k]["order_disagreements"] for k in sorted(rows)}
    legs["controls_order_sweep_is_satisfied_by_every_variant_executed"] = (
        (A["orderings"] == DECLARED_ORDERINGS
         and A["order_disagreements"] == 0
         and all(rows[k]["orderings"] == DECLARED_ORDERINGS for k in rows)
         and all(v == 0 for v in sweep_rows.values())
         and A["random_sweep"]["orderings"] == DECLARED_ORDERINGS
         and A["random_sweep"]["disagreements"] == 0),
        ("folding the seven sets in each of the {0} orderings produced {1} "
         "disagreements on the real filters, {2} on the three F6 mutants, "
         "and {3} on seven pseudo-random subsets carrying no physics "
         "(their intersection has {4} members). Set intersection is "
         "commutative and associative: a permutation sweep over fixed "
         "predicate sets is satisfied whatever the sets are, and the "
         "ordering count is 7! whatever the sets are, so EVERY CLAUSE OF "
         "THIS LEG IS UNFALSIFIABLE -- which is exactly what it is here "
         "to exhibit. It is a CONTROL, not evidence, and no other leg of "
         "this module reads an agreeing sweep.".format(
             A["orderings"], A["order_disagreements"], sweep_rows,
             A["random_sweep"]["disagreements"],
             A["random_sweep"]["survivors"])))

    os_row = A["one_sided"]
    legs["controls_one_sided_anomaly_filter_breaks_the_stream_agreement"] = (
        (os_row["stateful"] == DECLARED_ONE_SIDED_STATEFUL
         and os_row["pure"] == DECLARED_ONE_SIDED_PURE
         and not os_row["per_class_equal"]),
        ("replacing the [SU(3)]^3 filter by the one-sided predicate "
         "(anomaly sum <= 0) leaves a stream on which the stateful dedup "
         "keeps {0} templates and the pure predicate keeps {1}; the "
         "per-class counts DISAGREE ({2}). The filtered-stream agreement "
         "leg has a demonstrated failure channel.".format(
             os_row["stateful"], os_row["pure"],
             os_row["per_class_equal"])))

    legs["controls_dof_functional_edit_moves_multiset_not_survivor_set"] = (
        A["dof_mutant_multiset"] != DECLARED_SURVIVOR_DOF,
        ("replacing the DOF functional's product by a sum moves the DOF "
         "multiset from {0} to {1}. THIS LEG COMPUTES THAT ONE "
         "INEQUALITY AND NOTHING ELSE: it does not re-run the pipeline, "
         "so the survivor set's behaviour under the edit is asserted by "
         "this leg's NAME and computed by no clause of it, and neither "
         "is the converse direction -- the set moving while the "
         "multiset holds".format(
             list(DECLARED_SURVIVOR_DOF), list(A["dof_mutant_multiset"]))))

    # ---- (7) the frozen surface's name constraint, on the verdict path --
    key_result = (
        "over {0} distinct templates the seven-filter intersection is a "
        "declared set of {1} members with DOF multiset {2} and a unique "
        "minimum at {3}; the two F7 readings agree per CPT class on the "
        "filtered stream and on the full universe, and BOTH agreements "
        "are forced by a computed conjugation closure".format(
            len(U), len(A["survivors"]), list(A["survivor_dof"]),
            min(A["survivor_dof"]) if A["survivor_dof"] else None))
    summary = (
        "A computed survivor-set pin over the {0}-template universe "
        "gauge.py's own Phase-1 loop enumerates, plus the per-CPT-class "
        "agreement of the scan's stateful first-seen F7 dedup with the "
        "pure canonical-representative predicate. BOTH halves of that "
        "agreement are forced by a computed conjugation closure and a "
        "minimum over a one- or two-element orbit, and are declared as "
        "such rather than reported as results; the one computed fact "
        "behind them is the closure, which an executed one-sided-anomaly "
        "control breaks. Three F6 mutants move the "
        "pinned set to {1}. A permutation sweep over the seven fixed "
        "predicate sets is satisfied by all of them and by seven "
        "pseudo-random subsets, and is carried here only as a "
        "control.".format(
            len(U),
            [A["mutant_rows"][k]["survivors"]
             for k in sorted(A["mutant_rows"])]))

    scanned = " ".join((CHECK_NAME, key_result, summary)).lower()
    hits = sorted(tok for tok in BARRED_TOKENS if tok in scanned)
    legs["declared_barred_tokens_absent_from_name_key_result_and_summary"] = (
        not hits,
        ("the frozen surface bars {0} from this object's name, key_result "
         "and summary; scanning those three surfaces returned {1} hits. "
         "SCOPE, STATED -- TWO other surfaces this record returns are "
         "NOT scanned: the leg-evidence strings, including this leg's "
         "own, which prints the barred list; and the may_not_cite bars, "
         "which necessarily quote the tokens they bar (a bar has to be "
         "intelligible). Widening the scan to either would redden this "
         "leg and is not done".format(list(BARRED_TOKENS), hits)))

    return _result(CHECK_NAME, legs, key_result, summary, GRADE)


_CHECKS = {
    # LANDING REWIRE, disclosed: the audited table also carried the
    # "check_"-prefixed spelling of this same function, which would have
    # made this the only callable in the bank held under two keys -- the
    # key count and the distinct-callable count were measured equal at the
    # HEAD this module landed against, and that measurement lives in the
    # module's landing record, not here (R7@2026-08-10: a comment states a
    # genre and a reason, never a derived number).  D6@2026-08-03 makes
    # the BARE NAME canonical for a new module and puts the both-spellings
    # obligation on by-name GATES, not on registration.
    CHECK_NAME: check_L_scan_survivor_set_and_F7_dedup_equivalence,
}


def register(registry):
    """LIVE.  The hold is lifted; this module registers one check under
    the bare-name key per D6@2026-08-03.  The `HELD_OUT_OF_THE_BANK`
    guard is retained and reads False."""
    if HELD_OUT_OF_THE_BANK:
        return registry
    registry.update(_CHECKS)
    return registry


def run_all():
    return {CHECK_NAME: check_L_scan_survivor_set_and_F7_dedup_equivalence()}


if __name__ == "__main__":
    r = check_L_scan_survivor_set_and_F7_dedup_equivalence()
    print(r["name"], r["epistemic"],
          "PASS" if r["passed"] else "FAIL",
          "legs=%d" % r["leg_count"])
    for label in sorted(r["legs"]):
        leg = r["legs"][label]
        print("  [%s] %s" % ("ok" if leg["passed"] else "FAIL", label))
        print("      " + leg["evidence"])
    for f in r["fail_reasons"]:
        print("  - " + f)
    print("held_out_of_the_bank:", HELD_OUT_OF_THE_BANK)
