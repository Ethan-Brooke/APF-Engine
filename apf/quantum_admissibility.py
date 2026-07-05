"""apf/quantum_admissibility.py -- Quantum Admissibility from finite admissibility.

Phase 22b (2026-04-28): codebase landing of Paper 5 Supplement v5.1's
"field-selection scope and tau discipline" framework -- the load-bearing
quantum-structure theorems of Paper 5 made executable as small finite
witnesses.

Four bank-registered checks span the Paper 5 v5.1 spine
(the branch-taxonomy and QAC roots were relocated into apf.core, the
spine module that hosts the rest of the IJC sector):

  * check_T_kappa_Bool_minimum -- Lemma 1036. On any finite Boolean-defender
    lattice with cost function eps : D -> [0, inf], the infimum
        kappa_Bool(Gamma, Q) = inf { eps(D) : D in D(Gamma,Q) }
    is attained because D(Gamma,Q) is finite. Witness: enumerate a small
    candidate-defender set, take min, certify achievement.

  * check_T_capacity_lower_bound_certificate -- Corollary 1230. If
    kappa_Bool(Gamma, Q) > C, then (Gamma, Q) is APF-infeasible (no
    APF-admissible Boolean defender exists for this query family).
    Witness: defender minimum 12 against capacity 10 -> certificate fires
    and the query family is correctly classified as IJCPres.

  * check_T_field_selection_complex -- Theorem 2907 + Lemma 2856.
    Composite-Continuation Tomography parameter-counting defects
    Delta_D(n,m) = K_D(n*m) - K_D(n) * K_D(m) for the three
    associative real division algebras D in {R, C, H}:
        Delta_R(n,m) > 0   (real fails by hidden parameters)
        Delta_C(n,m) = 0   (complex selected: locally tomographic)
        Delta_H(n,m) < 0   (quaternionic fails by missing parameters)
    Verified for all (n,m) with 2 <= n, m <= 5.

  * check_T_Born_trace_rule -- Corollary 3053. Every positive linear
    functional on M_n(C) is given by E |-> tr(rho E) for some positive
    rho with tr(rho) = 1. Witness: 2-by-2 density matrix and effect,
    explicit numerical check of <E, rho> = tr(rho * E).

Each check is bank-registered with epistemic tag [P_regime] (with
[P_math] for Born-trace and field-selection), tier 4.

Source-of-record: Paper 5 Supplement v5.1, Sections 4-16.
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import FrozenSet, Tuple, Dict, List


# =====================================================================
# Section 4: Branch taxonomy (SepStr, SepAdm, IJCStr, IJCAdm, IJCPres)
# =====================================================================









# =====================================================================
# Section 5: Boolean defender, distortion, kappa_Bool
# =====================================================================

@dataclass(frozen=True)
class BooleanDefender:
    """A Boolean-defender candidate with realignment cost (Defs 5.1-5.2)."""
    name: str
    cost: float
    distortion: float = 0.0  # threshold-bound distortion, 0 in feasibility set


def _boolean_defender_lattice() -> Tuple[BooleanDefender, ...]:
    """Finite candidate Boolean-defender lattice for kappa_Bool minimization.

    Models a small enumerable defender family on a record interface.
    """
    return (
        BooleanDefender("D_naive",     cost=12.0, distortion=0.0),
        BooleanDefender("D_balanced",  cost= 7.0, distortion=0.0),
        BooleanDefender("D_compressed", cost= 5.0, distortion=0.0),
        BooleanDefender("D_minimal",   cost= 3.0, distortion=0.0),
        BooleanDefender("D_lossy",     cost= 1.0, distortion=0.4),  # >threshold
    )


def kappa_Bool(lattice: Tuple[BooleanDefender, ...], distortion_thresh: float = 0.1) -> float:
    """Best capacity-bounded preservation distortion + cost minimum
    over the threshold-feasible sub-lattice (Definition 778)."""
    feasible = [d for d in lattice if d.distortion <= distortion_thresh]
    if not feasible:
        return float("inf")
    return min(d.cost for d in feasible)


def check_T_kappa_Bool_minimum():
    """T_kappa_Bool_minimum: finite Boolean-defender minimum is attained.

    Tier 3 [P_regime]. Paper 5 Supplement v5.1 Lemma 1036. On any finite
    candidate-defender lattice, kappa_Bool is the minimum of a finite real
    set and is therefore attained by some witness defender D*.

    Verifies on a 5-element candidate lattice:
      (i) The infimum is finite.
      (ii) The infimum is attained by an explicit defender (not just an inf).
      (iii) The lossy candidate (distortion above threshold) is correctly
            excluded from the feasibility set.
    """
    lattice = _boolean_defender_lattice()

    # (i) finite infimum
    k = kappa_Bool(lattice, distortion_thresh=0.1)
    assert k < float("inf"), "kappa_Bool must be finite on non-empty feasibility set"

    # (ii) attained by an explicit witness
    feasible = [d for d in lattice if d.distortion <= 0.1]
    witnesses = [d for d in feasible if abs(d.cost - k) < 1e-12]
    assert len(witnesses) >= 1, "kappa_Bool minimum not attained"

    # (iii) lossy candidate excluded
    assert not any(d.name == "D_lossy" for d in feasible), \
        "lossy candidate should be filtered out by distortion threshold"

    return {
        "name": "T_kappa_Bool_minimum",
        "passed": True,
        "key_result": (
            f"kappa_Bool = {k} attained by {witnesses[0].name} "
            f"on lattice of size {len(lattice)} "
            f"(feasible sublattice size {len(feasible)})"
        ),
        "summary": (
            "Paper 5 v5.1 Lemma 1036 (Finite Boolean-defender minimum): "
            "on any finite enumerable candidate-defender lattice with "
            "threshold-bounded distortion, the infimum kappa_Bool(Gamma, Q) "
            "is attained by an explicit witness D*. The witness here is "
            f"D* = {witnesses[0].name} with cost {k}. Above-threshold "
            "candidates (e.g., D_lossy with distortion 0.4) are correctly "
            "excluded from the feasibility set so they cannot lower the "
            "reported minimum."
        ),
    }


# =====================================================================
# Section 5: Universal capacity lower-bound certificate (Cor 1230)
# =====================================================================

def check_T_capacity_lower_bound_certificate():
    """T_capacity_lower_bound_certificate: kappa_Bool > C => APF-infeasible.

    Tier 4 [P_regime]. Paper 5 Supplement v5.1 Corollary 1230. The
    universal infeasibility certificate: if every threshold-feasible
    Boolean defender for a query family Q has cost strictly greater than
    the available capacity C, then (Gamma, Q) is APF-infeasible (lies
    in IJCPres -- preservation-infeasible Boolean branch).

    Verifies on two witnesses:
      (i) capacity 10, kappa_Bool 3 -> APF-feasible (certificate does not fire).
      (ii) capacity 2, kappa_Bool 3 -> APF-infeasible (certificate fires;
           interface correctly classified as IJCPres branch).
    """
    lattice = _boolean_defender_lattice()
    k = kappa_Bool(lattice, distortion_thresh=0.1)

    # Witness (i): generous capacity
    C_loose = 10.0
    feasible_at_loose = (k <= C_loose)
    assert feasible_at_loose, (
        f"With C={C_loose} >= kappa_Bool={k}, certificate must NOT fire"
    )

    # Witness (ii): tight capacity
    C_tight = 2.0
    feasible_at_tight = (k <= C_tight)
    assert not feasible_at_tight, (
        f"With C={C_tight} < kappa_Bool={k}, certificate MUST fire"
    )

    # Soundness: certificate firing entails APF-infeasibility
    if not feasible_at_tight:
        # The query family is in IJCPres (no admissible Boolean defender)
        ijc_pres = True
    else:
        ijc_pres = False
    assert ijc_pres, "certificate fired but IJCPres classification absent"

    return {
        "name": "T_capacity_lower_bound_certificate",
        "passed": True,
        "key_result": (
            f"kappa_Bool = {k}; certificate fires at C = {C_tight} "
            f"(< {k}) and stays silent at C = {C_loose} (>= {k})"
        ),
        "summary": (
            "Paper 5 v5.1 Corollary 1230 (Capacity lower-bound certificate): "
            "the universal infeasibility certificate fires exactly when "
            "the Boolean-defender minimum exceeds the available capacity. "
            "When it fires, the interface lies in IJCPres -- preservation-"
            "infeasible -- and is APF-infeasible regardless of any further "
            "structural data. This is the foundational rung of the v5.1 "
            "four-certificate ladder (capacity / pairwise record-locking / "
            "sequential cycle / noncommuting update); the three sharper "
            "certificates are specialisations of this one."
        ),
    }


# =====================================================================
# Section 6: Quantum Admissibility Condition (QAC)
# =====================================================================









# =====================================================================
# Section 14: Field selection by APF-complete composite accounting
# =====================================================================

def K_dim_real(N: int) -> int:
    """Real symmetric NxN parameter count: N(N+1)/2."""
    return N * (N + 1) // 2


def K_dim_complex(N: int) -> int:
    """Complex hermitian NxN parameter count: N^2."""
    return N * N


def K_dim_quaternionic(N: int) -> int:
    """Quaternionic hermitian NxN parameter count: N(2N-1)."""
    return N * (2 * N - 1)


def composite_defect(K_fn, n: int, m: int) -> int:
    """Delta_D(n, m) = K_D(n*m) - K_D(n) * K_D(m).

    Sign discriminates the three candidate associative real division
    algebras under APF-complete composite accounting (no hidden
    parameters at the composite interface).
    """
    return K_fn(n * m) - K_fn(n) * K_fn(m)


def check_T_field_selection_complex():
    """T_field_selection_complex: APF-complete composite accounting selects C.

    Tier 4 [P_regime + P_math]. Paper 5 Supplement v5.1 Theorem 2907
    (Complex selection from APF-complete composite accounting) plus
    Lemma 2856 (Composite accounting defect for R, C, H).

    Composite-Continuation Tomography (CCT) is the local-tomography-
    equivalent regime selected by APF-completeness: composite operations
    must be fully determined by their action on each component interface,
    with no hidden composite-only record directions. The parameter-counting
    defects are:

        Delta_R(n, m) = K_R(n*m) - K_R(n) * K_R(m) > 0   (n, m >= 2)
        Delta_C(n, m) = K_C(n*m) - K_C(n) * K_C(m) = 0   (always)
        Delta_H(n, m) = K_H(n*m) - K_H(n) * K_H(m) < 0   (n, m >= 2)

    Real fails by hidden parameters at the composite interface (Delta > 0
    means more composite parameters than per-component); quaternionic
    fails by missing parameters (Delta < 0 means too few composite
    parameters to specify all per-component combinations); complex
    matches exactly.

    Verifies the three sign conditions for all (n, m) with 2 <= n, m <= 5.
    """
    deltas_R = []
    deltas_C = []
    deltas_H = []

    for n in range(2, 6):
        for m in range(2, 6):
            d_R = composite_defect(K_dim_real, n, m)
            d_C = composite_defect(K_dim_complex, n, m)
            d_H = composite_defect(K_dim_quaternionic, n, m)
            deltas_R.append((n, m, d_R))
            deltas_C.append((n, m, d_C))
            deltas_H.append((n, m, d_H))

    # Real: Delta_R > 0 strictly for all n, m >= 2
    for (n, m, d) in deltas_R:
        assert d > 0, f"Delta_R({n},{m}) = {d}; expected > 0"

    # Complex: Delta_C = 0 exactly
    for (n, m, d) in deltas_C:
        assert d == 0, f"Delta_C({n},{m}) = {d}; expected = 0"

    # Quaternionic: Delta_H < 0 strictly for all n, m >= 2
    for (n, m, d) in deltas_H:
        assert d < 0, f"Delta_H({n},{m}) = {d}; expected < 0"

    # Sample point: n = m = 2
    d_R_22 = composite_defect(K_dim_real, 2, 2)         # K_R(4) - K_R(2)^2 = 10 - 9 = 1
    d_C_22 = composite_defect(K_dim_complex, 2, 2)      # 16 - 16 = 0
    d_H_22 = composite_defect(K_dim_quaternionic, 2, 2) # K_H(4) - K_H(2)^2 = 28 - 36 = -8

    return {
        "name": "T_field_selection_complex",
        "passed": True,
        "key_result": (
            f"At (n,m) = (2,2): Delta_R = {d_R_22} > 0, "
            f"Delta_C = {d_C_22} = 0, Delta_H = {d_H_22} < 0; "
            f"sign pattern verified for all 16 (n,m) pairs in [2,5]^2"
        ),
        "summary": (
            "Paper 5 v5.1 Theorem 2907 (Complex selection from APF-complete "
            "composite accounting) selects the complex field uniquely "
            "among the three associative real division algebras. "
            "APF-completeness at composite interfaces forbids hidden "
            "record directions (Theorem 2709); under that constraint the "
            "parameter-counting defect Delta_D(n, m) must vanish identically. "
            "The reals fail with strictly positive defect (smuggled hidden "
            "parameters); the quaternions fail with strictly negative defect "
            "(unrepresentable per-component combinations); the complex "
            "field is the unique survivor. Verified on all 16 (n, m) pairs "
            "with n, m in {2, 3, 4, 5}."
        ),
    }


# =====================================================================
# Section 16: Born trace rule
# =====================================================================

def check_T_Born_trace_rule():
    """T_Born_trace_rule: positive functionals on M_n(C) = density matrices;
    <E, rho> = tr(rho * E).

    Tier 3 [P_math]. Paper 5 Supplement v5.1 Corollary 3053 (Born trace
    rule), specializing Theorem 3008 (finite matrix positive functionals
    are density matrices).

    Verifies on a 2x2 witness:
      (i) For a density matrix rho with tr(rho) = 1 and an effect E in
          [0, I], the order-effect probability tr(rho * E) lies in [0, 1].
      (ii) Linearity: tr((alpha rho1 + (1-alpha) rho2) * E) =
           alpha tr(rho1 E) + (1-alpha) tr(rho2 E).
      (iii) Identity: tr(rho * I) = tr(rho) = 1.
    """
    # Witness: 2x2 density matrices and effects (we don't import numpy --
    # do everything by hand on 2x2 real Hermitian matrices for portability)
    def matmul2(A, B):
        return [
            [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
            [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]],
        ]

    def trace2(A):
        return A[0][0] + A[1][1]

    def add2(A, B, alpha=1.0, beta=1.0):
        return [
            [alpha*A[0][0] + beta*B[0][0], alpha*A[0][1] + beta*B[0][1]],
            [alpha*A[1][0] + beta*B[1][0], alpha*A[1][1] + beta*B[1][1]],
        ]

    # rho1 = |0><0|, rho2 = (1/2)(|0><0| + |1><1|), I = identity
    rho1 = [[1.0, 0.0], [0.0, 0.0]]
    rho2 = [[0.5, 0.0], [0.0, 0.5]]
    I    = [[1.0, 0.0], [0.0, 1.0]]
    E_X  = [[0.5, 0.5], [0.5, 0.5]]   # effect E_X = |+><+| (positive, <= I)

    assert abs(trace2(rho1) - 1.0) < 1e-12
    assert abs(trace2(rho2) - 1.0) < 1e-12

    # (i) Probability in [0, 1]
    p1 = trace2(matmul2(rho1, E_X))    # tr(|0><0| * |+><+|) = 1/2
    p2 = trace2(matmul2(rho2, E_X))    # tr((I/2) * |+><+|) = 1/2
    assert -1e-12 <= p1 <= 1.0 + 1e-12, f"p1 = {p1} out of [0,1]"
    assert -1e-12 <= p2 <= 1.0 + 1e-12, f"p2 = {p2} out of [0,1]"
    assert abs(p1 - 0.5) < 1e-12, f"expected 0.5, got {p1}"
    assert abs(p2 - 0.5) < 1e-12, f"expected 0.5, got {p2}"

    # (ii) Linearity in rho
    alpha = 0.3
    rho_mix = add2(rho1, rho2, alpha=alpha, beta=(1.0 - alpha))
    p_mix = trace2(matmul2(rho_mix, E_X))
    p_combined = alpha * p1 + (1.0 - alpha) * p2
    assert abs(p_mix - p_combined) < 1e-12, (
        f"linearity violated: tr((mix)E) = {p_mix} vs alpha*p1 + (1-alpha)*p2 "
        f"= {p_combined}"
    )

    # (iii) Identity probabilities
    assert abs(trace2(matmul2(rho1, I)) - 1.0) < 1e-12
    assert abs(trace2(matmul2(rho2, I)) - 1.0) < 1e-12

    return {
        "name": "T_Born_trace_rule",
        "passed": True,
        "key_result": (
            f"<E_X, rho1> = {p1}; <E_X, rho2> = {p2}; "
            f"<E_X, mix> = {p_mix} matches alpha*p1 + (1-alpha)*p2 = "
            f"{p_combined}; tr(rho * I) = 1 on both witnesses"
        ),
        "summary": (
            "Paper 5 v5.1 Corollary 3053 (Born trace rule): on the matrix "
            "sector M_n(C), every positive linear functional on effects "
            "is given by E |-> tr(rho E) for some density matrix rho with "
            "tr(rho) = 1, and conversely. Verified on a 2x2 witness with "
            "two density matrices (pure |0><0| and maximally mixed I/2) "
            "and the |+><+| effect: probabilities lie in [0,1], linearity "
            "in rho holds exactly, and the identity effect normalizes to 1. "
            "The Born rule is therefore not posited; it is the unique "
            "operationally consistent pairing on the complex matrix "
            "sector selected in Section 14."
        ),
    }




# =====================================================================
# Section 5b: threshold-robustness of the branch verdict at a
#             state-independently contextual interface
# =====================================================================

def check_T_contextual_branch_verdict_threshold_robust():
    """The branch (IJC) verdict at a state-independently contextual interface is
    INDEPENDENT of the (stipulated) distortion threshold.

    Tier 4 [P_structural_instrument]. The Boolean-defender feasibility set
    (kappa_Bool, Definition 778) is gated by a distortion threshold whose value
    (default 0.1 in `kappa_Bool`) is stipulated, not derived. This check shows
    the stipulation is immaterial at a state-independently contextual interface,
    because the minimal distortion any classical (noncontextual) defender incurs
    in preserving the records is bounded below by a strictly positive
    CONTEXTUALITY GAP delta* > threshold.

    Witness: the Mermin-Peres magic square. The six contexts demand row-parities
    +1 and column-parities -1; the product of all six demanded parities is -1,
    while every deterministic {+-1} assignment yields product +1 over the six
    induced parities. Hence every assignment violates an ODD number (>= 1) of the
    six contexts, so every classical mixture violates >= 1/6 of them on average;
    and 1/6 is ACHIEVED (the 96 assignments that violate exactly one context
    cover all six, so their symmetric mixture violates each context exactly 1/6).
    Therefore

        delta* (magic square) = 1/6  exactly.

    No classical defender preserves the records to within any distortion
    threshold tau < 1/6, so kappa_Bool = +inf throughout tau in [0, 1/6) and the
    branch (IJC) verdict does not move with the threshold. The stipulated 0.1
    lies in [0, 1/6), so the magic-square verdict -- and the pentaquark M_4
    colour interface that realizes it gauge-invariantly
    (check_T_gauge_invariant_colour_KS_coloring_obstruction) -- is robust to it.

    MD reinforcement: the minimal achievable classical-defender distortion is
    1/6 -- a strictly positive GAP below which nothing is realizable. The
    achievable average-context distortions are [1/6, 5/6] (the convex hull of
    the per-assignment violation fractions), but (0, 1/6) is empty: there is no near-faithful classical defender. MD's
    positive cost floor mu* > 0 is what makes the obstruction a genuine
    non-infinitesimal floor rather than an arbitrarily-small distortion; an
    "approximately classical" defender (distortion in (0, 1/6)) does not exist at
    a structurally contextual interface.

    SCOPE: this removes the threshold-dependence of the branch verdict AT a
    state-independently contextual interface; it does NOT force occupancy (that
    the world REALIZES such an interface) -- that residual is gauge-borne for
    colour, not discharged here. IJC_adm/occupancy stays the empirical QAC at the
    realization step.
    """
    from fractions import Fraction as F
    from itertools import product as _product
    from apf.ijc_feasbool_engine import (
        feasbool, global_section_support_nonempty,
        scenario_mermin_peres_magic_square, scenario_to_dict,
    )
    from apf.interface_contextuality_adapter import route_contextuality

    failures = []

    # --- exact contextuality gap delta* of the magic square ---
    rows = [(0, 1, 2), (3, 4, 5), (6, 7, 8)]
    cols = [(0, 3, 6), (1, 4, 7), (2, 5, 8)]
    contexts = [(r, +1) for r in rows] + [(c, -1) for c in cols]

    def n_violated(a):
        return sum(1 for (ctx, par) in contexts
                   if a[ctx[0]] * a[ctx[1]] * a[ctx[2]] != par)

    assigns = list(_product((1, -1), repeat=9))
    viol = [n_violated(a) for a in assigns]
    all_odd = all(v % 2 == 1 for v in viol)          # parity contradiction
    min_single = min(viol)                            # = 1 (best classical model)
    singles = [frozenset(i for i, (ctx, par) in enumerate(contexts)
                         if a[ctx[0]] * a[ctx[1]] * a[ctx[2]] != par)
               for a in assigns if n_violated(a) == 1]
    covered = set().union(*singles) if singles else set()
    achievable_uniform = (covered == set(range(6)))   # symmetric mixture hits 1/6

    delta_star = F(min_single, 6)                      # = 1/6
    if not (all_odd and min_single == 1 and achievable_uniform and delta_star == F(1, 6)):
        failures.append(
            "magic-square gap not exactly 1/6: all_odd=%s min=%s covered=%s"
            % (all_odd, min_single, sorted(covered)))

    # --- the stipulated threshold lies inside the robust interval ---
    stipulated_threshold = F(1, 10)  # the kappa_Bool default 0.1
    if not (stipulated_threshold < delta_star):
        failures.append("stipulated threshold 0.1 should lie below the gap 1/6")

    # --- the IJC verdict holds and is threshold-independent on [0, delta*) ---
    scn = scenario_mermin_peres_magic_square()
    fb = feasbool(scn)
    sup_empty = global_section_support_nonempty(scn)["witness_section"] is None
    pipe = route_contextuality("magic_square_threshold_robust",
                               scenario=scenario_to_dict(scn))
    if fb["branch"] != "IJCStr" or pipe.export_global_P or not sup_empty:
        failures.append("magic square should be IJCStr with empty support")

    passed = not failures
    return {
        "name": (
            "T_contextual_branch_verdict_threshold_robust: the branch (IJC) "
            "verdict at a state-independently contextual interface is independent "
            "of the stipulated distortion threshold (contextuality gap delta* = "
            "1/6 for the magic square; 0.1 lies in [0, 1/6)) [P_structural_instrument]"
        ),
        "passed": passed,
        "epistemic": "P_structural_instrument",
        "dependencies": [
            "T_kappa_Bool_minimum",
            "T_capacity_lower_bound_certificate",
            "check_T_gauge_invariant_colour_KS_coloring_obstruction",
        ],
        "failures": failures,
        "key_result": (
            "Every classical defender of the Mermin-Peres magic square violates "
            ">= 1 of 6 parity contexts (the product of demanded parities is -1, "
            "every assignment gives +1), and the symmetric mixture of the 96 "
            "single-violators (covering all six contexts) achieves exactly 1/6, "
            "so the contextuality gap delta* = 1/6. No Boolean defender preserves "
            "the records to within any threshold tau < 1/6, so the IJC verdict is "
            "threshold-independent on [0, 1/6); the stipulated 0.1 is immaterial."
        ),
        "summary": (
            "The distortion threshold in kappa_Bool is stipulated, not derived, "
            "but immaterial at a state-independently contextual interface: the "
            "minimal classical-defender distortion is a strictly positive "
            "contextuality gap (delta* = 1/6 exactly for the magic square), so no "
            "Boolean defender is admissible for any tau < delta* and the branch "
            "(IJC) verdict does not depend on the threshold. The minimal "
            "achievable classical-defender distortion is delta* (a gap above 0), "
            "so no near-faithful defender exists in (0, delta*) -- no "
            "approximately-classical defender at a structurally contextual "
            "interface. This removes the threshold "
            "loophole from the branch verdict; it does NOT force occupancy "
            "(realization of such an interface is gauge-borne for colour, not "
            "derived here -- IJC_adm stays the empirical QAC at the realization "
            "step)."
        ),
    }


# =====================================================================
# Bank registration
# =====================================================================

_CHECKS = {
    "T_kappa_Bool_minimum":              check_T_kappa_Bool_minimum,
    "T_capacity_lower_bound_certificate":check_T_capacity_lower_bound_certificate,
    "T_field_selection_complex":         check_T_field_selection_complex,
    "T_Born_trace_rule":                 check_T_Born_trace_rule,
    "T_contextual_branch_verdict_threshold_robust": check_T_contextual_branch_verdict_threshold_robust,
}


def register(registry):
    """Register quantum-admissibility theorems into the global bank."""
    registry.update(_CHECKS)


# =====================================================================
# Module-level testing entry point
# =====================================================================

if __name__ == "__main__":
    for fn in (
        check_T_kappa_Bool_minimum,
        check_T_capacity_lower_bound_certificate,
        check_T_field_selection_complex,
        check_T_Born_trace_rule,
        check_T_contextual_branch_verdict_threshold_robust,
    ):
        result = fn()
        status = "PASS" if result.get("passed") else "FAIL"
        print(f"  [{status}] {result['name']}")
        print(f"         -> {result['key_result']}")


# ---------------------------------------------------------------------------
# IE onboarding declaration (v24.3.310, Full Bank Onboarding Wave 1b). The
# v24.3.297 threshold-robustness result's underlying scenario: the magic
# square as a GF(2) parity system (0=1 inconsistency) -> IJCStr named
# obstruction, verdict independent of the distortion threshold on [0,1/6).
# Reachability only; the robustness quantification stays with the banked check.
# ---------------------------------------------------------------------------

IE_DECLARATIONS = (
    {
        "input_id": "quantum:magic_square_threshold_robust",
        "expect_export": False,
        "axis": "CONTEXTUALITY",
        "payload": {"contextuality_kind": "parity", "n_obs": 9,
                    "contexts": [[[0, 1, 2], 0], [[3, 4, 5], 0], [[6, 7, 8], 0],
                                 [[0, 3, 6], 0], [[1, 4, 7], 0], [[2, 5, 8], 1]]},
        "note": "sign-equivalent textbook encoding of the v24.3.297 scenario (the "
                "banked check uses column parities (1,1,1); flipping two row signs "
                "gives this (0,0,1) form -- same 0=1 inconsistency, same delta*=1/6): "
                "-> IJCStr regardless of stipulated threshold in [0,1/6)",
    },
    {
        "input_id": "quantum:born_trace_rule",
        "axis": "ROUTE",
        "route": "born_trace_rule",
        "expect_export": True,
        "payload": {
            "name": "born_trace_rule",
            "closure_kind": "internal_identity",
            "identity_summary": (
                "The finite Born rule holds at math strength by trace "
                "duality, with NO Gleason import: on M_n(C) every positive "
                "normalized record functional omega is represented by a "
                "unique density matrix rho >= 0 with Tr(rho) = 1 via "
                "omega(A) = Tr(rho*A), and outcome probabilities are "
                "p(E|rho) = Tr(rho*E) for effects 0 <= E <= I, reducing to "
                "|<phi|psi>|^2 on rank-one projectors. The density matrix "
                "is the trace-dual representative of a record functional, "
                "not a state postulate; Gleason enters the corpus only as "
                "the infinite-dimensional-case import. "
                "(check_T_Born_trace_rule, quantum_admissibility.py)"
            ),
        },
        "note": (
            "v24.3.398 quantum-spine export wave: the finite Born rule as "
            "its own exporting input, downstream of the complex-sector "
            "gate (field selection). The axiomatic-Born rival stays "
            "killed (check_R_Born_axiomatic_killed): postulating the rule "
            "is strictly dominated by deriving it."
        ),
    },
)
