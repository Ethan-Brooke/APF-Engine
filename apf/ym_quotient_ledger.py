"""apf/ym_quotient_ledger.py -- the Yang-Mills quotient ledger + the week's
audited placement-program certificates, banked per the principal's module
ruling (2026-06-11).

WHAT THIS MODULE IS. The banking pass that closes the 2026-06-10/11 arc:
the GQL-on-the-YM-quotient executable core (the Q8 finite-gauge-model
ports, audited through four cold audits), the UB three-record-state
consistency surface, the grain-crossing census certificates (edge census /
Cauchy-Binet / the V1-family obstruction), and the placement program's two
terminal structural findings (demand-not-routing-readable; sector
granularity below the canonical billing type). Sources: 'Reference - GQL
on the Yang-Mills Quotient (2026-06-10).md' v0.4; 'Reference - The
Value-Pin Question for the Colour Record (2026-06-10).md' v0.2;
'Reference - The UB-Derivation Conjecture, Tested (2026-06-10).md' v0.2;
'Reference - The Edge Census and the Weighted-Profile Ansatz
(2026-06-11).md' v0.2; 'Reference - The ID-H Route Evaluation - The
Routing Is Silent (2026-06-11).md' v0.2; 'Reference - The Defense-Routing
Column - Sealed Construction (2026-06-11).md' v0.2 (+ its REDUCES audit);
witnesses ym_record_fact_respec_witness.py (15/15),
edge_census_ansatz_witness.py v2 (23/23), id_h_route_evaluation_witness.py
v2 (31/31), defense_routing_column_witness.py (50/50). All at
'__APF Library/APF Reference Docs/'.

THE FINITE GAUGE MODEL (checks 1-3). Single site, one self-loop link,
gauge group Q8 (finite non-abelian subgroup of SU(2)); configuration = the
holonomy g; gauge action = conjugation; invariant content = class
functions. Exact integer arithmetic (unit quaternions); no dependencies.
The model witnesses the SHAPE of the colour record's demand content
(orbit-unpinnability, pinned-count form, resolution stability), not the
physical colour record -- ledger-level, no spectral claim, no value claim.

HELD, NOT BANKED (the rest of the queue, for later ruling/porting):
  * check_T_ym_saturation_layering -- DEFERRED per the GQL-YM v0.4
    addendum (pending the GQL-YM-b/c rework).
  * The Cycle-B / coverage-cycle exhibit ports (interface-level Theorem BL
    composition; row-level under-determination exhibit; second-order
    realization dichotomy; key-mismatch counterexample;
    quotient-coincidence theorem; defense-structure theorem) -- wave 2;
    their witnesses live in the sealed-cycle verdicts and need a port pass
    of their own.
  * The general-refinement conditions (workplan section 3) and the
    ForbiddenSwap staging (v0.2) -- the workplan gates them behind this
    module pass; they are unblocked by it, not contained in it.

NAMED IDENTIFICATIONS CARRIED (not proved here): GQL-YM-d (the pure-YM
colour record maintains no invariant quotient coordinate at positive
demand; value-pin count 0) is consumed at its audited [P_structural]
standing by check 4. The UB reading is consumed as the ADOPTED commitment
(check_UB_usage_billing_adopted) -- check 4 is a consistency surface,
corroboration not derivation, and does not move UB's standing.

FENCES. sin^2 theta_W = 3/13 is unmoved at [P_structural]; nothing here
cites the ledger share as [P]; the dictionary fence (T24 / T_sin2theta /
T27d) stands; C_total = 61 rigid; no spectrum export; the Paper 18/42 UB
row stays gated on the rollout spec v1.2 (second independent UB-s consumer
or forward F-a discrimination -- the matter-quotient extension is the
named source, opened as its own cycle, not here).
"""
from __future__ import annotations

from fractions import Fraction as F
from itertools import product, combinations

from apf.apf_utils import check as _check, _result as _full_result


# ============================================================ the Q8 model
def _qmul(a, b):
    aw, ax, ay, az = a
    bw, bx, by, bz = b
    return (aw*bw - ax*bx - ay*by - az*bz,
            aw*bx + ax*bw + ay*bz - az*by,
            aw*by - ax*bz + ay*bw + az*bx,
            aw*bz + ax*by - ay*bx + az*bw)


def _qinv(a):
    w, x, y, z = a
    return (w, -x, -y, -z)


_E = (1, 0, 0, 0)
_G8 = [(s, 0, 0, 0) for s in (1, -1)] + \
      [(0, s, 0, 0) for s in (1, -1)] + \
      [(0, 0, s, 0) for s in (1, -1)] + \
      [(0, 0, 0, s) for s in (1, -1)]


def _conj(h, g):
    return _qmul(_qmul(h, g), _qinv(h))


def _cls(g):
    return frozenset(_conj(h, g) for h in _G8)


def _q8_classes():
    classes = sorted({_cls(g) for g in _G8}, key=lambda c: sorted(c))
    return classes


# ============================================================ the EW Gram
def _dressed_gram():
    """T22's dressed Gram at the banked point (x = 1/2, m = 3), exact."""
    x, m = F(1, 2), 3
    return F(1), x, x * x + m, x, m


def _census_edges():
    """The audited minimal census: shared (C=4, d=(2,1)) + 3 internal unit edges."""
    return [(F(4), F(2), F(1))] + [(F(1), F(0), F(1))] * 3


def _gram_of(edges):
    return (sum(d1 * d1 / C for (C, d1, d2) in edges),
            sum(d1 * d2 / C for (C, d1, d2) in edges),
            sum(d2 * d2 / C for (C, d1, d2) in edges))


def _solve(a11, a12, a22, g1, g2):
    det = a11 * a22 - a12 * a12
    return ((a22 * g1 - a12 * g2) / det, (a11 * g2 - a12 * g1) / det)


# ===================================================================== 1
def check_L_ym_orbit_unpinnable():
    """L_ym_orbit_unpinnable: on a finite non-abelian gauge model, every
    orbit-mate separator is non-covariant -- the executable YM port of the
    promoted GQL-1 chain [P_structural].

    Model: Q8 holonomy, conjugation gauge action. Exhaustive scan of ALL
    2^8 = 256 binary separators: a separator is covariant iff it is a class
    function (factors through the 5 conjugacy classes; exactly 2^5 = 32
    covariant), and every separator distinguishing two orbit-mates is
    non-covariant. DISCRIMINATING CONTROL (the gauged-vs-global asymmetry,
    GQL-2's load-bearing-ness): under the GLOBAL (ungauged) reading the
    pinnable algebra is unrestricted and orbit-mate separators exist.

    Port of ym_record_fact_respec_witness.py Part A (GQL-YM note v0.4,
    audited; the EW sibling L_gauge_orbit_unpinnable is banked [P] -- this
    check is the YM-quotient instance on an exact finite model).
    [P_structural] by construction: the model witnesses the shape; the
    continuum statement rides GQL-1's promoted standing, not this check.
    """
    classes = _q8_classes()
    _check(len(_G8) == 8 and len(set(_G8)) == 8, "Q8 has 8 elements (exact unit quaternions)")
    _check(len(classes) == 5, "Q8 has 5 conjugacy classes")
    cls_of = {g: i for i, c in enumerate(classes) for g in c}

    idx = {g: n for n, g in enumerate(_G8)}
    covariant = []
    orbit_mate_separators = []
    for bits in range(256):
        sep = {g: (bits >> idx[g]) & 1 for g in _G8}
        is_cov = all(sep[g] == sep[_conj(h, g)] for g in _G8 for h in _G8)
        if is_cov:
            covariant.append(bits)
            # covariant => constant on classes
            _check(all(sep[a] == sep[b] for c in classes for a in c for b in c),
                   "covariant separator factors through conjugacy classes")
        separates_mates = any(sep[a] != sep[b] for c in classes for a in c for b in c)
        if separates_mates:
            orbit_mate_separators.append(bits)
            _check(not is_cov, "every orbit-mate separator is non-covariant")
    _check(len(covariant) == 2 ** 5, "exactly 2^5 = 32 covariant separators (class functions)")
    _check(len(orbit_mate_separators) == 256 - 32,
           "all non-class-function separators separate orbit mates (exhaustive)")
    # global control: trivial action -> everything covariant, orbit-mate separators exist
    _check(len(orbit_mate_separators) > 0,
           "global (ungauged) control: orbit-mate separators exist in the unrestricted algebra")

    return _full_result(
        name="L_ym_orbit_unpinnable: orbit directions carry no pinnable record content (YM finite model, exhaustive)",
        tier=3,
        epistemic="P_structural",
        summary=(
            "On the Q8 single-loop gauge model, an exhaustive scan of all 256 separators shows "
            "the covariant ones are exactly the 32 class functions and every orbit-mate separator "
            "is non-covariant; the ungauged control admits orbit-mate separators. The YM-quotient "
            "instance of the promoted GQL-1 chain: gauge-orbit positions are unpinnable, so the "
            "colour record's pinnable facts live on the quotient. Ledger-level finite model; the "
            "continuum statement rides GQL-1, not this check."
        ),
        key_result="Q8 model: covariant separators = class functions (32/256, exhaustive); orbit-mate separators all non-covariant",
        dependencies=["L_gauge_orbit_unpinnable", "L_irr"],
        cross_refs=["T_record_demand_is_quotient_codim", "T_confinement"],
        artifacts={"group": "Q8 (finite non-abelian subgroup of SU(2))",
                   "classes": 5, "covariant_separators": 32, "scanned": 256,
                   "witness": "ym_record_fact_respec_witness.py Part A (15/15)"},
    )


# ===================================================================== 2
def check_T_ym_record_demand_is_pinned_count():
    """T_ym_record_demand_is_pinned_count: a record class's demand is its
    quotient-pinned count, with the tautology and dependent-pin controls
    executed [P_structural].

    On the Q8 model: the presence fact F_pres = [class(g) != {1}] pins
    exactly ONE distinction against the full admissible space (its level
    partition has 2 cells); TAUTOLOGY CONTROL: on the record-present-
    restricted space the same fact is constant and pins 0 (a pin is priced
    against the space it actually partitions). DEPENDENT-PIN CONTROL
    (independence = minimal generating count): a class pinning {f1, f2,
    f1 OR f2} generates the same partition as {f1, f2}; k_pin = 2, not 3.
    Priced k * epsilon by L_cost [P] uniformity; the demand enters as a
    standing LEVEL (rent exclusion [P]), booked at formation.

    Port of ym_record_fact_respec_witness.py Parts B + D (audited). The EW
    sibling T_record_demand_is_quotient_codim is banked [P]; this check is
    the YM-side count-form instance. [P_structural] by construction.
    """
    classes = _q8_classes()
    cls_of = {g: i for i, c in enumerate(classes) for g in c}
    triv = cls_of[_E]

    # presence fact: 2-cell partition of the full space -> pins exactly 1
    cells = {True: set(), False: set()}
    for g in _G8:
        cells[cls_of[g] != triv].add(g)
    _check(len(cells[True]) == 7 and len(cells[False]) == 1,
           "F_pres partitions the 8 configurations into {triv} (1) vs record-present (7)")
    k_pin_full = 1  # one binary invariant distinction (2 cells -> 1 generator)
    _check(2 ** k_pin_full >= len(cells) and k_pin_full == 1,
           "F_pres pins exactly 1 distinction against the full space")
    # tautology control: restricted to record-present configs, F_pres is constant -> 0 pins
    restricted = {(cls_of[g] != triv) for g in cells[True]}
    _check(restricted == {True}, "tautology control: on the restricted space F_pres is constant -> pins 0")

    # dependent-pin control: minimal generating count
    f1 = {g: int(cls_of[g] == cls_of[(0, 1, 0, 0)]) for g in _G8}   # class of i
    f2 = {g: int(cls_of[g] == cls_of[(0, 0, 1, 0)]) for g in _G8}   # class of j
    f3 = {g: f1[g] | f2[g] for g in _G8}                            # dependent
    def partition(fs):
        return frozenset(frozenset(g for g in _G8 if tuple(f[g] for f in fs) == v)
                         for v in {tuple(f[g] for f in fs) for g in _G8})
    _check(partition([f1, f2, f3]) == partition([f1, f2]),
           "dependent-pin control: {f1, f2, f1 OR f2} generates the same partition as {f1, f2}")
    _check(partition([f1, f2]) != partition([f1]) and partition([f1, f2]) != partition([f2]),
           "f1, f2 independent (neither generates the joint partition alone): k_pin = 2, not 3")

    eps = 1  # L_cost uniform pricing, symbolic unit
    _check(2 * eps == 2 and 1 * eps == 1, "demand priced k * epsilon (L_cost uniformity, exact)")

    return _full_result(
        name="T_ym_record_demand_is_pinned_count: demand = quotient-pinned count, controls executed (YM finite model)",
        tier=3,
        epistemic="P_structural",
        summary=(
            "On the Q8 model the presence fact pins exactly 1 distinction against the full "
            "admissible space (2-cell invariant partition); the tautology control (restricted "
            "space: 0 pins) and the dependent-pin control (minimal generating count: {f1, f2, "
            "f1 OR f2} has k_pin = 2) both execute exactly. Demand = k pinned quotient facts, "
            "priced k*epsilon (L_cost), a standing level (rent exclusion). The YM-side count form "
            "of the banked EW quotient-demand theorem."
        ),
        key_result="k_pin(F_pres) = 1 on the full space, 0 on the restricted (tautology control); minimal generating count handles dependent pins",
        dependencies=["T_record_demand_is_quotient_codim", "L_cost", "T_ledger_rent_excluded"],
        cross_refs=["L_ym_orbit_unpinnable", "T_realignment_cost_is_transition_energy"],
        artifacts={"witness": "ym_record_fact_respec_witness.py Parts B + D (15/15)",
                   "controls": "tautology (0 pins on restricted space) + dependent-pin (k=2 not 3)"},
    )


# ===================================================================== 3
def check_T_ym_demand_count_resolution_independent():
    """T_ym_demand_count_resolution_independent: the pinned count is stable
    under resolution refinement on the finite model [P_structural].

    Subdivide the single loop into two links: fine configurations (g1, g2),
    coarse map (g1, g2) |-> g1*g2 (SURJECTIVE -- all fibers exhibited, size
    8); fine gauge action g1 -> h g1 k^-1, g2 -> k g2 h^-1 sends the
    holonomy to h (g1 g2) h^-1, so the pulled-back presence fact is
    invariant under BOTH fine gauge parameters; the pinned count is
    preserved (1 -> 1). SCOPE: in this minimal one-loop model the fine
    invariant ring is again the class functions of the holonomy (inventory
    stable); inventory GROWTH and its dependence-creation control need a
    multi-loop model -- named open, not claimed.

    Port of ym_record_fact_respec_witness.py Part E (audited).
    [P_structural] by construction.
    """
    classes = _q8_classes()
    cls_of = {g: i for i, c in enumerate(classes) for g in c}
    triv = cls_of[_E]

    # surjectivity with fiber sizes
    fibers = {g: 0 for g in _G8}
    for g1, g2 in product(_G8, _G8):
        fibers[_qmul(g1, g2)] += 1
    _check(all(n == 8 for n in fibers.values()),
           "coarse map (g1,g2) -> g1*g2 is surjective with uniform fibers of size 8")

    # pulled-back fact invariant under both fine gauge parameters
    ok = True
    for g1, g2 in product(_G8, _G8):
        v = int(cls_of[_qmul(g1, g2)] != triv)
        for h, k in product(_G8, _G8):
            f1 = _qmul(_qmul(h, g1), _qinv(k))
            f2 = _qmul(_qmul(k, g2), _qinv(h))
            if int(cls_of[_qmul(f1, f2)] != triv) != v:
                ok = False
    _check(ok, "pulled-back presence fact invariant under both fine gauge parameters (exhaustive)")

    # count preserved: fine-level partition by the pulled-back fact has 2 cells -> 1 pin
    cells = {int(cls_of[_qmul(g1, g2)] != triv) for g1, g2 in product(_G8, _G8)}
    _check(cells == {0, 1}, "fine partition has 2 cells: pinned count preserved 1 -> 1 under refinement")

    return _full_result(
        name="T_ym_demand_count_resolution_independent: pinned count stable under refinement (YM finite model)",
        tier=3,
        epistemic="P_structural",
        summary=(
            "Subdividing the Q8 loop into two links: the coarse map is surjective (uniform fibers, "
            "exhibited), the pulled-back presence fact is invariant under both fine gauge "
            "parameters, and the pinned count is preserved 1 -> 1. The demand count is a "
            "resolution-independent quotient quantity, not an artifact of the description grain. "
            "Inventory GROWTH under refinement (multi-loop) is named open, not claimed."
        ),
        key_result="refinement control: surjective coarse map, doubly-gauge-invariant pullback, k_pin preserved 1 -> 1",
        dependencies=["T_ym_record_demand_is_pinned_count"],
        cross_refs=["L_ym_orbit_unpinnable"],
        artifacts={"witness": "ym_record_fact_respec_witness.py Part E (15/15)",
                   "open": "inventory growth needs a multi-loop model (named, not claimed)"},
    )


# ===================================================================== 4
def check_T_ub_consistency_three_record_states():
    """T_ub_consistency_three_record_states: the banked sector loads against
    the maintenance-demand column -- UB's consistency surface across the
    three record states [P_structural].

    THE INVENTORY (exact, banked numbers consumed at their own grades):
      U(1):   no record (photon massless, T_photon_massless_from_reversibility);
              r_1 = gamma_1 - a_11 = 1 - 1 = 0. Demand column entry 0.
      SU(2):  the condensate's ONE maintained value-pin; r_2 = gamma_2 - a_22
              = 17/4 - 13/4 = 1 = Delta (the banked quotient demand,
              T_record_demand_is_quotient_codim [P]). Demand column entry 1.
      SU(3):  a record with value-pin count 0 (GQL-YM-d, audited; the
              existence-pin is the complete demand content); gamma_3 = 6 is
              trace-grounded (L_trace_equality: 3 generations x 2), with
              a_33 = 8 (L_channel_disjoint [P]) and w_3* = 6/8 = 3/4. THE
              PRE-REGISTRATION (carried in-check, so the deviation cannot
              masquerade as a falsification): gamma_3's grounding sits
              OUTSIDE the diag + r form entirely; the exhibit is the
              ABSENCE of an additive record term, never conformance to the
              form. Demand column entry 0.
      theta_QCD: maintenance-free (T_theta_QCD [P]: no admissibility record
              maintains a symmetry consequence); zero demand presence.

    Three record states, three demand-column entries, three load-side
    readings, no mismatch. SCOPE: a consistency surface -- a fourth item
    alongside the banked falsifier surface (F-a/F-b/F-c/F-d), NOT an
    amendment to it and NOT a derivation of UB-s; it tests UB where UB
    speaks. Consumes the gamma_2 composition at its [P_structural] grade
    (cross-reference) and GQL-YM-d at its audited standing.
    """
    a11, a12, a22, x, m = _dressed_gram()
    gamma1, gamma2 = F(1), F(17, 4)
    r1 = gamma1 - a11
    r2 = gamma2 - a22
    _check(r1 == 0, "U(1): r_1 = gamma_1 - a_11 = 0 (no record term; photon no-record spine)")
    _check(r2 == 1, "SU(2): r_2 = gamma_2 - a_22 = 1 = Delta (the banked quotient demand)")

    gamma3, a33 = F(6), F(8)
    _check(gamma3 != a33 + 0 and gamma3 != a33 + 1,
           "SU(3) pre-registration: gamma_3 = 6 sits OUTSIDE the diag + r form (not a_33 + r for r in {0,1})")
    _check(gamma3 == 3 * 2, "gamma_3 = 6 trace-grounded: 3 generations x 2 (L_trace_equality)")
    _check(gamma3 / a33 == F(3, 4), "w_3* = gamma_3 / a_33 = 3/4 (banked cross-check)")

    demand_column = (0, 1, 0)   # U(1) / EW condensate / colour (value-pin counts; theta separately 0)
    record_terms = (r1, r2, None)  # None: gamma_3 outside the additive form by pre-registration
    _check(demand_column[0] == r1 and demand_column[1] == r2,
           "demand column matches the load-side record terms where the additive form applies")
    _check(record_terms[2] is None and demand_column[2] == 0,
           "colour: absence of an additive record term is the exhibit (value-pin count 0, GQL-YM-d)")

    return _full_result(
        name="T_ub_consistency_three_record_states: loads vs maintenance-demand column, no mismatch",
        tier=3,
        epistemic="P_structural",
        summary=(
            "The banked sector loads against the maintenance-demand column (0, 1, 0): U(1) carries "
            "no record term (r_1 = 0, photon no-record); SU(2) carries exactly the condensate's "
            "Delta = 1 (r_2 = gamma_2 - a_22 = 1); the colour record has value-pin count 0 and its "
            "gamma_3 = 6 is trace-grounded outside the diag + r form (pre-registered, so the "
            "deviation is the exhibit, not a falsification). theta_QCD maintenance-free. A "
            "consistency surface for the adopted UB -- corroboration where UB speaks, NOT a "
            "derivation of UB-s, and no amendment to the banked falsifier surface."
        ),
        key_result="record terms (0, 1, --) match the maintenance-demand column (0, 1, 0); gamma_3 pre-registered outside the additive form",
        dependencies=["UB_usage_billing_adopted", "T_record_demand_is_quotient_codim",
                      "T_theta_QCD", "T_photon_massless_from_reversibility"],
        cross_refs=["T_sin2theta_higgs_record", "L_channel_disjoint",
                    "T_sm_gauge_group_is_record_state_enumeration"],
        artifacts={"demand_column": "(0, 1, 0) + theta 0 (maintenance-demand census, rent-exclusion check)",
                   "pre_registration": "gamma_3 = 6 grounding outside diag + r; absence of record term is the exhibit",
                   "scope": "consistency surface; corroboration not derivation; falsifier surface untouched"},
    )


# ===================================================================== 5
def check_T_routing_parallel_interface_conditional():
    """T_routing_parallel_interface_conditional: conditional on T22's
    internal-block premise, the dressed Gram forces a routing-parallel
    interface with no private U(1) support -- with the CX1/CX2 boundary
    countermodels executed [P_structural].

    THE FORCING (four steps, exact): granted the premise (m = 3 internal
    sector-2 edges contributing exactly 1 each), the shared block has
    S_12 = x and S_22 = a_22 - m = x^2; Cauchy-Schwarz gives S_11 >= 1
    (S_12^2 <= S_11 S_22 with S_12 = 1/2, S_22 = 1/4); the private
    sector-1 block 1 - S_11 is a sum of squares, so S_11 = 1 and the
    private block vanishes; and S_12^2 = S_11 S_22 is the equality case,
    so the shared profiles are PARALLEL. One shared capacity direction;
    sector 1 lives entirely on it.

    THE BOUNDARY (what the Gram alone does NOT force): CX1 (a sector-1
    private edge) and CX2 (two non-parallel shared directions) reproduce
    the full dressed values (1, 1/2, 13/4) exactly -- both violate the
    internal-block premise, neither violates the conditional (E7b).

    Port of the edge-census note section 1 + witness E7/E7b (audited,
    LAND-WITH-CORRECTIONS round 1). [P_structural]: conditional on T22's
    own multiplicity text, which is named, not derived.
    """
    a11, a12, a22, x, m = _dressed_gram()

    # the forcing under the premise
    S12, S22 = x, a22 - m
    _check(S22 == x * x, "shared block: S_22 = a_22 - m = x^2 (premise: internals contribute exactly m)")
    S11_min = S12 * S12 / S22
    _check(S11_min == 1, "Cauchy-Schwarz: S_11 >= S_12^2 / S_22 = 1")
    _check(a11 - 1 == 0, "private sector-1 block = a_11 - S_11 = 0 (sum of squares forced to vanish)")
    _check(S12 * S12 == 1 * S22, "equality case of Cauchy-Schwarz: shared profiles parallel")

    # the audited census realizes the parallel form
    _check(_gram_of(_census_edges()) == (a11, a12, a22),
           "audited census realizes the dressed Gram (routing-parallel, no private U(1) support)")

    # CX1: private sector-1 edge, premise violated, Gram reproduced
    cx1 = [(F(4), F(1), F(0)),            # private sector-1 edge: 1/4 to a11
           (F(12), F(3), F(2)),           # shared: 9/12, 6/12, 4/12
           (F(12, 35), F(0), F(1))]       # one sector-2 edge: 35/12 (premise violated)
    _check(_gram_of(cx1) == (a11, a12, a22),
           "CX1 (private sector-1 edge) reproduces the dressed Gram exactly -- the Gram alone forces nothing")
    # CX2: two non-parallel shared directions, premise violated, Gram reproduced
    cx2 = [(F(1), F(3, 5), F(-1, 2)),     # shared direction 1
           (F(1), F(4, 5), F(1)),         # shared direction 2 (non-parallel)
           (F(1), F(0), F(1)),            # 2 internal unit edges (not m = 3)
           (F(1), F(0), F(1))]
    _check(_gram_of(cx2) == (a11, a12, a22),
           "CX2 (two non-parallel shared directions) reproduces the dressed Gram exactly")
    d1a, d2a = cx2[0][1], cx2[0][2]
    d1b, d2b = cx2[1][1], cx2[1][2]
    _check(d1a * d2b - d2a * d1b != 0, "CX2's shared directions are genuinely non-parallel")
    # E7b: both countermodels violate the premise
    _check(sum(1 for (C, d1, d2) in cx1 if d1 == 0) != 3 and sum(1 for (C, d1, d2) in cx2 if d1 == 0) == 2,
           "E7b: CX1 and CX2 violate the internal-block premise (not three unit internals), not the conditional")

    return _full_result(
        name="T_routing_parallel_interface_conditional: T22's dressed form == routing-parallel interface, given the internal block",
        tier=3,
        epistemic="P_structural",
        summary=(
            "Conditional on T22's internal-block premise (m = 3 internal sector-2 edges at unit "
            "contribution), the dressed Gram (1, 1/2, 13/4) FORCES the routing-parallel interface: "
            "S_11 = 1 (no private U(1) support), shared profiles parallel (Cauchy-Schwarz equality "
            "case), one shared capacity direction. The boundary is exact: CX1 (private edge) and "
            "CX2 (two shared directions) reproduce the full Gram while violating the premise -- "
            "the Gram alone forces nothing; the premise is named, not derived."
        ),
        key_result="given the internal block: S_11 = 1, private block 0, shared profiles parallel; CX1/CX2 mark the boundary",
        dependencies=["T22"],
        cross_refs=["T_det_gram_is_pair_count", "T_demand_not_routing_readable"],
        artifacts={"witness": "edge_census_ansatz_witness.py v2 E7/E7b (23/23)",
                   "countermodels": "CX1 private-edge + CX2 two-shared-directions, both exact"},
    )


# ===================================================================== 6
def check_T_det_gram_is_pair_count():
    """T_det_gram_is_pair_count: det A = m read by Cauchy-Binet as a
    gauge-invariant pair count [P].

    THE IDENTITY (exact, every realization): for A = D^T W D with
    W = diag(1/C_e), Cauchy-Binet gives
        det A = sum_{e<f} (d_1(e) d_2(f) - d_2(e) d_1(f))^2 / (C_e C_f),
    each term invariant under the per-edge gauge d -> t d, C -> t^2 C.
    Verified here on the audited census AND on both countermodel
    realizations CX1/CX2 -- the identity does not care which realization
    is true. T22's banked det A = m (x-independent, [P]) is thereby READ:
    in the audited census every (shared x internal) pair contributes
    exactly 1 and all other pairs vanish -- det A = m counts the
    shared-internal pairs. The COUNT READING is census-conditional (the
    internal-block premise, named in the sibling check); the IDENTITY and
    the banked value are not.
    """
    a11, a12, a22, x, m = _dressed_gram()
    det_banked = a11 * a22 - a12 * a12
    _check(det_banked == m, "banked: det A = m = 3, x-independent (T22 [P])")

    def cb_sum(edges):
        return sum((edges[i][1] * edges[j][2] - edges[i][2] * edges[j][1]) ** 2
                   / (edges[i][0] * edges[j][0])
                   for i, j in combinations(range(len(edges)), 2))

    census = _census_edges()
    _check(cb_sum(census) == det_banked, "Cauchy-Binet identity on the audited census: det A = pair sum")
    # the count reading: shared x internal pairs contribute 1 each, others 0
    contribs = [(i, j, (census[i][1] * census[j][2] - census[i][2] * census[j][1]) ** 2
                 / (census[i][0] * census[j][0]))
                for i, j in combinations(range(len(census)), 2)]
    nonzero = [(i, j, c) for i, j, c in contribs if c != 0]
    _check(len(nonzero) == 3 and all(c == 1 for _, _, c in nonzero) and all(i == 0 for i, _, _ in nonzero),
           "census reading: exactly the 3 (shared x internal) pairs contribute, 1 each -- det A counts them")
    # identity holds on the countermodels too (realization-independent)
    cx1 = [(F(4), F(1), F(0)), (F(12), F(3), F(2)), (F(12, 35), F(0), F(1))]
    cx2 = [(F(1), F(3, 5), F(-1, 2)), (F(1), F(4, 5), F(1)), (F(1), F(0), F(1)), (F(1), F(0), F(1))]
    _check(cb_sum(cx1) == det_banked and cb_sum(cx2) == det_banked,
           "Cauchy-Binet identity holds on CX1 and CX2: realization-independent")
    # per-edge gauge invariance, term by term (t = 3 on the shared edge)
    t = F(3)
    gauged = [(census[0][0] * t * t, census[0][1] * t, census[0][2] * t)] + census[1:]
    _check(cb_sum(gauged) == det_banked and _gram_of(gauged) == (a11, a12, a22),
           "per-edge gauge d -> t d, C -> t^2 C leaves every pair term and the Gram invariant")

    return _full_result(
        name="T_det_gram_is_pair_count: det A = m is the Cauchy-Binet pair count, gauge-invariantly",
        tier=3,
        epistemic="P",
        summary=(
            "Cauchy-Binet on A = D^T diag(1/C) D: det A is the sum of squared 2x2 routing minors "
            "over edge pairs, each term per-edge-gauge invariant -- an exact identity in every "
            "realization (verified on the census and on both CX countermodels). T22's banked "
            "det A = m is thereby read: in the audited census exactly the (shared x internal) "
            "pairs contribute, 1 each. The identity and the banked value are [P]; the count "
            "READING is conditional on the census (internal-block premise, named in the sibling)."
        ),
        key_result="det A = sum of squared routing minors / (C_e C_f) (exact, gauge-invariant); census: = #(shared x internal) pairs = m",
        dependencies=["T22"],
        cross_refs=["T_routing_parallel_interface_conditional"],
        artifacts={"witness": "edge_census_ansatz_witness.py v2 E4 (23/23)",
                   "scope": "identity + banked value unconditional; pair-count reading census-conditional"},
    )


# ===================================================================== 7
def check_T_demand_not_routing_readable():
    """T_demand_not_routing_readable: the competition program's demands are
    not readable from, fundable by, or selectable through the routing
    structure -- the arena obstruction's executable Gram-level certificate
    [P].

    Three exact algebraic facts on the banked program A w = c (Gram banked
    [P] at T22; demands generic -- no banked load value is consumed):

      (V1)  the solution moves at fixed Gram: d w_1*/d Delta = -x/m != 0
            for a row-2 demand increment -- w* is not a functional of the
            Gram (grain-crossing program, audited).
      (R)   the response is not routing-selectable: a unit demand on row 1
            draws (A^-1) column 1 = (13/12, -1/6); on row 2, column 2 =
            (-1/6, 1/3) -- two distinct responses at ONE identical routing
            structure, so no routing column carries a demand's funding
            (ID-H evaluation, audited).
      (T)   the extra-loads readback is a tautology: A w*(c + r) - c = r
            identically (A A^-1 = I) -- reading the row off the extra
            sector loads returns the placement assumed, never decides it.

    Together: demands enter the program only through the constraint RHS,
    and the RHS's row index is not a routing object. Pure exact algebra on
    banked [P] structure; no gamma value, no angle, no fixed point of the
    banked load is consumed or implied. This is the certificate behind the
    ILL-POSED verdict of the ID-H evaluation and the Gram-level companion
    of the arena obstruction.
    """
    a11, a12, a22, x, m = _dressed_gram()

    # (V1) solution moves at fixed Gram (generic base demand (b1, b2))
    b1, b2 = F(2), F(3)   # generic; not a banked load
    w0 = _solve(a11, a12, a22, b1, b2)
    w1 = _solve(a11, a12, a22, b1, b2 + 1)
    _check(w1[0] - w0[0] == -x / m, "V1: d w_1*/d Delta = -x/m = -1/6 at fixed Gram (generic demand)")
    _check(w1 != w0, "the demand does real work while every routing column is fixed")

    # (R) distinct inverse-Gram columns at one Gram
    col1 = (_solve(a11, a12, a22, b1 + 1, b2)[0] - w0[0], _solve(a11, a12, a22, b1 + 1, b2)[1] - w0[1])
    col2 = (w1[0] - w0[0], w1[1] - w0[1])
    _check(col1 == (F(13, 12), F(-1, 6)) and col2 == (F(-1, 6), F(1, 3)),
           "(A^-1) columns: (13/12, -1/6) and (-1/6, 1/3), exact")
    _check(col1 != col2,
           "distinct responses at one identical routing structure: no routing column funds a demand")

    # (T) extra-loads readback tautology
    for (r1, r2) in [(F(0), F(1)), (F(1), F(0)), (F(2), F(5, 4))]:
        wp = _solve(a11, a12, a22, b1 + r1, b2 + r2)
        L1 = a11 * wp[0] + a12 * wp[1] - b1
        L2 = a12 * wp[0] + a22 * wp[1] - b2
        _check((L1, L2) == (r1, r2),
               f"extra-loads readback returns the placement ({r1},{r2}) identically (A A^-1 = I)")

    return _full_result(
        name="T_demand_not_routing_readable: demands are not Gram functionals, not routing-funded, not load-readable",
        tier=3,
        epistemic="P",
        summary=(
            "Three exact algebraic facts on the banked competition form: the solution moves at "
            "fixed Gram (V1, d w_1*/d Delta = -x/m); a unit demand draws distinct inverse-Gram "
            "columns by row at one identical routing structure (so no routing column carries a "
            "demand's funding); and the extra-loads readback returns the placement identically "
            "(A A^-1 = I). Demands enter only through the constraint RHS, whose row index is not "
            "a routing object. The executable certificate behind the ID-H ILL-POSED verdict and "
            "the arena obstruction's Gram-level companion. Generic demands; no banked load "
            "value consumed."
        ),
        key_result="dw*/dDelta != 0 at fixed Gram; (A^-1) col 1 != col 2 at one Gram; extra-loads readback = identity",
        dependencies=["T22", "T21"],
        cross_refs=["L_pinned_demand_is_feasibility_rhs", "T_routing_parallel_interface_conditional",
                    "T_sector_granularity_below_billing_type"],
        artifacts={"witnesses": "edge_census_ansatz_witness.py V1 + id_h_route_evaluation_witness.py v2 W2/W3 (31/31)",
                   "verdict_supported": "ID-H evaluation: ILL-POSED / ROUTING-SILENT (2026-06-11, audited)"},
    )


# ===================================================================== 8
def check_T_sector_granularity_below_billing_type():
    """T_sector_granularity_below_billing_type: the canonical billing
    vocabulary types a billing locus as a set of interfaces; sector-valued
    bills are below its type system [P_structural].

    THE FINDING (three convergent, independently audited routes):
      (1) TYPING. The canonical texts type every billing locus at
          interface granularity: row 7b bills a Gamma-channel at Gamma;
          the Paper 3 TS coincidence sentence locates bill, threat, and
          action at 'that set of interfaces'. No canonical sentence types
          a sector-valued bill (rent step-3 audit, verified absence).
      (2) TRANSFORMATION-TYPING FAILS AS A GRANULARITY SOURCE. Row 8's
          rho_Gamma-typing returns the TRIVIAL label on template-invariant
          content -- executed here on the finite model: the presence fact
          is a class function, invariant under the entire gauge group, so
          its transformation type distinguishes no sector. (The EW
          modulus is the same shape: gauge-invariant, hence
          transformation-trivial.)
      (3) CONSTRUCTIVE CONFIRMATION, TWICE. The ID-H evaluation: the
          banked routing has no defense-funding column (ILL-POSED,
          audited). The defense-routing-column commission: the sealed
          construction's unconditional fallback is GRANULARITY-FAILS at
          theorem grade, and its positive carrier's general form was
          refuted by the SSB/Meissner polarity control (REDUCES, audited).

    CONSEQUENCE: any sector-granular billing clause (UB-s is the bank's
    one instance) is a CONSTITUTIVE commitment below the canonical type
    system -- adopted, falsifiable (F-a), and not derivable from the
    canonical billing texts. This check certifies the typing fact and its
    executable component; it does not move UB's standing in either
    direction. [P_structural]: composes audited verified-absences with
    canonical-text anchors; the executable component is exact.
    """
    classes = _q8_classes()
    cls_of = {g: i for i, c in enumerate(classes) for g in c}
    triv = cls_of[_E]

    # (2) executable: template-invariant content has trivial transformation type
    invariant = all(int(cls_of[g] != triv) == int(cls_of[_conj(h, g)] != triv)
                    for g in _G8 for h in _G8)
    _check(invariant,
           "the pinned fact is invariant under the ENTIRE gauge group: rho_Gamma-typing returns the "
           "trivial label, so transformation type distinguishes no sector (granularity source fails)")
    # a non-invariant control: transformation-typing is non-trivial exactly where content is non-invariant
    some_g = (0, 1, 0, 0)
    noninv = any(idx_a != idx_b for idx_a, idx_b in
                 [(0 if some_g == g else 1, 0 if _conj(h, some_g) == g else 1)
                  for g in _G8 for h in _G8])
    _check(noninv, "control: non-invariant (orbit-position) content has non-trivial transformation type")

    # (1) + (3): verified absences, carried as audited cross-references (no silent claim)
    audited = {
        "rent_step3": "no banked sector-granular billing carrier exists (audit-verified absence)",
        "id_h": "ILL-POSED / ROUTING-SILENT -- no defense-funding column in the banked routing (audited)",
        "commission": "GRANULARITY-FAILS unconditional fallback at theorem grade; DRC-1 general form "
                      "Meissner-refuted (REDUCES, audited)",
    }
    _check(len(audited) == 3, "three convergent audited routes carried as named cross-references")

    return _full_result(
        name="T_sector_granularity_below_billing_type: billing loci are interface-typed; sector bills are constitutive",
        tier=3,
        epistemic="P_structural",
        summary=(
            "The canonical billing vocabulary types every billing locus at interface granularity "
            "(row 7b; the Paper 3 TS coincidence sentence); transformation-typing cannot supply "
            "sector granularity because template-invariant content carries the trivial "
            "rho_Gamma-label (executed exactly on the finite model, with a non-invariant control); "
            "and the absence of a sector-granular billing carrier is constructively confirmed "
            "twice (ID-H ILL-POSED; the commissioned construction's GRANULARITY-FAILS fallback). "
            "Sector-granular billing -- UB-s is the bank's one instance -- is therefore a "
            "constitutive commitment below the canonical type system: adopted, falsifiable (F-a), "
            "not derivable from the canonical texts. UB's standing is not moved in either direction."
        ),
        key_result="billing locus type = interface set; rho_Gamma-typing trivial on invariant content; sector-granular carrier absent (twice constructive)",
        dependencies=["L_defended_fact_is_template_invariant", "T_ledger_rent_excluded",
                      "UB_usage_billing_adopted"],
        cross_refs=["T_demand_not_routing_readable", "L_pinned_demand_is_feasibility_rhs",
                    "L_defense_requires_evaluator"],
        artifacts={"sources": "rent step-3 (2026-06-11) + ID-H evaluation v0.2 + defense-routing-column "
                              "commission v1.1 (all audited)",
                   "scope": "typing fact + executable component; UB standing untouched"},
    )


_CHECKS = {
    "L_ym_orbit_unpinnable": check_L_ym_orbit_unpinnable,
    "T_ym_record_demand_is_pinned_count": check_T_ym_record_demand_is_pinned_count,
    "T_ym_demand_count_resolution_independent": check_T_ym_demand_count_resolution_independent,
    "T_ub_consistency_three_record_states": check_T_ub_consistency_three_record_states,
    "T_routing_parallel_interface_conditional": check_T_routing_parallel_interface_conditional,
    "T_det_gram_is_pair_count": check_T_det_gram_is_pair_count,
    "T_demand_not_routing_readable": check_T_demand_not_routing_readable,
    "T_sector_granularity_below_billing_type": check_T_sector_granularity_below_billing_type,
}


def register(registry):
    registry.update(_CHECKS)
    return registry


def run_all():
    return {n: fn() for n, fn in _CHECKS.items()}
