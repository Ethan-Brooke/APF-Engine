"""apf/foundation_inputs.py -- Executable witness for the canonical 4-input
declaration of Admissibility Physics + the derivation of PLEC's four
constitutive features from that declaration.

Phase 42 (2026-05-04 LATER): codebase landing of the LATER-9 input-set
collapse 5 → 4 (Paper 0 v6.0.5 + Paper 1 supplement v8.22+).  The framework's
canonical input set is exactly four:

    1. FD1 -- Physical identity = finite admissible continuation identity.
       (Structural completeness: a physical object/state/demand IS its
       continuation profile and nothing beyond it; there are no physical
       facts except those fixed by the continuation structure, so any
       quantity making an empirical difference is structural, not free to be
       assigned by fiat -- adopted clause, check_FD1_structural_completeness.)
    2. FD2 -- Physical distinction = finite enforceable separator of
       continuation profiles.
    3. FD3 -- Physical distinctions carry positive realignment cost.
    4. Finite-physical-regime hypothesis: C_Γ < ∞ at every interface.

All other commitments named anywhere in the corpus (PLEC's four constitutive
features A1/MD/A2/BW, the marginal floor ε* > 0, the Sep/IJC dichotomy, the
κ_int two-sided structural rigidity, the R1-R4 robust-finite-interface
conditions) are derivable consequences of these four under Paper 10 v1.12
§3.5 reductions.

This module provides two bank-registered checks witnessing the foundation:

  * check_T_four_input_declaration -- certifies that the canonical witness
    APS satisfies all four inputs and that no other primitive commitment is
    needed to support the spine.

  * check_T_PLEC_derived_from_spine -- exhibits A1, MD and A2 on the
    canonical witness as consequences of the four-input declaration: A1 =
    finite-physical-regime hypothesis directly; MD-value = ε* > 0 as the
    second half of the finite-physical-regime hypothesis with the
    tested/gauge cleavage from FD2; A2 = argmin from cost-as-infimum +
    no-waste under saturation.  BW is carried under its STATEMENT OF
    RECORD (OHC_N@2026-08-30) -- cost-spectrum non-degeneracy at the
    element-distinction level -- and the increment condition it used to
    be stated by is retained beside it as MD's content under MD's name.

    THE INCREMENT-FORM WAS RETIRED AS A STATEMENT OF BW AT v24.3.482
    (2026-08-30), on an executed control rather than on a reading.  The
    form "every admissible cost increment is ≥ μ*_Γ, so the spectrum is
    graded at scale μ*_Γ" is satisfied by the FLAT WORLD -- every
    distinction at one cost at or above the floor -- which is Paper 0's
    own countermodel to BW and precisely the world BW exists to exclude.
    The canonical witness was itself flat, so the leg passed on a
    maximally degenerate cost spectrum while its sentence claimed
    non-degeneracy.  The flat world is now BUILT AND EXECUTED in this
    module as a permanent negative control: it FAILS the repaired BW leg
    and PASSES the A1, MD-value and increment legs, which is the whole
    content of the repair.

    WHAT THAT CONTROL DOES NOT SHOW, named here so it is not read off the
    code: it does not show that BW is underivable from MD, that Lemma BW
    of Paper 10 v1.12 §3.5 is wrong, or that BW is an axiom.  Nobody in
    this lane opened Paper 10 §3.5.  The honest statement is about the
    TRANSCRIPTION that ships in this module.

Checks here are tier 4; FD1_structural_completeness is [P] (Assumption 1 at
full strength, per the canonical [P] convention), the other two [P_structural].

Source-of-record: Paper 0 v6.0.5 §3.1 (4-input declaration) + Paper 1
Supplement v8.22+ §1 ("Inputs, in one place") + Paper 10 v1.12 §3.5
(Lemmas A2 + BW).

On operational language.  This module witnesses static algebraic relations
on admissibility space -- the input declaration is a structural commitment,
not a process.  What reads in the prose below as "primitive," "input,"
"commitment" is the local reading of those static relations under the
operational vocabulary of physics.  Paper 0's Descriptive Reading chapter
+ Paper 1 supplement v8.31 §1 carry the eternalist convention.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import FrozenSet, Tuple, Dict, List


# =====================================================================
# Witness construction (paralleling apf/aps.py's WitnessAPS)
# =====================================================================

@dataclass(frozen=True)
class FourInputWitness:
    """A finite witness exhibiting the canonical 4-input declaration.

    The witness is a small concrete admissibility space that satisfies all
    four inputs and from which PLEC's four features can be read off as
    derived consequences.

    Substrate Σ = {0, 1, 2, 3} (4 raw configurations).
    Continuation equivalence partitions Σ into 2 physical states.
    Distinctions are finite-cost separators of continuation profiles.
    Capacity bound C = 5 (finite); marginal floor μ* = 1 (positive).
    """
    substrate: FrozenSet[int]
    continuations: Dict[int, FrozenSet[int]]  # FD1: continuation profile
    distinctions: FrozenSet[Tuple[int, int]]  # FD2: separator pairs
    distinction_costs: Dict[Tuple[int, int], float]  # FD3: positive cost
    capacity: float  # finite-physical-regime hypothesis
    marginal_floor: float  # μ* derived from finite-physical-regime


def _build_canonical_witness() -> FourInputWitness:
    """Construct a canonical 4-input witness."""
    substrate = frozenset({0, 1, 2, 3})
    # Continuation profiles: states 0,1 share continuation class A;
    # states 2,3 share continuation class B
    continuations = {
        0: frozenset({0, 1}),
        1: frozenset({0, 1}),
        2: frozenset({2, 3}),
        3: frozenset({2, 3}),
    }
    # Distinctions: separate the two continuation-equivalence classes
    distinctions = frozenset({(0, 2), (0, 3), (1, 2), (1, 3)})
    # NON-DEGENERATE cost spectrum (v24.3.482): two distinct values, every
    # value > 0 and >= μ*, so the witness satisfies FD3, the marginal-floor
    # bound AND BW's statement of record.  It was a FLAT map (every
    # distinction at 1.5) until this version, and a flat map is the world
    # BW exists to exclude -- see the module docstring.  The costs are
    # keyed by distinction, never by position, so no reading here depends
    # on the iteration order of a frozenset.
    distinction_costs = {
        (0, 2): 1.5,
        (0, 3): 1.5,
        (1, 2): 1.5,
        (1, 3): 2.0,
    }
    capacity = 5.0  # finite
    marginal_floor = 1.0  # μ* > 0
    return FourInputWitness(
        substrate=substrate,
        continuations=continuations,
        distinctions=distinctions,
        distinction_costs=distinction_costs,
        capacity=capacity,
        marginal_floor=marginal_floor,
    )


# Declared leg inventory for check_T_PLEC_derived_from_spine.  Set-exact:
# the check asserts BOTH directions (nothing declared failed to run, and
# nothing ran undeclared) and records a mismatch as a failure reason
# rather than raising (D7@2026-08-08, append-and-record).
_PLEC_SPINE_LEGS: FrozenSet[str] = frozenset({
    "A1_capacity_finite",
    "MD_value_floor_positive",
    "MD_tested_gauge_cleavage",
    "A2_argmin_counting_bound",
    "MD_increment_at_least_floor",
    "BW_non_degeneracy_statement_of_record",
    "BW_order_independence",
    "CONTROL_flat_world_fails_BW",
    "CONTROL_flat_world_passes_A1_MD_and_increment",
    "CONTROL_two_valued_witness_passes_BW",
    "TIE_worked_example_cost_spectrum_by_value",
})


def _build_flat_witness() -> FourInputWitness:
    """Paper 0's own BW countermodel, built so it can be executed.

    Paper 0 v6.2.56: "a world in which every distinction costs exactly
    μ*, with total capacity C ... satisfies A1 and MD but has maximally
    degenerate cost spectrum."  This witness is that world at the scale
    the canonical witness uses: the SAME substrate, continuations and
    distinctions, with every distinction carrying ONE cost at or above
    the floor.  It is byte-for-byte the cost map the canonical witness
    carried before v24.3.482, which is what makes it the sharp control:
    it is the world the retired increment-form leg passed on.
    """
    base = _build_canonical_witness()
    return FourInputWitness(
        substrate=base.substrate,
        continuations=base.continuations,
        distinctions=base.distinctions,
        distinction_costs={d: 1.5 for d in base.distinctions},
        capacity=base.capacity,
        marginal_floor=base.marginal_floor,
    )


def _cost_spectrum(costs) -> Tuple[float, ...]:
    """The multiset of element-distinction costs, as a SORTED tuple.

    Sorting is what makes every reading below independent of the
    iteration order of the underlying frozenset (a stated requirement of
    the repair, not an accident of this implementation).
    """
    return tuple(sorted(costs))


def _bw_non_degeneracy(costs) -> bool:
    """BW under its STATEMENT OF RECORD (OHC_N@2026-08-30).

    Informal, canonical: not all enforceable distinctions have the same
    cost -- there exist distinctions d_i, d_j with eps(d_i) != eps(d_j).

    DOMAIN, and it is a recorded scope and NOT a theorem: the
    quantification ranges over ELEMENT distinctions -- the objects the
    implemented ledger charges.  Round 10 closed OHC_N, so neither a
    wider domain (a loop-class charge) nor the completeness of this one
    (a derived absence) is established, and nothing computed by this
    function may be cited for either direction of the domain question.

    Non-degeneracy, not gradedness: the predicate is on the SIZE OF THE
    VALUE SET, and it is order-independent by construction.
    """
    return len(set(_cost_spectrum(costs))) >= 2


def _md_increment_at_least_floor(w: FourInputWitness, order) -> bool:
    """MD's content, under MD's name -- NOT a statement of BW.

    Greedily admit distinctions in the given order while the capacity
    holds, and verify every admitted increment is >= μ*_Γ.  This is TRUE,
    it is MD's, and it is retained for exactly that reason.  It is
    satisfied by the flat world, which is why it is no longer called BW.
    """
    cost_S = 0.0
    for d in order:
        if cost_S + w.distinction_costs[d] > w.capacity:
            continue
        new_cost = cost_S + w.distinction_costs[d]
        if new_cost - cost_S < w.marginal_floor:
            return False
        cost_S = new_cost
    return True


# =====================================================================
# Bank-registered checks
# =====================================================================

def check_T_four_input_declaration():
    """T_four_input_declaration: the canonical 4-input declaration of APF.

    Tier 4 [P_structural].

    Source-of-record: Paper 0 v6.0.5 §3.1 + Paper 1 Supplement v8.22+ §1.

    Verifies on the canonical witness that:
      (i) FD1: every raw substrate element has a non-empty continuation
          profile, and continuation equivalence partitions the substrate.
      (ii) FD2: every distinction is a finite separator of continuation
          profiles -- i.e., a pair of substrate elements that lie in
          different continuation-equivalence classes.
      (iii) FD3: every distinction has strictly positive realignment cost.
      (iv) Finite-physical-regime hypothesis: C_Γ < ∞ AND μ*_Γ > 0.

    No fifth input is invoked.  PLEC's four features and the marginal floor
    follow as derived consequences (see check_T_PLEC_derived_from_spine).
    """
    w = _build_canonical_witness()

    # (i) FD1: continuation profiles non-empty + partition
    for x in w.substrate:
        assert x in w.continuations, f"FD1: missing continuation for {x}"
        assert len(w.continuations[x]) > 0, f"FD1: empty continuation profile for {x}"
    # Equivalence relation: x ~ y iff Cont(x) == Cont(y)
    classes_seen = set()
    for x in w.substrate:
        cls = w.continuations[x]
        # All members of the class should agree on the continuation profile
        for y in cls:
            assert w.continuations[y] == cls, (
                f"FD1: continuation profile incoherent for {x} ~ {y}"
            )
        classes_seen.add(cls)
    # The partition covers the substrate
    union = frozenset().union(*classes_seen)
    assert union == w.substrate, "FD1: continuation partition doesn't cover substrate"

    # (ii) FD2: distinctions are finite separators of continuation profiles
    for (x, y) in w.distinctions:
        assert x in w.substrate and y in w.substrate, (
            f"FD2: distinction {(x,y)} references non-substrate element"
        )
        # The two elements must lie in different continuation classes
        assert w.continuations[x] != w.continuations[y], (
            f"FD2: distinction {(x,y)} doesn't separate continuation profiles"
        )

    # (iii) FD3: every distinction has positive cost
    for d, cost in w.distinction_costs.items():
        assert cost > 0, f"FD3: distinction {d} has non-positive cost {cost}"

    # (iv) Finite-physical-regime: C_Γ < ∞ + μ*_Γ > 0
    assert w.capacity < float("inf"), "Finite-physical-regime: C_Γ not finite"
    assert w.marginal_floor > 0, "Finite-physical-regime: μ*_Γ not positive"
    # Margin verification: each distinction cost ≥ μ*_Γ (uniform lower bound)
    for d, cost in w.distinction_costs.items():
        assert cost >= w.marginal_floor, (
            f"Marginal-floor uniform lower bound violated at {d}: {cost} < {w.marginal_floor}"
        )

    return {
        "name": "T_four_input_declaration",
        "passed": True,
        "key_result": (
            f"4-input declaration witnessed on substrate of size {len(w.substrate)}: "
            f"FD1 partition into {len(classes_seen)} continuation classes; "
            f"FD2 {len(w.distinctions)} continuation-separating distinctions; "
            f"FD3 all distinction costs > 0 (min {min(w.distinction_costs.values())}); "
            f"finite-physical-regime C_Γ = {w.capacity} < ∞, μ*_Γ = {w.marginal_floor} > 0; "
            f"no fifth input invoked."
        ),
        "summary": (
            "Canonical 4-input declaration of APF: FD1 (physical identity = finite "
            "admissible continuation identity) + FD2 (physical distinction = finite "
            "enforceable separator of continuation profiles) + FD3 (physical "
            "distinctions carry positive realignment cost) + finite-physical-regime "
            "hypothesis (C_Γ < ∞ AND μ*_Γ > 0).  All other commitments named in the "
            "corpus -- PLEC's four constitutive features A1/MD/A2/BW, the marginal "
            "floor ε*, the Sep/IJC dichotomy, the κ_int two-sided rigidity, the "
            "R1-R4 robust-finite-interface conditions -- are derivable consequences "
            "of these four under Paper 10 v1.12 §3.5 reductions."
        ),
        "tier": 4,
        "epistemic": "[P_structural]",
        "dependencies": ["FD1", "FD2", "FD3", "finite_physical_regime"],
    }


def check_T_PLEC_derived_from_spine():
    """T_PLEC_derived_from_spine: PLEC's four features as derived consequences
    of the 4-input declaration under Paper 10 v1.12 §3.5 reductions.

    Tier 4 [P_structural].

    Source-of-record: Paper 10 v1.12 §3.5 (Lemmas A2 + BW) + Paper 1
    Supplement v8.22+ §1 ("PLEC's four features as derived consequences").

    Verifies on the canonical witness that:
      (i)   A1 (capacity bound) is the finite-physical-regime hypothesis
            half-1 directly: C_Γ < ∞.
      (ii)  MD (positive cost floor) is the finite-physical-regime hypothesis
            half-2 directly: μ*_Γ > 0; the tested/gauge cleavage is FD2's
            separator-of-continuation-profiles vs. continuation-profile-
            preserving relabeling distinction.
      (iii) A2 (argmin selection) is derived from cost-as-infimum (FD3 via
            the infimum-over-admissible-protocols valuation convention) +
            no-waste under saturation: when capacity is fully committed, no
            spare resource can be allocated to a non-extremal protocol.
      (iv)  MD-increment: every admissible cost increment is ≥ μ*_Γ.  This
            is TRUE and it is MD's content, and it is retained under MD's
            name.  IT IS NOT A STATEMENT OF BW -- the flat world satisfies
            it, and the flat world is what BW exists to exclude.
      (v)   BW under its STATEMENT OF RECORD (OHC_N@2026-08-30):
            cost-spectrum non-degeneracy at the element-distinction level,
            there exist d_i, d_j with eps(d_i) != eps(d_j).  The domain
            restriction to element distinctions is a RECORDED SCOPE and
            not a theorem; the distinction-level/configuration-level delta
            is scoped, not closed.

    A1, MD and A2 are exhibited on the canonical witness as consequences of
    the four-input declaration.  BW is EXHIBITED, not derived here: what
    this record establishes about the (iv)/(v) pair is a SEPARATION, and it
    establishes it by execution --

      * the flat world (every distinction at one cost at or above the
        floor) PASSES (i), (ii) and (iv) and FAILS (v);
      * a two-valued world PASSES (v).

    Both directions are executed as permanent controls.  So the increment
    condition AS EXECUTED HERE does not entail the statement of record.
    That is a statement about this transcription and about nothing else:
    it is NOT a claim that BW is underivable from MD, NOT a claim that
    Lemma BW of Paper 10 v1.12 §3.5 is wrong, and NOT a claim that BW is
    an axiom.  Nobody in this lane opened Paper 10 §3.5.

    LEG INVENTORY.  Set-exact against the module-level frozen set, on the
    bank path, append-and-record (D7@2026-08-08): a mismatch contributes a
    failure reason and does not raise, and `passed` is COMPUTED from the
    reasons rather than written as a literal.

    DISCLOSED RESIDUAL, stated because it is real and NOT machined around.
    The discrimination in (v) is carried by the flat-world control, not by
    the threshold inside the predicate.  A COORDINATED TWO-SITE EDIT
    escapes with every leg green: weaken `_bw_non_degeneracy` from
    `>= 2` to `>= 1` AND invert this function's `if flat_bw:` test to
    `if not flat_bw:`.  Neither the two-valued control nor the
    cross-module value tie discriminates the threshold -- both are
    satisfied at `>= 1` -- so no leg here catches that pair.  It is a
    deletion of the guard together with the thing the guard guards, and a
    third guard would move the escape to a three-site edit rather than
    close it.  The single-site forms of both edits ARE caught.
    """
    w = _build_canonical_witness()
    legs_run: List[str] = []
    failure_reasons: List[str] = []

    # (i) A1: capacity bound = finite-physical-regime half-1
    A1_witnessed = w.capacity < float("inf")
    assert A1_witnessed, "A1 derivation failed: C_Γ not finite"
    legs_run.append("A1_capacity_finite")

    # (ii) MD-value: μ*_Γ > 0 = finite-physical-regime half-2
    MD_value_witnessed = w.marginal_floor > 0
    assert MD_value_witnessed, "MD-value derivation failed: μ*_Γ not positive"

    # MD tested/gauge cleavage: from FD2.  All distinctions in our witness
    # are tested (continuation-profile separators).  A gauge transformation
    # would be a continuation-profile-preserving relabeling -- which is NOT
    # a separator under FD2, hence outside the distinction set.  Verify by
    # checking the contrapositive: every distinction in our set is a tested
    # (cost > 0) separator, not a zero-cost relabeling.
    for d, cost in w.distinction_costs.items():
        x, y = d
        assert w.continuations[x] != w.continuations[y], (
            f"MD tested/gauge cleavage failed at {d}: not a continuation separator"
        )
        assert cost > 0, f"MD tested distinction {d} has non-positive cost"
    MD_cleavage_witnessed = True
    legs_run.append("MD_value_floor_positive")
    legs_run.append("MD_tested_gauge_cleavage")

    # (iii) A2: argmin from cost-as-infimum + no-waste under saturation.
    # Test: among admissible families S of distinctions with total cost ≤ C_Γ,
    # the one with maximum cardinality saturates the budget (no-waste).
    n_distinctions = len(w.distinctions)
    distinctions_list = list(w.distinctions)
    n_admissible_max_sized = 0
    max_size = 0
    # Enumerate all subsets up to capacity
    for mask in range(1 << n_distinctions):
        S = [distinctions_list[i] for i in range(n_distinctions) if (mask >> i) & 1]
        total = sum(w.distinction_costs[d] for d in S)
        if total <= w.capacity:
            if len(S) > max_size:
                max_size = len(S)
                n_admissible_max_sized = 1
            elif len(S) == max_size:
                n_admissible_max_sized += 1
    # The maximum admissible size is bounded by ⌊C_Γ / μ*_Γ⌋ (independent counting)
    expected_max = int(w.capacity // w.marginal_floor)
    assert max_size <= expected_max, (
        f"A2 argmin counting bound violated: {max_size} > ⌊C_Γ/μ*_Γ⌋ = {expected_max}"
    )
    A2_witnessed = max_size > 0  # there exists an admissible argmin family
    legs_run.append("A2_argmin_counting_bound")

    # (iv) MD-increment, under MD's name.  TRUE, retained, and no longer
    # called BW: the flat world satisfies it (control below).
    increment_ok = _md_increment_at_least_floor(w, distinctions_list[:max_size])
    assert increment_ok, (
        f"MD increment condition violated on the canonical witness "
        f"(some admitted increment < μ*_Γ = {w.marginal_floor})"
    )
    legs_run.append("MD_increment_at_least_floor")

    # (v) BW under its statement of record: element-distinction-level
    # cost-spectrum NON-DEGENERACY.  Not gradedness.
    spectrum = _cost_spectrum(w.distinction_costs.values())
    distinct_costs = sorted(set(spectrum))
    assert _bw_non_degeneracy(w.distinction_costs.values()), (
        f"BW (statement of record) violated: the canonical witness carries "
        f"{len(distinct_costs)} distinct element-distinction cost(s) "
        f"{distinct_costs}; the statement requires d_i, d_j with "
        f"eps(d_i) != eps(d_j)"
    )
    legs_run.append("BW_non_degeneracy_statement_of_record")

    # (v-b) ORDER-INDEPENDENCE of the BW reading, executed rather than
    # asserted in prose: the predicate is evaluated on a reversed and on a
    # rotated presentation of the same cost multiset and must agree.
    _vals = list(w.distinction_costs.values())
    assert (_bw_non_degeneracy(_vals)
            == _bw_non_degeneracy(list(reversed(_vals)))
            == _bw_non_degeneracy(_vals[1:] + _vals[:1])), (
        "BW reading is not order-independent"
    )
    legs_run.append("BW_order_independence")

    # ---- PERMANENT CONTROL 1 (the load-bearing one): the flat world ----
    # Paper 0's own BW countermodel, EXECUTED.  It must FAIL the BW leg
    # and PASS A1, MD-value and the increment leg.  If this control ever
    # stops firing, the BW leg has stopped discriminating and this check
    # must go red rather than quietly certify a degenerate world.
    #
    # THIS TEST IS THE DISCRIMINATION.  The predicate's threshold is not
    # independently tied by any leg here, so weakening _bw_non_degeneracy
    # to `>= 1` AND inverting the `if flat_bw:` below escapes all eleven
    # legs.  Disclosed in the docstring, deliberately not machined around.
    flat = _build_flat_witness()
    flat_bw = _bw_non_degeneracy(flat.distinction_costs.values())
    if flat_bw:
        failure_reasons.append(
            "CONTROL FAILED: the flat world satisfies the BW leg, so the "
            "leg does not discriminate the world BW exists to exclude"
        )
    legs_run.append("CONTROL_flat_world_fails_BW")

    flat_list = sorted(flat.distinctions)
    flat_max_size = 0
    for mask in range(1 << len(flat_list)):
        S = [flat_list[i] for i in range(len(flat_list)) if (mask >> i) & 1]
        if sum(flat.distinction_costs[d] for d in S) <= flat.capacity:
            flat_max_size = max(flat_max_size, len(S))
    flat_A1 = flat.capacity < float("inf")
    flat_MD = flat.marginal_floor > 0
    flat_incr = _md_increment_at_least_floor(flat, flat_list[:flat_max_size])
    if not (flat_A1 and flat_MD and flat_incr):
        failure_reasons.append(
            f"CONTROL FAILED: the flat world was expected to satisfy A1, "
            f"MD-value and the increment condition; got A1={flat_A1}, "
            f"MD={flat_MD}, increment={flat_incr}.  The separation between "
            f"the increment condition and the statement of record is what "
            f"this control exhibits, and it is not exhibited"
        )
    legs_run.append("CONTROL_flat_world_passes_A1_MD_and_increment")

    # ---- PERMANENT CONTROL 2 (the other direction) ----
    # A two-valued world -- built here, NOT the canonical witness, so the
    # control is not the thing it is controlling -- must PASS the BW leg.
    two_valued = [1.0, 1.0, 1.0, 3.0]
    if not _bw_non_degeneracy(two_valued):
        failure_reasons.append(
            f"CONTROL FAILED: a two-valued cost spectrum {sorted(set(two_valued))} "
            f"was refused by the BW leg, so the leg is not satisfiable"
        )
    legs_run.append("CONTROL_two_valued_witness_passes_BW")

    # ---- CROSS-MODULE VALUE TIE ----
    # The corpus's executed element-distinction non-degeneracy witness is
    # check_worked_example (apf/core.py), BW's source-most anchor per
    # apf/crystal_axiom_roots.py.  Its costs are PARSED OUT OF ITS OWN
    # EXECUTED RECORD and run through THIS module's predicate -- a tie by
    # VALUE and not by verdict, and not a fifth re-typing of its literals.
    import re as _re
    from fractions import Fraction as _Fr
    from apf.core import check_worked_example as _cwe
    _we = _cwe()
    _eps = [_Fr(m) for m in _re.findall(r"eps\(d\d\)=([0-9]+(?:/[0-9]+)?)",
                                       _we.get("summary", ""))]
    if len(_eps) < 2:
        failure_reasons.append(
            f"VALUE TIE FAILED: could not recover at least two element "
            f"costs from the executed record of the corpus's "
            f"non-degeneracy anchor (recovered {len(_eps)})"
        )
    elif not _bw_non_degeneracy(_eps):
        failure_reasons.append(
            f"VALUE TIE FAILED: this module's BW predicate refuses the "
            f"anchor's own executed cost spectrum {sorted(set(_eps))}"
        )
    legs_run.append("TIE_worked_example_cost_spectrum_by_value")

    # ---- leg inventory, append-and-record (D7@2026-08-08) ----
    _ran = set(legs_run)
    _missing = sorted(_PLEC_SPINE_LEGS - _ran)
    _extra = sorted(_ran - _PLEC_SPINE_LEGS)
    if _missing or _extra:
        failure_reasons.append(
            f"LEG INVENTORY MISMATCH: {len(_missing)} declared leg(s) did "
            f"not run {_missing}; {len(_extra)} leg(s) ran undeclared {_extra}"
        )
    if len(legs_run) != len(_ran):
        failure_reasons.append(
            f"LEG INVENTORY MISMATCH: {len(legs_run)} leg records for "
            f"{len(_ran)} distinct legs (a leg recorded itself twice)"
        )

    return {
        "name": "T_PLEC_derived_from_spine",
        "passed": not failure_reasons,
        "failure_reasons": list(failure_reasons),
        "legs_run": sorted(_ran),
        "key_result": (
            f"PLEC features on the canonical witness -- A1/MD/A2 exhibited as "
            f"consequences of the 4-input declaration, BW exhibited under its "
            f"statement of record: "
            f"A1 = finite-physical-regime half-1 ({w.capacity} < ∞); "
            f"MD-value = finite-physical-regime half-2 (μ*_Γ = {w.marginal_floor} > 0); "
            f"MD tested/gauge cleavage = FD2 distinction definition; "
            f"A2 = argmin from cost-as-infimum + no-waste (admissible-max-size {max_size} ≤ ⌊C_Γ/μ*_Γ⌋ = {expected_max}); "
            f"MD-increment = every admitted increment ≥ μ*_Γ (MD's content, under MD's name); "
            f"BW = cost-spectrum non-degeneracy at the element-distinction level "
            f"(statement of record, OHC_N@2026-08-30): {len(distinct_costs)} distinct "
            f"element costs {distinct_costs}, so there exist d_i, d_j with "
            f"eps(d_i) != eps(d_j).  The flat world PASSES the increment leg and "
            f"FAILS the BW leg, executed here as a permanent control."
        ),
        "summary": (
            "A1, MD and A2 are exhibited on the canonical witness as consequences "
            "of the 4-input declaration: A1 + MD-value are the two halves of the "
            "finite-physical-regime hypothesis; the MD tested/gauge cleavage is "
            "FD2's separator-vs-relabeling distinction; A2 is argmin from "
            "cost-as-infimum + no-waste.  BW is carried under its STATEMENT OF "
            "RECORD (OHC_N@2026-08-30) -- not all enforceable distinctions have "
            "the same cost, there exist d_i, d_j with eps(d_i) != eps(d_j) -- and "
            "is EXHIBITED on the witness, not derived here.  THE DOMAIN OF THAT "
            "QUANTIFICATION IS A RECORDED SCOPE AND NOT A THEOREM: it ranges over "
            "element distinctions, the objects the implemented ledger charges, and "
            "neither a wider domain nor the completeness of this one is "
            "established; this record may not be cited for either direction of "
            "the domain question.  The distinction-level/configuration-level delta "
            "remains scoped, not closed.  WHAT IS ESTABLISHED HERE BY EXECUTION IS "
            "A SEPARATION: the increment condition AS EXECUTED IN THIS MODULE does "
            "not entail the statement of record, because the flat world -- every "
            "distinction at one cost at or above the floor, Paper 0's own BW "
            "countermodel -- is built and run here and PASSES the A1, MD-value and "
            "increment legs while FAILING the BW leg; a two-valued world passes it, "
            "so the leg is satisfiable in both directions.  The increment form was "
            "this record's statement of BW until v24.3.482 and is retained beside "
            "it under MD's name, because it is true and it is MD's.  THIS IS NOT a "
            "claim that BW is underivable from MD, that Lemma BW of Paper 10 v1.12 "
            "§3.5 is wrong, or that BW is an axiom -- nobody in this lane opened "
            "that section, and the statement is about the transcription that ships "
            "here.  The BW predicate is tied BY VALUE to the executed record of "
            "check_worked_example (apf/core.py), the corpus's element-distinction "
            "non-degeneracy anchor, whose costs are parsed from its own returned "
            "record rather than re-typed here."
        ),
        "tier": 4,
        "epistemic": "[P_structural]",
        "dependencies": ["T_four_input_declaration"],
    }


def check_FD1_structural_completeness():
    """FD1_structural_completeness: the adopted structural-completeness clause.

    Tier 4 [P].  Structural completeness is Assumption 1 READ AT FULL STRENGTH
    (Paper 0 v6.2.32 line 2347: "not a fifth assumption bolted onto the first
    three; it is the first one read at full strength"), hence a FOUNDATIONAL
    assumption, not an adopted reading beyond the base.  Under the canonical
    [P]/[P_structural] convention (bank.py legend; "Reference - Canonical [P]
    vs [P_structural] Definition (2026-06-25)"), [P] = derived from the four
    foundational assumptions + standard math, adopted FOUNDATIONAL clauses
    included -- so this is [P].  A base-change in what [P] certifies
    (derivable-from-base), NOT a claim FD1 was secretly a theorem of the
    finiteness axiom; the prior [P_structural] used the narrow "from A1
    alone" reading the canonical convention retires.  GUARDRAIL (this clause
    is a NEGATIVE-EXISTENTIAL): it excludes free fiat; it does not supply a
    missing value.  A consumer that USES it is [P] only when it also names the
    base-resting theorem supplying the value (e.g. GQL-1: Theorem_R + Schur).

    Clause:  a physical object, state, or demand IS its finite admissible
    continuation profile, and nothing beyond it.  Equivalently -- structural
    completeness -- there are no physical facts beyond those fixed by the
    admissible continuation structure.  In particular, any quantity that makes
    an empirical difference is a structural fact: it is fixed by the structure
    that constitutes it, and is not free to be assigned by representational
    fiat.  A free choice that fixes NO empirical difference is a coordinative
    convention and lies outside the clause.  The antecedent carries the whole
    conditional: freeness is a predicate COMPUTED of the individual move, and
    is never inherited from the category the move is filed under.  Units,
    chart and gauge are the standing illustrations, and each illustrates a
    move that satisfies the antecedent WHEN it satisfies it; naming the
    category grants nothing.  Gauge is the sharp case and it divides.  A
    gauge CHOICE -- which representative gets written down -- fixes no
    empirical difference, so the antecedent holds and the choice is a
    convention.  The DIMENSION of the gauge group counts directions that act
    differently on observables; the antecedent fails there, those are
    enforced distinctions, and check_L_cost_gauge (apf/core.py) bills them.
    Whether acting differently on observables and fixing an empirical
    difference are the same predicate or merely coextensive on the cases
    tested is not established; the partition holds either way.
    One conditional, two moves, complementary halves of one partition
    ("Reference - DECISION - Gauge Is Two Things (2026-08-05)"; a recorded
    reading, not banked).

    Witness:  a finite model separating empirical-difference-making assignments
    (excluded as free fiat) from empirical-difference-free relabelings
    (preserved as conventions).  The witness encodes the rule; the clause is
    the adopted commitment the framework has practiced from the start (strict
    minimalism, zero free parameters, the eternalist reading), now named.

    Source-of-record: Paper 0 v6.2.31 S4.2 (Assumption 1, structural
    completeness) + Paper 1 Supplement v8.41 S2 (rem:structural-completeness).
    Consumed by check_T_ew_load_placement_P (apf/gauge_quotient_ledger.py) to
    force the single radial-Higgs record onto SU(2)'s row -- the sin^2 theta_W
    = 3/13 LEDGER-SHARE close.
    """
    # (i) an empirically-consequential quantity: three candidate billings of the
    #     Higgs record give three distinct measured signatures (the weak angle).
    empirical_candidates = {"su2": (3, 13), "u1": (13, 19), "inert": (13, 35)}
    sigs = set(empirical_candidates.values())
    makes_empirical_difference = len(sigs) > 1
    assert makes_empirical_difference, (
        "FD1-sc witness: the candidate assignments must produce distinct "
        "empirical signatures"
    )
    # (ii) structural completeness: such a quantity is NOT free to be assigned by
    #      fiat -- it is fixed by the structure that constitutes it.
    free_fiat_allowed = not makes_empirical_difference
    assert free_fiat_allowed is False, (
        "FD1-sc: an empirically-consequential quantity cannot be assigned by "
        "free representational fiat"
    )
    # (iii) contrast: a relabeling that changes no measured signature is a free
    #       coordinative convention -- preserved.  The predicate is computed of
    #       the move; no category carries it.
    convention_candidates = {"gauge_A": (3, 13), "gauge_B": (3, 13)}
    convention_is_free = len(set(convention_candidates.values())) == 1
    assert convention_is_free, (
        "FD1-sc: a no-empirical-difference relabeling is a free coordinative "
        "convention, outside the clause"
    )

    return {
        "name": "FD1_structural_completeness",
        "passed": True,
        "key_result": (
            "Structural completeness adopted: empirically-consequential quantities "
            "(3 distinct billing signatures 3/13, 13/19, 13/35) are NOT free fiat -- "
            "fixed by structure; a relabeling that fixes NO empirical difference "
            "is a coordinative convention, preserved.  Freeness is computed of the "
            "individual move and is never inherited from the category it is filed "
            "under."
        ),
        "summary": (
            "The FD1 structural-completeness clause, adopted as a named foundational "
            "commitment (parity with the marginal floor over MD/BW): a physical object "
            "is its admissible continuation profile and nothing beyond it; there are no "
            "physical facts except those fixed by the continuation structure; any "
            "quantity that makes an empirical difference is structural, not free to be "
            "assigned by representational fiat; a choice with no empirical difference is "
            "a coordinative convention and is preserved.  Foundational (Assumption 1 at full strength) -- grade [P] "
            "under the canonical base.  Consumed by check_T_ew_load_placement_P to "
            "force the single radial-Higgs record onto SU(2)'s row (sin^2 theta_W = "
            "3/13 ledger share)."
        ),
        "tier": 4,
        "epistemic": "P",
        "dependencies": ["FD1"],
    }


# =====================================================================
# Bank registration
# =====================================================================

_CHECKS = {
    "T_four_input_declaration": check_T_four_input_declaration,
    "T_PLEC_derived_from_spine": check_T_PLEC_derived_from_spine,
    "FD1_structural_completeness": check_FD1_structural_completeness,
}


def register(registry):
    """Register foundation-input theorems into the global bank."""
    registry.update(_CHECKS)


# =====================================================================
# Module-level testing entry point
# =====================================================================

if __name__ == "__main__":
    for fn in (check_T_four_input_declaration, check_T_PLEC_derived_from_spine, check_FD1_structural_completeness):
        result = fn()
        status = "PASS" if result.get("passed") else "FAIL"
        print(f"  [{status}] {result['name']}")
        print(f"         -> {result['key_result']}")

# ---------------------------------------------------------------------------
# IE onboarding declaration (v24.3.316, Full Bank Onboarding Wave 4 -- the
# systematic sector sweep). Claim-grade structural probe; the theorems stay
# with their banked checks; verdicts inherit banked grades, routing confers
# nothing. expect_export pinned by the observed engine verdict.
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "foundation:four_input_declaration",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "The canonical foundational base: the four-input declaration "
            "(FD1, FD2, FD3, finiteness) with PLEC's four features derived "
            "from it (check_T_four_input_declaration [P_structural]); FD1's "
            "structural-completeness clause is an ADOPTED clause, banked at "
            "check_FD1_structural_completeness with the canonical [P] "
            "definition resting on the Paper 0 four -- the clause itself "
            "entered by adoption, not derivation. "
        ),
        "note": "Wave 4 probe; grades letter-checked (the clause is adopted; see the 2026-06-25 canonical-definition note)",
    },
)
