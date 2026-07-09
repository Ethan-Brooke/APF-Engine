"""The frustrated choice family: an exact admissible whole whose every
proper part is inadmissible, with the barrier carried entirely by
dangling-threat defence cost.

L_frustrated_witness.  Under the premise stack below there EXISTS, in the
FD5b threat-defence cost structure with exact positive-rational
per-direction costs, a frustrated choice family: a whole X of 3
distinctions over a 9-direction universe (anchors a_i cheap, passivation
directions h_(i,j) dear; M_i = {a_i}; one bond threat p_(i,j) per ordered
pair with MONOTONE membership -- p_(i,j) in T(S) iff d_i in S, so FD5
containment (T_IJC_dichotomy Step 3; graded-FD5 monotone dominance,
L_graded_threat_collapses_to_crisp) is respected at the membership level
-- and configuration-dependent, sector-clean defence supports:
W(p_(i,j), S) = {a_i} when d_j in S, contained, zero escape;
W(p_(i,j), S) = {a_i, h_(i,j)} when d_j not in S, dangling, escapes) such
that:

  (1) bill(X) = 15/4 exactly, X fully-contained (zero escaped threat
      directions); EVERY proper nonempty subset S bills >= 9 > bill(X),
      with the excess PURE dangling escape -- anchor-support cost alone
      is always admissible (the load-bearing clause; the excess-equals-
      escape decomposition is true by the billing construction).
  (2) On the exact nonempty window C in [15/4, 9) = [bill(X),
      min_S bill(S)) -- an interval, not a tuned point; sup-tightness
      exhibited -- X is A1-admissible and every proper part is
      A1-inadmissible.
  (3) Consequence: with single-flip moves (add/remove one distinction)
      gated on A1-admissible endpoints, the admissible configuration
      graph at any window C is exactly {empty, X} in TWO components:
      empty cannot reach X (BFS-exact).  GATE-INDEPENDENCE of the
      keystone direction: under the UNADAPTED gapless_serial_floor
      moves() convention (removals ungated), BFS from empty still
      reaches only {empty}; the both-directions gate is the A1 endpoint
      condition under non-monotone bills (an ungated removal would
      occupy a bill > C state) and is load-bearing only for the
      X-isolation phrasing (under the unadapted gate X descends to empty
      only through states billing above C -- exhibited).
  (4) Control (the no-rigging baseline): configuration-INDEPENDENT
      threat supports with FD5-legal monotone membership can NEVER
      frustrate under this billing convention -- the billed set
      M(S) | union of live fixed supports is monotone under inclusion,
      so bill(S) <= bill(X) for all S (algebra asserted + seeded
      enumeration here; the full 80-draw per-distinction + 200-draw
      monotone-membership sweep is the lane walker's).  Configuration-
      dependent supports are therefore NECESSARY for frustration.
  (5) Convention boundary, quantified: per-threat multiplicity billing
      leaves the barrier intact (escaped sets threat-disjoint), but
      NO-anchor-sharing billing collapses it -- bill_noshare(X) = 45/4
      >= 11 = min proper -- so the consumed codef convention is
      load-bearing (premise stack item 2).

PREMISE STACK (the adjudicated grade line; section references in item 1
are to WITNESS_NOTE_v0.2.md, carried verbatim from its Section 0 item 1):

  1. P-dangling (OPEN, NAMED premise -- ADJUDICATED, DANGLES_NOTE_v0.2.md
     in this lane; adjudication hostile-audited UPHOLD-WITH-EDITS, edits
     carried).  Threat-defence supports may be configuration-dependent:
     W_p(S) != W_p(S') for the same live threat p, with every
     partner-present support contained in the standing anchor union.
     Precedents are PRECEDENT-ONLY: per-configuration threat structure in
     T_IJC_dichotomy/L_Pi (the banked superadditive direction);
     configuration-relative AGGREGATE defence in
     L_threat_substrate_realization [P_structural_reading, Step-2 clause
     HOLD-NAMED] -- membership-induced only (one fixed support per
     threat, escape at the larger configuration), i.e. inside the class
     control leg W10 proves cannot frustrate.  Neither is a license, and
     the landscape route to deriving the premise is KILLED (missing
     clause: the off-argmin persistence surcharge; standing-rent form
     barred by T_ledger_rent_excluded [P], transition-booked form barred
     by T_realignment_cost_is_transition_energy [P] (C(transition) =
     n*eps = Delta-E exactly), per-activation form relocates the
     premise).  Unique-door scope: within fixed per-direction world-data
     costs and the consumed codef billing convention (item 2),
     configuration-dependent supports are the only unbarred entry to
     frustration (DANGLES_NOTE Section 4 necessity dichotomy + W10); a
     configuration-dependent cost map or re-conventioned escape billing
     is a distinct, unbanked, unadjudicated door (Section 7.2) -- same
     epistemic class as P-dangling, named here, not absorbed.  This is
     the open blade -- see the kill condition below.
  2. The codef support-billing convention (CONSUMED, BANKED):
     bill(S) = cost(anchor union) + cost(escaped threat directions),
     escape billed as cost(W - M-union) at plain direction cost, shared
     directions paid once -- exactly codef_aggregation.bill_joint and the
     T_sep pay-once axis.  Load-bearing: witness clause (5) computes the
     no-sharing collapse.  The bill's disjoint decomposition is checked
     as INTERNAL CONSISTENCY of the consumed convention, not derived.
  3. A1 endpoint gating on both flip directions (LICENSED): the A1
     endpoint condition applied to non-monotone bills; not load-bearing
     for the keystone direction (clause (3) gate-independence).

KILL CONDITION (LOUD -- a live blade, documented, one adjudication away).
The one unadjudicated gap is whether graded-FD5's commensurable "degree
of threat" (the well-typing fence of L_graded_threat_collapses_to_crisp)
may be identified with DEFENCE DEMAND.  Under that identification this
witness's implied demand-grade is sub-dominant -- defending p_(i,j) on
{d_i} demands h_(i,j) > 0 = its demand on X -- exactly the barred third
branch; the graded lemma's own forcing prose ("any perturbation endangers
the joint at least as much as it endangers either member") sits one
adjudication away from that reading.  IF DEMAND-COMMENSURABLE GRADING IS
EVER ADJUDICATED AS DEFENCE DEMAND, THIS CHECK DIES.

MAY-NOT-CITE (the fences; citation without the premise stack is
misciting):
  - NO serial-impossibility claim beyond single-flip worlds.  P-arity
    (arbitrary move arities) belongs to the UNBANKED composed theorem
    (lane record); do not import it from here.
  - NO hold, quantum, or selection claim of any kind -- this lemma is
    pure cost/reachability structure; it consumes no branch content and
    asserts none.
  - NO N >= 2 choice-family claim; no A2 content.
  - NOTHING concluding occupancy.
  - NO magnitude claims: the barrier is structural on the stated exact
    window; the rationals are witnesses, not thresholds.
  - No citation without the premise stack above.

GRADE [P_structural | P-dangling (open, named, adjudicated) + codef
support-billing convention (consumed-banked) + A1 endpoint gating;
frustration witness class].  Tier 4.  The composed slack-run-minimizer
theorem stays a LANE RECORD (not banked); this module banks the lemma
only.

Lane records: The Turning (parked)/slack_run_minimizer_2026-07-09/
(walk_frustrated_witness.py [25391 checks, exit 0], WITNESS_NOTE_v0.2.md,
AUDIT_keystone_stage1.md LAND-WITH-FIXES 0.82, AUDIT_stage2_final.md,
DANGLES_NOTE_v0.2.md + AUDIT_dangles_adjudication.md).
"""

from fractions import Fraction as F
from itertools import combinations
from collections import deque
import random

_DIST = ('d1', 'd2', 'd3')
_ANCHOR = {'d1': F(1), 'd2': F(3, 2), 'd3': F(5, 4)}
_DANGLE = {('d1', 'd2'): F(7, 2), ('d2', 'd1'): F(4),
           ('d1', 'd3'): F(9, 2), ('d3', 'd1'): F(5),
           ('d2', 'd3'): F(11, 2), ('d3', 'd2'): F(6)}


def _subsets():
    out = []
    for r in range(len(_DIST) + 1):
        out.extend(frozenset(c) for c in combinations(_DIST, r))
    return out


_ALL_S = _subsets()
_X = frozenset(_DIST)
_PROPER = [S for S in _ALL_S if S and S != _X]
_EMPTY = frozenset()


class _World:
    """The frustrated world: sector-clean P-dangling support assignment
    over the fixed combinatorial structure, parametric in the cost map."""

    def __init__(self, anchor_cost, dangling_cost):
        self.cost = {('a', d): anchor_cost[d] for d in _DIST}
        self.cost.update({('h', i, j): c for (i, j), c in dangling_cost.items()})

    def M(self, S):
        return frozenset(('a', d) for d in S)

    def T(self, S):
        # MONOTONE membership (FD5 containment respected).
        return frozenset(('p', i, j) for i in S for j in _DIST if j != i)

    def W(self, p, S):
        # P-dangling, sector-clean: partner present -> own anchor only
        # (contained, no cross-sector defence); partner absent -> the
        # missing bond end is passivated at h_(i,j), which escapes.
        _, i, j = p
        if j in S:
            return frozenset({('a', i)})
        return frozenset({('a', i), ('h', i, j)})

    def escaped(self, S):
        out = set()
        for p in self.T(S):
            out |= self.W(p, S)
        return frozenset(out) - self.M(S)      # codef union semantics

    def c(self, dirs):
        return sum((self.cost[x] for x in dirs), F(0))

    def bill(self, S):
        # consumed codef convention: anchor union + escaped at plain cost
        return self.c(self.M(S)) + self.c(self.escaped(S))


def _component(w, C, start, gate_removals):
    """BFS over single-flip moves.  gate_removals=True is the A1 endpoint
    gate on both directions; False is the unadapted gapless_serial_floor
    moves() convention (additions gated, removals ungated)."""
    if gate_removals and w.bill(start) > C:
        return frozenset()
    seen = {start}
    q = deque([start])
    while q:
        u = q.popleft()
        for d in _DIST:
            if d in u:
                v = u - {d}
                if (not gate_removals or w.bill(v) <= C) and v not in seen:
                    seen.add(v)
                    q.append(v)
            else:
                v = u | {d}
                if w.bill(v) <= C and v not in seen:
                    seen.add(v)
                    q.append(v)
    return frozenset(seen)


def _violations(w, C):
    """The frustration battery as a violation list (empty = frustrated at
    C).  Used positively on the witness and negatively as the in-check
    non-vacuity control."""
    v = []
    if w.escaped(_X) != frozenset():
        v.append("X not fully-contained")
    if w.bill(_X) != w.c(w.M(_X)):
        v.append("bill(X) != anchor cost")
    if not (w.bill(_X) <= C):
        v.append("X inadmissible")
    if not (w.bill(_EMPTY) == 0 <= C):
        v.append("empty not admissible at zero bill")
    for S in _PROPER:
        if not (w.bill(S) > C):
            v.append(f"proper subset {sorted(S)} admissible")
        if not (w.c(w.M(S)) <= w.c(w.M(_X)) <= C):
            v.append(f"anchor cost of {sorted(S)} breaks admissibility")
        if not (w.c(w.escaped(S)) > 0):
            v.append(f"{sorted(S)} carries no dangling escape")
    comp0 = _component(w, C, _EMPTY, gate_removals=True)
    adm = frozenset(S for S in _ALL_S if w.bill(S) <= C)
    if comp0 != frozenset({_EMPTY}):
        v.append("empty's admissible component != {empty}")
    if _component(w, C, _X, gate_removals=True) != frozenset({_X}):
        v.append("X not isolated")
    if adm != frozenset({_EMPTY, _X}):
        v.append("admissible states != {empty, X}")
    return v


def check_L_frustrated_witness():
    """L_frustrated_witness: the frustrated choice family exists (exact,
    conditional on the adjudicated premise stack).  See the module
    docstring for the statement, premise stack (item 1 verbatim from
    WITNESS_NOTE_v0.2.md Section 0), kill condition, and MAY-NOT-CITE
    fences.  This is the distilled battery; the 25391-check walker is the
    lane record."""
    from apf.core import check_T_sep
    from apf.codef_aggregation import check_L_codef_aggregation_argmin
    from apf.gapless_serial_floor import check_T_gapless_serial_floor

    fails = []
    n_checks = [0]

    def ck(cond, msg):
        if not cond:
            fails.append(msg)
        n_checks[0] += 1

    # ---- live bank anchors, consumed where the witness consumes them ----
    r_sep = check_T_sep()
    ck(r_sep.get('passed') is True and r_sep.get('epistemic') == 'P',
       "anchor T_sep [P] passes (the pay-once subadditive axis the billing "
       "convention rides)")
    r_codef = check_L_codef_aggregation_argmin()
    ck(r_codef.get('passed') is True and r_codef.get('epistemic') == 'P',
       "anchor L_codef_aggregation_argmin [P] passes")
    ck('support-billing' in r_codef.get('summary', ''),
       "codef CONTENT PIN: the support-billing convention this lemma "
       "consumes is the check's own returned summary content")
    r_floor = check_T_gapless_serial_floor()
    ck(r_floor.get('passed') is True and
       r_floor.get('epistemic') == 'P_structural',
       "anchor T_gapless_serial_floor [P_structural] passes (source of the "
       "single-flip endpoint-gated move alphabet)")

    w = _World(_ANCHOR, _DANGLE)

    # ---- (1) world well-formedness + exact bills, exhaustive ------------
    ck(len(w.cost) == 9 and all(isinstance(c, F) and c > 0
                                for c in w.cost.values()),
       "9-direction universe, every per-direction cost a positive exact "
       "Fraction (SP/K2)")
    ck(len(_PROPER) == 6, "all 6 proper nonempty subsets enumerated (|X|=3)")
    for Sa in _ALL_S:
        for Sb in _ALL_S:
            if Sa <= Sb:
                ck(w.T(Sa) <= w.T(Sb),
                   "threat MEMBERSHIP monotone (FD5 containment respected; "
                   "the barred proper-subset branch is not used)")
    for S in _ALL_S:
        for p in w.T(S):
            _, i, j = p
            if j in S:
                ck(w.W(p, S) == frozenset({('a', i)}) <= w.M(S),
                   "partner-present support = {a_i}: contained AND "
                   "sector-clean (no cross-sector defence; Lemma-2 Step-2 "
                   "clause not bet against)")
        # internal consistency of the consumed billing convention (not a
        # derivation): anchor union and escaped set are disjoint, so the
        # bill decomposes as the cost of one union set.
        ck(w.M(S) & w.escaped(S) == frozenset() and
           w.bill(S) == w.c(w.M(S) | w.escaped(S)),
           "bill = cost(M | escaped): disjoint decomposition, internal "
           "consistency of the consumed codef convention")
    expected = {_X: F(15, 4),
                frozenset({'d1'}): F(9), frozenset({'d2'}): F(11),
                frozenset({'d3'}): F(49, 4),
                frozenset({'d1', 'd2'}): F(25, 2),
                frozenset({'d1', 'd3'}): F(47, 4),
                frozenset({'d2', 'd3'}): F(47, 4)}
    for S, b in expected.items():
        ck(w.bill(S) == b, f"exact bill {sorted(S)} = {b}")
    ck(w.escaped(_X) == frozenset() and w.bill(_X) == w.c(w.M(_X)),
       "whole fully-contained: zero escaped threat directions, "
       "bill(X) = anchor cost = 15/4")
    for S in _PROPER:
        ck(w.bill(S) >= F(9) > w.bill(_X),
           f"every proper partial bills >= 9 > 15/4 ({sorted(S)})")
        ck(w.c(w.M(S)) <= w.c(w.M(_X)),
           f"LOAD-BEARING: anchor cost of {sorted(S)} alone never exceeds "
           "the whole's (excess never from anchor-support cost)")
        ck(w.bill(S) - w.c(w.M(S)) == w.c(w.escaped(S)) > 0,
           f"excess of {sorted(S)} is the dangling escape (positive; "
           "decomposition by billing construction)")

    # ---- (2) the C-window: ends, interior, sup-tightness ----------------
    LO, HI = w.bill(_X), min(w.bill(S) for S in _PROPER)
    ck(LO == F(15, 4) and HI == F(9) and LO < HI,
       "C-window [15/4, 9) exact and NONEMPTY")
    for C in (LO, (LO + HI) / 2, HI - (HI - LO) / 10**6):
        ck(LO <= C < HI and _violations(w, C) == [],
           f"full frustration battery holds at C = {C} (window end/interior)")
    ck(any(w.bill(S) <= HI for S in _PROPER),
       "sup-tightness: at C = 9 a proper subset is admissible -- the "
       "window statement is exact, not padded")

    # ---- (3) disconnection + gate-independence --------------------------
    Cmid = (LO + HI) / 2
    ck(_component(w, Cmid, _EMPTY, gate_removals=True) == frozenset({_EMPTY}),
       "A1-gated single-flip BFS: empty's component is exactly {empty}")
    ck(_component(w, Cmid, _X, gate_removals=True) == frozenset({_X}),
       "A1-gated: X is isolated -- admissible graph = {empty, X}, two "
       "components")
    c411 = _component(w, Cmid, _EMPTY, gate_removals=False)
    ck(c411 == frozenset({_EMPTY}),
       "GATE-INDEPENDENCE: under the UNADAPTED .411 moves() convention "
       "(removals ungated) BFS from empty still reaches only {empty}")
    cX411 = _component(w, Cmid, _X, gate_removals=False)
    ck(cX411 == frozenset(_ALL_S) and
       all(w.bill(S) > Cmid for S in cX411 if S not in (_EMPTY, _X)),
       "the removal gate is A1's endpoint condition: under the unadapted "
       "gate X descends to empty ONLY through states billing above C "
       "(occupancy A1 forbids); the gate is load-bearing only for "
       "X-isolation")

    # ---- (4) control legs: configuration-independence cannot frustrate --
    def bill_fixed(costmap, live, Wp, S):
        # fixed supports Wp[k]; live(k, S) a MONOTONE membership predicate
        U = frozenset(('a', d) for d in S)
        for k in range(len(Wp)):
            if live(k, S):
                U |= Wp[k]
        return sum((costmap[x] for x in U), F(0)), U

    def control(costmap, live, Wp, tag):
        billed = {S: bill_fixed(costmap, live, Wp, S) for S in _ALL_S}
        for Sa in _ALL_S:
            for Sb in _ALL_S:
                if Sa <= Sb:
                    ck(billed[Sa][1] <= billed[Sb][1] and
                       billed[Sa][0] <= billed[Sb][0],
                       f"[{tag}] billed set + bill MONOTONE under inclusion "
                       "(fixed supports, monotone membership)")
        for S in _PROPER:
            ck(billed[S][0] <= billed[_X][0],
               f"[{tag}] bill(S) <= bill(X): barrier IMPOSSIBLE without "
               "configuration-dependent supports")

    dirs = sorted(w.cost)
    # (4a) per-distinction fixed supports on the witness cost map, threats
    # landing inside M(X) (the baseline): bill(X) = anchor cost exactly.
    WX = [frozenset({('a', d)}) for d in _DIST]
    lv_pd = lambda k, S: sorted(_DIST)[k] in S
    ck(bill_fixed(w.cost, lv_pd, WX, _X)[0] == w.c(w.M(_X)),
       "control (4a): inside-landing fixed threats => bill(X) = cost(M(X))")
    control(w.cost, lv_pd, WX, "4a")
    # (4b) seeded random fixed supports over the whole universe, including
    # the IJC-superadditive monotone joint-threat shape (live iff |S| >= 2).
    # Distilled: 5 draws here; the 80 + 200-draw sweep is the walker's.
    rng = random.Random(20260709)
    for t in range(5):
        cm = {k: F(rng.randint(1, 720), rng.randint(1, 720)) for k in dirs}
        Wp = [frozenset(x for x in dirs if rng.random() < 0.4)
              for _ in range(4)]
        lv = lambda k, S: (sorted(_DIST)[k] in S) if k < 3 else (len(S) >= 2)
        for Sa in _ALL_S:
            for Sb in _ALL_S:
                if Sa <= Sb:
                    ck(all(lv(k, Sa) <= lv(k, Sb) for k in range(4)),
                       f"[4b-{t}] membership monotone (incl. joint threat "
                       "live only at |S| >= 2)")
        control(cm, lv, Wp, f"4b-{t}")

    # ---- (5) convention boundary: no-sharing collapse --------------------
    def bill_noshare(S):
        return w.c(w.M(S)) + sum((w.c(w.W(p, S)) for p in w.T(S)), F(0))

    def bill_per_threat(S):
        return w.c(w.M(S)) + sum((w.c(w.W(p, S) - w.M(S))
                                  for p in w.T(S)), F(0))

    for S in _ALL_S:
        ck(bill_per_threat(S) == w.bill(S),
           "per-threat multiplicity billing == union billing (escaped sets "
           "threat-disjoint; billed-once not load-bearing)")
    ck(bill_noshare(_X) == F(45, 4) and
       min(bill_noshare(S) for S in _PROPER) == F(11) and
       not (bill_noshare(_X) < F(11)),
       "NO-anchor-sharing billing COLLAPSES the barrier (45/4 >= 11): the "
       "consumed codef pay-once convention is load-bearing (stack item 2)")

    # ---- (6) negative control (non-vacuity travels with the check) ------
    w_cheap = _World(_ANCHOR, {k: F(1, 10) for k in _DANGLE})
    ck(not (w_cheap.bill(_X) < min(w_cheap.bill(S) for S in _PROPER)),
       "negative control: cheap passivation => window EMPTY")
    ck(_violations(w_cheap, w_cheap.bill(_X)) != [],
       "negative control: the frustration battery FAILS on a "
       "non-frustrated draw (the clauses can fail; not theater)")
    w_nodang = _World(_ANCHOR, _DANGLE)
    w_nodang.W = lambda p, S: frozenset(
        {('a', p[1]), ('h', p[1], p[2])})          # partner never helps
    ck(w_nodang.bill(_X) == F(129, 4) and
       _violations(w_nodang, F(15, 4)) != [],
       "negative control: P-dangling broken (configuration-independent "
       "support) => bill(X) = 129/4, battery FAILS -- the premise is "
       "load-bearing")

    # ---- (7) robustness: seeded rational re-draws, same structure -------
    rng2 = random.Random(4111)
    for t in range(5):
        ac = {d: F(rng2.randint(1, 99), 100) for d in _DIST}
        dc = {k: F(rng2.randint(200, 300), 100) for k in _DANGLE}
        w2 = _World(ac, dc)
        lo, hi = w2.bill(_X), min(w2.bill(S) for S in _PROPER)
        ck(lo < hi, f"re-draw {t}: window nonempty (structural, not tuned)")
        ck(_violations(w2, (lo + hi) / 2) == [],
           f"re-draw {t}: full battery holds at the window midpoint")

    passed = not fails
    return {
        'name': 'L_frustrated_witness',
        'epistemic': ('P_structural | P-dangling (open, named, adjudicated) '
                      '+ codef support-billing convention (consumed-banked) '
                      '+ A1 endpoint gating; frustration witness class'),
        'passed': passed,
        'tier': 4,
        'key_result': (
            'Under P-dangling (adjudicated named premise: configuration-'
            'dependent, contained, sector-clean defence supports) + the '
            'consumed codef support-billing convention + A1 endpoint gating, '
            'a frustrated choice family EXISTS exactly: |X| = 3 over 9 '
            'directions, bill(X) = 15/4 fully-contained, every proper '
            'nonempty subset bills >= 9 with the excess pure dangling '
            'escape, and on the whole window C in [15/4, 9) the admissible '
            'single-flip graph is exactly {empty, X} in two components '
            '(empty cannot reach X; gate-independent under the unadapted '
            '.411 gate). Configuration-independent supports with FD5-'
            'monotone membership can NEVER frustrate (billed-set '
            'monotonicity) -- configuration-dependence is the unique '
            'unbarred door; no-anchor-sharing billing collapses the barrier '
            '(45/4 >= 11), so the convention is load-bearing. Pure '
            'cost/reachability; DIES if graded-FD5 commensurable grade is '
            'adjudicated as defence demand.'
        ),
        'dependencies': ['A1', 'T_sep', 'L_codef_aggregation_argmin',
                         'T_gapless_serial_floor'],
        'cross_refs': ['T_IJC_dichotomy', 'L_threat_substrate_realization',
                       'L_graded_threat_collapses_to_crisp',
                       'T_ledger_rent_excluded',
                       'T_realignment_cost_is_transition_energy',
                       'L_mechanism_trichotomy',
                       'T_hold_cost_dominance_split'],
        'artifacts': {
            'witness': ('|X| = 3, 9 directions; bill(X) = 15/4; partials '
                        '9, 11, 49/4, 25/2, 47/4, 47/4; window [15/4, 9)'),
            'premise_stack': ('P-dangling (open, named, adjudicated '
                              'UPHOLD-WITH-EDITS) + codef convention '
                              '(consumed-banked, load-bearing: no-sharing '
                              'collapse 45/4 >= 11) + A1 endpoint gating '
                              '(licensed; keystone gate-independent)'),
            'kill_condition': ('LIVE BLADE: dies if graded-FD5 '
                               'commensurable "degree of threat" is '
                               'adjudicated as defence demand (the implied '
                               'demand-grade is then the barred '
                               'sub-dominant branch)'),
            'unique_door_scope': ('within fixed per-direction costs + the '
                                  'codef convention only; config-dependent '
                                  'cost maps / re-conventioned billing are '
                                  'distinct unadjudicated doors, named not '
                                  'absorbed'),
            'landscape_route': ('KILLED: standing-rent barred by '
                                'T_ledger_rent_excluded [P]; transition-'
                                'booked barred by T_realignment_cost_is_'
                                'transition_energy [P]; per-activation '
                                'relocates the premise'),
            'may_not_cite': ('no serial-impossibility beyond single-flip '
                             '(P-arity is the unbanked composition\'s); no '
                             'hold/quantum/selection; no N >= 2 '
                             'choice-family; no occupancy; no citation '
                             'without the premise stack'),
            'composed_theorem': 'LANE RECORD ONLY (not banked)',
            'walker': ('walk_frustrated_witness.py, 25391 checks, exit 0; '
                       'audit LAND-WITH-FIXES 0.82, all fixes carried'),
            'note_home': 'The Turning (parked)/slack_run_minimizer_2026-07-09/',
        },
        'fail_reasons': fails,
        'n_checks': n_checks[0],
    }


_CHECKS = {'L_frustrated_witness': check_L_frustrated_witness}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}


if __name__ == '__main__':
    import sys
    r = check_L_frustrated_witness()
    print(r['name'], 'PASS' if r['passed'] else 'FAIL',
          f"({r['n_checks']} checks)")
    if not r['passed']:
        for f in r['fail_reasons']:
            print('  -', f)
    sys.exit(0 if r['passed'] else 1)
