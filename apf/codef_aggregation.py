"""The CoDef aggregation-selection corollary: A2 on the T_sep gradient.

For a pair of distinctions {d1, d2} at a finite-capacity interface, sharing
an interface has two orthogonal consequences: the SUBADDITIVE axis
(check_T_sep [P] -- overlapping anchor supports make joint defense strictly
cheaper than the sum, the shared substrate directions being paid once) and
the SUPERADDITIVE axis (the IJC excess -- a genuinely joint threat escaping
to a pool sector adds cost).  This module banks the corollary that on the
subadditive side, least-cost selection points at aggregation:

    CoDef(d1, d2)  :=  (M_d1 /\\ M_d2 != {})  AND  (W_12 subset-of M_d1 (+) M_d2)

    (overlapping anchors; contained joint threat).  Under K3-additive
    support-billing, the NAMED FD3-definitional coverage premise (every
    defense configuration engages each direction of M_d1 | M_d2 at least
    once -- an undefended anchor direction is an undefended distinction),
    and the well-posedness rider eps_joint = cost(M_d1 | M_d2) <= C_Gamma:

    (a) eps_joint < eps_apart = cost(M_d1) + cost(M_d2), with EXACT deficit
        cost(M_d1 /\\ M_d2) > 0 -- T_sep's subadditivity clause
        (inclusion-exclusion for an additive set function; the identity is
        already banked in check_T_sep; this corollary COMPOSES it).
    (b) The containment clause adds NO excess term to the joint bill, by
        support-billing alone: a contained threat engages nothing outside
        M_d1 | M_d2.  The Sep/IJC dichotomy machinery is NOT consumed
        (cross-ref only); zero excess here is K3/FD3 construction.
    (c) cost(M_d1 | M_d2) is a GLOBAL lower bound over all covering defense
        configurations -- any configuration pays each union direction at
        least once, sum(m_i c_i) >= sum(c_i) for integer m_i >= 1 and
        c_i > 0, with equality iff every m_i = 1 -- so the aggregated
        (engage-once) configuration is the UNIQUE global argmin
        (uniqueness from deficit > 0; BW not load-bearing).
    (d) A2 (Minimum Cost Selection -- CONSTITUTIVE AXIOM, NAMED here the way
        occupancy is named) selects the aggregated configuration among the
        admissible ones.  Where capacity binds (eps_joint <= C < eps_apart)
        A1 excludes the SEPARATED configuration (selection still names A2:
        over-engaged configurations can remain admissible); in the
        TIGHTENED WINDOW eps_joint <= C < eps_joint + min_{i in union} c_i
        every non-minimal covering engagement is inadmissible and A1 alone
        forces aggregation (the aggregated configuration is the unique
        admissible one).

OUTSIDE CoDef the corollary is SILENT: an escaped threat direction is
K3-billed and the sign of (deficit - escape cost) is undetermined -- both
outcomes are exhibited below.  CoDef is scope, not a derived gate.

GRADE [P] on the constitutive base, A2 NAMED, CoDef-scoped, STATICS ONLY
(a configuration-ordering statement).  Grading basis of record: A2 is a
constitutive axiom root (crystal_axiom_roots PLEC anchor 'A2'; "a named
certificate target, not a theorem" [Paper 1 Supp v8.43] means NAME it, not
sub-[P] -- the occupancy precedent); the FD3 -> A2 reduction FAILS at
selection strength (2026-07-03 Mythos ruling: budget-tightness derived,
between-branch selection a named target), so this corollary does NOT close
below A2.

READING REMARK (outside the claim): the corollary gives the imported
tendency-toward-aggregation (Paper 37's Gamma_app; the energy-condition-
shaped input GR-side) an internal constitutive counterpart -- least-cost
selection descends the T_sep subadditivity gradient toward co-defendable
aggregation.  The identification "this is gravity's attractive sign" is a
READING and stays outside the claim: check_T9_grav derives the Einstein
equations from Lovelock and imports no sign for this corollary to supply.
NAMED OPENS: (dyn) the dynamic realization -- the transition/realignment
cost of the merge, where attract-vs-metastable is decided (Paper 37
class_transition is the named home); (phys) whether physical matter is
CoDef (an identification); (law) the force law, downstream.

FENCES (both hostile audits): no P4 coverage-kappa anywhere -- P4's kappa
is substrate-defense coverage |S_substrate /\\ M_d| / |M_d| and
check_kappa_zero_Tsep derives kappa = 0 from DISJOINT mechanisms (the
opposite convention); the refuted 2026-07-07 prototype's mechanism-overlap
substitution is a stamped do-not-re-walk.  No entropic route (check_T_entropy
makes S = committed cost; the second law drives cost UP).  No E_rec / gamma_C
(magnitude, not sign).  "A1 alone forces" outside the tightened window is
FALSE (round-2 counterexample) -- do not restate it.

Provenance: walk_T_aggregation_drive_v01-v03.py + two hostile audits
(REDUCE 0.82 -> LAND-WITH-FIXES 0.85, all 13 fixes carried), The
Turning/kappa_master_knob_2026-07-07/; banked per principal ruling
2026-07-07 ("proceed as recommended").

Grade [P].  Dependencies: A1, T_sep, L_epsilon*, Regime_R (A2's axiom-root
check).  Cross-refs: T_IJC_dichotomy, L_MD_extension,
L_threat_substrate_realization (the escaped-threat reading),
kappa_zero_Tsep + P4_IMP (the P4-side kappa convention this corollary
deliberately does not touch).
"""

from fractions import Fraction as F
from itertools import combinations, product

from apf.apf_utils import check, _result

# The witness substrate: six directions with exact positive rational
# per-direction costs (SP/K2); K3-additive billing.
_COSTS = {0: F(3, 2), 1: F(1), 2: F(7, 3), 3: F(2), 4: F(5, 4), 5: F(1, 2)}


def _cost(S):
    return sum(_COSTS[i] for i in S) if S else F(0)


def _anchors():
    universe = sorted(_COSTS)
    out = []
    for r in range(1, len(universe) + 1):
        out += [frozenset(c) for c in combinations(universe, r)]
    return out


def check_L_codef_aggregation_argmin():
    """L_codef_aggregation_argmin: A2 selects aggregation on CoDef pairs.

    Corollary of T_sep [P] + A2 (named constitutive axiom).  See the
    module docstring for the full statement, grade block, fences, and
    named opens.  Witness legs (all exact-rational, every clause asserts):

      Leg 1  deficit identity: cost(M1) + cost(M2) == cost(M1|M2) +
             cost(M1&M2) exactly, on all 1953 anchor pairs of the
             6-direction universe AND on 25 random positive-rational cost
             maps (the identity is inclusion-exclusion for additive set
             functions -- the algebra carries the generality, the
             enumeration corroborates).  Overlap <=> strict deficit ==
             cost(shared) > 0; disjoint <=> exact additivity (T_sep's
             biconditional, composed).
      Leg 2  zero excess under containment: bill_joint = cost(union) +
             cost(escaped); contained => escaped empty => excess 0 by
             construction (support-billing; the dichotomy machinery is
             cross-ref only, not consumed).
      Leg 3  global argmin: on every CoDef pair, sum(m_i c_i) >= eps_joint
             for multiplicity vectors m_i >= 1, equality iff engage-once
             (exhaustive over {1,2}^union for |union| <= 4 -- cutoff
             flagged, the one-line algebra covers all multiplicities --
             plus a random spot-check in {1..3} on every pair).
      Leg 4  selection: A2 (NAMED) selects the unique global argmin ==
             aggregated on all A1-admissible CoDef pairs; where capacity
             binds, A1 excludes the separated configuration; in the
             tightened window (C < eps_joint + cheapest union direction)
             the aggregated configuration is the UNIQUE admissible one
             (A1-only forcing, verified exhaustively).
      Leg 5  outside-CoDef silence: cheap escape (< deficit) still
             aggregates; dear escape (> deficit) does not -- both signs on
             the one witness; the corollary asserts nothing outside CoDef.
    """
    import random as _random
    rng = _random.Random(20260707)
    anchors = _anchors()
    check(len(anchors) == 63, "anchor universe: 63 nonempty subsets")

    # ---- Leg 1: the deficit identity, algebraically general ----------
    def _identity_sweep(costmap):
        def c(S):
            return sum(costmap[i] for i in S) if S else F(0)
        for Ma, Mb in combinations(anchors, 2):
            check(c(Ma) + c(Mb) == c(Ma | Mb) + c(Ma & Mb),
                  "inclusion-exclusion exact")
            if Ma & Mb:
                check(c(Ma) + c(Mb) - c(Ma | Mb) == c(Ma & Mb) > 0,
                      "overlap => strict deficit == cost(shared) > 0")
            else:
                check(c(Ma) + c(Mb) == c(Ma | Mb),
                      "disjoint => exact additivity (T_sep converse)")

    _identity_sweep(_COSTS)
    for _ in range(25):
        _identity_sweep({i: F(rng.randint(1, 720), rng.randint(1, 720))
                         for i in _COSTS})

    # ---- Legs 2-4: CoDef pairs -- zero excess, global argmin, selection
    def bill_joint(M1, M2, W12):
        return _cost(M1 | M2) + _cost(W12 - (M1 | M2))

    C_nonbind = F(25)
    C_bind = F(8)
    n_codef = n_bind = n_window = 0
    for Ma, Mb in combinations(anchors, 2):
        if not (Ma & Mb):
            continue
        n_codef += 1
        union = sorted(Ma | Mb)
        W12 = frozenset(Ma & Mb)                    # contained joint threat
        check(W12 <= (Ma | Mb), "CoDef clause (ii): containment")
        ej = bill_joint(Ma, Mb, W12)
        check(ej == _cost(Ma | Mb), "Leg 2: zero excess under containment")
        ea = _cost(Ma) + _cost(Mb)
        check(ea == ej + _cost(Ma & Mb) > ej, "apart over-pays by the deficit")
        # Leg 3: global lower bound; exhaustive for small unions (cutoff
        # flagged), random multiplicity spot-check for every pair.
        if len(union) <= 4:
            for mvec in product((1, 2), repeat=len(union)):
                bill = sum(m * _COSTS[i] for i, m in zip(union, mvec))
                check(bill >= ej, "covering engagement >= eps_joint")
                if bill == ej:
                    check(all(m == 1 for m in mvec),
                          "equality iff engage-once (unique argmin)")
        mvec = tuple(rng.randint(1, 3) for _ in union)
        bill = sum(m * _COSTS[i] for i, m in zip(union, mvec))
        check(bill >= ej and (bill > ej or all(m == 1 for m in mvec)),
              "random multiplicity spot-check")
        # Leg 4: selection.
        check(ea < C_nonbind, "non-binding regime: both configurations admissible")
        if ej <= C_bind < ea:
            n_bind += 1                             # A1 excludes SEPARATED only
            cheapest = min(_COSTS[i] for i in union)
            if C_bind < ej + cheapest:
                n_window += 1                       # A1-only forcing, genuine
                for mvec in product((1, 2), repeat=len(union)):
                    if any(m > 1 for m in mvec):
                        bill = sum(m * _COSTS[i] for i, m in zip(union, mvec))
                        check(bill >= ej + cheapest > C_bind,
                              "tightened window: non-minimal engagement inadmissible")
    check(n_codef == 1652, "1652 CoDef pairs enumerated")
    check(0 < n_window < n_bind, "binding + tightened-window regimes both realized")

    # ---- Leg 5: outside-CoDef silence (both signs, one witness) -------
    Ma, Mb = frozenset({0, 1, 2}), frozenset({1, 2, 3})          # deficit 10/3
    check(bill_joint(Ma, Mb, frozenset(Ma & Mb) | {5}) < _cost(Ma) + _cost(Mb),
          "cheap escape (1/2 < 10/3): still aggregates")
    Mc, Md = frozenset({0, 5}), frozenset({1, 5})                # deficit 1/2
    check(bill_joint(Mc, Md, frozenset(Mc & Md) | {2}) > _cost(Mc) + _cost(Md),
          "dear escape (7/3 > 1/2): does NOT aggregate")

    return _result(
        name='L_codef_aggregation_argmin',
        tier=4,
        epistemic='P',
        summary=(
            'Corollary of T_sep [P] + A2 (NAMED constitutive axiom): for CoDef '
            'pairs (overlapping anchors, contained joint threat) under '
            'K3-additive support-billing, the named FD3 coverage premise, and '
            'the rider eps_joint <= C, the aggregated configuration is the '
            'unique GLOBAL argmin -- eps_joint = cost(M1|M2) < eps_apart with '
            'exact deficit cost(M1&M2) > 0, zero excess by construction (the '
            'Sep/IJC dichotomy machinery is cross-ref only, not consumed) -- '
            'and A2 selects it; where capacity binds, A1 excludes the separated '
            'configuration (selection still names A2); in the tightened window '
            'eps_joint <= C < eps_joint + cheapest-union-direction, A1 alone '
            'forces aggregation. Statics only; silent outside CoDef; BW not '
            'load-bearing. The gravity-sign identification is a READING outside '
            'the claim (T9_grav imports no sign). Named opens: dynamic '
            'realization (Paper 37 class_transition), matter-is-CoDef, force law.'
        ),
        key_result=(
            'CoDef(d1,d2) => aggregated configuration = unique global argmin '
            '(deficit == cost(M1&M2) exactly, T_sep); A2 (named) selects it; '
            'tightened window gives A1-only forcing; silent outside CoDef [P]'
        ),
        dependencies=['A1', 'T_sep', 'L_epsilon*', 'Regime_R'],
        cross_refs=['T_IJC_dichotomy', 'L_MD_extension',
                    'L_threat_substrate_realization', 'kappa_zero_Tsep',
                    'P4_IMP'],
        artifacts={
            'universe': '6 directions, exact positive rational costs; 63 anchors, 1953 pairs',
            'leg1_identity': 'PASS (fixed + 25 random cost maps, exact)',
            'leg2_zero_excess': 'PASS (all 1652 CoDef pairs)',
            'leg3_global_argmin': 'PASS (exhaustive |union|<=4, flagged cutoff; random m in {1..3} all pairs)',
            'leg4_selection': 'PASS (non-binding; binding excludes separated; tightened window A1-only)',
            'leg5_silence': 'PASS (cheap 1/2 < 10/3 aggregates; dear 7/3 > 1/2 does not)',
            'coverage_premise': 'NAMED (FD3-definitional: every configuration engages each union direction >= once)',
            'a2_status': "constitutive axiom root (crystal_axiom_roots 'A2'); NAMED, occupancy precedent",
            'fd3_reduction': 'FAILS at selection strength (2026-07-03 ruling); no closure below A2',
            'fences': 'no P4-kappa; no entropic route; no T9_grav import; no E_rec',
            'note_home': 'The Turning/kappa_master_knob_2026-07-07/',
        },
    )


_CHECKS = {
    'L_codef_aggregation_argmin': check_L_codef_aggregation_argmin,
}


def register(registry):
    """Register the CoDef aggregation-selection corollary into the bank."""
    registry.update(_CHECKS)
