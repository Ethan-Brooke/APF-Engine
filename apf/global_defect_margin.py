"""
global_defect_margin.py -- The Global Attachment-Defect Stability Theorem
================================================================================

Self-contained bank port of the exact combinatorial defect-margin theorem
(P14B). Stdlib only (fractions / itertools / typing); NO scipy / numpy / pool /
lane imports. Non-exporting. Tier 4. ppc = False. Exact arithmetic
(fractions.Fraction); no floats.

WHAT IS BANKED (and ONLY this) -- a precise, EXACT combinatorial theorem about
signed attachment cycles, computed by enumeration for m in {3, 4, 5, 6}.

Object: a signed attachment m-cycle with edge signs sigma_i in {+1, -1}; the
cycle product chi = prod(sigma_i). A COMMUTING THIRD BOAT is a global vertex
sign assignment x_i in {+1, -1}; edge i is satisfied iff x_i * x_{i+1} == sigma_i
(indices cyclic). The DEFECT of an assignment is the fraction of violated edges.

Theorem [P_math], verified EXACTLY by enumeration (Fraction) for m in {3,4,5,6}:

  (1) TWISTED => IRREPARABLE, best commuting defect = 1/m. When chi = -1 no
      global assignment satisfies every edge. Parity law: for every assignment,
      (-1)^defect == chi (because prod_i x_i x_{i+1} = 1 identically, while
      prod_i sigma_i = chi). Hence a twisted cycle forces ODD defect, so the
      best commuting third boat violates EXACTLY ONE edge -- best defect = 1/m.
      This is ENUMERATED (min over all 2^m assignments of the violated-edge
      count over ALL chi = -1 sign patterns), never asserted. Convex mixtures
      of commuting third boats cannot lower the average violation below 1/m
      (the average defect is a convex combination of vertex defects, each
      >= 1/m; witnessed to be ATTAINED by the uniform mixture over the m
      single-edge-optimal assignments, whose per-edge violation probability is
      exactly 1/m). Untwisted (chi = +1) covers have a zero-defect completion.

  (2) ACTIVE PATTERN. The uniform operational active pattern at visibility v has
      P(edge truth) = (1+v)/2, hence active defect = (1-v)/2 = 1 - (1+v)/2.

  (3) STRICT GLOBAL DEFECT DOMINANCE. The active pattern beats EVERY commuting
      third boat exactly when its defect is strictly smaller:
          Delta_stab(v) = 1/m - (1-v)/2 > 0   <=>   v > 1 - 2/m.

  (4) K_{2,2} FOUR-CYCLE (m = 4, the canonical twisted attachment square):
          threshold  v > 1/2,   Delta_stab(v) = (2v - 1)/4.

WHAT IS NOT BANKED (named premises / fenced reading). The step from "strict
global defect dominance" to PROCESS-IJC LOADING is CONDITIONAL, and its
antecedents are the UNFORCED content: a COMPLETE competitor set (all commuting
third boats enumerated) and an EXACT attachment-defect burden dictionary. The
theorem does NOT derive that APF's generic stability gate carries this complete,
competitor-relative meaning; that missing bridge is FENCED, not closed. The
conditional is billed at [P_structural_instrument] in
check_T_defect_margin_conditional_bridge with physical_premises_certified=False.

MAY NOT BE CITED FROM THIS MODULE (see MAY_NOT_CITE):
  'the loading is derived' -- it is CONDITIONAL on the unforced defect-burden
  dictionary + the complete-competitor-set antecedent; neither is forced.
  any '[P]' grade on Process-IJC realization -- the bridge is
  [P_structural_instrument], physical_premises_certified = False.
  'v > 1/2 is forced' -- v > 1 - 2/m is the boundary of a CONDITIONAL defect
  dominance, not a forced physical visibility.
"""

from __future__ import annotations

from fractions import Fraction as F
from itertools import product
from typing import Dict, List, Sequence, Tuple

FAMILY = "quantum.global_attachment_defect_margin"

# Claims this module's results do NOT support and that MUST NOT be cited from
# any of its checks.
MAY_NOT_CITE: Tuple[str, ...] = (
    "the loading is derived (it is CONDITIONAL on the unforced defect-burden "
    "dictionary + the complete-competitor-set antecedent; neither is forced)",
    "any '[P]' grade on Process-IJC realization (the bridge is "
    "[P_structural_instrument], physical_premises_certified=False)",
    "'v > 1/2 is forced' (v > 1 - 2/m is the boundary of a CONDITIONAL defect "
    "dominance, not a forced physical visibility)",
    "'APF's generic stability gate carries this complete competitor-relative "
    "meaning' (that bridge is fenced here, not closed)",
)

# Banked concordances (cited, NOT re-derived). The m = 4 twisted cycle is the
# CHSH / Boole four-cycle facet structure.
CROSS_REFS: Tuple[str, ...] = (
    "fp4_process_defender (the measurement-incompatibility gate; the m=4 "
    "twisted cycle is the CHSH/Boole facet structure)",
    "ijc_boolean_defender_bridge (CHSH raw-count box disjoint from the "
    "Boole/local polytope via a Fine facet)",
    "T_IJC_dichotomy; commutative_no_unresolved_hold (.412 coherence-witness)",
)


# ---------------------------------------------------------------------------
# exact combinatorics on a signed attachment m-cycle (stdlib only)
# ---------------------------------------------------------------------------

def _cycle_product(signs: Sequence[int]) -> int:
    p = 1
    for s in signs:
        p *= int(s)
    return p


def _all_assignments(m: int):
    return product((-1, 1), repeat=m)


def _defect_count(signs: Sequence[int], assignment: Sequence[int]) -> int:
    """Number of edges i where x_i * x_{i+1} != sigma_i (indices cyclic)."""
    m = len(signs)
    return sum(
        1
        for i in range(m)
        if assignment[i] * assignment[(i + 1) % m] != signs[i]
    )


def _best_third_boat_defect_count(signs: Sequence[int]) -> int:
    """EXACT best commuting third boat: the MINIMUM violated-edge count over
    ALL 2^m global sign assignments. Enumerated, never asserted."""
    return min(_defect_count(signs, a) for a in _all_assignments(len(signs)))


def _best_third_boat_defect_fraction(signs: Sequence[int]) -> F:
    return F(_best_third_boat_defect_count(signs), len(signs))


def _defect_spectrum(signs: Sequence[int]) -> Tuple[int, ...]:
    return tuple(sorted({_defect_count(signs, a)
                         for a in _all_assignments(len(signs))}))


def _single_edge_optimal_assignments(
    signs: Sequence[int],
) -> Dict[int, Tuple[int, ...]]:
    """One global assignment per edge that violates EXACTLY that edge. For a
    twisted (chi = -1) cycle one such assignment exists for every edge (solving
    x_i x_{i+1} = sigma_i off the target edge and = -sigma_i on it is
    consistent: the product of the RHS around the cycle is -chi = 1). Found by
    enumeration; the uniform mixture over these witnesses attains the 1/m
    floor."""
    m = len(signs)
    reps: Dict[int, Tuple[int, ...]] = {}
    for a in _all_assignments(m):
        violated = [i for i in range(m)
                    if a[i] * a[(i + 1) % m] != signs[i]]
        if len(violated) == 1 and violated[0] not in reps:
            reps[violated[0]] = a
    return reps


def _canonical_twisted(m: int) -> Tuple[int, ...]:
    """One -1 edge, the rest +1: chi = -1, the canonical twisted m-cycle."""
    return tuple([1] * (m - 1) + [-1])


def _active_defect_fraction(v: F) -> F:
    """Uniform active pattern at visibility v: P(truth) = (1+v)/2, so the active
    defect fraction is (1-v)/2."""
    return (F(1) - v) / 2


def _dominance_threshold(m: int) -> F:
    """Strict global defect dominance boundary: active beats every commuting
    third boat iff v > 1 - 2/m."""
    return F(1) - F(2, m)


def _stability_margin(d_third: F, v: F) -> F:
    """Delta_stab = d_third* - d_active(v)."""
    return d_third - _active_defect_fraction(v)


# ---------------------------------------------------------------------------
# T_global_defect_margin -- the exact combinatorial theorem [P_math]
# ---------------------------------------------------------------------------

def check_T_global_defect_margin():
    """[P_math] The exact global attachment-defect stability theorem, computed
    by enumeration (Fraction) for m in {3, 4, 5, 6}.

    ENUMERATED (not asserted):
      - parity law: (-1)^defect == chi for EVERY assignment of EVERY sign
        pattern (forces the min-defect parity);
      - twisted (chi = -1): the best commuting third-boat defect = 1/m, i.e.
        the MINIMUM violated-edge count over all 2^m assignments equals 1, over
        ALL chi = -1 sign patterns (not just the canonical one);
      - untwisted (chi = +1): a zero-defect completion exists;
      - convex-mixture floor = 1/m, ATTAINED by the uniform mixture over the m
        single-edge-optimal assignments (per-edge violation probability 1/m;
        no mixture beats the vertex minimum, which is 1/m).
    DERIVED exactly:
      - active defect = (1-v)/2 = 1 - (1+v)/2;
      - strict dominance  Delta_stab(v) = 1/m - (1-v)/2 > 0  <=>  v > 1 - 2/m;
      - K_{2,2} (m = 4): threshold 1/2, margin (2v - 1)/4.

    The load-bearing status of every helper (enumerator, defect kernel, active
    identity, threshold, margin, mixture witness) is confirmed EXTERNALLY by the
    real monkeypatch battery in run_mutations(): each helper is corrupted in
    turn, this check is re-run, and passed is verified to flip to False. The
    genuine tooth twisted_best_is_1_over_m already refutes any inflated defect;
    dominance_iff_ok already refutes any shifted threshold."""
    fail_reasons: List[str] = []
    ms = (3, 4, 5, 6)
    v_samples = (F(0), F(1, 3), F(1, 2), F(2, 3), F(1))
    per_m: Dict[int, dict] = {}

    parity_law_ok = True
    twisted_best_is_1_over_m = True
    untwisted_has_zero_defect = True
    mixture_floor_ok = True
    active_identity_ok = True
    dominance_iff_ok = True
    k22_threshold_ok = None
    k22_margin_ok = None

    for m in ms:
        twisted = [s for s in _all_assignments(m) if _cycle_product(s) == -1]
        untwisted = [s for s in _all_assignments(m) if _cycle_product(s) == 1]

        # parity law over ALL assignments of ALL sign patterns
        for s in _all_assignments(m):
            chi = _cycle_product(s)
            for a in _all_assignments(m):
                if (-1) ** _defect_count(s, a) != chi:
                    parity_law_ok = False
                    fail_reasons.append(f"m={m}: parity law violated")

        # (1) twisted best defect = 1/m by ENUMERATION over all twisted patterns
        for s in twisted:
            if _best_third_boat_defect_count(s) != 1:
                twisted_best_is_1_over_m = False
                fail_reasons.append(
                    f"m={m}: a twisted pattern has enumerated best defect != 1")
                break
        for s in untwisted:
            if _best_third_boat_defect_count(s) != 0:
                untwisted_has_zero_defect = False
                fail_reasons.append(
                    f"m={m}: an untwisted pattern lacks a 0-defect completion")
                break

        canon = _canonical_twisted(m)
        d_third = _best_third_boat_defect_fraction(canon)  # ENUMERATED
        if d_third != F(1, m):
            twisted_best_is_1_over_m = False
            fail_reasons.append(
                f"m={m}: enumerated canonical best defect {d_third} != 1/{m}")

        # (2) convex-mixture floor = 1/m via the m single-edge-optimal witnesses
        reps = _single_edge_optimal_assignments(canon)
        witness_full = (len(reps) == m)
        edge_viol_prob = [
            F(sum(1 for j in reps
                  if reps[j][k] * reps[j][(k + 1) % m] != canon[k]), m)
            for k in range(m)
        ]
        mixture_avg_over_edges = sum(edge_viol_prob, F(0)) / m if m else None
        mixture_avg_defect = (
            sum(F(_defect_count(canon, reps[j]), m) for j in reps) / m
            if reps else None
        )
        this_mix_ok = (
            witness_full
            and all(p == F(1, m) for p in edge_viol_prob)
            and mixture_avg_over_edges == F(1, m)
            and mixture_avg_defect == F(1, m)
            and d_third == F(1, m)  # vertex minimum: no mixture beats it
        )
        if not this_mix_ok:
            mixture_floor_ok = False
            fail_reasons.append(f"m={m}: convex-mixture floor != 1/m")

        # (3) active-defect identity
        for v in v_samples:
            if _active_defect_fraction(v) != F(1) - (F(1) + v) / 2:
                active_identity_ok = False
                fail_reasons.append(f"m={m}, v={v}: active defect != (1-v)/2")

        # (4) dominance <=> v > 1 - 2/m (below / at / above + full rational grid)
        thr = _dominance_threshold(m)
        below, at, above = thr - F(1, 100), thr, thr + F(1, 100)
        margin_at = _stability_margin(d_third, at)
        this_dom_ok = (
            (_stability_margin(d_third, below) > 0) is False
            and (_stability_margin(d_third, at) > 0) is False
            and margin_at == 0
            and (_stability_margin(d_third, above) > 0) is True
        )
        for num in range(0, 21):
            vv = F(num, 20)
            if (_stability_margin(d_third, vv) > 0) != (vv > thr):
                this_dom_ok = False
        if not this_dom_ok:
            dominance_iff_ok = False
            fail_reasons.append(f"m={m}: dominance predicate != (v > 1 - 2/m)")

        # (5) K_{2,2}
        if m == 4:
            k22_threshold_ok = (thr == F(1, 2))
            k22_margin_ok = all(
                _stability_margin(d_third, v) == (2 * v - 1) / 4
                for v in v_samples
            )
            if not k22_threshold_ok:
                fail_reasons.append("K22: threshold != 1/2")
            if not k22_margin_ok:
                fail_reasons.append("K22: margin != (2v-1)/4")

        per_m[m] = {
            "twisted_best_defect_fraction": str(d_third),
            "defect_spectrum_canonical": _defect_spectrum(canon),
            "dominance_threshold": str(thr),
            "margin_at_threshold": str(margin_at),
            "single_edge_witness_full": witness_full,
            "mixture_avg_defect": str(mixture_avg_defect),
        }

    passed = (
        parity_law_ok and twisted_best_is_1_over_m
        and untwisted_has_zero_defect and mixture_floor_ok
        and active_identity_ok and dominance_iff_ok
        and k22_threshold_ok is True and k22_margin_ok is True
    )

    return {
        "passed": passed,
        "name": "T_global_defect_margin",
        "family": FAMILY,
        "epistemic": "P_math",
        "tier": 4,
        "physical_premises_certified": False,
        "key_result": (
            "twisted m-cycle best commuting third-boat defect = 1/m "
            "(ENUMERATED for m in {3,4,5,6}; general m via the parity identity "
            "(-1)^defect = chi, forcing odd >= 1 defect on every twisted cycle); "
            "active defect = (1-v)/2; strict dominance <=> v > 1 - 2/m; "
            "K22 (m=4): v>1/2, margin (2v-1)/4"),
        "cross_refs": CROSS_REFS,
        "may_not_cite": MAY_NOT_CITE,
        "fail_reasons": fail_reasons,
        "ms_tested": ms,
        "parity_law_minus1_pow_defect_equals_chi": parity_law_ok,
        "twisted_best_defect_is_1_over_m_enumerated": twisted_best_is_1_over_m,
        "untwisted_has_zero_defect_completion": untwisted_has_zero_defect,
        "convex_mixture_floor_is_1_over_m": mixture_floor_ok,
        "active_defect_identity_ok": active_identity_ok,
        "dominance_iff_v_gt_1_minus_2_over_m": dominance_iff_ok,
        "k22_threshold_is_one_half": k22_threshold_ok,
        "k22_margin_is_2v_minus_1_over_4": k22_margin_ok,
        "per_m": per_m,
    }


# ---------------------------------------------------------------------------
# T_defect_margin_conditional_bridge -- the CONDITIONAL loading instrument
# ---------------------------------------------------------------------------

def check_T_defect_margin_conditional_bridge():
    """[P_structural_instrument] The CONDITIONAL Attachment Pattern Stability
    bridge:

        complete competitor set  +  exact attachment-defect burden
        +  strict global defect dominance   =>   Process-IJC loading.

    Billed CONDITIONAL. The antecedents -- a COMPLETE commuting-competitor set
    and an EXACT defect-burden dictionary -- are the UNFORCED content: named
    premises about the interface, NOT derived here. The theorem does NOT
    establish that APF's generic stability gate carries this complete,
    competitor-relative meaning; that bridge is FENCED, not closed
    (generic_apf_stability_gate_identified_with_margin = False;
    physical_stability_law_derived = False; physical_premises_certified = False).

    Verified on the canonical twisted K22 four-cycle:
      weak (v = 1/3 < 1/2):   margin < 0, NOT strict, NOT loaded;
      boundary (v = 1/2):     margin = 0, NOT strict, NOT loaded;
      strong (v = 2/3 > 1/2): margin > 0, strict, loaded (conditionally);
      trivial cover (chi = +1 flat, v = 1): a zero-defect completion exists,
        NEVER loaded (control).
    Strictness is LOAD-BEARING: the boundary is unloaded while the strong case
    loads. TEETH: a '>= 0' mutation of the dominance test would wrongly load the
    boundary; that mutation is exhibited and caught."""
    fail_reasons: List[str] = []

    def receipt(signs, v):
        v = F(v)
        chi = _cycle_product(signs)
        d3 = _best_third_boat_defect_fraction(signs)   # ENUMERATED
        margin = _stability_margin(d3, v)
        strict = margin > 0
        # the two UNFORCED, NAMED antecedents (stipulated for the argument):
        complete_competitor_set = True
        defect_burden_exact = True
        forced_conditionally = (chi == -1 and strict
                                and complete_competitor_set
                                and defect_burden_exact)
        return {"chi": chi, "d_third": d3, "margin": margin,
                "strict": strict, "forced": forced_conditionally}

    k22 = (1, 1, 1, -1)
    weak = receipt(k22, F(1, 3))
    boundary = receipt(k22, F(1, 2))
    strong = receipt(k22, F(2, 3))
    trivial = receipt((1, 1, 1, 1), F(1))

    weak_ok = (weak["strict"] is False and weak["forced"] is False)
    boundary_ok = (boundary["margin"] == 0 and boundary["strict"] is False
                   and boundary["forced"] is False)
    strong_ok = (strong["strict"] is True and strong["forced"] is True)
    trivial_ok = (trivial["forced"] is False)
    strictness_load_bearing = (boundary["forced"] is False
                               and strong["forced"] is True)

    # TEETH: a '>= 0' mutation of the dominance test wrongly loads the boundary
    mut_forces_boundary = (boundary["chi"] == -1 and boundary["margin"] >= 0)
    strictness_teeth_caught = (mut_forces_boundary is True
                               and boundary["forced"] is False)

    # FENCES -- the theorem does NOT do these:
    generic_apf_stability_gate_identified_with_margin = False
    physical_stability_law_derived = False

    if not weak_ok:
        fail_reasons.append("weak (v<1/2) should be unloaded")
    if not boundary_ok:
        fail_reasons.append("boundary (v=1/2) should be unloaded with margin 0")
    if not strong_ok:
        fail_reasons.append("strong (v>1/2) should be conditionally loaded")
    if not trivial_ok:
        fail_reasons.append("trivial chi=+1 cover should never be loaded")
    if not strictness_load_bearing:
        fail_reasons.append("strictness not load-bearing")
    if not strictness_teeth_caught:
        fail_reasons.append("strictness fail-control not caught")

    passed = (
        weak_ok and boundary_ok and strong_ok and trivial_ok
        and strictness_load_bearing and strictness_teeth_caught
        and generic_apf_stability_gate_identified_with_margin is False
        and physical_stability_law_derived is False
    )

    return {
        "passed": passed,
        "name": "T_defect_margin_conditional_bridge",
        "family": FAMILY,
        "epistemic": "P_structural_instrument",
        "tier": 4,
        "physical_premises_certified": False,
        "key_result": (
            "CONDITIONAL: complete competitor set + exact defect burden + "
            "strict dominance (v > 1 - 2/m) => Process-IJC loading; antecedents "
            "UNFORCED; generic stability gate NOT identified with the margin "
            "(fenced)"),
        "cross_refs": CROSS_REFS,
        "may_not_cite": MAY_NOT_CITE,
        "fail_reasons": fail_reasons,
        "weak_v_1_3_unloaded": weak_ok,
        "boundary_v_1_2_unloaded_margin_zero": boundary_ok,
        "strong_v_2_3_conditionally_loaded": strong_ok,
        "trivial_cover_never_loaded": trivial_ok,
        "strictness_load_bearing": strictness_load_bearing,
        "strictness_fail_control_caught": strictness_teeth_caught,
        "complete_competitor_set_is_named_unforced_premise": True,
        "defect_burden_exact_is_named_unforced_premise": True,
        "generic_apf_stability_gate_identified_with_margin":
            generic_apf_stability_gate_identified_with_margin,
        "physical_stability_law_derived": physical_stability_law_derived,
        "receipts": {
            "weak": {"v": "1/3", "margin": str(weak["margin"]),
                     "forced": weak["forced"]},
            "boundary": {"v": "1/2", "margin": str(boundary["margin"]),
                         "forced": boundary["forced"]},
            "strong": {"v": "2/3", "margin": str(strong["margin"]),
                       "forced": strong["forced"]},
            "trivial": {"chi": trivial["chi"], "forced": trivial["forced"]},
        },
    }


# ---------------------------------------------------------------------------
# run_mutations -- REAL monkeypatch battery: corrupt each load-bearing helper,
# re-run the banked check, confirm passed flips to False (independent teeth)
# ---------------------------------------------------------------------------


def run_mutations():
    """REAL monkeypatch mutation battery (INDEPENDENT teeth).

    Each named mutation temporarily overwrites ONE load-bearing helper on this
    module's namespace, RE-RUNS the actual banked check (main or bridge), then
    restores the helper in a finally-block. A genuine tooth means the corrupted
    run's own verdict flips to passed=False. This is NOT a read-back of
    self-reported flags: it proves every enumerator / kernel / identity /
    threshold / margin / witness is load-bearing by breaking it and watching the
    banked theorem fail. A "<name>_caught" value of True means the mutation was
    caught (the check FAILED under it); "all_caught" requires BOTH baselines to
    pass AND every mutation to be caught.
    """
    G = globals()
    r: Dict[str, bool] = {}

    # baselines: with nothing mutated, both banked checks pass
    r["baseline_main_passes"] = \
        check_T_global_defect_margin()["passed"] is True
    r["baseline_bridge_passes"] = \
        check_T_defect_margin_conditional_bridge()["passed"] is True

    def _caught(check, helper, bad):
        """Overwrite module helper `helper` with `bad`, re-run `check`, restore
        it. Returns True iff the check FAILED under the mutation (tooth bit)."""
        original = G[helper]
        G[helper] = bad
        try:
            broke = check()["passed"] is False
        finally:
            G[helper] = original
        return broke

    main = check_T_global_defect_margin
    bridge = check_T_defect_margin_conditional_bridge

    # --- main-check helpers: each corruption must break the theorem ---
    r["M1_corrupt_best_defect_enumerator_caught"] = _caught(
        main, "_best_third_boat_defect_count", lambda signs: 2)
    r["M2_corrupt_defect_count_kernel_caught"] = _caught(
        main, "_defect_count", lambda signs, a: 0)
    r["M3_corrupt_active_defect_identity_caught"] = _caught(
        main, "_active_defect_fraction", lambda v: F(1))
    r["M4_corrupt_dominance_threshold_caught"] = _caught(
        main, "_dominance_threshold", lambda m: F(1) - F(1, m))
    r["M5_corrupt_stability_margin_caught"] = _caught(
        main, "_stability_margin", lambda d, v: F(0))
    r["M6_corrupt_mixture_witness_caught"] = _caught(
        main, "_single_edge_optimal_assignments", lambda signs: {})

    # --- bridge helpers: the enumerated defect and the margin feed the loading ---
    r["M7_bridge_corrupt_enumerated_defect_caught"] = _caught(
        bridge, "_best_third_boat_defect_fraction", lambda signs: F(0))
    r["M8_bridge_corrupt_stability_margin_caught"] = _caught(
        bridge, "_stability_margin", lambda d, v: F(1))

    r["all_caught"] = all(r.values())
    return r


_CHECKS = {
    "T_global_defect_margin": check_T_global_defect_margin,
    "T_defect_margin_conditional_bridge": check_T_defect_margin_conditional_bridge,
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
            print(("PASS" if rr["passed"] else "FAIL"), name,
                  "[" + rr["epistemic"] + "]")
    muts = run_mutations()
    out["mutations"] = muts
    if verbose:
        n = sum(1 for k in muts if k.startswith("M"))
        print(("PASS" if muts["all_caught"] else "FAIL"),
              "mutation_battery ({} named)".format(n))
        np_ = sum(1 for k, v in out.items()
                  if k != "mutations" and v["passed"])
        print("== {} / {} checks pass; mutations all caught: {}".format(
            np_, len(_CHECKS), muts["all_caught"]))
    return out


if __name__ == "__main__":
    run_all()
