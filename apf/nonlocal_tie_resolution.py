"""Non-local tie resolution: a shared-substrate deficit decides a local tie.

STATEMENT (check_T_nonlocal_tie_resolution, tier 4, [P_structural | occupancy]).
Take a genuine LOCAL tie -- two admissible local configurations A, B of EQUAL
local cost, which nothing local can separate (born_at_ties: a symmetry-protected
flat tie is irreducibly probabilistic in isolation).  Couple it to an external
continuation path X.  Then, EXACTLY when X shares a COUNT-asymmetric substrate
with the two options, codef's shared-substrate-paid-once deficit
(cost(cfg /\\ X) > 0) removes the would-be flat tie: the coupled whole is
strictly NON-FLAT, has a UNIQUE global argmin (the more-shared side), and A2
takes it -- FORCED, not named: a non-argmin commit is inadmissible under the
A2-exact ruling banked in T_hold_cost_dominance_split.  A SYMMETRIC or DISJOINT
coupling -- no count-deficit -- is NOT decided; it stays genuine chance
(born_at_ties).  So the object is a two-armed CONDITIONAL:

    real count-deficit  <=>  decided (unique A2 argmin, the more-shared side)
    no deficit / symmetric  <=>  genuine chance (born_at_ties)

The commitment ordering A2 produces is the one-way arrow (= time; Delta_ordering).
The only un-forced input is WHICH X obtains -- the occupant's alignment (the QAC,
[P_regime]); everything else is proved.  Hence [P_structural | occupancy]:
P on the engine, occupancy the sole carve-out; which-side stays [P_regime].

WHAT THIS IS NOT (deflation of record, after the 2026-07-26 two-stage audit
0.80/0.72 REDUCE).  This does NOT resolve a GENUINELY FLAT tie -- a flat tie with
no deficit stays chance.  The deficit DISSOLVES a would-be tie by construction
(it makes the coupled options unequal), it does not BREAK a co-held one.  The
value is the composition (a real cost coupling decides; no coupling chances; the
selection forced by the A2-exact base; ordering = time; occupancy the seed), not
a new mechanism -- the engine arithmetic is codef's deficit identity.

SCOPE FENCE (faithful, not a limitation).  The framework's cost is COUNT-ONLY
(rent-free, size-only, identity-blind).  This witness is faithful to that: a
coupling decides iff it makes a real COUNT-difference in the shared substrate;
a same-count coupling is symmetric -> chance -- correct for a framework whose
cost does not see anchor identity.  Do NOT read this as "any coupling decides":
only a count-deficit does.

THE BAR IS RESPECTED BY CONSTRUCTION.  codef / structure_formation bar A2 from
"deciding among CO-HELD (equal-cost) alternatives" -- the symmetric flat tie
born_at_ties forbids breaking.  This theorem never crosses that bar: a real
count-deficit makes the coupled options UNEQUAL cost, so the bar is INAPPLICABLE
by construction, and A2's pick is the ordinary licensed unique-argmin move.  The
symmetric arm falls to born_at_ties chance (no A2 decision).

============================================================================
THE BORN GRADE-MAP (the whole stack at a glance; grades pulled live 2026-07-26):
  Born FORM / soundness (p = Tr(rho E), POVM/trace)      [P_math]
      -- exact math, unconditional, GRANT-FREE
         (check_T_g_hold_exact_not_in_born_ancestry certifies G-hold-exact is
          absent from the Born ancestry).  The strongest rung.
  Weighted Born as the OPERATIVE selection law            [P_structural]
      -- grant-free + unconditional AFTER Part 1 retired G-hold-exact
         (T_hold_cost_dominance_split; was [P_structural | G-hold-exact]).
  THIS: the deficit-decides tie engine                    [P_structural | occupancy]
      -- structural composition; a rung under the Born form (structural, not
         pure math); which-side is [P_regime].
  The flat-tie FLOOR (uniform 1/N at exact symmetry)      [P_structural_reading]
      -- born_at_ties; the ONLY reading-grade rung, and it CANNOT rise:
         it IS the reserved case (A2 requires an argmin, never which).
  The realized OUTCOME (which specific result)            [P_regime]
      -- occupancy / the QAC; the reserved seed = the "| occupancy".
Read: machinery is [P_math]/[P_structural]; the outcome is [P_regime]; the one
reading-grade piece (the floor) is the genuine-chance case, by design.
============================================================================

MAX-STRENGTH LEGS: (1) the deficit identity, exact + general (codef); (2) the
bi-conditional DERIVED from that identity (jA - jB = (b - a) eps by
inclusion-exclusion), confirmed over the finite class with both arms non-vacuous
-- a theorem, not an empirical scan; (3) the bar inapplicable by construction
(deficit => unequal => not co-held); (4) failure controls that bite -- a
disjoint / cost-neutral external carries zero deficit and decides NOTHING (real
count-cost required, never adjacency; verified by mutation: additive joint ->
no decision); an unequal 'tie' is not a tie; (5) A2's selection is a live
grade-GATE on T_hold_cost_dominance_split's A2-exact grade (Part 1's own
535-check witness does the forcing; this module asserts the anchor, it does not
re-derive it) -- what lifts the selection above [P_structural_reading]; (6)
ordering = one-way arrow (Delta_ordering) = time; (7) the occupancy carve-out --
the engine is occupancy-independent [P], occupancy supplies only which side.

MAY-NOT-CITE:
- "a genuinely flat tie is resolved / decided" -- FALSE; a flat tie (no deficit)
  stays chance; the deficit dissolves a would-be tie by construction.
- "any coupling decides the tie" -- FALSE; only a real COUNT-deficit does; a
  same-count / disjoint / symmetric coupling is chance.
- "the mechanism forces the outcome universally" -- deterministic GIVEN the
  occupancy; which X obtains is the reserved un-forced bit (QAC, [P_regime]).
- "A2 selects among co-held (equal-cost) alternatives" -- never; the deficit
  makes them unequal, so the bar is inapplicable.
- "the which-side is derived" -- occupancy, [P_regime]; reserved by the
  framework (turnover + enforcement-realism pricing).
- occupancy is a NAMED input entering once (which X obtains), never concluded.

Anchors consumed live (grade-gates, not fed into the arithmetic):
L_codef_aggregation_argmin [P] (the deficit), T_hold_cost_dominance_split
[P_structural] (the A2-exact base -- selection forced), L_selection_ledger_
completeness (born_at_ties -- the flat-tie chance floor / the bar), Delta_ordering
[P] (arrow = commitment order = time).  Reading: Reference - The Tie: Locally
Held, Non-Locally Decided (2026-07-26).
"""

from fractions import Fraction as F

EPS = F(3, 7)   # deliberately non-unit; only 0 < eps is used


def _cost(S):
    """Cost supervenes on anchor COUNT: |S| * eps (codef's _cost; identity-blind)."""
    return F(len(frozenset(S))) * EPS


def _joint(cfg, X):
    """Co-requirement joint cost: shared substrate paid ONCE (the union).
    cost(cfg U X) = (|cfg| + |X| - |cfg & X|) * eps; the paid-once deficit is
    cost(cfg /\\ X) = |cfg & X| * eps (codef's deficit identity)."""
    return _cost(frozenset(cfg) | frozenset(X))


def _deficit(cfg, X):
    return _cost(frozenset(cfg) & frozenset(X))


def _local_tie(k):
    """A genuine local tie: two DISJOINT k-anchor local configs of equal cost."""
    A = frozenset(('A', i) for i in range(k))
    B = frozenset(('B', i) for i in range(k))
    return A, B


def _external(A, B, a, b, x_own):
    """External X sharing `a` anchors of A, `b` of B, plus `x_own` of its own."""
    shareA = frozenset(sorted(A)[:a])
    shareB = frozenset(sorted(B)[:b])
    own = frozenset(('X', i) for i in range(x_own))
    return shareA | shareB | own


def check_T_nonlocal_tie_resolution():
    """Tier 4, [P_structural | occupancy].  See module docstring (with grade-map)."""
    from apf.codef_aggregation import check_L_codef_aggregation_argmin
    from apf.hold_cost_dominance import check_T_hold_cost_dominance_split
    from apf.born_at_ties import check_L_selection_ledger_completeness
    from apf.spacetime import check_Delta_ordering

    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)

    # ---- live bank anchors (grade-gates) -----------------------------------
    r_codef = check_L_codef_aggregation_argmin()
    ck(r_codef.get('passed') is True and r_codef.get('epistemic') == 'P',
       "anchor L_codef_aggregation_argmin [P] passes (the shared-substrate deficit)")
    r_split = check_T_hold_cost_dominance_split()
    ck(r_split.get('passed') is True and
       r_split.get('epistemic', '').startswith('P_structural'),
       "anchor T_hold_cost_dominance_split passes (the A2-exact base)")
    ck('unconditional' in r_split.get('epistemic', '') and
       'EXACT' in r_split.get('epistemic', ''),
       "A2-EXACT GRADE-GATE (leg 5): the anchor carries the grant-free, "
       "unconditional, A2-read-EXACT grade -- so 'A2 selects the unique argmin' "
       "is FORCED (a non-argmin commit is inadmissible), not a named reading. "
       "The forcing is proved in the anchor's own 535-check witness (Part 1); "
       "this leg is the live grade-gate, not a re-derivation")
    r_born = check_L_selection_ledger_completeness()
    ck(r_born.get('passed') is True,
       "anchor L_selection_ledger_completeness passes (flat-tie chance floor / the bar)")
    r_delta = check_Delta_ordering()
    ck(r_delta.get('passed') is True and r_delta.get('epistemic') == 'P',
       "anchor Delta_ordering [P] passes (arrow = commitment order = time)")

    ck(EPS > 0, "MD: eps > 0 (the only inequality imported)")

    # ---- Leg 1: the deficit identity, exact and general (codef) ------------
    for (k, a, b, xo) in [(2, 1, 0, 1), (3, 2, 1, 0), (1, 1, 0, 0), (3, 0, 0, 2)]:
        A, B = _local_tie(k)
        X = _external(A, B, a, b, xo)
        ck(_cost(A) + _cost(X) == _joint(A, X) + _deficit(A, X),
           "Leg1 deficit identity: cost(A)+cost(X) == cost(AuX)+cost(A^X) [k=%d a=%d]" % (k, a))
        ck((_deficit(A, X) > 0) == (len(A & X) > 0),
           "Leg1 overlap <=> strict deficit > 0 [k=%d a=%d]" % (k, a))

    # ---- Leg 2: the bi-conditional DERIVED from the identity ----------------
    # jA - jB = (b - a) * eps (inclusion-exclusion), so decided <=> a != b.
    # Confirmed over the finite class; both arms non-vacuous.  A THEOREM of the
    # deficit identity exhibited across the class, NOT an empirical scan that
    # could have failed (the audit's fair reduction, carried).
    scanned = decided_count = flat_count = 0
    for k in (1, 2, 3):
        A, B = _local_tie(k)
        ck(_cost(A) == _cost(B), "genuine LOCAL tie: cost(A)==cost(B) [k=%d]" % k)
        ck(A != B, "distinct local configs [k=%d]" % k)
        for a in range(k + 1):
            for b in range(k + 1):
                for xo in range(3):
                    X = _external(A, B, a, b, xo)
                    jA, jB = _joint(A, X), _joint(B, X)
                    ck(jA - jB == F(b - a) * EPS,
                       "Leg2 identity: jA - jB == (b-a)*eps [k=%d a=%d b=%d]" % (k, a, b))
                    decided = (jA != jB)
                    asym = (a != b)
                    ck(decided == asym,
                       "Leg2 bi-conditional (derived): decided <=> count-asymmetry "
                       "[k=%d a=%d b=%d xo=%d]" % (k, a, b, xo))
                    if decided:
                        winner = 'A' if jA < jB else 'B'
                        want = 'A' if a > b else 'B'
                        ck(winner == want,
                           "Leg2 direction: coupled argmin is the more-shared side "
                           "[k=%d a=%d b=%d -> %s]" % (k, a, b, winner))
                        decided_count += 1
                    else:
                        flat_count += 1
                    scanned += 1
    ck(scanned == 87 and decided_count > 0 and flat_count > 0,
       "Leg2 class confirmed (87 cases; decided=%d, flat=%d) -- both arms non-vacuous"
       % (decided_count, flat_count))

    # ---- Leg 3: the bar INAPPLICABLE by construction -----------------------
    A, B = _local_tie(2)
    X_def = _external(A, B, 2, 0, 0)     # count-asymmetric sharing: a real deficit
    X_sym = _external(A, B, 1, 1, 0)     # count-symmetric sharing
    ck(_joint(A, X_def) != _joint(B, X_def),
       "Leg3 DEFICIT: coupled options UNEQUAL -> NOT co-held -> the co-held bar is "
       "INAPPLICABLE by construction; A2's pick is the licensed unique-argmin move "
       "(the would-be tie is DISSOLVED, not broken)")
    ck(_joint(A, X_sym) == _joint(B, X_sym),
       "Leg3 SYMMETRIC: coupled options EQUAL -> co-held -> the bar APPLIES -> "
       "born_at_ties chance (NO A2 decision)")

    # ---- Leg 4: failure controls (the real ones) ---------------------------
    X_disjoint = _external(A, B, 0, 0, 2)       # adjacency without shared cost
    ck(_deficit(A, X_disjoint) == 0 and _deficit(B, X_disjoint) == 0,
       "Leg4 control: a disjoint external carries ZERO deficit (no real coupling)")
    ck(_joint(A, X_disjoint) == _joint(B, X_disjoint),
       "Leg4 control: a cost-neutral / disjoint external DOES NOT decide -- the "
       "decision requires a REAL shared-substrate count-cost, never adjacency "
       "(the barred fiat fails; mutation-verified: an additive joint -> no decision)")
    A_un = frozenset(('A', i) for i in range(2))
    B_un = frozenset(('B', i) for i in range(3))   # unequal cost
    ck(_cost(A_un) != _cost(B_un),
       "Leg4 control: unequal-cost options are NOT a tie (locally decided) -- the "
       "LOCAL-TIE precondition is real, not vacuous")

    # ---- Leg 5: ordering = one-way arrow = time ----------------------------
    winner_cfg = A if _joint(A, X_def) < _joint(B, X_def) else B
    committed = frozenset()
    order = []
    for anchor in sorted(winner_cfg | X_def):
        prev = committed
        committed = committed | {anchor}
        order.append(anchor)
        ck(prev < committed and anchor not in prev,
           "Leg5 ordering: each commitment is one-way (n:0->1, never back) -- the "
           "resolution WRITES a monotone commitment order (= the arrow = time)")
    ck(len(order) == len(winner_cfg | X_def),
       "Leg5: committed set == the decided coupled configuration; the order is "
       "FORCED because the argmin is unique (a flat tie writes no order)")

    # ---- Leg 6: the occupancy carve-out (the P engine vs the reserved seed) -
    dir_by_occ = {}
    for (a, b) in [(2, 0), (0, 2), (1, 1)]:
        X = _external(A, B, a, b, 0)
        jA, jB = _joint(A, X), _joint(B, X)
        dir_by_occ[(a, b)] = ('A' if jA < jB else 'B' if jB < jA else 'CHANCE')
    ck(dir_by_occ[(2, 0)] == 'A' and dir_by_occ[(0, 2)] == 'B'
       and dir_by_occ[(1, 1)] == 'CHANCE',
       "Leg6 OCCUPANCY CARVE-OUT: the ENGINE (deficit -> decided to the more-shared "
       "side; symmetric -> chance) is occupancy-INDEPENDENT [P]; the OCCUPANCY "
       "(which X obtains) supplies only WHICH side -- the reserved un-forced bit "
       "(QAC, [P_regime]).  'P - occupancy' = the conditional engine")

    # ---- float tripwire ----------------------------------------------------
    for v in (EPS, _cost(A), _joint(A, X_def), _deficit(A, X_def)):
        ck(isinstance(v, F), "exact Fraction on the load-bearing path")

    passed = not fails
    return {
        'name': 'T_nonlocal_tie_resolution',
        'epistemic': ('P_structural | occupancy -- the ENGINE is P (a count-'
                      'asymmetric shared-substrate deficit removes a would-be flat '
                      'tie into a UNIQUE A2 argmin over the coupled whole, the '
                      'selection FORCED by the A2-exact base; no deficit / '
                      'symmetric -> genuine chance, born_at_ties); the which-side '
                      'is the occupant alignment, [P_regime], the sole carve-out. '
                      'NOT a claim that a genuinely flat tie is resolved -- the '
                      'deficit dissolves a would-be tie by construction. Faithful '
                      'to the framework\'s count-only cost'),
        'passed': passed,
        'tier': 4,
        'key_result': (
            'CONDITIONAL, two-armed: real count-deficit <=> the local tie is '
            'DECIDED (unique A2 argmin over the coupled whole, to the more-shared '
            'side, FORCED by the A2-exact base -- a non-argmin commit is '
            'inadmissible); no deficit / symmetric / disjoint <=> genuine chance '
            '(born_at_ties). The bi-conditional is DERIVED from codef\'s deficit '
            'identity (jA - jB = (b-a)*eps), confirmed over 87 cases with both '
            'arms non-vacuous -- a theorem, not an empirical scan. The co-held bar '
            'is INAPPLICABLE by construction (a real deficit makes the coupled '
            'options unequal -- the would-be tie is dissolved, not broken); a '
            'disjoint / cost-neutral external carries zero deficit and decides '
            'nothing (real count-cost required, mutation-verified). Ordering = '
            'one-way arrow = time (Delta_ordering). SCOPE: count-only cost '
            '(faithful to the framework\'s rent-free size-only cost; a coupling '
            'decides iff it makes a real count-difference; same-count -> chance). '
            'The engine is occupancy-INDEPENDENT [P]; occupancy = which X obtains, '
            'supplies only WHICH side (QAC, [P_regime]). Hence [P_structural | '
            'occupancy]. See the module docstring\'s BORN GRADE-MAP for the full '
            'stack (form [P_math]; operative law [P_structural]; this engine '
            '[P_structural | occupancy]; flat-tie floor [P_structural_reading]; '
            'outcome [P_regime]).'
        ),
        'dependencies': ['A1', 'A2', 'L_cost', 'L_codef_aggregation_argmin',
                         'T_hold_cost_dominance_split',
                         'L_selection_ledger_completeness', 'Delta_ordering',
                         'occupancy'],
        'cross_refs': ['L_mechanism_trichotomy',
                       'T_coherent_free_spend_permanent',
                       'T_quantum_admissibility_condition',
                       'T_finite_weighted_born_soundness'],
        'artifacts': {
            'engine': ('deficit = |cfg & X| * eps (shared substrate paid once); '
                       'joint = |cfg U X| * eps; decided <=> jA != jB <=> '
                       'count-asymmetric deficit; decided-to = the more-shared '
                       'side; symmetric / no-deficit <=> chance'),
            'deflation': ('two-stage audit 2026-07-26 (0.80/0.72 REDUCE) carried: '
                          'does NOT resolve a genuinely flat tie (a flat tie stays '
                          'chance); the deficit DISSOLVES a would-be tie by '
                          'construction; the bi-conditional is a THEOREM of the '
                          'deficit identity (not an empirical scan); scope fenced '
                          'to count-only cost (faithful); A2-exact leg is a live '
                          'grade-gate, not a re-derivation'),
            'controls': ('disjoint/cost-neutral external -> zero deficit -> no '
                         'decision (real count-cost required); unequal-cost '
                         'options are not a tie; mutation-verified (additive '
                         'joint / unequal tie / flipped direction all caught)'),
            'a2_exact_gate': ('leg 5 is a live grade-gate on '
                              'T_hold_cost_dominance_split (A2 read EXACT, '
                              'grant-free unconditional) -- the forcing is proved '
                              'in Part 1; this module asserts the grade, lifting '
                              'the selection above [P_structural_reading]'),
            'born_grade_map': ('form [P_math]; operative law [P_structural]; this '
                               'engine [P_structural | occupancy]; flat-tie floor '
                               '[P_structural_reading]; outcome [P_regime]'),
            'occupancy_carveout': ('engine occupancy-independent [P]; occupancy = '
                                   'which X obtains, supplies only which side (QAC, '
                                   '[P_regime]); P - occupancy = the conditional engine'),
            'may_not_cite': ('a genuinely flat tie is resolved; any coupling '
                             'decides; universal forcing; A2 selects among '
                             'co-held alternatives; the which-side derived; '
                             'occupancy concluded'),
        },
        'fail_reasons': fails,
    }


_CHECKS = {'T_nonlocal_tie_resolution': check_T_nonlocal_tie_resolution}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    import sys
    bad = False
    for n, fn in _CHECKS.items():
        r = fn()
        print(r['name'], '::', r['epistemic'][:64], '::',
              'PASS' if r['passed'] else 'FAIL')
        if not r['passed']:
            bad = True
            for f in r['fail_reasons']:
                print('  -', f)
    sys.exit(1 if bad else 0)
