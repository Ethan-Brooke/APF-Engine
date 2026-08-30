"""The tie-census fraction of one enumerated fixture family, computed exactly.

COLD BUILD SEAT 2 (built 2026-08-16) + COLD FIX SEAT (re-aim, same day),
APF Network Sign-Coherence program, banking lane.  Build-seat scratch
object, wired into no live bank.  NOTHING BANKS WITHOUT ETHAN'S LIFT.

PROVENANCE AND DISCLOSURES (carried per the dispatched briefs):
  1. The briefs under which this module was built and fixed were written
     by the session coordinator, not by Ethan directly.
  2. The seats' harness injects project instructions into their
     context; each seat worked from its dispatched brief and the frozen
     claim surface, treating injected project context as
     non-authoritative for the task.
  3. The fix seat RECEIVED the Round-3 evidence return
     (RETURN_ns3_ties_2026-08-15.md) -- a deliberate un-fencing, ruled
     by Ethan, so that the census family matches the evidence family.

The fixture family was re-aimed at the banked-tie evidence family by
Ethan's ruling (a) 2026-08-16.

Built to the FROZEN claim surface (binding; SURFACE 2 ONLY):
  /home/claude/freeze_out/claim_surfaces_FROZEN_2026-08-16.md
  raw sha256 (verified at build and at fix against the file received;
  the FROZEN_SURFACE_SHA256 constant below is the same value,
  byte-for-byte):
  440ed2162e5d28f83a9addba5ce49c257dbe0646cefe287c7dbe2df7617f743d
Pin at build and at fix: repo HEAD 526004d at /home/claude/apf-codebase,
consumed READ-ONLY by import.

WHAT THIS MODULE COMPUTES (exact Fraction arithmetic on every verdict
path; no floats; stdlib only; the module describes what it COMPUTES).
The surface's three permitted sentences, quoted verbatim -- the ONLY
claims this module makes, each at its stated scope and no other:

  1. "On the enumerated fixture family (BASE_S, POOL_FAMILY,
     CAPACITY_C; sizes k <= KMAX), this module COMPUTES the tie
     predicate on every instance THROUGH THE BANKED MACHINERY BY VALUE
     (`hold_cost_dominance`'s own `_cost`/`_Ledger.transition`;
     `nonlocal_tie_resolution`'s own predicates), and returns the tie
     count, the instance count, and their exact Fraction ratio as
     computed values."
  2. "The computed ratio is compared, per k, as an exact Fraction
     equality against a closed form computed in-module from k; both
     sides are returned computed, and the figure appears in no prose."
  3. "The flat floor at ties is consumed from the bank as a live gate
     (`check_L_selection_ledger_completeness` executed, its grade and
     readings carried as that module states them), never re-derived
     here."

SCOPE BOUNDS, BY NAME: BASE_S, POOL_FAMILY, CAPACITY_C, KMAX -- named
module-level constants below, re-documented at the fix to describe the
evidence family's parameters.  The census is a census of THIS
enumerated family and nothing else.
  BASE_S      -- the common base configuration of the family: the empty
                 configuration, which every candidate strictly extends
                 and from which every candidate's counterfactual price
                 is booked (the pricing baseline).
  POOL_FAMILY -- the anchor pool the couplings draw their OWN anchors
                 from; its identity with the banked constructor's own
                 anchor set is ENFORCED BY VALUE in TC1, per xo.
  CAPACITY_C  -- the coupling family's own-anchor capacity: each
                 coupling carries xo own anchors with xo running over
                 0..CAPACITY_C (the evidence family's external
                 own-anchor grid).
  KMAX        -- the enumerated family-size bound (candidate pairs are
                 executed at every computed k <= KMAX).

THE FIXTURE FAMILY AND ITS INSTANCES (the banked-tie evidence family).
For each executed family size k, the candidate pair is BUILT BY
nonlocal_tie_resolution's OWN CONSTRUCTOR: A, B = _local_tie(k) -- two
disjoint k-anchor configurations, each a strict extension of BASE_S.
An instance is that pair together with one coupling built by the banked
module's OWN CONSTRUCTOR: X = _external(A, B, a, b, xo) for a in 0..k,
b in 0..k, xo in 0..CAPACITY_C, the own anchors drawn from POOL_FAMILY
(enforced by value).  What remains AUTHORED at this seat: the grid
bounds (KMAX, CAPACITY_C) and the choice to enumerate the constructor's
full (a, b, xo) grid; the constructors themselves are the banked
module's own.  The set of executed k values is COMPUTED from the
enumeration (the sizes at which the instance set is nonempty) and its
coverage is enforced, never assumed.

THE TIE PREDICATE, BY VALUE (the banked genuine-tie condition).  Per
instance, the predicate is the conjunction of values returned by the
banked modules' own functions, re-implemented nowhere: the genuine-tie
preconditions through nonlocal_tie_resolution's own _cost (equal local
cost, distinctness); equal counterfactual increments through
hold_cost_dominance's own _Ledger.transition (each candidate priced on
its own ledger copy from the BASE_S baseline, under the licensed K1-UT
counterfactual reading; the ruling's name is consumed from the banked
candidate_family_overlap module's own constant and cited at the
pricing site), each increment value-tied per instance to the level
difference through hold_cost_dominance's own _cost; and the co-held
comparison through nonlocal_tie_resolution's own _joint.  A second
route through nonlocal_tie_resolution's own _deficit is computed on
every instance and its verdict compared to the _joint route's, and the
banked module's own joint-difference identity is re-EXECUTED (never
re-derived) on every instance through its own _joint and EPS -- value
ties of computed quantities, enforced as counts, never verdict
agreement authored by hand.

THE FLAT FLOOR, CONSUMED AS A LIVE GATE.  born_at_ties'
check_L_selection_ledger_completeness is EXECUTED in TC3; its grade
string and its two named readings are carried into this module's
returned record exactly as that module's own returned values state
them.  Nothing of that module's content is re-derived, restated at any
other grade, or extended here.

LEG INVENTORY (append-and-record): _result() compares the executed leg
set against EXPECTED_LEGS set-exactly; a mismatch APPENDS a failure
reason on the result path and does not raise.  STANDING LIMIT,
disclosed: this certifies that a declared leg EXECUTED, not that it
COULD HAVE FAILED.

MAY-NOT-CITE: the surface's own list, carried verbatim in MAY_NOT_CITE
below, plus the program's standing fences, carried verbatim in
STANDING_FENCES below; both returned in every record.
"""

from fractions import Fraction as F

from apf import hold_cost_dominance as _hcd
from apf import nonlocal_tie_resolution as _ntr
from apf import candidate_family_overlap as _cfo
from apf.born_at_ties import check_L_selection_ledger_completeness

HELD_OUT_OF_THE_BANK = False  # BANKED v24.3.478 (2026-08-16); landing rewire disclosed in the manifest

FROZEN_SURFACE_SHA256 = (
    "440ed2162e5d28f83a9addba5ce49c257dbe0646cefe287c7dbe2df7617f743d")

REPO_PIN = "526004d"

# The K1-UT counterfactual-reading ruling, consumed as a NAME from the
# banked module's own constant (cited at every pricing site below;
# neither constructed nor discharged here).
K1UT_READING_RULING = _cfo.K1UT_READING_RULING

# The surface's own MAY-NOT-CITE list, binding here, carried verbatim.
MAY_NOT_CITE = (
    "any tie-rate statement beyond the enumerated fixture family (the "
    "census is of authored witnesses); the flat floor as this module's "
    "content, or at any grade other than born_at_ties' own "
    "[P_structural_reading] with its two named readings; \"ties occur at "
    "this rate\" as a physical claim; anything about WHICH outcome occurs "
    "at a token commit (born_at_ties' own fence, carried); any supply "
    "claim.")

# The program's standing fences (frozen-surface header), carried verbatim.
STANDING_FENCES = (
    '"the transfer is forced" -- negative; may not be claimed.',
    '"the carrier gap is closed / narrowed" -- may not be claimed.',
    '"Born is derived" without its conditional clause -- may not be '
    'claimed.',
    'The O2 close and the OT3 vacuity ruling are quotable only whole.',
    'ORIENTATION_COVER_REALIZED is uncertified.',
    'The Paper 9 ladder is not banked.',
    'record_coherence_tradeoff is never a supply.',
    'The banked join network supplies no sign.',
    'Adjacency is not identification.',
)

AUTHORED_INPUTS = ("BASE_S", "POOL_FAMILY", "CAPACITY_C", "KMAX",
                   "the choice to enumerate the banked constructor's "
                   "full (a, b, xo) grid")

# ---------------------------------------------------------------------------
# Scope bounds -- named module-level constants (the census is a census of
# THIS enumerated family and nothing else).  Re-documented at the fix to
# describe the evidence family; see the docstring's SCOPE BOUNDS block.
# ---------------------------------------------------------------------------

# The common base configuration: empty; every candidate strictly extends
# it, and every counterfactual price is booked from it (enforced in TC1).
BASE_S = frozenset()

KMAX = 6

# The coupling family's own-anchor capacity: xo runs over 0..CAPACITY_C.
CAPACITY_C = 2

# The anchor pool the couplings draw their OWN anchors from; TC1 enforces
# BY VALUE that the banked constructor's own-anchor set IS the xo-prefix
# of this pool, per xo.
POOL_FAMILY = tuple(('X', i) for i in range(CAPACITY_C))


EXPECTED_LEGS = {
    "check_TC1_fixture_family_enumeration": [
        "base_is_the_common_extension_and_pricing_baseline",
        "candidate_pairs_built_by_banked_local_tie",
        "cross_module_cost_value_tie",
        "executed_k_set_computed_and_covered",
        "pool_and_capacity_name_the_banked_own_anchor_grid",
    ],
    "check_TC2_tie_census_fraction": [
        "banked_joint_difference_identity_reexecuted_per_instance",
        "both_arms_populated_at_every_executed_k",
        "instances_enumerated_counts_enforced",
        "joint_route_and_deficit_route_value_tied_per_instance",
        "no_float_on_returned_path",
        "per_k_ratio_equals_closed_form_exact_fraction",
        "tie_predicate_by_value_on_every_instance",
    ],
    "check_TC3_flat_floor_live_gate": [
        "floor_gate_executed_and_green",
        "grade_carried_exactly_as_stated",
        "two_named_readings_carried_verbatim",
    ],
}


# ---------------------------------------------------------------------------
# result plumbing (append-and-record leg inventory)
# ---------------------------------------------------------------------------

def _result(name, legs, key_result, record=None, disclosures=()):
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
        "record": record if record is not None else {},
        "scope_bounds": {
            "BASE_S": sorted(BASE_S),
            "POOL_FAMILY": list(POOL_FAMILY),
            "CAPACITY_C": CAPACITY_C,
            "KMAX": KMAX,
            "census_scope": ("a census of THIS enumerated family and "
                             "nothing else; every instance is an authored "
                             "witness"),
        },
        "authored_inputs": list(AUTHORED_INPUTS),
        "disclosures": list(disclosures),
        "may_not_cite": MAY_NOT_CITE,
        "standing_fences": list(STANDING_FENCES),
        "held_out_of_the_bank": HELD_OUT_OF_THE_BANK,
        "frozen_claim_surface_sha256": FROZEN_SURFACE_SHA256,
        "repo_pin": REPO_PIN,
        "inventory_note": (
            "append-and-record: certifies a declared leg EXECUTED, not "
            "that it could have failed; value ties certify VALUES; that "
            "the values came through the banked callables is certified by "
            "code review, not by any leg"),
    }


def _no_float(x, path="root"):
    if isinstance(x, float):
        return [path]
    if isinstance(x, dict):
        out = []
        for k, v in x.items():
            out += _no_float(v, path + "." + str(k))
        return out
    if isinstance(x, (list, tuple, set, frozenset)):
        out = []
        for i, v in enumerate(sorted(x, key=repr) if isinstance(
                x, (set, frozenset)) else x):
            out += _no_float(v, path + "[%d]" % i)
        return out
    return []


# ---------------------------------------------------------------------------
# the fixture family, its instances, and the tie predicate (banked values)
# ---------------------------------------------------------------------------

def _instances(k):
    """The size-k instance set of the evidence family: the banked candidate
    pair A, B = nonlocal_tie_resolution's own _local_tie(k), crossed with
    every coupling X = its own _external(A, B, a, b, xo) over the full
    grid a in 0..k, b in 0..k, xo in 0..CAPACITY_C.  A size at which the
    banked constructor returns no genuine pair (A == B) contributes no
    instances -- exclusion by computation, not by authored bound."""
    A, B = _ntr._local_tie(k)
    if A == B:
        return []
    return [(k, a, b, xo, A, B, _ntr._external(A, B, a, b, xo))
            for a in range(k + 1)
            for b in range(k + 1)
            for xo in range(CAPACITY_C + 1)]


def _counterfactual_price(cfg):
    """The K1-UT increment a candidate WOULD book, priced on its own
    ledger copy through hold_cost_dominance's own _Ledger.transition,
    as the single transition from the BASE_S baseline (the ledger's
    empty initial support) to the candidate (counterfactual reading
    licensed per the ruling named in K1UT_READING_RULING, consumed from
    the banked module's own constant; nothing here is booked into any
    shared world's ledger)."""
    L = _hcd._Ledger('tie_census_counterfactual_copy')
    assert L.support == BASE_S
    return L.transition(cfg)


def tie_predicate(cfg_u, cfg_v, X):
    """The banked genuine-tie condition on one instance, computed THROUGH
    THE BANKED MACHINERY BY VALUE and re-implemented nowhere:
    nonlocal_tie_resolution's own _cost supplies the genuine-tie
    preconditions (equal local cost, distinctness); hold_cost_dominance's
    own _Ledger.transition and _cost price the two candidates and
    value-tie each price to its level difference; the co-held comparison
    runs through nonlocal_tie_resolution's own _joint, with its own
    _deficit as the second route.  Returns (tie, facts)."""
    price_u = _counterfactual_price(cfg_u)
    price_v = _counterfactual_price(cfg_v)
    facts = {
        "price_u": price_u,
        "price_v": price_v,
        # increment == level difference, both through _hcd's own functions
        "price_level_tie": (
            price_u == _hcd._cost(cfg_u) - _hcd._cost(BASE_S) and
            price_v == _hcd._cost(cfg_v) - _hcd._cost(BASE_S)),
        "distinct": cfg_u != cfg_v,
        "equal_local_cost": _ntr._cost(cfg_u) == _ntr._cost(cfg_v),
        "joint_u": _ntr._joint(cfg_u, X),
        "joint_v": _ntr._joint(cfg_v, X),
        "coheld_deficit_route": (_ntr._deficit(cfg_u, X)
                                 == _ntr._deficit(cfg_v, X)),
    }
    facts["coheld_joint_route"] = (facts["joint_u"] == facts["joint_v"])
    facts["tie"] = (facts["distinct"] and
                    facts["equal_local_cost"] and
                    price_u == price_v and
                    facts["coheld_joint_route"])
    return facts["tie"], facts


def _closed_form(k):
    """The in-module closed form of the per-k census ratio, computed from
    k and returned as an exact Fraction (surface sentence 2: both sides
    are returned computed; the figure appears in no prose)."""
    return F(1, k + 1)


def _executed_k_values():
    """The executed family sizes: COMPUTED from the enumeration as the
    k <= KMAX at which the instance set is nonempty."""
    return tuple(k for k in range(KMAX + 1) if len(_instances(k)) > 0)


def run_census():
    """The census: per executed k, the tie predicate computed on every
    instance by value; tie count, instance count, exact Fraction ratio,
    and the in-module closed form, all returned computed."""
    per_k = {}
    for k in _executed_k_values():
        inst = _instances(k)
        n_eval = n_tie = n_pre = n_price_tie = n_route_agree = 0
        n_identity = 0
        for (kk, a, b, xo, cfg_u, cfg_v, X) in inst:
            tie, facts = tie_predicate(cfg_u, cfg_v, X)
            n_eval += 1
            n_tie += 1 if tie else 0
            n_pre += 1 if (facts["distinct"] and
                           facts["equal_local_cost"]) else 0
            n_price_tie += 1 if facts["price_level_tie"] else 0
            n_route_agree += 1 if (facts["coheld_joint_route"]
                                   == facts["coheld_deficit_route"]) else 0
            # the banked module's own joint-difference identity,
            # re-EXECUTED on this instance through its own _joint and EPS
            n_identity += 1 if (facts["joint_u"] - facts["joint_v"]
                                == F(b - a) * _ntr.EPS) else 0
        per_k[k] = {
            "instance_count": len(inst),
            "evaluated_count": n_eval,
            "tie_count": n_tie,
            "decided_count": n_eval - n_tie,
            "preconditions_held_count": n_pre,
            "price_level_tie_count": n_price_tie,
            "route_agreement_count": n_route_agree,
            "identity_held_count": n_identity,
            "ratio": F(n_tie, len(inst)),
            "closed_form": _closed_form(k),
        }
        per_k[k]["ratio_equals_closed_form"] = (
            per_k[k]["ratio"] == per_k[k]["closed_form"])
    return per_k


# ---------------------------------------------------------------------------
# TC1 -- the fixture family enumeration
# ---------------------------------------------------------------------------

def check_TC1_fixture_family_enumeration():
    legs = {}
    k_exec = _executed_k_values()

    pairs = {k: _ntr._local_tie(k) for k in k_exec}
    ok = (len(k_exec) > 0 and all(
        A != B and A & B == frozenset() and
        len(A) == k and len(B) == k and
        _ntr._cost(A) == _ntr._cost(B)
        for k, (A, B) in pairs.items()))
    legs["candidate_pairs_built_by_banked_local_tie"] = (ok, (
        f"at every executed k the candidate pair is "
        f"nonlocal_tie_resolution's own _local_tie(k): distinct, disjoint, "
        f"k anchors each, equal local cost through the banked _cost "
        f"({len(pairs)} pairs executed, sizes {sorted(pairs)}); no "
        f"candidate is authored at this seat"))

    ok = all(
        BASE_S < A and BASE_S < B and
        _hcd._cost(BASE_S) == _ntr._cost(BASE_S) == F(0)
        for (A, B) in pairs.values())
    legs["base_is_the_common_extension_and_pricing_baseline"] = (ok, (
        f"BASE_S is the common base configuration: every candidate at "
        f"every executed k strictly extends it, its cost through both "
        f"banked cost functions is the computed zero Fraction, and every "
        f"counterfactual price below is booked from it (a fresh banked "
        f"ledger's own initial support, asserted equal to BASE_S at the "
        f"pricing site); |BASE_S| = {len(BASE_S)}"))

    pool_ok = [len(POOL_FAMILY) == CAPACITY_C,
               len(set(POOL_FAMILY)) == CAPACITY_C]
    n_pool_cmp = 0
    n_inst_cmp = 0
    for k, (A, B) in pairs.items():
        pool_ok.append(frozenset(POOL_FAMILY) & (A | B) == frozenset())
        for xo in range(CAPACITY_C + 1):
            own = _ntr._external(A, B, 0, 0, xo)
            pool_ok.append(own == frozenset(POOL_FAMILY[:xo]))
            n_pool_cmp += 1
        for (_kk, _a, _b, xo_i, A_i, B_i, X) in _instances(k):
            pool_ok.append(
                X - (A_i | B_i) == frozenset(POOL_FAMILY[:xo_i]))
            n_inst_cmp += 1
    ok = all(pool_ok)
    legs["pool_and_capacity_name_the_banked_own_anchor_grid"] = (ok, (
        f"POOL_FAMILY carries {len(set(POOL_FAMILY))} distinct anchors "
        f"(gated equal to CAPACITY_C = {CAPACITY_C}), disjoint from every "
        f"executed candidate pair; BY VALUE, at every executed k and every "
        f"xo in 0..CAPACITY_C, the banked constructor's own-anchor set "
        f"_external(A, B, 0, 0, xo) IS the xo-prefix of POOL_FAMILY "
        f"({n_pool_cmp} constructor comparisons, gated by conjunction), "
        f"and on EVERY enumerated instance the coupling's non-candidate "
        f"remainder IS that prefix ({n_inst_cmp} instance comparisons, "
        f"gated by conjunction) -- the pool names the banked "
        f"constructor's own grid, it does not replace it"))

    compared = [_hcd.EPS == _ntr.EPS,
                _hcd._cost(BASE_S) == _ntr._cost(BASE_S)]
    n_expected = 2
    for k in k_exec:
        A, B = pairs[k]
        compared.append(_hcd._cost(A) == _ntr._cost(A))
        compared.append(_hcd._cost(B) == _ntr._cost(B))
        n_expected += 2
        for (_kk, _a, _b, _xo, _A, _B, X) in _instances(k):
            compared.append(_hcd._cost(X) == _ntr._cost(X))
            n_expected += 1
    ok = (len(compared) == n_expected and all(compared))
    legs["cross_module_cost_value_tie"] = (ok, (
        f"cross-module VALUE tie: hold_cost_dominance._cost and "
        f"nonlocal_tie_resolution._cost return EQUAL exact Fractions on "
        f"the enumerated comparison set ({len(compared)} comparisons "
        f"executed, gated equal to the enumerated {n_expected}: both "
        f"candidates at every executed k, the base, every enumerated "
        f"coupling, and the two modules' EPS constants) -- equality of "
        f"computed quantities through the banked functions, never verdict "
        f"agreement"))

    ok = (k_exec == tuple(range(1, KMAX + 1)))
    legs["executed_k_set_computed_and_covered"] = (ok, (
        f"the executed k set is COMPUTED from the enumeration (nonempty "
        f"instance sets; the sizes at which the banked constructor returns "
        f"no genuine pair drop out by computation) as {list(k_exec)}, "
        f"gated set-exactly against the contiguous range whose top is "
        f"KMAX = {KMAX}"))

    return _result(
        "check_TC1_fixture_family_enumeration", legs,
        key_result=(
            f"the enumerated fixture family (BASE_S, POOL_FAMILY, "
            f"CAPACITY_C; executed sizes {list(k_exec)}, all <= KMAX = "
            f"{KMAX}) is the banked-tie evidence family: candidate pairs "
            f"by nonlocal_tie_resolution's own _local_tie, couplings by "
            f"its own _external over the full (a, b, xo) grid, the pool "
            f"and capacity enforced by value against the banked "
            f"constructor, and the cross-module cost value tie computed "
            f"on the enumerated comparison set ({len(compared)} exact "
            f"Fraction equalities)"),
        record={"executed_k": list(k_exec),
                "grid_per_k": {k: {"a_b_values": k + 1,
                                   "xo_values": CAPACITY_C + 1}
                               for k in k_exec}},
        disclosures=[
            "the grid bounds (KMAX, CAPACITY_C) and the choice to "
            "enumerate the banked constructor's full (a, b, xo) grid are "
            "authored inputs (disclosed, not discharged); the "
            "constructors themselves are the banked module's own",
            "the fixture family was re-aimed at the banked-tie evidence "
            "family by Ethan's ruling (a) 2026-08-16"])


# ---------------------------------------------------------------------------
# TC2 -- the tie census and the closed-form comparison
# ---------------------------------------------------------------------------

def check_TC2_tie_census_fraction():
    legs = {}
    per_k = run_census()

    ok = all(
        per_k[k]["instance_count"] == (k + 1) * (k + 1) * (CAPACITY_C + 1)
        and per_k[k]["evaluated_count"] == per_k[k]["instance_count"]
        for k in per_k)
    total_inst = sum(per_k[k]["instance_count"] for k in per_k)
    total_eval = sum(per_k[k]["evaluated_count"] for k in per_k)
    ok = ok and total_eval == total_inst and total_inst > 0
    legs["instances_enumerated_counts_enforced"] = (ok, (
        f"per-k instance counts {[per_k[k]['instance_count'] for k in sorted(per_k)]} "
        f"each gated equal to the (a, b, xo)-grid count of the "
        f"enumeration, and the predicate was EVALUATED on every instance "
        f"({total_eval} evaluations, gated equal to {total_inst} "
        f"instances)"))

    ok = all(
        per_k[k]["preconditions_held_count"] == per_k[k]["instance_count"]
        and per_k[k]["price_level_tie_count"] == per_k[k]["instance_count"]
        for k in per_k)
    legs["tie_predicate_by_value_on_every_instance"] = (ok, (
        f"on every one of the {total_inst} instances the predicate ran "
        f"through the banked machinery by value: the genuine-tie "
        f"preconditions (nonlocal_tie_resolution's own _cost equality + "
        f"distinctness) held on "
        f"{sum(per_k[k]['preconditions_held_count'] for k in per_k)} "
        f"instances (gated equal to the instance count), and on each "
        f"instance both candidates' counterfactual increments through "
        f"hold_cost_dominance's own _Ledger.transition (each on its own "
        f"ledger copy from the BASE_S baseline; reading licensed per "
        f"{K1UT_READING_RULING}) were value-tied to the level difference "
        f"through _cost "
        f"({sum(per_k[k]['price_level_tie_count'] for k in per_k)} "
        f"instances, gated equal)"))

    ok = all(per_k[k]["route_agreement_count"] == per_k[k]["instance_count"]
             for k in per_k)
    legs["joint_route_and_deficit_route_value_tied_per_instance"] = (ok, (
        f"two routes, one verdict, per instance: the co-held comparison "
        f"through nonlocal_tie_resolution's own _joint and the comparison "
        f"through its own _deficit returned the same value on "
        f"{sum(per_k[k]['route_agreement_count'] for k in per_k)} of "
        f"{total_inst} instances (gated equal) -- computed quantities "
        f"through the banked functions on both routes"))

    ok = all(per_k[k]["identity_held_count"] == per_k[k]["instance_count"]
             for k in per_k)
    legs["banked_joint_difference_identity_reexecuted_per_instance"] = (ok, (
        f"the banked module's own joint-difference identity was "
        f"re-EXECUTED (never re-derived) on every instance through its "
        f"own _joint and EPS: it held on "
        f"{sum(per_k[k]['identity_held_count'] for k in per_k)} of "
        f"{total_inst} instances (gated equal) -- a value tie of computed "
        f"quantities to the coupling profile's computed difference"))

    ok = all(per_k[k]["ratio_equals_closed_form"] and
             isinstance(per_k[k]["ratio"], F) and
             isinstance(per_k[k]["closed_form"], F) and
             # the returned ratio IS the count-derived fraction, gated from
             # the same record entries (fix seat, audit MINOR F1)
             per_k[k]["ratio"] == F(per_k[k]["tie_count"],
                                    per_k[k]["instance_count"])
             for k in per_k)
    legs["per_k_ratio_equals_closed_form_exact_fraction"] = (ok, (
        f"per k, the computed census ratio equals the in-module closed "
        f"form computed from k, as exact Fraction equality -- "
        + "; ".join(
            f"k={k}: {per_k[k]['tie_count']}/{per_k[k]['instance_count']} "
            f"= {per_k[k]['ratio']} == {per_k[k]['closed_form']}"
            for k in sorted(per_k))
        + " (both sides returned computed; the figure appears in no prose)"))

    total_tie = sum(per_k[k]["tie_count"] for k in per_k)
    total_decided = sum(per_k[k]["decided_count"] for k in per_k)
    ok = (total_tie > 0 and total_decided > 0 and
          all(per_k[k]["tie_count"] > 0 and per_k[k]["decided_count"] > 0
              for k in per_k))
    legs["both_arms_populated_at_every_executed_k"] = (ok, (
        f"both predicate arms are populated at EVERY executed k: "
        f"{total_tie} ties and {total_decided} decided instances across "
        f"the family; per-k tie counts "
        f"{[per_k[k]['tie_count'] for k in sorted(per_k)]} and decided "
        f"counts {[per_k[k]['decided_count'] for k in sorted(per_k)]}, "
        f"each gated nonzero"))

    record = {
        "per_k": per_k,
        "tie_count": total_tie,
        "instance_count": total_inst,
        "ratio": F(total_tie, total_inst),
    }
    float_paths = _no_float({
        "per_k": per_k, "ratio": record["ratio"],
        "EPS_hcd": _hcd.EPS, "EPS_ntr": _ntr.EPS})
    ok = (float_paths == [])
    legs["no_float_on_returned_path"] = (ok, (
        f"no float anywhere on the returned path ({len(float_paths)} "
        f"float sites found, gated zero); counts are ints, every ratio "
        f"and cost an exact Fraction"))

    return _result(
        "check_TC2_tie_census_fraction", legs,
        key_result=(
            f"on the enumerated fixture family (executed sizes "
            f"{sorted(per_k)}, all <= KMAX = {KMAX}) the tie predicate was "
            f"computed on every instance through the banked machinery by "
            f"value; tie count {total_tie}, instance count {total_inst}, "
            f"ratio {record['ratio']} (computed values); per k the "
            f"computed ratio equals the in-module closed form as exact "
            f"Fraction equality -- a census of THIS enumerated family of "
            f"authored witnesses and nothing else"),
        record=record,
        disclosures=[
            "the census is of authored witnesses; the computed fraction "
            "is a property of this enumerated family at its named scope "
            "bounds and of nothing beyond them",
            "on this family (equal-size disjoint candidate pairs from the "
            "banked constructor) the equal-price condition, the "
            "increment==level-difference tie, the two-route agreement, "
            "and the joint-difference identity are algebraic identities "
            "of the banked count-only cost; those legs certify the "
            "identities EXECUTED through the banked functions on every "
            "instance, not contingencies of the fixture",
            "the counterfactual pricing sites consume the K1-UT reading "
            "as a licensed NAME from the banked module's own constant: "
            + K1UT_READING_RULING])


# ---------------------------------------------------------------------------
# TC3 -- the flat floor at ties, consumed as a live gate
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
def check_TC3_flat_floor_live_gate():
    legs = {}
    r_born = check_L_selection_ledger_completeness()

    ok = (r_born.get("passed") is True and
          r_born.get("name") == "L_selection_ledger_completeness")
    legs["floor_gate_executed_and_green"] = (ok, (
        f"check_L_selection_ledger_completeness EXECUTED live here: "
        f"name '{r_born.get('name')}', passed {r_born.get('passed')}, "
        f"with {len(r_born.get('fail_reasons', []))} fail reasons "
        f"(gated zero via passed)"))

    grade = r_born.get("epistemic")
    ok = (grade == "P_structural_reading")
    legs["grade_carried_exactly_as_stated"] = (ok, (
        f"the gate's grade is carried exactly as the banked module's own "
        f"returned value states it: '{grade}' (gated equal to born_at_ties' "
        f"own grade string; carried at no other grade)"))

    readings = r_born.get("artifacts", {}).get("readings", {})
    ok = (set(readings) == {"R-sel-LC", "R-event-model"} and
          all(isinstance(v, str) and len(v) > 0 for v in readings.values()))
    legs["two_named_readings_carried_verbatim"] = (ok, (
        f"the two named readings are carried verbatim from the banked "
        f"module's own returned artifacts ({len(readings)} readings, "
        f"names {sorted(readings)}): "
        + " || ".join(f"{n}: {readings[n]}" for n in sorted(readings))))

    return _result(
        "check_TC3_flat_floor_live_gate", legs,
        key_result=(
            f"the flat floor at ties is consumed from the bank as a live "
            f"gate: check_L_selection_ledger_completeness executed here, "
            f"passed {r_born.get('passed')}, at its own grade '{grade}' "
            f"with its {len(readings)} named readings carried as that "
            f"module states them -- nothing of its content is re-derived, "
            f"regraded, or extended by this module"),
        record={
            "floor_gate": {
                "name": r_born.get("name"),
                "passed": r_born.get("passed"),
                "epistemic_as_stated": grade,
                "readings_as_stated": dict(readings),
            },
        },
        disclosures=[
            "this leg set is CONSUMPTION: the floor's grade and readings "
            "are born_at_ties' own returned values, quoted, not this "
            "module's content"])


# ---------------------------------------------------------------------------
# registration
# ---------------------------------------------------------------------------

_CHECKS = {
    "check_TC1_fixture_family_enumeration":
        check_TC1_fixture_family_enumeration,
    "check_TC2_tie_census_fraction": check_TC2_tie_census_fraction,
    "check_TC3_flat_floor_live_gate": check_TC3_flat_floor_live_gate,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == "__main__":
    import sys
    results = run_all()
    n_pass = sum(1 for r in results.values() if r["passed"])
    n_legs = sum(r["leg_count"] for r in results.values())
    print("tie_fraction_census: BANKED v24.3.478 (2026-08-16) "
          "(SURFACE 2; fixture family re-aimed at "
          "the banked-tie evidence family, Ethan's ruling (a) 2026-08-16)")
    for name, r in results.items():
        status = "PASS" if r["passed"] else "FAIL"
        print(f"  [{status}] {name} ({r['leg_count']} legs)")
        for reason in r["fail_reasons"]:
            print(f"      FAIL: {reason}")
    census = results["check_TC2_tie_census_fraction"]["record"]
    for k in sorted(census["per_k"]):
        row = census["per_k"][k]
        print(f"  k={k}: instances={row['instance_count']} "
              f"ties={row['tie_count']} ratio={row['ratio']} "
              f"closed_form={row['closed_form']} "
              f"equal={row['ratio_equals_closed_form']}")
    print(f"  totals: ties={census['tie_count']} "
          f"instances={census['instance_count']} ratio={census['ratio']}")
    gate = results["check_TC3_flat_floor_live_gate"]["record"]["floor_gate"]
    print(f"  floor gate: {gate['name']} passed={gate['passed']} "
          f"grade={gate['epistemic_as_stated']} "
          f"readings={sorted(gate['readings_as_stated'])}")
    print(f"{n_pass}/{len(results)} checks pass; {n_legs} legs")
    sys.exit(0 if n_pass == len(results) else 1)
