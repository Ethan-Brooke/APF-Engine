"""The hold cost-dominance split: the mechanism trichotomy and the two-clause
conditional theorem.

Lane: The Turning/quantum_selected_mechanism_2026-07-08/ (charter: Reference -
CONTINUATION - Quantum as the Selected Mechanism (2026-07-08), as MODIFIED by
the pricing audit's marginality determination and by the stage-1/stage-2
composed audits).  Three hostile audits of record: pricing REDUCE 0.85
(proceeds-with-fixes, all lemma-side fixes carried); stage-1 composed
LAND-WITH-FIXES 0.82 (mandatory fixes 1-3 + ride-alongs 4-5, all carried at
code level); stage-2 final LAND-WITH-FIXES 0.85 (pre-registration fixes F1-F3
carried: family-level quantifier; pricing-note scoping rider; K1-UT
disambiguation).  Long-form witnesses: walk_trichotomy_theorem.py (346 exact
checks) + walk_pricing_lemma.py (189 exact checks), both exit 0 against the
v24.3.412 tree; the check bodies below port the walker's legs (classifier +
battery constructors + guard + withheld-grant conditional + spectator pass +
genuine re-run + float tripwire + UNBINNED tripwire) as self-contained exact
Fraction arithmetic, consuming banked checks live at content level.

L_mechanism_trichotomy [P_structural].  At a genuine N >= 2 BW-distinct-cost
choice event sigma over an admissible configuration family W, every
admissible selection mechanism -- under the faithful-representation reading
(every mechanism's pre-commit conditioning is empty, fresh-formed, standing,
or held, WORLD-UNIFORMLY: one conditioning category per mechanism across the
family, the clause that absorbs world-heterogeneous consult/form rows, which
land UNBINNED; exhaustiveness rides this reading, [P_structural] cap, named)
-- lands, per event, AT THE WORLD-FAMILY LEVEL (exactness is a family-level
property; bookings are realized per world -- stage-2 fix F1), in exactly one
of:
  (i)   pays-fresh: exact per-event selection via structure FORMED by
        transitions in the event's own evaluation history ==> books >= eps
        marginal in that world (reduced pricing lemma B1, non-null clause);
  (i')  consults-standing: exact per-event selection via fused reads of
        standing / inherited / default-coded registers ==> ZERO marginal
        booking -- the reduced pricing lemma's honest boundary, an explicit
        bin, never collapsed into (i);
  (ii)  the hold: co-present coherent survey, zero booking until the single
        commit (FREE leg [P]); availability is what OCCUPANCY provides (the
        one occupancy entry); defined WITH its dual premise exemption
        (constitutive of the bin); populated as an EXACT competitor only
        under the named grant G-hold-exact.  DISCLOSURE: the hold's bin is
        TYPE-ASSIGNED via the reading's 'held' conditioning category, not
        cost-computed (untagged, its facts land UNBINNED -- computed), and
        no cost column separates the hold from R9's default world -- the
        separation is carried by typing + the .412 commutativity axis;
  (iii) does-not-exactly-select per-event: blind/fiat (exact ONLY on
        argmin-degenerate families -- named family assumption),
        approximate-A2 (the banked spectator form), eventual-argmin folds
        (exact per-history, never per-event).
The marginal column is genuinely two-valued {0} u [eps, oo) (computed: no
booking in (0, eps) exists in any ledger).  The UNBINNED branch is a live
tripwire with two owned firing modes (stage-2 F1): the untagged-hold
disclosure probe, and any world-heterogeneous conditioning row.

T_hold_cost_dominance_split [P_structural] WITH THE NAMED GRANT G-hold-exact
(re-headlined from T_A2_selects_the_hold per stage-1 M3: "A2 selects the
hold" simpliciter is computed FALSE by this module's own guard and is NOT
the claim).  Given the constitutive base {A1, MD, A2, BW, occupancy}, with
occupancy entering exactly once (hold-availability), and -- as a named model
input -- G-hold-exact:
  (1) CONDITIONAL STRICT LEG (on fresh).  Granted G-hold-exact, the hold is
      strictly cheaper than every bin-(i) fresh-formation mechanism --
      marginal 0 vs >= eps (MD), the common commit floor computed equal per
      world and cancelling -- by 0 < eps ONLY; A2 at mechanism granularity
      (named reading R-A2-mech) prefers the hold on the fresh bin.  Citation
      form: CONDITIONAL_ON_G_HOLD_EXACT, always.
  (2) INDIFFERENCE LEG (never dispreferred).  Among exact mechanisms the
      hold is never cost-dispreferred; vs every bin-(i') standing-consult
      mechanism the comparison is 0-vs-0 and A2 alone does NOT pick -- the
      tie is witnessed and GUARDED (strict-over-all-classical is computed
      FALSE, permanently).  B2 standing levels do not break the tie (levels,
      typed NOT bookings and NOT A2-comparable spend -- the banked cost-kind
      dichotomy consumed as typed).
  Riders: (c) bin-(iii) mechanisms are not competitors for exact per-event
  selection on argmin-SEPARATING families (named separation assumption;
  eventual-argmin concession named); on argmin-DEGENERATE families the
  fiat/blind rows are exact at zero marginal and JOIN the 0-vs-0
  indifference class (computed).  (d) The Sep spectator (no hold available)
  selects approximately (banked form) or pays fresh or consults standing --
  FULLY ADMISSIBLE; occupancy stays the QAC, no leg concludes it.
No citation may drop the indifference clause.

THE TWO SCOPED NAMED PREMISES (stage-1 fix 2; disambiguation = stage-2 F3):
  K1-UT, universal-transition form, SCOPED to COMMITTED REALIGNMENTS: every
    ledger transition (committed realignment of >= 1 distinction) books
    >= eps; null relabelings are not transitions.  The premise ranges over
    committed/classical structure ONLY.  The hold's pre-commit survey
    commits nothing (FREE leg [P] + the 2026-07-04 superadditivity ruling:
    coherent realignment commits no distinction) and is OUTSIDE K1-UT's
    range -- its zero booking is an exemption, not a violation.
    DISAMBIGUATION (stage-2 F3): K1-UT is NOT the bank's K1 (the dependency
    label of check_D_quotient_forced -- bank-kinematic content), and NOT
    .411's K1 (check_T_gapless_serial_floor's candidate-switch premise,
    scoped inside the all-Sep antecedent).  Three distinct labels; this
    module's premise is registered as K1-UT everywhere.
  Omega-conditioning, SCOPED to CLASSICAL/Sep MECHANISMS: every classical
    mechanism's admissible conditioning factors through the D-quotient (the
    Omega-visible state).  The hold conditions on coherent structure
    invisible to the classical ledger (.412 leg (ii)) and is OUTSIDE the
    premise's range.
  THE DUAL EXEMPTION is constitutive of bin (ii).  INTERNAL SPLIT (stage-2
    m2): exemption 1 (K1-UT/price: empty pre-commit history) is PRICE-shaped
    and grant-FREE (computed for both the granted and the withheld hold);
    exemption 2 (non-constant outcome map on identical empty classical
    state) is CAPABILITY-shaped and obtains UNDER the grant G-hold-exact.

G-HOLD-EXACT -- THE NAMED GRANT (status block):
  - GRANTED, NOT DERIVED: the banked triad certifies the hold's PRICE
    profile only; the bank's mechanized A2 is approximate-only (status
    fence consumed live: 'approximate form certified; A2 tie-selection + BW
    non-degeneracy remain named opens') -- the granted capability is
    precisely the named-open content;
  - RECORD-SIDE UNVERIFIABLE: .412's dephasing leg (ii) -- post-commit, no
    admissible observable in the commutative record algebra distinguishes a
    hold-fed commit from a fiat that happened to land argmin;
  - POSSIBLY PERMANENT: the benefit-leg discharge route is graveyarded
    (charter section 6); the theorem may never rise above conditional form
    on this axis;
  - COMPUTED CONDITIONAL STRUCTURE: with the grant withheld the hold's facts
    land in bin (iii) by the same classifier, its price profile unchanged
    (the grant is capability-shaped, not price-shaped).
  GRANT-DECLINING CONSUMERS read the theorem at [P_structural_reading];
  clause 2 survives grant-free as the price-table fact (the hold's marginal
  is 0 in every world by the [P] FREE leg, no mechanism books below 0, and
  every standing-consult exact mechanism ties it 0-vs-0).

THE R7 WIDTH DIAL -- RULED AS-IS (Ethan, 2026-07-09; ruling-of-record, this
corrigendum): the fused-computation convention (fused computation free --
the pricing audit's own construction) STANDS as the convention-of-record.
Grounds recorded with the ruling: (1) the pricing lemma's M2 counter-world
(the default-coded register at zero booking) is walked, audited arithmetic
-- reversing would overturn a counter-world, not reinterpret it (pricing-
not-forbidding discipline, the 2026-07-08 re-target ruling); (2) billing
locus: L_cost [P] attaches cost to committed realignment per transition,
uniquely -- a pure read realigns nothing; conditioning is not a transition;
(3) the strict claims the reversed setting would manufacture globally are
available structurally on frustrated sub-families (the slack-run-minimizer
lane, 2026-07-09) without touching the convention.  PRACTICAL CONTENT NOW
UNCONDITIONAL: a classical zero-marginal exact route exists at every choice
event (fresh formation never forced); the theorem's practical width is the
indifference clause plus conditional fresh-side dominance.  The reversed
branch (computation books; R7/R4/R9 migrate toward bin (i), strict leg
widens) is RETAINED as the recorded road-not-taken, no longer a pending
ruling.  All statements were verified STABLE under either ruling
(clause-by-clause, stage-2 surface 4), so this ruling lands as this
corrigendum alone -- no width rewalk owed.

FENCES (all mandatory): NO FORBIDDING (every classical exact mechanism ran
and was priced or zero-priced -- computed fence; nothing blocked or
unavailable); NO MAGNITUDE (only 0 < eps is imported; EPS = 3/7 deliberately
non-unit; the R2 hit rate 1/N is computed but consumed by nothing);
OCCUPANCY stays the QAC -- input, never conclusion, entering EXACTLY ONCE at
hold-AVAILABILITY (read-registry tripwired == ['hold_availability']);
DEGENERATE-FAMILY CONCESSION (bin (iii)'s exclusion is per-family, under the
named separation assumption); FLOOR EQUALITY IS DERIVED (stage-2 m4: the
common commit floor follows from M1 + shared outcome -- exactness => same
final structure => same floor -- not independently measured); Regime_R is a
CROSS_REF, not a dependency (stage-2 m3: consumed naming-only on the M4 leg,
per the .402 SCC edge-hygiene discipline).

MAY NOT CITE: "A2 selects the hold" simpliciter (computed FALSE -- the
guard); clause 1 without the grant; the split without the indifference
clause; strict preference over standing-consult mechanisms in any phrasing;
bin-(iii) exclusion without the family-separation assumption (degenerate
families join the indifference class -- computed); any per-world floor from
the pricing lemma; that the hold's existence-as-exact-competitor is banked
(it is the grant); anything concluding occupancy; any classical mechanism
forbidden, blocked, or unavailable; eps's magnitude anywhere.

COROLLARIES (folded into the theorem's key_result/artifacts; no separate
reading-grade check):
  Corollary 1 (the .412 bridge, [P_math]-on-banked, strictly conditional):
    if selection at sigma is realized via the hold -- a coherent pre-commit
    co-presence witnessed by some admissible observable -- the interface
    algebra is NON-COMMUTATIVE (contrapositive of
    check_L_commutative_no_unresolved_hold [P_math], deps == []).  Nothing
    forces selection to be hold-realized (consuming the bridge changes no
    bin -- computed); no forcing anywhere.
  Corollary 2 (the exact-A2 openness reframe, [P_structural_reading],
    fresh-side only, grant-conditional): the bank mechanizes only
    approximate A2; among FRESH realizations the zero-price exact option is
    the hold -- conditional on G-hold-exact; the standing side is the
    indifference clause's territory.

GRADES (2026-06-29 grade-by-tracked-dependencies ruling; stage-2 grade
ruling of record).  L_mechanism_trichotomy: [P_structural] -- the grade
string names the faithful-representation reading incl. the world-uniform
conditioning category, the two scoped premises K1-UT + Omega-conditioning,
and the bin-(ii) type-assignment disclosure.  T_hold_cost_dominance_split:
[P_structural] with the named grant G-hold-exact + the named reading
R-A2-mech -- the registered claim is the CONDITIONAL (the grant sits in the
antecedent, hoisted into the statement), resting on [P]/[P_math] anchors
throughout the gating arithmetic + two named scoped premises + two named
readings; the grade string itself carries the grant so no scraper reads a
bare [P_structural].

Lane records: The Turning/quantum_selected_mechanism_2026-07-08/
(NOTE_v0.2_trichotomy_and_theorem.md + NOTE_v0.2_pricing_lemma.md, both as
fixed per stage-2 F1/F2; HOSTILE_AUDIT_stage2_final.md = the banking shape
of record; WALK_RESULTS_LOG.md).
"""

from fractions import Fraction as F

# ---------------------------------------------------------------------------
# Assertable verdict flags (pinned; editing them is a visible act).
# ---------------------------------------------------------------------------
EPS = F(3, 7)                 # deliberately non-unit; only 0 < eps is imported
G_HOLD_EXACT = 'GRANTED'      # the named grant (stage-1 fix 1, hoisted)
STRICT_LEG_FORM = 'CONDITIONAL_ON_G_HOLD_EXACT'
HOLD_EXEMPTION_BUNDLE = ('K1_UT_committed_scope_exempt',
                         'Omega_conditioning_exempt')
M4_STATUS = 'NAMED_READING'   # R-A2-mech: named reading, never banked content
TRICHOTOMY_EXHAUSTIVENESS = 'FAITHFUL_REPRESENTATION_READING_WORLD_UNIFORM'
R7_WIDTH_DIAL = 'RULED_AS_IS_FUSED_READS_FREE_2026_07_09'  # was NEEDS_ETHAN_...; ruled by Ethan 2026-07-09


def _cost(S):
    """M1: cost supervenes on structure alone -- n(S) * eps, nothing else."""
    return F(len(S)) * EPS


class _Ledger:
    """Per-region ledger.  throughput = monotone sum of transition bookings
    (K1-UT: every committed realignment of >= 1 distinction books n*eps;
    null relabelings are not transitions); level = standing capacity
    commitment (B2 type: a LEVEL, never a booking, never A2-comparable
    spend -- the banked cost-kind dichotomy consumed as typed)."""

    def __init__(self, region):
        self.region = region
        self.support = frozenset()
        self.throughput = F(0)
        self.history = []

    def level(self):
        return _cost(self.support)

    def transition(self, new_support):
        new_support = frozenset(new_support)
        n = len(self.support ^ new_support)
        if n == 0:
            raise ValueError(
                "K1-UT named premise (universal-transition form, SCOPED to "
                "committed realignments): null relabeling is not a transition")
        booking = F(n) * EPS
        self.throughput += booking
        self.history.append((n, booking))
        self.support = new_support
        return booking


def _world(tag, sizes):
    return {p: frozenset({(tag, p, k) for k in range(sz)})
            for p, sz in enumerate(sizes)}


V_SEP = [_world('s0', (2, 3)),   # argmin position 0
         _world('s1', (3, 2))]   # argmin position 1 (family SEPARATES argmin)
V_DEG = [_world('g0', (2, 3)),   # argmin position 0
         _world('g1', (2, 5))]   # argmin position 0 (degenerate; worlds distinct)


def _argmin_pos(w):
    costs = {p: _cost(s) for p, s in w.items()}
    return min(costs, key=lambda p: costs[p])


def _row_facts(name, per_world, is_hold=False):
    """Family-aggregated mechanism facts (stage-2 F1: exactness and the cost
    tests are FAMILY-LEVEL properties; bookings are realized per world)."""
    outcomes_exact = all(pw['outcome'] == _argmin_pos(w)
                         for pw, w in zip(per_world, V_SEP))
    no_viol = all(pw['viol'] == 0 for pw in per_world)
    return {
        'row': name,
        'per_world': per_world,
        'is_hold': is_hold,
        'exact_per_event': outcomes_exact and no_viol,
        'eventual_exact': outcomes_exact,
        'marginal_min': min(pw['marginal'] for pw in per_world),
        'marginal_max': max(pw['marginal'] for pw in per_world),
        'consults_standing': any(pw['consults_standing'] for pw in per_world),
    }


def _assign_bin(facts, hold_available):
    """The classifier -- one computed predicate, applied uniformly; operates
    on family-aggregated facts (F1).  The 'ii' branch fires on the is_hold
    TAG (the reading's 'held' conditioning category): bin (ii) is
    TYPE-ASSIGNED, not cost-computed (disclosed; computed below).  The
    UNBINNED branch is a live tripwire with two owned firing modes."""
    if facts['is_hold'] and not hold_available:
        return 'UNAVAILABLE'          # bin (ii) unpopulated without occupancy
    if not facts['exact_per_event']:
        return 'iii'
    if facts['is_hold']:
        return 'ii'
    if facts['marginal_min'] >= EPS:
        return 'i'
    if facts['marginal_max'] == 0 and facts['consults_standing']:
        return "i'"
    return 'UNBINNED'


_EXPECTED_BINS = {
    'R1_inslot_fold': 'iii',
    'R2_blind': 'iii',
    'R3_scratch_survey': 'i',
    'R4_inherited_ordering': "i'",
    'R5_population_parallel': 'i',
    'R6a_amortized_event1': 'i',
    'R6b_amortized_event2plus': "i'",
    'R7_antecedent_bookkeeping': "i'",
    'R8_fiat_commit': 'iii',
    'R9_default_coded_register': "i'",
    'RH_the_hold': 'ii',
}


def _run_model(ck):
    """Build the full battery + hold in a fresh model context and run every
    model-level assertion (ported from walk_trichotomy_theorem.py, the
    346-check long-form witness).  Exact Fraction arithmetic throughout;
    occupancy read-registry local to the run; float tripwire at the end.
    Returns the computed objects both checks consume."""
    ledgers = []
    occupancy_reads = []

    def mk(region):
        L = _Ledger(region)
        ledgers.append(L)
        return L

    def occupancy_available(source):
        # named constitutive input [P] (v24.3.304 ruling), never derived here
        occupancy_reads.append(source)
        return True

    # ---- MD floor + M1 tripwires --------------------------------------
    ck(EPS > 0, "MD: eps > 0 (the ONLY inequality the theorem imports)")
    for S in (frozenset(), frozenset({'a'}), frozenset({'a', 'b'})):
        ck(_cost(S) == F(len(S)) * EPS, "M1: cost recomputes from structure alone")
    ck(_cost.__code__.co_argcount == 1, "M1: cost takes the structure and nothing else")

    # ---- world families ------------------------------------------------
    for fam, name, expect in ((V_SEP, 'V_SEP', [0, 1]), (V_DEG, 'V_DEG', [0, 0])):
        for j, w in enumerate(fam):
            costs = [_cost(w[p]) for p in sorted(w)]
            ck(len(set(costs)) == len(costs), "%s w%d: BW-distinct costs" % (name, j))
            ck(len(w) == 2, "%s w%d: genuine N = 2 choice" % (name, j))
            ck(_argmin_pos(w) == expect[j],
               "%s w%d: argmin position %d" % (name, j, expect[j]))
    ck(len({_argmin_pos(w) for w in V_SEP}) == 2,
       "V_SEP separates argmin positions (the bin-(iii) family assumption HOLDS)")
    ck(len({_argmin_pos(w) for w in V_DEG}) == 1,
       "V_DEG does NOT separate argmin positions (the degenerate-family arena)")

    # ---- battery constructors (rows 1-9 + the hold) ---------------------
    def build_r1(tag=''):
        # in-slot serial running-min fold: intermediate commits AT sigma
        pw = []
        for j, w in enumerate(V_SEP):
            sig = mk('r1_sigma%s_w%d' % (tag, j))
            realized = []
            best, best_cost = None, None
            for p in sorted(w):
                sig.transition(w[p])
                realized.append(p)
                if best_cost is None or _cost(w[p]) < best_cost:
                    best, best_cost = p, _cost(w[p])
            if sig.support != w[best]:
                sig.transition(w[best])
                realized.append(best)
            am = _argmin_pos(w)
            viol = sum(1 for p in realized if p != am)
            pw.append({'outcome': best, 'viol': viol, 'marginal': sig.throughput,
                       'standing_level': F(0), 'consults_standing': False,
                       'upstream_booking': F(0)})
            ck(viol >= 1, "R1 w%d: >= 1 per-event A2 violation" % j)
            ck(sig.throughput >= EPS, "R1 w%d: the fold is PRICED (>= eps)" % j)
        return _row_facts('R1_inslot_fold', pw)

    def build_r2(tag=''):
        # blind / randomized resolution: no-input => constant selector
        const_results = {}
        for k in (0, 1):
            hits = sum(1 for w in V_SEP if k == _argmin_pos(w))
            const_results[k] = hits
            ck(hits < len(V_SEP),
               "R2: constant selector %d fails somewhere on V_SEP" % k)
        hr = F(sum(const_results.values()), len(const_results) * len(V_SEP))
        ck(hr == F(1, 2), "R2: uniform-random hit rate exactly 1/N = 1/2 "
                          "(computed, consumed by nothing -- no-magnitude fence)")
        pw = [{'outcome': 0, 'viol': 0, 'marginal': F(0), 'standing_level': F(0),
               'consults_standing': False, 'upstream_booking': F(0)} for _ in V_SEP]
        ck(pw[1]['outcome'] != _argmin_pos(V_SEP[1]),
           "R2: representative constant-0 selector WRONG in w1 (computed)")
        facts = _row_facts('R2_blind', pw)
        facts['hit_rate'] = hr
        return facts

    def build_r3(tag=''):
        # costed scratch/simulation survey: fresh formation, priced (B1)
        pw = []
        for j, w in enumerate(V_SEP):
            scratch = mk('r3_scratch%s_w%d' % (tag, j))
            observed = {}
            for p in sorted(w):
                b_in = scratch.transition(w[p])
                ck(b_in == _cost(w[p]), "R3 w%d: copy books intrinsic cost" % j)
                observed[p] = _cost(scratch.support)
                scratch.transition(frozenset())
            outcome = min(observed, key=lambda p: observed[p])
            pw.append({'outcome': outcome, 'viol': 0, 'marginal': scratch.throughput,
                       'standing_level': F(0), 'consults_standing': False,
                       'upstream_booking': F(0)})
            ck(scratch.throughput == 2 * sum(_cost(w[p]) for p in w),
               "R3 w%d: marginal = 2*sum n(c_i)*eps exactly" % j)
            ck(scratch.throughput >= EPS, "R3 w%d: marginal >= eps (B1)" % j)
        return _row_facts('R3_scratch_survey', pw)

    def build_r4(tag=''):
        # inherited/precomputed ordering: formed upstream, fused read free (D2)
        pw = []
        for j, w in enumerate(V_SEP):
            up = mk('r4_upstream%s_w%d' % (tag, j))
            b_up = up.transition({('R4', 'argmin_is_%d' % _argmin_pos(w))})
            ck(b_up >= EPS, "R4 w%d: upstream formation booked >= eps (B1)" % j)
            tp0 = up.throughput
            decoded = (_argmin_pos(w)
                       if ('R4', 'argmin_is_%d' % _argmin_pos(w)) in up.support
                       else None)
            ck(up.throughput == tp0, "R4 w%d: FUSED read books NOTHING (D2)" % j)
            pw.append({'outcome': decoded, 'viol': 0, 'marginal': F(0),
                       'standing_level': up.level(), 'consults_standing': True,
                       'upstream_booking': b_up})
            ck(up.level() >= EPS, "R4 w%d: standing register commits >= eps "
                                  "(B2 LEVEL, typed NOT a booking)" % j)
        facts = _row_facts('R4_inherited_ordering', pw)
        ck(all(p['upstream_booking'] >= EPS for p in pw),
           "R4: per-family clause trivially saturated")
        return facts

    def build_r5(tag=''):
        # population-parallel instantiation + registered communication
        pw = []
        for j, w in enumerate(V_SEP):
            regA = mk('r5_regA%s_w%d' % (tag, j))
            regB = mk('r5_regB%s_w%d' % (tag, j))
            home = mk('r5_home%s_w%d' % (tag, j))
            bA = regA.transition(w[0])
            bB = regB.transition(w[1])
            b_comm = home.transition({('r5', 'comm', j)})
            ck(bA == _cost(w[0]) and bB == _cost(w[1]),
               "R5 w%d: per-region bookings are intrinsic costs" % j)
            ck(b_comm >= EPS, "R5 w%d: registered communication books >= eps" % j)
            outcome = 0 if _cost(regA.support) < _cost(regB.support) else 1
            marg = regA.throughput + regB.throughput + home.throughput
            pw.append({'outcome': outcome, 'viol': 0, 'marginal': marg,
                       'standing_level': F(0), 'consults_standing': False,
                       'upstream_booking': F(0)})
            ck(marg >= EPS, "R5 w%d: total marginal >= eps" % j)
        return _row_facts('R5_population_parallel', pw)

    def build_r6(tag=''):
        # amortized: event 1 forms fresh (bin i); events 2..k fuse-consult (i')
        pw_e1, pw_e2 = [], []
        for j, w in enumerate(V_SEP):
            amort = mk('r6_amort%s_w%d' % (tag, j))
            b_form = amort.transition({('R6', 'ord_%d' % _argmin_pos(w))})
            ck(b_form >= EPS, "R6 w%d event1: fresh formation books >= eps" % j)
            pw_e1.append({'outcome': _argmin_pos(w), 'viol': 0, 'marginal': b_form,
                          'standing_level': F(0), 'consults_standing': False,
                          'upstream_booking': F(0)})
            tp1 = amort.throughput
            decoded = (_argmin_pos(w)
                       if ('R6', 'ord_%d' % _argmin_pos(w)) in amort.support
                       else None)
            ck(amort.throughput == tp1, "R6 w%d event2: fused consult free (D2)" % j)
            pw_e2.append({'outcome': decoded, 'viol': 0, 'marginal': F(0),
                          'standing_level': amort.level(), 'consults_standing': True,
                          'upstream_booking': b_form})
        return (_row_facts('R6a_amortized_event1', pw_e1),
                _row_facts('R6b_amortized_event2plus', pw_e2))

    def build_r7(tag=''):
        # fused bookkeeping on the world-borne antecedent (the R7 dial's row)
        pw = []
        for j, w in enumerate(V_SEP):
            antecedent_level = sum(_cost(w[p]) for p in w)
            outcome = _argmin_pos(w)
            pw.append({'outcome': outcome, 'viol': 0, 'marginal': F(0),
                       'standing_level': antecedent_level, 'consults_standing': True,
                       'upstream_booking': F(0)})
            ck(antecedent_level == sum(_cost(w[p]) for p in w),
               "R7 w%d: antecedent level is WORLD-BORNE (identical in the "
               "hold-run; charging it double-counts world structure)" % j)
        return _row_facts('R7_antecedent_bookkeeping', pw)

    def build_r8(tag=''):
        # representation-free fiat commit (outside the pricing antecedent)
        for k in (0, 1):
            hits = sum(1 for w in V_SEP if k == _argmin_pos(w))
            ck(hits < len(V_SEP),
               "R8: fiat (constant %d) fails somewhere on V_SEP (exhaustive)" % k)
        pw = [{'outcome': 0, 'viol': 0, 'marginal': F(0), 'standing_level': F(0),
               'consults_standing': False, 'upstream_booking': F(0)} for _ in V_SEP]
        return _row_facts('R8_fiat_commit', pw)

    def build_r9(tag=''):
        # the default-coded register (the pricing countermodel, Leg F-CM)
        def R9_state(j):
            return frozenset({('R9', 'argmin_is_1')}) if j == 1 else frozenset()
        ck(R9_state(0) != R9_state(1), "R9: faithful at the FAMILY level")
        up9 = {0: mk('r9_upstream%s_w0' % tag), 1: mk('r9_upstream%s_w1' % tag)}
        up9[1].transition(R9_state(1))
        ck(up9[0].throughput == 0 and up9[0].history == [] and up9[0].level() == 0,
           "R9 w0: ZERO booked, ZERO committed, EMPTY history (null default world)")
        ck(up9[1].throughput >= EPS, "R9 w1: upstream formation booked >= eps")
        pw = []
        for j, w in enumerate(V_SEP):
            decoded = 1 if ('R9', 'argmin_is_1') in R9_state(j) else 0
            pw.append({'outcome': decoded, 'viol': 0, 'marginal': F(0),
                       'standing_level': up9[j].level(), 'consults_standing': True,
                       'upstream_booking': up9[j].throughput})
        facts = _row_facts('R9_default_coded_register', pw)
        ck(pw[0]['standing_level'] == 0 and pw[0]['upstream_booking'] == 0,
           "R9 w0: zero-vs-zero on EVERY cost column in the default world")
        ck(any(p['upstream_booking'] >= EPS for p in pw),
           "R9: per-family clause holds (SOME world booked upstream) -- the "
           "strongest world-unconditional form, consumed exactly as reduced")
        return facts

    def build_hold(grant, tag=''):
        # bin-(ii) reference mechanism; exactness = the G-hold-exact GRANT
        pw = []
        for j, w in enumerate(V_SEP):
            hold_pre = mk('rh_precommit%s_%s_w%d' % (tag, grant.lower(), j))
            ck(hold_pre.throughput == 0,
               "RH(%s) w%d: pre-commit survey books ZERO" % (grant, j))
            ck(hold_pre.level() == 0,
               "RH(%s) w%d: pre-commit survey commits ZERO level" % (grant, j))
            ck(hold_pre.history == [],
               "RH(%s) w%d: K1-UT EXEMPTION computed -- no committed "
               "realignment exists pre-commit (FREE leg + superadditivity "
               "ruling); exemption 1 is PRICE-shaped and GRANT-FREE" % (grant, j))
            if grant == 'GRANTED':
                outcome = _argmin_pos(w)   # THE GRANT: exact per-event selection
            else:
                outcome = 0                # withheld: approximate/spectator shape
            pw.append({'outcome': outcome, 'viol': 0, 'marginal': F(0),
                       'standing_level': F(0), 'consults_standing': False,
                       'upstream_booking': F(0)})
        name = 'RH_the_hold' if grant == 'GRANTED' else 'RH_hold_grant_withheld'
        return _row_facts(name, pw, is_hold=True)

    # ---- main pass ------------------------------------------------------
    R1 = build_r1()
    ck(R1['eventual_exact'], "R1: eventual-argmin -- exact PER-HISTORY only")
    ck(not R1['exact_per_event'], "R1: NOT exact per-event")
    R2 = build_r2()
    hit_rate = R2.pop('hit_rate')
    ck(not R2['exact_per_event'], "R2: blind NOT exact on the separating family")
    R3 = build_r3()
    ck(R3['exact_per_event'], "R3: scratch survey IS exact per-event")
    R4 = build_r4()
    ck(R4['exact_per_event'], "R4: inherited ordering IS exact per-event")
    R5 = build_r5()
    ck(R5['exact_per_event'], "R5: population-parallel IS exact per-event")
    R6a, R6b = build_r6()
    ck(R6a['exact_per_event'] and R6b['exact_per_event'],
       "R6: amortized route exact per-event at both phases")
    R7 = build_r7()
    ck(R7['exact_per_event'], "R7: fused antecedent bookkeeping IS exact")
    ck(R7['marginal_max'] == 0, "R7: zero marginal (fused reads free, D2)")
    R8 = build_r8()
    ck(not R8['exact_per_event'], "R8: fiat NOT exact on the separating family")
    fiat_deg_hits = sum(1 for w in V_DEG if 0 == _argmin_pos(w))
    ck(fiat_deg_hits == len(V_DEG),
       "R8 FINDING (loud): the fiat commit IS exact on the argmin-degenerate "
       "family V_DEG at zero cost -- bin (iii) is per-family; on degenerate "
       "families the fiat joins the 0-vs-0 indifference class")
    R9 = build_r9()
    ck(R9['exact_per_event'], "R9: EXACT in BOTH worlds (incl. the default)")
    ck(R9['marginal_max'] == 0, "R9: zero marginal in BOTH worlds")

    hold_available = occupancy_available('hold_availability')
    ck(hold_available is True, "hold availability = occupancy as NAMED INPUT")
    ck(G_HOLD_EXACT == 'GRANTED',
       "G-HOLD-EXACT GRANT FLAG (assertable): granted, not derived; carried "
       "possibly permanently (benefit-leg graveyard; .412 record-side "
       "unverifiability)")
    RH = build_hold(G_HOLD_EXACT)
    ck(RH['exact_per_event'],
       "RH: single commit to the argmin UNDER the G-hold-exact grant (the "
       "grant is the source of this line, not a derivation)")
    ck(RH['marginal_min'] == RH['marginal_max'] == 0,
       "RH: zero marginal pre-commit booking")
    ck(HOLD_EXEMPTION_BUNDLE == ('K1_UT_committed_scope_exempt',
                                 'Omega_conditioning_exempt'),
       "EXEMPTION BUNDLE FLAG: dual exemption constitutive of bin (ii), "
       "bundled with occupancy (availability) + the grant")
    ck(all(pw['consults_standing'] is False and pw['standing_level'] == 0 and
           pw['upstream_booking'] == 0 for pw in RH['per_world']),
       "RH: consults NO Omega-ledger-visible input (no standing register, no "
       "upstream formation, empty pre-commit ledger in BOTH worlds)")
    ck(len({pw['outcome'] for pw in RH['per_world']}) == 2,
       "RH: Omega-CONDITIONING EXEMPTION computed -- outcome map NON-constant "
       "across V_SEP despite identical (empty) classical pre-commit state "
       "(exemption 2 is CAPABILITY-shaped and obtains UNDER the grant)")

    battery = [R1, R2, R3, R4, R5, R6a, R6b, R7, R8, R9, RH]

    # ---- trichotomy bins ------------------------------------------------
    bins = {}
    for facts in battery:
        b = _assign_bin(facts, hold_available=hold_available)
        bins[facts['row']] = b
        ck(b != 'UNBINNED', "classifier tripwire: %s must land in a bin" % facts['row'])
        ck(b == _EXPECTED_BINS[facts['row']],
           "computed bin of %s is %s (expected %s)"
           % (facts['row'], b, _EXPECTED_BINS[facts['row']]))
    ck(len(bins) == len(battery), "every battery row binned exactly once")
    ck(set(bins.values()) == {'i', "i'", 'ii', 'iii'}, "all four bins populated")
    for L in ledgers:
        for (_n, b) in L.history:
            ck(b >= EPS, "no booking in (0, eps): K1-UT + L_cost close the "
                         "(i)/(i') classifier gap (ledger %s)" % L.region)

    # ---- bin-(ii) tag disclosure (computed, loud) ------------------------
    _untagged = dict(RH)
    _untagged['is_hold'] = False
    ck(_assign_bin(_untagged, hold_available=hold_available) == 'UNBINNED',
       "DISCLOSURE (computed): bin (ii) is TYPE-ASSIGNED -- untagged, the "
       "hold's own facts land UNBINNED (firing mode 1 of the tripwire)")
    for col in ('marginal', 'standing_level', 'upstream_booking'):
        ck(RH['per_world'][0][col] == R9['per_world'][0][col] == 0,
           "DISCLOSURE (computed): no cost column separates the hold from "
           "R9's default world (%s: 0 vs 0) -- separation carried by typing "
           "+ the .412 commutativity axis, never by cost" % col)

    # ---- common commit floor (derived from M1 + shared outcome; m4) ------
    exact_rows = [f for f in battery if f['exact_per_event']]
    commit_bookings = {}
    for facts in exact_rows:
        for j, w in enumerate(V_SEP):
            cl = mk('%s_commit_w%d' % (facts['row'], j))
            b_commit = cl.transition(w[_argmin_pos(w)])
            commit_bookings.setdefault(j, []).append(b_commit)
            ck(b_commit >= EPS, "commit floor >= eps (%s, w%d)" % (facts['row'], j))
    for j, lst in commit_bookings.items():
        ck(len(set(lst)) == 1,
           "w%d: commit floor IDENTICAL across all exact mechanisms (cancels; "
           "DERIVED from M1 + shared outcome, not independently measured)" % j)

    # ---- the computed conditional structure (grant withheld) -------------
    RH_WITHHELD = build_hold('WITHHELD', tag='_cf')
    ck(not RH_WITHHELD['exact_per_event'],
       "CONDITIONAL STRUCTURE computed: grant withheld => exact_per_event FAILS")
    ck(_assign_bin(RH_WITHHELD, hold_available=hold_available) == 'iii',
       "CONDITIONAL STRUCTURE computed: the withheld-grant hold lands in bin "
       "(iii) by the same classifier -- bin (ii)'s population as an EXACT "
       "competitor is GRANT-DEPENDENT")
    ck(RH_WITHHELD['marginal_min'] == RH_WITHHELD['marginal_max'] == 0,
       "the grant is CAPABILITY-shaped, not price-shaped: the withheld hold's "
       "price profile is unchanged (the banked triad certifies price only)")

    # ---- spectator pass (Sep world, no hold available) --------------------
    bins_sep = {}
    for facts in battery:
        bins_sep[facts['row']] = _assign_bin(facts, hold_available=False)
    ck(bins_sep['RH_the_hold'] == 'UNAVAILABLE',
       "spectator: bin (ii) UNPOPULATED without occupancy")
    for facts in battery:
        if facts['row'] != 'RH_the_hold':
            ck(bins_sep[facts['row']] == bins[facts['row']],
               "spectator: %s bin UNCHANGED without occupancy" % facts['row'])
    ck(any(bins_sep[r] == 'i' for r in bins_sep) and
       any(bins_sep[r] == "i'" for r in bins_sep),
       "spectator: exact selection remains AVAILABLE classically (>= eps "
       "fresh or standing registers) -- PERMITTED and PRICED, nothing forbidden")
    ck(any(bins_sep[r] == 'iii' for r in bins_sep),
       "spectator: approximate/blind routes remain -- fully admissible")

    # ---- genuine constructor re-run (fresh ledgers, recomputed facts) -----
    classical_rows = [f for f in battery if not f['is_hold']]
    rebuilt = [build_r1(tag='_z'), None, build_r3(tag='_z'), build_r4(tag='_z'),
               build_r5(tag='_z')]
    _r2z = build_r2(tag='_z')
    _r2z.pop('hit_rate')
    rebuilt[1] = _r2z
    _r6az, _r6bz = build_r6(tag='_z')
    rebuilt += [_r6az, _r6bz, build_r7(tag='_z'), build_r8(tag='_z'),
                build_r9(tag='_z')]
    ck(len(rebuilt) == len(classical_rows),
       "re-run: all nine classical constructors re-executed (R6 gives two rows)")
    for old, new in zip(classical_rows, rebuilt):
        ck(old['row'] == new['row'], "re-run: row identity %s" % old['row'])
        ck(old['per_world'] == new['per_world'],
           "re-run: %s per-world facts RECOMPUTED identical (exact Fraction "
           "equality, all columns, both worlds)" % old['row'])
        ck(_assign_bin(new, hold_available=False) == bins_sep[old['row']],
           "re-run: %s re-classified under hold-withdrawn matches" % old['row'])
    ck(occupancy_reads == ['hold_availability'],
       "OCCUPANCY TRIPWIRE: consumed exactly once, at hold-AVAILABILITY only; "
       "registry UNCHANGED by the constructor re-run (reads: %s)" % occupancy_reads)

    # ---- float tripwire ---------------------------------------------------
    def no_float(x, path="root"):
        if isinstance(x, float):
            ck(False, "FLOAT on load-bearing path: %s" % path)
        elif isinstance(x, dict):
            for k, v in x.items():
                no_float(v, path + "." + str(k))
        elif isinstance(x, (list, tuple, set, frozenset)):
            for i, v in enumerate(x):
                no_float(v, path + "[%d]" % i)
    no_float({
        'EPS': EPS,
        'ledgers': {L.region: (L.throughput, L.level(), L.history) for L in ledgers},
        'battery': [{k: v for k, v in f.items() if k != 'row'} for f in battery],
        'rebuilt': [{k: v for k, v in f.items() if k != 'row'} for f in rebuilt],
        'withheld_hold': {k: v for k, v in RH_WITHHELD.items() if k != 'row'},
        'commit_bookings': commit_bookings,
        'hit_rate': hit_rate,
    })
    ck(isinstance(EPS, F), "eps is exact Fraction")

    # ---- no-forbidding fence (structural, computed) ------------------------
    ck(all(bins[f['row']] in ('i', "i'") for f in exact_rows if not f['is_hold']),
       "NO-FORBIDDING fence: every classical exact-selection mechanism is "
       "ADMITTED and priced (bin i) or zero-marginal-priced (bin i')")

    return {
        'battery': battery,
        'bins': bins,
        'bins_sep': bins_sep,
        'RH': RH,
        'RH_WITHHELD': RH_WITHHELD,
        'R9': R9,
        'exact_rows': exact_rows,
        'commit_bookings': commit_bookings,
        'fiat_deg_hits': fiat_deg_hits,
        'hit_rate': hit_rate,
        'occupancy_reads': occupancy_reads,
        'hold_available': hold_available,
    }


def check_L_mechanism_trichotomy():
    """The family-level four-bin trichotomy (see module docstring, statement 1).
    Tier 4, [P_structural]; grade string names the faithful-representation
    reading (incl. the world-uniform conditioning category, stage-2 F1), the
    two scoped premises K1-UT + Omega-conditioning, and the bin-(ii)
    type-assignment disclosure."""
    from apf.core import (check_L_cost, check_L_epsilon_star,
                          check_D_quotient_forced)
    from apf.class_transition import check_T_coherent_free_spend_permanent
    from apf.continuation_calculus import check_T_selection_approximate_A2

    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)

    # ---- live bank anchors, consumed at content level ---------------------
    r_cost = check_L_cost()
    ck(r_cost.get('passed') is True and r_cost.get('epistemic') == 'P',
       "anchor L_cost [P] passes")
    ck('C(E) = n(E)*epsilon is FORCED' in r_cost.get('key_result', ''),
       "L_cost CONTENT PIN: the intrinsic n(E)*eps form this model embeds is "
       "the check's own returned key_result")
    r_eps = check_L_epsilon_star()
    ck(r_eps.get('passed') is True and r_eps.get('epistemic') == 'P',
       "anchor L_epsilon_star [P] passes")
    ck('MD' in r_eps.get('dependencies', []),
       "the eps > 0 floor is MD's content (the only imported inequality)")
    r_dq = check_D_quotient_forced()
    ck(r_dq.get('passed') is True and r_dq.get('epistemic') == 'P',
       "anchor D_quotient_forced [P] passes (row-8 constancy's KINEMATIC "
       "half; the operational half stays the scoped Omega-conditioning "
       "named premise)")
    ck(sorted(r_dq.get('dependencies', [])) == ['A1', 'K1'],
       "D-quotient rides A1 + the BANK's K1 -- which is NOT this module's "
       "K1-UT premise (stage-2 F3 disambiguation: bank-kinematic content vs "
       "the lane's universal-transition form scoped to committed realignments)")
    r_triad = check_T_coherent_free_spend_permanent()
    ck(r_triad.get('passed') is True and r_triad.get('epistemic') == 'P',
       "anchor T_coherent_free_spend_permanent [P] passes")
    ck('occupancy' in r_triad.get('dependencies', []),
       "the triad carries occupancy -- exactly where bin (ii) names its one "
       "occupancy input (hold-AVAILABILITY)")
    ck('FREE = ledger_rent_excluded' in r_triad.get('key_result', ''),
       "FREE leg present (coherent hold books zero until commit)")
    r_a2 = check_T_selection_approximate_A2()
    ck(r_a2.get('passed') is True and r_a2.get('epistemic') == 'P_structural',
       "anchor T_selection_approximate_A2 [P_structural] passes (bin (iii)'s "
       "banked spectator form)")
    ck(r_a2.get('artifacts', {}).get('status_fence') ==
       'approximate form certified; A2 tie-selection + BW non-degeneracy '
       'remain named opens',
       "the bank mechanizes only APPROXIMATE A2 (exact field pin)")

    # ---- the model: battery, classifier, disclosure, spectator, re-run ----
    M = _run_model(ck)

    # ---- F1: the family-level quantifier's two owned firing modes ---------
    # Probe 1 (R8-in-w0): the fiat's w0 facts are per-world exact at zero
    # cost, consulting nothing -- a per-world classifier would leave them
    # unbinned; the FAMILY classifier lands R8 in (iii).  This is WHY the
    # registered quantifier is family-level: accidental per-world exactness
    # of a constant selector is not selection.
    r8 = next(f for f in M['battery'] if f['row'] == 'R8_fiat_commit')
    ck(r8['per_world'][0]['outcome'] == _argmin_pos(V_SEP[0]) and
       r8['per_world'][0]['viol'] == 0 and
       r8['per_world'][0]['marginal'] == 0,
       "F1 probe 1: R8-in-w0 is per-world exact at zero marginal, consulting "
       "nothing (the boundary owned as stated)")
    ck(M['bins']['R8_fiat_commit'] == 'iii',
       "F1 probe 1: the family-level classifier verdicts R8 into bin (iii) -- "
       "the registered quantifier is family-level, and correctly so")
    # Probe 2 (heterogeneous consult/form row): consults standing in w0
    # (marginal 0), forms fresh in w1 (marginal >= eps) -- the row-level
    # classifier lands it UNBINNED (firing mode 2); it is absorbed by the
    # reading's world-uniform conditioning category (one conditioning
    # category per mechanism across the family), stated in the reading.
    het_ledger = _Ledger('f1_hetero_w1')
    b_het = het_ledger.transition({('F1', 'fresh_w1')})
    het = _row_facts('F1_heterogeneous_probe', [
        {'outcome': _argmin_pos(V_SEP[0]), 'viol': 0, 'marginal': F(0),
         'standing_level': b_het, 'consults_standing': True,
         'upstream_booking': b_het},
        {'outcome': _argmin_pos(V_SEP[1]), 'viol': 0, 'marginal': b_het,
         'standing_level': F(0), 'consults_standing': False,
         'upstream_booking': F(0)},
    ])
    ck(het['exact_per_event'] is True,
       "F1 probe 2: the heterogeneous row is honestly exact per world")
    ck(het['marginal_min'] == 0 and het['marginal_max'] >= EPS,
       "F1 probe 2: mixed marginal profile (0 in w0, >= eps in w1)")
    ck(_assign_bin(het, hold_available=True) == 'UNBINNED',
       "F1 probe 2: the world-heterogeneous conditioning row lands UNBINNED "
       "(firing mode 2 of the tripwire) -- absorbed by the reading's "
       "world-uniform conditioning category, stated, [P_structural]-priced")

    # ---- the named flags, assertable ---------------------------------------
    ck(TRICHOTOMY_EXHAUSTIVENESS == 'FAITHFUL_REPRESENTATION_READING_WORLD_UNIFORM',
       "exhaustiveness rides the faithful-representation reading incl. the "
       "world-uniform conditioning category ([P_structural] cap, NAMED)")

    passed = not fails
    return {
        'name': 'L_mechanism_trichotomy',
        'epistemic': ('P_structural | faithful-representation reading '
                      '(world-uniform conditioning category); scoped premises '
                      'K1-UT + Omega-conditioning; bin (ii) type-assigned'),
        'passed': passed,
        'tier': 4,
        'key_result': (
            'Per admissible configuration family: every admissible selection '
            'mechanism at a genuine N >= 2 BW-distinct-cost choice event lands '
            '-- per event, at the world-family level (exactness is a '
            'family-level property; bookings are realized per world) -- in '
            'exactly one of four bins: (i) pays-fresh (books >= eps marginal); '
            "(i') consults-standing (zero marginal); (ii) the hold (zero "
            'pre-commit; TYPE-ASSIGNED via the held conditioning category; '
            'dual premise exemption constitutive; populated as an exact '
            'competitor only under the named grant G-hold-exact); (iii) '
            'does-not-exactly-select per-event. Exhaustiveness rides the '
            'faithful-representation reading incl. the world-uniform '
            'conditioning category [P_structural cap, named]; the marginal '
            'column is two-valued {0} u [eps, oo) (computed); the UNBINNED '
            'tripwire is live with two owned firing modes (untagged hold; '
            'world-heterogeneous conditioning row).'
        ),
        'dependencies': ['A1', 'L_epsilon_star', 'L_cost', 'D_quotient_forced',
                         'T_coherent_free_spend_permanent',
                         'T_selection_approximate_A2', 'occupancy'],
        'cross_refs': ['L_commutative_no_unresolved_hold',
                       'T_no_IJC_no_noncommutativity',
                       'T_hold_cost_dominance_split', 'T_gapless_serial_floor'],
        'artifacts': {
            'bins': ("R1/R2/R8 -> iii; R3/R5/R6a -> i; R4/R6b/R7/R9 -> i'; "
                     "hold -> ii (type-assigned); rows 1-9 binned BY "
                     "COMPUTATION (the scope of that phrase)"),
            'premise_scopes': ('K1-UT scoped to committed realignments (ledger '
                               'transitions); Omega-conditioning scoped to '
                               'classical/Sep mechanisms; the hold exempt from '
                               'both (exemption 1 price-shaped grant-free; '
                               'exemption 2 capability-shaped under the grant)'),
            'k1_ut_disambiguation': ("K1-UT is NOT the bank's K1 "
                                     "(D_quotient_forced dep label) and NOT "
                                     ".411's candidate-switch K1 (stage-2 F3)"),
            'f1_firing_modes': ('UNBINNED fires on (1) untagged hold facts '
                                '(bin (ii) is type-assigned, not '
                                'cost-computed) and (2) world-heterogeneous '
                                'conditioning rows (absorbed by the '
                                'world-uniform conditioning category)'),
            'fences': ('no-forbidding (computed); no-magnitude (0 < eps only); '
                       'occupancy = input at hold-availability only '
                       '(registry tripwired); degenerate-family concession'),
            'walk_checks': ('walk_trichotomy_theorem.py 346 + '
                            'walk_pricing_lemma.py 189, 0 fail; audits: '
                            'pricing REDUCE 0.85 fixed, stage-1 '
                            'LAND-WITH-FIXES 0.82 fixed, stage-2 '
                            'LAND-WITH-FIXES 0.85 (F1-F3 carried)'),
            'note_home': 'The Turning/quantum_selected_mechanism_2026-07-08/',
        },
        'fail_reasons': fails,
    }


def check_T_hold_cost_dominance_split():
    """The two-clause conditional theorem (see module docstring, statement 2).
    Tier 4, [P_structural] WITH THE NAMED GRANT G-hold-exact + the named
    reading R-A2-mech; grant-declining consumers read [P_structural_reading]
    (clause 2 survives grant-free as the price-table fact).  No citation may
    drop the indifference clause.  Regime_R is a cross_ref, not a dependency
    (naming-only consumption on the M4 leg; stage-2 m3)."""
    from apf.core import check_T_no_IJC_no_noncommutativity
    from apf.operational_completeness import check_T_ledger_rent_excluded
    from apf.commutative_no_unresolved_hold import (
        check_L_commutative_no_unresolved_hold)
    from apf.continuation_calculus import check_T_selection_approximate_A2
    from apf.plec import check_Regime_R
    from apf.crystal_axiom_roots import PLEC_AXIOM_ROOTS

    fails = []

    def ck(cond, msg):
        if not cond:
            fails.append(msg)

    # ---- the trichotomy, consumed live as the theorem's frame -------------
    r_lem = check_L_mechanism_trichotomy()
    ck(r_lem.get('passed') is True, "L_mechanism_trichotomy passes")
    ck(r_lem.get('epistemic', '').startswith('P_structural'),
       "the trichotomy's [P_structural] cap is inherited (the reading + the "
       "two scoped premises travel into this theorem)")

    # ---- live bank anchors -------------------------------------------------
    r_rent = check_T_ledger_rent_excluded()
    ck(r_rent.get('passed') is True and r_rent.get('epistemic') == 'P',
       "anchor T_ledger_rent_excluded [P] passes")
    ck('Two cost kinds, no standing rent' in r_rent.get('key_result', ''),
       "the cost-kind dichotomy present: B2 standing levels are typed NOT "
       "bookings and NOT A2-comparable spend (consumed as typed)")
    ck('occupancy' not in r_rent.get('dependencies', []),
       "rent-exclusion anchor is occupancy-free (live dep check)")
    r_hold = check_L_commutative_no_unresolved_hold()
    ck(r_hold.get('passed') is True and r_hold.get('epistemic') == 'P_math',
       "anchor L_commutative_no_unresolved_hold [P_math] passes")
    ck(r_hold.get('dependencies', None) == [],
       ".412 lemma deps == [] (self-contained exact linear algebra)")
    ck('grade_gate' in r_hold.get('artifacts', {}) and
       '[P_math]' in r_hold['artifacts']['grade_gate'],
       ".412 [P_math] gate confirmed via artifacts (field pin)")
    ck('no admissible observable witnesses a coherent hold'
       in r_hold.get('key_result', ''),
       "Corollary 1's banked direction present in key_result (the "
       "contrapositive consumed: witnessed coherent hold => NON-commutative "
       "interface algebra; strictly conditional, no forcing)")
    r_a2 = check_T_selection_approximate_A2()
    ck(r_a2.get('passed') is True and r_a2.get('epistemic') == 'P_structural',
       "anchor T_selection_approximate_A2 [P_structural] passes")
    ck(r_a2.get('artifacts', {}).get('status_fence') ==
       'approximate form certified; A2 tie-selection + BW non-degeneracy '
       'remain named opens',
       "Corollary 2 + the grant tie: the bank mechanizes only APPROXIMATE A2 "
       "(exact field pin); the granted capability (exact per-event selection) "
       "is precisely the named-open content -- the grant is a NAMED MODEL "
       "INPUT, never banked content")
    r_spec = check_T_no_IJC_no_noncommutativity()
    ck(r_spec.get('passed') is True and
       r_spec.get('epistemic') == 'P_structural',
       "anchor T_no_IJC_no_noncommutativity [P_structural] passes (rider (d): "
       "the Sep spectator satisfies the constitutive base minus "
       "occupancy-hosted structure)")
    ck(sorted(r_spec.get('dependencies', [])) == ['A1', 'A2', 'BW', 'MD'],
       "the spectator rides A1+MD+A2+BW (Sep branch)")
    # M4 leg -- NAMING-ONLY consumption (Regime_R is a cross_ref, not a dep,
    # per stage-2 m3 + the .402 SCC edge-hygiene discipline):
    r_R = check_Regime_R()
    ck(r_R.get('passed') is True and r_R.get('epistemic') == 'P',
       "Regime_R [P] passes (the A2 root's well-posedness anchor; "
       "naming-only -- cross_ref, never strict-leg gating)")
    ck('L_irr' in r_R.get('dependencies', []),
       "Regime_R rides L_irr (occupancy-adjacent) -- one more reason the "
       "A2-root consumption is naming-only")
    a2_root = PLEC_AXIOM_ROOTS['A2']
    ck(a2_root['statement'] ==
       'G_realized = argmin_{q in A_Gamma} K[q] (PLEC selector)',
       "M4: the banked A2 root is the PATH-FUNCTIONAL argmin (exact field "
       "pin); the extension to mechanism-histories is the NAMED READING "
       "R-A2-mech, not banked content")
    ck(a2_root['check'] == 'Regime_R',
       "M4: the root's check is Regime_R (well-posedness), not a per-event law")
    ck(M4_STATUS == 'NAMED_READING',
       "M4 VERDICT FLAG: R-A2-mech is a NAMED READING (per-event exact A2 "
       "NOT banked)")

    # ---- the model ----------------------------------------------------------
    M = _run_model(ck)
    battery, bins = M['battery'], M['bins']
    RH, RH_WITHHELD = M['RH'], M['RH_WITHHELD']
    commit_bookings, exact_rows = M['commit_bookings'], M['exact_rows']

    # ---- Clause 1: CONDITIONAL STRICT LEG vs bin (i) ------------------------
    ck(STRICT_LEG_FORM == 'CONDITIONAL_ON_G_HOLD_EXACT',
       "STRICT-LEG CITATION FORM (assertable): conditional on the named "
       "grant; may not be cited simpliciter")
    ck(G_HOLD_EXACT == 'GRANTED', "the grant is in force for this pass")
    bin_i = [f for f in battery if bins[f['row']] == 'i']
    ck(len(bin_i) >= 3, "bin (i) is populated (R3, R5, R6a)")
    for facts in bin_i:
        for j in range(len(V_SEP)):
            m = facts['per_world'][j]['marginal']
            h = RH['per_world'][j]['marginal']
            ck(m >= EPS, "strict leg: %s w%d marginal >= eps (pricing B1)" %
               (facts['row'], j))
            ck(h == 0, "strict leg: hold w%d marginal == 0 (FREE leg)" % j)
            ck(h < m, "STRICT (conditional on G-hold-exact): hold 0 < %s "
                      "marginal (only 0 < eps used)" % facts['row'])
            floor_j = commit_bookings[j][0]
            ck(h + floor_j < m + floor_j,
               "STRICT with commit floor (conditional): hold total < %s "
               "total (floor cancels; derived from M1 + shared outcome)"
               % facts['row'])

    # ---- Clause 2: INDIFFERENCE LEG vs bin (i') -----------------------------
    bin_ip = [f for f in battery if bins[f['row']] == "i'"]
    ck(len(bin_ip) >= 4, "bin (i') is populated (R4, R6b, R7, R9)")
    for facts in bin_ip:
        for j in range(len(V_SEP)):
            ck(facts['per_world'][j]['marginal'] == 0 and
               RH['per_world'][j]['marginal'] == 0,
               "indifference: %s w%d comparison is 0-vs-0 (computed)"
               % (facts['row'], j))
    for facts in exact_rows:
        for j in range(len(V_SEP)):
            ck(RH['per_world'][j]['marginal'] <=
               facts['per_world'][j]['marginal'],
               "hold never cost-dispreferred vs %s (w%d)" % (facts['row'], j))
    # THE GUARD (permanent anti-strengthening tripwire): an exact non-hold
    # mechanism with marginal EQUAL to the hold's exists, so "A2 selects the
    # hold" SIMPLICITER (strictly over every classical mechanism) is
    # computed FALSE.  The indifference clause is load-bearing and may never
    # be dropped from a citation.
    equal_exists = any(
        facts['per_world'][j]['marginal'] == RH['per_world'][j]['marginal']
        for facts in bin_ip for j in range(len(V_SEP)))
    ck(equal_exists,
       "GUARD: strict preference on (i') is FALSE by computation (0-vs-0 tie "
       "witnessed on four independent rows)")
    # B2 levels do not rescue the standing bin (two-sided structural witness;
    # the exclusion is typed via the banked cost-kind dichotomy):
    ck(any(f['per_world'][j]['standing_level'] >= EPS
           for f in bin_ip for j in range(len(V_SEP))),
       "B2 witness (i): standing levels GENUINELY stand >= eps on the "
       "standing bin")
    ck(all(f['per_world'][j]['marginal'] == 0
           for f in bin_ip for j in range(len(V_SEP))),
       "B2 witness (ii): those levels NEVER enter the marginal column "
       "(levels typed apart from bookings; dichotomy consumed as typed)")

    # ---- Rider (c): bin (iii) + the degenerate-family concession -----------
    bin_iii = [f for f in battery if bins[f['row']] == 'iii']
    ck(len(bin_iii) == 3, "bin (iii) holds R1, R2, R8 on the separating family")
    for facts in bin_iii:
        ck(not facts['exact_per_event'],
           "%s does not exactly select per-event (computed)" % facts['row'])
    r1 = next(f for f in battery if f['row'] == 'R1_inslot_fold')
    ck(r1['eventual_exact'],
       "eventual-argmin concession NAMED: the fold is exact per-history")
    ck(M['fiat_deg_hits'] == len(V_DEG),
       "(c) rider: on argmin-degenerate families fiat/blind are exact at "
       "zero cost and JOIN the 0-vs-0 indifference class (computed) -- bin "
       "(iii)'s exclusion is per-family under the named separation assumption")

    # ---- Rider (d): the spectator is fully admissible -----------------------
    bins_sep = M['bins_sep']
    ck(bins_sep['RH_the_hold'] == 'UNAVAILABLE' and
       any(bins_sep[r] == 'i' for r in bins_sep) and
       any(bins_sep[r] == "i'" for r in bins_sep) and
       any(bins_sep[r] == 'iii' for r in bins_sep),
       "rider (d): the Sep spectator selects approximately (banked form) or "
       "pays fresh or consults standing -- FULLY ADMISSIBLE; occupancy stays "
       "the QAC, no leg concludes it")

    # ---- Corollary 1 is conditional: consuming the bridge changes no bin ----
    ck(bins == {f['row']: _assign_bin(f, M['hold_available']) for f in battery},
       "Corollary 1 (.412 bridge) is CONDITIONAL: consuming it changes no "
       "bin -- nothing forces selection to be hold-realized; occupancy says "
       "which worlds host holds; no forcing anywhere")

    # ---- flags + registry ---------------------------------------------------
    ck(R7_WIDTH_DIAL == 'RULED_AS_IS_FUSED_READS_FREE_2026_07_09',
       "R7 WIDTH DIAL RULED AS-IS (Ethan 2026-07-09): fused reads free is "
       "the convention-of-record; statements verified stable, widths "
       "unchanged; the reversed branch retained as road-not-taken")
    ck(M['occupancy_reads'] == ['hold_availability'],
       "occupancy consumed exactly once, at hold-AVAILABILITY only")

    passed = not fails
    return {
        'name': 'T_hold_cost_dominance_split',
        'epistemic': ('P_structural | named grant G-hold-exact; named reading '
                      'R-A2-mech'),
        'passed': passed,
        'tier': 4,
        'key_result': (
            'Conditional on the named grant G-hold-exact (granted, not '
            'derived; possibly permanent): (1) the hold is strictly cheaper '
            'than every bin-(i) fresh-formation mechanism -- marginal 0 vs '
            '>= eps, common commit floor cancelling (derived from M1 + '
            'shared outcome) -- by 0 < eps only; (2) among exact mechanisms '
            'the hold is never cost-dispreferred: vs every bin-(i\') '
            'standing-consult mechanism the comparison is 0-vs-0 and A2 '
            'alone does not pick (tie witnessed + GUARDED: '
            'strict-over-all-classical computed FALSE). No citation may drop '
            'the indifference clause. Grant-free residue (clause 2 '
            'fallback): the hold\'s marginal is 0 in every world ([P] FREE '
            'leg), no mechanism books below 0, every standing-consult exact '
            'mechanism ties it 0-vs-0. Riders: bin-(iii) exclusion is '
            'per-family (named separation assumption; degenerate families '
            'join the indifference class -- computed); the Sep spectator is '
            'fully admissible. Corollary 1 (.412 bridge, [P_math]-on-banked, '
            'strictly conditional, no forcing): a witnessed coherent hold => '
            'non-commutative interface algebra. Corollary 2 (openness '
            'reframe, [P_structural_reading], fresh-side only, '
            'grant-conditional): among fresh realizations the zero-price '
            'exact option is hold-shaped. Grant-declining consumers read '
            '[P_structural_reading].'
        ),
        'dependencies': ['A1', 'L_epsilon_star', 'L_cost', 'D_quotient_forced',
                         'T_coherent_free_spend_permanent',
                         'T_ledger_rent_excluded',
                         'L_commutative_no_unresolved_hold',
                         'T_selection_approximate_A2',
                         'T_no_IJC_no_noncommutativity',
                         'L_mechanism_trichotomy', 'occupancy'],
        'cross_refs': ['Regime_R', 'T_gapless_serial_floor'],
        'artifacts': {
            'grade_gate': ('[P_structural] with the named grant G-hold-exact '
                           '+ named reading R-A2-mech (stage-2 grade ruling, '
                           '2026-06-29 grade-by-tracked-dependencies); '
                           'grant-declining consumers read '
                           '[P_structural_reading] -- clause 2 survives '
                           'grant-free as the price-table fact'),
            'grant_status': ('granted-not-derived (approximate-A2 status '
                             'fence names the capability OPEN); record-side '
                             'unverifiable (.412 dephasing leg); benefit-leg '
                             'discharge graveyarded => possibly permanent; '
                             'capability-shaped not price-shaped (withheld '
                             'hold: bin (iii), price unchanged -- computed)'),
            'r7_dial': ('RULED AS-IS (Ethan 2026-07-09): fused reads free '
                        'is the convention-of-record; practical content now '
                        'unconditional -- the indifference clause + '
                        'conditional fresh-side dominance; the reversed '
                        'branch (R7/R4/R9 migrate to bin (i), strict leg '
                        'widens) retained as the recorded road-not-taken; '
                        'grounds: the M2 counter-world arithmetic, the '
                        'L_cost per-transition billing locus, and the '
                        'frustrated-family structural route to strictness'),
            'may_not_cite': ('"A2 selects the hold" simpliciter (computed '
                             'FALSE -- the guard); clause 1 grant-free; the '
                             'split without the indifference clause; strict '
                             'preference over standing-consult in any '
                             'phrasing; bin-(iii) exclusion without the '
                             'family-separation assumption; any per-world '
                             'pricing floor; hold-existence-as-exact-'
                             'competitor as banked (it is the grant); '
                             'anything concluding occupancy; any forbidding; '
                             'eps magnitude'),
            'floor_equality': ('DERIVED from M1 + shared outcome (exactness '
                               '=> same final structure => same floor), not '
                               'independently measured (stage-2 m4)'),
            'regime_r': ('cross_ref, NOT a dependency: naming-only '
                         'consumption on the M4 leg (stage-2 m3; .402 SCC '
                         'edge-hygiene discipline)'),
            'exemption_split': ('exemption 1 (K1-UT/price) grant-free; '
                                'exemption 2 (Omega/capability) under the '
                                'grant (stage-2 m2)'),
            'fences': ('no-forbidding (computed); no-magnitude (0 < eps '
                       'only); occupancy input-never-conclusion '
                       '(hold-availability only, registry tripwired); '
                       'degenerate-family concession; exemption-bundle split'),
            'walk_checks': ('walk_trichotomy_theorem.py 346 + '
                            'walk_pricing_lemma.py 189, 0 fail; audits: '
                            'pricing REDUCE 0.85 fixed, stage-1 '
                            'LAND-WITH-FIXES 0.82 fixed, stage-2 '
                            'LAND-WITH-FIXES 0.85 (F1-F3 carried)'),
            'note_home': 'The Turning/quantum_selected_mechanism_2026-07-08/',
        },
        'fail_reasons': fails,
    }


_CHECKS = {
    'L_mechanism_trichotomy': check_L_mechanism_trichotomy,
    'T_hold_cost_dominance_split': check_T_hold_cost_dominance_split,
}


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
        print(r['name'], '::', r['epistemic'], '::',
              'PASS' if r['passed'] else 'FAIL')
        if not r['passed']:
            bad = True
            for f in r['fail_reasons']:
                print('  -', f)
    sys.exit(1 if bad else 0)
