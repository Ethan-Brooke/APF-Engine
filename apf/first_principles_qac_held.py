"""
first_principles_qac_held.py -- The Zipper Clearance Lane, FP1 / FP3
================================================================================

Charter: Reference - CONTINUATION - The Zipper Clearance Lane (2026-07-23).md
Source:  The Turning (parked)/zipper_clearance_2026-07-23/
         first_principles_qac_held.py (unbanked finite theorem instrument;
         prior blind audit LAND 0.90 with one fix to carry, carried below).

Target: the FP1 / FP3 legs of the First-Principles QAC-Held Reduction, ported
        as a SELF-CONTAINED, stdlib-only, bank-registered module.

TWO THEOREM-LEVEL FACTS (present mediator + active record kernel)
----------------------------------------------------------------------
FP1  L_fp1_present_mediator_required   [P_math]
     A finite terminal relation F(p, c) that depends on BOTH the earlier
     preparation p and the later context c admits NO preparation-only rule and
     NO context-only rule; any local factorization needs a present mediator, and
     the minimal mediator is exactly the quotient of preparations by equality of
     their complete future-response profiles:
         p ~ q  iff  F(p, c) = F(q, c)  for every admissible later context c.
     Minimality is certified against an INDEPENDENT brute-forced minimum-state
     count (not the profile count read back twice), and -- the carried fix --
     an explicit oversized-mediator CONTROL exercises the refutation surface.

FP3  L_fp3_active_record_kernel        [P_math]
     There exist two DISTINCT present mediator states that share the same
     current record yet are distinguished by a later completion (an "active
     record kernel" witness). A distinct-record control confirms the witness
     search genuinely depends on co-record structure (not vacuous).

GRADE
-----
The source frames its content as "conditional finite mathematics only" and
consumes NO A1 premise; both results are exact finite combinatorics. They are
therefore graded [P_math] (not bare [P], which would assert A1-derivation the
code does not contain). physical_premises_certified = False throughout.

SCOPE FENCE (does NOT derive)
-----------------------------
physical realization of a contextually nonfactorizing interface; noncommutativity;
complex structure; Hilbert space; Born weighting. Deterministic finite terminal
relations only. Stochastic / general process defenders are the later FP4
Completion-Process No-Defender leg (fp4_process_defender.py).

MAY NOT BE CITED FROM THIS MODULE
---------------------------------
'occupancy derives quantum' / 'Held => quantum'; any noncommutativity, complex
structure, Hilbert space, or Born content; the present mediator as a PHYSICAL
mediator (it is the minimal-sufficient-statistic mediator of a finite relation).

Tier 4. Non-exporting. Exact / integer arithmetic; no floats.
"""

from __future__ import annotations

from itertools import combinations, product
from typing import Dict, List, Optional, Tuple

FAMILY = "quantum.zipper_fp1_fp3_present_mediator_held"


# =====================================================================
# ported finite-selection machinery (self-contained, stdlib only)
# =====================================================================

class FiniteSelectionProblem:
    """A finite terminal relation F : P x C -> O, totality-checked."""

    def __init__(self, preparations, contexts, relation):
        self.preparations: Tuple = tuple(preparations)
        self.contexts: Tuple = tuple(contexts)
        self.relation: Dict[Tuple, object] = dict(relation)

        if not self.preparations or not self.contexts:
            raise ValueError("nonempty preparation and context sets required")
        if len(set(self.preparations)) != len(self.preparations):
            raise ValueError("preparations must be unique")
        if len(set(self.contexts)) != len(self.contexts):
            raise ValueError("contexts must be unique")

        expected = {(p, c) for p in self.preparations for c in self.contexts}
        actual = set(self.relation)
        if actual != expected:
            raise ValueError(
                "relation must be total on preparations x contexts; "
                "missing={!r}, extra={!r}".format(
                    expected - actual, actual - expected))

    # -- response-profile quotient ------------------------------------

    def response_profile(self, preparation) -> Tuple:
        if preparation not in self.preparations:
            raise KeyError(preparation)
        return tuple(self.relation[(preparation, c)] for c in self.contexts)

    def profile_classes(self) -> Tuple[Tuple[Tuple, Tuple], ...]:
        classes: Dict[Tuple, List] = {}
        for p in self.preparations:
            classes.setdefault(self.response_profile(p), []).append(p)
        return tuple((prof, tuple(mem)) for prof, mem in classes.items())

    # -- nonfactorization tests ---------------------------------------

    def depends_on_preparation(self) -> bool:
        """Some fixed context distinguishes preparations."""
        return any(
            len({self.relation[(p, c)] for p in self.preparations}) > 1
            for c in self.contexts)

    def depends_on_later_context(self) -> bool:
        """Some preparation responds differently to later contexts."""
        return any(
            len({self.relation[(p, c)] for c in self.contexts}) > 1
            for p in self.preparations)

    def jointly_nonfactorizing(self) -> bool:
        return self.depends_on_preparation() and self.depends_on_later_context()

    def early_winner_possible(self) -> bool:
        """F factors through preparation alone (every row constant in c)."""
        return not self.depends_on_later_context()

    def context_only_rule_possible(self) -> bool:
        """F factors through later context alone."""
        return not self.depends_on_preparation()

    # -- canonical mediator theorem -----------------------------------

    def canonical_mediator(self) -> Dict[str, object]:
        """Unique minimal mediator (up to state relabeling): the profile
        quotient. Returns state_of_preparation, profile_of_state, decoder,
        n_states."""
        profile_to_state: Dict[Tuple, int] = {}
        profiles: List[Tuple] = []
        state_of: Dict[object, int] = {}
        for p in self.preparations:
            prof = self.response_profile(p)
            if prof not in profile_to_state:
                profile_to_state[prof] = len(profiles)
                profiles.append(prof)
            state_of[p] = profile_to_state[prof]
        decoder = {(s, c): prof[i]
                   for s, prof in enumerate(profiles)
                   for i, c in enumerate(self.contexts)}
        return {"state_of_preparation": state_of,
                "profile_of_state": tuple(profiles),
                "decoder": decoder,
                "n_states": len(profiles)}

    def validate_mediator(self, state_of_preparation, decoder
                          ) -> Tuple[bool, bool, Tuple[str, ...]]:
        """A valid mediator must (1) reproduce F and (2) never merge two
        preparations whose complete response profiles differ. Returns
        (reproduces_relation, separates_distinct_profiles, errors)."""
        errors: List[str] = []
        reproduction_ok = True
        for p in self.preparations:
            if p not in state_of_preparation:
                errors.append("missing mediator state for {!r}".format(p))
                reproduction_ok = False
                continue
            s = state_of_preparation[p]
            for c in self.contexts:
                key = (s, c)
                if key not in decoder:
                    errors.append("decoder missing {!r}".format(key))
                    reproduction_ok = False
                    continue
                if decoder[key] != self.relation[(p, c)]:
                    errors.append("decoder mismatch at {!r}".format((p, c)))
                    reproduction_ok = False
        separates = True
        if all(p in state_of_preparation for p in self.preparations):
            for pa, pb in combinations(self.preparations, 2):
                profiles_differ = (self.response_profile(pa)
                                   != self.response_profile(pb))
                states_equal = (state_of_preparation[pa]
                                == state_of_preparation[pb])
                if profiles_differ and states_equal:
                    separates = False
                    errors.append(
                        "candidate merges distinct profiles {!r}, {!r}".format(
                            pa, pb))
        return reproduction_ok, separates, tuple(errors)

    def minimum_mediator_cardinality_independent(self) -> int:
        """INDEPENDENT minimality witness. The smallest k for which SOME
        k-state mediator -- a state assignment P -> {0..k-1} plus a decoder
        consistent with F -- reproduces F. Brute-forces state assignments; does
        NOT reuse the response-profile count, so 'n_states == this' is a genuine
        minimality check with a real refutation surface (unlike the tautological
        n_states == len(distinct profiles), which is one quantity twice)."""
        preps = self.preparations
        n = len(preps)
        for k in range(1, n + 1):
            for assignment in product(range(k), repeat=n):
                state_of = dict(zip(preps, assignment))
                decoder: Dict[Tuple, object] = {}
                consistent = True
                for p in preps:
                    for c in self.contexts:
                        key = (state_of[p], c)
                        val = self.relation[(p, c)]
                        if key in decoder and decoder[key] != val:
                            consistent = False
                            break
                        decoder[key] = val
                    if not consistent:
                        break
                if consistent:
                    return k
        return n

    # -- active record-kernel theorem ---------------------------------

    def find_record_kernel_witness(self, record_of_state
                                   ) -> Optional[Dict[str, object]]:
        """Find two co-record mediator states distinguished by completion.
        Returns a witness dict or None."""
        mediator = self.canonical_mediator()
        states = set(range(mediator["n_states"]))
        if set(record_of_state) != states:
            raise ValueError(
                "record map must be total exactly on canonical mediator "
                "states {}; got {}".format(states, set(record_of_state)))
        profiles = mediator["profile_of_state"]
        for sa, sb in combinations(range(mediator["n_states"]), 2):
            if record_of_state[sa] != record_of_state[sb]:
                continue
            pa, pb = profiles[sa], profiles[sb]
            distinguishing = tuple(c for i, c in enumerate(self.contexts)
                                   if pa[i] != pb[i])
            if distinguishing:
                return {"state_a": sa, "state_b": sb,
                        "common_record": record_of_state[sa],
                        "distinguishing_contexts": distinguishing,
                        "profile_a": pa, "profile_b": pb}
        return None


# =====================================================================
# scenarios (stdlib-only builders)
# =====================================================================

def _xor_problem() -> FiniteSelectionProblem:
    """The minimal contextually nonfactorizing relation r = p XOR c.
    Both preparations have DISTINCT profiles, so the canonical mediator has two
    states and (co-record) carries an active record kernel."""
    preps, ctxs = (0, 1), (0, 1)
    rel = {(p, c): p ^ c for p in preps for c in ctxs}
    return FiniteSelectionProblem(preps, ctxs, rel)


def _shared_profile_problem() -> FiniteSelectionProblem:
    """A relation with a REDUNDANT preparation: preps 0 and 1 share a response
    profile, prep 2 differs. The canonical (profile-quotient) mediator merges
    0 and 1 -> two states, the exact minimum. Because a same-profile pair
    exists, a strictly LARGER valid mediator (one state per preparation) also
    exists -- this is the control that gives the minimality leg a live
    refutation surface."""
    preps, ctxs = (0, 1, 2), (0, 1)
    rel = {
        (0, 0): 0, (0, 1): 1,   # profile (0, 1)
        (1, 0): 0, (1, 1): 1,   # profile (0, 1)  -- same as prep 0
        (2, 0): 1, (2, 1): 0,   # profile (1, 0)  -- distinct
    }
    return FiniteSelectionProblem(preps, ctxs, rel)


def _mediator_is_minimal(problem, state_of, decoder) -> bool:
    """The GENUINE minimality predicate, with a real refutation surface.

    A candidate mediator is 'minimal' iff (1) it is a valid factorization of F
    (reproduces F and separates distinct response profiles) AND (2) its distinct
    state count equals the INDEPENDENT brute-forced minimum mediator cardinality.
    Clause (2) is what makes this falsifiable: a valid-but-oversized mediator
    fails it. (Contrast the tautology n_states == len(distinct profiles), which
    compares one quantity with itself and can never fail.)"""
    reproduces, separates, _ = problem.validate_mediator(state_of, decoder)
    n_states = len(set(state_of.values()))
    min_k = problem.minimum_mediator_cardinality_independent()
    return reproduces and separates and (n_states == min_k)


def _oversized_identity_mediator(problem):
    """A VALID but NON-minimal mediator: one distinct state per preparation.
    Whenever two preparations share a response profile this uses strictly more
    states than the minimum, so the minimality predicate must reject it while
    still recognizing it as a valid factorization of F."""
    state_of = {p: i for i, p in enumerate(problem.preparations)}
    decoder = {(i, c): problem.relation[(p, c)]
               for i, p in enumerate(problem.preparations)
               for c in problem.contexts}
    return state_of, decoder


# =====================================================================
# FP1 -- present mediator required + exact minimality (with the carried fix)
# =====================================================================

def check_L_fp1_present_mediator_required():
    """FP1 [P_math]. A jointly context/preparation-dependent finite terminal
    relation admits NO preparation-only rule and NO context-only rule; the
    response-profile quotient is an exact, minimal present mediator.

    CARRIED FIX (prior audit's one finding). The source's profile_quotient_minimal
    leg had no live refutation surface: inside certify() the candidate is always
    the profile quotient, so n_states always equals the minimum and the leg
    cannot fail. This check adds an explicit oversized-mediator CONTROL: in a
    shared-profile scenario the identity mediator (one state per preparation) is
    a VALID factorization but uses strictly more states than the brute-forced
    minimum, and the minimality predicate REJECTS it. If the profile quotient
    were not minimal -- or if the predicate were the tautological
    n_states == len(distinct profiles) -- this control could not fail. Here it
    does, so the minimality claim is genuinely falsifiable."""
    fail: List[str] = []
    prob = _xor_problem()

    depends_p = prob.depends_on_preparation()
    depends_c = prob.depends_on_later_context()
    jointly_nonfactorizing = prob.jointly_nonfactorizing()
    early_winner_impossible = not prob.early_winner_possible()
    context_only_rule_impossible = not prob.context_only_rule_possible()

    med = prob.canonical_mediator()
    reproduces, separates, _ = prob.validate_mediator(
        med["state_of_preparation"], med["decoder"])
    canonical_mediator_exact = reproduces and separates

    n_states = med["n_states"]
    independent_min_k = prob.minimum_mediator_cardinality_independent()
    profile_quotient_minimal = (n_states == independent_min_k)

    # -------- REFUTATION SURFACE (the carried fix) --------
    ctrl = _shared_profile_problem()
    ctrl_med = ctrl.canonical_mediator()
    # (a) the canonical (profile-quotient) mediator is accepted as minimal
    control_minimal_accepted = _mediator_is_minimal(
        ctrl, ctrl_med["state_of_preparation"], ctrl_med["decoder"])
    # (b) the oversized identity mediator is a VALID factorization ...
    ov_state_of, ov_decoder = _oversized_identity_mediator(ctrl)
    ov_reproduces, ov_separates, _ = ctrl.validate_mediator(ov_state_of, ov_decoder)
    control_oversized_is_valid_factorization = ov_reproduces and ov_separates
    # ... but the minimality predicate REJECTS it (this is the falsifying arm)
    control_oversized_rejected = not _mediator_is_minimal(
        ctrl, ov_state_of, ov_decoder)
    refutation_surface_live = (
        control_minimal_accepted
        and control_oversized_is_valid_factorization
        and control_oversized_rejected)

    legs = {
        "depends_on_preparation": depends_p,
        "depends_on_later_context": depends_c,
        "jointly_nonfactorizing": jointly_nonfactorizing,
        "early_winner_impossible": early_winner_impossible,
        "context_only_rule_impossible": context_only_rule_impossible,
        "canonical_mediator_exact": canonical_mediator_exact,
        "profile_quotient_minimal": profile_quotient_minimal,
        "refutation_surface_live": refutation_surface_live,
    }
    for k, v in legs.items():
        if not v:
            fail.append(k)
    passed = not fail

    return {
        "passed": passed,
        "epistemic": "P_math",
        "physical_premises_certified": False,
        "name": "L_fp1_present_mediator_required",
        "tier": 4,
        "family": FAMILY,
        "key_result": (
            "A finite terminal relation depending on both the earlier "
            "preparation and the later context admits no preparation-only and "
            "no context-only rule; the response-profile quotient is an exact, "
            "minimal present mediator (minimum certified vs an independent "
            "brute-force, with an oversized-mediator control that fails when "
            "minimality is violated)."),
        "cross_refs": [
            "A1",
            "T_sep",
            "L_fp4_structural_defender_exists (fp4_process_defender.py)",
            "L_fp4_minimal_clause_and_not_entailed (fp4_process_defender.py)",
        ],
        "refutation_surface": (
            "oversized-mediator control on a shared-profile relation: the "
            "identity mediator (one state per preparation) is a VALID "
            "factorization of F but has more distinct states than the "
            "brute-forced minimum (3 vs 2); the minimality predicate "
            "_mediator_is_minimal REJECTS it (returns False). The tautological "
            "n_states==len(distinct profiles) could never reject anything; this "
            "control does, so profile_quotient_minimal is falsifiable."),
        "minimum_mediator_states": n_states,
        "independent_min_k": independent_min_k,
        "control_minimal_accepted": control_minimal_accepted,
        "control_oversized_is_valid_factorization":
            control_oversized_is_valid_factorization,
        "control_oversized_rejected": control_oversized_rejected,
        "fail_reasons": fail,
    }


# =====================================================================
# FP3 -- active record-kernel witness (co-record states, future-distinguished)
# =====================================================================

def check_L_fp3_active_record_kernel():
    """FP3 [P_math]. Two DISTINCT present mediator states can share the same
    current record yet be distinguished by a later completion -- an active
    record-kernel witness. Demonstrated on the XOR relation: both mediator
    states currently carry record 0, but their future-response profiles differ,
    so a later completion separates them.

    NON-VACUITY CONTROL: when the current record instead DISTINGUISHES the two
    states, the co-record witness search returns None. The witness therefore
    genuinely depends on co-record structure; the search is not a pass-by-
    construction."""
    fail: List[str] = []
    prob = _xor_problem()
    med = prob.canonical_mediator()
    n = med["n_states"]

    # co-record: both mediator states currently share one record
    co_record = {s: 0 for s in range(n)}
    witness = prob.find_record_kernel_witness(co_record)
    active_record_kernel_witness = witness is not None

    # control: distinct records => no co-record kernel witness
    distinct_record = {s: s for s in range(n)}
    witness_ctrl = prob.find_record_kernel_witness(distinct_record)
    distinct_record_control_has_no_witness = witness_ctrl is None

    # the module proves conditional finite mathematics only
    classical_scope_fenced = True

    legs = {
        "canonical_has_multiple_states": n >= 2,
        "active_record_kernel_witness": active_record_kernel_witness,
        "distinct_record_control_has_no_witness":
            distinct_record_control_has_no_witness,
        "classical_scope_fenced": classical_scope_fenced,
    }
    for k, v in legs.items():
        if not v:
            fail.append(k)
    passed = not fail

    witness_serializable = None
    if witness is not None:
        witness_serializable = {
            "state_a": witness["state_a"],
            "state_b": witness["state_b"],
            "common_record": witness["common_record"],
            "distinguishing_contexts": list(witness["distinguishing_contexts"]),
            "profile_a": list(witness["profile_a"]),
            "profile_b": list(witness["profile_b"]),
        }

    return {
        "passed": passed,
        "epistemic": "P_math",
        "physical_premises_certified": False,
        "name": "L_fp3_active_record_kernel",
        "tier": 4,
        "family": FAMILY,
        "key_result": (
            "Two distinct present mediator states share the same current record "
            "yet are distinguished by a later completion -- an active "
            "record-kernel witness exists (finite, deterministic; no "
            "noncommutativity, complex structure, Hilbert space, or Born "
            "content is derived)."),
        "cross_refs": [
            "A1",
            "L_irr",
            "L_fp1_present_mediator_required",
            "L_fp4_minimal_clause_and_not_entailed (fp4_process_defender.py)",
        ],
        "refutation_surface": (
            "distinct-record control: when the current record already "
            "distinguishes the two mediator states, the co-record witness "
            "search returns None. The witness depends on genuine co-record "
            "structure and is not vacuous."),
        "witness": witness_serializable,
        "distinct_record_control_witness_is_none": distinct_record_control_has_no_witness,
        "scope": {
            "noncommutativity_derived": False,
            "complex_structure_derived": False,
            "hilbert_space_derived": False,
            "born_rule_derived": False,
        },
        "fail_reasons": fail,
    }


# =====================================================================
# mutation battery (demonstrates the refutation surfaces fire)
# =====================================================================

def run_mutations():
    """Explicit controls proving each refutation surface is live (returns False
    on the mutated / non-minimal / non-co-record inputs)."""
    r = {}

    # M1 (the carried fix): the minimality predicate REJECTS a valid oversized
    # mediator. If minimality were a tautology this would be True (not rejected).
    ctrl = _shared_profile_problem()
    ov_state_of, ov_decoder = _oversized_identity_mediator(ctrl)
    oversized_predicate_value = _mediator_is_minimal(ctrl, ov_state_of, ov_decoder)
    r["M1_oversized_mediator_predicate_is_False"] = (oversized_predicate_value is False)
    ov_rep, ov_sep, _ = ctrl.validate_mediator(ov_state_of, ov_decoder)
    r["M1_oversized_mediator_is_valid_factorization"] = (ov_rep and ov_sep)

    # M2: the canonical (profile-quotient) mediator IS accepted as minimal.
    ctrl_med = ctrl.canonical_mediator()
    r["M2_canonical_mediator_accepted_minimal"] = _mediator_is_minimal(
        ctrl, ctrl_med["state_of_preparation"], ctrl_med["decoder"])

    # M3: the brute-forced minimum on the shared-profile relation is 2 (< 3),
    # i.e. minimality has real content (there IS a smaller mediator than identity).
    r["M3_independent_minimum_is_strictly_below_identity"] = (
        ctrl.minimum_mediator_cardinality_independent() < len(ctrl.preparations))

    # M4 (FP3): distinct records => no active record-kernel witness.
    prob = _xor_problem()
    n = prob.canonical_mediator()["n_states"]
    r["M4_distinct_record_no_witness"] = (
        prob.find_record_kernel_witness({s: s for s in range(n)}) is None)

    # M5 (FP3): co-record => a witness DOES exist (the positive arm).
    r["M5_co_record_has_witness"] = (
        prob.find_record_kernel_witness({s: 0 for s in range(n)}) is not None)

    r["all_caught"] = all(bool(v) for v in r.values())
    return r


_CHECKS = {
    "L_fp1_present_mediator_required": check_L_fp1_present_mediator_required,
    "L_fp3_active_record_kernel": check_L_fp3_active_record_kernel,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all(verbose=True):
    out = {}
    for name, fn in _CHECKS.items():
        rr = fn()
        out[name] = rr
        if verbose:
            print(("PASS" if rr["passed"] else "FAIL"), name, rr["epistemic"])
    muts = run_mutations()
    out["mutations"] = muts
    if verbose:
        n = sum(1 for k in muts if k.startswith("M"))
        print(("PASS" if muts["all_caught"] else "FAIL"),
              "mutation_battery ({} named controls)".format(n))
        np_ = sum(1 for k, v in out.items()
                  if k != "mutations" and v["passed"])
        print("== {} / {} checks pass; mutations all caught: {}".format(
            np_, len(_CHECKS), muts["all_caught"]))
    return out


if __name__ == "__main__":
    run_all()
