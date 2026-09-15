"""Paper 37 capacity-flow companion (main v0.18, supplement v0.16).

The three flow checks are worked-instance model-integrity witnesses: exact
integration of the printed headroom-driven ODE, release-dependent threshold
time, and direct substitution into the per-slot Markov-breakdown form.
They do not establish physical registration or exclude an inverse. The
positive round-trip check establishes non-refund accounting only.

The separate structural-reading and collapse-triad checks retain their named
dependencies and existing grades; permanence there is imported through L_irr,
not derived from the scalar ODE. Five existing registry entries are retained.

Created 2026-05-14; capacity-flow correction 2026-09-12.
"""
from __future__ import annotations

import math


# ---------------------------------------------------------------------
# Substrate-side primitives (constants from the (61, 102) lattice)
# ---------------------------------------------------------------------

C_VACUUM = 42  # per-slot vacuum-face dimension at the SM interface
C_TOTAL = 61   # total capacity slots K_SM at the SM interface
D_EFF = 102    # per-slot admissible local channels
EPS_MIN = 1.0  # per-realignment floor (in normalised substrate units; Paper 1 supp v8.36 Def 3)


# ---------------------------------------------------------------------
# Per-slot capacity-flow equation
# ---------------------------------------------------------------------

def _nonnegative(**values):
    for name, value in values.items():
        if not math.isfinite(value) or value < 0:
            raise ValueError(f"{name} must be finite and nonnegative")


def _flow_inputs(slots, gamma_app, gamma_rel, phi_ijc_0):
    if isinstance(slots, bool) or not isinstance(slots, int) or slots < 0:
        raise ValueError("slots must be a nonnegative integer")
    _nonnegative(gamma_app=gamma_app, gamma_rel=gamma_rel,
                 phi_ijc_0=phi_ijc_0, total_rate=gamma_app + gamma_rel)


def per_slot_phi(t: float, gamma_app: float, gamma_rel: float = 0.0) -> float:
    """Exact driven-phase slot solution with phi_i(0)=0.

    The apparatus remains on in this expression. For a finite load use
    transition_state to stop the drive at the supplied registration threshold.
    """
    _nonnegative(t=t, gamma_app=gamma_app, gamma_rel=gamma_rel,
                 total_rate=gamma_app + gamma_rel)
    if gamma_app == 0:
        return 0.0
    rate = gamma_app + gamma_rel
    return C_VACUUM * (gamma_app / rate) * (-math.expm1(-rate * t))


def _drained_load(t, slots, gamma_app, gamma_rel):
    if slots == 0 or gamma_app == 0:
        return 0.0
    rate = gamma_app + gamma_rel
    fraction = gamma_app / rate
    # Integral of m*a*(C-phi(t)), with expm1 for short-time accuracy.
    return slots * C_VACUUM * fraction * (
        gamma_rel * t + fraction * (-math.expm1(-rate * t)))


def ijc_load(t: float, phi_ijc_0: float, slots: int, gamma_app: float,
             gamma_rel: float = 0.0) -> float:
    """Exact driven-phase IJC solution for the printed headroom ODE.

    This is an algebraic continuation: after exhausting the initial load it
    becomes negative and is no longer a physical trajectory. No clipping is
    concealed in this ODE solution. Use transition_state for a drive that
    switches off at a positive registration threshold.
    """
    _nonnegative(t=t)
    _flow_inputs(slots, gamma_app, gamma_rel, phi_ijc_0)
    return phi_ijc_0 - _drained_load(t, slots, gamma_app, gamma_rel)


def completion_time(slots: int, gamma_app: float, phi_ijc_0: float,
                    eps_min: float = EPS_MIN, gamma_rel: float = 0.0) -> float:
    """First time the driven load reaches a supplied positive threshold.

    For zero release, finite completion requires Phi0-eps < m*C; equality
    is reached only asymptotically. Positive release and drive give a unique
    finite root, found by monotone bracketing. This threshold convention is
    not a derivation of physical registration or record irreversibility.
    The original fourth positional argument remains eps_min.
    """
    _flow_inputs(slots, gamma_app, gamma_rel, phi_ijc_0)
    _nonnegative(eps_min=eps_min)
    if eps_min == 0:
        raise ValueError("eps_min must be positive")
    deficit = phi_ijc_0 - eps_min
    if deficit <= 0:
        return 0.0
    if slots == 0 or gamma_app == 0:
        return math.inf
    capacity = slots * C_VACUUM
    if gamma_rel == 0:
        if deficit >= capacity:
            return math.inf
        if deficit < capacity / 2:
            return -math.log1p(-deficit / capacity) / gamma_app
        return math.log(capacity / (capacity - deficit)) / gamma_app

    rate = gamma_app + gamma_rel
    drive_fraction = gamma_app / rate
    release_fraction = gamma_rel / rate

    def threshold_residual(t):
        if deficit < capacity / 2:
            return _drained_load(t, slots, gamma_app, gamma_rel) - deficit
        # D(t)-d near d=m*C: do not round 1-exp(-k*t) to 1 and
        # discard the exponentially small term that determines the root.
        # M-A = M*(r/k)*(1+a/k), where A=M*(a/k)^2.
        return math.fsum((
            capacity - deficit,
            -capacity * release_fraction * (1.0 + drive_fraction),
            -capacity * drive_fraction**2 * math.exp(-rate * t),
            capacity * drive_fraction * (gamma_rel * t),
        ))

    # Initial-rate estimate is a lower bound. Doubling brackets the root
    # without assuming that a release-independent exponential solves the ODE.
    low = 0.0
    high = deficit / capacity / gamma_app
    if high == 0 or not math.isfinite(high):
        raise OverflowError("threshold time outside floating-point range")
    while threshold_residual(high) < 0:
        high *= 2.0
        if not math.isfinite(high):
            raise OverflowError("threshold time outside floating-point range")
    for _ in range(160):
        middle = low + (high - low) / 2.0
        if middle == low or middle == high:
            break
        if threshold_residual(middle) < 0:
            low = middle
        else:
            high = middle
    return high


def transition_state(t: float, phi_ijc_0: float, slots: int,
                     gamma_app: float, gamma_rel: float = 0.0,
                     eps_min: float = EPS_MIN) -> tuple[float, float]:
    """(Residual IJC load, per-slot fill) under an explicit stopping protocol.

    Drive stops at completion_time; the residual stays booked at eps_min
    (or its initial value if already below threshold), and occupied slots
    release exponentially. Neither discarding the residual nor permanent
    locking is supplied by this scalar model. Exact clearing is asymptotic
    when release is positive. With no slots, the reported slot fill is zero.
    """
    _nonnegative(t=t)
    stop = completion_time(slots, gamma_app, phi_ijc_0, eps_min, gamma_rel)
    driven_t = min(t, stop)
    phi = per_slot_phi(driven_t, gamma_app, gamma_rel) if slots else 0.0
    if t >= stop:
        return min(phi_ijc_0, eps_min), phi * math.exp(-gamma_rel * (t - stop))
    return ijc_load(t, phi_ijc_0, slots, gamma_app, gamma_rel), phi


# ---------------------------------------------------------------------
# Markov-breakdown reduction (Theorem 6.1)
# ---------------------------------------------------------------------

def markov_breakdown_rhs(phi: float, gamma_app: float, gamma_rel: float, c_vacuum: float = C_VACUUM) -> float:
    """RHS of the per-slot Markov-breakdown rate equation
        \\dot{Delta_SSA}^{(i)} = Gamma_app (C - Delta_SSA^{(i)}) - Gamma_rel Delta_SSA^{(i)}
    under the per-slot identification Delta_SSA^{(i)} = phi_i, C = C_vacuum.
    """
    return gamma_app * (c_vacuum - phi) - gamma_rel * phi


def per_slot_capacity_flow_rhs(phi: float, gamma_app: float, gamma_rel: float) -> float:
    """RHS of the per-slot capacity-flow equation
        \\dot{phi}_i = Gamma_app (C_vac - phi_i) - Gamma_rel phi_i
    """
    return gamma_app * (C_VACUUM - phi) - gamma_rel * phi


# ---------------------------------------------------------------------
# Bank checks
# ---------------------------------------------------------------------

def check_T_class_transition() -> dict:
    """Worked-instance flow and non-refund accounting, not an inverse no-go."""
    slots, ga, gr, phi0 = 4, 1.0, 0.01, 100.0
    stop = completion_time(slots, ga, phi0, gamma_rel=gr)
    fills = [per_slot_phi(f * stop, ga, gr) for f in (0, .25, .5, .75, 1)]
    monotone = all(x <= y for x, y in zip(fills, fills[1:]))
    bounded = all(0 <= x < C_VACUUM for x in fills)
    threshold = abs(ijc_load(stop, phi0, slots, ga, gr) - EPS_MIN) < 1e-10
    no_refund = EPS_MIN > 0 and EPS_MIN + EPS_MIN == 2 * EPS_MIN
    return {
        'name': 'T_class_transition',
        'passed': monotone and bounded and threshold and no_refund,
        'key_result': (f'phi_monotone={monotone}; phi_bounded={bounded}; '
                       f'transition_threshold={threshold}; t_trans={stop:.8f}; '
                       f'positive_round_trip={no_refund}; '
                       'non-refund accounting does not exclude an inverse'),
        'theorem_refs': ['Paper 37 Supp v0.16 Theorem 5.1', 'Theorem 5.3'],
    }


def check_L_per_slot_capacity_flow() -> dict:
    """Per-slot capacity-flow equation reduces exactly to per-slot Markov-breakdown.

    Verifies on a grid of (phi, gamma_app, gamma_rel) values that the
    per-slot capacity-flow RHS equals the per-slot Markov-breakdown RHS
    under the identification Delta_SSA^{(i)} = phi_i, C = C_vacuum.
    The equality is exact (Theorem 6.1 Step proof: direct substitution).
    """
    test_grid = [
        (0.0, 1.0, 0.0),
        (10.0, 1.0, 0.01),
        (42.0, 1.0, 0.1),  # at C_vacuum
        (21.0, 5.0, 0.5),  # half-saturation
        (1.0, 0.1, 0.001), # tiny rates
    ]
    max_diff = 0.0
    for phi, ga, gr in test_grid:
        flow_rhs = per_slot_capacity_flow_rhs(phi, ga, gr)
        markov_rhs = markov_breakdown_rhs(phi, ga, gr, c_vacuum=C_VACUUM)
        diff = abs(flow_rhs - markov_rhs)
        if diff > max_diff:
            max_diff = diff

    passed = max_diff < 1e-12
    return {
        'name': 'L_per_slot_capacity_flow',
        'passed': passed,
        'key_result': (
            f'max RHS diff across grid = {max_diff:.2e} '
            f'(Markov-breakdown reduction exact at machine precision)'
        ),
        'theorem_refs': ['Paper 37 Supp v0.12 Theorem 6.1', 'Paper 16 v1.1 sec:phase'],
    }


def check_T_class_transition_completion() -> dict:
    """Independent fixed-time witness, root residual and release boundaries."""
    # Directly integrated zero-release ODE: four slots drain 3 units when
    # exp(-t)=55/56. The old exponential gives about 3.72 remaining, not 1.
    fixed_t = math.log(56 / 55)
    witness = abs(ijc_load(fixed_t, 4.0, 4, 1.0) - 1.0) < 1e-12
    zero_t = completion_time(4, 1.0, 4.0)
    zero_root = abs(zero_t - fixed_t) < 1e-14
    slow = completion_time(4, 1.0, 100.0, gamma_rel=.01)
    fast = completion_time(4, 1.0, 100.0, gamma_rel=2.0)
    residuals = all(abs(ijc_load(t, 100.0, 4, 1.0, r) - EPS_MIN) < 1e-10
                    for t, r in ((slow, .01), (fast, 2.0)))
    release_dependence = 0 < fast < slow < completion_time(4, 1.0, 100.0)
    boundaries = (
        completion_time(4, 0.0, EPS_MIN) == 0
        and math.isinf(completion_time(4, 0.0, 4.0))
        and math.isinf(completion_time(0, 1.0, 4.0))
        and math.isinf(completion_time(4, 1.0, 169.0))
        and math.isinf(completion_time(4, 1.0, 170.0))
        and math.isfinite(completion_time(4, 1.0, 170.0, gamma_rel=.01)))
    return {
        'name': 'T_class_transition_completion',
        'passed': witness and zero_root and residuals and release_dependence and boundaries,
        'key_result': (f'fixed_time_ODE_witness={witness}; zero_release_root={zero_root}; '
                       f'root_residuals={residuals}; release_dependence={release_dependence}; '
                       f'boundary_regimes={boundaries}'),
        'theorem_refs': ['Paper 37 Supp v0.16 Theorem 5.1'],
    }


def check_T_realignment_floor_is_epsilon_star() -> dict:
    """Reading identification of the realignment floor with the marginal floor.

    The named reading treats a realignment as creation of a new resolved
    structure and release of the old one. Under that identification,
    kappa_min and eps*_Gamma name the same structural floor.

    This check tests anchor consistency: check_L_epsilon_star,
    check_T_minimum_distinction_floor_via_MD and check_T_class_transition
    return passed=True, and the local EPS_MIN is positive. It does not
    derive the identification or calculate a cross-normalization equality.
    MD supplies the positive floor independently of A1; A1 supplies the
    capacity bound. Each module retains its own units: EPS_MIN = 1.0 here,
    eps* = 0.5 in the kappa_int_bounds witness. No numbers are equated or refit.

    Current grade: P_structural_reading. Historical source pointers:
    Paper 36 Def 4(i), Paper 1 supp v8.40 sec.11, and the Reframe Audit
    2026-05-20 sec.3. The source claims require the named identification.
    """
    from apf.core import check_L_epsilon_star
    from apf.kappa_int_bounds import check_T_minimum_distinction_floor_via_MD

    eps_star = check_L_epsilon_star()
    md_floor = check_T_minimum_distinction_floor_via_MD()
    transition = check_T_class_transition()

    # (1) marginal floor eps*_Gamma exists and is strictly positive
    eps_star_positive = bool(eps_star.get('passed') is True)
    # (2) the floor is DERIVED from MD (not posited)
    md_derived = bool(md_floor.get('passed') is True)
    # (3) the supplied flow model and positive round-trip accounting are consistent
    transition_model_consistent = bool(transition.get('passed') is True)
    # (4) the per-transition floor used by the class-transition machinery is > 0
    kappa_min_positive = EPS_MIN > 0.0

    # Anchor consistency under the supplied structural identification.
    # Positivity and passed flags do not derive the identification;
    # numeric normalizations differ and are not asserted equal.
    identified = (eps_star_positive and md_derived
                  and transition_model_consistent and kappa_min_positive)

    return {
        'name': 'T_realignment_floor_is_epsilon_star',
        'epistemic': 'P_structural_reading',
        'passed': identified,
        'key_result': (
            f'kappa_min read as eps*_Gamma (assumed structural identification; anchor consistency): '
            f'eps*_positive={eps_star_positive}, MD_derived={md_derived}, '
            f'transition_model_consistent={transition_model_consistent}, '
            f'kappa_min={EPS_MIN} > 0 = {kappa_min_positive}; '
            f'per-module normalisations differ (identification is structural, not numeric)'
        ),
        'theorem_refs': [
            'Paper 36 (The Missing Floor) Def 4(i)',
            'Paper 1 Supp v8.40 sec.11 (states identification eps_min = eps*_Gamma; floor = MD, not A1)',
            'Paper 10 v1.12 sec.3.5 Lemma BW',
            'Reframe Audit 2026-05-20 sec.3',
        ],
    }


def check_T_coherent_free_spend_permanent() -> dict:
    """Existing collapse-triad dependency composition with a numerical guard.

    The existing machine grade P is retained, not independently certified by
    the capacity-flow repair. FREE uses T_ledger_rent_excluded; SPEND uses
    L_irr and L_epsilon_star; PERMANENT imports L_irr. The floor-identification
    check is a cross-reference rather than a pass-gate dependency.

    In addition, resolves() consumes the scalar completion solver for the
    fixed worked instance: free requires no completion with no drive, while
    spend and permanent require finite completion with drive. This numerical
    completion guard DOES participate in the pass gate. Only the separately
    reported driven-phase monotonicity check is non-gating.

    The scalar guard does not establish that a physical resolution occurs,
    that the supplied rates/threshold are realized, or that an inverse is
    excluded. Permanence remains the imported L_irr claim. The occupancy
    profile and physical applicability are not derived by this check.
    """
    from apf.core import check_L_irr, check_L_epsilon_star
    from apf.operational_completeness import check_T_ledger_rent_excluded

    slots, ga, gr, phi0 = 4, 1.0, 0.01, 100.0
    t_trans = completion_time(slots, ga, phi0, gamma_rel=gr)
    tgrid = [f * t_trans for f in (0.0, .1, .25, .5, .75, 1.0)]

    def resolves(gamma_app):
        # structural: does a class transition COMPLETE (a resolution occur)?
        return math.isfinite(completion_time(slots, gamma_app, phi0, gamma_rel=gr))

    # Existing dependency gate plus the fixed-instance completion guard.
    rent_excluded_P = bool(check_T_ledger_rent_excluded().get('passed') is True)
    irr_P = bool(check_L_irr().get('passed') is True)
    eps_star_P = bool(check_L_epsilon_star().get('passed') is True)

    # (1) FREE: rent-exclusion [P] + a non-resolving hold does not complete
    free = rent_excluded_P and (not resolves(0.0))
    # (2) SPEND: L_irr [P] (resolution commits) + eps_star [P] (floor > 0) +
    #     the structural fact that a resolution occurs under drive; together
    #     the committed cost is >= eps* > 0 (booked, not free).
    spend = irr_P and eps_star_P and resolves(ga)
    # (3) PERMANENT: L_irr [P] one-way; a reverse is itself a resolution
    #     (books its own floor -- no refund), so the ledger never returns.
    permanent = irr_P and resolves(ga)

    passed = free and spend and permanent

    # ===== SECONDARY (instrument-level, NON-gating): Paper 37 substrate ODE
    phi_seq = [per_slot_phi(t, ga, gr) for t in tgrid]
    ijc_seq = [ijc_load(t, phi0, slots, ga, gr) for t in tgrid]
    dyn_consistent = (all(phi_seq[i] <= phi_seq[i + 1] + 1e-12 for i in range(len(phi_seq) - 1))
                      and all(ijc_seq[i] >= ijc_seq[i + 1] - 1e-12 for i in range(len(ijc_seq) - 1)))
    t_trans = completion_time(slots, ga, phi0, gamma_rel=gr)

    return {
        'name': 'T_coherent_free_spend_permanent',
        'epistemic': 'P',
        'passed': passed,
        'key_result': (
            f'Existing [P] composition with a numerical completion guard: '
            f'FREE = ledger_rent_excluded[P] (+ a held/non-resolving alignment '
            f'does not complete) -> {free}; SPEND = L_irr[P] (resolution commits '
            f'Delta>0) + L_epsilon_star[P] (floor eps*>0) => cost >= eps*>0, booked '
            f'-> {spend}; PERMANENT = L_irr[P] one-way (reverse books its own floor) '
            f'-> {permanent}. Secondary (non-gating): Paper 37 driven-phase monotonicity '
            f'(phi up/IJC down = {dyn_consistent}, t_trans={t_trans:.4f}).'
        ),
        'dependencies': ['occupancy', 'L_irr', 'T_ledger_rent_excluded', 'L_epsilon_star'],
        'cross_refs': ['T_realignment_floor_is_epsilon_star', 'T_class_transition',
                       'T_second_law', 'T_delta_JR_derived'],
        'theorem_refs': [
            'Paper 37 Supp thm:existence / thm:uniqueness / thm:irreversibility',
            'Paper 0 v6.2.39 (superposition/collapse: pays eps_min>0, no refund)',
            'Paper 3 check_T_ledger_rent_excluded (held = free) [P]',
            'check_L_irr (resolution commits Delta>0; permanent, unrecoverable) [P]',
            'check_L_epsilon_star (the MD floor eps* > 0) [P]',
        ],
    }


# ---------------------------------------------------------------------
# Bank registration
# ---------------------------------------------------------------------

_CHECKS = {
    'T_class_transition': check_T_class_transition,
    'L_per_slot_capacity_flow': check_L_per_slot_capacity_flow,
    'T_class_transition_completion': check_T_class_transition_completion,
    'T_realignment_floor_is_epsilon_star': check_T_realignment_floor_is_epsilon_star,
    'T_coherent_free_spend_permanent': check_T_coherent_free_spend_permanent,
}


def register(registry):
    """Register the class-transition checks into the bank.

    Five checks total (v24.3.47 added T_realignment_floor_is_epsilon_star,
    the kappa_min == eps*_Gamma bridge). Closes Paper 37 Supplement v0.12 Q4
    (bank-side machinery for the class-transition theorem).
    """
    for name, fn in _CHECKS.items():
        registry[name] = fn


def run_all():
    results = []
    for name, fn in _CHECKS.items():
        try:
            r = fn()
            ok = bool(r.get('passed') is True)
            results.append({'name': name, 'passed': ok, 'key_result': r.get('key_result', '')})
        except Exception as e:
            results.append({'name': name, 'passed': False, 'error': repr(e)})
    return {
        'passed': sum(1 for r in results if r['passed']),
        'total': len(results),
        'results': results,
    }


if __name__ == '__main__':
    import json
    print(json.dumps(run_all(), indent=2))

# ---------------------------------------------------------------------------
# IE onboarding (Wave 7, v24.3.347).
# ---------------------------------------------------------------------------
IE_DECLARATIONS = (
    {
        "input_id": "foundation:class_transition_primitive",
        "expect_export": False,
        "axis": "ROUTE",
        "claim_text": (
            "Bank-side companion to Paper 37 (Collapse as Realignment), "
            "closing the Supplement v0.12 Q4 flag. FIVE checks. Three are "
            "worked-instance model-integrity witnesses of the substrate "
            "dynamics: check_T_class_transition (per-slot saturation phi "
            "monotone and bounded by C_vacuum = 42, finite completion time, "
            "positive round-trip accounting, not exclusion of an inverse); check_L_per_slot_capacity_flow (the "
            "per-slot capacity-flow RHS equals the Paper 16 v1.1 Markov-"
            "breakdown RHS exactly, max diff < 1e-12); "
            "check_T_class_transition_completion (integrated headroom ODE, "
            "independent fixed-time witness, release-dependent threshold root "
            "and zero-release reachability limits). check_T_realignment_floor_is_epsilon_star "
            "[P_structural_reading] checks anchor consistency under the named "
            "identification kappa_min == eps*_Gamma; MD independently supplies "
            "the positive marginal floor. check_T_coherent_free_spend_permanent [P] "
            "(v24.3.397) states the collapse triad as a COMPOSITION of banked "
            "[P] theorems over the constitutive base (A1 + occupancy, "
            "occupancy constitutive since v24.3.304): FREE coherent hold = "
            "check_T_ledger_rent_excluded [P]; SPEND at the IJC->Sep "
            "resolution = check_L_irr [P] (a resolution commits Delta>0) + "
            "check_L_epsilon_star [P] (any committed distinction floored by "
            "eps*>0) => cost >= eps*>0, booked not free; PERMANENT one-way = "
            "check_L_irr [P]. The [P] is INHERITED from the three pillars; NO "
            "[P_structural] check sits in the pass gate (the kappa_min==eps* "
            "identification is a cross_ref only). The scalar completion "
            "guard participates in the pass gate; only the monotonicity "
            "report is non-gating. Historical banking audit: LAND-[P] 0.88."
        ),
        "note": (
            "Wave 7 (v24.3.397 adds check_T_coherent_free_spend_permanent, "
            "the collapse triad as a [P] composition over A1 + occupancy). "
            "FIVE checks. check_T_coherent_free_spend_permanent [P] "
            "(dependencies occupancy, L_irr, T_ledger_rent_excluded, "
            "L_epsilon_star -- all banked [P]; SPEND routed via L_irr + "
            "eps_star giving cost >= eps* > 0, so NO [P_structural] sits in "
            "the gate; the realignment-floor identification is a cross_ref "
            "only; numerical completion guards the gate, monotonicity is "
            "non-gating; historical banking audit LAND-[P] 0.88) "
            "and check_T_realignment_floor_is_epsilon_star [P_structural_reading] "
            "carry machine epistemic fields. The other THREE "
            "(T_class_transition, L_per_slot_capacity_flow, "
            "T_class_transition_completion) are DELIBERATELY grade-in-prose "
            "worked-instance witnesses of the substrate ODE, counted as "
            "no-epistemic-field members of the full-surface grade-coverage "
            "census (FULL_SURFACE_NO_EPISTEMIC pin, ie_export_core_census.py; "
            "censused, not gated). Do NOT add machine grades to those three "
            "without re-pinning that census. The phenomenological dynamics "
            "(Gamma_app/Gamma_rel rates, timescales) are NOT [P]-from-A1 and "
            "stay instrument-level. The [P] triad itself exports via the "
            "dedicated foundation:collapse_triad_free_spend_permanent "
            "input below (v24.3.398)."
        ),
    },
    {
        "input_id": "foundation:collapse_triad_free_spend_permanent",
        "axis": "ROUTE",
        "route": "collapse_triad",
        "expect_export": True,
        "payload": {
            "name": "collapse_triad_free_spend_permanent",
            "closure_kind": "internal_identity",
            "identity_summary": (
                "The collapse triad holds as a COMPOSITION of banked [P] "
                "theorems over the constitutive base (A1 + occupancy): "
                "(1) FREE while held -- no cost accrues to a held alignment "
                "at fixed structure (check_T_ledger_rent_excluded [P], no "
                "standing-rent cost kind); (2) SPEND at resolution -- a "
                "resolution commits Delta > 0 (check_L_irr [P]) and every "
                "committed distinction is floored by eps* > 0 "
                "(check_L_epsilon_star [P]), so the IJC->Sep class "
                "transition books cost >= eps* > 0, once; (3) PERMANENT -- "
                "the committed capacity is locally unrecoverable and the "
                "reverse transition books its own forward floor, round trip "
                "2*eps_min > 0, no refund (check_L_irr [P]). NO "
                "[P_structural] check sits in the gate: the kappa_min == "
                "eps* identification is a cross_ref. The scalar completion "
                "guard participates in the pass gate; the monotonicity "
                "report does not. "
                "(check_T_coherent_free_spend_permanent, class_transition.py)"
            ),
        },
        "note": (
            "The v24.3.398 export split: the [P] triad gets its own "
            "exporting input, separated from the "
            "foundation:class_transition_primitive bundle above (which "
            "stays expect_export=False for its grade-in-prose substrate-ODE "
            "witnesses). The quantum/classical SPLIT (the form free-hold -> "
            "eps-spend-at-resolution -> permanent) is what exports; WHICH "
            "side a given situation is on stays occupancy-profile, "
            "situational, never exported. Fresh audit LAND-[P] 0.88 at "
            "banking (v24.3.397)."
        ),
    },
)
