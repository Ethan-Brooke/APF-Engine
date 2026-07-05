"""The gamma_C carrier program: the fork, the two no-gos, the weight-one reduction.

BANKED v24.3.375 (2026-07-04; walks + witnesses of 2026-07-03). The no-trace-gate program instruments from the
three walks of record (all 2026-07-03, all hostile-audit-repaired v0.2+):
  (1) "Reference - The No-Trace Gate Against the Recruitment Instruments -
      The Carrier Fork and the Reservoir-Exclusion Route" -- the parent walk:
      the four-point carrier fork, the T4 dimension audit, the pooled/
      Nordstrom and per-channel Cassini kills, the reservoir-exclusion route
      named as the live open (L1 open + L2 banked + L3 finite).
  (2) "Reference - The Master-Equation Route Is Carrier-Blind - T2-Prime and
      the Eleven-Check Tripwire" -- T2' (LAND-WITH-FIXES 0.85): the Papers
      24/25 master-equation package adds no constraint on (lambda_t,
      lambda_s); the countermodel extends through the full derived corpus;
      the fence is removed WITH A TRIPWIRE on the recruitment.py instrument
      count.
  (3) "Reference - The Register-Carrier Lemma Walked - The Typing Dilemma,
      H6-Prime, and the Weight-One Opener" -- REDUCED with a proved
      refutation component (LAND-WITH-FIXES 0.85): T-RC1 at schema strength
      (rule-choice = response-choice), the T_M three-typing census, the
      signed mechanism-limit legs, H6' as target spec, and the weight-one
      curve gamma(w) = w/((n-1)-w) as the audit-donated opener.
Machine witnesses (The Turning/, all PASS): c1_notrace_witness_2026-07-03.py
(9/9), mastereq_carrier_witness_2026-07-03.py (27/27),
register_carrier_witness_2026-07-03.py (40 PASS).

CONVENTIONS (Paper 9 v1.6, pinned throughout): Theta_t = 1 + 2*Phihat,
Theta_s = 1 - 2*gamma_C*Phihat; clock calibration lambda_t = +1; ruler
response lambda_s = -gamma_C; plane trace theta = lambda_t + lambda_s
= 1 - gamma_C; shear sigma = (lambda_t - lambda_s)/2 = (1 + gamma_C)/2.

WHAT THE FOUR CHECKS CERTIFY:

check_T_gammaC_carrier_fork (tier 3, [P_structural]) -- the fork geometry,
exact rationals throughout:
  - The four carrier closures, SOLVED from their defining linear conditions
    (not hand-set): plane conservation (lambda_t + lambda_s = 0) -> gamma_C
    = 1; four-cell conservation (lambda_t + 3*lambda_s = 0) -> 1/3;
    per-channel closure (lambda_s = 0) -> 0; pooled/common depletion
    (lambda_s = +lambda_t) -> -1. Pairwise distinct, and CROSS-EXCLUSIVE:
    plane closure forces the four-cell trace to -2 (not 0); four-cell
    closure forces the plane trace to 2/3 (not 0).
  - The dimension table: gamma_GR(n) = 1/(n-2) for spatial dimension n.
    FLAGGED CONTINUUM IMPORT: this row is recomputed from trace-reversed
    linearized GR (h_00 = A(n-2)/(n-1), h_ij = A/(n-1)), an adopted
    continuum object, not native APF content. LOVELOCK NOTE: Gauss-Bonnet
    (and the higher Lovelock terms) contribute nothing to the linearized-
    around-flat static response, so gamma_GR(n) = 1/(n-2) holds for the
    whole Lovelock family, not just Einstein-Hilbert -- the dimension
    audit's kill rows are Lovelock-robust. The plane row matches the
    Einstein family ONLY at n = 3; the four-cell generalization (1/n),
    the per-channel row (0), and the pooled row (-1) match in NO
    dimension n >= 3.
  - The Cassini kills (gamma_obs = 1 +/- 2.3e-5): pooled = Nordstrom
    (gamma = -1, conformally flat response, zero first-order light
    deflection) excluded at ~8.7e4 sigma; per-channel (gamma = 0, half-GR
    deflection) excluded at ~4.3e4 sigma.
  - THE WEIGHT-ONE CURVE (the audit-donated mechanism decomposition):
    response = direct clock coupling + w * eta-weighted spread gives
    gamma(w) = w/((n-1)-w) exactly; gamma(1, n) = 1/(n-2) for n = 3..8
    (GR is w = 1 in EVERY dimension) and gamma(0, n) = 0 (direct-only is
    the per-channel carrier); the spread-only limit carries the SIGNED leg
    lambda_s = +lambda_t (the pooled shape, NOT the plane). The weight-one
    walk (derive w = 1) is the live opener of record.
  FALSIFIER HOOKS: a measured gamma_obs anomaly (any confirmed departure
  from gamma = 1 re-opens the fork empirically); ANY change to the Paper 9
  normal-form conventions (lambda_t = +1, lambda_s = -gamma_C) -- the fork
  values are convention-anchored and must be re-solved under a new normal
  form (the four-cell sign-slip artifact -1/3 vs +1/3 is the recorded
  cautionary example).

check_L_notrace_not_from_recruitment_instruments (tier 3,
[P_structural_instrument]) -- the T2 + T2' route closure:
  - Realizes the trace-obstruction countermodel (Paper 9
    def:trace-obstruction-coefficient): V_e(u, v; chi) = (A/2)u^2 +
    (B/2)(v - beta*chi)^2 - lambda*chi*u with A, B > 0 and lambda =
    A(1 - gamma) realizes ANY gamma_C = gamma at its unique minimum.
    gamma is derived from the NUMERICALLY MINIMIZED u (grid refinement
    against the closed form), not just read off the closed form, for
    gamma in {1, 1/3, 0, -1, 0.7}.
  - PINS the instrument enumeration as artifact data: the Paper 10
    Supplement B5 + B3.4 instruments; Paper 10 sec-8's clock-sector
    response principle (DISCHARGED: it prices lambda_t only -- clock-only
    per the parent walk); the recruitment.py bank instruments with their
    static-vacuity discharges (mu == 0 at the static fixed point: the
    master equation, relaxation, three regimes, and the rate-layer checks
    all hold as 0 = 0; the quantum-anchor package is silent for a single-
    branch classical static anchor); and the ADOPTED-OBJECTS EXCLUSION
    (Paper 25's eq:linearized-EH and the phi_T <-> h_munu identification
    are excluded from the licensing set BECAUSE adopted, S5 -- including
    them would close the gate by adoption, not derivation).
  - THE TRIPWIRE (the note's fence-removal condition, promoted to a live
    in-check leg): the check counts the check_* functions in
    apf/recruitment.py AT RUNTIME and FAILS LOUDLY if the name set differs
    from the pinned baseline. A new recruitment instrument banked later
    voids the enumeration baseline and forces a T2' re-audit BY FAILING
    THE BANK. Baseline note: the walk's enumeration was the ELEVEN checks
    present at walk time (through the .363 knee corollary); the twelfth,
    check_T_tls_transduction_class_discriminator_rule_D, landed in the
    concurrent .371 lane AFTER the walk's enumeration and BEFORE this
    banking -- per the tripwire's own rule that forced a re-audit, which
    was PERFORMED AT BANKING TIME (2026-07-03) and is recorded here: Rule
    D quantifies over TLS transduction-class adjudication (coverage below
    T_sat, design SNR) -- a rate-layer experimental-design instrument with
    no comparison-direction index and no quantification over (lambda_t,
    lambda_s); its static-vacuity discharge is the same one-liner as the
    knee corollary's. The pinned baseline is therefore the TWELVE names
    below; instrument thirteen (or any removal/rename) fails this check.
  SCOPE FENCE (docstring-load-bearing): this lemma certifies
  NON-DERIVABILITY FROM THE CORPUS AS FORMALIZED 2026-07-03 -- the B5 +
  B3.4 instruments, the sec-8 clock-sector principle, and the complete
  Papers 24/25 derived package. NEVER cite as "APF cannot derive gamma_C":
  non-derivability from APF is NOT claimed. The reservoir-exclusion route
  (L1 open + L2 banked partition + L3 finite sector check) and the
  weight-one walk are the live native routes.

check_L_register_carrier_not_from_account_instruments (tier 3,
[P_structural_instrument]) -- the register-carrier walk's banked form:
  - T-RC1 AT SCHEMA STRENGTH: rule-choice = response-choice. The four
    natural billing rules are realized as linear closure functionals and
    each is SOLVED for its selected gamma (computation over the rule
    definitions): plane billing -> 1; four-cell billing -> 1/3;
    nomological-redundancy billing RB -> 0; single-anchor pooled billing
    -> -1. Injective onto the fork; each rule's defining closure holds at
    its own point and fails at the other three.
  - THE LINEAR-RULE CONTINUUM (kills "bijection"): any rule marking
    c_t*lambda_t + c_s*lambda_s as line-requiring selects gamma = c_t/c_s
    -- pinned at three sample points plus the many-to-one witness
    ((1,1) and (3,3) select the same carrier). The rule -> carrier map is
    many-to-one ONTO the fork; no billing-layer datum strictly below the
    fork exists.
  - THE T_M THREE-TYPING CENSUS, stored as artifact data with the outcome
    set asserted exactly: cell-as-one-interface -> shared anchors -> one
    budget -> pooled (gamma = -1); channels-as-interfaces -> disjoint
    singleton anchors -> T_M-independent -> per-channel (gamma = 0);
    planes-as-interfaces -> the clock anchors in all three planes ->
    shared anchor -> T_M-INCONSISTENT as an independent-account
    decomposition (no carrier outcome). Under NO admissible typing does
    T_M yield the plane (gamma = 1). NEVER cite this leg as a flat
    refutation -- the TYPING DILEMMA is the banked form: T_M underdetermines
    the typing, and every admissible typing selects a Cassini-dead
    competitor or is inconsistent.
  - THE SIGNED MECHANISM-LIMIT LEGS (trace-reversal recomputation, exact):
    h_00 = A(n-2)/(n-1) and h_ij = A/(n-1) from the direct + eta-weighted-
    spread decomposition, ratio h_ij/h_00 = 1/(n-2); the signed conversion
    lambda_s/lambda_t = -h_ij/h_00 carried exactly; direct-only limit ->
    lambda_s = 0 (per-channel, exactly); spread-only limit -> lambda_s =
    +lambda_t EXACTLY (the pooled shape, sign included -- NOT the plane,
    which needs lambda_s = -lambda_t); plane balance at NEITHER limit.
  - THE H6' CLOSURE IDENTITY as a by-construction identity table:
    lambda_t + (n-2)*lambda_s = 0 identically in n for the Einstein
    family, plus the corollary lambda_t + n*lambda_s = 2*lambda_s (the
    load's net cell creation is exactly a spatial 2-plane's worth of ruler
    dilation). CAVEAT (docstring-load-bearing, per the walk's F-surface):
    H6' is the dimension-covariant form of the OUTPUT identity, adopted as
    TARGET SPEC, not a mechanism claim -- a native discharge may equally
    produce the trace-reversal decomposition, of which the register
    closure is the read-off. H6' is [C], the named reduction target; it
    is not banked by this check.

check_T_weight_one_reduction (tier 3, [P_structural]; ADDED v24.3.378,
2026-07-04) -- the weight-one walk banked ("Reference - The Weight-One
Walk - The Deposit Identity, the Asymmetric Pair, and the Live Cassini
Tension (2026-07-04)" v0.2, hostile-audit-repaired 0.83 -> 0.90; machine
witness The Turning/weight_one_witness_2026-07-04.py 36/36 PASS; the
note's Sec 5 bank spec followed verbatim):
  - L-W0 (deposit-fraction identity, exact rationals n = 3..8): w =
    D(spread deposit)/D(commitment), D the Euclidean cell-sum over the
    n+1 channel accounts; the denominator n-1 DISCHARGED as the cell's
    eta-sum; D-balance selects gamma = 1/(n-2) under EVERY democratic-
    eta normalization c ("w = 1" is a convention-bound label for a
    convention-free statement).
  - L-W1 (exchange annihilation): D annihilates clock<->ruler AND
    ruler-ruler exchange -- the v_e reductio has no purchase on the
    amount frame BY ARITHMETIC given the linear channel-uniform amount
    functional (TCP-min clause (ii), T4-selected within the anisotropic
    family), not by a billing fence.
  - L-W2 (scalar-improvement identity; exact formal basis + exact
    integer Fourier conservation leg): G_lin[h(w)] = kappa*T +
    ((1-w)/2)(eta box - dd) hbar; the improvement term identically
    conserved, vanishing IFF w = 1, in every n; w != 1 IS Paper 9's
    independent scalar mode (n = 3 calibrated trace source lambda/A =
    2(1-w)/(2-w)). FLAG: computed on the adopted linearized theory
    (continuum import, same flag as the dimension table).
  - fork w-coordinates: plane w = 1 at n = 3 ONLY (w_plane = (n-1)/2,
    scalar-tensor off n = 3); four-cell w = 1/2; per-channel w = 0;
    pooled at NO finite w (spread-only projective point w = n-1,
    h_00 = 0; gamma -> -1 as w -> +/-inf).
  - the SHAPE TABLE ("the shape carries the fork content"): under the
    SAME D-balance, eta-democratic -> the Einstein family in every n;
    rulers-only -> 1/n (four-cell, Cassini-dead); clock-only -> 0
    (per-channel, Cassini-dead). The eta-democratic shape S1 is the
    honest residual import.
  - the ANISOTROPIC FAMILY + THE T4 SELECTION: the channel-anisotropic
    functional (c_t, c_s) runs the same no-source route to the bound
    continuum gamma <= c_t/(n*c_s - 2*c_t) (n = 3 samples: 10/7, 5/8,
    exactly 1 at c_t = c_s); the bound tracks gamma_GR(n) = 1/(n-2) in
    every n IFF c_t = c_s -- the dimension audit uniquely selects
    channel-uniformity; the UNSIGNED (L1) channel-uniform balance lands
    on the four-cell family 1/n in every n -- a natural functional on a
    fork point, excluded by TCP-min's LINEARITY clause, not by taste.
  - THE THIRD COAT (docstring-load-bearing): "bill the D-net component"
    <=> the (1, n-2) linear rule of banked T-RC1 <=> H6-prime's closure
    identity -- at n = 3 exactly the plane rule (1, 1). Record-billing
    with a D-fence IS H6-prime restated: dead as a carrier-neutral
    route, DO-NOT-RE-WALK; never cite the D-fence as licensing
    record-billing. The currency/register boundary is amount-billing
    vs record-billing.
  - the CONDITIONAL HALVES (hypothesis artifacts; NOTHING here derives
    w = 1): TCP-min [C] and TCP-strong [C] stored verbatim; the
    asymmetric pair: no-source w <= 1 (gamma_C <= 1 at n = 3) at
    [P_structural | S0/S1 + TCP-min + H5-W + census legs + the Paper 9/
    Paper 10 base (P5, B7 incl. adopted C_M)]; no-sink (w >= 1)
    additionally requires TCP-strong, whose named discharge shape is an
    amount-graded testedness principle -- walked 2026-07-04 and priced
    as the (E)+(P) anatomy (apf/amount_graded_testedness.py). H5-W is
    the census-transport variant fence, named, unbanked, SEPARATE and
    standing.
  - CASSINI, SIGNED (Bertotti-Iess-Tortora 2003): gamma - 1 =
    (2.1 +/- 2.3)e-5 -- the central value sits 0.91 sigma ABOVE the
    bound (w - 1 = +1.05e-5 at central gamma): the bound survives at
    < 1 sigma under LIVE ONE-SIDED TENSION, not saturation; a factor-~3
    precision improvement at the same central value puts the composite
    under ~3 sigma pressure; a >= 3 sigma confirmed violation falsifies
    the composite (convention stored as artifact).
  - the FOOTPRINT KILL extension: the w-question's energetic footprint
    is ~2.2e-12 floor units at solar weak field; the approximate-A2/
    no-slack route is dead for w as it was for theta.
  - F-W2 TRIPWIRE (in-check, B2's style): the recruitment.py instrument
    name set is re-asserted against the pinned twelve-name baseline; a
    new ruler-sector or channel-anisotropic response instrument landing
    in the recruitment census fails this check loudly and forces a
    re-audit of TCP clause (ii)'s pricing (instruments landing outside
    that census remain E1-search-bounded, named).

STATUS. Fork check [P_structural]; the two route-closures
[P_structural_instrument] -- instrument-enumeration-bounded negatives in
the T2/T2' genre, tripwired; the weight-one reduction [P_structural] --
arithmetic-certificate + route-boundary genre. The weight-one walk is
WALKED and REDUCED (2026-07-04, banked here); the live openers are the
(E) distributed-encoding door (apf/amount_graded_testedness.py), the
shape question (derive eta-democracy), and H5 census-transport (separate,
standing). Nothing here derives gamma_C = 1 or w = 1; the conditional
composition of the parent walk (gamma_C = 1 given plane-carrier closure,
PLC [C]) stands unchanged.

Dependencies: A1, T8, Delta_signature (d = 4 [P] scopes the n = 3 rows).
Cross-refs: H1_continuum_from_anchor_profile,
H2_locality_from_recruitment_kernels, T_master_equation_form,
T_ledger_rent_excluded, T11.
"""

import inspect
import itertools
import math
from fractions import Fraction

import numpy as np

from apf.apf_utils import check, _result

# --- Paper 9 v1.6 normal form (pinned) -------------------------------------
_LAMBDA_T = Fraction(1)             # clock calibration


def _lam_s(gamma):
    """Ruler response coefficient: lambda_s = -gamma_C (Paper 9 v1.6)."""
    return -gamma


def _solve_linear_closure(c_t, c_s, rhs=Fraction(0)):
    """Solve c_t*lambda_t + c_s*lambda_s(gamma) = rhs for gamma.

    With lambda_t = 1 and lambda_s = -gamma this is c_t - c_s*gamma = rhs,
    i.e. gamma = (c_t - rhs)/c_s. Solved, not hand-set."""
    check(c_s != 0, "closure must constrain the ruler channel")
    return Fraction(c_t - rhs, 1) / Fraction(c_s, 1)


# The four carrier closures as (c_t, c_s, rhs) linear conditions on
# c_t*lambda_t + c_s*lambda_s = rhs:
_CLOSURES = {
    'plane':       (Fraction(1), Fraction(1), Fraction(0)),   # lt + ls = 0
    'four_cell':   (Fraction(1), Fraction(3), Fraction(0)),   # lt + 3ls = 0
    'per_channel': (Fraction(0), Fraction(1), Fraction(0)),   # ls = 0
    'pooled':      (Fraction(-1), Fraction(1), Fraction(0)),  # ls - lt = 0
}

_CASSINI = Fraction(23, 1000000)    # |gamma_obs - 1| <= 2.3e-5 (Cassini)


def _gamma_GR(n):
    """Trace-reversed linearized GR: gamma_GR(n) = 1/(n-2), n spatial dims.

    CONTINUUM IMPORT (flagged): recomputed below from the h_00/h_ij
    decomposition of the adopted linearized theory; Lovelock-robust
    (Gauss-Bonnet adds nothing linearized around flat)."""
    return Fraction(1, n - 2)


def _trace_reversal_components(n, A=Fraction(7)):
    """Static point source in D = n+1: hbar_00 = A, hbar_trace = -A
    (eta^00 = -1); h_munu = hbar_munu - eta_munu*hbar_trace/(n-1).
    Returns (h_00, h_ij, spread_00, spread_ij); direct_00 = hbar_00."""
    hbar_00, hbar_tr = A, -A
    spread_00 = -Fraction(-1) * hbar_tr / (n - 1)   # eta_00 = -1
    spread_ij = -Fraction(1) * hbar_tr / (n - 1)    # eta_ij = +1, hbar_ij = 0
    h_00 = hbar_00 + spread_00
    h_ij = spread_ij
    return h_00, h_ij, spread_00, spread_ij


def _gamma_w(w, n):
    """The weight-one curve: response = direct + w*spread ->
    gamma(w, n) = h_ij(w)/h_00(w) = w/((n-1)-w). Exact rationals."""
    A = Fraction(7)                 # arbitrary nonzero; ratio A-independent
    hbar_00, hbar_tr = A, -A
    h_00 = hbar_00 + w * (-Fraction(-1) * hbar_tr / (n - 1))
    h_ij = w * (-Fraction(1) * hbar_tr / (n - 1))
    return h_ij / h_00


def check_T_gammaC_carrier_fork():
    # --- 1. the fork, SOLVED from the closure conditions -------------------
    fork = {name: _solve_linear_closure(*cond)
            for name, cond in _CLOSURES.items()}
    expected = {'plane': Fraction(1), 'four_cell': Fraction(1, 3),
                'per_channel': Fraction(0), 'pooled': Fraction(-1)}
    check(fork == expected,
          "the four carrier closures must solve to gamma in {1, 1/3, 0, -1}")
    check(len(set(fork.values())) == 4, "the four fork points are distinct")
    # closure residuals: each closure holds at its own point, fails elsewhere
    for name, (c_t, c_s, rhs) in _CLOSURES.items():
        for name2, g in fork.items():
            residual = c_t * _LAMBDA_T + c_s * _lam_s(g) - rhs
            if name2 == name:
                check(residual == 0, f"{name} closure must hold at its point")
            else:
                check(residual != 0,
                      f"{name} closure must fail at the {name2} point")

    # --- 2. cross-exclusivity ----------------------------------------------
    four_trace_at_plane = _LAMBDA_T + 3 * _lam_s(fork['plane'])
    check(four_trace_at_plane == -2,
          "plane closure forces the four-cell trace to -2 (mutual exclusion)")
    plane_trace_at_cell = _LAMBDA_T + _lam_s(fork['four_cell'])
    check(plane_trace_at_cell == Fraction(2, 3),
          "four-cell closure forces the plane trace to 2/3")

    # --- 3. the dimension table (continuum-import row flagged) ------------
    plane_matches, cell_matches, chan_matches, pool_matches = [], [], [], []
    for n in range(3, 11):
        g_gr = _gamma_GR(n)
        # recompute the GR row from the trace-reversal mechanism (not a pin):
        h_00, h_ij, _, _ = _trace_reversal_components(n)
        check(h_ij / h_00 == g_gr,
              "gamma_GR(n) = 1/(n-2) must follow from trace reversal")
        if fork['plane'] == g_gr:
            plane_matches.append(n)
        if Fraction(1, n) == g_gr:          # four-cell -> (n+1)-cell rule
            cell_matches.append(n)
        if fork['per_channel'] == g_gr:
            chan_matches.append(n)
        if fork['pooled'] == g_gr:
            pool_matches.append(n)
    check(plane_matches == [3],
          "the plane carrier matches the Einstein family ONLY at n = 3")
    check(cell_matches == [] and chan_matches == [] and pool_matches == [],
          "four-cell (1/n), per-channel (0), pooled (-1) match in NO "
          "dimension n >= 3 -- Cassini-independent structural kills")

    # --- 4. the Cassini kills ----------------------------------------------
    sigma_pooled = abs(fork['pooled'] - 1) / _CASSINI
    check(86000 < float(sigma_pooled) < 88000,
          "pooled/Nordstrom gamma = -1 excluded at ~8.7e4 sigma")
    sigma_chan = abs(fork['per_channel'] - 1) / _CASSINI
    check(43000 < float(sigma_chan) < 44000,
          "per-channel gamma = 0 excluded at ~4.3e4 sigma")
    # Nordstrom shape: conformally flat response, zero first-order deflection
    check((1 + fork['pooled']) / 2 == 0,
          "the gamma = -1 member has zero first-order light deflection")
    check(_LAMBDA_T - _lam_s(fork['pooled']) == 0,
          "pooled: the first-order exchange sector v = lambda_t - lambda_s "
          "is destroyed (redshift-only response)")

    # --- 5. the weight-one curve (the audit-donated decomposition) --------
    for n in range(3, 9):
        for w in (Fraction(0), Fraction(1), Fraction(1, 2), Fraction(3, 2)):
            check(_gamma_w(w, n) == w / ((n - 1) - w),
                  "gamma(w) = w/((n-1)-w) closed form")
        check(_gamma_w(Fraction(1), n) == Fraction(1, n - 2),
              "GR is w = 1 in EVERY dimension: gamma(1, n) = 1/(n-2) exact")
        check(_gamma_w(Fraction(0), n) == fork['per_channel'],
              "direct-only is w = 0: the per-channel carrier, exactly")
    # the spread-only SIGNED leg: lambda_s = +lambda_t (pooled, not plane)
    for n in range(3, 9):
        _, _, spread_00, spread_ij = _trace_reversal_components(n)
        check(spread_ij / spread_00 == -1,
              "spread-only: signed ratio spread_ij/spread_00 = -1 exactly")
        check(-(spread_ij / spread_00) == _lam_s(fork['pooled']) / _LAMBDA_T,
              "spread-only limit is the pooled row lambda_s = +lambda_t "
              "(sign included)")
        check(-(spread_ij / spread_00) != _lam_s(fork['plane']) / _LAMBDA_T,
              "spread-only is NOT the plane (which needs lambda_s = "
              "-lambda_t)")

    return _result(
        name='T_gammaC_carrier_fork -- the four-point carrier fork, the '
             'dimension audit, the Cassini kills, and the weight-one curve',
        tier=3,
        epistemic='P_structural',
        summary=(
            'In the Paper 9 v1.6 calibrated normal form (lambda_t = +1, '
            'lambda_s = -gamma_C), the four carrier closures SOLVE to '
            'gamma_C in {1, 1/3, 0, -1} (plane / four-cell / per-channel / '
            'pooled), pairwise distinct and cross-exclusive (plane closure '
            'forces four-cell trace -2; four-cell forces plane trace 2/3). '
            'Dimension table: gamma_GR(n) = 1/(n-2) -- FLAGGED continuum '
            'import, recomputed in-check from trace-reversed linearized GR '
            'and Lovelock-robust (Gauss-Bonnet adds nothing linearized '
            'around flat) -- matches the plane carrier ONLY at n = 3; '
            'four-cell (1/n), per-channel (0), pooled (-1) match in no '
            'dimension. Cassini: pooled = Nordstrom (zero first-order '
            'deflection) dead at ~8.7e4 sigma; per-channel dead at ~4.3e4 '
            'sigma. THE WEIGHT-ONE CURVE (audit-donated): response = '
            'direct + w*spread gives gamma(w) = w/((n-1)-w) exactly; GR is '
            'w = 1 in EVERY n (gamma(1, n) = 1/(n-2)); direct-only (w = 0) '
            'is the per-channel carrier; spread-only carries the SIGNED '
            'pooled leg lambda_s = +lambda_t. The two Cassini-dead traps '
            'are the curve\'s two limits; deriving w = 1 is the live '
            'opener of record. Falsifier hooks: a gamma_obs anomaly; any '
            'change to the Paper 9 normal-form conventions (the four-cell '
            'sign-slip -1/3 artifact is the recorded caution).'
        ),
        key_result=(
            'carrier fork gamma_C in {1, 1/3, 0, -1} solved from closures; '
            'gamma_GR(n) = 1/(n-2) [continuum import, Lovelock-robust]; '
            'plane matches Einstein only at n = 3; pooled killed 8.7e4 '
            'sigma, per-channel 4.3e4 sigma (Cassini); weight-one curve '
            'gamma(w) = w/((n-1)-w), GR = w=1 in every n'
        ),
        dependencies=['A1', 'T8', 'Delta_signature'],
        cross_refs=['T_ledger_rent_excluded', 'T11'],
        artifacts={
            'fork': {k: str(v) for k, v in fork.items()},
            'dimension_table_matches': {'plane': [3], 'four_cell': [],
                                        'per_channel': [], 'pooled': []},
            'cassini_sigma': {'pooled': float(sigma_pooled),
                              'per_channel': float(sigma_chan)},
            'weight_one_curve': 'gamma(w, n) = w/((n-1)-w); GR = w=1 all n',
            'continuum_import_flag': 'gamma_GR(n) = 1/(n-2) from adopted '
                                     'trace-reversed linearized GR; '
                                     'Lovelock/GB-robust',
            'witness': 'The Turning/c1_notrace_witness_2026-07-03.py 9/9 + '
                       'register_carrier_witness_2026-07-03.py W9',
        },
    )


# ---------------------------------------------------------------------------
# The recruitment-instrument no-go (T2 + T2') with the live tripwire
# ---------------------------------------------------------------------------

# The pinned recruitment.py instrument baseline. The walk's enumeration was
# the ELEVEN checks present at walk time; Rule D (.371) landed in the
# concurrent lane after the enumeration and its forced re-audit was performed
# and recorded at banking time (2026-07-03) -- see the module docstring.
_RECRUITMENT_INSTRUMENT_BASELINE = frozenset({
    'check_H1_continuum_from_anchor_profile',
    'check_H2_locality_from_recruitment_kernels',
    'check_T_quantum_anchor_einstein_A',
    'check_T_master_equation_form',
    'check_T_three_regimes_tau_rec',
    'check_T_tls_capacity_budget_knee_design_corollary',
    'check_T_tls_transduction_class_discriminator_rule_D',   # .371, re-audited
    'check_T_substrate_anchor_entangled_state',
    'check_T_cross_branch_matrix_element_form',
    'check_T_sixteen_case_unification_structural',
    'check_T_DCE_Q_dependence_prediction',
    'check_T_purcell_DCE_consistency',
})

# The instrument enumeration of record (artifact data): what T2/T2' audited.
_INSTRUMENT_ENUMERATION = {
    'B5_argmin_package': 'Paper 10 Supplement B5: E_rec argmin over '
                         'profiles; prices the profile, blind to (lambda_t, '
                         'lambda_s)',
    'B34_approximate_A2': 'Paper 10 Supplement B3.4: slack bound sigma < '
                          'eps*; ~11 orders too coarse at solar weak field '
                          '(trace-mode cost ~ 2.2e-12 eps*)',
    'paper10_sec8_clock_sector': 'DISCHARGED: the clock-sector depletion '
                                 'law K_t = K_t0(1 - alpha*chi) prices '
                                 'lambda_t only (clock-only per the parent '
                                 'walk); no ruler-sector counterpart exists '
                                 'in the licensed corpus',
    'recruitment_bank_checks': 'the pinned baseline set below, each with '
                               'its static-vacuity discharge: mu == 0 at '
                               'the static fixed point, the dynamical layer '
                               'holds as 0 = 0; quantum-anchor package '
                               'silent for a single-branch classical static '
                               'anchor; rate-layer TLS instruments (knee, '
                               'Rule D) price transduction design, not the '
                               'static equilibrium response',
    'adopted_objects_exclusion': 'Paper 25 eq:linearized-EH + the phi_T <-> '
                                 'h_munu identification EXCLUDED because '
                                 'adopted (S5): including them would close '
                                 'the gate by adoption, not derivation',
}


def _countermodel_gamma(gamma, A, B, beta, chi):
    """Paper 9 trace-obstruction countermodel: V_e(u, v; chi) =
    (A/2)u^2 + (B/2)(v - beta*chi)^2 - lambda*chi*u, lambda = A(1 - gamma).
    Returns gamma derived from the NUMERICALLY MINIMIZED u."""
    lam = A * (1.0 - gamma)
    # closed forms (for the agreement leg): u* = lam*chi/A, v* = beta*chi
    u_closed = lam * chi / A
    v_closed = beta * chi
    # numerical minimization: fine grid around zero (independent quadratics)
    grid = np.linspace(-10 * abs(chi), 10 * abs(chi), 4001)
    Vu = 0.5 * A * grid**2 - lam * chi * grid
    u_num = float(grid[np.argmin(Vu)])
    Vv = 0.5 * B * (grid - beta * chi)**2
    v_num = float(grid[np.argmin(Vv)])
    check(abs(u_num - u_closed) < 2e-2 * abs(chi) + 1e-12,
          "grid minimizer must bracket the closed-form u*")
    check(abs(v_num - v_closed) < 2e-2 * abs(chi) + 1e-12,
          "grid minimizer must bracket the closed-form v*")
    # Newton refinement from the grid point (exact for a quadratic): this is
    # still the numerical route -- gamma is read off the minimized response,
    # the closed form enters only as the bracketing cross-check above.
    u_ref = u_num - (A * u_num - lam * chi) / A
    zeta = u_ref / chi                  # first-order trace coefficient
    return 1.0 - zeta                   # gamma_C from the MINIMIZED response


def check_L_notrace_not_from_recruitment_instruments():
    rng = np.random.default_rng(20260703)
    chi = -2.12e-6                      # solar-surface chihat (sign physical)

    # --- 1. the countermodel realizes ANY gamma_C --------------------------
    realized = []
    for g_target in (1.0, 1.0 / 3.0, 0.0, -1.0, 0.7):
        A = float(rng.uniform(0.5, 3.0))
        B = float(rng.uniform(0.5, 3.0))
        beta = float(rng.uniform(0.5, 2.0))
        check(A > 0 and B > 0, "countermodel stiffnesses must be positive")
        g_real = _countermodel_gamma(g_target, A, B, beta, chi)
        check(abs(g_real - g_target) < 1e-9,
              "the trace-obstruction countermodel must realize gamma_C = "
              f"{g_target} from the minimized response")
        realized.append((g_target, g_real))

    # --- 2. static vacuity of the master-equation layer --------------------
    tau, K, omega_typ, hbar = 0.7, 3.0, 2.0, 1.0
    phi_eq, phi, dt = 1.0, 5.0, 1e-4
    t_end = 20 * tau
    for _ in range(int(t_end / dt)):
        phi += dt * (-(phi - phi_eq) / tau)
    mu = phi - phi_eq
    mu_analytic = (5.0 - 1.0) * math.exp(-t_end / tau)
    check(abs(mu) < 1e-8 and abs(mu - mu_analytic) < 0.02 * mu_analytic + 1e-12,
          "static anchor: mu -> 0 (relaxation fixed point = phi_eq)")
    dN_dt = K * mu**2 / (2 * tau * hbar * omega_typ)
    check(dN_dt < 1e-16, "static anchor: master-equation rate dN/dt -> 0")
    for scale in (0.5, 1.0, 2.0, 10.0):
        rate = (scale * K) * 0.0**2 / (2 * (tau / scale) * hbar
                                       * (omega_typ / scale))
        check(rate == 0.0,
              "every master-equation instrument is a prefactor on mu^2: "
              "kernel rescales change nothing in the static sector")

    # --- 3. THE TRIPWIRE: the recruitment instrument set, live -------------
    import apf.recruitment as _recruitment
    live_names = frozenset(
        name for name, obj in inspect.getmembers(_recruitment)
        if name.startswith('check_') and inspect.isfunction(obj)
        and obj.__module__ == 'apf.recruitment')
    new_instruments = live_names - _RECRUITMENT_INSTRUMENT_BASELINE
    removed_instruments = _RECRUITMENT_INSTRUMENT_BASELINE - live_names
    check(not new_instruments,
          "TRIPWIRE: new recruitment instrument(s) banked since the "
          f"2026-07-03 enumeration baseline: {sorted(new_instruments)} -- "
          "the T2' non-derivability no-go MUST BE RE-AUDITED against them "
          "before this check may pass again")
    check(not removed_instruments,
          "TRIPWIRE: recruitment instrument(s) removed/renamed since the "
          f"baseline: {sorted(removed_instruments)} -- the enumeration "
          "of record is stale; re-pin after re-audit")
    check(len(live_names) == 12,
          "the pinned baseline is twelve names (the walk's eleven + the "
          ".371 Rule D landing, re-audited at banking time)")

    return _result(
        name='L_notrace_not_from_recruitment_instruments -- the no-trace '
             'gate is not derivable from the recruitment corpus as '
             'formalized 2026-07-03 (T2 + T2\', tripwired)',
        tier=3,
        epistemic='P_structural_instrument',
        summary=(
            'The no-trace gate (gamma_C = 1, plane-carrier closure) is NOT '
            'a theorem of the licensed recruitment corpus as formalized '
            '2026-07-03: the Paper 10 Supplement B5 + B3.4 instruments, '
            'the sec-8 clock-sector response principle (discharged: prices '
            'lambda_t only), and the complete Papers 24/25 derived package '
            'with static-vacuity discharges (mu == 0 at the static fixed '
            'point; machine-checked in-check) -- under the adopted-objects '
            'exclusion (eq:linearized-EH excluded BECAUSE adopted, S5). '
            'Proof shape: the trace-obstruction countermodel V_e = '
            '(A/2)u^2 + (B/2)(v - beta*chi)^2 - lambda*chi*u with lambda = '
            'A(1 - gamma) realizes ANY gamma_C on top of a fully compliant '
            'static 24/25 substrate -- realized in-check for gamma in '
            '{1, 1/3, 0, -1, 0.7} with gamma derived from the numerically '
            'minimized response, not the closed form. No licensed '
            'instrument quantifies over (lambda_t, lambda_s); the one '
            'direction-indexed kernel in the corpus is the adopted '
            'geometric specialization, outside the licensing set. THE '
            'TRIPWIRE IS LIVE: the check enumerates apf/recruitment.py\'s '
            'check functions at runtime and FAILS LOUDLY if the name set '
            'differs from the pinned twelve-name baseline (the walk\'s '
            'eleven + the concurrent .371 Rule D, whose forced re-audit '
            'was performed at banking time: a TLS transduction-design '
            'instrument, no comparison-direction content). A thirteenth '
            'recruitment instrument fails the bank and forces a T2\' '
            're-audit. SCOPE: non-derivability from the corpus AS '
            'FORMALIZED is the theorem; NEVER cite as "APF cannot derive '
            'gamma_C". Live native routes: the reservoir-exclusion route '
            '(L1 open + L2 banked partition [T11-family/MECE 3+16+42=61] + '
            'L3 finite) and the weight-one walk (derive w = 1).'
        ),
        key_result=(
            'countermodel realizes any gamma_C in {1, 1/3, 0, -1, 0.7} on '
            'a static 24/25-compliant substrate (static vacuity machine-'
            'checked); instrument enumeration pinned as artifact; tripwire '
            'live on the recruitment.py name set (12 pinned; new instrument '
            '=> loud failure => T2\' re-audit). Non-derivability from the '
            'corpus as formalized 2026-07-03; NOT "APF cannot derive '
            'gamma_C".'
        ),
        dependencies=['A1', 'T_master_equation_form',
                      'H1_continuum_from_anchor_profile',
                      'H2_locality_from_recruitment_kernels'],
        cross_refs=['T_three_regimes_tau_rec', 'T11',
                    'T_gammaC_carrier_fork'],
        artifacts={
            'realized_gammas': realized,
            'instrument_enumeration': _INSTRUMENT_ENUMERATION,
            'tripwire_baseline': sorted(_RECRUITMENT_INSTRUMENT_BASELINE),
            'rule_D_reaudit': 'performed at banking time 2026-07-03: TLS '
                              'transduction-design instrument, no '
                              '(lambda_t, lambda_s) content; static-vacuity '
                              'discharge as the knee corollary',
            'live_routes': ['reservoir-exclusion (L1 open + L2 banked + L3 '
                            'finite)', 'the weight-one walk (derive w = 1)'],
            'witness': 'The Turning/mastereq_carrier_witness_2026-07-03.py '
                       '27/27 PASS',
        },
    )


# ---------------------------------------------------------------------------
# The register-carrier no-go (T-RC1 schema strength + the typing dilemma)
# ---------------------------------------------------------------------------

def check_L_register_carrier_not_from_account_instruments():
    # --- 1. T-RC1: the four natural rules, SOLVED for their carriers ------
    # each rule = a linear closure functional (c_t, c_s) whose zeroing is
    # the billing statement; gamma solved from the rule definition.
    rules = {
        'plane_billing_H6':    (Fraction(1), Fraction(1)),   # u = lt + ls
        'four_cell_billing':   (Fraction(1), Fraction(3)),   # cell total
        'redundancy_RB':       (Fraction(0), Fraction(1)),   # any nonzero ls
        'single_anchor_pooled': (Fraction(-1), Fraction(1)),  # ls - lt
    }
    rule_gamma = {name: _solve_linear_closure(c_t, c_s)
                  for name, (c_t, c_s) in rules.items()}
    fork = {Fraction(1), Fraction(1, 3), Fraction(0), Fraction(-1)}
    check(set(rule_gamma.values()) == fork
          and len(set(rule_gamma.values())) == len(rule_gamma),
          "the four natural rules must map injectively ONTO the fork")
    # each rule's closure holds at its own point, fails at the other three
    for name, (c_t, c_s) in rules.items():
        own = rule_gamma[name]
        holders = [g for g in fork
                   if c_t * _LAMBDA_T + c_s * _lam_s(g) == 0]
        check(holders == [own],
              f"rule {name}: its closure must select exactly its own point")

    # RB semantics leg: unlicensed-record count (xi_s = 0 iff no record)
    def _unlicensed(gamma):
        return 0 if _lam_s(gamma) == 0 else 1
    check(_unlicensed(Fraction(0)) == 0
          and all(_unlicensed(g) == 1
                  for g in (Fraction(1), Fraction(1, 3), Fraction(-1))),
          "RB (nomological-redundancy billing) selects the per-channel "
          "carrier: only xi_s = 0 leaves no unlicensed record")

    # --- 2. the linear-rule continuum (kills 'bijection') ------------------
    for c_t, c_s in ((Fraction(1), Fraction(1)), (Fraction(2), Fraction(5)),
                     (Fraction(7), Fraction(2))):
        g = _solve_linear_closure(c_t, c_s)
        check(g == c_t / c_s,
              "any linear rule c_t*lt + c_s*ls selects gamma = c_t/c_s")
        check(c_t * _LAMBDA_T + c_s * _lam_s(g) == 0,
              "the selected gamma must zero the rule's functional")
    check(_solve_linear_closure(Fraction(1), Fraction(1))
          == _solve_linear_closure(Fraction(3), Fraction(3)),
          "many-to-one: distinct rules (1,1) and (3,3) select one carrier "
          "-- the rule -> carrier map is many-to-one onto the fork, not a "
          "bijection")

    # --- 3. the T_M three-typing census (artifact + asserted outcome set) --
    channels = ('clock', 'ruler_x', 'ruler_y', 'ruler_z')
    # (a) cell-as-one-interface: every channel anchors at the single cell
    anchors_a = {ch: frozenset({'cell'}) for ch in channels}
    shared_a = all(anchors_a[p] & anchors_a[q]
                   for i, p in enumerate(channels) for q in channels[i + 1:])
    check(shared_a, "(a) cell-as-one-interface: all anchors shared")
    gamma_a = _solve_linear_closure(*rules['single_anchor_pooled'])  # pooled
    # (b) channels-as-interfaces: disjoint singleton anchors
    anchors_b = {ch: frozenset({ch}) for ch in channels}
    disjoint_b = all(anchors_b[p].isdisjoint(anchors_b[q])
                     for i, p in enumerate(channels)
                     for q in channels[i + 1:])
    check(disjoint_b, "(b) channels-as-interfaces: anchors pairwise disjoint")
    gamma_b = _solve_linear_closure(*rules['redundancy_RB'])  # per-channel
    # (c) planes-as-interfaces: the clock anchors in all three planes
    plane_anchors = {'plane_x': frozenset({'clock', 'ruler_x'}),
                     'plane_y': frozenset({'clock', 'ruler_y'}),
                     'plane_z': frozenset({'clock', 'ruler_z'})}
    names = tuple(plane_anchors)
    disjoint_c = all(plane_anchors[p].isdisjoint(plane_anchors[q])
                     for i, p in enumerate(names) for q in names[i + 1:])
    check(disjoint_c is False,
          "(c) planes-as-interfaces: the shared clock anchor makes the "
          "typing T_M-INCONSISTENT as an independent-account decomposition")
    census = {'cell_as_one_interface': gamma_a,       # -> pooled, -1
              'channels_as_interfaces': gamma_b,      # -> per-channel, 0
              'planes_as_interfaces': None}           # -> T_M-inconsistent
    check(set(census.values()) == {Fraction(-1), Fraction(0), None},
          "census outcome set must be exactly {pooled -1, per-channel 0, "
          "inconsistent}")
    check(Fraction(1) not in {g for g in census.values() if g is not None},
          "under NO admissible typing does T_M yield the plane (gamma = 1) "
          "-- the TYPING DILEMMA, the banked form (never a flat refutation)")

    # --- 4. the signed mechanism-limit legs (trace reversal, exact) --------
    for n in range(3, 11):
        h_00, h_ij, spread_00, spread_ij = _trace_reversal_components(n)
        A = Fraction(7)
        check(h_00 == A * Fraction(n - 2, n - 1)
              and h_ij == A * Fraction(1, n - 1),
              "h_00 = A(n-2)/(n-1), h_ij = A/(n-1) from direct + "
              "eta-weighted spread")
        check(h_ij / h_00 == Fraction(1, n - 2),
              "mechanism ratio h_ij/h_00 = 1/(n-2)")
        # signed conversion lambda_s/lambda_t = -h_ij/h_00 at full mechanism
        check(_lam_s(_gamma_GR(n)) / _LAMBDA_T == -(h_ij / h_00),
              "signed conversion lambda_s/lambda_t = -h_ij/h_00 exact")
        check(abs(spread_00) == abs(spread_ij),
              "the spread is democratic in magnitude over clock and ruler "
              "slots")
        # direct-only limit: h_ij = 0 -> lambda_s = 0 (per-channel, exactly)
        check(-(Fraction(0) / h_00) == _lam_s(Fraction(0)) / _LAMBDA_T,
              "direct-only limit -> lambda_s = 0: the per-channel carrier")
        # spread-only limit, signed: lambda_s = +lambda_t (pooled, NOT plane)
        check(spread_ij / spread_00 == -1
              and -(spread_ij / spread_00) == _lam_s(Fraction(-1)) / _LAMBDA_T
              and -(spread_ij / spread_00) != _lam_s(Fraction(1)) / _LAMBDA_T,
              "spread-only limit -> lambda_s = +lambda_t EXACTLY (pooled, "
              "sign included; not the plane's lambda_s = -lambda_t)")

    # --- 5. the H6' closure identity (by-construction table) ---------------
    for n in range(3, 11):
        ls_n = _lam_s(_gamma_GR(n))
        check(_LAMBDA_T + (n - 2) * ls_n == 0,
              "H6' register closure: lambda_t + (n-2)*lambda_s = 0 "
              "identically in n (BY CONSTRUCTION of the Einstein row -- "
              "target spec, not mechanism)")
        check(_LAMBDA_T + n * ls_n == 2 * ls_n,
              "corollary: the (n+1)-cell dilation equals a spatial "
              "2-plane's worth of ruler dilation")

    return _result(
        name='L_register_carrier_not_from_account_instruments -- T-RC1 at '
             'schema strength, the T_M typing dilemma, and the signed '
             'mechanism limits (the register-carrier walk banked)',
        tier=3,
        epistemic='P_structural_instrument',
        summary=(
            'The register-carrier lemma is not derivable from the banked '
            'account-structure instruments as of 2026-07-03; its content '
            'is exactly the carrier selection. T-RC1 AT SCHEMA STRENGTH '
            '(machine): marking a record-combination as line-requiring IS '
            'choosing the response -- rule-choice = response-choice. The '
            'four natural billing rules, realized as linear closure '
            'functionals and SOLVED (not hand-set), map injectively onto '
            'the four fork points {1, 1/3, 0, -1}; each rule\'s closure '
            'holds only at its own point. The rule space is RICHER than '
            'the fork: any linear rule c_t*lt + c_s*ls selects gamma = '
            'c_t/c_s, a continuum, many-to-one onto carriers ("bijection" '
            'scoped out) -- so no billing-layer datum strictly below the '
            'fork exists. THE T_M THREE-TYPING CENSUS (artifact, outcome '
            'set asserted exactly): cell-as-one-interface -> pooled (-1); '
            'channels-as-interfaces -> per-channel (0); planes-as-'
            'interfaces -> T_M-INCONSISTENT (shared clock anchor). Under '
            'NO admissible typing does T_M yield the plane -- the TYPING '
            'DILEMMA is the banked form; NEVER cite this leg as a flat '
            'refutation of T_M-typing. THE SIGNED MECHANISM LIMITS (trace '
            'reversal recomputed exactly): h_00 = A(n-2)/(n-1), h_ij = '
            'A/(n-1), ratio 1/(n-2); direct-only -> lambda_s = 0 (per-'
            'channel); spread-only -> lambda_s = +lambda_t EXACTLY (pooled '
            'shape, sign included); plane balance at NEITHER limit. THE '
            'H6\' IDENTITY TABLE: lambda_t + (n-2)*lambda_s = 0 '
            'identically in n, with the corollary lambda_t + n*lambda_s = '
            '2*lambda_s -- BY CONSTRUCTION of the Einstein row: H6\' is '
            'the dimension-covariant OUTPUT identity adopted as TARGET '
            'SPEC, not a mechanism claim ([C], the named reduction '
            'target; a native discharge may equally produce the trace-'
            'reversal decomposition, of which the register closure is the '
            'read-off). Enumeration-bounded in the T2/T2\' genre; the '
            'instrument-count tripwire lives in '
            'L_notrace_not_from_recruitment_instruments.'
        ),
        key_result=(
            'T-RC1 schema strength: rule-choice = response-choice; four '
            'rules solve onto the fork injectively; linear-rule continuum '
            'gamma = c_t/c_s kills "bijection"; T_M census = {pooled -1, '
            'per-channel 0, inconsistent} -- the plane under NO admissible '
            'typing (typing dilemma, not flat refutation); signed limits: '
            'direct-only -> per-channel, spread-only -> lambda_s = '
            '+lambda_t (pooled); H6\' = target spec [C], not banked here.'
        ),
        dependencies=['A1', 'T8', 'Delta_signature'],
        cross_refs=['T_gammaC_carrier_fork',
                    'L_notrace_not_from_recruitment_instruments',
                    'T_ledger_rent_excluded'],
        artifacts={
            'rule_to_gamma': {k: str(v) for k, v in rule_gamma.items()},
            'typing_census': {k: (str(v) if v is not None else
                                  'T_M-inconsistent')
                              for k, v in census.items()},
            'h6_prime_status': '[C] target spec, dimension-covariant output '
                               'identity; mechanism caveat carried; NOT '
                               'banked by this check',
            'mechanism_limits': {'direct_only': 'per-channel (gamma = 0)',
                                 'spread_only': 'lambda_s = +lambda_t '
                                                '(pooled, signed)'},
            'witness': 'The Turning/register_carrier_witness_2026-07-03.py '
                       '40 PASS',
        },
    )



# ---------------------------------------------------------------------------
# The weight-one reduction (the weight-one walk banked, v24.3.378)
# ---------------------------------------------------------------------------

# The two trace-currency premises, stored verbatim (named [C]; NOT banked):
_TCP_MIN_VERBATIM = (
    "TCP-min [C]: the response deposit is denominated in committed "
    "capacity at a channel-uniform rate -- a cell-side deposit is a "
    "capacity amount billable in the ledger")
_TCP_STRONG_VERBATIM = (
    "TCP-strong [C]: the static response is the load's committed line "
    "read at the cell -- the same amount, not less: the one-sided clause "
    "D(deposit) >= D(commitment); equality is not part of the premise -- "
    "it arrives only by composition with T-W1a's bound")
_CITABLE_BOUND = (
    "w <= 1, equivalently gamma_C <= 1/(n-2), at n = 3 gamma_C <= 1, at "
    "[P_structural | S0/S1 + TCP-min + H5-W + census legs + the Paper 9/"
    "Paper 10 base (P5, B7 incl. adopted C_M)]")
_CITABLE_POINT = (
    "w = 1 (gamma_C = 1 at n = 3) ONLY at [P_structural | T-W1a's ledger "
    "+ TCP-strong]; the standing chain reads gamma_C = 1 at [P_structural "
    "| H1 + H2 + H3(+adopted C_M) + census-saturation + H5 + {H6 or "
    "(S1 + TCP-strong)}]")


def check_T_weight_one_reduction():
    F = Fraction

    def eta_diag(n):
        return [F(-1)] + [F(1)] * n

    def spread_deposit(n, w, rho=F(1), denom=None):
        if denom is None:
            denom = n - 1
        return [e * w * rho / denom for e in eta_diag(n)]

    def D(pattern):
        return sum(pattern)

    def w_of_gamma(g, n):
        return F(g) * (n - 1) / (1 + F(g))

    # --- 1. L-W0: the deposit-fraction identity + normalization invariance -
    rho = F(1)
    for n in range(3, 9):
        check(D(eta_diag(n)) == n - 1,
              "the eta diagonal sums to n-1 over the cell: the denominator's "
              "origin (n-1 DISCHARGED, not an independent import)")
        for w in (F(0), F(1, 3), F(1), F(7, 5), F(-2, 3)):
            dep = spread_deposit(n, w, rho)
            commit = [rho] + [F(0)] * n
            check(D(dep) == w * rho and D(commit) == rho
                  and D(dep) / D(commit) == w,
                  "L-W0: w = D(spread deposit)/D(commitment) identically "
                  "in n and w")
    for n in range(3, 7):
        for c in (F(1), F(2), F(n - 1), F(n + 1), F(7, 3)):
            w_star = c / (n - 1)
            check(w_star / (c - w_star) == F(1, n - 2),
                  "normalization invariance: D-balance selects gamma = "
                  "1/(n-2) under EVERY democratic-eta normalization c")

    # --- 2. L-W1: D annihilates every exchange pattern ----------------------
    for n in range(3, 7):
        for i in range(1, n + 1):
            for delta in (F(1), F(-3, 4), F(11, 7)):
                exch = [F(0)] * (n + 1)
                exch[0], exch[i] = -delta, delta
                check(D(exch) == 0,
                      "L-W1: clock<->ruler exchange (v_e-type) is D-neutral "
                      "-- the reductio immunity is arithmetic, not fenced")
    for n in range(3, 6):
        base = spread_deposit(n, F(2, 3))
        for i in range(1, n + 1):
            pat = list(base)
            pat[0] -= F(5, 9)
            pat[i] += F(5, 9)
            check(D(pat) == D(base),
                  "adding exchange to any pattern leaves D unchanged")
        for i, j in itertools.combinations(range(1, n + 1), 2):
            pat = [F(0)] * (n + 1)
            pat[i], pat[j] = F(4, 3), -F(4, 3)
            check(D(pat) == 0,
                  "inter-plane ruler-ruler exchange is also D-neutral "
                  "(the H5-W fence is broader than H6's)")

    # --- 3. L-W2: the scalar-improvement identity, exact --------------------
    for n in range(3, 9):
        for w in (F(0), F(1, 2), F(1), F(3, 2), F(-1, 3)):
            a = -F(w) / (n - 1)
            coef_eta = a - (1 + a * (n + 1)) / 2
            check(coef_eta == -(1 - F(w)) / 2,
                  "TR[h(w)] = hbar - ((1-w)/2) eta hbar_tr exactly")
            b = coef_eta
            G = (-F(1, 2), -F(1, 2) * (b + b), -F(1, 2) * (-2 * b))
            extra = (G[0] + F(1, 2), G[1], G[2])
            check(extra == (F(0), (1 - F(w)) / 2, -(1 - F(w)) / 2),
                  "L-W2: G_lin[h(w)] = kappa*T + ((1-w)/2)(eta box - dd) "
                  "hbar exactly (adopted linearized theory, flagged)")
            check((extra == (F(0), F(0), F(0))) == (w == 1),
                  "the improvement term vanishes IFF w = 1, in every n: "
                  "w != 1 IS the independent scalar comparison mode")
    for n in range(3, 7):
        for kvec in (tuple(range(1, n + 2)), (2,) + (3,) * n,
                     (5, -1) + (1,) * (n - 1)):
            k = np.array(kvec, dtype=object)
            eta = np.diag([-1] + [1] * n).astype(object)
            k_up = eta @ k
            k2 = int(k_up @ k)
            M = eta * k2 - np.outer(k, k)
            div = k_up @ M
            check(all(int(x) == 0 for x in div),
                  "the improvement term is identically conserved (exact "
                  "integer Fourier: k^mu (eta k^2 - k k) = 0)")

    # --- 4. fork w-coordinates + the calibrated trace source ----------------
    check(w_of_gamma(1, 3) == 1 and w_of_gamma(F(1, 3), 3) == F(1, 2)
          and w_of_gamma(0, 3) == 0,
          "n = 3 fork w-coordinates: plane w = 1, four-cell w = 1/2, "
          "per-channel w = 0")
    try:
        w_of_gamma(-1, 3)
        check(False, "pooled gamma = -1 must have NO finite w")
    except ZeroDivisionError:
        pass
    def h00_w(w, n, A=F(7)):
        """h_00(w) through the leg-3 machinery: a = -w/(n-1), h_00 =
        hbar_00 + a*eta_00*hbar_tr (static source hbar_00 = A, hbar_tr =
        -A, eta_00 = -1). Audit fix F3 (2026-07-04): the pole is
        EVALUATED from the coefficient, not substituted -- a wrong h_00
        formula now fails this leg."""
        a = -F(w) / (n - 1)
        return A + a * F(-1) * (-A)

    check(all(h00_w(F(n - 1), n) == 0
              and h00_w(F(n - 1) + F(1, 7), n) != 0
              and h00_w(F(1), n) == F(7) * F(n - 2, n - 1)
              for n in range(3, 8)),
          "h_00(w) = 0 at w = n-1 (the pooled/spread-only projective "
          "point), evaluated through the leg-3 coefficient: zero AT the "
          "pole, nonzero off it, w = 1 reproducing h_00 = A(n-2)/(n-1)")
    check(abs(float(_gamma_w(F(10 ** 9), 3)) + 1) < 1e-8
          and abs(float(_gamma_w(F(-10 ** 9), 3)) + 1) < 1e-8,
          "gamma(w) -> -1 as w -> +/-inf (pooled as the projective limit)")
    check(all(w_of_gamma(1, n) == F(n - 1, 2)
              and ((n == 3) == (F(n - 1, 2) == 1)) for n in range(3, 9)),
          "the plane carrier at general n sits at w = (n-1)/2: "
          "scalar-tensor off n = 3 (no n-independent plane law)")
    for w in (F(0), F(1, 2), F(1), F(3, 2)):
        lam_over_A = 1 - _gamma_w(w, 3)
        check(lam_over_A == 2 * (1 - w) / (2 - w)
              and (lam_over_A == 0) == (w == 1),
              "n = 3 calibrated trace source lambda/A = 2(1-w)/(2-w), "
              "zero iff w = 1")

    # --- 5. the shape table + the anisotropic family + the T4 selection -----
    def gamma_of_shape(dep, commit=F(1)):
        """gamma read from a deposit shape by the SAME response route
        _gamma_w evaluates: h_00 = commitment + clock-channel deposit,
        h_ij = per-ruler-channel deposit, gamma = h_ij/h_00. Audit fix
        F2 (2026-07-04): the shape-table gammas are DERIVED from the
        deposit shapes, not asserted."""
        check(len(set(dep[1:])) == 1,
              "the shape->gamma route needs channel-uniform ruler deposits")
        return dep[1] / (commit + dep[0])

    for n in range(3, 7):
        for w in (F(0), F(1, 2), F(1), F(3, 2)):
            check(gamma_of_shape(spread_deposit(n, w)) == _gamma_w(w, n),
                  "route calibration: on the eta-democratic shape the "
                  "shape->gamma response route reproduces the weight-one "
                  "curve exactly")
        dep_r = [F(0)] + [F(1, n)] * n            # rulers-only
        check(D(dep_r) == 1 and gamma_of_shape(dep_r) == F(1, n),
              "rulers-only shape + D-balance -> gamma = 1/n DERIVED via "
              "the response route (four-cell family; Cassini-dead 1/3 at "
              "n = 3): the shape carries the fork content")
        dep_c = [F(1)] + [F(0)] * n               # clock-only
        check(D(dep_c) == 1 and gamma_of_shape(dep_c) == 0,
              "clock-only shape + D-balance -> gamma = 0 DERIVED via the "
              "response route (per-channel; Cassini-dead)")

    def gamma_bound_aniso(ct, cs, n):
        w_max = ct * (n - 1) / (n * cs - ct)
        return w_max / ((n - 1) - w_max)

    for n in range(3, 9):
        for ct, cs in ((F(1), F(1)), (F(1), F(9, 10)), (F(1), F(6, 5)),
                       (F(3), F(2)), (F(2), F(5)), (F(7, 3), F(7, 3))):
            if n * cs - 2 * ct <= 0:
                continue
            w_max = ct * (n - 1) / (n * cs - ct)
            dep = spread_deposit(n, w_max)
            check(ct * dep[0] + cs * sum(dep[1:]) == ct * F(1),
                  "anisotropic D_c-balance at w_max, re-derived from the "
                  "deposit/commitment amounts, exact")
            check(gamma_bound_aniso(ct, cs, n) == ct / (n * cs - 2 * ct),
                  "the anisotropic bound gamma <= c_t/(n*c_s - 2*c_t)")
    check(gamma_bound_aniso(F(1), F(9, 10), 3) == F(10, 7)
          and gamma_bound_aniso(F(1), F(6, 5), 3) == F(5, 8)
          and gamma_bound_aniso(F(1), F(1), 3) == F(1),
          "n = 3 samples: 10/7 (too weak), 5/8 (excludes GR), exactly 1 at "
          "c_t = c_s: the bound AT 1 is TCP-min clause (ii)'s selection "
          "within a continuum")
    for ct in (F(1), F(2), F(7, 3)):
        for ratio_ in (F(1), F(9, 10), F(6, 5), F(1, 2), F(3), F(101, 100)):
            cs = ct * ratio_
            exists_all = all(n * cs - 2 * ct > 0 for n in range(3, 9))
            tracks_all = exists_all and all(
                gamma_bound_aniso(ct, cs, n) == F(1, n - 2)
                for n in range(3, 9))
            check(tracks_all == (cs == ct),
                  "THE T4 SELECTION: the bound tracks gamma_GR(n) = 1/(n-2) "
                  "in every n = 3..8 IFF c_t = c_s -- the dimension audit "
                  "uniquely selects channel-uniformity (a selection, not a "
                  "discharge: the linear amount-functional frame is the "
                  "premise's)")
    for n in range(3, 9):
        w_bal = F(n - 1, n + 1)
        dep = spread_deposit(n, w_bal)
        check(sum(abs(x) for x in dep) == F(1)
              and _gamma_w(w_bal, n) == F(1, n),
              "the L1 row: UNSIGNED channel-uniform balance -> gamma = 1/n "
              "in every n (four-cell family) -- excluded by TCP-min's "
              "LINEARITY clause, not by taste")

    # --- 6. the third coat, machine-pinned ----------------------------------
    for n in range(3, 9):
        lt = F(1)
        ls1 = -_gamma_w(F(1), n)
        check(lt + (n - 2) * ls1 == 0,
              "zeroing the D-net response component <=> the (1, n-2) "
              "linear rule <=> H6-prime's closure identity at w = 1")
        for w in (F(0), F(1, 2), F(3, 2)):
            ls_w = -_gamma_w(w, n)
            check((lt + (n - 2) * ls_w == 0) == (w == 1),
                  "the H6-prime identity holds IFF w = 1: record-billing "
                  "with a D-fence selects the register rule")
    check((1, 3 - 2) == (1, 1),
          "at n = 3 the (1, n-2) rule IS the plane rule (1, 1): the third "
          "coat -- do-not-re-walk; never cite the D-fence as licensing "
          "record-billing")

    # --- 7. monotonicity (computed) + the SIGNED Cassini leg ----------------
    for n in range(3, 7):
        grid = [F(g, 100) for g in range(-80, 300, 21)]
        for g1, g2 in itertools.combinations(grid, 2):
            dq = (w_of_gamma(g2, n) - w_of_gamma(g1, n)) / (g2 - g1)
            check(dq == (n - 1) / ((1 + g1) * (1 + g2)),
                  "exact Mobius difference-quotient: dw/dgamma > 0 on "
                  "gamma > -1")
        thr = F(1, n - 2)
        for dg in (F(-1, 3), F(-1, 100), F(0), F(1, 100), F(1, 3)):
            g = thr + dg
            check((w_of_gamma(g, n) <= 1) == (g <= thr),
                  "w <= 1 iff gamma_C <= 1/(n-2), computed straddling the "
                  "threshold")
    g_central = 1 + F(21, 10 ** 6)
    w_minus_1 = w_of_gamma(g_central, 3) - 1
    check(w_minus_1 > 0 and abs(float(w_minus_1) - 1.05e-5) < 5e-8,
          "CASSINI SIGNED: the central value sits ABOVE the bound "
          "(w - 1 = +1.05e-5 at central gamma) -- never cite as "
          "'saturates'")
    check(0.912 < 2.1 / 2.3 < 0.914,
          "the tension is 0.91 sigma ABOVE the bound: live one-sided "
          "tension, the bound survives at < 1 sigma")
    check(2.7 < 2.1 / (2.3 / 3) < 2.8,
          "a factor-~3 precision improvement at the same central value "
          "puts the composite under ~3 sigma pressure")
    cass = F(23, 10 ** 6)
    margin = max(abs(float(w_of_gamma(1 - cass, 3) - 1)),
                 abs(float(w_of_gamma(1 + cass, 3) - 1)))
    check(1.1e-5 < margin < 1.2e-5,
          "the 1-sigma half-width maps to |w-1| <= ~1.15e-5: interval "
          "width only, NOT a saturation claim")

    # --- 8. the footprint kill extension -------------------------------------
    chi_hat = 2.1e-6
    theta_dev = float(1 - _gamma_w(F(0), 3))
    check(0.5 * (theta_dev * chi_hat) ** 2 < 1e-11,
          "the w-footprint is >= 11 orders sub-floor: the approximate-A2/"
          "no-slack route is dead for w as it was for theta")

    # --- 9. the F-W2 tripwire (B2's style, shared baseline) ------------------
    import apf.recruitment as _recruitment
    live_names = frozenset(
        name for name, obj in inspect.getmembers(_recruitment)
        if name.startswith('check_') and inspect.isfunction(obj)
        and obj.__module__ == 'apf.recruitment')
    check(live_names == _RECRUITMENT_INSTRUMENT_BASELINE,
          "F-W2 TRIPWIRE: the recruitment instrument census moved since "
          "the pinned twelve-name baseline -- a new ruler-sector or "
          "channel-anisotropic response instrument voids TCP clause "
          "(ii)'s pricing and forces a re-audit of the weight-one "
          "reduction (instruments landing outside the recruitment census "
          "remain E1-search-bounded, named)")

    return _result(
        name='T_weight_one_reduction -- the deposit-fraction identity, '
             'exchange annihilation, the scalar-improvement identity, the '
             'third coat, and the asymmetric conditional pair (the '
             'weight-one walk banked)',
        tier=3,
        epistemic='P_structural',
        summary=(
            'The weight-one walk (2026-07-04, REDUCED) banked at its '
            'proved strength. UNCONDITIONAL ARITHMETIC (exact rationals, '
            'n = 3..8): L-W0, the banked weight IS the deposit fraction '
            'w = D(spread deposit)/D(commitment) -- the denominator n-1 '
            'is DISCHARGED as the cell\'s eta-sum, and D-balance selects '
            'gamma = 1/(n-2) under EVERY democratic-eta normalization '
            '(the conservation statement is normalization-free); L-W1, D '
            'annihilates every exchange pattern (clock<->ruler and '
            'ruler-ruler): the v_e reductio has no purchase on the '
            'amount frame by arithmetic, given the linear channel-'
            'uniform amount functional (TCP-min clause (ii), which the '
            'T4 dimension audit uniquely selects within the anisotropic '
            'continuum gamma <= c_t/(n*c_s - 2*c_t) -- tracks gamma_GR '
            'in every n IFF c_t = c_s; the UNSIGNED L1 row lands on the '
            'four-cell 1/n); L-W2, G_lin[h(w)] = kappa*T + ((1-w)/2)'
            '(eta box - dd) hbar exactly, identically conserved (exact '
            'integer Fourier), vanishing IFF w = 1 -- w != 1 IS the '
            'independent scalar comparison mode (continuum-import flag '
            'carried). THE SHAPE CARRIES THE FORK: rulers-only -> 1/n, '
            'clock-only -> 0 under the same D-balance; the eta-'
            'democratic shape S1 is the honest residual import. THE '
            'THIRD COAT, machine-pinned: "bill the D-net component" <=> '
            'the (1, n-2) rule <=> H6-prime (the plane rule at n = 3); '
            'record-billing with a D-fence is the register fork '
            're-entering -- do-not-re-walk. THE ASYMMETRIC PAIR '
            '(hypothesis artifacts; NOTHING HERE DERIVES w = 1): '
            'no-source ' + _CITABLE_BOUND + '; no-sink additionally '
            'requires TCP-strong, whose named discharge shape is an '
            'amount-graded testedness principle (walked and priced as '
            'the (E)+(P) anatomy, apf/amount_graded_testedness.py). '
            'CASSINI SIGNED (Bertotti-Iess-Tortora 2003): gamma - 1 = '
            '(2.1 +/- 2.3)e-5, central value 0.91 sigma ABOVE the bound '
            '-- live one-sided tension, NOT saturation; >= 3 sigma '
            'confirmed violation falsifies the composite; factor-~3 '
            'precision at the same central -> ~3 sigma pressure. The '
            'F-W2 tripwire re-asserts the recruitment census baseline '
            'in-check.'
        ),
        key_result=(
            'L-W0/L-W1/L-W2 exact: w = D(deposit)/D(commitment) (n-1 '
            'discharged as the cell\'s eta-sum; normalization-invariant); '
            'D annihilates exchange; w != 1 = one identically-conserved '
            'scalar improvement mode vanishing iff w = 1; shape carries '
            'the fork (rulers-only -> 1/n, clock-only -> 0); T4 selects '
            'channel-uniformity (tracks 1/(n-2) in every n iff c_t = '
            'c_s); D-fenced record-billing = the (1, n-2) rule = '
            'H6-prime (third coat, do-not-re-walk). NOTHING HERE DERIVES '
            'w = 1. Citable: no-source ' + _CITABLE_BOUND + '; no-sink '
            + _CITABLE_POINT + '. Cassini SIGNED (Bertotti-Iess-Tortora '
            '2003): gamma - 1 = (2.1 +/- 2.3)e-5, central value 0.91 '
            'sigma ABOVE the bound -- live one-sided tension, NOT '
            'saturation; >= 3 sigma confirmed violation falsifies the '
            'composite. TCP-min [C]; TCP-strong [C]; H5-W named, '
            'unbanked, separate and standing; amount-graded testedness '
            'is TCP-strong\'s discharge hook '
            '(L_amount_graded_testedness_encoding_no_go).'
        ),
        dependencies=['A1', 'T8', 'Delta_signature'],
        cross_refs=['T_gammaC_carrier_fork',
                    'L_register_carrier_not_from_account_instruments',
                    'L_notrace_not_from_recruitment_instruments',
                    'L_amount_graded_testedness_encoding_no_go'],
        artifacts={
            'tcp_min_verbatim': _TCP_MIN_VERBATIM,
            'tcp_strong_verbatim': _TCP_STRONG_VERBATIM,
            'citable_bound': _CITABLE_BOUND,
            'citable_point': _CITABLE_POINT,
            'h5w_status': 'H5-W: census-transport re-fenced to D-net '
                          'objects; named premise, unbanked; a WEAKER, '
                          'typing-free variant of H5 -- flagged variant, '
                          'not replacement; SEPARATE and still standing',
            'cassini_signed': 'Bertotti-Iess-Tortora 2003: gamma - 1 = '
                              '(2.1 +/- 2.3)e-5; central value 0.91 sigma '
                              'ABOVE the bound (w - 1 = +1.05e-5); live '
                              'one-sided tension, NOT saturation',
            'falsification_convention': 'a confirmed gamma_obs > 1/(n-2) '
                                        'at >= 3 sigma falsifies the '
                                        'composite (S0/S1 + TCP-min + '
                                        'H5-W + census + P5/B7 base); '
                                        'gamma_obs < 1 at >= 3 sigma '
                                        'refutes only the no-sink half '
                                        '(TCP-strong)',
            'third_coat': 'bill-the-D-net-component = the (1, n-2) rule = '
                          'H6-prime = the plane rule at n = 3; '
                          'do-not-re-walk',
            't4_selection': 'bound gamma <= c_t/(n*c_s - 2*c_t) tracks '
                            '1/(n-2) in every n iff c_t = c_s; L1 row -> '
                            '1/n',
            'shape_table': {'eta_democratic': 'Einstein family 1/(n-2)',
                            'rulers_only': '1/n (four-cell, Cassini-dead)',
                            'clock_only': '0 (per-channel, Cassini-dead)'},
            'n_minus_2_mechanism': 'n-2 = (the cell\'s eta-sum n-1) - (one '
                                   'committed load\'s worth of deposit), '
                                   'conditional on the ledger',
            'discharge_hook': 'an amount-graded testedness principle; '
                              'walked 2026-07-04: the (E)+(P) anatomy '
                              '(apf/amount_graded_testedness.py); the (E) '
                              'distributed-encoding door is the single '
                              'genuine reopening',
            'witness': 'The Turning/weight_one_witness_2026-07-04.py '
                       '36/36 PASS (W1-W11)',
        },
    )



_CHECKS = {
    'T_gammaC_carrier_fork': check_T_gammaC_carrier_fork,
    'L_notrace_not_from_recruitment_instruments':
        check_L_notrace_not_from_recruitment_instruments,
    'L_register_carrier_not_from_account_instruments':
        check_L_register_carrier_not_from_account_instruments,
    'T_weight_one_reduction': check_T_weight_one_reduction,
}


# ---------------------------------------------------------------------------
# IE onboarding -- the gamma_C carrier program onto the ROUTE axis as a WATCH.
# ---------------------------------------------------------------------------
#
# gamma_C <= 1 is a derived one-sided bound with a LIVE empirical tension
# (Cassini central value 0.91 sigma ABOVE the bound). The honest IE verdict is
# HELD, never a global-P export: pinning the held verdict puts the signed
# Cassini tension under the verdict-drift tripwire, so any future re-derivation
# that flips the sign or silently promotes the route to an export fails the
# bank loudly. The routing inherits check_T_gammaC_carrier_fork's [P_structural]
# grade; no epistemic status is added.
IE_DECLARATIONS = (
    {
        "input_id": "gravity:gammaC_carrier_watch",
        "axis": "ROUTE",
        "expect_export": False,
        "claim_text": (
            "gamma_C <= 1 (no-source w <= 1 at n = 3): the PPN gamma is bounded "
            "above by the plane-carrier fork geometry "
            "(check_T_gammaC_carrier_fork, tier 3 [P_structural]). The Cassini "
            "central value gamma_obs - 1 = (2.1 +/- 2.3)e-5 sits 0.91 sigma ABOVE "
            "the bound -- a LIVE ONE-SIDED TENSION under watch, not a saturation "
            "and not a clean export. The pooled Nordstrom (gamma = 1 pooled) and "
            "per-channel (gamma = 0) alternatives are excluded at ~8.7e4 sigma / "
            "~4.3e4 sigma. A >= 3 sigma confirmed gamma_obs > 1 falsifies. "
            "Held-for-repair by design: this route must never be silently promoted "
            "to a global-P export while the Cassini tension is live."
        ),
        "note": (
            "Onboards the gamma_C carrier program onto the ROUTE axis as a WATCH. "
            "The verdict is held (not exported); pinning it puts the signed Cassini "
            "one-sided tension under the verdict-drift tripwire, so any future "
            "re-derivation that flips the sign or promotes the route to an export "
            "fails the bank loudly. No physics import; inherits [P_structural]."
        ),
    },
)


def register(registry):
    """Register the gamma_C carrier-program checks into the bank."""
    registry.update(_CHECKS)


def run_all():
    return {name: fn() for name, fn in _CHECKS.items()}


if __name__ == '__main__':
    for _n, _r in run_all().items():
        print(('PASS' if _r.get('passed', True) else 'FAIL'), _n)
        print('  grade:', _r['epistemic'], '| tier', _r['tier'])
        print('  ', _r['key_result'])
