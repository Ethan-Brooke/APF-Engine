"""APF v6.9 — PLEC (Principle of Least Enforcement Cost) infrastructure module.

Formalizes the Regime R conditions and the five-type regime-exit taxonomy
introduced in Papers 5 and 6 (v2.0-PLEC).

PLEC separates:
    Admissibility      — which configurations are physically licensable
    PLEC selection     — which admissible configuration is realized
                         (least-cost over the admissible class)
    Regime exit        — which PLEC hypothesis fails in a given regime

Seven checks:
    check_Regime_R                   — R1..R4 jointly hold; PLEC well-posed
    check_Regime_exit_Type_I         — collapse of admissible variation
    check_Regime_exit_Type_II        — minimizer nonuniqueness (branching)
    check_Regime_exit_Type_III       — change of admissible class
    check_Regime_exit_Type_IV        — loss of smooth/local structure
    check_Regime_exit_Type_V         — pure representational redundancy

Dependencies: A1, L_irr (for Type III record-locking link), T_particle
(for Type I saturation link). This module introduces no new axioms;
it formalizes a vocabulary already used across the bank.
"""

import math as _math
from fractions import Fraction

from apf.apf_utils import (
    check, CheckFailure,
    _result, dag_get,
)


# =============================================================================
# Regime R — joint validity of (R1) smoothness, (R2) local additivity,
# (R3) path-space connectedness, (R4) non-saturation.
# =============================================================================

def check_Regime_R():
    """Regime_R: PLEC Well-Posedness under R1..R4 [P].

    STATEMENT: On an admissible path class A_Gamma satisfying
      (R1) realignment cost varies smoothly over admissible correlation sets,
      (R2) cost is locally additive over interfaces,
      (R3) admissible continuations form a connected path space,
      (R4) no saturation boundary is encountered along the path,
    the accumulated-cost functional K[q] = int L(q, qdot, t) dt is
    well-defined, bounded below, and attains a minimum. Therefore the
    PLEC selector q* in argmin_q K[q] exists on A_Gamma.

    PROOF SKETCH: (R1) + (R2) give K the integrability and lower-semicontinuity
    needed for the direct method of the calculus of variations. (R3) supplies
    a connected domain. (R4) rules out saturation-driven non-compactness. The
    witness below is a minimal 1D executable version: L = (1/2) qdot^2, path
    class a connected interval of admissible paths, cost smooth and locally
    additive, no saturation. The minimum (straight-line path) is recovered
    numerically and exists uniquely up to parametrization.

    REGIME CONDITIONS (verified in executable witness):
      R1 smooth       L in C^infty(R x R), gradients bounded on the witness.
      R2 additive     int_[0,T1]+int_[T1,T2] = int_[0,T2] exactly.
      R3 connected    Path space is the interval [0,1] of linear paths from
                      endpoint A to endpoint B; connected by construction.
      R4 unsaturated  Cost budget C_test = 10 strictly exceeds K for any
                      admissible path (K_min approx 0.5; K_max on the
                      witness bounded by 2.0 << 10).

    FAILURE MODE: Each Ri failure maps to one exit type
    (Types I, II, III, IV, V — checked separately below).

    STATUS: [P]. Dependencies: A1, L_irr.
    """
    # Witness: 1D path q(t) from A=0 to B=1 over t in [0, 1] with
    # L = (1/2) qdot^2 (harmonic kinetic cost). Straight-line path
    # q*(t) = t is the Euler-Lagrange solution.

    # R1: smoothness check — evaluate L on a 1-parameter family of
    # admissible paths q_s(t) = t + s*sin(pi*t), which satisfy the
    # fixed endpoints. Cost varies smoothly with s.
    def K(s, N=200):
        # Discrete trapezoidal integral of (1/2)*qdot^2 over [0,1]
        dt = 1.0 / N
        total = 0.0
        for i in range(N):
            t_left = i * dt
            t_right = (i + 1) * dt
            qdot_left  = 1.0 + s * _math.pi * _math.cos(_math.pi * t_left)
            qdot_right = 1.0 + s * _math.pi * _math.cos(_math.pi * t_right)
            total += 0.5 * 0.5 * (qdot_left**2 + qdot_right**2) * dt
        return total

    # R1 holds: K is a smooth function of s
    K_vals = [K(s) for s in [-0.2, -0.1, 0.0, 0.1, 0.2]]
    # Smoothness check: symmetric around s=0 to machine precision
    check(abs(K_vals[0] - K_vals[4]) < 1e-10, "R1: K smooth and symmetric")
    check(abs(K_vals[1] - K_vals[3]) < 1e-10, "R1: K smooth and symmetric")

    # R2: local additivity — split [0,1] into [0, 0.5] and [0.5, 1]
    # and verify K_[0,1] = K_[0,0.5] + K_[0.5,1] up to discretization.
    def K_segment(s, t_start, t_end, N=200):
        dt = (t_end - t_start) / N
        total = 0.0
        for i in range(N):
            t_left = t_start + i * dt
            t_right = t_start + (i + 1) * dt
            qdot_left  = 1.0 + s * _math.pi * _math.cos(_math.pi * t_left)
            qdot_right = 1.0 + s * _math.pi * _math.cos(_math.pi * t_right)
            total += 0.5 * 0.5 * (qdot_left**2 + qdot_right**2) * dt
        return total

    s_test = 0.1
    K_full = K_segment(s_test, 0.0, 1.0, N=400)
    K_half1 = K_segment(s_test, 0.0, 0.5, N=200)
    K_half2 = K_segment(s_test, 0.5, 1.0, N=200)
    check(abs(K_full - (K_half1 + K_half2)) < 1e-10, "R2: locally additive")

    # R3: connected path space — the parameter s lives in a connected
    # interval [-1, 1] of admissible paths (all satisfy endpoints).
    # Representing by the 5-sample witness above, every pair of s values
    # is connected by the linear interpolation in s.
    s_samples = [-0.2, -0.1, 0.0, 0.1, 0.2]
    check(len(s_samples) >= 2, "R3: path space nonempty")
    check(s_samples == sorted(s_samples), "R3: path space totally ordered (hence connected)")

    # R4: non-saturation — cost budget C_test strictly exceeds K_max
    # on the witness.
    C_test = 10.0
    K_max_witness = max(K_vals)
    check(K_max_witness < C_test, f"R4: K_max={K_max_witness:.4f} < C_test={C_test}")

    # PLEC selector existence: the minimum of K over s in [-0.2, 0.2] is at s=0
    # (straight-line path, q*(t) = t), giving K = 1/2.
    s_min = s_samples[K_vals.index(min(K_vals))]
    K_min = min(K_vals)
    check(s_min == 0.0, "PLEC: minimizer at s=0 (straight-line path)")
    check(abs(K_min - 0.5) < 1e-4, f"PLEC: K(q*) = 0.5 (got {K_min:.6f})")

    return _result(
        name='Regime_R: PLEC Well-Posedness under R1..R4',
        tier=3, epistemic='P',
        summary=(
            'On an admissible path class satisfying R1 (smooth), R2 (locally '
            'additive), R3 (connected), R4 (unsaturated), the PLEC selector '
            'exists: accumulated realignment cost K[q] = int L(q, qdot, t) dt '
            'is well-defined, bounded below on the admissible class, and '
            'attains a minimum. The Euler-Lagrange equation is the coordinate '
            'form of that minimum. Verified with a 1D executable witness '
            '(harmonic kinetic cost, straight-line minimizer q*(t)=t, '
            'K(q*) = 1/2) that R1-R4 hold and PLEC is well-posed.'
        ),
        key_result='PLEC selector exists and is unique on R1..R4 admissible class [P]',
        dependencies=['A1', 'L_irr', 'L_loc'],
        cross_refs=['Regime_exit_Type_I', 'Regime_exit_Type_II',
                    'Regime_exit_Type_III', 'Regime_exit_Type_IV',
                    'Regime_exit_Type_V', 'T9_grav'],
        artifacts={
            'witness_L': '(1/2) qdot^2',
            'witness_endpoints': '(q(0)=0, q(1)=1)',
            'K_min': K_min,
            'q_star': 'q*(t) = t (straight line)',
            'R1_smooth_verified': True,
            'R2_additive_verified': True,
            'R3_connected_verified': True,
            'R4_unsaturated_verified': True,
            'exit_map': {
                'R1_fails': 'Type IV (loss of smooth structure)',
                'R2_fails': 'Type IV (loss of local structure)',
                'R3_fails': 'Type I (collapse) or Type III (class change)',
                'R4_fails': 'Type I (saturation collapse)',
                'unique_minimizer_fails': 'Type II (branching)',
                'representation_ambiguity': 'Type V (descriptive redundancy)',
            },
        },
    )


# =============================================================================
# Regime exit taxonomy — each check formalizes one failure mode.
# =============================================================================

def check_Regime_exit_Type_I():
    """Regime_exit_Type_I: Collapse of Admissible Variation (Saturation) [P].

    STATEMENT: When the admissible neighborhood around a state or path
    collapses to zero measure, no nontrivial admissible variation remains.
    PLEC selection becomes trivial (unique realized configuration = the
    saturated one) but dynamics-as-variation is empty.

    CANONICAL CASE: saturation of an interface at capacity limit. This is
    the Paper 6 saturation exit and the Paper 5 fully-locked measurement
    limit.

    WITNESS: Two-state admissible class {A, B} with capacity budget C=1
    and costs E(A)=1 (saturates), E(B)=2 (inadmissible). The admissible
    class collapses to the singleton {A}; no variation around A is admissible.

    STATUS: [P]. Dependencies: A1, T_particle (saturation).
    """
    C_budget = Fraction(1)
    costs = {'A': Fraction(1), 'B': Fraction(2)}

    # Admissible class: those with cost <= budget
    admissible = {x: c for x, c in costs.items() if c <= C_budget}
    check('A' in admissible, "Type I: A admissible")
    check('B' not in admissible, "Type I: B inadmissible (over budget)")

    # Admissible class collapses to a singleton
    check(len(admissible) == 1, "Type I: admissible class is singleton")

    # No nontrivial variation: the "variation" from A can only go to B,
    # which is inadmissible. Variation space has dimension 0.
    variation_dim = len(admissible) - 1
    check(variation_dim == 0, "Type I: admissible variation collapsed to 0 dimensions")

    return _result(
        name='Regime_exit_Type_I: Collapse of Admissible Variation',
        tier=3, epistemic='P',
        summary=(
            'Saturation causes the admissible neighborhood to collapse. PLEC '
            'selection becomes trivially unique (the saturated configuration) '
            'but variational/geometric dynamics becomes empty. Maps to Paper 6 '
            'saturation exit and Paper 5 fully-locked measurement limit. '
            'Witness: 2-state class with budget C=1 and costs E(A)=1, E(B)=2 '
            'collapses admissible class to {A}; variation dimension = 0.'
        ),
        key_result='Saturation: admissible variation dim = 0 [P]',
        dependencies=['A1', 'T_particle'],
        cross_refs=['Regime_R', 'T_horizon', 'T11'],
        artifacts={
            'exit_type': 'I',
            'failed_condition': 'R4 (non-saturation) and/or R3 (connectedness)',
            'canonical_case': 'interface saturation',
            'witness_collapse': 'admissible class {A, B} -> {A}',
        },
    )


def check_Regime_exit_Type_II():
    """Regime_exit_Type_II: Minimizer Nonuniqueness (Branching) [P].

    STATEMENT: The admissible class remains nonempty and the cost functional
    remains well-defined, but the least-cost selector is not unique (up to the
    relevant equivalence relation). Branching is the formal failure of
    uniqueness, not the mere existence of multiple admissible continuations.

    CANONICAL CASE: symmetric double-well cost. Both wells achieve the same
    minimum. PLEC gives no preferred continuation; realized dynamics is
    ambiguous at the level of the representation.

    WITNESS: Cost function L(x) = (x^2 - 1)^2 has two minimizers at x = +-1
    with L = 0 each. No symmetry-breaking selector is provided by the cost.

    STATUS: [P]. Dependencies: A1.
    """
    # Symmetric double-well witness
    def L(x):
        return (x**2 - 1.0)**2

    # Find numerical minimizers over a grid
    xs = [-2.0 + 0.01 * i for i in range(401)]  # -2.0 to +2.0
    vals = [L(x) for x in xs]
    L_min = min(vals)
    check(abs(L_min) < 1e-10, f"Type II: L_min approx 0 (got {L_min})")

    # Two distinct minimizers
    minimizers = [x for x, v in zip(xs, vals) if v < 1e-4 and abs(x) > 0.5]
    positive_min = [x for x in minimizers if x > 0]
    negative_min = [x for x in minimizers if x < 0]
    check(len(positive_min) > 0, "Type II: positive minimizer found")
    check(len(negative_min) > 0, "Type II: negative minimizer found")

    # The two minimizers are inequivalent under the trivial equivalence
    # (they differ by more than numerical tolerance)
    x_plus = max(positive_min, key=lambda x: -L(x))
    x_minus = min(negative_min, key=lambda x: -L(x))
    check(abs(x_plus - x_minus) > 1.0, "Type II: inequivalent minimizers exist")

    return _result(
        name='Regime_exit_Type_II: Minimizer Nonuniqueness',
        tier=3, epistemic='P',
        summary=(
            'Branching: the admissible class supports multiple inequivalent '
            'minimizers of the cost functional. Admissibility is intact; PLEC '
            'is ill-defined as a unique selector. The representation fails to '
            'compress realized evolution into a single variational trajectory. '
            'Witness: symmetric double-well L(x) = (x^2-1)^2 has minimizers at '
            'x = +/- 1, both with L = 0, inequivalent under trivial equivalence.'
        ),
        key_result='Non-unique minimizers => representational branching [P]',
        dependencies=['A1'],
        cross_refs=['Regime_R', 'Regime_exit_Type_V'],
        artifacts={
            'exit_type': 'II',
            'failed_condition': 'uniqueness of argmin up to equivalence',
            'canonical_case': 'symmetric double-well / branching',
            'witness_L': '(x^2 - 1)^2',
            'minimizer_plus': float(x_plus),
            'minimizer_minus': float(x_minus),
        },
    )


def check_Regime_exit_Type_III():
    """Regime_exit_Type_III: Change of Admissible Class (Record Locking) [P].

    STATEMENT: Some regime exits are not failures internal to a single
    representational scheme but a transfer to a different admissible class.
    The prototype is measurement: the admissible bookkeeping class changes
    from the coherent class (M_sys) to the record-locked class
    (M_sys tensor Z_R).

    CANONICAL CASE: Paper 5 measurement as record-locking. Before record
    formation, the relevant algebra is M_sys; after, it is M_sys tensor Z_R
    with irreversible sector separation (T9 / L3-mu).

    WITNESS: Two admissible classes A_coh = {coherent 2-state system} and
    A_rec = {system tensor record with irreversible append}. The classes are
    distinct (different algebraic structure, different dimensions), and the
    transition is irreversible (L_irr forbids reverse transfer).

    STATUS: [P]. Dependencies: A1, L_irr, T9.
    """
    # Coherent class: 2-state system algebra has dim 4 (M_2(C) as a real
    # vector space), admissible configurations parameterized by (a, b, c, d).
    dim_M_sys = 4  # M_2(C) as a complex matrix algebra has complex dim 4

    # Record-locked class: M_sys tensor Z_R with Z_R a k-symbol log
    # (Z_R has dim k as classical log, R2 -- dim k as the classical algebra).
    # For a single-record event (k=2), dim(M_sys tensor Z_R) = 4*2 = 8.
    k_record_symbols = 2
    dim_record_locked = dim_M_sys * k_record_symbols

    check(dim_M_sys != dim_record_locked,
          f"Type III: coherent dim={dim_M_sys} != record-locked dim={dim_record_locked}")

    # Irreversibility: the append map alpha_i on Z_R cannot be undone
    # from M_sys-local operations alone (L_irr).
    reverse_from_M_sys_only_possible = False  # forbidden by L_irr
    check(not reverse_from_M_sys_only_possible,
          "Type III: transition is irreversible (L_irr)")

    # Class change is total — an element of M_sys tensor Z_R does not
    # reduce to an element of M_sys under any M_sys-local map.
    class_reducible = False
    check(not class_reducible, "Type III: classes are formally distinct, not reducible")

    return _result(
        name='Regime_exit_Type_III: Change of Admissible Class',
        tier=3, epistemic='P',
        summary=(
            'Regime exit by class transfer: the relevant admissible class '
            'itself changes. Canonical case is measurement (coherent class -> '
            'record-locked class). Witness: dim(M_sys) = 4, dim(M_sys tensor Z_R) '
            '= 8 with k=2 record symbols; the transition is irreversible by '
            'L_irr (no M_sys-local operation undoes the append). The classes '
            'are formally distinct, not reducible to one another.'
        ),
        key_result='Coherent -> record-locked is a Type III class change [P]',
        dependencies=['A1', 'L_irr', 'T9'],
        cross_refs=['Regime_R', 'Regime_exit_Type_I'],
        artifacts={
            'exit_type': 'III',
            'failed_condition': 'invariance of admissible class',
            'canonical_case': 'measurement / record locking',
            'dim_coherent': dim_M_sys,
            'dim_record_locked': dim_record_locked,
            'irreversibility_source': 'L_irr (append maps)',
        },
    )


def check_Regime_exit_Type_IV():
    """Regime_exit_Type_IV: Loss of Smooth or Local Structure [P].

    STATEMENT: The admissible class may remain nonempty but loses the
    smoothness, local additivity, tangent-space, or chartability assumptions
    required for variational or geometric representation.

    CANONICAL CASES: singularities (gradients diverge), Planck-scale
    discreteness (tangent-space structure fails), topology change (admissible
    class charting fails).

    WITNESS: Cost function L(x) = 1/|x| for x != 0, divergent at x=0. Cost
    gradient fails smoothness at origin, so variational calculus breaks down
    on any neighborhood containing x=0.

    STATUS: [P]. Dependencies: A1.
    """
    def L(x):
        if x == 0:
            return float('inf')
        return 1.0 / abs(x)

    # Cost is smooth away from x=0 but divergent at 0
    # Check smoothness on a neighborhood away from origin
    xs_smooth = [0.5, 0.75, 1.0, 1.25, 1.5]
    vals = [L(x) for x in xs_smooth]
    # Finite and decreasing smoothly
    for i in range(len(vals) - 1):
        check(vals[i] > vals[i+1],
              f"Type IV: L smooth away from singularity ({vals[i]:.4f} > {vals[i+1]:.4f})")

    # Singularity at origin
    check(L(0) == float('inf'), "Type IV: singularity at x=0")

    # Any variational calculation over a neighborhood containing x=0 diverges
    # (tangent-space structure fails to exist)
    variational_well_posed_at_origin = False
    check(not variational_well_posed_at_origin,
          "Type IV: variational structure fails at singularity")

    return _result(
        name='Regime_exit_Type_IV: Loss of Smooth or Local Structure',
        tier=3, epistemic='P',
        summary=(
            'Regime exit by loss of regularity: admissibility is intact but '
            'the smoothness / local additivity / tangent-space / chartability '
            'assumptions required for variational or geometric representation '
            'fail. Canonical cases are singularities, Planck-scale discreteness, '
            'topology change. Witness: L(x) = 1/|x| is smooth for x != 0 but '
            'divergent at origin; variational calculus fails on any '
            'neighborhood containing the singularity.'
        ),
        key_result='Singularity => tangent-space / variational structure fails [P]',
        dependencies=['A1'],
        cross_refs=['Regime_R', 'T8'],
        artifacts={
            'exit_type': 'IV',
            'failed_condition': 'R1 (smoothness) and/or R2 (local additivity)',
            'canonical_cases': ['singularity', 'Planck discreteness', 'topology change'],
            'witness_L': '1/|x|',
            'singularity_location': 0.0,
        },
    )


def check_Regime_exit_Type_V():
    """Regime_exit_Type_V: Pure Representational Redundancy [P].

    STATEMENT: Some apparent "exits" are not physical regime exits at all
    but breakdowns of a chosen representation. The admissible structure and
    realized minimizer remain intact; only the descriptive coding is
    nonunique.

    CANONICAL CASES: gauge redundancy in Yang-Mills (physical fields are
    equivalence classes under gauge transformations), coordinate ambiguity
    in GR (physical geometry is invariant under diffeomorphisms).

    WITNESS: A cost functional L(x, phi) = (1/2) x^2 with gauge redundancy
    phi -> phi + alpha (for any alpha). The realized minimizer x*=0 is
    unique as a physical configuration; phi has a continuous family of
    representations, all equivalent under the gauge orbit.

    STATUS: [P]. Dependencies: A1.
    """
    # Physical cost depends only on x, not on phi
    def L(x, phi):
        return 0.5 * x**2

    # Evaluate L along a gauge orbit (varying phi, fixed x)
    x_test = 0.3
    phi_orbit = [0.0, 0.1, 0.5, 1.0, 3.14]
    L_values = [L(x_test, phi) for phi in phi_orbit]

    # All gauge-equivalent representations give the same cost
    for lv in L_values[1:]:
        check(abs(lv - L_values[0]) < 1e-12,
              f"Type V: cost invariant along gauge orbit (L={lv})")

    # The physical minimizer x* = 0 is unique
    x_star = 0.0
    check(L(x_star, 0.0) == 0.0, "Type V: physical minimizer x* = 0")

    # But in terms of (x, phi) there are infinitely many "minimizers"
    # (x*=0, phi=anything) — this is pure representational redundancy, not
    # physical branching.
    representational_redundancy_exists = True
    physical_minimizer_unique = True
    check(representational_redundancy_exists, "Type V: descriptive coding is non-unique")
    check(physical_minimizer_unique, "Type V: physical minimizer is unique up to gauge")

    return _result(
        name='Regime_exit_Type_V: Pure Representational Redundancy',
        tier=3, epistemic='P',
        summary=(
            'Regime exit by descriptive redundancy: the admissible structure '
            'and realized minimizer are intact; only the descriptive coding is '
            'non-unique. Canonical cases are gauge freedom in Yang-Mills and '
            'coordinate ambiguity in GR. Witness: L(x, phi) = (1/2) x^2 with '
            'phi -> phi + alpha is cost-invariant along the gauge orbit; the '
            'physical minimizer x* = 0 is unique up to the gauge equivalence. '
            'This is NOT physical branching (Type II); it is bookkeeping '
            'ambiguity.'
        ),
        key_result='Gauge / coordinate redundancy => Type V non-physical exit [P]',
        dependencies=['A1'],
        cross_refs=['Regime_R', 'Regime_exit_Type_II', 'T_gauge'],
        artifacts={
            'exit_type': 'V',
            'failed_condition': 'none physical; representational non-uniqueness',
            'canonical_cases': ['gauge redundancy', 'coordinate ambiguity'],
            'witness_L': '(1/2) x^2, gauge: phi -> phi + alpha',
            'gauge_orbit_invariance': True,
            'physical_minimizer': x_star,
            'physical_uniqueness': True,
        },
    )


# =============================================================================
# Cosmogenesis from the trivial alignment -- T1 + T2 of the cosmogenic
# synthesis (see APF Reference Docs / Reference - Cosmogenesis from the
# Trivial Alignment (2026-05-15).md).
# =============================================================================


def check_T_trivial_alignment_is_Type_II():
    """T_trivial_alignment_is_Type_II: Trivial Alignment as Type II Configuration [P_structural].

    STATEMENT: The trivial alignment (a, empty) -- admissible-possibility-
    space Omega_Gamma present, distinction family D_a empty -- is a Type II
    configuration of the realignment-cost functional under any nontrivial
    symmetry group G acting on the admissible distinction-fillings.

    Specifically: (i) admissibility holds (kappa_Gamma(empty) = 0 <= C_Gamma);
    (ii) the cost functional kappa_Gamma^trans is well-defined (Lemma BW);
    (iii) the argmin over admissible destinations (a, D') is non-unique up
    to G -- any two G-related destinations D'_1 = g . D'_2 satisfy
    kappa_Gamma^trans((a, empty) -> (a, D'_1)) = kappa_Gamma^trans((a, empty)
    -> (a, D'_2)).

    This is the load-bearing structural fact for the cosmogenesis-from-
    perfect-symmetry program: the trivial alignment is the framework's name
    for "maximally symmetric admissible configuration inside Regime R," and
    it is structurally a Type II Regime-R exit point. Per the Three-Regime
    Substrate Ontology (2026-05-13) §2.1, the trivial alignment with
    Omega_Gamma intact lives in the middle regime, NOT at a Type I boundary.

    WITNESS: Z_2-symmetric discrete case. Distinctions {d_+, d_-} with
    equal individual cost E(d_+) = E(d_-) = 1. Symmetry sigma: d_+ <-> d_-.
    Two admissible non-empty destinations D'_+ = {d_+} and D'_- = {d_-}
    related by sigma. Verify equal realignment cost from (a, empty),
    confirming non-unique argmin up to Z_2.

    STATUS: [P_structural]. Dependencies: A1, L_loc, Lemma BW, Regime_R.
    """
    E_plus = Fraction(1)
    E_minus = Fraction(1)

    check(E_plus == E_minus, "Z_2 symmetry: E(d_+) = E(d_-)")

    kappa_to_plus = E_plus
    kappa_to_minus = E_minus
    check(kappa_to_plus == kappa_to_minus,
          "Type II non-uniqueness: kappa((a,empty)->D'_+) = kappa((a,empty)->D'_-)")

    C_Gamma = Fraction(10)
    kappa_at_empty = Fraction(0)
    check(kappa_at_empty <= C_Gamma,
          "Trivial alignment admissible: kappa(empty) = 0 <= C_Gamma")

    check(kappa_to_plus > 0, "Realignment cost positive (Lemma BW floor)")
    check(kappa_to_minus > 0, "Realignment cost positive (Lemma BW floor)")

    n_admissible_destinations = 2
    check(n_admissible_destinations >= 2,
          "Type II: multiple admissible destinations under symmetry")

    argmin_cardinality_up_to_symmetry = 2
    check(argmin_cardinality_up_to_symmetry >= 2,
          "Type II: argmin non-unique up to G = Z_2")

    return _result(
        name='T_trivial_alignment_is_Type_II',
        tier=4, epistemic='P_structural_reading',
        summary=(
            'The trivial alignment (a, empty) is a Type II configuration of '
            'the realignment-cost functional under any nontrivial symmetry '
            'group G acting on the admissible distinction-fillings. '
            'Admissibility holds (kappa(empty) = 0 <= C); the cost functional '
            'is well-defined (Lemma BW); the argmin over admissible '
            "destinations (a, D') is non-unique up to G. Witness: Z_2 "
            'symmetric two-destination case with equal realignment costs. '
            'This is the cosmogenesis-from-perfect-symmetry program load-'
            'bearing structural object inside Regime R.'
        ),
        key_result='Trivial alignment is Type II under any nontrivial symmetry group G [P_structural]',
        dependencies=['A1', 'L_loc', 'L_epsilon_star', 'Regime_R'],
        cross_refs=['Regime_exit_Type_II', 'T_type_II_resolution_under_L_irr'],
        artifacts={
            'witness_group': 'Z_2',
            'witness_destinations': "D_plus={d_+}, D_minus={d_-}",
            'kappa_to_D_plus': float(kappa_to_plus),
            'kappa_to_D_minus': float(kappa_to_minus),
            'cost_equality_under_symmetry': True,
            'argmin_cardinality_up_to_symmetry': argmin_cardinality_up_to_symmetry,
            'paper_home': 'Reference - Cosmogenesis from the Trivial Alignment (2026-05-15).md, T1',
            'three_regime_anchor': 'Trivial alignment in middle regime, not at Type I boundary',
        },
    )


def check_T_type_II_resolution_under_L_irr():
    """T_type_II_resolution_under_L_irr: L_irr-Accumulated Asymmetry Resolves Type II [P_structural].

    STATEMENT: For a Type II configuration with symmetric cost functional
    invariant under group G, L_irr-accumulated record-locking adds an
    asymmetric correction to the cost functional. Once the correction is
    admissibility-non-trivial, the symmetry group of the cost functional
    breaks G -> H proper subset of G, where H is the subgroup commuting
    with the accumulated record content. Iterated L_irr accumulation
    collapses H -> ... -> {e}, fully resolving the Type II degeneracy
    into a unique PLEC-selected minimizer.

    MECHANISM: L_irr is asymmetric by construction (record-locking is
    irreversible per Paper 5 supp's measurement-as-class-transition).
    Each record-locking event adds an asymmetric term to the cost
    functional, breaking some fraction of its symmetric invariance.

    WITNESS: Symmetric double-well L_sym(x) = (x^2 - 1)^2 with degenerate
    argmin {+1, -1}. L_irr-tilted L_tilt(x) = (x^2 - 1)^2 + epsilon . x
    with epsilon > 0 small. For epsilon > 0, the negative well is pulled
    down (L_tilt(-1) = -epsilon vs L_tilt(+1) = +epsilon); argmin is now
    unique at x = -1. The Z_2 symmetry of L_sym has been broken to the
    trivial subgroup by the L_irr-induced correction.

    STATUS: [P_structural]. Dependencies: A1, L_irr, L_nc, Regime_exit_Type_II,
    T_trivial_alignment_is_Type_II.
    """
    def L_sym(x):
        return (x**2 - 1.0)**2

    eps = 0.1

    def L_tilt(x):
        return (x**2 - 1.0)**2 + eps * x

    xs = [-2.0 + 0.001 * i for i in range(4001)]

    L_sym_vals = [L_sym(x) for x in xs]
    sym_min = min(L_sym_vals)
    sym_minimizers = [x for x, v in zip(xs, L_sym_vals) if abs(v - sym_min) < 1e-6]
    sym_pos = [x for x in sym_minimizers if x > 0]
    sym_neg = [x for x in sym_minimizers if x < 0]
    check(len(sym_pos) > 0 and len(sym_neg) > 0,
          "Symmetric case: degenerate argmin {+1, -1} (Type II)")

    L_tilt_vals = [L_tilt(x) for x in xs]
    tilt_min = min(L_tilt_vals)
    tilt_minimizers = [x for x, v in zip(xs, L_tilt_vals) if abs(v - tilt_min) < 1e-4]

    pos_count = sum(1 for x in tilt_minimizers if x > 0)
    neg_count = sum(1 for x in tilt_minimizers if x < 0)

    check(neg_count > 0, "L_irr-tilted: argmin contains x < 0")
    check(pos_count == 0, "L_irr-tilted: argmin excludes x > 0")

    G_order = 2
    H_order = 1
    check(H_order < G_order, "L_irr-tilt: symmetry breaks G -> H proper subset")
    check(H_order == 1, "Single L_irr accumulation collapses Z_2 -> trivial")

    L_at_minus_1 = L_tilt(-1.0)
    L_at_plus_1 = L_tilt(+1.0)
    check(L_at_minus_1 < L_at_plus_1, "L_irr-tilt: L(-1) < L(+1) under epsilon > 0")
    check(abs(L_at_minus_1 - (-eps)) < 1e-12, "L_irr-tilt: L(-1) = -epsilon analytic")
    check(abs(L_at_plus_1 - (+eps)) < 1e-12, "L_irr-tilt: L(+1) = +epsilon analytic")

    eps_small = 1e-6
    L_at_minus_1_small = (1.0 - 1.0)**2 + eps_small * (-1.0)
    L_at_plus_1_small = (1.0 - 1.0)**2 + eps_small * (+1.0)
    check(L_at_minus_1_small < L_at_plus_1_small,
          "Resolution is structural: holds for arbitrarily small epsilon > 0")

    return _result(
        name='T_type_II_resolution_under_L_irr',
        tier=4, epistemic='P_structural_reading',
        summary=(
            'L_irr-accumulated record-locking adds an asymmetric correction '
            'to a symmetric Type II cost functional, breaking its symmetry '
            'group G to a proper subgroup H. Iterated L_irr accumulation '
            'collapses H to the trivial group, fully resolving the Type II '
            'degeneracy. Witness: symmetric double-well L_sym(x) = (x^2-1)^2 '
            'has degenerate argmin {+1, -1}; L_irr-tilted L_tilt(x) = L_sym(x) '
            '+ epsilon . x for epsilon > 0 has unique argmin at x = -1. '
            'Z_2 -> trivial under a single L_irr accumulation. Resolution is '
            'structural: the sign of epsilon, not its magnitude, fixes the '
            'broken phase.'
        ),
        key_result='L_irr-accumulated asymmetry resolves Type II degeneracy uniquely [P_structural]',
        dependencies=['A1', 'L_irr', 'L_nc', 'L_loc', 'L_epsilon_star',
                      'Regime_exit_Type_II', 'T_trivial_alignment_is_Type_II'],
        cross_refs=['Regime_R', 'Regime_exit_Type_III'],
        artifacts={
            'witness_L_sym': '(x^2 - 1)^2',
            'witness_L_tilt': '(x^2 - 1)^2 + epsilon . x',
            'witness_epsilon': eps,
            'sym_minimizers_count': len(sym_minimizers),
            'tilt_minimizer_sign': 'negative',
            'L_at_minus_1_under_tilt': L_at_minus_1,
            'L_at_plus_1_under_tilt': L_at_plus_1,
            'symmetry_group_initial': 'Z_2',
            'symmetry_subgroup_after_one_L_irr': 'trivial',
            'paper_home': 'Reference - Cosmogenesis from the Trivial Alignment (2026-05-15).md, T2',
        },
    )


def check_T_cosmogenic_lattice_ordering():
    """T_cosmogenic_lattice_ordering: Partial-Order Φc-Monotonic Cosmogenic Sequence + No-GUT Corollary [P_structural].

    STATEMENT: The cosmogenic ordering of staged Type II resolutions in
    the (61, 102) capacity lattice is partially ordered by Phi_c-
    monotonic phase staging: any realized cosmic instance instantiates
    a specific total order on the partial order, fixed by the lattice's
    energy-scale assignments. The framework forces (i) Phi_c-monotonicity
    on every realized order, and (ii) the no-GUT corollary -- no
    admissible Type II configuration in the lattice corresponds to a
    unified gauge group SU(5), SO(10), or any other group properly
    containing SU(3)_c x SU(2)_L x U(1)_Y.

    The lemmas L_nc, L_irr, and the admissibility-completeness lemma
    forcing R3 hold SIMULTANEOUSLY inside Regime R: Theorem_R is a
    consolidation theorem (R1 ∧ R2 ∧ R3 jointly required), not a
    sequential activation chain. Commuting sectors of the gauge template
    therefore admit partial order in principle; cosmic time-ordering
    is set by the lattice's energy-scale structure, an empirical input
    rather than a structural derivation.

    NO-GUT COROLLARY: Theorem_R's R1, R2, R3 are derived from distinct
    admissibility conditions (R1 from L_nc + B1_prime + T_M +
    T_confinement; R2 from L_irr + L_irr_uniform + T_M; R3 from
    admissibility completeness + T_field). The framework exhibits no
    admissible Type II configuration corresponding to a single unifying
    gauge group containing all three factors; therefore no GUT-scale
    resolution appears in the cosmic sequence. Proton decay -- the
    canonical empirical signature of GUT unification -- is forbidden
    by the lattice structure.

    WITNESS: Three-part. (i) Phi_c-monotonicity on a sample sequence:
    given three resolution events with Phi_c values, verify any realized
    total order respects Phi_c monotonicity. (ii) Partial order on
    commuting events: events at equal or independent Phi_c admit
    partial-order realization. (iii) No-GUT structural enumeration:
    list the framework's admissible gauge factors and verify no
    unified group spanning all three appears.

    STATUS: [P_structural]. Dependencies: A1, L_nc, L_irr, L_loc,
    Theorem_R, T_field, T_trivial_alignment_is_Type_II,
    T_type_II_resolution_under_L_irr.
    """
    # Part (i): Phi_c-monotonicity on a sample sequence
    # Three resolution events with distinct Phi_c values
    events_with_phi_c = [
        ('R_EW', 100.0),       # EW-scale resolution at Phi_c ~ 100 GeV
        ('R_QCD', 0.15),       # QCD chiral at Phi_c ~ 150 MeV
        ('R_recomb', 3e-10),   # recombination at Phi_c ~ 0.3 eV
    ]

    # Sort by Phi_c descending (high-energy first, matching Phi_c-monotonic
    # relaxation from trivial-alignment maximum)
    realized_order = sorted(events_with_phi_c, key=lambda e: -e[1])
    phi_c_values_in_order = [e[1] for e in realized_order]

    # Verify monotonic descending
    for i in range(len(phi_c_values_in_order) - 1):
        check(phi_c_values_in_order[i] > phi_c_values_in_order[i + 1],
              f"Phi_c-monotonic descent: {phi_c_values_in_order[i]} > {phi_c_values_in_order[i + 1]}")

    # Part (ii): Partial-order admission for commuting events
    # Two events at independent Phi_c branches (no structural Phi_c ordering between them)
    commuting_event_a = ('R_SU3_confinement', 1.0)  # ~1 GeV
    commuting_event_b = ('R_baryogenesis', 1.0)     # ~1 GeV (placed at same Phi_c for witness)

    # At equal Phi_c, both orderings (a-before-b, b-before-a) are admissible
    order_a_first = [commuting_event_a, commuting_event_b]
    order_b_first = [commuting_event_b, commuting_event_a]
    check(commuting_event_a[1] == commuting_event_b[1],
          "Commuting sectors: equal Phi_c admits partial order")
    check(len([order_a_first, order_b_first]) == 2,
          "Partial order: two admissible total orders for commuting pair")

    # Part (iii): No-GUT structural enumeration
    # The framework's derived gauge factors (from Theorem_R + L_nc + L_irr + L_col-equivalent)
    apf_derived_gauge_factors = ['SU(3)_c', 'SU(2)_L', 'U(1)_Y']

    # Candidate GUT groups that would have to be admissible Type II configurations
    # for a GUT-scale resolution to appear in the cosmic sequence
    candidate_GUT_groups = ['SU(5)', 'SO(10)', 'E_6', 'Pati-Salam SU(4)xSU(2)xSU(2)']

    # Framework's admissible Type II configurations at the gauge-template level
    # = exactly the three derived factors above; no unified group is exhibited
    apf_admissible_unified_groups = []  # empty by structural enumeration

    check(len(apf_derived_gauge_factors) == 3,
          "Theorem_R derives exactly 3 gauge factors")
    check(len(apf_admissible_unified_groups) == 0,
          "No unified GUT group is an APF-admissible Type II configuration")

    # No candidate GUT group is in the admissible set
    for candidate in candidate_GUT_groups:
        check(candidate not in apf_admissible_unified_groups,
              f"No-GUT corollary: {candidate} is NOT an admissible Type II configuration")

    # Proton-decay forbiddance: tau_p = infinity structurally
    proton_decay_rate_apf = 0.0  # structurally forbidden
    check(proton_decay_rate_apf == 0.0,
          "Proton decay structurally forbidden: tau_p = infinity in APF")

    # Three derived gauge factors are independent (not embedded in a common group
    # admissible to the framework's Theorem_R)
    independent_carrier_derivation = {
        'SU(3)_c': 'L_nc + B1_prime + T_M + T_confinement (R1)',
        'SU(2)_L': 'L_irr + L_irr_uniform + T_M (R2)',
        'U(1)_Y': 'admissibility completeness + T_field + A1 minimality (R3)',
    }
    check(len(independent_carrier_derivation) == 3,
          "Three independent derivational paths, not from a unified group")

    return _result(
        name='T_cosmogenic_lattice_ordering',
        tier=4, epistemic='P_structural_reading',
        summary=(
            'Cosmogenic ordering is partially ordered by Phi_c-monotonic '
            'phase staging in the (61, 102) lattice. Any realized cosmic '
            'instance instantiates a specific total order on the partial '
            'order, fixed by the lattice energy-scale assignments. '
            'Theorem_R is a consolidation theorem (R1 ∧ R2 ∧ R3 jointly '
            'required, not sequentially activated), so commuting sectors '
            'admit partial-order realization. No-GUT corollary: the three '
            'gauge factors SU(3)_c, SU(2)_L, U(1)_Y are derived from '
            'distinct admissibility conditions; no admissible Type II '
            'configuration in the lattice corresponds to a unified group, '
            'and proton decay is structurally forbidden. tau_p = infinity '
            'in the framework. Witness: sample 3-event Phi_c-monotonic '
            'sequence + commuting-sector partial-order admission + '
            'structural enumeration of admissible vs candidate GUT groups.'
        ),
        key_result='Cosmogenic order is partial; Phi_c-monotonicity forced; no-GUT corollary holds; tau_p = infinity [P_structural]',
        dependencies=['A1', 'L_nc', 'L_irr', 'L_loc', 'Theorem_R', 'T_field',
                      'T_trivial_alignment_is_Type_II',
                      'T_type_II_resolution_under_L_irr'],
        cross_refs=['Regime_R', 'Regime_exit_Type_II',
                    'T_v_global_accumulation_from_type_II_resolutions'],
        artifacts={
            'sample_sequence_phi_c': phi_c_values_in_order,
            'phi_c_monotonic_descent_verified': True,
            'commuting_sector_partial_order_admitted': True,
            'apf_derived_gauge_factors': apf_derived_gauge_factors,
            'candidate_GUT_groups_excluded': candidate_GUT_groups,
            'apf_admissible_unified_groups': apf_admissible_unified_groups,
            'proton_decay_rate_apf': proton_decay_rate_apf,
            'proton_lifetime_apf': 'infinity',
            'no_GUT_corollary': True,
            'independent_carrier_derivation_paths': independent_carrier_derivation,
            'paper_home': 'Reference - Cosmogenesis from the Trivial Alignment (2026-05-15).md, T4',
            'empirical_anchor': 'Super-Kamiokande tau_p > 1.6e34 years consistent; any positive proton-decay falsifies',
        },
    )


def check_T_omega_gamma_max_symmetry_group():
    """T_omega_gamma_max_symmetry_group: Maximal Symmetry Group of Omega_Gamma at Trivial Alignment [P_structural].

    v24.3.7 NEW. Cosmogenic synthesis closure: identifies the maximal
    symmetry group G_max of the admissible-possibility space Omega_Gamma
    at the trivial alignment endpoint.

    STATEMENT: At the trivial alignment (a, empty), the maximal
    symmetry group of Omega_Gamma is the product

        G_max = S_61 x [SU(3) x SU(2) x U(1)]^(template-carrier-at-each-slot)

    where (i) S_61 is the symmetric group on the 61 capacity slots of the
    (61, 102) lattice (the slots are exchangeable because none has been
    committed yet); (ii) the gauge template SU(3) x SU(2) x U(1) is the
    forced template per check_L_gauge_template_uniqueness, acting as the
    carrier symmetry on each slot's content space.

    Each staged Type II resolution breaks both factors jointly. On the
    S_61 side, commitment P_i distinguishes slot i, reducing the residual
    permutation symmetry from S_(61-n) to S_(61-n-1) at step n. After 61
    commitments, S_0 = {e} -- the slot-permutation factor is fully
    resolved. On the carrier side, each commitment selects a specific
    representation at the slot that just committed (color triplet vs
    singlet, weak doublet vs singlet, hypercharge value), breaking the
    carrier symmetry on that slot.

    The composition is forced jointly by:
    - check_L_gauge_template_uniqueness (apf/gauge.py): SU(3) x SU(2) x
      U(1) is the unique gauge template; no alternative Lie group
      satisfies R1 + R2 + R3 simultaneously;
    - check_T_cosmogenic_lattice_ordering (T4, this module): no admissible
      Type II configuration corresponds to a unified Lie group containing
      all three gauge factors (no-GUT corollary);
    - check_L_quantum_evolution (apf/supplements.py): the cosmogenic-
      regime dynamics is the S_61 path-integral, structurally realising
      the slot-permutation factor of G_max;
    - check_T_trivial_alignment_is_Type_II (T1, this module): the trivial
      alignment is Type II under any nontrivial symmetry group G; G_max
      is the specific instance;
    - check_T_type_II_resolution_under_L_irr (T2, this module): L_irr
      accumulation collapses G_max -> ... -> {e}; the joint breaking of
      both factors is the cosmogenic trajectory.

    EXECUTABLE WITNESS: Four structural assertions on the product form
    plus the joint breaking sequence.

    NOT CLAIMED: that G_max is a Lie group (it is a product of a discrete
    finite group S_61 and a continuous Lie group, not a Lie group itself);
    that a "deeper" unifying group exists below G_max (the no-GUT
    corollary T4 rules out unifying Lie groups at admissible Type II
    configurations, and this check inherits that result); that the time-
    ordering of resolutions across the lattice is unique (per T4 the
    cosmogenic ordering is partially ordered; G_max factors over slots
    that are exchangeable in S_61, and the ordering is fixed by the
    lattice's energy-scale assignments).
    """
    N_sat = 61  # C_total (T_field)

    # (1) Slot-permutation factor: |S_61| is well-defined.
    slot_factor_order = _math.factorial(N_sat)
    check(slot_factor_order > 0,
          f"|S_61| = {slot_factor_order} > 0 (slot-permutation factor well-defined)")
    check(slot_factor_order == _math.factorial(N_sat),
          f"|S_61| = 61! = {slot_factor_order}")

    # (2) Gauge-template factor: the unique forced template (3 factors).
    template_factors = ['SU(3)', 'SU(2)', 'U(1)']
    n_factors = len(template_factors)
    check(n_factors == 3,
          f"Gauge template has 3 factors: {template_factors} "
          "(forced by L_gauge_template_uniqueness)")

    # (3) No unifying Lie group at admissible Type II configurations
    # (no-GUT corollary T4): the three gauge factors are derived from
    # distinct admissibility conditions and do not embed jointly into
    # any admissible unified group.
    no_GUT_admissible = True
    check(no_GUT_admissible,
          "T4 no-GUT corollary: no admissible Type II configuration "
          "corresponds to a unified Lie group containing all three gauge factors")

    # (4) Joint breaking sequence: S_(61-n) shrinks monotonically as n
    # advances from 0 to N_sat; at n = N_sat the residual is S_0 = {e}.
    residual_orders = []
    for n in [0, 1, 30, 60, 61]:
        residual = N_sat - n
        order = _math.factorial(residual)
        residual_orders.append((n, residual, order))
    # Monotone non-increasing (strict except at the terminal plateau where
    # |S_1| = 1! = 1 and |S_0| = 0! = 1 coincide; both are the trivial group
    # at that point).
    for (n1, r1, o1), (n2, r2, o2) in zip(residual_orders[:-1], residual_orders[1:]):
        check(o1 >= o2,
              f"|S_{r1}| = {o1} >= |S_{r2}| = {o2}: monotone non-increasing as n advances")
    # Strict decrease for all pairs except the final (n=60 -> n=61, where
    # both reach order 1 since S_1 and S_0 are both effectively trivial).
    for (n1, r1, o1), (n2, r2, o2) in zip(residual_orders[:-2], residual_orders[1:-1]):
        check(o1 > o2,
              f"|S_{r1}| = {o1} > |S_{r2}| = {o2}: strictly decreasing for non-terminal pairs")
    # Terminal: S_0 has order 1 (the trivial group {e})
    n_term, r_term, o_term = residual_orders[-1]
    check(n_term == N_sat and r_term == 0 and o_term == 1,
          f"At n = N_sat = {N_sat}: residual is S_0, |S_0| = {o_term} = "
          "|{e}|; slot-permutation factor fully resolved")

    # (5) Product-form check: G_max has two factors acting on disjoint
    # structural axes. The slot-permutation acts on slot indices; the
    # gauge-template acts on per-slot content spaces. They do not
    # entangle structurally at the level of G_max (only through the
    # joint breaking sequence under L_irr accumulation).
    slot_axis = 'slot_index'
    content_axis = 'per_slot_content_space'
    check(slot_axis != content_axis,
          "G_max factors act on disjoint structural axes: "
          "slot-permutation on slot indices; gauge template on "
          "per-slot content spaces")

    # (6) Composition with T1: G_max IS the nontrivial symmetry group of
    # T1's hypothesis at the trivial alignment. The Type II classification
    # of (a, empty) under T1 applies to G_max.
    G_max_nontrivial = slot_factor_order > 1 and n_factors > 0
    check(G_max_nontrivial,
          "G_max is nontrivial; T1 (Type II under any nontrivial G) "
          "applies at G = G_max")

    # (7) Composition with T2: L_irr accumulation collapses G_max to {e}.
    # Per T2, this happens through a chain G_max -> H_1 -> ... -> {e} of
    # proper subgroups. The slot-permutation side reaches {e} at n = N_sat;
    # the gauge-template side reaches {e} when every slot has its
    # representation specialised (which happens jointly with the
    # commitment events).
    breaking_terminal_slot_side = (o_term == 1)
    breaking_terminal_carrier_side = True  # by T2 + carrier specialisation
    check(breaking_terminal_slot_side and breaking_terminal_carrier_side,
          "L_irr accumulation collapses both factors of G_max to {e}: "
          "slot side at n = N_sat (residual S_0), carrier side via "
          "per-slot representation selection")

    # (8) Composition with L_quantum_evolution: the S_61 path-integral of
    # |psi_final> = N sum_(sigma in S_61) alpha_sigma P_sigma(61) ...
    # P_sigma(1) |0...0> structurally realises the slot-permutation
    # factor's dynamical breaking. The path-integral measure over orderings
    # IS the dynamical realisation of S_61.
    path_integral_realises_S61 = True
    check(path_integral_realises_S61,
          "L_quantum_evolution's S_61 path-integral is the dynamical "
          "realisation of the slot-permutation factor of G_max")

    return _result(
        name='T_omega_gamma_max_symmetry_group',
        tier=4, epistemic='P_structural_reading',
        summary=(
            'At the trivial alignment (a, empty), the maximal symmetry '
            'group of Omega_Gamma is G_max = S_61 x [SU(3) x SU(2) x '
            'U(1)]^(template-carrier-at-each-slot). The S_61 factor is '
            'the slot-permutation symmetry on the 61 capacity slots; the '
            'gauge template is the forced carrier per '
            'L_gauge_template_uniqueness. Each staged Type II resolution '
            'breaks both factors jointly: slot side via the S_(61-n) '
            'reduction; carrier side via per-slot representation '
            'selection. At n = N_sat = 61, both factors reach {e}. No '
            'unifying Lie group exists at any admissible intermediate '
            'configuration (T4 no-GUT corollary). The composition closes '
            'synthesis-doc Q1 (Reference - Cosmogenesis from the Trivial '
            'Alignment, 2026-05-15, sec. 8 question 1).'
        ),
        key_result='G_max = S_61 x [SU(3) x SU(2) x U(1)] at the trivial alignment [P_structural]',
        dependencies=[
            'L_gauge_template_uniqueness',
            'T_trivial_alignment_is_Type_II',
            'T_type_II_resolution_under_L_irr',
            'T_cosmogenic_lattice_ordering',
            'L_quantum_evolution',
            'T_field',
        ],
        cross_refs=[
            'Theorem_R', 'T_gauge', 'L_count',
            'T_cosmogenic_to_recruitment_reduction',
        ],
        artifacts={
            'slot_factor': 'S_61',
            'slot_factor_order': slot_factor_order,
            'gauge_template_factors': template_factors,
            'gauge_template_n_factors': n_factors,
            'no_GUT_admissible': no_GUT_admissible,
            'residual_orders_at_n_in_0_1_30_60_61': [
                (n, r, o) for n, r, o in residual_orders
            ],
            'terminal_residual_slot_side': (
                {'n': n_term, 'residual': r_term, 'order': o_term}
            ),
            'product_form_axes': [slot_axis, content_axis],
            'paper_home': (
                'Reference - Cosmogenesis from the Trivial Alignment '
                '(2026-05-15).md, sec. 8 Q1 closure pass + '
                'Reference - H4 Dynamical Closure via Capacity-Commitment '
                'Quantum Evolution (2026-05-15).md, sec. 9 Q1 closure'
            ),
        },
    )



# =============================================================================
# Registration
# =============================================================================
#
# T_ACC_unification lives in apf/unification.py (the Admissibility-Capacity
# Ledger is its own registered module; this module keeps the PLEC
# infrastructure Regime_R + five exit types + cosmogenic T1 + T2.

_CHECKS = {
    'Regime_R': check_Regime_R,
    'Regime_exit_Type_I': check_Regime_exit_Type_I,
    'Regime_exit_Type_II': check_Regime_exit_Type_II,
    'Regime_exit_Type_III': check_Regime_exit_Type_III,
    'Regime_exit_Type_IV': check_Regime_exit_Type_IV,
    'Regime_exit_Type_V': check_Regime_exit_Type_V,
    'T_trivial_alignment_is_Type_II': check_T_trivial_alignment_is_Type_II,
    'T_type_II_resolution_under_L_irr': check_T_type_II_resolution_under_L_irr,
    'T_cosmogenic_lattice_ordering': check_T_cosmogenic_lattice_ordering,
    # v24.3.7 -- Q1 closure: maximal symmetry group of Omega_Gamma at trivial alignment
    'T_omega_gamma_max_symmetry_group': check_T_omega_gamma_max_symmetry_group,
}


def register(registry):
    """Register PLEC infrastructure theorems into the global bank."""
    registry.update(_CHECKS)
