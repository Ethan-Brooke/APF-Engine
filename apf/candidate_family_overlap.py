"""The candidate family of a hold, with the overlap pattern computed, exactly.

BANKED v24.3.475 (2026-08-14), Situational Sign program,
candidate-family lane.  Built 2026-08-13 as a build-seat scratch object;
landed after two blinded cold audits (LWF 0.85 / 0.86, zero arithmetic
disagreement) and a cold fix seat, lifted by Ethan.  register() below
carries BARE-NAME keys per D6@2026-08-03 and is wired into the live bank
(manifest entry; EXPECTED 4178 -> 4183).  LANDING NOTE (hold-state text
and registration only; the check functions' AST is unchanged at
landing): CF4(a)'s evidence sentence still narrates the build-time
registration-shape execution -- the clause it defers to landing is met
by this landing (weakening W1 below, now discharged).
Built to the FROZEN claim surface (binding; F1-F5 adopted from it;
weakening is the permitted direction, strengthening is not):
  Artifacts_2026-08-11_session/overlap_supply_scratch/CLAIM_SURFACE_FROZEN_2026-08-13.md
  raw sha256 (verified at build against the file received; the
  CLAIM_SURFACE_SHA256 constant below is the same value, byte-for-byte):
  17526cdf1083500a15ab02fba858bcdaaf13e284f58955a285c3252bb765e1bc
Pin at build: repo HEAD `0725469`, bank EXPECTED == LOADED, gap 0
(re-verified live by the build seat 2026-08-13).

WHAT THIS MODULE COMPUTES (exact Fraction arithmetic on every verdict
path; no floats; stdlib only; the module describes what it COMPUTES).

THE PREMISE BILL (ruled 2026-08-13): TWO named premises, consumed as
names at every leg that uses them; neither is constructed, derived, or
discharged here:
  (i)  finite joint extension (`finite_joint_extension_or_amalgamation`,
       the named open obligation of apf/continuation_calculus.py --
       the name is read below from that module's own obligation
       tuple).  The family's joint existence as co-present
       admissible extensions is consumed under this premise, not
       derived: continuation_calculus's no-amalgamation guard is the
       reason the premise is owed.
  (ii) K1-UT (`K1_UT_committed_scope_exempt`, apf/hold_cost_dominance.py
       -- the name is read below from that module's own
       HOLD_EXEMPTION_BUNDLE).  The counterfactual increment-pricing of
       uncommitted alternatives -- each candidate priced on its own
       ledger copy, as what it WOULD book -- is a LICENSED K1-UT reading
       per `Reference - DECISION - The K1-UT Counterfactual Reading Is
       Licensed (2026-08-13).md`, not a third premise.  That ruling
       distinguishes reading a price from paying one: the FREE leg is
       untouched, pre-commit holding books ZERO.  Every pricing site
       below cites the ruling.

AUTHORED INPUTS (disclosed, not discharged): the base support S, the
candidate anchor pool, the capacity C, the X-sourcing, and the
base-anchoring of the coupling are AUTHORED INPUTS of every executed
instance.  This module does not discharge them and may not claim to.
What it derives, it derives GIVEN these inputs and the two named
premises.

CF1 (check_CF1_candidate_family_construction).  Given the authored base
S (frozenset-of-anchors presentation, the `_world`/anchor-tuple genre of
apf/hold_cost_dominance.py) and the authored pool, CONSTRUCTS the set of
admissible single-anchor next-commits { S u {a} : a in pool, S u {a}
admissible }, admissibility evaluated by the banked A1-capacity
functional only (count-only cost through hold_cost_dominance's own
_cost, against the authored capacity C; nothing else -- no new
admissibility notion is supplied), and TYPES it as a hold's candidate
family (the co-present pre-commit alternatives of one hold, of which at
most one will commit).  The typing is a TYPE ASSIGNMENT consistent with
the hold arc's vocabulary (L_mechanism_trichotomy,
T_hold_cost_dominance_split), NOT an identification: extension-candidate
!= hold-candidate-as-banked != sep(P) edge != branch (adjacency is not
identification -- the standing fence).  For every pair of distinct
members the pairwise support intersection is COMPUTED and VERIFIED equal
to S -- the whole retained base -- so the overlap pattern is DERIVED
from the extension type (set theory executed on the constructed family),
not authored per witness: no leg writes an intersection in by hand.  A
pool anchor already inside S is rejected by the banked K1-UT guard
itself (a null relabeling is not a transition -- _Ledger.transition
raises), executed as a control.

CF2 (check_CF2_tie_by_value).  Executed instances in which two distinct
members book EQUAL increment cost under the K1-UT ledger -- computed BY
VALUE through hold_cost_dominance's own machinery (_Ledger.transition
booking |S delta S'| * eps, and _cost), each candidate priced on its own
ledger copy under the licensed counterfactual reading (ruling cited at
the site), never by an authored equality of literals -- and which PASS
the banked genuine-tie preconditions BY VALUE through
nonlocal_tie_resolution's own predicates (_cost equality, distinctness,
the coupled-cost comparison through _joint; count-symmetric X => equal
coupled cost => co-held => the born_at_ties chance arm governs;
count-asymmetric X => decided).  One executed instance exhibits the tie
SURVIVING (co-held, chance arm) at NONZERO pairwise join
j_uv = |cfg_u & cfg_v & X| > 0, with X anchored in the base (an authored
input).  The support-blindness of the tie predicate is EXHIBITED: two
instances with every count-functional value the tie machinery computes
pairwise EQUAL (costs, joints, deficits, all as Fractions) and the join
j_uv DIFFERENT -- the verdict unmoved while j_uv moves.  Booking on
overlapping candidates is the inclusion-exclusion form
(|cfg_v & X| - |cfg_u & X|) * eps on COMPUTED intersections, never the
disjoint-witness parameter form (the section 1.1 Leg-2 rider of the
post-fix scoping return, carried as a build requirement; the _external
parametrization is not used on overlapping candidates anywhere here).

CF3 (check_CF3_carrier_join_read).  The pairwise join
j_uv = |cfg_u & cfg_v & X| on the constructed family -- nonzero on the
derived overlaps wherever X meets the base -- computed on the
constructed (authored) instance and reported as a datum of that
instance.  The join values inherit the authoredness of X (executed: the
values move when the authored X moves).  Where the pair structure closes
a cycle, the parity class of the join pattern along the cycle is
computed as a type-level invariant of the constructed instance, pinned
to its expected value derived from the authored base and X, typed in
the switching-class vocabulary as a NAMED import of classical content
(Zaslavsky-genre), and nothing more.  NO SUPPLY CLAIM: no map from the
join data to any target datum is constructed (the S4 no-canonical-map
genre bars exactly that identification; CF5(d) records the absence).

CF4 (check_CF4_falsifier_meeting).  The Arm-2a falsifier condition of
RETURN_tie_event_adversarial_2026-08-12.md, quoted verbatim in the
FALSIFIER_ARM_2A constant (an external falsifier text, quoted, not
re-derived).  Executed: the CF1 family is (a) registry-shaped under
bare-name keys (executed on a fresh registry; the banked clause is met
in full at landing -- this is a build-seat scratch object, wired into no
live bank); (b) co-present (typed as ONE hold's pre-commit alternatives,
gated on the live banked hold-arc check, with the FREE leg's zero
pre-commit booking computed); (c) overlapping (every pair intersects on
S, executed); (d) its overlap pattern DERIVED from banked transition
structure -- the extension type plus the K1-UT increment pricing --
rather than authored per witness.  THE HONEST FORM, in-module: DERIVED
means derived GIVEN the two named premises and the authored inputs; the
falsifier is met on its own terms at that conditional strength and no
other.  What meeting it does NOT do is carried as returned scope
statements: (i) the deflationary rival survives untouched; (ii) the read
channel is not opened; (iii) the stage-split verdict stands with both
halves carrying their stage (disjointness FORCED at the
realized/committed stage -- check_disjoint_partition, banked [P], gated
live here -- UNFORCED at the pre-commit candidate stage).

CF5 (check_CF5_permanent_controls).  Four permanent controls in the
K5/G5 import-control genre.  (a) The disjoint-family control: a banked
_local_tie pair of nonlocal_tie_resolution is rebuilt through that
module's own constructor and its disjointness verified; that
disjointness was CONVENIENT (a constructor's label scheme), not premised
and not wrong; nothing here retro-types those witnesses as overlapping
or re-claims them.  (b) The CoDef non-identity control: the
covering-engagement family of apf/codef_aggregation.py is
SUPPORT-IDENTICAL (every member's support equals the union; the family
varies in multiplicity, never in support extent -- the degenerate
total-overlap extreme, a TYPE precedent and NOT partial overlap), and
its argmin is provably unique (engage-once; equal-cost members are
dominated), so it cannot tie at the argmin -- executed on the banked
family through the banked module's own cost map.  (c) The FREE-leg
consistency control: the hold's pre-commit booking (ZERO, read from the
hold arc's own ledger machinery) and the counterfactual K1-UT increment
prices (nonzero, generally differing across non-tied pairs, each on its
own ledger copy; ruling cited) exhibited as DIFFERENT quantities in one
executed leg; reading a price is not paying one; no leg of this module
books a pre-commit cost into any world's ledger (enforced: the hold
ledger is still empty after all pricing).  (d) The named-absence record:
a census-conditioned negative at the pin -- an exact-token source scan
of the apf package directory finds NO banked module carrying the token
`j_uv` (census scope stated in the leg; a consumer under a different
name is outside this census's reach -- a stated limitation, and the
wider pairwise-consumption negative is the adversarial seat's Arm-1
census, cross-referenced as prior art, not re-executed).  This module
computes j_uv and feeds it NOWHERE: the value terminates in the returned
record.  The read-channel quarantine (Arm-3) stands unopened by this
module, and the module says so.

WEAKENINGS CARRIED (permitted direction) -- disclosed here and in the
build return:
  (W1) F4(a) "banked": executed as the registration SHAPE on a fresh
       registry; a scratch object cannot execute its own bankedness.
       The clause is met in full only at landing.  Met at the v24.3.475
       landing (2026-08-14): this module is registered in the live bank.
  (W2) F3 cycle-parity: computed on the one authored instance's
       3-cycles; no switching-class machinery beyond the parity product
       is built.

LEG INVENTORY (D7@2026-08-08, APPEND-AND-RECORD): _result() compares the
executed leg set against EXPECTED_LEGS set-exactly on the path the bank
would execute; a mismatch contributes a failure reason and does not
raise.  STANDING LIMIT, disclosed: this certifies that a declared leg
EXECUTED, not that it COULD HAVE FAILED.

DISCLOSED RESIDUALS (battery genre).  (1) A coherent relabel of the two
candidates u <-> v at every site of the inclusion-exclusion form is a
true invariance and escapes, as is a double negation of an equality
(the same equality either way); single-site sign or order edits are
caught.
(2) The census in CF5(d) is an exact-token scan; a consumer spelled
differently escapes it (stated in the leg).  (3) The identity-level and
record legs are disclosed as records in their evidence strings.  (4) A
coordinated replacement of the ledger-path price by the cost-difference
path collapses the two-source value tie of CF2's level-difference leg
into one source and escapes; the booked value itself remains pinned by
an independent third comparison (the unit-increment pin in the
equal-increments leg), so the collapse vacates the tie's independence,
not the value.  (5) The census token in CF5(d) is a named convention; a
self-consistent re-edit of the token is the standing
re-parametrization genre (the leg's positive control demonstrates the
scanner reports presence; it does not tie the token).  (6) The
constructor's admissibility clause is intensional: an extensionally
identical predicate substituted inside the constructor escapes; what a
leg can see -- the banked functional re-verified on the constructed
output plus the capacity-bite control -- is executed in CF1.

MAY-NOT-CITE: the frozen surface's binding 11-item list, carried in
MAY_NOT_CITE below and returned in every record.
"""

import os
from fractions import Fraction as F

from apf import continuation_calculus as _cc
from apf import hold_cost_dominance as _hcd
from apf import nonlocal_tie_resolution as _ntr
from apf import codef_aggregation as _codef

HELD_OUT_OF_THE_BANK = False  # landed v24.3.475 (2026-08-14); wired via _module_manifest

CLAIM_SURFACE_SHA256 = (
    "17526cdf1083500a15ab02fba858bcdaaf13e284f58955a285c3252bb765e1bc")

# The two named premises, READ from the banked modules' own
# declarations (asserted by name in CF1; consumed as names at the legs
# that use them; neither constructed nor discharged here).
PREMISE_I_FJE = "finite_joint_extension_or_amalgamation"
PREMISE_II_K1UT = "K1_UT_committed_scope_exempt"
K1UT_READING_RULING = (
    "Reference - DECISION - The K1-UT Counterfactual Reading Is Licensed "
    "(2026-08-13)")
NAMED_PREMISES = (PREMISE_I_FJE, PREMISE_II_K1UT)

AUTHORED_INPUTS = ("base_support_S", "candidate_anchor_pool", "capacity_C",
                   "X_sourcing", "base_anchoring_of_coupling")

# The Arm-2a falsifier, an external falsifier text: quoted verbatim from
# RETURN_tie_event_adversarial_2026-08-12.md, never re-derived.
FALSIFIER_ARM_2A = (
    "A banked co-present candidate family with OVERLAPPING configs, with "
    "the overlap pattern derived rather than authored, falsifies Arm 2a's "
    "sourcing close.")

# The frozen surface's MAY-NOT-CITE list, binding here, carried verbatim.
MAY_NOT_CITE = (
    "1. No supply claim for the sign class.  Not 'the substrate supplies "
    "the sign', not 'j_uv sources class(S_P)', not any weakened variant.  "
    "The module supplies a typed family and reads a join datum on authored "
    "instances; unforced is not supplied, and constructed is not supplied.",
    "2. No read-channel claim.  Nothing here may be cited as the dynamics, "
    "the selection law, or any banked functional READING j_uv or any "
    "pre-commit pairwise datum.  The record-exhaustion premises are "
    "unrenegotiated; the Arm-3 quarantine stands.",
    "3. Not 'the tie arc's disjointness was wrong.'  It was CONVENIENT -- "
    "a constructor's label scheme -- not premised and not an error.  The "
    "stage-split is the citable form and both halves carry their stage in "
    "the same sentence: FORCED at the realized/committed stage, UNFORCED "
    "at the pre-commit candidate stage.  Neither half may be quoted alone.",
    "4. No unconditional 'overlap is physical' / 'overlap is derived.'  "
    "The derivation is conditional on two named premises (finite joint "
    "extension + K1-UT) and on authored inputs (S, pool, X, "
    "base-anchoring); every citation carries the conditional or is a "
    "misuse.  The deflationary rival -- overlap real only where nothing "
    "banked reads -- is untouched by this build.",
    "5. Not for or against situational-S.  The hypothesis stands whatever "
    "this module computes.  Program section 4 binds in full: no "
    "frustration<->exit identification (magnitude-conditional "
    "corpus-wide); nothing from the parked 256-family sweep; adjacency is "
    "not identification; the K4 occupancy fences carry -- this module is "
    "not 'an occupancy supplier exists' and not 'no occupancy supplier "
    "exists.'",
    "6. The j-parity <-> class(S_P) identification is NOT claimed and may "
    "not be constructed from this module's outputs by citation.  The S4 "
    "no-canonical-map genre bars it; CF5(d) records the absence.",
    "7. Not as a K1-UT scope renegotiation.  The 2026-08-13 ruling "
    "licenses READING counterfactual prices; it does not move where "
    "prices are PAID.  The FREE leg is untouched: pre-commit holding "
    "books zero.  Any citation of this module as weakening the FREE leg "
    "is a misuse.",
    "8. The CoDef family may not be cited via this module as 'a banked "
    "overlapping tie' or as a partial-overlap precedent.  It is "
    "support-identical, argmin-unique, and its equal-cost pairs are "
    "dominated (non-argmin).",
    "9. No identification of the CF1 family with any banked family.  "
    "Extension-candidate != hold-candidate-as-previously-banked != sep(P) "
    "edge != branch != the CoDef family.  The typing is a type "
    "assignment, not an identification.",
    "10. The module describes what it computes, never what it prevents -- "
    "no tamper-resistance claims, no 'cannot be re-aligned' sentences, no "
    "universals its legs did not compute.",
    "11. Executed values are values of authored witnesses.  No leg string "
    "or returned field may carry 'read not authored', 'per edge from the "
    "world', or equivalent phrasing about join values; the derived thing "
    "is the overlap PATTERN under the stated conditionals (CF1), nothing "
    "else.",
)

# ---------------------------------------------------------------------------
# The authored instance (disclosed, not discharged).
# ---------------------------------------------------------------------------

BASE_S = frozenset({('s', 0), ('s', 1), ('s', 2)})

# Pool: candidate anchors, deliberately including one anchor already in
# the base so the banked null-relabeling guard is exercised (CF1).
POOL = (('c', 0), ('c', 1), ('c', 2), ('c', 3), ('s', 0))

# Capacity: authored, expressed through the banked cost functional so
# the admissibility boundary is computed, never a literal figure:
# every single-anchor extension is admissible, every two-anchor
# extension is not (enforced in CF1).
CAPACITY_C = _hcd._cost(BASE_S) + _hcd.EPS

# Coupling instances (X-sourcing and base-anchoring: authored inputs).
X_COHELD = frozenset({('s', 0), ('s', 1), ('x', 0)})      # anchored in the base
X_ASYM = frozenset({('s', 0), ('c', 0)})                  # count-asymmetric
# The support-blindness pair: every count the tie machinery reads is
# pairwise equal between these two instances; the join differs.
X_JOIN_A = frozenset({('s', 0), ('c', 0), ('c', 1), ('x', 0)})
X_JOIN_B = frozenset({('s', 0), ('s', 1), ('x', 0), ('x', 1)})

EXPECTED_LEGS = {
    "check_CF1_candidate_family_construction": [
        "extension_type_facts_and_type_assignment",
        "family_constructed_a1_capacity_only",
        "named_premises_read_from_source_declarations",
        "null_relabeling_rejected_by_banked_guard",
        "pairwise_intersections_equal_base",
    ],
    "check_CF2_tie_by_value": [
        "coheld_chance_arm_at_positive_join",
        "counterfactual_increments_equal_by_value",
        "free_leg_consumed_as_typed",
        "genuine_tie_preconditions_by_value",
        "inclusion_exclusion_booking_form_on_overlaps",
        "increment_equals_level_difference_value_tie",
        "support_blindness_fixed_count_profile",
    ],
    "check_CF3_carrier_join_read": [
        "cycle_class_type_level_invariant",
        "join_values_computed_on_authored_instance",
        "join_varies_with_authored_X",
        "no_map_constructed_join_terminates",
    ],
    "check_CF4_falsifier_meeting": [
        "a_registration_shape_executed",
        "b_co_present_typing_gated_on_banked_hold_arc",
        "c_overlapping_configs_executed",
        "d_derivation_conditional_on_named_premises",
        "honest_form_scope_statements",
    ],
    "check_CF5_permanent_controls": [
        "a_disjoint_family_control",
        "b_codef_support_identical_control",
        "c_free_leg_consistency_control",
        "d_named_absence_census",
    ],
}


# ---------------------------------------------------------------------------
# result plumbing (append-and-record leg inventory, on the bank path)
# ---------------------------------------------------------------------------

def _result(name, legs, key_result, dependencies=(), cross_refs=(),
            disclosures=()):
    fails = []
    have = tuple(sorted(legs))
    want = tuple(EXPECTED_LEGS[name])
    if have != want:
        missing = sorted(set(want) - set(have))
        extra = sorted(set(have) - set(want))
        fails.append(
            f"leg inventory mismatch: missing={missing} extra={extra}")
    for label in sorted(legs):
        ok, ev = legs[label]
        if not ok:
            fails.append(f"{label}: {ev}")
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
        "conditional_on": [PREMISE_I_FJE,
                           PREMISE_II_K1UT + " (counterfactual reading "
                           "licensed per " + K1UT_READING_RULING + ")"],
        "authored_inputs": list(AUTHORED_INPUTS),
        "dependencies": list(dependencies),
        "cross_refs": list(cross_refs),
        "disclosures": list(disclosures),
        "may_not_cite": list(MAY_NOT_CITE),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": CLAIM_SURFACE_SHA256,
        "inventory_note": (
            "append-and-record (D7@2026-08-08): certifies a declared leg "
            "EXECUTED, not that it could have failed"),
    }


def _no_float(values):
    return all(isinstance(v, F) for v in values)


# ---------------------------------------------------------------------------
# shared machinery (banked records memoized so gate legs in different
# checks read the SAME live execution)
# ---------------------------------------------------------------------------

_MEMO = {}


def _banked(key):
    if key in _MEMO:
        return _MEMO[key]
    if key == "split":
        _MEMO[key] = _hcd.check_T_hold_cost_dominance_split()
    elif key == "codef":
        _MEMO[key] = _codef.check_L_codef_aggregation_argmin()
    elif key == "tie":
        _MEMO[key] = _ntr.check_T_nonlocal_tie_resolution()
    elif key == "partition":
        from apf.core import check_disjoint_partition
        _MEMO[key] = check_disjoint_partition()
    else:
        raise KeyError(key)
    return _MEMO[key]


def build_family(S=BASE_S, pool=POOL, C=CAPACITY_C):
    """CF1: the admissible single-anchor next-commits of S from the pool.

    Admissibility is the banked A1-capacity functional ONLY: count-only
    cost through hold_cost_dominance's own _cost, against the authored
    capacity C.  A pool anchor already inside S yields S u {a} == S,
    which is not an extension (and which the banked K1-UT guard itself
    rejects: a null relabeling is not a transition -- executed in CF1).
    """
    members = {}
    null_anchors = []
    inadmissible = []
    for a in pool:
        cfg = frozenset(S) | {a}
        if cfg == frozenset(S):
            null_anchors.append(a)
            continue
        if _hcd._cost(cfg) <= C:
            members[a] = cfg
        else:
            inadmissible.append(a)
    return members, null_anchors, inadmissible


def _pairs(members):
    anchors = sorted(members)
    out = []
    for i in range(len(anchors)):
        for j in range(i + 1, len(anchors)):
            out.append((anchors[i], anchors[j]))
    return out


def _ie_difference(cfg_u, cfg_v, X):
    """The inclusion-exclusion booking form on overlapping candidates:
    joint(u,X) - joint(v,X) as (|cfg_v & X| - |cfg_u & X|) * eps, on
    COMPUTED intersections (never the disjoint-witness parameter form)."""
    return (F(len(cfg_v & X)) - F(len(cfg_u & X))) * _ntr.EPS


def _counterfactual_price(S, cfg):
    """The K1-UT increment a candidate WOULD book, priced on its own
    ledger copy (counterfactual reading licensed per the 2026-08-13
    ruling named in K1UT_READING_RULING; the FREE leg is untouched --
    nothing here is booked into any shared world's ledger)."""
    L = _hcd._Ledger('counterfactual_copy')
    L.transition(S)          # the realized base: a committed realignment
    return L.transition(cfg)  # what THIS candidate would book


# ---------------------------------------------------------------------------
# CF1 -- the family construction
# ---------------------------------------------------------------------------

def check_CF1_candidate_family_construction():
    legs = {}

    # named premises tied by value to the banked modules' own declarations
    ok = (PREMISE_I_FJE in _cc._FINITE_BASIS_GENERAL_OPEN_OBLIGATIONS and
          PREMISE_II_K1UT in _hcd.HOLD_EXEMPTION_BUNDLE and
          _hcd.EPS > 0 and _ntr.EPS > 0)
    legs["named_premises_read_from_source_declarations"] = (ok, (
        f"premise (i) '{PREMISE_I_FJE}' read from continuation_calculus's "
        f"own open-obligation tuple; premise (ii) '{PREMISE_II_K1UT}' read "
        f"from hold_cost_dominance's own HOLD_EXEMPTION_BUNDLE; both "
        f"consumed as NAMES (constructed nowhere here); eps > 0 the only "
        f"inequality imported"))

    members, null_anchors, inadmissible = build_family()
    n_expected = len([a for a in POOL if a not in BASE_S])
    two_anchor = frozenset(BASE_S) | {('c', 0), ('c', 1)}
    ok = (len(members) == n_expected and len(inadmissible) == 0 and
          all(_hcd._cost(cfg) <= CAPACITY_C for cfg in members.values()) and
          _hcd._cost(two_anchor) > CAPACITY_C)
    legs["family_constructed_a1_capacity_only"] = (ok, (
        f"family of {len(members)} admissible single-anchor next-commits "
        f"constructed from a pool of {len(POOL)} over a base of "
        f"|S| = {len(BASE_S)}; admissibility is the banked A1-capacity "
        f"functional only (hold_cost_dominance._cost <= C, authored C); "
        f"the functional bites: a two-anchor extension is inadmissible at "
        f"the same C (cost {_hcd._cost(two_anchor)} > C {CAPACITY_C})"))

    # the banked K1-UT guard itself rejects the null relabeling
    guard_fired = False
    L = _hcd._Ledger('null_relabel_control')
    L.transition(BASE_S)
    try:
        L.transition(frozenset(BASE_S) | {null_anchors[0]})
    except ValueError:
        guard_fired = True
    ok = (len(null_anchors) == 1 and guard_fired)
    legs["null_relabeling_rejected_by_banked_guard"] = (ok, (
        f"{len(null_anchors)} pool anchor(s) already in S excluded by the "
        f"extension type, and the banked machinery agrees: "
        f"_Ledger.transition raises on the null relabeling (K1-UT's own "
        f"guard, executed)"))

    pairs = _pairs(members)
    n = len(members)
    ok = (len(pairs) == n * (n - 1) // 2 and
          all(members[u] & members[v] == BASE_S for (u, v) in pairs))
    legs["pairwise_intersections_equal_base"] = (ok, (
        f"all {len(pairs)} pairwise support intersections COMPUTED from "
        f"the constructed members and each equal to S, the whole retained "
        f"base (|S| = {len(BASE_S)}); no intersection is written in by "
        f"hand -- the overlap pattern is set theory executed on the "
        f"extension type, GIVEN the named premises and the authored "
        f"inputs"))

    ok = (all(cfg > BASE_S and len(cfg) == len(BASE_S) + 1
              for cfg in members.values()) and
          len(set(members.values())) == len(members) and
          _no_float([CAPACITY_C, _hcd._cost(BASE_S)]))
    legs["extension_type_facts_and_type_assignment"] = (ok, (
        f"every member is a strict single-anchor superset of S and the "
        f"{len(members)} members are pairwise distinct; the family is "
        f"TYPED as one hold's candidate family (co-present pre-commit "
        f"alternatives, of which at most one will commit) -- a TYPE "
        f"assignment in the hold arc's vocabulary, NOT an identification "
        f"(extension-candidate != hold-candidate-as-banked != sep(P) edge "
        f"!= branch); joint existence of the co-present family consumed "
        f"under the named premise '{PREMISE_I_FJE}'"))

    return _result(
        "check_CF1_candidate_family_construction", legs,
        key_result=(
            f"GIVEN the two named premises and the authored inputs: the "
            f"{len(members)}-member admissible single-anchor next-commit "
            f"family of the authored base S is constructed under the "
            f"banked A1-capacity functional only, typed (type assignment) "
            f"as one hold's candidate family, and every one of its "
            f"{len(pairs)} pairwise support intersections is COMPUTED "
            f"equal to S -- the overlap pattern is derived from the "
            f"extension type, not authored per witness"),
        dependencies=["A1", "T_hold_cost_dominance_split"],
        cross_refs=["L_mechanism_trichotomy", "T_nonlocal_tie_resolution"],
        disclosures=[
            "S, pool, and C are authored inputs (disclosed, not "
            "discharged)",
            "the family's joint existence as co-present admissible "
            "extensions is consumed under premise (i), not derived"])


# ---------------------------------------------------------------------------
# CF2 -- the tie
# ---------------------------------------------------------------------------

# INHERITED RED (E1@2026-08-28: sub-lemma L_cost_C1 of check_L_cost
# demoted off 'P' to a POSTULATE).  THIS CHECK HOLDS NO VIEW ABOUT
# L_cost_C1: it reddens because its proximate anchor reddened, and that
# anchor is check_T_nonlocal_tie_resolution (nonlocal_tie_resolution.py).
# The leg that reads C1's status literal is in
# check_L_selection_ledger_completeness (born_at_ties.py); this red is
# inherited from it, and a reader who counts it as a separate finding
# over-counts the corpus's damage.
# NOT to be widened, tuned green, or reverted: the predicate is
# satisfiable and clears when C1 is discharged or the anchor's
# predicate is ruled.
def check_CF2_tie_by_value():
    legs = {}
    members, _, _ = build_family()
    anchors = sorted(members)
    u, v = anchors[0], anchors[1]
    cfg_u, cfg_v = members[u], members[v]

    # counterfactual increments, each on its own ledger copy
    prices = {a: _counterfactual_price(BASE_S, members[a]) for a in anchors}
    vals = set(prices.values())
    ok = (len(vals) == 1 and
          vals == {F(1) * _hcd.EPS} and
          _no_float(list(prices.values())))
    legs["counterfactual_increments_equal_by_value"] = (ok, (
        f"all {len(prices)} candidates book the SAME K1-UT increment "
        f"{sorted(vals)[0] if len(vals) == 1 else sorted(vals)} through "
        f"hold_cost_dominance's own _Ledger.transition, each priced on "
        f"its own ledger copy under the licensed counterfactual reading "
        f"({K1UT_READING_RULING}); equal computed Fractions, never an "
        f"authored equality of literals"))

    ok = all(prices[a] == _hcd._cost(members[a]) - _hcd._cost(BASE_S)
             for a in anchors)
    legs["increment_equals_level_difference_value_tie"] = (ok, (
        f"value tie, two computations one quantity: for every candidate "
        f"the transition booking |S delta S'|*eps equals the level "
        f"difference _cost(cfg) - _cost(S), both through the banked "
        f"module's own functions, as exact Fractions"))

    r_tie = _banked("tie")
    ok = (r_tie.get("passed") is True and
          _ntr._cost(cfg_u) == _ntr._cost(cfg_v) and
          cfg_u != cfg_v and
          _no_float([_ntr._cost(cfg_u), _ntr._cost(cfg_v)]))
    legs["genuine_tie_preconditions_by_value"] = (ok, (
        f"the banked tie check runs green live, and the genuine-tie "
        f"preconditions pass BY VALUE through its own predicates: "
        f"_cost(cfg_u) == _cost(cfg_v) == {_ntr._cost(cfg_u)} as computed "
        f"Fractions, cfg_u != cfg_v"))

    j_uv = len(cfg_u & cfg_v & X_COHELD)
    ju, jv = _ntr._joint(cfg_u, X_COHELD), _ntr._joint(cfg_v, X_COHELD)
    ja_u, ja_v = _ntr._joint(cfg_u, X_ASYM), _ntr._joint(cfg_v, X_ASYM)
    ok = (X_COHELD & BASE_S != frozenset() and       # X anchored in the base
          len(cfg_u & X_COHELD) == len(cfg_v & X_COHELD) and
          ju == jv and                               # co-held: chance arm
          j_uv > 0 and
          j_uv == len(BASE_S & X_COHELD) and         # value tie, second route
          len(cfg_u & X_ASYM) != len(cfg_v & X_ASYM) and
          ja_u != ja_v)                              # asymmetric: decided
    legs["coheld_chance_arm_at_positive_join"] = (ok, (
        f"executed co-held instance: X anchored in the base (authored "
        f"X-sourcing) is count-symmetric (shares "
        f"{len(cfg_u & X_COHELD)} with each candidate), the coupled "
        f"costs through the banked _joint are EQUAL ({ju} == {jv}) so "
        f"the tie SURVIVES -- co-held, the born_at_ties chance arm "
        f"governs -- at NONZERO pairwise join j_uv = {j_uv}, tied by "
        f"value to |S & X| = {len(BASE_S & X_COHELD)} computed through "
        f"the base (a second route, independent of the pairwise "
        f"computation); the "
        f"count-asymmetric control X is decided ({ja_u} != {ja_v}), "
        f"exercising both arms of the banked conditional"))

    # the inclusion-exclusion booking form, on computed intersections
    sweep = [X_COHELD, X_ASYM, X_JOIN_A, X_JOIN_B]
    ok = all(_ntr._joint(cfg_u, X) - _ntr._joint(cfg_v, X)
             == _ie_difference(cfg_u, cfg_v, X) for X in sweep)
    ok = ok and len(sweep) == 4
    legs["inclusion_exclusion_booking_form_on_overlaps"] = (ok, (
        f"on the overlapping pair, the joint-cost difference equals the "
        f"inclusion-exclusion form (|cfg_v & X| - |cfg_u & X|) * eps on "
        f"COMPUTED intersections, verified as Fraction equalities over "
        f"{len(sweep)} coupling instances -- given the members' equal "
        f"size this is an algebraic identity of the count-only cost, "
        f"both sides computed through the banked functions, and the "
        f"count-asymmetric instance decides the sign -- (the scoping "
        f"return's Leg-2 "
        f"rider, carried as a build requirement: intersections, never "
        f"the disjoint-witness constructor parameters, are the "
        f"bookkeeping on overlapping candidates)"))

    # support-blindness: full count-profile equal, join moves
    jA = len(cfg_u & cfg_v & X_JOIN_A)
    jB = len(cfg_u & cfg_v & X_JOIN_B)
    profile_equal = (
        _ntr._cost(X_JOIN_A) == _ntr._cost(X_JOIN_B) and
        _ntr._joint(cfg_u, X_JOIN_A) == _ntr._joint(cfg_u, X_JOIN_B) and
        _ntr._joint(cfg_v, X_JOIN_A) == _ntr._joint(cfg_v, X_JOIN_B) and
        _ntr._deficit(cfg_u, X_JOIN_A) == _ntr._deficit(cfg_u, X_JOIN_B) and
        _ntr._deficit(cfg_v, X_JOIN_A) == _ntr._deficit(cfg_v, X_JOIN_B))
    coheld_A = (_ntr._joint(cfg_u, X_JOIN_A) == _ntr._joint(cfg_v, X_JOIN_A))
    coheld_B = (_ntr._joint(cfg_u, X_JOIN_B) == _ntr._joint(cfg_v, X_JOIN_B))
    ok = (profile_equal and coheld_A and coheld_B and jA != jB and
          jA == len(BASE_S & X_JOIN_A) and           # value ties, second route
          jB == len(BASE_S & X_JOIN_B))
    legs["support_blindness_fixed_count_profile"] = (ok, (
        f"the tie predicate reads counts only (the banked _cost is "
        f"|S|*eps, identity-blind): two instances with the banked tie "
        f"module's three count functionals (_cost, _joint, _deficit) "
        f"evaluated pairwise equal (as Fractions, on X and on both "
        f"candidates) carry DIFFERENT joins j_uv = {jA} vs {jB}, each "
        f"tied by value to |S & X| computed through the base ("
        f"{len(BASE_S & X_JOIN_A)} and {len(BASE_S & X_JOIN_B)}); the "
        f"tie verdict (co-held in both) is unmoved while j_uv moves"))

    hold = _hcd._Ledger('the_hold_pre_commit')
    ok = (hold.throughput == F(0) and hold.level() == F(0) and
          hold.history == [])
    legs["free_leg_consumed_as_typed"] = (ok, (
        f"the FREE leg consumed as typed: pre-commit holding books ZERO "
        f"(throughput {hold.throughput}, level {hold.level()}, empty "
        f"history, through the hold arc's own ledger) -- a consumption "
        f"record of the banked constructor's initial state, disclosed "
        f"as a record; the tie is "
        f"between counterfactual prices, not between paid bookings "
        f"(CF5(c) is the executed control)"))

    return _result(
        "check_CF2_tie_by_value", legs,
        key_result=(
            f"GIVEN the two named premises and the authored inputs: two "
            f"distinct family members book equal K1-UT increments BY "
            f"VALUE through the banked ledger (each on its own copy, "
            f"counterfactual reading licensed per {K1UT_READING_RULING}), "
            f"pass the banked genuine-tie preconditions by value, and "
            f"the tie survives co-held (chance arm) at j_uv = {j_uv} > 0 "
            f"under a base-anchored authored X; the tie predicate is "
            f"support-blind (verdict unmoved while j_uv moves under an "
            f"equal count-profile); bookings on overlaps are the "
            f"inclusion-exclusion form on computed intersections"),
        dependencies=["T_hold_cost_dominance_split",
                      "T_nonlocal_tie_resolution",
                      "L_codef_aggregation_argmin"],
        cross_refs=["L_selection_ledger_completeness"],
        disclosures=[
            "X-sourcing and base-anchoring are authored inputs",
            "equal-increment is a consequence of the banked count-only "
            "pricing applied to equal-size single-anchor extensions -- "
            "stated as that consequence, executed, not as a discovery "
            "about nature"])


# ---------------------------------------------------------------------------
# CF3 -- the carrier read
# ---------------------------------------------------------------------------

def check_CF3_carrier_join_read():
    legs = {}
    members, _, _ = build_family()
    pairs = _pairs(members)

    joins = {(u, v): len(members[u] & members[v] & X_COHELD)
             for (u, v) in pairs}
    ok = (len(joins) == len(pairs) and
          all(j == len(BASE_S & X_COHELD) for j in joins.values()) and
          all(j > 0 for j in joins.values()))
    legs["join_values_computed_on_authored_instance"] = (ok, (
        f"j_uv computed on the constructed (authored) instance for all "
        f"{len(joins)} pairs; every value equals |S & X| = "
        f"{len(BASE_S & X_COHELD)} (the join lives on the derived "
        f"overlap, which is S, wherever the authored X meets the base); "
        f"values of authored witnesses, reported as data of this "
        f"instance"))

    X_alt = frozenset({('s', 0), ('x', 0)})
    j_alt = len(members[sorted(members)[0]] & members[sorted(members)[1]]
                & X_alt)
    j_orig = joins[pairs[0]]
    ok = (j_alt != j_orig)
    legs["join_varies_with_authored_X"] = (ok, (
        f"the join values inherit the authoredness of X, exhibited "
        f"computationally: moving the authored X moves the join "
        f"({j_orig} -> {j_alt}); the derived thing is the overlap "
        f"PATTERN (CF1), never the join values"))

    a0, a1, a2 = sorted(members)[:3]
    cycle = [(a0, a1), (a1, a2), (a0, a2)]
    parities = [(-1) ** joins[p] for p in cycle]
    prod = parities[0] * parities[1] * parities[2]
    # value pin (second route): every join on this instance equals
    # |S & X| (tied in the leg above), so the cycle class is
    # (-1)^(3*|S & X|), computed from the authored base and X rather
    # than from the joins dict the parities were read from
    expect_pinned = (-1) ** (3 * len(BASE_S & X_COHELD))
    ok = (prod == expect_pinned)
    legs["cycle_class_type_level_invariant"] = (ok, (
        f"the parity class of the join pattern along the 3-cycle is "
        f"computed as a type-level invariant of this constructed "
        f"instance (cycle product {prod}, a Z2 value, pinned to its "
        f"expected value {expect_pinned} = (-1)^(3*|S & X|) computed "
        f"from the authored base and X); the "
        f"switching-class vocabulary is a NAMED import of classical "
        f"content (Zaslavsky-genre); a type-level fact of an authored "
        f"witness, nothing more"))

    ok = True and len(pairs) > 0
    legs["no_map_constructed_join_terminates"] = (ok, (
        f"record (disclosed as a record): no map from the join data to "
        f"any target datum is constructed here -- the S4 "
        f"no-canonical-map genre bars that identification and CF5(d) "
        f"records the absence; the {len(joins)} join values terminate in "
        f"this returned record"))

    return _result(
        "check_CF3_carrier_join_read", legs,
        key_result=(
            f"the pairwise join j_uv on the constructed family is "
            f"computed and reported as a datum of the authored instance "
            f"(all {len(joins)} pairs; nonzero wherever the authored X "
            f"meets the base); the cycle parity class is a computed "
            f"type-level invariant; NO supply claim -- the join values "
            f"inherit the authoredness of X, and no map from join data "
            f"to any target datum exists here"),
        dependencies=["A1"],
        cross_refs=["T_nonlocal_tie_resolution"],
        disclosures=[
            "the switching-class vocabulary is a named import of "
            "classical content (Zaslavsky-genre)",
            "the no_map leg is a record, not a measurement"])


# ---------------------------------------------------------------------------
# CF4 -- the falsifier meeting
# ---------------------------------------------------------------------------

def check_CF4_falsifier_meeting():
    legs = {}
    members, _, _ = build_family()
    pairs = _pairs(members)

    fresh = {}
    register(fresh)
    expected_keys = {name[len("check_"):] for name in EXPECTED_LEGS}
    ok = (set(fresh) == expected_keys and
          "CF1_candidate_family_construction" in fresh)
    legs["a_registration_shape_executed"] = (ok, (
        f"falsifier clause (a): registration shape executed on a fresh "
        f"registry -- {len(fresh)} checks under bare-name keys "
        f"(D6@2026-08-03), the family constructor among them; this is a "
        f"build-seat scratch object wired into no live bank, so the "
        f"banked clause is met in full only at landing (disclosed "
        f"weakening W1)"))

    r_split = _banked("split")
    hold = _hcd._Ledger('cf4_hold_pre_commit')
    ok = (r_split.get("passed") is True and
          r_split.get("epistemic", "").startswith("P_structural") and
          hold.throughput == F(0) and hold.history == [])
    legs["b_co_present_typing_gated_on_banked_hold_arc"] = (ok, (
        f"falsifier clause (b): the family is typed as ONE hold's "
        f"co-present pre-commit alternatives -- the type source, the "
        f"banked hold-arc split check, runs green live "
        f"(epistemic '{r_split.get('epistemic', '')[:24]}...'), and the "
        f"FREE leg's zero pre-commit booking is computed on the hold "
        f"arc's own ledger (a consumption record of the constructor's "
        f"initial state); a type assignment, not an identification"))

    ok = (len(pairs) > 0 and
          all(members[u] & members[v] == BASE_S for (u, v) in pairs) and
          len(BASE_S) > 0)
    legs["c_overlapping_configs_executed"] = (ok, (
        f"falsifier clause (c): every one of the {len(pairs)} pairs "
        f"intersects on the nonempty base S (|S| = {len(BASE_S)}), "
        f"executed"))

    u, v = sorted(members)[:2]
    price_u = _counterfactual_price(BASE_S, members[u])
    price_v = _counterfactual_price(BASE_S, members[v])
    ok = (members[u] & members[v] == BASE_S and price_u == price_v)
    legs["d_derivation_conditional_on_named_premises"] = (ok, (
        f"falsifier clause (d): the overlap pattern is DERIVED from "
        f"banked transition structure -- the extension type (the "
        f"intersection recomputed here from the constructed members) "
        f"plus the K1-UT increment pricing (equal counterfactual prices "
        f"{price_u} == {price_v} through the banked ledger, reading "
        f"licensed per {K1UT_READING_RULING}) -- rather than authored "
        f"per witness.  DERIVED means: derived GIVEN the two named "
        f"premises ('{PREMISE_I_FJE}' + '{PREMISE_II_K1UT}') and the "
        f"authored inputs (S, pool, X, base-anchoring, C).  The "
        f"falsifier is met on its own terms at that conditional "
        f"strength and no other"))

    r_part = _banked("partition")
    scope_statements = (
        "(i) the deflationary rival is untouched: 'overlap may be real "
        "only where nothing banked can ever read' survives this build",
        "(ii) the read channel is not opened: the record-exhaustion "
        "premises (R-sel-LC / R-event-model, born_at_ties) are "
        "unrenegotiated, and nothing here claims the dynamics read j_uv "
        "or any pre-commit pairwise datum",
        "(iii) the stage-split verdict stands with both halves carrying "
        "their stage: disjointness FORCED at the realized/committed "
        f"stage (check_disjoint_partition, epistemic "
        f"{r_part.get('epistemic')!r} consumed from the live record "
        f"fetched here rather than stated, integrality-witnessed, passed "
        f"gated green live here; the partition argued in the check's own "
        f"proof text; record-resolution orthogonality a named input) and "
        f"UNFORCED at "
        f"the pre-commit candidate stage -- the stage-split verdict does "
        f"not depend on which grade that is; this leg requires of that "
        f"field only that it be present and a non-empty string, and the "
        f"grade is carried as a datum")
    ok = (r_part.get("passed") is True
          and isinstance(r_part.get("epistemic"), str)
          and r_part.get("epistemic") != "")
    legs["honest_form_scope_statements"] = (ok, (
        "the honest form, in-module (records, disclosed as records, "
        "with the forced half's banked anchor gated live): "
        + " | ".join(scope_statements)))

    return _result(
        "check_CF4_falsifier_meeting", legs,
        key_result=(
            f"the Arm-2a falsifier condition -- quoted verbatim: "
            f"\"{FALSIFIER_ARM_2A}\" -- is met at conditional strength: "
            f"the CF1 family is registry-shaped (banked in full at "
            f"landing), co-present (typed as one hold's pre-commit "
            f"alternatives), overlapping (all {len(pairs)} pairs "
            f"intersect on S, executed), and its overlap pattern is "
            f"derived from banked transition structure GIVEN the two "
            f"named premises and the authored inputs -- and no other "
            f"strength; scope statements (i)-(iii) carried"),
        dependencies=["T_hold_cost_dominance_split", "disjoint_partition"],
        cross_refs=["T_nonlocal_tie_resolution",
                    "L_codef_aggregation_argmin"],
        disclosures=[
            "the falsifier text is an external quotation, not "
            "re-derived",
            "clause (a) executed as registration shape (weakening W1, "
            "disclosed)"])


# ---------------------------------------------------------------------------
# CF5 -- the permanent controls (K5/G5 import-control genre)
# ---------------------------------------------------------------------------

def check_CF5_permanent_controls():
    legs = {}

    # (a) the disjoint-family control
    A, B = _ntr._local_tie(2)
    A3, B3 = _ntr._local_tie(3)
    ok = (A & B == frozenset() and A3 & B3 == frozenset() and
          _ntr._cost(A) == _ntr._cost(B) and A != B)
    legs["a_disjoint_family_control"] = (ok, (
        f"the banked _local_tie families remain DISJOINT label-scheme "
        f"constructions (rebuilt through the banked module's own "
        f"constructor; intersections empty, executed); that disjointness "
        f"was CONVENIENT -- a constructor's label scheme -- not premised "
        f"and not wrong; nothing in this module retro-types those "
        f"witnesses as overlapping or re-claims them (the stage-split's "
        f"own terms: forced at the realized stage, unforced at the "
        f"pre-commit candidate stage, both halves in one sentence)"))

    # (b) the CoDef non-identity control
    r_codef = _banked("codef")
    Ma, Mb = frozenset({0, 1}), frozenset({1, 5})
    union = sorted(Ma | Mb)
    eps_joint = _codef._cost(frozenset(union))
    from itertools import product as _product
    fam = list(_product((1, 2), repeat=len(union)))
    supports = [frozenset(d for d, m in zip(union, mvec) if m >= 1)
                for mvec in fam]
    n_pairs = 0
    support_identical = True
    for i in range(len(fam)):
        for j in range(i + 1, len(fam)):
            n_pairs += 1
            if supports[i] != supports[j]:
                support_identical = False
    bills = {mvec: sum(F(m) * _codef._COSTS[d]
                       for d, m in zip(union, mvec)) for mvec in fam}
    engage_once = tuple(1 for _ in union)
    argmin_unique = (bills[engage_once] == eps_joint and
                     all(b > eps_joint for m, b in bills.items()
                         if m != engage_once))
    ok = (r_codef.get("passed") is True and
          r_codef.get("epistemic") == "P" and
          all(s == frozenset(union) for s in supports) and
          support_identical and
          n_pairs == len(fam) * (len(fam) - 1) // 2 and
          argmin_unique)
    legs["b_codef_support_identical_control"] = (ok, (
        f"the banked covering-engagement family (codef, gated green "
        f"live at [P]) is SUPPORT-IDENTICAL, not partially overlapping: "
        f"all {len(fam)} members' supports equal the union exactly "
        f"(re-verified through the banked module's own cost map; all "
        f"{n_pairs} pairs degenerate), the family varies in "
        f"multiplicity, never in support extent -- the degenerate "
        f"total-overlap extreme, a TYPE precedent for shared-support "
        f"co-presence at [P]; and its argmin is unique on the executed "
        f"pair (engage-once; every other member strictly dominated, "
        f"executed -- the equality-iff-engage-once generality is the "
        f"banked module's own Leg 3), so it cannot tie at the argmin"))

    # (c) the FREE-leg consistency control
    members, _, _ = build_family()
    hold = _hcd._Ledger('cf5_hold_pre_commit')
    prices = {a: _counterfactual_price(BASE_S, members[a])
              for a in sorted(members)}
    two_anchor = frozenset(BASE_S) | {('c', 0), ('c', 1)}
    price_two = _counterfactual_price(BASE_S, two_anchor)
    ok = (hold.level() == F(0) and
          hold.history == [] and
          all(p > 0 for p in prices.values()) and
          price_two != sorted(prices.values())[0] and
          hold.throughput == F(0))     # zero after all pricing
    legs["c_free_leg_consistency_control"] = (ok, (
        f"both quantities exhibited as DIFFERENT quantities in one "
        f"executed leg: the hold's pre-commit booking is ZERO (the FREE "
        f"leg, read from the hold arc's own ledger machinery -- "
        f"throughput {hold.throughput}, empty history, unchanged after "
        f"all pricing) while the counterfactual K1-UT increment prices "
        f"are NONZERO (family members at {sorted(set(prices.values()))}, "
        f"a non-tied two-anchor extension at {price_two}), each on its "
        f"own ledger copy ({K1UT_READING_RULING}); reading a price is "
        f"not paying one -- no leg of this module books a pre-commit "
        f"cost into any world's ledger"))

    # (d) the named-absence census
    import apf as _apf
    apf_dir = os.path.dirname(os.path.abspath(_apf.__file__))
    token = "j_uv"
    control_token = "def check_"   # known-present token: positive control
    hits = []
    n_control_hits = 0
    n_scanned = 0
    n_unreadable = 0
    for fn in sorted(os.listdir(apf_dir)):
        if not fn.endswith(".py") or fn == "candidate_family_overlap.py":
            continue
        path = os.path.join(apf_dir, fn)
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                src = fh.read()
        except OSError:
            n_unreadable += 1
            continue
        n_scanned += 1
        if token in src:
            hits.append(fn)
        if control_token in src:
            n_control_hits += 1
    ok = (n_scanned > 0 and hits == [] and n_control_hits > 0 and
          n_unreadable == 0)
    legs["d_named_absence_census"] = (ok, (
        f"census-conditioned negative at the pin: an exact-token source "
        f"scan of the apf package directory ({n_scanned} .py files, "
        f"token '{token}', this module excluded by its landing "
        f"filename) finds {len(hits)} "
        f"carriers of the token (gated: zero required); positive "
        f"control executed in the same "
        f"scan: the control token '{control_token}' is found in "
        f"{n_control_hits} files, so the scanner reads sources and can "
        f"report presence; {n_unreadable} files unreadable (gated: the "
        f"negative is certified only over files actually read); census "
        f"scope: exact token, source text, top-level apf dir; a consumer "
        f"under a different name, or a re-pointed token constant, is "
        f"outside this census's reach (stated "
        f"limitation; the wider pairwise-consumption negative is the "
        f"adversarial seat's Arm-1 census, prior art, not re-executed).  "
        f"This module computes j_uv and feeds it NOWHERE -- the value "
        f"terminates in the returned record; the read-channel quarantine "
        f"(Arm-3) stands unopened by this module"))

    return _result(
        "check_CF5_permanent_controls", legs,
        key_result=(
            "four permanent controls executed: (a) the banked tie-arc "
            "witnesses stay disjoint by their own constructor (label "
            "scheme, convenient, not premised, not re-claimed); (b) the "
            "banked CoDef family is support-identical and argmin-unique "
            "(not a partial-overlap precedent); (c) the FREE leg's zero "
            "pre-commit booking and the nonzero counterfactual prices "
            "are different quantities, and nothing here pays a "
            "pre-commit cost; (d) at the pin no banked module carries "
            "the join token (exact-token census, scope stated) and this "
            "module's join value terminates in its own record"),
        dependencies=["L_codef_aggregation_argmin",
                      "T_nonlocal_tie_resolution",
                      "T_hold_cost_dominance_split"],
        cross_refs=["K5_import_controls",
                    "G5_sign_and_nonidentity_controls"],
        disclosures=[
            "the census is exact-token and directory-scoped; its "
            "limitation is stated in the leg",
            "the four absences these controls record may not be "
            "converted to presences by any successor's wording (frozen "
            "surface F5 scope)"])


# ---------------------------------------------------------------------------
# registration (bare-name keys per D6@2026-08-03; wired into the live
# bank at v24.3.475: manifest entry, EXPECTED 4178 -> 4183)
# ---------------------------------------------------------------------------

_CHECKS = {
    "check_CF1_candidate_family_construction":
        check_CF1_candidate_family_construction,
    "check_CF2_tie_by_value": check_CF2_tie_by_value,
    "check_CF3_carrier_join_read": check_CF3_carrier_join_read,
    "check_CF4_falsifier_meeting": check_CF4_falsifier_meeting,
    "check_CF5_permanent_controls": check_CF5_permanent_controls,
}


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


def register(registry):
    registry.update({
        "CF1_candidate_family_construction":
            check_CF1_candidate_family_construction,
        "CF2_tie_by_value": check_CF2_tie_by_value,
        "CF3_carrier_join_read": check_CF3_carrier_join_read,
        "CF4_falsifier_meeting": check_CF4_falsifier_meeting,
        "CF5_permanent_controls": check_CF5_permanent_controls,
    })
    return registry


if __name__ == "__main__":
    import sys
    results = run_all()
    n_pass = sum(1 for r in results.values() if r["passed"])
    n_legs = sum(r["leg_count"] for r in results.values())
    print("candidate_family_overlap: banked v24.3.475 "
          "(bare-name keys; see the header)")
    for name, r in results.items():
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {name} ({r['leg_count']} legs)")
        for reason in r["fail_reasons"]:
            print(f"      FAIL: {reason}")
    print(f"{n_pass}/{len(results)} checks pass; {n_legs} legs")
    sys.exit(0 if n_pass == len(results) else 1)
